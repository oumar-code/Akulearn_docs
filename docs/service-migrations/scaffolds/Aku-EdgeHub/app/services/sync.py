"""Async cloud-sync service — calls Akudemy content sync API via httpx."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_SYNC_ENDPOINT = "/api/v1/content/sync"
_INFER_ENDPOINT = "/api/v1/models/gemma/infer"


async def trigger_cloud_sync(
    *,
    force: bool = False,
    scope: list[str] | None = None,
) -> dict[str, object]:
    """Push a sync request to Akudemy's content sync API.

    Returns a dict with keys: accepted, job_id, message.
    Falls back gracefully when the hub is fully offline.
    """
    job_id = str(uuid.uuid4())
    payload: dict[str, object] = {
        "job_id": job_id,
        "force": force,
        "scope": scope or [],
        "requested_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        async with httpx.AsyncClient(
            base_url=settings.akudemy_base_url,
            timeout=settings.sync_timeout_seconds,
            headers={"X-Api-Key": settings.akudemy_api_key},
        ) as client:
            resp = await client.post(_SYNC_ENDPOINT, json=payload)
            resp.raise_for_status()
            data: dict[str, object] = resp.json()
            logger.info("Sync job %s accepted by Akudemy", job_id)
            return {
                "accepted": True,
                "job_id": data.get("job_id", job_id),
                "message": data.get("message", "Sync accepted"),
            }
    except httpx.HTTPStatusError as exc:
        logger.warning("Akudemy rejected sync request: %s", exc.response.text)
        return {
            "accepted": False,
            "job_id": None,
            "message": f"Remote error {exc.response.status_code}: {exc.response.text[:200]}",
        }
    except httpx.RequestError as exc:
        logger.warning("Cannot reach Akudemy (offline?): %s", exc)
        return {
            "accepted": False,
            "job_id": None,
            "message": "Hub is offline — sync queued locally",
        }


async def relay_infer(payload: dict[str, object]) -> dict[str, object]:
    """Relay a small inference request to AkuAI's Gemma endpoint.

    Raises httpx.HTTPStatusError on upstream HTTP errors so the caller
    can decide how to surface the failure.
    """
    async with httpx.AsyncClient(
        base_url=settings.akuai_base_url,
        timeout=settings.infer_timeout_seconds,
        headers={"X-Api-Key": settings.akuai_api_key},
    ) as client:
        resp = await client.post(_INFER_ENDPOINT, json=payload)
        resp.raise_for_status()
        return resp.json()
