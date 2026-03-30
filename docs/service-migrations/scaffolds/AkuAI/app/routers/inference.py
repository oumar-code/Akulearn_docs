"""AkuAI inference router — text generation, classification, summarisation, embeddings."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.schemas.inference import (
    EmbeddingsRequest,
    EmbeddingsResponse,
    InferenceRequest,
    InferenceResponse,
    TextClassifyRequest,
    TextClassifyResponse,
    TextGenerateRequest,
    TextGenerateResponse,
    TextSummarizeRequest,
    TextSummarizeResponse,
)
from app.services.inference import InferenceService, get_inference_service

router = APIRouter(prefix="/api/v1", tags=["inference"])


@router.post(
    "/inference",
    response_model=InferenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Generic inference",
    description="Run inference against any registered model.  Pass model-specific parameters in `params`.",
)
async def run_inference(
    body: InferenceRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> InferenceResponse:
    return await svc.run_inference(body)


@router.post(
    "/text/generate",
    response_model=TextGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="LLM text generation",
    description="Generate text from a prompt using a local or remote LLM.",
)
async def generate_text(
    body: TextGenerateRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> TextGenerateResponse:
    return await svc.generate_text(body)


@router.post(
    "/text/classify",
    response_model=TextClassifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Zero-shot text classification",
    description="Classify text into one or more of the provided candidate labels.",
)
async def classify_text(
    body: TextClassifyRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> TextClassifyResponse:
    return await svc.classify_text(body)


@router.post(
    "/text/summarize",
    response_model=TextSummarizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Text summarisation",
    description="Summarise a long document into a shorter passage.",
)
async def summarize_text(
    body: TextSummarizeRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> TextSummarizeResponse:
    return await svc.summarize_text(body)


@router.post(
    "/embeddings",
    response_model=EmbeddingsResponse,
    status_code=status.HTTP_200_OK,
    summary="Vector embeddings",
    description="Generate dense vector embeddings for semantic search and similarity tasks.",
)
async def get_embeddings(
    body: EmbeddingsRequest,
    svc: InferenceService = Depends(get_inference_service),
) -> EmbeddingsResponse:
    return await svc.get_embeddings(body)
