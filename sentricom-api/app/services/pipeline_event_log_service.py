# app/services/pipeline_event_log_service.py

import logging
from typing import Optional
from app.db.connection import execute

logger = logging.getLogger(__name__)

MAX_PIPELINE_LOG_ROWS = 1000


def log_pipeline_event(
    event_type: str,
    severity: str = "info",
    reason: Optional[str] = None,
    batch_id: Optional[str] = None,
    zone_count: Optional[int] = None,
    age_seconds: Optional[float] = None,
    queue_depth: Optional[int] = None,
    validation_error: Optional[str] = None,
    problem_record: Optional[str] = None,
) -> None:
    """
    Persist a metadata-only API pipeline lifecycle event.
    Raw occupancy data must never be stored but batch processing events and states should be visible.
    """
    try:
        execute(
            """
            INSERT INTO pipeline_event_log (
                event_type,
                severity,
                reason,
                batch_id,
                zone_count,
                age_seconds,
                queue_depth,
                validation_error,
                problem_record
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_type,
                severity,
                reason,
                batch_id,
                zone_count,
                age_seconds,
                queue_depth,
                validation_error,
                problem_record,
            ),
        )

        execute(
            """
            DELETE FROM pipeline_event_log
            WHERE log_id NOT IN (
                SELECT log_id
                FROM pipeline_event_log
                ORDER BY log_id DESC
                LIMIT ?
            )
            """,
            (MAX_PIPELINE_LOG_ROWS,),
        )
    except Exception as exc:
        # Logging failure must not break the pipeline.
        logger.exception("Failed to write pipeline event log: %s", exc)