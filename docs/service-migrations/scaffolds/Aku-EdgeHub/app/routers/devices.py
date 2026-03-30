"""Devices router — registration and lookup against local SQLite store."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session_sqlite import get_db
from app.schemas.devices import (
    DeviceRecord,
    DeviceRegisterRequest,
    DeviceRegisterResponse,
    DeviceStatus,
)

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS devices (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id        TEXT NOT NULL UNIQUE,
    name             TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'pending',
    capabilities     TEXT NOT NULL DEFAULT '[]',
    metadata         TEXT NOT NULL DEFAULT '{}',
    registered_at    TEXT NOT NULL,
    last_seen_at     TEXT
)
"""


async def _ensure_table(db: AsyncSession) -> None:
    await db.execute(text(_CREATE_TABLE))
    await db.commit()


# ---------------------------------------------------------------------------
# POST /api/v1/devices/register
# ---------------------------------------------------------------------------


@router.post(
    "/register",
    response_model=DeviceRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new device (writes to SQLite)",
)
async def register_device(
    body: DeviceRegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> DeviceRegisterResponse:
    await _ensure_table(db)

    now = datetime.now(timezone.utc)

    existing = await db.execute(
        text("SELECT id FROM devices WHERE device_id = :did"),
        {"did": body.device_id},
    )
    if existing.first():
        # Idempotent: update last_seen and return existing record
        await db.execute(
            text("UPDATE devices SET last_seen_at = :ts WHERE device_id = :did"),
            {"ts": now.isoformat(), "did": body.device_id},
        )
        return DeviceRegisterResponse(
            device_id=body.device_id,
            status=DeviceStatus.active,
            registered_at=now,
            message="Device already registered — last_seen updated",
        )

    await db.execute(
        text(
            """
            INSERT INTO devices
                (device_id, name, firmware_version, status, capabilities, metadata, registered_at)
            VALUES
                (:device_id, :name, :fw, :status, :caps, :meta, :registered_at)
            """
        ),
        {
            "device_id": body.device_id,
            "name": body.name,
            "fw": body.firmware_version,
            "status": DeviceStatus.pending,
            "caps": json.dumps(body.capabilities),
            "meta": json.dumps(body.metadata),
            "registered_at": now.isoformat(),
        },
    )

    return DeviceRegisterResponse(
        device_id=body.device_id,
        status=DeviceStatus.pending,
        registered_at=now,
    )


# ---------------------------------------------------------------------------
# GET /api/v1/devices/{id}
# ---------------------------------------------------------------------------


@router.get(
    "/{device_id}",
    response_model=DeviceRecord,
    summary="Look up a registered device by device_id",
)
async def get_device(
    device_id: str,
    db: AsyncSession = Depends(get_db),
) -> DeviceRecord:
    await _ensure_table(db)

    row = await db.execute(
        text("SELECT * FROM devices WHERE device_id = :did"),
        {"did": device_id},
    )
    record = row.mappings().first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{device_id}' not found",
        )

    return DeviceRecord(
        id=record["id"],
        device_id=record["device_id"],
        name=record["name"],
        firmware_version=record["firmware_version"],
        status=DeviceStatus(record["status"]),
        capabilities=json.loads(record["capabilities"]),
        metadata=json.loads(record["metadata"]),
        registered_at=datetime.fromisoformat(record["registered_at"]),
        last_seen_at=(
            datetime.fromisoformat(record["last_seen_at"])
            if record["last_seen_at"]
            else None
        ),
    )
