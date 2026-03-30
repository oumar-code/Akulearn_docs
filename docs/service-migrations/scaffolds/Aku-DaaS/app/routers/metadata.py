"""Anonymised metadata publishing router — forwards to Aku-IGHub."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/metadata", tags=["metadata"])


# ---------------------------------------------------------------------------
# Local schemas (DaaS-side publish contract)
# ---------------------------------------------------------------------------


class MetadataPublishRequest(BaseModel):
    """Anonymised metadata record forwarded to Aku-IGHub for global distribution."""

    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str = Field(
        ...,
        description="UUID of the anonymised dataset being published",
    )
    category: str = Field(
        ...,
        description="Metadata category — must match Aku-IGHub MetadataCategory vocabulary",
    )
    payload: dict[str, Any] = Field(
        ...,
        description="Anonymised summary payload — must not contain PII",
    )
    tags: list[str] = Field(default_factory=list, description="Searchable classification tags")
    source_service: str = Field(
        default="Aku-DaaS",
        description="Originating service identifier forwarded to IGHub",
    )
    schema_version: str = Field("1.0", description="Payload schema version")


class MetadataPublishResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    publish_id: str = Field(..., description="DaaS-local publish event ID (UUID v4)")
    dataset_id: str
    ighub_metadata_id: str | None = Field(
        default=None,
        description="Metadata ID assigned by Aku-IGHub; None if IGHub is unreachable",
    )
    ighub_acknowledged: bool = Field(
        ...,
        description="True when Aku-IGHub returned a successful response",
    )
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# In-memory publish log (replace with DB persistence in production)
# ---------------------------------------------------------------------------

_publish_log: dict[str, MetadataPublishResponse] = {}


# ---------------------------------------------------------------------------
# POST /api/v1/metadata/publish
# ---------------------------------------------------------------------------


@router.post(
    "/publish",
    response_model=MetadataPublishResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish anonymised metadata → Aku-IGHub",
    description=(
        "Publishes an anonymised dataset summary to Aku-IGHub via "
        "`POST /api/v1/metadata/publish`. If IGHub is unreachable the record is "
        "still logged locally and `ighub_acknowledged: false` is returned. "
        "Authentication required in production."
    ),
)
async def publish_metadata(body: MetadataPublishRequest) -> MetadataPublishResponse:
    publish_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    ighub_metadata_id, ighub_ack = await _forward_to_ighub(body)

    response = MetadataPublishResponse(
        publish_id=publish_id,
        dataset_id=body.dataset_id,
        ighub_metadata_id=ighub_metadata_id,
        ighub_acknowledged=ighub_ack,
        published_at=now,
    )
    _publish_log[publish_id] = response

    logger.info(
        "metadata.publish dataset_id=%s publish_id=%s ighub_ack=%s",
        body.dataset_id,
        publish_id,
        ighub_ack,
    )
    return response


# ---------------------------------------------------------------------------
# IGHub forwarding helper
# ---------------------------------------------------------------------------


async def _forward_to_ighub(body: MetadataPublishRequest) -> tuple[str | None, bool]:
    """POST the metadata record to Aku-IGHub.

    Returns:
        (ighub_metadata_id, success_bool)  — id is None on failure.
    """
    try:
        from app.core.config import settings  # lazy import — avoids circular deps at module load

        ighub_url = getattr(settings, "ighub_metadata_publish_url", None)
    except Exception:  # noqa: BLE001
        ighub_url = None

    if not ighub_url:
        logger.warning("metadata.publish: IGHUB_METADATA_PUBLISH_URL not configured — skipping forward")
        return None, False

    payload = {
        "category": body.category,
        "payload": body.payload,
        "tags": body.tags,
        "source_service": body.source_service,
        "schema_version": body.schema_version,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(ighub_url, json=payload)
            if resp.is_success:
                data = resp.json()
                return data.get("metadata_id"), True
            logger.warning(
                "metadata.publish: IGHub returned %d: %s",
                resp.status_code,
                resp.text[:200],
            )
            return None, False
    except httpx.RequestError as exc:
        logger.warning("metadata.publish: IGHub unreachable — %s", exc)
        return None, False
