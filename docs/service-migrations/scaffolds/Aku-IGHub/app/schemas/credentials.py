"""Pydantic v2 schemas for the verifiable credential domain."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CredentialType(StrEnum):
    LEARNING_ACHIEVEMENT = "LearningAchievement"
    IDENTITY = "Identity"
    SKILL_BADGE = "SkillBadge"
    CERTIFICATE = "Certificate"


# ---------------------------------------------------------------------------
# Issue
# ---------------------------------------------------------------------------


class CredentialIssueRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    subject_did: str = Field(..., description="W3C DID of the credential subject")
    credential_type: CredentialType
    claims: dict[str, Any] = Field(..., description="Domain-specific credential claims; must not contain raw PII")
    expiry_date: datetime | None = Field(None, description="Optional credential expiry (UTC)")
    issuer_did: str | None = Field(
        None,
        description="Issuing DID; defaults to the gateway's own service DID when omitted",
    )


class CredentialIssueResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credential_id: str = Field(..., description="Unique credential identifier (UUID v4)")
    credential_type: CredentialType
    subject_did: str
    issuer_did: str
    issued_at: datetime
    expiry_date: datetime | None = None
    jwt: str = Field(..., description="Signed W3C Verifiable Credential as a compact JWT")


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------


class CredentialVerifyResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credential_id: str
    valid: bool = Field(..., description="True only when signature, expiry, and revocation checks all pass")
    subject_did: str | None = None
    issuer_did: str | None = None
    issued_at: datetime | None = None
    expiry_date: datetime | None = None
    revoked: bool = Field(False, description="True if the credential appears on the revocation registry")
    verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    failure_reason: str | None = Field(None, description="Human-readable reason when valid=False")
