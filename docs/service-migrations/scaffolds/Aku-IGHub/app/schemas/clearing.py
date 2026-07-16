"""Pydantic v2 schemas for Aku Coin financial clearing domain."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ClearingStatus(StrEnum):
    PENDING = "PENDING"
    SETTLED = "SETTLED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Settle
# ---------------------------------------------------------------------------


class ClearingSettleRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_wallet: str = Field(..., description="Source wallet DID or address")
    to_wallet: str = Field(..., description="Destination wallet DID or address")
    amount: Decimal = Field(..., gt=Decimal("0"), description="AKU Coin amount (positive)")
    currency: str = Field("AKU", description="Currency token identifier — always AKU for Aku Coin")
    reference: str | None = Field(None, description="Optional human-readable payment reference")
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Arbitrary settlement metadata"
    )


class ClearingSettleResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tx_id: str = Field(..., description="Unique clearing transaction ID")
    status: ClearingStatus
    idempotency_key: str = Field(..., description="Echo of the submitted Idempotency-Key header")
    already_processed: bool = Field(
        False,
        description="True when the idempotency key was already consumed (HTTP 200 replay)",
    )
    settled_at: datetime | None = Field(
        None, description="UTC timestamp of settlement; None while PENDING"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Transaction status
# ---------------------------------------------------------------------------


class ClearingTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tx_id: str
    status: ClearingStatus
    from_wallet: str
    to_wallet: str
    amount: Decimal
    currency: str
    reference: str | None = None
    idempotency_key: str
    created_at: datetime
    settled_at: datetime | None = None
    failed_reason: str | None = Field(
        None, description="Human-readable failure reason when status=FAILED"
    )
