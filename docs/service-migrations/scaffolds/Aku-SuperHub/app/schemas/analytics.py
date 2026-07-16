from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    SESSION_START = "SESSION_START"
    SESSION_END = "SESSION_END"
    CONTENT_VIEW = "CONTENT_VIEW"
    ASSESSMENT_SUBMIT = "ASSESSMENT_SUBMIT"
    MODEL_INFERENCE = "MODEL_INFERENCE"


class AnalyticsEvent(BaseModel):
    """A single analytics event emitted by an Edge Hub."""

    model_config = ConfigDict(frozen=True)

    event_id: UUID = Field(..., description="Unique event identifier (set by Edge Hub)")
    hub_id: UUID = Field(..., description="Originating Edge Hub identifier")
    learner_id: UUID = Field(..., description="Anonymised learner identifier")
    event_type: EventType
    occurred_at: datetime = Field(..., description="Event timestamp in UTC (set by Edge Hub)")
    content_id: UUID | None = Field(
        default=None, description="Content item involved, if applicable"
    )
    session_id: UUID | None = Field(default=None, description="Session this event belongs to")
    duration_seconds: float | None = Field(
        default=None, ge=0.0, description="Duration, if applicable"
    )
    metadata: dict[str, str | int | float | bool] = Field(
        default_factory=dict, description="Additional event-specific key/value pairs"
    )


class AnalyticsBatch(BaseModel):
    """Batch of analytics events sent from one or more Edge Hubs."""

    model_config = ConfigDict(frozen=True)

    events: list[AnalyticsEvent] = Field(..., min_length=1, max_length=1000)


class BatchIngestResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    received: int = Field(..., ge=0, description="Total events in the batch")
    inserted: int = Field(..., ge=0, description="New events inserted")
    duplicates: int = Field(..., ge=0, description="Duplicate event_ids skipped")
    errors: int = Field(..., ge=0, description="Events that failed validation or write")
    ingested_at: datetime = Field(default_factory=datetime.utcnow)


class RegionalSummary(BaseModel):
    """Aggregated analytics summary for the SuperHub's region."""

    model_config = ConfigDict(frozen=True)

    region: str
    total_learners: int = Field(..., ge=0, description="Distinct learners with at least one event")
    total_sessions: int = Field(..., ge=0, description="Total completed sessions")
    total_content_views: int = Field(..., ge=0, description="Total CONTENT_VIEW events")
    total_assessments: int = Field(..., ge=0, description="Total ASSESSMENT_SUBMIT events")
    average_session_duration_seconds: float | None = Field(
        default=None, ge=0.0, description="Mean session duration; null if no sessions"
    )
    active_hubs: int = Field(..., ge=0, description="Hubs that reported events in the window")
    window_start: datetime = Field(..., description="Start of the aggregation window (UTC)")
    window_end: datetime = Field(..., description="End of the aggregation window (UTC)")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
