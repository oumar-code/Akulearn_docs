"""Content service: business logic, persistence stubs, and Redis caching."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

import redis.asyncio as aioredis

from app.schemas.content import (
    ContentCreate,
    ContentRead,
    ContentSyncResponse,
    ContentType,
    LessonRead,
)

logger = logging.getLogger(__name__)

_SYNC_CACHE_TTL_SECONDS = 30
_SYNC_CACHE_KEY_PREFIX = "akudemy:sync:"


# ---------------------------------------------------------------------------
# In-memory stub store (replace with real DB layer)
# ---------------------------------------------------------------------------

_CONTENT_STORE: dict[UUID, ContentRead] = {
    uuid4(): ContentRead(
        id=uuid4(),
        title="Introduction to Python",
        content_type=ContentType.VIDEO,
        language_code="en",
        description="Beginner Python programming video.",
        tags=["python", "beginner"],
        offline_available=True,
        size_bytes=524_288_000,
        lesson_id=None,
        asset_url="https://cdn.akulearn.example/intro-python.mp4",
        created_at=datetime(2024, 1, 10, tzinfo=timezone.utc),
        updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )
}

_LESSON_STORE: list[LessonRead] = [
    LessonRead(
        id=uuid4(),
        title="Python Fundamentals",
        subject="Computer Science",
        grade_level="Secondary",
        duration_minutes=60,
        is_published=True,
        content_count=3,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cache_key(since: datetime) -> str:
    return f"{_SYNC_CACHE_KEY_PREFIX}{since.isoformat()}"


def _items_since(since: datetime) -> list[ContentRead]:
    return [item for item in _CONTENT_STORE.values() if item.updated_at >= since]


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------


async def get_sync_delta(
    since: datetime,
    redis_client: aioredis.Redis | None,
) -> ContentSyncResponse:
    """Return all content items updated since *since*.

    Results are cached in Redis for :data:`_SYNC_CACHE_TTL_SECONDS` seconds to
    reduce latency for Edge Hub polling.
    """
    key = _cache_key(since)

    if redis_client is not None:
        try:
            cached = await redis_client.get(key)
            if cached:
                logger.debug("Cache hit for sync key %s", key)
                return ContentSyncResponse.model_validate_json(cached)
        except Exception:
            logger.warning("Redis read failed for key %s; falling through to DB", key, exc_info=True)

    items = _items_since(since)
    response = ContentSyncResponse(
        since=since,
        count=len(items),
        items=items,
        next_sync_token=datetime.now(tz=timezone.utc).isoformat(),
    )

    if redis_client is not None:
        try:
            await redis_client.setex(key, _SYNC_CACHE_TTL_SECONDS, response.model_dump_json())
        except Exception:
            logger.warning("Redis write failed for key %s", key, exc_info=True)

    return response


async def get_content_by_id(content_id: UUID) -> ContentRead | None:
    return _CONTENT_STORE.get(content_id)


async def upsert_content(payload: ContentCreate) -> ContentRead:
    now = datetime.now(tz=timezone.utc)
    item = ContentRead(
        id=uuid4(),
        **payload.model_dump(),
        created_at=now,
        updated_at=now,
    )
    _CONTENT_STORE[item.id] = item
    return item


async def list_lessons() -> list[LessonRead]:
    return _LESSON_STORE
