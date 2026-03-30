"""Edge-hub domain router — health, sync, cache, AI inference relay."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session_sqlite import get_db
from app.schemas.edge import (
    CacheStatusResponse,
    InferRequest,
    InferResponse,
    OfflineHealthResponse,
    OperatingMode,
    SyncTriggerRequest,
    SyncTriggerResponse,
)
from app.services import sync as sync_svc

router = APIRouter(prefix="/api/v1", tags=["edge"])


def _operating_mode() -> OperatingMode:
    return OperatingMode(settings.operating_mode)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@router.get(
    "/health/offline",
    response_model=OfflineHealthResponse,
    summary="Offline health check (no external calls)",
)
async def offline_health(db: AsyncSession = Depends(get_db)) -> OfflineHealthResponse:
    db_reachable = False
    try:
        await db.execute(text("SELECT 1"))
        db_reachable = True
    except Exception:
        pass

    return OfflineHealthResponse(
        status="ok",
        mode=_operating_mode(),
        db_reachable=db_reachable,
        timestamp=datetime.now(timezone.utc),
    )


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


@router.post(
    "/sync/trigger",
    response_model=SyncTriggerResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Push sync request to cloud (calls Akudemy)",
)
async def trigger_sync(body: SyncTriggerRequest) -> SyncTriggerResponse:
    result = await sync_svc.trigger_cloud_sync(force=body.force, scope=body.scope)
    return SyncTriggerResponse(**result)


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


@router.get(
    "/cache/status",
    response_model=CacheStatusResponse,
    summary="Local SQLite content cache status",
)
async def cache_status(db: AsyncSession = Depends(get_db)) -> CacheStatusResponse:
    # Item count — table may not exist yet on a fresh node
    try:
        row = await db.execute(text("SELECT COUNT(*) FROM content_cache"))
        item_count: int = row.scalar_one()
    except Exception:
        item_count = 0

    # Last sync timestamp
    last_sync_at: datetime | None = None
    try:
        row = await db.execute(
            text("SELECT MAX(synced_at) FROM content_cache")
        )
        value = row.scalar_one()
        if value:
            last_sync_at = datetime.fromisoformat(value)
    except Exception:
        pass

    # Disk usage
    db_path = Path(settings.database_url.replace("sqlite+aiosqlite:///", ""))
    disk_usage_bytes = db_path.stat().st_size if db_path.exists() else 0

    return CacheStatusResponse(
        item_count=item_count,
        last_sync_at=last_sync_at,
        disk_usage_bytes=disk_usage_bytes,
        mode=_operating_mode(),
    )


# ---------------------------------------------------------------------------
# AI inference relay
# ---------------------------------------------------------------------------


@router.post(
    "/ai/infer",
    response_model=InferResponse,
    summary="Local AI inference relay → AkuAI Gemma",
)
async def ai_infer(body: InferRequest) -> InferResponse:
    payload = {
        "prompt": body.prompt,
        "max_tokens": body.max_tokens,
        "temperature": body.temperature,
    }
    try:
        data = await sync_svc.relay_infer(payload)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"AkuAI upstream error: {exc.response.text[:300]}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AkuAI service unreachable — hub may be offline",
        ) from exc
    return InferResponse(**data)
