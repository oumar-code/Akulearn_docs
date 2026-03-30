"""Pydantic v2 schemas for blockchain credential domain."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CredentialType(StrEnum):
    COURSE_COMPLETION = "course_completion"
    SKILL_BADGE = "skill_badge"
    ASSESSMENT_PASS = "assessment_pass"


class CredentialStatus(StrEnum):
    PENDING = "pending"
    ISSUED = "issued"
    REVOKED = "revoked"
    FAILED = "failed"


class CredentialIssueRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    learner_id: UUID
    learner_wallet_address: str = Field(
        ...,
        description="Polygon-compatible EOA or contract address (0x…).",
        pattern=r"^0x[0-9a-fA-F]{40}$",
    )
    credential_type: CredentialType
    course_id: UUID
    lesson_ids: list[UUID] = Field(
        default_factory=list,
        description="Specific lessons covered by this credential.",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Arbitrary key-value pairs embedded in the on-chain token URI.",
    )
    issued_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))


class CredentialIssueResponse(BaseModel):
    """Result returned immediately after submitting the issuance transaction."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    credential_id: UUID
    tx_hash: str = Field(..., description="Polygon transaction hash (0x…).")
    status: CredentialStatus = CredentialStatus.PENDING
    polygon_explorer_url: str | None = Field(
        default=None,
        description="PolygonScan URL for the transaction.",
    )
    issued_at: datetime


class CredentialVerifyResponse(BaseModel):
    """On-chain verification result for a credential."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    credential_id: UUID
    status: CredentialStatus
    tx_hash: str | None = None
    learner_wallet_address: str | None = None
    credential_type: CredentialType | None = None
    course_id: UUID | None = None
    issued_at: datetime | None = None
    revoked_at: datetime | None = None
    on_chain_verified: bool = Field(
        ...,
        description="True when the tx receipt confirms the mint succeeded.",
    )
