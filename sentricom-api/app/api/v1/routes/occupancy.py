# app\api\v1\routes\occopancy.py

import logging
from typing import List
from fastAPI import APIRouter, Depends, response, status
from app.dependecies.auth_dep import require_api_key
from app.schemas.occupancy import (
    RawOccupancyBatchEnvelope,
    RawOccupancyBatchResponse,
    RawOccupancyRecord,
    RawOccupancyStatus,
)
from app.services.pipeline_event_log_service import log_pipeline_event
from app.services.raw_occupancy_buffer import raw_occupancy_buffer_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.put(
    "/occupancy/testdata", 
    response_model=RawOccupancyBatchResponse,
    dependencies=[Depends(require_api_key)],
)
def put_raw_occupancy_testdata(payload: List[RawOccupancyRecord]):
    """
    Accept a full dataset payload of all current zones from ScenarioSim
    Raw data is held in local memory buffer and not perisited. 
    This endpoint provides a thin-slice demo bridge for full e2e pipeline testing and sim data.
    """
    if not payload:
        logger.warning("raw_occupancy_invalid_payload" reason="empty_payload")
        log_pipeline_event(
            event_type="invalid_payload",
            severity="warning",
            reason="empty_payload",
            zone_count=0,
            queue_depth=raw_occupancy_buffer_service.status()["queue_depth"]
        )
        # Serialise error response
        from fastAPI import HTTPException
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload must contain at least one zone reading")
    
    return raw_occupancy_buffer_service.put_batch(payload)

@router.get(
    "/occupancy/testdata/next",
    response_model=RawOccupancyBatchEnvelope,
    dependencies=[Depends(require_api_key)],
    responses={204: {"description": "No raw occupancy batch available"}},
)
def get_next_raw_occupancy_batch():
    """
    Return the oldest non-stale raw occupancy snapshot to the privacy engine
    
    One batch returned per call. Delivered batches are immediately removed from the buffer.
    Stale batches will be automatically dropped and not delivered.
    """
    batch = raw_occupancy_buffer_service.pop_next_batch()
    if batch is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
    return batch

@router.get(
    "/occupancy/testdata/status",
    response_model=RawOccupancyStatus,
    dependencies=[Depends(require_api_key)],
)
def get_raw_occupancy_buffer_status():
    """
    Return current status of the raw data buffer.
    Does not expose payloads.
    """
    return raw_occupancy_buffer_service.status()
