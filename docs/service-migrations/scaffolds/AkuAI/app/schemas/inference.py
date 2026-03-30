"""Pydantic v2 schemas for AkuAI inference endpoints."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Shared enums
# ---------------------------------------------------------------------------


class ModelProvider(str, Enum):
    LOCAL = "local"
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"


class OutputFormat(str, Enum):
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"


# ---------------------------------------------------------------------------
# Generic inference
# ---------------------------------------------------------------------------


class InferenceRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    model: str = Field(..., description="Model identifier, e.g. 'gemma-2b' or 'gpt-4o'")
    prompt: str = Field(..., min_length=1, max_length=32_768)
    params: dict[str, Any] = Field(default_factory=dict, description="Model-specific parameters")
    provider: ModelProvider = Field(ModelProvider.LOCAL)
    output_format: OutputFormat = Field(OutputFormat.TEXT)
    max_tokens: int = Field(default=512, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    request_id: str
    model: str
    output: str
    provider: ModelProvider
    tokens_used: int | None = None
    latency_ms: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Text generation
# ---------------------------------------------------------------------------


class TextGenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, max_length=32_768)
    model: str = Field(default="gemma-2b")
    max_tokens: int = Field(default=512, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    stop_sequences: list[str] = Field(default_factory=list)
    stream: bool = Field(default=False, description="Streaming not yet implemented")


class TextGenerateResponse(BaseModel):
    request_id: str
    text: str
    model: str
    tokens_used: int | None = None
    finish_reason: str | None = None


# ---------------------------------------------------------------------------
# Text classification
# ---------------------------------------------------------------------------


class TextClassifyRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(..., min_length=1, max_length=16_384)
    labels: list[str] = Field(..., min_length=2, description="Candidate labels for zero-shot classification")
    model: str = Field(default="facebook/bart-large-mnli")
    multi_label: bool = Field(default=False)


class LabelScore(BaseModel):
    label: str
    score: float = Field(ge=0.0, le=1.0)


class TextClassifyResponse(BaseModel):
    request_id: str
    scores: list[LabelScore]
    top_label: str
    model: str


# ---------------------------------------------------------------------------
# Summarisation
# ---------------------------------------------------------------------------


class TextSummarizeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(..., min_length=50, max_length=65_536)
    model: str = Field(default="facebook/bart-large-cnn")
    max_length: int = Field(default=150, ge=20, le=1024)
    min_length: int = Field(default=40, ge=10, le=512)
    language: str = Field(default="en", max_length=8)


class TextSummarizeResponse(BaseModel):
    request_id: str
    summary: str
    model: str
    original_length: int
    summary_length: int


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------


class EmbeddingsRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    input: str | list[str] = Field(..., description="Text or list of texts to embed")
    model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    normalize: bool = Field(default=True)


class EmbeddingsResponse(BaseModel):
    request_id: str
    embeddings: list[list[float]]
    model: str
    dimensions: int
    token_count: int | None = None


# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------


class ModelCapability(str, Enum):
    TEXT_GENERATION = "text-generation"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    EMBEDDINGS = "embeddings"
    INFERENCE = "inference"


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: ModelProvider
    capabilities: list[ModelCapability]
    context_length: int | None = None
    dimensions: int | None = Field(None, description="Embedding dimensions, if applicable")
    loaded: bool = False
    description: str = ""


class ModelListResponse(BaseModel):
    models: list[ModelInfo]
    total: int


# ---------------------------------------------------------------------------
# Gemma edge relay  (payload kept small: < 4 KB)
# ---------------------------------------------------------------------------


class GemmaInferRequest(BaseModel):
    """Lightweight payload for Edge Hub containers — keep total size < 4 KB."""

    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, max_length=2048)
    max_tokens: int = Field(default=256, ge=1, le=1024)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    hub_id: str = Field(..., description="Originating Edge Hub identifier")


class GemmaInferResponse(BaseModel):
    """Minimal response — keep total size < 4 KB."""

    request_id: str
    text: str
    model: str = "gemma-2b"
    hub_id: str
    tokens_used: int | None = None
