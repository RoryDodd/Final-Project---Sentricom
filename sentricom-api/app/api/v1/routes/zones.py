# app/api/v1/routes/zones.py

from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import require_api_key
from app.schemas.zones import ZoneLatest

router = APIRouter()

# Hardcoded datasets for test
# TODO - likely need also active, alarm_status, priority_persons, response_code fields for each zone
ZONES = [
    {
        "timestamp": "2026-04-23T11:00:04Z",
        "zone_id": 1,
        "zone_name": "Zone A",
        "dp_count": 42,
        "capacity": 100,
        "risk_status": "low"
    },
    {
        "timestamp": "2026-04-23T11:00:55Z",
        "zone_id": 2,
        "zone_name": "Zone B",
        "dp_count": 12,
        "capacity": 25,
        "risk_status": "low"
    },
    {
        "timestamp": "2026-04-23T11:01:03Z",
        "zone_id": 3,
        "zone_name": "Tuckshop",
        "dp_count": 65,
        "capacity": 130,
        "risk_status": "medium"
    },
    {
        "timestamp": "2026-04-23T11:01:13Z",
        "zone_id": 4,
        "zone_name": "Loading Zone",
        "dp_count": 3,
        "capacity": 20,
        "risk_status": "low"
    },
    {
        "timestamp": "2026-04-23T11:01:22Z",
        "zone_id": 5,
        "zone_name": "Zone E",
        "dp_count": 12,
        "capacity": 45,
        "risk_status": "high"
    },
    {
        "timestamp": "2026-04-23T11:02:00Z",
        "zone_id": 6,
        "zone_name": "Zone F",
        "dp_count": 2,
        "capacity": 30,
        "risk_status": "low"
    }
]

@router.get("/zones/latest", response_model=list[ZoneLatest])
#def get_all_latest_zones(auth=Depends(require_api_key)):
def get_all_latest_zones():
    """
    Get the latest occupancy data for all zones.
    """
    return ZONES

@router.get("/zones/latest/{zone_id}", response_model=ZoneLatest)
#def get_latest_zone(zone_id: int, auth=Depends(require_api_key)):
def get_latest_zone(zone_id: int):
    """Return the latest data for a single zone by ID"""
    for zone in ZONES:
        if zone["zone_id"] == zone_id:
            return zone
    raise HTTPException(status_code=404, detail="Zone not found")