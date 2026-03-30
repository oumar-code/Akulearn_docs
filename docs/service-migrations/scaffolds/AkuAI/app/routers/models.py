"""AkuAI models router — model registry and Gemma Edge Hub relay."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.schemas.inference import (
    GemmaInferRequest,
    GemmaInferResponse,
    ModelListResponse,
)
from app.services.inference import InferenceService, get_inference_service

router = APIRouter(prefix="/api/v1", tags=["models"])


@router.get(
    "/models",
    response_model=ModelListResponse,
    status_code=status.HTTP_200_OK,
    summary="List available models",
    description="Return all models registered with AkuAI, including their capabilities and load status.",
)
async def list_models(
    svc: InferenceService = Depends(get_inference_service),
) -> ModelListResponse:
    return await svc.list_models()


@router.post(
    "/models/gemma/infer",
    response_model=GemmaInferResponse,
    status_code=status.HTTP_200_OK,
    summary="Gemma Edge Hub relay",
    description=(
        "Lightweight inference endpoint for Edge Hub containers running Gemma locally. "
        "Request and response payloads are intentionally kept under 4 KB. "
        "Callers must supply their `hub_id` so responses can be routed back correctly."
    ),
)
async def gemma_infer(
    body: GemmaInferRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> GemmaInferResponse:
    return await svc.gemma_infer(body)
