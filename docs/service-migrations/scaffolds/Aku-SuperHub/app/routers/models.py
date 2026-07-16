from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from fastapi import APIRouter, status
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/models", tags=["Model Fine-Tuning"])


# ---------------------------------------------------------------------------
# Schemas (local to this router — no external consumers yet)
# ---------------------------------------------------------------------------


class FineTuneStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class FineTuneRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_model_id: str = Field(
        ..., min_length=1, max_length=256, description="Identifier of the base model to fine-tune"
    )
    dataset_window_hours: int = Field(
        default=168,
        ge=1,
        le=8760,
        description="Hours of recent analytics data to use as the training dataset",
    )
    max_steps: int = Field(default=500, ge=1, le=10_000, description="Maximum training steps")
    learning_rate: float = Field(
        default=2e-5, gt=0.0, description="Learning rate for the fine-tune run"
    )
    notes: str | None = Field(
        default=None, max_length=1024, description="Optional free-text notes for this job"
    )


class FineTuneJobResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    job_id: UUID = Field(..., description="Unique identifier for the fine-tuning job")
    status: FineTuneStatus
    base_model_id: str
    queued_at: datetime = Field(default_factory=datetime.utcnow)
    message: str = Field(..., description="Human-readable status message")


# ---------------------------------------------------------------------------
# Background job implementation — replace with real ML pipeline
# ---------------------------------------------------------------------------


async def _run_finetune_job(job_id: UUID, request: FineTuneRequest) -> None:
    """
    Background coroutine that drives the fine-tuning pipeline.

    Replace the placeholder logic below with calls to your ML training
    infrastructure (e.g., submit to a job queue, call a training API, etc.).
    """
    logger.info("Fine-tune job %s started (base_model=%s)", job_id, request.base_model_id)
    try:
        # TODO: Replace with real pipeline call, e.g.:
        #   await ml_client.submit_finetune(job_id=job_id, config=request)
        raise NotImplementedError(
            "Replace _run_finetune_job with a real ML training pipeline call."
        )
    except NotImplementedError:
        # Surface as a warning so the scaffold doesn't crash the event loop
        logger.warning("Fine-tune job %s: pipeline not implemented — marking as FAILED.", job_id)
    except Exception:
        logger.exception("Fine-tune job %s encountered an unexpected error.", job_id)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "/finetune",
    response_model=FineTuneJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger regional model fine-tuning",
    description=(
        "Enqueue a regional model fine-tuning job using recent analytics data "
        "collected from this SuperHub's Edge Hub fleet. The job runs asynchronously; "
        "poll the returned job_id for status updates (not yet implemented in this scaffold)."
    ),
)
async def trigger_finetune(request: FineTuneRequest) -> FineTuneJobResponse:
    job_id = uuid4()

    asyncio.create_task(
        _run_finetune_job(job_id, request),
        name=f"finetune-{job_id}",
    )

    logger.info(
        "Accepted fine-tune job %s for base_model=%s (window=%dh, steps=%d)",
        job_id,
        request.base_model_id,
        request.dataset_window_hours,
        request.max_steps,
    )

    return FineTuneJobResponse(
        job_id=job_id,
        status=FineTuneStatus.QUEUED,
        base_model_id=request.base_model_id,
        message=(
            f"Fine-tuning job queued successfully. "
            f"Training dataset window: {request.dataset_window_hours}h, "
            f"max steps: {request.max_steps}."
        ),
    )
