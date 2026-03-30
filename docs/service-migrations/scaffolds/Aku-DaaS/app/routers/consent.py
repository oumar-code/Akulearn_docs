"""Consent record management router."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.schemas.consent import ConsentPurpose, ConsentRecord, ConsentResponse, ConsentUpsertRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/consent", tags=["consent"])


# ---------------------------------------------------------------------------
# In-memory consent store (replace with persistent DB in production)
# ---------------------------------------------------------------------------

_consent_store: dict[str, ConsentRecord] = {}


# ---------------------------------------------------------------------------
# GET /api/v1/consent/{user_id}
# ---------------------------------------------------------------------------


@router.get(
    "/{user_id}",
    response_model=ConsentResponse,
    summary="Get user consent record",
    description=(
        "Retrieve the current consent record for a user. "
        "Returns 404 if no consent record exists — clients should treat absence "
        "as implicit withdrawal and prompt the user to set preferences."
    ),
)
async def get_consent(user_id: str) -> ConsentResponse:
    record = _consent_store.get(user_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"No consent record found for user '{user_id}'. "
                "Treat absence as consent_given=False."
            ),
        )
    return ConsentResponse(
        user_id=record.user_id,
        consent_given=record.consent_given,
        consent_for=record.consent_for,
        jurisdiction=record.jurisdiction,
        updated_at=record.updated_at,
        is_new=False,
    )


# ---------------------------------------------------------------------------
# POST /api/v1/consent/{user_id}
# ---------------------------------------------------------------------------


@router.post(
    "/{user_id}",
    response_model=ConsentResponse,
    status_code=status.HTTP_200_OK,
    summary="Create or update user consent record",
    description=(
        "Upsert the consent record for a user. "
        "When `consent_given` is **False**, `consent_for` is automatically cleared "
        "regardless of the submitted value — a withdrawal applies to all purposes. "
        "Responds with 200 (update) or 201 (new record) via the `is_new` flag."
    ),
    responses={status.HTTP_201_CREATED: {"description": "Consent record created"}},
)
async def upsert_consent(
    user_id: str,
    body: ConsentUpsertRequest,
) -> ConsentResponse:
    is_new = user_id not in _consent_store
    now = datetime.now(timezone.utc)

    # Consent withdrawal clears all granular purposes
    effective_purposes: list[ConsentPurpose] = body.consent_for if body.consent_given else []

    record = ConsentRecord(
        user_id=user_id,
        consent_given=body.consent_given,
        consent_for=effective_purposes,
        jurisdiction=body.jurisdiction,
        updated_at=now,
    )
    _consent_store[user_id] = record

    logger.info(
        "consent.upsert user_id=%s consent_given=%s purposes=%s jurisdiction=%s is_new=%s",
        user_id,
        body.consent_given,
        [p.value for p in effective_purposes],
        body.jurisdiction,
        is_new,
    )

    return ConsentResponse(
        user_id=user_id,
        consent_given=record.consent_given,
        consent_for=record.consent_for,
        jurisdiction=record.jurisdiction,
        updated_at=now,
        is_new=is_new,
    )
