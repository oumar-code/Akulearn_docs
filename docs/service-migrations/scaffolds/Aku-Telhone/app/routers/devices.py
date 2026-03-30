"""Devices router — device attestation via Aku-IGHub.

POST /api/v1/devices/{id}/attest
  Forwards the device attestation token to Aku-IGHub for verification.
  Returns a structured attestation result including trust level.
"""

from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.schemas.esim import DeviceAttestRequest, DeviceAttestResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])

_IGHUB_ATTEST_PATH = "/api/v1/devices/attest"


# ---------------------------------------------------------------------------
# POST /api/v1/devices/{id}/attest
# ---------------------------------------------------------------------------


@router.post(
    "/{device_id}/attest",
    response_model=DeviceAttestResponse,
    summary="Attest a device via Aku-IGHub",
    description=(
        "Forwards the device attestation token (Android Key Attestation, "
        "Apple DeviceCheck, or embedded platform token) to Aku-IGHub for "
        "cryptographic verification. "
        "Returns the trust level assigned by IGHub: FULL | LIMITED | UNTRUSTED. "
        "An attested device is a prerequisite for eSIM provisioning in production."
    ),
)
async def attest_device(device_id: str, body: DeviceAttestRequest) -> DeviceAttestResponse:
    if body.device_id != device_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Path device_id and body device_id must match",
        )

    payload = {
        "device_id": device_id,
        "attestation_token": body.attestation_token,
        "platform": body.platform,
        "firmware_hash": body.firmware_hash,
        "requester_service": "aku-telhone",
    }

    try:
        async with httpx.AsyncClient(
            base_url=settings.aku_ighub_url,
            timeout=settings.ighub_timeout_seconds,
            headers={
                "X-Api-Key": settings.aku_ighub_api_key,
                "X-Service-Name": "aku-telhone",
            },
        ) as client:
            resp = await client.post(_IGHUB_ATTEST_PATH, json=payload)
            resp.raise_for_status()
            data: dict = resp.json()

    except httpx.HTTPStatusError as exc:
        logger.warning(
            "IGHub attestation rejected device_id=%s status=%d",
            device_id,
            exc.response.status_code,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"IGHub returned {exc.response.status_code}: {exc.response.text[:200]}",
        ) from exc

    except httpx.RequestError as exc:
        logger.error("Cannot reach Aku-IGHub for device attestation: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Aku-IGHub is unreachable — device attestation unavailable",
        ) from exc

    return DeviceAttestResponse(
        device_id=device_id,
        attested=data.get("attested", False),
        trust_level=data.get("trust_level"),
        reason=data.get("reason"),
        ighub_ref=data.get("ref") or data.get("ighub_ref"),
    )
