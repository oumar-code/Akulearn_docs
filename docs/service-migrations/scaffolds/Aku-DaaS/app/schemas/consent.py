"""Pydantic v2 schemas for consent record management."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Consent purpose vocabulary
# ---------------------------------------------------------------------------


class ConsentPurpose(StrEnum):
    ANALYTICS = "analytics"
    RESEARCH = "research"
    PERSONALISATION = "personalisation"
    THIRD_PARTY_SHARING = "third_party_sharing"
    MARKETING = "marketing"
    SERVICE_IMPROVEMENT = "service_improvement"


# ---------------------------------------------------------------------------
# Consent record
# ---------------------------------------------------------------------------


class ConsentRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., description="Platform user identifier (UUID or opaque ID — never raw PII)")
    consent_given: bool = Field(
        ...,
        description="Master consent flag; False implies withdrawal of all purposes",
    )
    consent_for: list[ConsentPurpose] = Field(
        default_factory=list,
        description="Granular list of purposes for which consent is granted",
    )
    jurisdiction: str = Field(
        default="NG",
        min_length=2,
        max_length=5,
        description="ISO 3166-1 alpha-2 jurisdiction code (affects applicable framework: GDPR, NDPR, …)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the last consent change",
    )

    @field_validator("consent_for", mode="after")
    @classmethod
    def _clear_purposes_on_withdrawal(cls, v: list[ConsentPurpose]) -> list[ConsentPurpose]:
        return v  # enforcement handled in the router after full model is built


class ConsentUpsertRequest(BaseModel):
    """Request body for creating or updating a user's consent record."""

    model_config = ConfigDict(populate_by_name=True)

    consent_given: bool = Field(
        ...,
        description="Set True to grant consent, False to withdraw all consent",
    )
    consent_for: list[ConsentPurpose] = Field(
        default_factory=list,
        description=(
            "Purposes explicitly consented to. Ignored (cleared) when consent_given is False."
        ),
    )
    jurisdiction: str = Field(
        default="NG",
        min_length=2,
        max_length=5,
        description="ISO 3166-1 alpha-2 country code",
    )


class ConsentResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str
    consent_given: bool
    consent_for: list[ConsentPurpose]
    jurisdiction: str
    updated_at: datetime
    is_new: bool = Field(
        default=False,
        description="True when the record was created (rather than updated) by this request",
    )
