"""Pydantic v2 schemas for AkuWorkspace workflow and context domain."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class WorkflowType(StrEnum):
    DATA_QUERY = "DATA_QUERY"
    DOC_GENERATION = "DOC_GENERATION"
    CONTENT_SEARCH = "CONTENT_SEARCH"
    TUTORING_ASSIST = "TUTORING_ASSIST"


class WorkflowStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Workflow schemas
# ---------------------------------------------------------------------------


class WorkflowStep(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., description="Human-readable step label")
    service: str = Field(..., description="Target micro-service (akuai | daas | akudemy)")
    endpoint: str = Field(..., description="Relative endpoint path on target service")
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Static payload merged with runtime context before dispatch",
    )


class WorkflowCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=128)
    type: WorkflowType
    steps: list[WorkflowStep] = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    type: WorkflowType
    status: WorkflowStatus
    steps: list[WorkflowStep]
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class WorkflowRunRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    input: dict[str, Any] = Field(
        default_factory=dict,
        description="Runtime input merged into each step payload",
    )


class WorkflowRunResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_id: uuid.UUID
    status: WorkflowStatus
    outputs: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Ordered list of per-step response payloads",
    )
    error: str | None = None
    duration_ms: int | None = None


# ---------------------------------------------------------------------------
# Context schemas
# ---------------------------------------------------------------------------


class ContextEntry(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    key: str = Field(..., description="Arbitrary context key (e.g. 'last_topic')")
    value: Any = Field(..., description="JSON-serialisable context value")


class ContextUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    entries: list[ContextEntry] = Field(..., min_length=1)


class ContextRead(BaseModel):
    user_id: str
    data: dict[str, Any]
    updated_at: datetime | None = None


# ---------------------------------------------------------------------------
# Doc generation schemas
# ---------------------------------------------------------------------------


class DocGenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, description="Natural language prompt")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context forwarded to AkuAI",
    )
    max_tokens: int = Field(default=1024, ge=64, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class DocGenerateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document: str
    model: str | None = None
    usage: dict[str, int] | None = None
