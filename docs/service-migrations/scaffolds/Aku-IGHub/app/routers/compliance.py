"""Cross-border compliance and policy-check router."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field

from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])


# ---------------------------------------------------------------------------
# Inline schemas (compliance is self-contained; no shared schema module needed)
# ---------------------------------------------------------------------------


class ComplianceDecision(StrEnum):
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class PolicyDomain(StrEnum):
    GDPR = "GDPR"
    PDPA = "PDPA"           # Thailand / Singapore
    FERPA = "FERPA"         # US education records
    COPPA = "COPPA"         # US child privacy
    NDPR = "NDPR"           # Nigeria Data Protection Regulation
    POPIA = "POPIA"         # South Africa
    LGPD = "LGPD"           # Brazil
    CUSTOM = "CUSTOM"


class ComplianceCheckRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    operation: str = Field(
        ...,
        description="Logical operation being checked, e.g. 'data.export', 'credential.share'",
    )
    source_jurisdiction: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code of the data source (e.g. 'NG', 'US')",
        min_length=2,
        max_length=2,
    )
    target_jurisdiction: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code of the data destination (e.g. 'DE', 'ZA')",
        min_length=2,
        max_length=2,
    )
    applicable_policies: list[PolicyDomain] = Field(
        default_factory=list,
        description="Explicitly requested policy frameworks; empty means auto-detect from jurisdictions",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (data categories, user age group, consent status, etc.)",
    )


class PolicyViolation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    policy: PolicyDomain
    rule: str = Field(..., description="Short rule identifier, e.g. 'GDPR.Art.46'")
    description: str
    severity: str = Field(..., description="'blocking' | 'warning' | 'informational'")


class ComplianceCheckResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    decision: ComplianceDecision
    operation: str
    source_jurisdiction: str
    target_jurisdiction: str
    policies_evaluated: list[PolicyDomain]
    violations: list[PolicyViolation] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Cross-border policy check
# ---------------------------------------------------------------------------


@router.post(
    "/check",
    response_model=ComplianceCheckResponse,
    summary="Cross-border policy / compliance check",
    description=(
        "Evaluates a proposed cross-border data operation against the applicable "
        "regulatory frameworks (GDPR, PDPA, FERPA, NDPR, etc.) derived from "
        "the source and target jurisdictions. Returns a structured decision with "
        "any violations and remediation recommendations. JWT authentication required."
    ),
)
async def compliance_check(
    body: ComplianceCheckRequest,
    current_user: dict = Depends(get_current_user),
) -> ComplianceCheckResponse:
    # TODO: integrate with a policy-engine service (e.g. OPA / Cedar)
    policies = body.applicable_policies or _infer_policies(
        body.source_jurisdiction, body.target_jurisdiction
    )

    violations: list[PolicyViolation] = []
    recommendations: list[str] = []

    # Stub: surface a warning for EU→non-adequate-country transfers
    _eu_member_states = {
        "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
        "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
        "NL", "PL", "PT", "RO", "SE", "SI", "SK",
    }
    _gdpr_adequate = {"AD", "AR", "CA", "CH", "FO", "GB", "GG", "IL", "IM", "JP", "JE", "NZ", "UY"}

    if (
        body.source_jurisdiction.upper() in _eu_member_states
        and body.target_jurisdiction.upper() not in _eu_member_states | _gdpr_adequate
        and PolicyDomain.GDPR in policies
    ):
        violations.append(
            PolicyViolation(
                policy=PolicyDomain.GDPR,
                rule="GDPR.Art.46",
                description=(
                    f"Transfer to '{body.target_jurisdiction}' requires appropriate "
                    "safeguards (SCCs, BCRs, or adequacy decision)."
                ),
                severity="blocking",
            )
        )
        recommendations.append(
            "Implement Standard Contractual Clauses (SCCs) before transferring personal data."
        )

    decision = (
        ComplianceDecision.BLOCKED
        if any(v.severity == "blocking" for v in violations)
        else ComplianceDecision.ALLOWED
    )

    return ComplianceCheckResponse(
        decision=decision,
        operation=body.operation,
        source_jurisdiction=body.source_jurisdiction.upper(),
        target_jurisdiction=body.target_jurisdiction.upper(),
        policies_evaluated=policies,
        violations=violations,
        recommendations=recommendations,
    )


def _infer_policies(source: str, target: str) -> list[PolicyDomain]:
    """Derive a best-guess list of applicable policy frameworks from jurisdiction codes."""
    _eu = {
        "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
        "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
        "NL", "PL", "PT", "RO", "SE", "SI", "SK",
    }
    policies: list[PolicyDomain] = []
    jurisdictions = {source.upper(), target.upper()}

    if jurisdictions & _eu:
        policies.append(PolicyDomain.GDPR)
    if jurisdictions & {"TH", "SG"}:
        policies.append(PolicyDomain.PDPA)
    if "US" in jurisdictions:
        policies.extend([PolicyDomain.FERPA, PolicyDomain.COPPA])
    if "NG" in jurisdictions:
        policies.append(PolicyDomain.NDPR)
    if "ZA" in jurisdictions:
        policies.append(PolicyDomain.POPIA)
    if "BR" in jurisdictions:
        policies.append(PolicyDomain.LGPD)

    return policies or [PolicyDomain.CUSTOM]
