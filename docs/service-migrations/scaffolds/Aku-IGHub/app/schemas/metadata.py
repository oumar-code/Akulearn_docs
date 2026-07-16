"""Pydantic v2 schemas for anonymised metadata exchange (→ Aku-DaaS)."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MetadataCategory(StrEnum):
    LEARNING_ACTIVITY = "learning_activity"
    SKILL_ASSESSMENT = "skill_assessment"
    CONTENT_INTERACTION = "content_interaction"
    SYSTEM_TELEMETRY = "system_telemetry"


# ---------------------------------------------------------------------------
# Publish
# ---------------------------------------------------------------------------


class MetadataPublishRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category: MetadataCategory
    payload: dict[str, Any] = Field(
        ...,
        description="Anonymised payload — must not contain PII (name, email, DOB, etc.)",
    )
    tags: list[str] = Field(
        default_factory=list, description="Searchable tags for downstream DaaS indexing"
    )
    source_service: str = Field(
        ..., description="Originating Aku service identifier, e.g. 'Akudemy'"
    )
    schema_version: str = Field("1.0", description="Payload schema version for DaaS compatibility")

    @model_validator(mode="after")
    def _reject_pii_keys(self) -> MetadataPublishRequest:
        """Best-effort guard: reject payloads with obvious PII field names."""
        pii_keys = {"name", "email", "phone", "dob", "date_of_birth", "ssn", "passport", "address"}
        found = pii_keys & {k.lower() for k in self.payload}
        if found:
            raise ValueError(
                f"Payload contains probable PII keys: {found}. Strip PII before publishing."
            )
        return self


class MetadataPublishResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    metadata_id: str = Field(..., description="Unique metadata record ID (UUID v4)")
    category: MetadataCategory
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    daas_ingested: bool = Field(
        ...,
        description="True when Aku-DaaS acknowledged the publish event synchronously",
    )


# ---------------------------------------------------------------------------
# Retrieve
# ---------------------------------------------------------------------------


class MetadataRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    metadata_id: str
    category: MetadataCategory
    payload: dict[str, Any]
    tags: list[str]
    source_service: str
    schema_version: str
    published_at: datetime
