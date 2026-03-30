"""Context router — manage per-user contextual memory backed by Redis."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Annotated

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.schemas.workflows import ContextRead, ContextUpdate

router = APIRouter(prefix="/api/v1/context", tags=["Context"])


# ---------------------------------------------------------------------------
# Dependency helpers
# ---------------------------------------------------------------------------


def get_redis(request: Request) -> aioredis.Redis:
    """Retrieve the shared Redis client from app state."""
    return request.app.state.redis


RedisDep = Annotated[aioredis.Redis, Depends(get_redis)]

_CONTEXT_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 days


def _context_key(user_id: str) -> str:
    return f"context:{user_id}"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get(
    "/{user_id}",
    response_model=ContextRead,
    summary="Retrieve contextual memory for a user",
)
async def get_context(user_id: str, redis: RedisDep) -> ContextRead:
    """Fetch all key/value context entries stored for *user_id*.

    Returns an empty ``data`` dict when no context has been saved yet.
    """
    raw: dict[bytes, bytes] = await redis.hgetall(_context_key(user_id))
    data: dict[str, object] = {}
    updated_at: datetime | None = None

    for field, value in raw.items():
        field_str = field.decode() if isinstance(field, bytes) else field
        value_str = value.decode() if isinstance(value, bytes) else value

        if field_str == "__updated_at__":
            try:
                updated_at = datetime.fromisoformat(value_str)
            except ValueError:
                pass
            continue

        try:
            data[field_str] = json.loads(value_str)
        except json.JSONDecodeError:
            data[field_str] = value_str

    return ContextRead(user_id=user_id, data=data, updated_at=updated_at)


@router.post(
    "/{user_id}",
    response_model=ContextRead,
    status_code=status.HTTP_200_OK,
    summary="Save or update context entries for a user",
    description=(
        "Upserts one or more key/value pairs into the user's Redis context "
        "hash. Existing keys are overwritten; unmentioned keys are preserved."
    ),
)
async def update_context(
    user_id: str,
    body: ContextUpdate,
    redis: RedisDep,
) -> ContextRead:
    key = _context_key(user_id)
    now_iso = datetime.now(tz=timezone.utc).isoformat()

    mapping: dict[str, str] = {"__updated_at__": now_iso}
    for entry in body.entries:
        mapping[entry.key] = json.dumps(entry.value)

    try:
        pipe = redis.pipeline(transaction=True)
        await pipe.hset(key, mapping=mapping)  # type: ignore[arg-type]
        await pipe.expire(key, _CONTEXT_TTL_SECONDS)
        await pipe.execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Context store unavailable: {exc}",
        ) from exc

    # Re-read to return the authoritative state
    return await get_context(user_id, redis)
