"""AkuAI InferenceService — async-ready stub with mock responses.

Real implementation will load torch / transformers / llama-cpp-python /
sentence-transformers in the lifespan hook and store handles in app.state.
"""

from __future__ import annotations

import uuid
from time import monotonic
from typing import TYPE_CHECKING

from app.schemas.inference import (
    EmbeddingsRequest,
    EmbeddingsResponse,
    GemmaInferRequest,
    GemmaInferResponse,
    InferenceRequest,
    InferenceResponse,
    LabelScore,
    ModelCapability,
    ModelInfo,
    ModelListResponse,
    ModelProvider,
    TextClassifyRequest,
    TextClassifyResponse,
    TextGenerateRequest,
    TextGenerateResponse,
    TextSummarizeRequest,
    TextSummarizeResponse,
)

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Mock catalogue — replaced by dynamic discovery once models are loaded
# ---------------------------------------------------------------------------

_MODEL_CATALOGUE: list[ModelInfo] = [
    ModelInfo(
        id="gemma-2b",
        name="Gemma 2B",
        provider=ModelProvider.LOCAL,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.INFERENCE],
        context_length=8192,
        loaded=False,
        description="Google Gemma 2B — lightweight local LLM, primary model for Edge Hubs.",
    ),
    ModelInfo(
        id="facebook/bart-large-cnn",
        name="BART Large CNN",
        provider=ModelProvider.LOCAL,
        capabilities=[ModelCapability.SUMMARIZATION],
        context_length=1024,
        loaded=False,
        description="Fine-tuned BART for news summarisation.",
    ),
    ModelInfo(
        id="facebook/bart-large-mnli",
        name="BART Large MNLI",
        provider=ModelProvider.LOCAL,
        capabilities=[ModelCapability.CLASSIFICATION],
        context_length=1024,
        loaded=False,
        description="Zero-shot text classification via NLI.",
    ),
    ModelInfo(
        id="sentence-transformers/all-MiniLM-L6-v2",
        name="all-MiniLM-L6-v2",
        provider=ModelProvider.LOCAL,
        capabilities=[ModelCapability.EMBEDDINGS],
        dimensions=384,
        loaded=False,
        description="Fast, high-quality sentence embeddings — 384 dimensions.",
    ),
]


class InferenceService:
    """Central inference façade called by all AkuAI routers.

    Stub returns deterministic mock data.  Replace each ``_load_*`` method
    and the ``_run_*`` internals with real torch/transformers calls.
    """

    # ------------------------------------------------------------------
    # Lifecycle helpers (called from FastAPI lifespan)
    # ------------------------------------------------------------------

    async def startup(self) -> None:
        """Load models into memory.  Currently a no-op stub."""
        # TODO: call self._load_text_gen(), self._load_embeddings(), etc.
        pass

    async def shutdown(self) -> None:
        """Release model resources gracefully."""
        pass

    # ------------------------------------------------------------------
    # Generic inference
    # ------------------------------------------------------------------

    async def run_inference(self, req: InferenceRequest) -> InferenceResponse:
        start = monotonic()
        # TODO: route to appropriate model pipeline based on req.model / req.provider
        output = f"[STUB] Inference response for model={req.model!r}, prompt={req.prompt[:60]!r}…"
        return InferenceResponse(
            request_id=_new_id(),
            model=req.model,
            output=output,
            provider=req.provider,
            tokens_used=len(req.prompt.split()),
            latency_ms=_elapsed_ms(start),
        )

    # ------------------------------------------------------------------
    # Text generation
    # ------------------------------------------------------------------

    async def generate_text(self, req: TextGenerateRequest) -> TextGenerateResponse:
        # TODO: load Gemma / llama-cpp pipeline and call generate()
        text = (
            f"[STUB] Generated text for prompt: {req.prompt[:80]}…  "
            f"(max_tokens={req.max_tokens}, temperature={req.temperature})"
        )
        return TextGenerateResponse(
            request_id=_new_id(),
            text=text,
            model=req.model,
            tokens_used=req.max_tokens,
            finish_reason="length",
        )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    async def classify_text(self, req: TextClassifyRequest) -> TextClassifyResponse:
        # TODO: load zero-shot pipeline (BART-MNLI) and run classification
        n = len(req.labels)
        mock_scores = [
            LabelScore(label=label, score=round(1.0 / n, 4))
            for label in req.labels
        ]
        return TextClassifyResponse(
            request_id=_new_id(),
            scores=mock_scores,
            top_label=req.labels[0],
            model=req.model,
        )

    # ------------------------------------------------------------------
    # Summarisation
    # ------------------------------------------------------------------

    async def summarize_text(self, req: TextSummarizeRequest) -> TextSummarizeResponse:
        # TODO: load BART-CNN pipeline and call summarize()
        summary = f"[STUB] Summary of {len(req.text)} chars → (min={req.min_length}, max={req.max_length} tokens)."
        return TextSummarizeResponse(
            request_id=_new_id(),
            summary=summary,
            model=req.model,
            original_length=len(req.text),
            summary_length=len(summary),
        )

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    async def get_embeddings(self, req: EmbeddingsRequest) -> EmbeddingsResponse:
        # TODO: load SentenceTransformer and call encode()
        texts = [req.input] if isinstance(req.input, str) else req.input
        stub_vector = [0.0] * 384  # all-MiniLM-L6-v2 produces 384-dim vectors
        return EmbeddingsResponse(
            request_id=_new_id(),
            embeddings=[stub_vector for _ in texts],
            model=req.model,
            dimensions=384,
            token_count=sum(len(t.split()) for t in texts),
        )

    # ------------------------------------------------------------------
    # Model registry
    # ------------------------------------------------------------------

    async def list_models(self) -> ModelListResponse:
        return ModelListResponse(
            models=_MODEL_CATALOGUE,
            total=len(_MODEL_CATALOGUE),
        )

    # ------------------------------------------------------------------
    # Gemma Edge Hub relay
    # ------------------------------------------------------------------

    async def gemma_infer(self, req: GemmaInferRequest) -> GemmaInferResponse:
        # TODO: route to locally loaded Gemma pipeline (llama-cpp-python)
        # Response deliberately minimal to stay well under 4 KB over the wire.
        text = f"[STUB] Gemma response for hub={req.hub_id!r}: {req.prompt[:60]}…"
        return GemmaInferResponse(
            request_id=_new_id(),
            text=text,
            model="gemma-2b",
            hub_id=req.hub_id,
            tokens_used=req.max_tokens,
        )


# ---------------------------------------------------------------------------
# Module-level singleton — imported by routers via dependency injection
# ---------------------------------------------------------------------------

inference_service = InferenceService()


def get_inference_service() -> InferenceService:
    """FastAPI dependency that returns the shared InferenceService instance."""
    return inference_service


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _new_id() -> str:
    return str(uuid.uuid4())


def _elapsed_ms(start: float) -> float:
    return round((monotonic() - start) * 1000, 2)
