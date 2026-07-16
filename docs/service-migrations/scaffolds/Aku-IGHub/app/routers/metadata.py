"""Anonymised metadata exchange router — publish and retrieve (→ Aku-DaaS)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.metadata import (
    MetadataPublishRequest,
    MetadataPublishResponse,
    MetadataRecord,
)

router = APIRouter(prefix="/api/v1/metadata", tags=["metadata"])

# ---------------------------------------------------------------------------
# In-memory store — replace with persistent DB / cache in production
# ---------------------------------------------------------------------------

_metadata_store: dict[str, MetadataRecord] = {}


# ---------------------------------------------------------------------------
# Publish
# ---------------------------------------------------------------------------


@router.post(
    "/publish",
    response_model=MetadataPublishResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish anonymised metadata (forwarded to Aku-DaaS)",
    description=(
        "Accepts anonymised event metadata from any Aku service and forwards it "
        "to the Aku-DaaS data analytics service. PII keys are rejected at schema "
        "validation level. JWT authentication required."
    ),
)
async def publish_metadata(
    body: MetadataPublishRequest,
    current_user: dict = Depends(get_current_user),
) -> MetadataPublishResponse:
    metadata_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    record = MetadataRecord(
        metadata_id=metadata_id,
        category=body.category,
        payload=body.payload,
        tags=body.tags,
        source_service=body.source_service,
        schema_version=body.schema_version,
        published_at=now,
    )

    _metadata_store[metadata_id] = record

    # Forward to Aku-DaaS asynchronously (fire-and-forget with best-effort ack)
    daas_ingested = await _forward_to_daas(record)

    return MetadataPublishResponse(
        metadata_id=metadata_id,
        category=body.category,
        published_at=now,
        daas_ingested=daas_ingested,
    )


async def _forward_to_daas(record: MetadataRecord) -> bool:
    """Forward a metadata record to Aku-DaaS; returns True on acknowledged receipt."""
    from app.core.config import settings  # lazy import to avoid circular deps

    daas_url = getattr(settings, "daas_ingest_url", None)
    if not daas_url:
        return False

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                daas_url,
                json=record.model_dump(mode="json"),
            )
            return resp.is_success
    except httpx.RequestError:
        return False


# ---------------------------------------------------------------------------
# Retrieve
# ---------------------------------------------------------------------------


@router.get(
    "/{metadata_id}",
    response_model=MetadataRecord,
    summary="Retrieve a published metadata record",
    description="Fetch a previously published metadata record by its ID. JWT authentication required.",
)
async def get_metadata(
    metadata_id: str,
    current_user: dict = Depends(get_current_user),
) -> MetadataRecord:
    # TODO: query persistent store (e.g. Supabase / PostgreSQL)
    record = _metadata_store.get(metadata_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Metadata record '{metadata_id}' not found.",
        )
    return record
