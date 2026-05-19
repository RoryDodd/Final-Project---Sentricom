# app/api/v1/routes/zones.py

import json
import sqlite3
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth_dep import require_api_key
from app.dependencies.session_dep import require_session
from app.db.connection import fetch_one, fetch_all, execute, execute_and_return
from app.schemas.zones import (
    ZoneLatest,
    PrivacyZoneReadingIn,
    ZoneBatchWriteResponse,
    ZoneUpdatesResponse,
)
from app.services.pipeline_event_log_service import log_pipeline_event
from pydantic import ValidationError



router = APIRouter()

# TODO - likely need also active, alarm_status, priority_persons, response_code fields for each zone
# check timestamp join logic to make sure our select aligns with latest reading for each table

def _write_privacy_zone_reading(record: PrivacyZoneReadingIn) -> dict:
    """
    Write one privatised Priv eng zone record

    - use provider timestamp
    - zone config is source of truth (except risk status which can be updated by priv eng)
    - duplicate zone_id + timestamp is ignored
    - event_type writes to events when present
    - vuln_flag writes to vulnerable_tracking when true
    """

    provider_timestamp = record.time.isoformat()

    zone = fetch_one(
        "SELECT zone_id FROM zones WHERE zone_id = ?",
        (record.zone_id,)
    )

    if not zone:
        return {
            "zone_id": record.zone_id,
            "status": "failed",
            "detail": "zone_id not in zones config"
        }
    
    duplicate = fetch_one(
        """
        SELECT reading_id 
        FROM occupancy_readings
        WHERE zone_id = ?
            AND timestamp = ?
        LIMIT 1
        """,
        (record.zone_id, provider_timestamp)
    )
    
    if duplicate:
        return {
            "zone_id": record.zone_id,
            "status": "duplicate_ignored",
            "detail": f"reading already exists for this zone_id + timestamp ({record.zone_id}, {record.time})",
        }
    
    if record.risk_level is not None:
        execute(
            """
            UPDATE zones
            SET risk_status = ?
            WHERE zone_id = ?
            """,
            (record.risk_level, record.zone_id),
        )

    execute_and_return(
        """
        INSERT INTO occupancy_readings (
            zone_id,
            site_id,
            noisy_count,
            confidence,
            zone_state,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            record.zone_id,
            record.site_id,
            float(record.dp_count),
            record.confidence,
            record.zone_state,
            provider_timestamp,
        ),
    )

    if record.event_type:
        execute(
            """
            INSERT INTO events (
                zone_id,
                event_type,
                description,
                severity,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                record.zone_id,
                record.event_type,
                f"Event detail: {record.event_type}",
                "info",
                provider_timestamp,
            ),
        )

    # Vulnerable flag will require logic on movement chain to identify from/to zones
    # Will need some refactoring after inital testing
    if record.vuln_flag:
        execute(
            """
            INSERT INTO vulnerable_tracking (
                zone_from,
                zone_to,
                vulnerable_type,
                estimated_count,
                passed_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                None,
                record.zone_id,
                "vulnerability_flagged",
                None,
                provider_timestamp,
            ),
        )

    return {
        "zone_id": record.zone_id,
        "status": "inserted",
        "detail": None,
    }

# ----- Get /zones/latest (All)----- #
@router.get("/zones/latest", response_model=list[ZoneLatest], dependencies=[Depends(require_session)])
def get_all_latest_zones():
    """
    Get the latest occupancy data for all zones, with zone metadata.
    Risk field missing from db but this will be addressed once working
    """
    sql = """
        SELECT
            r.reading_id,
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
                WHERE r2.zone_id = z.zone_id
                ORDER BY timestamp DESC
                LIMIT 1
            )
        ORDER BY z.zone_id
    """    
    rec = fetch_all(sql, ())
    result = []
    for r in rec:
        result.append({
            "reading_id": r.get("reading_id"),
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

# ----- Get /zones/updates (Cursor tracked append batch) ----- #
@router.get("/zones/updates", response_model=ZoneUpdatesResponse, dependencies=[Depends(require_session)])
def get_zone_updates(after_reading_id: int = 0, limit: int = 100):
    """
    Return append-log style zone updates newer than after_reading_id.
    Return zone updates using append that are newer than provided reading_id cursor, ordered by reading_id ascending.

    This endpoint is for client delta polling. It does not track delivery
    Enables client delat polling and does not track a delivery state
    server-side; the client is responisble for tracking its cursor..
    """
    safe_limit = max(1, min(limit, 1000))

    sql = """
        SELECT
            r.reading_id,
            r.zone_id,
            z.zone_name,
            z.capacity,
            z.risk_status,
            r.noisy_count AS dp_count,
            r.confidence,
            r.zone_state,
            r.timestamp AS reading_timestamp
        FROM occupancy_readings r
        JOIN zones z
            ON z.zone_id = r.zone_id
        WHERE r.reading_id > ?
        ORDER BY r.reading_id ASC
        LIMIT ?
    """

    rows = fetch_all(sql, (after_reading_id, safe_limit))

    items = []
    for r in rows:
        items.append({
            "reading_id": r["reading_id"],
            "timestamp": r.get("reading_timestamp"),
            "zone_id": r["zone_id"],
            "zone_name": r["zone_name"],
            "dp_count": r.get("dp_count"),
            "capacity": r.get("capacity"),
            "risk_status": r.get("risk_status"),
            "confidence": r.get("confidence"),
            "zone_state": r.get("zone_state"),
        })

    next_cursor = items[-1]["reading_id"] if items else after_reading_id

    return {
        "items": items,
        "next_cursor": next_cursor,
    }

# ----- Get /zones/latest/{zone_id} (Single) ----- #
@router.get("/zones/latest/{zone_id}", response_model=ZoneLatest, dependencies=[Depends(require_session)])
def get_latest_zone(zone_id: int):
    """Return the latest data for a single zone by ID"""
    sql = """
        SELECT
            r.reading_id,
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
                WHERE r2.zone_id = z.zone_id
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
        "reading_id": rec.get("reading_id"),
        "timestamp": rec.get("reading_timestamp"),
        "zone_id": rec["zone_id"],
        "zone_name": rec["zone_name"],
        "dp_count": rec.get("dp_count"),
        "capacity": rec.get("capacity"),
        "risk_status": rec.get("risk_status"),
        "confidence": rec.get("confidence"),
        "zone_state": rec.get("zone_state")
    }

# ----- PUT /zones/latest (Batch/Bulk) ----- #
@router.put(
        "/zones/latest",
        response_model=ZoneBatchWriteResponse,
        dependencies=[Depends(require_api_key)]
)
#def upsert_multiple_zone_readings(payload: List[Dict[str, Any]]):
def upsert_multiple_zone_readings(payload: List[dict]):
    """
    Ingest batch of privatised zone readings with metadata updates.

    Partial success behaviour:
    - valid records are inserted
    - duplicate records are ignored
    - invalid records are skipped and logged
    """

    processed = 0
    inserted = 0
    duplicates = 0
    failed = 0
    results = []

    # for loop to update
    for raw_record in payload:
        processed += 1

        try:
            #record = PrivacyZoneReadingIn.model_validate(raw_record) #pydantic v2 only
            record = PrivacyZoneReadingIn(**raw_record) #pydantic v1 and v2
            result = _write_privacy_zone_reading(record)

            if result["status"] == "inserted":
                inserted += 1
            elif result["status"] == "duplicate_ignored":
                duplicates += 1
            else:
                failed += 1
                log_pipeline_event(
                    event_type="privacy_zone_reading_batch_record_update_failed",
                    severity="warning",
                    reason="record_write_failed",
                    validation_error=result.get("detail"),
                    problem_record=json.dumps(raw_record, default=str),
                )
        
            results.append(result)

        except ValidationError as e:
            failed += 1

            zone_id = raw_record.get("zone_id") if isinstance(raw_record, dict) else None

            log_pipeline_event(
                event_type="privacy_zone_reading_batch_validation_failed",
                severity="warning",
                reason="pydantic_validation_error",
                validation_error=str(e),
                problem_record=json.dumps(raw_record, default=str),
            )

            results.append({
                "zone_id": zone_id,
                "status": "failed",
                "detail": str(e)
            })

        except sqlite3.IntegrityError as e:
            zone_id = raw_record.get("zone_id") if isinstance(raw_record, dict) else None

            # fallback duplicate logic
            error_text = str(e)

            if (
                "UNIQUE constraint failed" in error_text
                or "occupancy_readings.zone_id" in error_text
                or "occupancy_readings.timestamp" in error_text
            ):
                duplicates += 1

                results.append({
                    "zone_id": zone_id,
                    "status": "duplicate_ignored",
                    "detail": f"reading already exists for this zone_id + timestamp ({zone_id}, {record.time})",
                })

                continue

            failed += 1

            log_pipeline_event(
                event_type="privacy_zone_reading_batch_record_update_failed",
                severity="warning",
                reason="sqlite_integrity_error",
                validation_error=str(e),
                problem_record=json.dumps(raw_record, default=str),
            )

            results.append({
                "zone_id": zone_id,
                "status": "failed",
                "detail": "Database integrity error while writing record",
            })

        except Exception as e:
            failed += 1

            zone_id = raw_record.get("zone_id") if isinstance(raw_record, dict) else None

            log_pipeline_event(
                event_type="privacy_zone_reading_batch_record_update_failed",
                severity="critical",
                reason="unexpected_error",
                validation_error=str(e),
                problem_record=json.dumps(raw_record, default=str),
            )

            results.append({
                "zone_id": zone_id,
                "status": "failed",
                #"detail": "Unexpected error while writing record",
                "detail": str(e),
            })

    return {
        "processed": processed,
        "inserted": inserted,
        "duplicates": duplicates,
        "failed": failed,
        "results": results,
    }

# ----- PUT /zones/{zone_id} (Single) ----- #
@router.put("/zones/{zone_id}", dependencies=[Depends(require_api_key)])
def upsert_zone_reading(zone_id: int, payload: PrivacyZoneReadingIn):
    """
    Ingest single privatised zone reading with metadata updates.

    Reading timestamp is preserved
    DB zone config is configured bu risk status is updated by priv eng if provided
    Duplicate zone_id + timestamp will be ignored
    """
    
    if payload.zone_id != zone_id:
        log_pipeline_event(
            event_type="priv_zone_data_write_validation_failure",
            severity="warning",
            reason="zone_id_mismatch",
            validation_error=f"path zone_id={zone_id}, payload zone_id={payload.zone_id}",
            problem_record=payload.model_dump_json(), #should work in pydantic v1 and v2
            # problem_record=payload.json(), #pydantic v1 syntax 
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path zone_id must match payload zone_id."
        )
    
    try:
        result = _write_privacy_zone_reading(payload)

    except sqlite3.IntegrityError as e:
        log_pipeline_event(
            event_type="priv_zone_data_write_validation_failure",
            severity="warning",
            reason="sqlite_integrity_error",
            validation_error=str(e),
            problem_record=payload.model_dump_json(), #should work in pydantic v1 and v2
            # problem_record=payload.json(), #pydantic v1 syntax
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database integrity error while writing zone data.",
        )
    
    except Exception as e:
        log_pipeline_event(
            event_type="priv_zone_data_write_failed",
            severity="critical",
            reason="unexpected_error",
            validation_error=str(e),
            problem_record=payload.model_dump_json(), #should work in pydantic v1 and v2
            # problem_record=payload.json(), #pydantic v1 syntax
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while writing zone reading.",
        )
    
    if result["status"] == "failed":
        log_pipeline_event(
            event_type="priv_zone_data_write_validation_failure",
            severity="warning",
            reason="invalid_zone_record",
            validation_error=result["detail"],
            problem_record=payload.model_dump_json(), #should work in pydantic v1 and v2
            # problem_record=payload.json(), #pydantic v1 syntax
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["detail"],
        )
    
    return result

