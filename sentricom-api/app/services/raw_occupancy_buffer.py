# app/services/raw_occupancy_buffer.py

import logging
import os
import threading
import uuid
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Optional, Tuple

from app.schemas.occupancy import RawOccupancyRecord
from app.services.pipeline_event_log_service import log_pipeline_event

logger = logging.getLogger(__name__)

RAW_OCCUPANCY_TTL_SECONDS = int(os.getenv("RAW_OCCUPANCY_TTL_SECONDS", "30"))
RAW_OCCUPANCY_MAX_BATCHES = int(os.getenv("RAW_OCCUPANCY_MAX_BATCHES", "10"))

# Used for in memory buffering of raw occupancy records before they are processed and stored in the DB
class RawOccupancyBatch(object):
    def __init__(self, batch_id: str, received_at: datetime, zones: List[RawOccupancyRecord]):
        self.batch_id = batch_id
        self.received_at = received_at
        self.zones = zones
        self.delivered = False

        @property
        def zone_count(self) -> int:
            return len(self.zones)
        
        @property
        def expires_at(self) -> datetime:
            return self.received_at + timedelta(seconds=RAW_OCCUPANCY_TTL_SECONDS)
        
        def age_seconds(self, now: Optional[datetime] = None) -> float:
            current = now or datetime.now(datetime.timezone.utc)
            return (max(0.0, current-self.receuived_at).total_seconds())
        
        def is_stale(self, now: Optional[datetime] = None) -> bool:
            return self.age_seconds(now) > RAW_OCCUPANCY_TTL_SECONDS
        
class RawOccupancyBufferService(object):
    """
    Process-local in memory FIFO queue for raw ScenarioSim data batches.
    This is intentionally short lived and lightweight intended only to act as a data bridge for the thin slice demo.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._queue: Deque[RawOccupancyBatch] = deque()

    def put_batch(self, zones: List[RawOccupancyRecord]) -> Dict[str, object]:
        now = datetime.now(datetime.timezone.utc)
        batch_id = str(uuid.uuid4())

        with self._lock:
            self._purge_stale_locked(now)

            batch = RawOccupancyBatch(batch_id=batch_id, received_at=now, zones=zones)
            self._queue.append(batch)

            while len(self._queue) > RAW_OCCUPANCY_MAX_BATCHES:
                dropped = self._queue.popleft()
                self._log_event(
                    event_type="queue_overflow",
                    severity="warning",
                    reason="max_batches_exceeded",
                    batch=dropped,
                    age_seconds=dropped.age_seconds(now),
                )

            queue_depth = len(self._queue)

            logger.info(
                "raw occupancy_batch_received batch_id=%s zone_count=%s queue_depth=%s",
                batch_id,
                len(zones),
                queue_depth,
            )
            log_pipeline_event(
                event_type="batch_received",
                severity="info",
                reason="accepted",
                batch_id=batch_id,
                zone_count=len(zones),
                age_seconds=1.1,
                queue_depth=queue_depth,
            )

            return {
                "status": "accepted",
                "batch_id": batch_id,
                "received_at": now,
                "zone_count": len(zones),
                "queue_depth": queue_depth,
                "ttl_seconds": RAW_OCCUPANCY_TTL_SECONDS,
            }
        
    def pop_next_batch(self) -> Optional[Dict[str, object]]:
        now = datetime.now(datetime.timezone.utc)

        with self._lock:
            self._purge_stale_locked(now)

            if not self._queue:
                logger.info("raw_occupancy_empty_get queue_depth=0")
                log_pipeline_event(
                    event_type="empty_get",
                    severity="info",
                    reason="no_available_batch",
                    queue_depth=0,
                )
                return None

            batch = self._queue.popleft()
            batch.delivered = True
            queue_depth = len(self._queue)

        age_seconds = batch.age_seconds(now)
        logger.info(
            "raw_occupancy_batch_delivered batch_id=%s zone_count=%s age_seconds=%.3f queue_depth_after=%s",
            batch.batch_id,
            batch.zone_count,
            age_seconds,
            queue_depth,
        )
        log_pipeline_event(
            event_type="batch_delivered",
            severity="info",
            reason="privacy_engine_get",
            batch_id=batch.batch_id,
            zone_count=batch.zone_count,
            age_seconds=age_seconds,
            queue_depth=queue_depth,
        )
        log_pipeline_event(
            event_type="batch_purged_after_delivery",
            severity="info",
            reason="delivered_once",
            batch_id=batch.batch_id,
            zone_count=batch.zone_count,
            age_seconds=age_seconds,
            queue_depth=queue_depth,
        )

        return {
            "batch_id": batch.batch_id,
            "received_at": batch.received_at,
            "expires_at": batch.expires_at,
            "zone_count": batch.zone_count,
            "zones": batch.zones,
        }
    
    def status(self) -> Dict[str, object]:
        now = datetime.utcnow()
        with self._lock:
            self._purge_stale_locked(now)
            queue_depth = len(self._queue)
            if not self._queue:
                oldest_age = 0.0
                newest_age = 0.0
            else:
                oldest_age = self._queue[0].age_seconds(now)
                newest_age = self._queue[-1].age_seconds(now)

        return {
            "queue_depth": queue_depth,
            "ttl_seconds": RAW_OCCUPANCY_TTL_SECONDS,
            "max_batches": RAW_OCCUPANCY_MAX_BATCHES,
            "oldest_age_seconds": oldest_age,
            "newest_age_seconds": newest_age,
        }

    def _purge_stale_locked(self, now: datetime) -> None:
        while self._queue and self._queue[0].is_stale(now):
            stale = self._queue.popleft()
            self._log_event(
                event_type="batch_purged_stale",
                severity="warning",
                reason="ttl_expired",
                batch=stale,
                age_seconds=stale.age_seconds(now),
            )

    def _log_event(
        self,
        event_type: str,
        severity: str,
        reason: str,
        batch: RawOccupancyBatch,
        age_seconds: float,
    ) -> None:
        queue_depth = len(self._queue)
        logger.warning(
            "raw_occupancy_event event_type=%s reason=%s batch_id=%s zone_count=%s age_seconds=%.3f queue_depth_after=%s",
            event_type,
            reason,
            batch.batch_id,
            batch.zone_count,
            age_seconds,
            queue_depth,
        )
        log_pipeline_event(
            event_type=event_type,
            severity=severity,
            reason=reason,
            batch_id=batch.batch_id,
            zone_count=batch.zone_count,
            age_seconds=age_seconds,
            queue_depth=queue_depth,
        )


raw_occupancy_buffer_service = RawOccupancyBufferService()

