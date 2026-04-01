"""Pydantic v2 schemas for edge hub domain models."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class OperatingMode(StrEnum):
    online = "online"
    offline = "offline"


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class OfflineHealthResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: str = "ok"
    mode: OperatingMode
    db_reachable: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


class CacheStatusResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    item_count: int = Field(..., description="Number of cached content records")
    last_sync_at: datetime | None = Field(None, description="UTC timestamp of last successful sync")
    disk_usage_bytes: int = Field(..., description="Approximate SQLite file size in bytes")
    mode: OperatingMode


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


class SyncTriggerRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    force: bool = Field(False, description="Force full re-sync even if recently synced")
    scope: list[str] = Field(
        default_factory=list,
        description="Optional list of content topic IDs to sync; empty means all",
    )


class SyncTriggerResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    accepted: bool
    job_id: str | None = None
    message: str


# ---------------------------------------------------------------------------
# AI inference relay
# ---------------------------------------------------------------------------


class InferRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    prompt: str = Field(..., min_length=1, max_length=4096)
    max_tokens: int = Field(256, ge=1, le=2048)
    temperature: float = Field(0.7, ge=0.0, le=2.0)


class InferResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    text: str
    model: str
    finish_reason: str
    usage: dict[str, int]
