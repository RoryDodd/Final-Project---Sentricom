# app/schemas/zones.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ZoneLatest(BaseModel):
    timestamp: Optional[datetime]
    reading_id: Optional[int] = None
    zone_id: int
    zone_name: str
    dp_count: Optional[float]
    capacity: Optional[int]
    risk_status: Optional[str]
    confidence: Optional[float]
    zone_state: Optional[str]
    vuln_flag: Optional[bool] = None

    model_config = {"from_attributes": True}

class PrivacyZoneReadingIn(BaseModel):
    """
    Privatised zone data model from Priv Eng.

    Field names match current Priv Eng output to PUT
    """
    time: datetime
    zone_id: int = Field(..., ge=1)
    dp_count: float = Field(..., ge=0)
    risk_level: str = Field(..., min_length=1)
    event_type: Optional[str] = None
    vuln_flag: bool

    desnity: Optional[float] = None
    speed: Optional[float] = None
    confidence: Optional[float] = None
    zone_state: Optional[str] = None
    site_id: int = 1

    location_id: Optional[int] = None
    scenario_id: Optional[float] = None
    epsilon: Optional[float] = None
    mechanism: Optional[str] = None


class ZoneWriteResult(BaseModel):
    zone_id: Optional[int] = None
    status: str
    detail: Optional[str] = None

class ZoneBatchWriteResponse(BaseModel):
    processed: int
    inserted: int
    duplicates: int
    failed: int
    results: List[ZoneWriteResult]

class ZoneUpdateItem(BaseModel):
    reading_id: int
    timestamp: datetime
    zone_id: int
    zone_name: str
    dp_count: Optional[float] = None
    capacity: Optional[int] = None
    risk_status: Optional[str] = None
    confidence: Optional[float] = None
    zone_state: Optional[str] = None

class ZoneUpdatesResponse(BaseModel):
    items: List[ZoneUpdateItem]
    next_cursor: int

