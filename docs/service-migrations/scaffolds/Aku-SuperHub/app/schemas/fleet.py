from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HubStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"


class HubHealthMetrics(BaseModel):
    model_config = ConfigDict(frozen=True)

    cpu_percent: float = Field(..., ge=0.0, le=100.0, description="CPU utilisation %")
    memory_percent: float = Field(..., ge=0.0, le=100.0, description="Memory utilisation %")
    disk_percent: float = Field(..., ge=0.0, le=100.0, description="Disk utilisation %")
    active_learners: int = Field(..., ge=0, description="Learners currently active on hub")
    uptime_seconds: int = Field(..., ge=0, description="Hub process uptime in seconds")


class EdgeHub(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hub_id: UUID = Field(..., description="Unique hub identifier")
    region: str = Field(
        ..., min_length=1, max_length=64, description="Region code (e.g. 'us-east-1')"
    )
    name: str = Field(..., min_length=1, max_length=128, description="Human-readable hub name")
    status: HubStatus
    ip_address: str = Field(..., description="Hub IP address or hostname")
    firmware_version: str = Field(..., description="Semantic version string of hub firmware")
    last_seen_at: datetime | None = Field(
        default=None, description="Last heartbeat timestamp (UTC)"
    )
    registered_at: datetime = Field(..., description="Hub registration timestamp (UTC)")
    tags: dict[str, str] = Field(default_factory=dict, description="Arbitrary key/value labels")


class EdgeHubHealth(BaseModel):
    model_config = ConfigDict(frozen=True)

    hub_id: UUID
    status: HubStatus
    metrics: HubHealthMetrics
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    alerts: list[str] = Field(default_factory=list, description="Active alert messages, if any")


class PaginatedHubs(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[EdgeHub]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    pages: int = Field(..., ge=0)
