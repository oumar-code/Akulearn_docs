"""Pydantic v2 schemas for the eSIM provisioning and MVNO connectivity domain."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class ESIMStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SWITCHING = "SWITCHING"
    DEACTIVATED = "DEACTIVATED"


class NetworkTechnology(StrEnum):
    LTE = "LTE"
    LTE_M = "LTE-M"
    NB_IOT = "NB-IoT"
    FIVE_G = "5G"


# ---------------------------------------------------------------------------
# Provision
# ---------------------------------------------------------------------------


class ESIMProvisionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(..., description="Unique identifier of the target device")
    imei: str = Field(
        ...,
        min_length=15,
        max_length=15,
        description="15-digit IMEI of the device requesting eSIM provisioning",
    )
    eid: str = Field(
        ...,
        description="eUICC Identifier (EID) embedded in the device's eSIM chip",
    )
    preferred_network: NetworkTechnology = Field(
        NetworkTechnology.LTE,
        description="Preferred radio access technology for the provisioned profile",
    )
    plan_id: str = Field(..., description="MVNO data-plan identifier to associate with the profile")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional free-form provisioning context (carrier region, device model, etc.)",
    )

    @field_validator("imei")
    @classmethod
    def imei_must_be_digits(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("IMEI must contain only digits")
        return v


class ESIMProvisionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    iccid: str = Field(..., description="Integrated Circuit Card Identifier — unique profile ID")
    eid: str = Field(..., description="eUICC Identifier the profile was provisioned to")
    device_id: str
    status: ESIMStatus = ESIMStatus.PENDING
    activation_code: str = Field(
        ...,
        description="LPA activation code (AC$ format) used by the device to download the profile",
    )
    qr_code_url: str = Field(
        ...,
        description="URL to the scannable QR code that encodes the activation code",
    )
    plan_id: str
    preferred_network: NetworkTechnology
    provisioned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Profile status
# ---------------------------------------------------------------------------


class ESIMProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    iccid: str
    eid: str
    device_id: str
    status: ESIMStatus
    plan_id: str
    preferred_network: NetworkTechnology
    provisioned_at: datetime
    activated_at: datetime | None = None
    last_ota_push_at: datetime | None = None
    deactivated_at: datetime | None = None


# ---------------------------------------------------------------------------
# Network switch (OTA)
# ---------------------------------------------------------------------------


class NetworkSwitchRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    target_network: NetworkTechnology = Field(
        ...,
        description="Network technology to switch the eSIM profile to via OTA",
    )
    target_plan_id: str | None = Field(
        None,
        description="Optional new MVNO plan to associate after the network switch",
    )
    reason: str | None = Field(
        None,
        max_length=512,
        description="Human-readable reason for the network switch (audit log)",
    )


class NetworkSwitchAccepted(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    iccid: str
    status: ESIMStatus = ESIMStatus.SWITCHING
    task_id: str = Field(..., description="Background task identifier for status polling")
    message: str = (
        "OTA network switch initiated — profile status will update to ACTIVE when complete"
    )
    accepted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# OTA push
# ---------------------------------------------------------------------------


class OTAPushRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    payload_type: str = Field(
        "PROFILE_UPDATE",
        description="OTA payload class: PROFILE_UPDATE | CONFIG_DELTA | DIAGNOSTICS",
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Opaque OTA payload forwarded to the MVNO OTA platform",
    )
    priority: int = Field(
        5,
        ge=1,
        le=10,
        description="Delivery priority (1 = low, 10 = urgent)",
    )


class OTAPushAccepted(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    iccid: str
    task_id: str = Field(..., description="Background task identifier for the OTA push job")
    status: str = "QUEUED"
    message: str = "OTA push queued — delivery will complete asynchronously"
    queued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Deactivation
# ---------------------------------------------------------------------------


class ESIMDeactivateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    iccid: str
    status: ESIMStatus = ESIMStatus.DEACTIVATED
    deactivated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = "eSIM profile deactivated successfully"


# ---------------------------------------------------------------------------
# Device attestation (delegates to Aku-IGHub)
# ---------------------------------------------------------------------------


class DeviceAttestRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(..., description="Device identifier to attest")
    attestation_token: str = Field(
        ...,
        description="Platform attestation token (e.g. Android Key Attestation, Apple DeviceCheck)",
    )
    platform: str = Field(
        ...,
        description="Device platform: android | ios | embedded",
    )
    firmware_hash: str | None = Field(
        None,
        description="Optional SHA-256 of the current firmware image for integrity verification",
    )


class DeviceAttestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str
    attested: bool = Field(..., description="True when Aku-IGHub confirmed the device attestation")
    trust_level: str | None = Field(
        None,
        description="Trust tier returned by IGHub: FULL | LIMITED | UNTRUSTED",
    )
    reason: str | None = Field(None, description="Human-readable explanation when attested=False")
    attested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ighub_ref: str | None = Field(
        None,
        description="Reference ID assigned by Aku-IGHub for audit correlation",
    )
