"""Comprehensive API tests for Aku-Telhone eSIM lifecycle and device attestation."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

_DEVICE_ID = "device-test-001"
_IMEI = "490154203237518"
_EID = "89049032004008882600190520680736"
_PLAN_ID = "aku-edu-basic"

_PROVISION_PAYLOAD = {
    "device_id": _DEVICE_ID,
    "imei": _IMEI,
    "eid": _EID,
    "preferred_network": "LTE",
    "plan_id": _PLAN_ID,
}


# ---------------------------------------------------------------------------
# Test isolation — clear in-memory stores between tests
# ---------------------------------------------------------------------------


async def _reset_stores() -> None:
    import app.services.ota as _ota

    _ota._profile_store.clear()
    _ota._task_registry.clear()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Aku-Telhone"


# ---------------------------------------------------------------------------
# POST /api/v1/esim/provision
# ---------------------------------------------------------------------------


async def test_provision_esim_returns_201_with_iccid(client: AsyncClient) -> None:
    await _reset_stores()
    response = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert "iccid" in data
    assert data["iccid"].startswith("89234")
    assert data["device_id"] == _DEVICE_ID
    assert data["status"] == "PENDING"
    assert data["activation_code"].startswith("AC$")
    assert "qr_code_url" in data
    assert data["plan_id"] == _PLAN_ID


async def test_provision_esim_is_idempotent_for_same_eid(client: AsyncClient) -> None:
    await _reset_stores()
    r1 = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    r2 = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    # Both succeed; the ICCID is deterministic from EID
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.json()["iccid"] == r2.json()["iccid"]


async def test_provision_esim_rejects_non_digit_imei(client: AsyncClient) -> None:
    payload = {**_PROVISION_PAYLOAD, "imei": "ABCDE1234567890"}
    response = await client.post("/api/v1/esim/provision", json=payload)
    assert response.status_code == 422


async def test_provision_esim_rejects_short_imei(client: AsyncClient) -> None:
    payload = {**_PROVISION_PAYLOAD, "imei": "12345"}
    response = await client.post("/api/v1/esim/provision", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/esim/{iccid}
# ---------------------------------------------------------------------------


async def test_get_esim_profile_returns_status(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    get_resp = await client.get(f"/api/v1/esim/{iccid}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["iccid"] == iccid
    assert data["status"] == "PENDING"
    assert data["plan_id"] == _PLAN_ID


async def test_get_esim_profile_404_for_unknown_iccid(client: AsyncClient) -> None:
    response = await client.get("/api/v1/esim/8923400000000000000")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /api/v1/esim/{iccid}/switch-network
# ---------------------------------------------------------------------------


async def test_switch_network_returns_202_accepted(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    switch_resp = await client.patch(
        f"/api/v1/esim/{iccid}/switch-network",
        json={"target_network": "5G", "target_plan_id": "aku-edu-premium"},
    )
    assert switch_resp.status_code == 202
    data = switch_resp.json()
    assert data["iccid"] == iccid
    assert data["status"] == "SWITCHING"
    assert "task_id" in data


async def test_switch_network_404_for_unknown_iccid(client: AsyncClient) -> None:
    response = await client.patch(
        "/api/v1/esim/unknown-iccid-xyz/switch-network",
        json={"target_network": "LTE"},
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /api/v1/esim/{iccid}
# ---------------------------------------------------------------------------


async def test_deactivate_esim_returns_200(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    deactivate_resp = await client.delete(f"/api/v1/esim/{iccid}")
    assert deactivate_resp.status_code == 200
    data = deactivate_resp.json()
    assert data["iccid"] == iccid
    assert data["status"] == "DEACTIVATED"


async def test_deactivate_esim_409_when_already_deactivated(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    await client.delete(f"/api/v1/esim/{iccid}")
    second = await client.delete(f"/api/v1/esim/{iccid}")
    assert second.status_code == 409


async def test_deactivate_esim_404_for_unknown_iccid(client: AsyncClient) -> None:
    response = await client.delete("/api/v1/esim/unknown-iccid-xyz")
    assert response.status_code == 404


async def test_switch_network_409_on_deactivated_profile(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]
    await client.delete(f"/api/v1/esim/{iccid}")

    resp = await client.patch(
        f"/api/v1/esim/{iccid}/switch-network",
        json={"target_network": "LTE"},
    )
    assert resp.status_code == 409


# ---------------------------------------------------------------------------
# POST /api/v1/esim/{iccid}/ota-push
# ---------------------------------------------------------------------------


async def test_ota_push_returns_202_accepted(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    push_resp = await client.post(
        f"/api/v1/esim/{iccid}/ota-push",
        json={"payload_type": "CONFIG_DELTA", "payload": {"apn": "akulearn.mno"}, "priority": 7},
    )
    assert push_resp.status_code == 202
    data = push_resp.json()
    assert data["iccid"] == iccid
    assert data["status"] == "QUEUED"
    assert "task_id" in data


async def test_ota_push_404_for_unknown_iccid(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/esim/unknown-xyz/ota-push",
        json={"payload_type": "PROFILE_UPDATE"},
    )
    assert response.status_code == 404


async def test_ota_push_409_on_deactivated_profile(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]
    await client.delete(f"/api/v1/esim/{iccid}")

    resp = await client.post(
        f"/api/v1/esim/{iccid}/ota-push",
        json={"payload_type": "PROFILE_UPDATE"},
    )
    assert resp.status_code == 409


async def test_ota_push_rejects_invalid_priority(client: AsyncClient) -> None:
    await _reset_stores()
    prov = await client.post("/api/v1/esim/provision", json=_PROVISION_PAYLOAD)
    iccid = prov.json()["iccid"]

    resp = await client.post(
        f"/api/v1/esim/{iccid}/ota-push",
        json={"payload_type": "PROFILE_UPDATE", "priority": 0},  # ge=1
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/devices/{id}/attest — mock IGHub call
# ---------------------------------------------------------------------------


async def test_attest_device_returns_200_with_mocked_ighub(client: AsyncClient) -> None:
    import httpx
    from unittest.mock import MagicMock

    mock_response_data = {
        "attested": True,
        "trust_level": "FULL",
        "reason": None,
        "ref": "ighub-ref-abc123",
    }

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = mock_response_data

    mock_client_instance = AsyncMock()
    mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_client_instance.__aexit__ = AsyncMock(return_value=None)
    mock_client_instance.post = AsyncMock(return_value=mock_resp)

    with patch("app.routers.devices.httpx.AsyncClient", return_value=mock_client_instance):
        resp = await client.post(
            f"/api/v1/devices/{_DEVICE_ID}/attest",
            json={
                "device_id": _DEVICE_ID,
                "attestation_token": "token-abc123",
                "platform": "android",
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["device_id"] == _DEVICE_ID
    assert data["attested"] is True
    assert data["trust_level"] == "FULL"


async def test_attest_device_422_when_path_body_id_mismatch(client: AsyncClient) -> None:
    resp = await client.post(
        f"/api/v1/devices/{_DEVICE_ID}/attest",
        json={
            "device_id": "different-device",
            "attestation_token": "tok",
            "platform": "android",
        },
    )
    assert resp.status_code == 422
