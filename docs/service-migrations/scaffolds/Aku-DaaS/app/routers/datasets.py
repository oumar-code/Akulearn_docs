"""Dataset ingestion, anonymisation trigger, and status routing."""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
from fastapi import File, Form

from app.schemas.datasets import (
    AnonymiseRequest,
    AnonymiseResponse,
    DatasetIngestRequest,
    DatasetIngestResponse,
    DatasetStatus,
    DatasetStatusResponse,
)
from app.services.anonymisation import AnonymisationService, get_dataset_store

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


# ---------------------------------------------------------------------------
# POST /api/v1/datasets/ingest
# ---------------------------------------------------------------------------


@router.post(
    "/ingest",
    response_model=DatasetIngestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a raw dataset",
    description=(
        "Accepts a raw dataset via **multipart file upload** (CSV / Parquet / JSON Lines) "
        "**or** an inline JSON payload body. The dataset is stored in INGESTED state and "
        "awaits an explicit anonymisation trigger. Authentication required in production."
    ),
)
async def ingest_dataset(
    file: UploadFile | None = File(default=None, description="Raw dataset file (CSV, Parquet, JSONL)"),
    name: str = Form(default=""),
    description: str = Form(default=""),
    source_service: str = Form(default="unknown"),
    schema_version: str = Form(default="1.0"),
    tags: str = Form(default="", description="Comma-separated tag list"),
    body: DatasetIngestRequest | None = None,
) -> DatasetIngestResponse:
    """Ingest endpoint supporting both multipart and JSON body variants.

    When ``file`` is supplied (multipart), form fields provide metadata.
    When ``file`` is None, ``body`` must carry the JSON payload.
    """
    store = get_dataset_store()

    if file is not None:
        # Multipart path — read file bytes, metadata from form fields
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        dataset_name = name or file.filename or "unnamed"
        source = source_service
        schema_ver = schema_version
        desc = description
        raw_payload = None  # stored to object storage in real implementation
        file_bytes = await file.read()
        logger.info(
            "datasets.ingest multipart name=%s source=%s bytes=%d",
            dataset_name,
            source,
            len(file_bytes),
        )
    elif body is not None:
        # JSON body path
        tag_list = body.tags
        dataset_name = body.name
        source = body.source_service
        schema_ver = body.schema_version
        desc = body.description
        raw_payload = body.raw_payload
        logger.info(
            "datasets.ingest json name=%s source=%s",
            dataset_name,
            source,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide either a multipart file upload or a JSON request body.",
        )

    dataset_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    store[dataset_id] = {
        "dataset_id": dataset_id,
        "name": dataset_name,
        "description": desc,
        "source_service": source,
        "schema_version": schema_ver,
        "tags": tag_list,
        "raw_payload": raw_payload,
        "status": DatasetStatus.INGESTED,
        "created_at": now,
        "updated_at": now,
        "anonymised_at": None,
        "published_at": None,
        "error_detail": None,
    }

    return DatasetIngestResponse(
        dataset_id=dataset_id,
        name=dataset_name,
        status=DatasetStatus.INGESTED,
        created_at=now,
    )


# ---------------------------------------------------------------------------
# GET /api/v1/datasets/{id}/status
# ---------------------------------------------------------------------------


@router.get(
    "/{dataset_id}/status",
    response_model=DatasetStatusResponse,
    summary="Get anonymisation pipeline status",
    description="Return the current processing status for a dataset by its UUID.",
)
async def get_dataset_status(dataset_id: str) -> DatasetStatusResponse:
    store = get_dataset_store()
    record = store.get(dataset_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{dataset_id}' not found.",
        )
    return DatasetStatusResponse(**record)


# ---------------------------------------------------------------------------
# POST /api/v1/datasets/{id}/anonymise
# ---------------------------------------------------------------------------


@router.post(
    "/{dataset_id}/anonymise",
    response_model=AnonymiseResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger the anonymisation pipeline",
    description=(
        "Launches the anonymisation pipeline as an **async background task**. "
        "The dataset must be in INGESTED state. Poll `/status` to track progress. "
        "Returns 202 Accepted immediately — the pipeline runs concurrently."
    ),
)
async def trigger_anonymise(
    dataset_id: str,
    body: AnonymiseRequest = AnonymiseRequest(),
) -> AnonymiseResponse:
    store = get_dataset_store()
    record = store.get(dataset_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{dataset_id}' not found.",
        )

    current_status = record["status"]
    if current_status not in {DatasetStatus.INGESTED, DatasetStatus.FAILED}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot start anonymisation: dataset is in '{current_status}' state. "
                f"Anonymisation can only be triggered from INGESTED or FAILED."
            ),
        )

    service = AnonymisationService(
        dataset_id=dataset_id,
        k_value=body.k_value,
        quasi_identifiers=body.quasi_identifiers,
        suppress_threshold=body.suppress_threshold,
        store=store,
    )

    # Fire-and-forget — status transitions are managed inside the service
    asyncio.create_task(service.run(), name=f"anonymise-{dataset_id}")

    logger.info(
        "datasets.anonymise.triggered dataset_id=%s k=%d",
        dataset_id,
        body.k_value,
    )

    return AnonymiseResponse(
        dataset_id=dataset_id,
        status=DatasetStatus.ANONYMISING,
        k_value=body.k_value,
    )
