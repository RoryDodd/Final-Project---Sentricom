# app/schemas/zones.py
from pydantic import BaseModel
from datetime import datetime

class ZoneLatest(BaseModel):
    timestamp: datetime
    zone_id: int
    zone_name: str
    dp_count: int
    capacity: int
    risk_status: str