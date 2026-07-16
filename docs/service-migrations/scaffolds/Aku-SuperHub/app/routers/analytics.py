from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Query, status

from app.schemas.analytics import AnalyticsBatch, BatchIngestResult, RegionalSummary

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


# ---------------------------------------------------------------------------
# Stub helpers — replace with real DB / warehouse calls in production
# ---------------------------------------------------------------------------


def _batch_upsert_events(batch: AnalyticsBatch) -> BatchIngestResult:
    """
    Persist events to the analytics store, skipping duplicates by event_id.
    Returns a result summary including counts of inserted / duplicate events.
    """
    raise NotImplementedError("Replace with real data-access layer")


def _compute_regional_summary(window_start: datetime, window_end: datetime) -> RegionalSummary:
    """Aggregate stored events within the given time window and return summary stats."""
    raise NotImplementedError("Replace with real aggregation query")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "/aggregate",
    response_model=BatchIngestResult,
    status_code=status.HTTP_200_OK,
    summary="Ingest analytics events from Edge Hubs",
    description=(
        "Accept a batch of analytics events forwarded by Edge Hub devices. "
        "Events are upserted; duplicates (matched on event_id) are silently skipped. "
        "Batch size is capped at 1 000 events per request."
    ),
)
async def aggregate_analytics(batch: AnalyticsBatch) -> BatchIngestResult:
    return _batch_upsert_events(batch)


@router.get(
    "/summary",
    response_model=RegionalSummary,
    summary="Regional analytics summary",
    description=(
        "Return aggregated analytics for the SuperHub's region over the requested "
        "time window (defaults to the last 24 hours). Metrics include total learners, "
        "sessions, content views, assessments, and average session duration."
    ),
)
async def get_analytics_summary(
    window_hours: int = Query(
        default=24,
        ge=1,
        le=720,
        description="Aggregation window size in hours (max 720 = 30 days)",
    ),
) -> RegionalSummary:
    window_end = datetime.utcnow()
    window_start = window_end - timedelta(hours=window_hours)
    return _compute_regional_summary(window_start, window_end)
