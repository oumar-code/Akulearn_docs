"""eSIM provisioning router.

Implements the full eSIM profile lifecycle:
  - Provision a new profile (POST /provision)
  - Retrieve profile status (GET /{iccid})
  - Trigger OTA network switch, returns 202 Accepted (PATCH /{iccid}/switch-network)
  - Deactivate a profile (DELETE /{iccid})
  - Trigger a direct OTA push, returns 202 Accepted (POST /{iccid}/ota-push)

OTA operations are fired as asyncio background tasks so the HTTP response is
returned immediately while delivery proceeds in the event loop.
"""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.esim import (
    ESIMDeactivateResponse,
    ESIMProfileResponse,
    ESIMProvisionRequest,
    ESIMProvisionResponse,
    ESIMStatus,
    NetworkSwitchAccepted,
    NetworkSwitchRequest,
    OTAPushAccepted,
    OTAPushRequest,
)
from app.services.esim import esim_service
from app.services.ota import new_task_id, ota_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/esim", tags=["esim"])


# ---------------------------------------------------------------------------
# POST /api/v1/esim/provision
# ---------------------------------------------------------------------------


@router.post(
    "/provision",
    response_model=ESIMProvisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Provision a new eSIM profile",
    description=(
        "Allocates a new eSIM profile via the MVNO SM-DP+ platform. "
        "Returns the ICCID, LPA activation code, and QR code URL required by the device "
        "to download the profile. Profile status is initially PENDING until the device "
        "completes profile download and activates."
    ),
)
async def provision_esim(body: ESIMProvisionRequest) -> ESIMProvisionResponse:
    try:
        return await esim_service.provision(body)
    except Exception as exc:
        logger.exception("eSIM provisioning failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Provisioning failed: {exc}",
        ) from exc


# ---------------------------------------------------------------------------
# GET /api/v1/esim/{iccid}
# ---------------------------------------------------------------------------


@router.get(
    "/{iccid}",
    response_model=ESIMProfileResponse,
    summary="Get eSIM profile status",
    description=(
        "Returns the current state of an eSIM profile identified by its ICCID. "
        "Possible statuses: PENDING | ACTIVE | SWITCHING | DEACTIVATED."
    ),
)
async def get_esim_profile(iccid: str) -> ESIMProfileResponse:
    try:
        return await esim_service.get_profile(iccid)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"eSIM profile '{iccid}' not found",
        )


# ---------------------------------------------------------------------------
# PATCH /api/v1/esim/{iccid}/switch-network
# ---------------------------------------------------------------------------


@router.patch(
    "/{iccid}/switch-network",
    response_model=NetworkSwitchAccepted,
    status_code=status.HTTP_202_ACCEPTED,
    summary="OTA network switch (MVNO)",
    description=(
        "Initiates an over-the-air network switch for the eSIM profile. "
        "Sets profile status to SWITCHING and returns 202 Accepted immediately. "
        "The switch completes asynchronously; poll GET /{iccid} to confirm ACTIVE status."
    ),
)
async def switch_network(iccid: str, body: NetworkSwitchRequest) -> NetworkSwitchAccepted:
    try:
        await esim_service.get_profile(iccid)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"eSIM profile '{iccid}' not found",
        )

    if await esim_service.is_deactivated(iccid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot switch network on a deactivated eSIM profile",
        )

    task_id = new_task_id()

    asyncio.create_task(
        ota_service.switch_network(
            iccid=iccid,
            task_id=task_id,
            target_network=body.target_network.value,
            target_plan_id=body.target_plan_id,
        ),
        name=f"ota-network-switch-{iccid}",
    )

    logger.info("Network switch task %s queued for iccid=%s", task_id, iccid)

    return NetworkSwitchAccepted(
        iccid=iccid,
        status=ESIMStatus.SWITCHING,
        task_id=task_id,
    )


# ---------------------------------------------------------------------------
# DELETE /api/v1/esim/{iccid}
# ---------------------------------------------------------------------------


@router.delete(
    "/{iccid}",
    response_model=ESIMDeactivateResponse,
    summary="Deactivate an eSIM profile",
    description=(
        "Permanently deactivates the eSIM profile and notifies the MVNO. "
        "A deactivated profile cannot be reactivated — provision a new profile if needed."
    ),
)
async def deactivate_esim(iccid: str) -> ESIMDeactivateResponse:
    try:
        return await esim_service.deactivate(iccid)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"eSIM profile '{iccid}' not found",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------------------------
# POST /api/v1/esim/{iccid}/ota-push
# ---------------------------------------------------------------------------


@router.post(
    "/{iccid}/ota-push",
    response_model=OTAPushAccepted,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger a direct OTA push",
    description=(
        "Enqueues an OTA payload delivery to the eSIM profile. "
        "Returns 202 Accepted immediately; the push executes as a background task. "
        "Use the task_id to correlate logs or poll an internal status endpoint."
    ),
)
async def trigger_ota_push(iccid: str, body: OTAPushRequest) -> OTAPushAccepted:
    try:
        await esim_service.get_profile(iccid)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"eSIM profile '{iccid}' not found",
        )

    if await esim_service.is_deactivated(iccid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot push OTA to a deactivated eSIM profile",
        )

    task_id = new_task_id()

    asyncio.create_task(
        ota_service.push_profile(
            iccid=iccid,
            task_id=task_id,
            payload_type=body.payload_type,
            payload=body.payload,
            priority=body.priority,
        ),
        name=f"ota-push-{iccid}",
    )

    logger.info("OTA push task %s queued for iccid=%s type=%s", task_id, iccid, body.payload_type)

    return OTAPushAccepted(
        iccid=iccid,
        task_id=task_id,
    )
