# app/api/v1/routes/zones.py

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth_dep import require_api_key
from app.dependencies.session_dep import require_session
from app.db.connection import fetch_one, fetch_all, execute, execute_and_return
from app.schemas.zones import ZoneLatest


router = APIRouter()

# TODO - likely need also active, alarm_status, priority_persons, response_code fields for each zone
# check timestamp join logic to make sure our select aligns with latest reading for each table

# ----- Get /zones/latest (All)----- #
@router.get("/zones/latest", response_model=list[ZoneLatest], dependencies=[Depends(require_session)])
def get_all_latest_zones():
    """
    Get the latest occupancy data for all zones, with zone metadata.
    Risk field missing from db but this will be addressed once working
    """
    sql = """
        SELECT
            z.zone_id,
            z.zone_name,
            z.capacity,
            z.risk_status,
            r.noisy_count AS dp_count,
            r.confidence,
            r.zone_state,
            r.timestamp AS reading_timestamp
        FROM zones z
        LEFT JOIN occupancy_readings r
            ON r.reading_id = (
                SELECT reading_id
                FROM occupancy_readings r2
                WHERE zone_id = z.zone_id
                ORDER BY timestamp DESC
                LIMIT 1
            )
        ORDER BY z.zone_id
    """    
    rec = fetch_all(sql, ())
    result = []
    for r in rec:
        result.append({
            "timestamp": r.get("reading_timestamp"),
            "zone_id": r["zone_id"],
            "zone_name": r["zone_name"],
            "dp_count": r.get("dp_count"),
            "capacity": r.get("capacity"),
            "risk_status": r.get("risk_status"),
            "confidence": r.get("confidence"),
            "zone_state": r.get("zone_state")
        })
    return result

# ----- Get /zones/latest/{zone_id} (Single) ----- #
@router.get("/zones/latest/{zone_id}", response_model=ZoneLatest, dependencies=[Depends(require_session)])
#def get_latest_zone(zone_id: int, auth=Depends(require_api_key)):
def get_latest_zone(zone_id: int):
    """Return the latest data for a single zone by ID"""
    sql = """
        SELECT
            z.zone_id,
            z.zone_name,
            z.capacity,
            z.risk_status,
            r.noisy_count AS dp_count,
            r.confidence,
            r.zone_state,
            r.timestamp AS reading_timestamp
        FROM zones z
        LEFT JOIN occupancy_readings r
            ON r.reading_id = (
                SELECT reading_id
                FROM occupancy_readings r2
                WHERE zone_id = z.zone_id
                ORDER BY timestamp DESC
                LIMIT 1
            )
        WHERE z.zone_id = ?
        LIMIT 1;
    """
    rec = fetch_one(sql, (zone_id,))
    if not rec:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    return {
        "timestamp": rec.get("reading_timestamp"),
        "zone_id": rec["zone_id"],
        "zone_name": rec["zone_name"],
        "dp_count": rec.get("dp_count"),
        "capacity": rec.get("capacity"),
        "risk_status": rec.get("risk_status"),
        "confidence": rec.get("confidence"),
        "zone_state": rec.get("zone_state")
    }

# ----- PUT /zones/{zone_id} (Single) ----- #
@router.put("/zones/{zone_id}", dependencies=[Depends(require_api_key)])
def upsert_zone_reading(zone_id: int, payload: Dict[str, Any]):
    """
    Expected payload structure:
    - noisy_count: int (required)
    - confidence: float (optional)
    - zone_state: str (optional)
    - zone_name: str (optional)
    - capacity: int (optional)
    - risk_status: str (optional)
    - site_id int (optional, defaults to 1)
    """
    if "noisy_count" not in payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="noisy_count is required")
    
    zone_name = payload.get("zone_name")
    capacity = payload.get("capacity")
    risk_status = payload.get("risk_status")
    site_id = payload.get("site_id", 1)

    # 1) Validate zone exists (INSERT OR IGNORE)
    execute(
        """
        INSERT OR IGNORE INTO zones (zone_id, zone_name, capacity, risk_status)
        VALUES (?, ?, ?, ?)
        """,
        (zone_id, zone_name or f"Zone {zone_id}", capacity if capacity is not None else 0, risk_status or 'LOW RISK')
    )

    # 2) Update metadata fields if provided
    update_fields = []
    params = []

    if zone_name is not None:
        update_fields.append("zone_name = ?")
        params.append(zone_name)
    if capacity is not None:
        update_fields.append("capacity = ?")
        params.append(capacity)
    if risk_status is not None:
        update_fields.append("risk_status = ?")
        params.append(risk_status)

    if update_fields:
        params.append(zone_id)
        execute(
            f"UPDATE zones SET {', '.join(update_fields)} WHERE zone_id = ?",
            tuple(params)
        )

    # 3) Insert occupancy reading
    execute(
        """
        INSERT INTO occupancy_readings (zone_id, site_id, noisy_count, confidence, zone_sate, timestamp)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (
            zone_id,
            site_id,
            float(payload["noisy_count"]),
            payload.get("confidence"),
            payload.get("zone_state")
        )
    )

    return {"status" : "ok"}


# ----- PUT /zones/latest (Batch/Bulk) ----- #
@router.put("/zones/latest", dependencies=[Depends(require_api_key)])
def upsert_multiple_zone_readings(payload: List[Dict[str, Any]]):
    """
    Bulk ingestion endpoint.
    Expected payload structure:
    - zone_id: int (required)
    - noisy_count: int (required)
    - confidence: float (optional)
    - zone_state: str (optional)
    - zone_name: str (optional)
    - capacity: int (optional)
    - risk_status: str (optional)
    - site_id int (optional)
    """
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="Payload must be a list of zone records")
    
    results = []
    for record in payload:

        # Validate required fields
        if "zone_id" not in record:
            raise HTTPException(status_code=400, detail="Each record must include zone_id")
        if "noisy_count" not in record:
            raise HTTPException(status_code=400, detail="Each record must include noisy_count")
        
        zone_id = record["zone_id"]
        zone_name = record.get("zone_name")
        cpacity = record.get("capacity")
        risk_status = record.get("risk_status")
        site_id = record.get("site_id", 1)

        # 1) Validate zone exists (INSERT OR IGNORE)
        execute(
            """
            INSERT OR IGNORE INTO zones (zone_id, zone_name, capacity, risk_status)
            VALUES (?, ?, ?, ?)
            """,
            (
                zone_id, 
                zone_name or f"Zone {zone_id}", 
                capacity if capacity is not None else 0, 
                risk_status or 'LOW RISK'
            )
        )

        # 2) Update metadata if provided
        update_fields = []
        params = []

        if zone_name is not None:
            update_fields.append("zone_name = ?")
            params.append(zone_name)
        if capacity is not None:
            update_fields.append("capacity = ?")
            params.append(capacity)
        if risk_status is not None:
            update_fields.append("risk_status = ?")
            params.append(risk_status)

        if update_fields:
            params.append(zone_id)
            execute(
                f"UPDATE zones SET {', '.join(update_fields)} WHERE zone_id = ?",
                tuple(params)
            )

        # 3) Insert occupancy reading data
        execute_and_return(
            """
            INSERT INTO occupancy_readings (zone_id, site_id, noisy_count, confidence, zone_state, timestamp)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                zone_id,
                site_id,
                float(record["noisy_count"]),
                record.get("confidence"),
                record.get("zone_state")
            )
        )

        results.append({"zone_id": zone_id, "status": "ok"})

    return {"processed": len(results), "results": results}