# app/schemas/zones.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ZoneLatest(BaseModel):
    timestamp: Optional[datetime]
    zone_id: int
    zone_name: str
    dp_count: Optional[float]
    capacity: Optional[int]
    risk_status: Optional[str]
    confidence: Optional[float]
    zone_state: Optional[str]

    model_config = {"from_attributes": True}