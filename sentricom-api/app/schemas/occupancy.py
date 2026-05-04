# app/chemas/occupancy.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


#TODO - fix typo - vuln_flag not vuld_flag
#vuln flag as a string 
class RawOccupancyRecord(BaseModel):
    """
    Represents structure of non-privatised zone occupancy record from ScenarioSim.

    - Buffer for in memory transport only.
    - Records using this schema must never be persisted as the raw data may contain PII.
    """
    timestamp: datetime
    zone_id: int = Field(..., ge=1)
    zone_name: str = Field(..., min_length=1)
    real_count: int = Field(..., ge=0)
    risk_status: str = Field(..., min_length=1)
    event: Optional[str] = None
    vuln_flag: bool

    @validator("zone_name", "risk_status")
    def non_empty_str(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value
    
class RawOccupancyBatchResponse(BaseModel):
    status: str
    batch_id: str
    received_at: datetime
    zone_count: int
    queue_depth: int
    ttl_seconds: int

class RawOccupancyBatchEnvelope(BaseModel):
    """
    Represents data returned to PrivacyEngine by GET /occoupancy/testdata/next endpoint.
    """
    
    batch_id: str
    received_at: datetime
    expires_at: datetime
    zone_count: int
    zones: List[RawOccupancyRecord]
    
class RawOccupancyStatus(BaseModel):
    queue_depth: int
    ttl_seconds: int
    max_batches: int
    oldest_age_seconds: float
    newest_age_seconds: float
