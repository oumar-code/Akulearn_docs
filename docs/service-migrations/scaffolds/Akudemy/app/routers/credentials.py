"""Credentials router — Polygon blockchain credential issuance and verification."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.credentials import (
    CredentialIssueRequest,
    CredentialIssueResponse,
    CredentialStatus,
    CredentialVerifyResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["credentials"])

# In-memory credential store (replace with persistent DB layer)
_CREDENTIAL_STORE: dict[UUID, CredentialIssueResponse] = {}


# ---------------------------------------------------------------------------
# Polygon / web3.py stub
# ---------------------------------------------------------------------------


def _issue_on_polygon(request: CredentialIssueRequest) -> str:
    """Submit a credential-mint transaction to Polygon and return the tx hash.

    This is a stub implementation. In production:
      - Instantiate Web3 with the configured RPC URL.
      - Load the issuer wallet from POLYGON_PRIVATE_KEY.
      - Call the credential NFT contract's ``mint`` function with the learner's
        wallet address and a token URI pointing to the credential metadata.
      - Return the resulting transaction hash.

    Example (production pattern)::

        from web3 import Web3

        w3 = Web3(Web3.HTTPProvider(os.environ["POLYGON_RPC_URL"]))
        account = w3.eth.account.from_key(os.environ["POLYGON_PRIVATE_KEY"])
        contract = w3.eth.contract(
            address=os.environ["CREDENTIAL_CONTRACT_ADDRESS"],
            abi=CREDENTIAL_ABI,
        )
        tx = contract.functions.mint(
            request.learner_wallet_address,
            token_uri,
        ).build_transaction({
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200_000,
        })
        signed = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    """
    # Stub: return a deterministic-looking mock hash derived from the request.
    # Polygon tx hashes are 32 bytes = 64 hex characters after the 0x prefix.
    _TX_HASH_HEX_LENGTH = 64
    mock_hash = "0x" + format(
        abs(hash(str(request.learner_wallet_address) + str(request.course_id))),
        f"0{_TX_HASH_HEX_LENGTH}x",
    )
    logger.info(
        "STUB: Would issue credential on Polygon. learner=%s course=%s mock_tx=%s",
        request.learner_wallet_address,
        request.course_id,
        mock_hash,
    )
    return mock_hash


def _build_explorer_url(tx_hash: str) -> str:
    network = os.getenv("POLYGON_NETWORK", "amoy")  # amoy = testnet, polygon = mainnet
    base = "https://amoy.polygonscan.com" if network == "amoy" else "https://polygonscan.com"
    return f"{base}/tx/{tx_hash}"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/credentials/issue",
    response_model=CredentialIssueResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Issue a blockchain credential via Polygon",
    description=(
        "Mints an on-chain credential NFT on the Polygon network. "
        "Returns immediately with a PENDING status and the transaction hash; "
        "the caller should poll /credentials/{id}/verify for confirmation."
    ),
)
async def issue_credential(payload: CredentialIssueRequest) -> CredentialIssueResponse:
    try:
        tx_hash = _issue_on_polygon(payload)
    except Exception as exc:
        logger.exception("Polygon issuance failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Credential issuance on Polygon failed. Please retry.",
        ) from exc

    credential_id = uuid4()
    now = datetime.now(tz=timezone.utc)
    response = CredentialIssueResponse(
        credential_id=credential_id,
        tx_hash=tx_hash,
        status=CredentialStatus.PENDING,
        polygon_explorer_url=_build_explorer_url(tx_hash),
        issued_at=now,
    )
    _CREDENTIAL_STORE[credential_id] = response
    return response


@router.get(
    "/credentials/{credential_id}/verify",
    response_model=CredentialVerifyResponse,
    summary="Verify an issued credential on-chain",
    description=(
        "Checks the Polygon transaction receipt for the given credential and "
        "returns the current on-chain verification status."
    ),
)
async def verify_credential(credential_id: UUID) -> CredentialVerifyResponse:
    stored = _CREDENTIAL_STORE.get(credential_id)
    if stored is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Credential {credential_id} not found.",
        )

    # Stub: in production, call w3.eth.get_transaction_receipt(stored.tx_hash)
    # and inspect the receipt status field.
    on_chain_verified = stored.tx_hash is not None

    return CredentialVerifyResponse(
        credential_id=stored.credential_id,
        status=CredentialStatus.ISSUED if on_chain_verified else CredentialStatus.PENDING,
        tx_hash=stored.tx_hash,
        issued_at=stored.issued_at,
        on_chain_verified=on_chain_verified,
    )
