"""Aku Coin financial clearing router — idempotent settlement and status."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.clearing import (
    ClearingSettleRequest,
    ClearingSettleResponse,
    ClearingStatus,
    ClearingTransactionResponse,
)

router = APIRouter(prefix="/api/v1/clearing", tags=["clearing"])

# ---------------------------------------------------------------------------
# In-memory idempotency store — replace with Redis / DB in production
# ---------------------------------------------------------------------------

_idempotency_store: dict[str, ClearingSettleResponse] = {}
_idempotency_requests: dict[str, ClearingSettleRequest] = {}  # mirrors store for status replay


def _get_idempotency_key(
    idempotency_key: Annotated[
        str,
        Header(
            alias="Idempotency-Key",
            description=(
                "Client-generated unique key (UUID v4 recommended) that makes this "
                "request idempotent. Identical keys within the retention window replay "
                "the original response with HTTP 200 instead of HTTP 201."
            ),
        ),
    ],
) -> str:
    if not idempotency_key.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header must not be blank.",
        )
    return idempotency_key


# ---------------------------------------------------------------------------
# Settle
# ---------------------------------------------------------------------------


@router.post(
    "/settle",
    response_model=ClearingSettleResponse,
    summary="Settle an Aku Coin clearing transaction (idempotent)",
    description=(
        "Initiates or replays an Aku Coin financial clearing operation. "
        "Provide a unique **Idempotency-Key** header per logical transaction. "
        "If the key has already been processed the original response is returned "
        "with HTTP 200 (no double-debit). New settlements return HTTP 201."
    ),
    responses={
        status.HTTP_201_CREATED: {"description": "New clearing transaction accepted"},
        status.HTTP_200_OK: {"description": "Idempotent replay — transaction already processed"},
    },
)
async def settle_clearing(
    body: ClearingSettleRequest,
    idempotency_key: str = Depends(_get_idempotency_key),
    current_user: dict = Depends(get_current_user),
) -> ClearingSettleResponse:
    from fastapi.responses import JSONResponse  # local import to attach dynamic status

    # --- Idempotency check ---
    if idempotency_key in _idempotency_store:
        cached = _idempotency_store[idempotency_key]
        # Return 200 to signal replay; mutate already_processed flag on a copy
        replay = cached.model_copy(update={"already_processed": True})
        return JSONResponse(  # type: ignore[return-value]
            status_code=status.HTTP_200_OK,
            content=replay.model_dump(mode="json"),
        )

    # --- New transaction ---
    # TODO: call internal ledger service to debit/credit wallets atomically
    tx_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    result = ClearingSettleResponse(
        tx_id=tx_id,
        status=ClearingStatus.SETTLED,
        idempotency_key=idempotency_key,
        already_processed=False,
        settled_at=now,
        created_at=now,
    )

    _idempotency_store[idempotency_key] = result
    _idempotency_requests[idempotency_key] = body
    return result  # FastAPI uses status_code=201 from the decorator


# ---------------------------------------------------------------------------
# Transaction status
# ---------------------------------------------------------------------------


@router.get(
    "/{tx_id}",
    response_model=ClearingTransactionResponse,
    summary="Get clearing transaction status",
    description="Retrieve the current status and details of a clearing transaction by its ID.",
)
async def get_clearing_status(
    tx_id: str,
    current_user: dict = Depends(get_current_user),
) -> ClearingTransactionResponse:
    # TODO: query persistent ledger store
    # Stub: look up from idempotency store for demonstration
    for idem_key, record in _idempotency_store.items():
        if record.tx_id == tx_id:
            req = _idempotency_requests.get(idem_key)
            return ClearingTransactionResponse(
                tx_id=record.tx_id,
                status=record.status,
                from_wallet=req.from_wallet if req else "unknown",
                to_wallet=req.to_wallet if req else "unknown",
                amount=req.amount if req else "0.00",
                currency=req.currency if req else "AKU",
                reference=req.reference if req else None,
                idempotency_key=record.idempotency_key,
                created_at=record.created_at,
                settled_at=record.settled_at,
                failed_reason=None,
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Clearing transaction '{tx_id}' not found.",
    )
