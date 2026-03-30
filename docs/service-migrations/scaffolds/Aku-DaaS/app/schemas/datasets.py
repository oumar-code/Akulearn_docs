"""Pydantic v2 schemas for dataset ingestion, status tracking, and anonymisation."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------------------
# Status enum
# ---------------------------------------------------------------------------


class DatasetStatus(StrEnum):
    PENDING = "pending"
    INGESTED = "ingested"
    ANONYMISING = "anonymising"
    ANONYMISED = "anonymised"
    PUBLISHED = "published"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


class DatasetIngestRequest(BaseModel):
    """JSON body variant of the ingest endpoint (multipart upload handled at router level)."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., description="Human-readable dataset name", min_length=1, max_length=255)
    description: str = Field(default="", description="Optional dataset description")
    source_service: str = Field(
        ...,
        description="Originating Aku service identifier, e.g. 'Akudemy'",
    )
    schema_version: str = Field("1.0", description="Dataset schema version for downstream compatibility")
    tags: list[str] = Field(default_factory=list, description="Searchable classification tags")
    raw_payload: dict[str, Any] | None = Field(
        default=None,
        description="Inline JSON dataset — mutually exclusive with multipart file upload",
    )

    @model_validator(mode="after")
    def _require_payload_or_file(self) -> "DatasetIngestRequest":
        """raw_payload is optional here because the multipart path supplies no JSON body."""
        return self


class DatasetIngestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str = Field(..., description="Unique dataset ID (UUID v4)")
    name: str
    status: DatasetStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = Field(default="Dataset ingested. Trigger anonymisation to proceed.")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


class DatasetStatusResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str
    name: str
    status: DatasetStatus
    source_service: str
    schema_version: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    anonymised_at: datetime | None = None
    published_at: datetime | None = None
    error_detail: str | None = Field(
        default=None,
        description="Populated when status is FAILED",
    )


# ---------------------------------------------------------------------------
# Anonymise trigger
# ---------------------------------------------------------------------------


class AnonymiseRequest(BaseModel):
    """Optional runtime configuration for the anonymisation pipeline."""

    model_config = ConfigDict(populate_by_name=True)

    k_value: int = Field(
        default=5,
        ge=2,
        le=100,
        description="k-anonymity parameter — minimum equivalence class size",
    )
    quasi_identifiers: list[str] = Field(
        default_factory=list,
        description="Column names treated as quasi-identifiers for k-anonymity",
    )
    suppress_threshold: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
        description="Row suppression rate above which the job aborts (0–1 fraction)",
    )


class AnonymiseResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str
    status: DatasetStatus
    message: str = Field(default="Anonymisation pipeline started as a background task.")
    k_value: int
