"""Content router — offline-sync and CRUD endpoints."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from uuid import UUID

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.content import (
    ContentCreate,
    ContentRead,
    ContentSyncResponse,
    LessonRead,
)
from app.services import content as content_svc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["content"])


# ---------------------------------------------------------------------------
# Redis dependency (override in tests / production wiring)
# ---------------------------------------------------------------------------


async def get_redis() -> aioredis.Redis | None:  # pragma: no cover
    """Return an async Redis client, or None if REDIS_URL is not configured."""
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        logger.warning("REDIS_URL not set; Redis cache disabled for this request.")
        return None
    return aioredis.from_url(redis_url, decode_responses=True)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/content/sync",
    response_model=ContentSyncResponse,
    summary="Offline content sync (Edge Hub)",
    description=(
        "Returns all content items updated since the given timestamp. "
        "Results are served from a short-lived Redis cache to minimise "
        "latency for Edge Hub polling."
    ),
)
async def sync_content(
    since: datetime = Query(
        default=...,
        description="ISO-8601 timestamp; return items updated after this point.",
        example="2024-01-01T00:00:00Z",
    ),
    redis: aioredis.Redis | None = Depends(get_redis),
) -> ContentSyncResponse:
    since_utc = since.replace(tzinfo=timezone.utc) if since.tzinfo is None else since
    return await content_svc.get_sync_delta(since=since_utc, redis_client=redis)


@router.get(
    "/content/{content_id}",
    response_model=ContentRead,
    summary="Fetch a single content item",
)
async def get_content(content_id: UUID) -> ContentRead:
    item = await content_svc.get_content_by_id(content_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content {content_id} not found.",
        )
    return item


@router.post(
    "/content",
    response_model=ContentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update a content item (admin)",
)
async def create_content(payload: ContentCreate) -> ContentRead:
    return await content_svc.upsert_content(payload)


@router.get(
    "/lessons",
    response_model=list[LessonRead],
    summary="Lesson catalogue",
)
async def list_lessons() -> list[LessonRead]:
    return await content_svc.list_lessons()
