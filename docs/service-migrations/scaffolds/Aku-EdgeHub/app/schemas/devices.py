"""Pydantic v2 schemas for device domain models."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DeviceStatus(StrEnum):
    active = "active"
    inactive = "inactive"
    pending = "pending"


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


class DeviceRegisterRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(..., min_length=1, max_length=128, description="Client-supplied unique device ID")
    name: str = Field(..., min_length=1, max_length=256)
    firmware_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    capabilities: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class DeviceRegisterResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str
    status: DeviceStatus
    registered_at: datetime
    message: str = "Device registered successfully"


# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------


class DeviceRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    device_id: str
    name: str
    firmware_version: str
    status: DeviceStatus
    capabilities: list[str]
    metadata: dict[str, str]
    registered_at: datetime
    last_seen_at: datetime | None = None
