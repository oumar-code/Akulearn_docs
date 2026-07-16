"""Verifiable credential router — issue and verify W3C VCs."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.credentials import (
    CredentialIssueRequest,
    CredentialIssueResponse,
    CredentialVerifyResponse,
)

router = APIRouter(prefix="/api/v1/credentials", tags=["credentials"])


# ---------------------------------------------------------------------------
# Issue
# ---------------------------------------------------------------------------


@router.post(
    "/issue",
    response_model=CredentialIssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Issue a verifiable credential",
    description=(
        "Signs and registers a new W3C Verifiable Credential for the given subject DID. "
        "Returns a compact JWT VC. JWT authentication is required at this gateway boundary."
    ),
)
async def issue_credential(
    body: CredentialIssueRequest,
    current_user: dict = Depends(get_current_user),
) -> CredentialIssueResponse:
    # TODO: integrate with VC signing service (e.g. SpruceID / DIDKit)
    credential_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    issuer_did: str = body.issuer_did or "did:web:ighub.akulearn.io"

    # Stub: real implementation calls an internal signing microservice
    signed_jwt = (
        f"eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9"
        f".STUB_{credential_id.replace('-', '')}"
        f".SIGNATURE_PLACEHOLDER"
    )

    return CredentialIssueResponse(
        credential_id=credential_id,
        credential_type=body.credential_type,
        subject_did=body.subject_did,
        issuer_did=issuer_did,
        issued_at=now,
        expiry_date=body.expiry_date,
        jwt=signed_jwt,
    )


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------


@router.get(
    "/{credential_id}/verify",
    response_model=CredentialVerifyResponse,
    summary="Verify a verifiable credential",
    description=(
        "Validates the credential signature, expiry, and revocation status. "
        "Returns a structured verification result. JWT authentication required."
    ),
)
async def verify_credential(
    credential_id: str,
    current_user: dict = Depends(get_current_user),
) -> CredentialVerifyResponse:
    # TODO: resolve credential from registry, validate signature, check revocation list
    if not credential_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="credential_id must not be empty",
        )

    # Stub: real implementation resolves the DID document and validates the JWT
    return CredentialVerifyResponse(
        credential_id=credential_id,
        valid=True,
        subject_did="did:web:subject.example",
        issuer_did="did:web:ighub.akulearn.io",
        issued_at=datetime.now(timezone.utc),
        expiry_date=None,
        revoked=False,
        failure_reason=None,
    )
