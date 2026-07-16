"""eSIM provisioning service — business logic layer.

Owns profile lifecycle: provision, status lookup, and deactivation.
OTA operations are delegated to app.services.ota.OTAService.
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.schemas.esim import (
    ESIMDeactivateResponse,
    ESIMProfileResponse,
    ESIMProvisionRequest,
    ESIMProvisionResponse,
    ESIMStatus,
    NetworkTechnology,
)
from app.services.ota import _profile_store, _upsert_profile

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ICCID / activation-code generators
# ---------------------------------------------------------------------------


def _generate_iccid(eid: str) -> str:
    """Derive a deterministic, MCC-prefixed 20-digit ICCID stub from EID.

    Real implementation: allocate from the MVNO's ICCID pool via API.
    Format: 89 (telecom) + 234 (MCC/MNC stub) + 13 digits from EID hash.
    """
    digest = hashlib.sha256(eid.encode()).hexdigest()
    numeric_suffix = "".join(c for c in digest if c.isdigit())[:13].ljust(13, "0")
    return f"89234{numeric_suffix}"


def _generate_activation_code(iccid: str) -> str:
    """Return an LPA activation code (AC$-prefixed) for the profile.

    Real implementation: obtained from the MVNO SM-DP+ server.
    """
    token = uuid.uuid5(uuid.NAMESPACE_URL, f"telhone:{iccid}").hex.upper()
    return f"AC${token}"


def _qr_code_url(iccid: str, activation_code: str) -> str:
    """Return the URL of the QR code image for this activation code.

    Real implementation: call the QR generation service or SM-DP+ endpoint.
    """
    slug = activation_code.replace("$", "").replace("-", "")
    return f"{settings.qr_base_url}/esim/{iccid}/{slug}.png"


# ---------------------------------------------------------------------------
# ESIMService
# ---------------------------------------------------------------------------


class ESIMService:
    """Manages eSIM profile provisioning and lifecycle."""

    async def provision(self, request: ESIMProvisionRequest) -> ESIMProvisionResponse:
        """Provision a new eSIM profile and persist it in the profile store.

        Returns the ICCID, activation code, and QR code URL required by
        the device to download the profile via LPA.
        """
        iccid = _generate_iccid(request.eid)

        if iccid in _profile_store:
            logger.warning(
                "Duplicate provisioning request for EID %s (iccid=%s)", request.eid, iccid
            )

        activation_code = _generate_activation_code(iccid)
        qr_code_url = _qr_code_url(iccid, activation_code)
        now = datetime.now(timezone.utc)

        _upsert_profile(
            iccid,
            iccid=iccid,
            eid=request.eid,
            device_id=request.device_id,
            imei=request.imei,
            status=ESIMStatus.PENDING,
            plan_id=request.plan_id,
            preferred_network=request.preferred_network,
            activation_code=activation_code,
            qr_code_url=qr_code_url,
            provisioned_at=now.isoformat(),
            activated_at=None,
            last_ota_push_at=None,
            deactivated_at=None,
            metadata=request.metadata,
        )

        logger.info("Provisioned eSIM iccid=%s device_id=%s", iccid, request.device_id)

        return ESIMProvisionResponse(
            iccid=iccid,
            eid=request.eid,
            device_id=request.device_id,
            status=ESIMStatus.PENDING,
            activation_code=activation_code,
            qr_code_url=qr_code_url,
            plan_id=request.plan_id,
            preferred_network=request.preferred_network,
            provisioned_at=now,
        )

    async def get_profile(self, iccid: str) -> ESIMProfileResponse:
        """Return the current profile record for the given ICCID.

        Raises KeyError when the ICCID is not found — callers should map
        this to HTTP 404.
        """
        record = _profile_store.get(iccid)
        if record is None:
            raise KeyError(iccid)

        return self._record_to_response(record)

    async def is_deactivated(self, iccid: str) -> bool:
        """Return True when the profile exists and has DEACTIVATED status."""
        record = _profile_store.get(iccid)
        return record is not None and record.get("status") == ESIMStatus.DEACTIVATED

    async def deactivate(self, iccid: str) -> ESIMDeactivateResponse:
        """Mark the eSIM profile as DEACTIVATED.

        Raises KeyError when the ICCID is not found.
        Raises ValueError when the profile is already deactivated.
        """
        record = _profile_store.get(iccid)
        if record is None:
            raise KeyError(iccid)

        if record.get("status") == ESIMStatus.DEACTIVATED:
            raise ValueError(f"eSIM profile {iccid!r} is already deactivated")

        now = datetime.now(timezone.utc)
        _upsert_profile(iccid, status=ESIMStatus.DEACTIVATED, deactivated_at=now.isoformat())

        logger.info("Deactivated eSIM iccid=%s", iccid)

        return ESIMDeactivateResponse(
            iccid=iccid,
            status=ESIMStatus.DEACTIVATED,
            deactivated_at=now,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _record_to_response(record: dict[str, Any]) -> ESIMProfileResponse:
        def _dt(val: str | None) -> datetime | None:
            return datetime.fromisoformat(val) if val else None

        return ESIMProfileResponse(
            iccid=record["iccid"],
            eid=record["eid"],
            device_id=record["device_id"],
            status=ESIMStatus(record["status"]),
            plan_id=record["plan_id"],
            preferred_network=NetworkTechnology(record["preferred_network"]),
            provisioned_at=datetime.fromisoformat(record["provisioned_at"]),
            activated_at=_dt(record.get("activated_at")),
            last_ota_push_at=_dt(record.get("last_ota_push_at")),
            deactivated_at=_dt(record.get("deactivated_at")),
        )


# Module-level singleton
esim_service = ESIMService()
