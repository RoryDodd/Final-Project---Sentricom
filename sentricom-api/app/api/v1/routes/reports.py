# app/api/v1/routes/reports.py

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.session_dep import require_session
from app.db.connection import fetch_all

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/occupancy/history", dependencies=[Depends(require_session)])
def get_occupancy_history(
    zone_id: Optional[int] = None,
    from_timestamp: Optional[datetime] = None,
    to_timestamp: Optional[datetime] = None,
    limit: int = 500,
):
    """
    Get historical occupancy readings for a specific zone or all zones, with optional time range filtering.

    - zone_id: Filter by specific zone ID (optional)
    - timestamp range: from_timestamp and to_timestamp (optional, ISO 8601 format)
    - zone_id + timestamp range can be combined for more specific filtering
    """

    # input validation
    if from_timestamp and to_timestamp and from_timestamp > to_timestamp:
        raise HTTPException(status_code=400, detail="from_timestamp must be before to_timestamp")
    
    safe_limit = max(1, min(limit, 5000)) # Throttle limit to manage excessive load

    # Dynamic clause variable declaration and population
    where_clauses = []
    params = []

    if zone_id is not None:
        where_clauses.append("z.zone_id = ?")
        params.append(zone_id)
    if from_timestamp is not None:
        where_clauses.append("r.timestamp >= ?")
        params.append(from_timestamp.isoformat())
    if to_timestamp is not None:
        where_clauses.append("r.timestamp <= ?")
        params.append(to_timestamp.isoformat())

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT 
            r.reading_id,
            z.zone_id,
            z.zone_name,
            z.capacity,
            z,risk_status,
            r.site_id,
            r.noisy_count AS dp_count,
            r.confidence,
            r.zone_state,
            r.vuln_flag,
            r.timestamp
        FROM occupancy_readings r
        JOIN zones z
            ON r.zone_id = z.zone_id
        {where_sql}
        ORDER BY r.timestamp ASC, r.reading_id ASC
        LIMIT ?
    """

    params.append(safe_limit)

    rows = fetch_all(sql, tuple(params))

    return {
        "items": [
            {
                "reading_id": r["reading_id"],
                "timestamp": r["timestamp"],
                "zone_id": r["zone_id"],
                "zone_name": r["zone_name"],
                "site_id": r["site_id"],
                "dp_count": r["dp_count"],
                "capacity": r["capacity"],
                "risk_status": r["risk_status"],
                "confidence": r["confidence"],
                "zone_state": r["zone_state"],
                "vuln_flag": r["vuln_flag"],
            } 
            for r in rows
        ],
        "count": len(rows),
        "limit": safe_limit,
    }