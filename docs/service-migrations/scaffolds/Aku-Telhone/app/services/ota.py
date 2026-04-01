"""OTA push background task service.

OTAService.push_profile() is designed to be launched with asyncio.create_task()
from an endpoint handler, returning HTTP 202 Accepted immediately while the
long-running OTA delivery proceeds in the background event loop.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-process task registry
# ---------------------------------------------------------------------------
# Maps task_id → metadata dict.  Replace with Redis / DB in production.
_task_registry: dict[str, dict[str, Any]] = {}


def get_task_status(task_id: str) -> dict[str, Any] | None:
    """Return the current status record for a background OTA task, or None."""
    return _task_registry.get(task_id)


# ---------------------------------------------------------------------------
# Simulated profile store
# ---------------------------------------------------------------------------
# Keyed by iccid → profile dict.  Replace with async DB session in production.
_profile_store: dict[str, dict[str, Any]] = {}


def _upsert_profile(iccid: str, **updates: Any) -> None:
    """Merge updates into the in-process profile store."""
    existing = _profile_store.setdefault(iccid, {})
    existing.update(updates)


def get_profile(iccid: str) -> dict[str, Any] | None:
    """Retrieve a stored profile by ICCID."""
    return _profile_store.get(iccid)


# ---------------------------------------------------------------------------
# OTAService
# ---------------------------------------------------------------------------


class OTAService:
    """Handles over-the-air profile delivery for eSIM profiles.

    All public methods are coroutines and are safe to run as background tasks.
    """

    # Simulated delivery window in seconds (replace with real MVNO SDK calls).
    _OTA_SIMULATED_DELAY: float = 5.0

    async def push_profile(
        self,
        *,
        iccid: str,
        task_id: str,
        payload_type: str = "PROFILE_UPDATE",
        payload: dict[str, Any] | None = None,
        priority: int = 5,
    ) -> None:
        """Execute an OTA profile push for the given ICCID.

        This coroutine is meant to be wrapped with asyncio.create_task().
        It updates the task registry on start, completion, and failure so
        callers can poll for status.

        Args:
            iccid: The target eSIM profile identifier.
            task_id: Caller-supplied task identifier (for status polling).
            payload_type: OTA payload class (PROFILE_UPDATE, CONFIG_DELTA, …).
            payload: Opaque payload forwarded to the MVNO OTA platform.
            priority: Delivery priority (1–10; higher = more urgent).
        """
        _task_registry[task_id] = {
            "task_id": task_id,
            "iccid": iccid,
            "status": "IN_PROGRESS",
            "payload_type": payload_type,
            "priority": priority,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "error": None,
        }

        try:
            logger.info(
                "OTA push %s starting — iccid=%s type=%s priority=%d",
                task_id,
                iccid,
                payload_type,
                priority,
            )

            # --- Simulate MVNO OTA platform latency ---
            # Real implementation: call MVNO OTA REST/SOAP API, poll for
            # delivery confirmation, handle retries with exponential back-off.
            await asyncio.sleep(self._OTA_SIMULATED_DELAY)

            now = datetime.now(timezone.utc)

            # Update the in-process profile store
            _upsert_profile(
                iccid,
                last_ota_push_at=now.isoformat(),
                status="ACTIVE",
            )

            _task_registry[task_id].update(
                {
                    "status": "COMPLETED",
                    "completed_at": now.isoformat(),
                }
            )

            logger.info("OTA push %s completed — iccid=%s", task_id, iccid)

        except Exception as exc:  # noqa: BLE001
            logger.exception("OTA push %s failed — iccid=%s error=%s", task_id, iccid, exc)
            _task_registry[task_id].update(
                {
                    "status": "FAILED",
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "error": str(exc),
                }
            )

    async def switch_network(
        self,
        *,
        iccid: str,
        task_id: str,
        target_network: str,
        target_plan_id: str | None = None,
    ) -> None:
        """Execute an OTA network-switch for the given ICCID.

        Sets the profile status to SWITCHING on start and ACTIVE on completion.
        Designed to be launched via asyncio.create_task().
        """
        _task_registry[task_id] = {
            "task_id": task_id,
            "iccid": iccid,
            "status": "IN_PROGRESS",
            "operation": "NETWORK_SWITCH",
            "target_network": target_network,
            "target_plan_id": target_plan_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "error": None,
        }

        _upsert_profile(iccid, status="SWITCHING")

        try:
            logger.info(
                "OTA network-switch %s starting — iccid=%s target=%s",
                task_id,
                iccid,
                target_network,
            )

            # Simulate MVNO network reconfiguration latency
            await asyncio.sleep(self._OTA_SIMULATED_DELAY)

            now = datetime.now(timezone.utc)

            updates: dict[str, Any] = {
                "status": "ACTIVE",
                "preferred_network": target_network,
                "last_ota_push_at": now.isoformat(),
            }
            if target_plan_id:
                updates["plan_id"] = target_plan_id

            _upsert_profile(iccid, **updates)

            _task_registry[task_id].update(
                {
                    "status": "COMPLETED",
                    "completed_at": now.isoformat(),
                }
            )

            logger.info("OTA network-switch %s completed — iccid=%s", task_id, iccid)

        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "OTA network-switch %s failed — iccid=%s error=%s",
                task_id,
                iccid,
                exc,
            )
            # Revert profile status so it is not left in SWITCHING forever
            _upsert_profile(iccid, status="ACTIVE")
            _task_registry[task_id].update(
                {
                    "status": "FAILED",
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "error": str(exc),
                }
            )


# Module-level singleton — import and reuse across request handlers.
ota_service = OTAService()


def new_task_id() -> str:
    """Generate a unique task identifier for OTA background jobs."""
    return f"ota-{uuid.uuid4()}"
