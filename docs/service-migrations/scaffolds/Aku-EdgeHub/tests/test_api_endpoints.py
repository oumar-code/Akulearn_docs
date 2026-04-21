"""Comprehensive API tests for Aku-EdgeHub edge, device, and sync endpoints."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Aku-EdgeHub"


# ---------------------------------------------------------------------------
# GET /api/v1/health/offline — offline health check with DB probe
# ---------------------------------------------------------------------------


async def test_offline_health_returns_ok_with_db(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/offline")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db_reachable"] is True
    assert "mode" in data
    assert "timestamp" in data


# ---------------------------------------------------------------------------
# POST /api/v1/devices/register
# ---------------------------------------------------------------------------


async def test_register_device_returns_201(client: AsyncClient) -> None:
    payload = {
        "device_id": "edge-device-001",
        "name": "Classroom Hub Kano",
        "firmware_version": "1.2.3",
        "capabilities": ["AI", "offline-sync"],
        "metadata": {"location": "kano"},
    }
    response = await client.post("/api/v1/devices/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == "edge-device-001"
    assert data["status"] == "pending"


async def test_register_device_idempotent_on_duplicate(client: AsyncClient) -> None:
    payload = {
        "device_id": "edge-device-dup",
        "name": "Dup Hub",
        "firmware_version": "2.0.0",
    }
    r1 = await client.post("/api/v1/devices/register", json=payload)
    r2 = await client.post("/api/v1/devices/register", json=payload)
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r2.json()["device_id"] == "edge-device-dup"
    assert "already registered" in r2.json()["message"].lower()


async def test_register_device_rejects_invalid_firmware_version(
    client: AsyncClient,
) -> None:
    payload = {
        "device_id": "edge-device-bad-fw",
        "name": "Bad Firmware Hub",
        "firmware_version": "not-semver",
    }
    response = await client.post("/api/v1/devices/register", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/devices/{id}
# ---------------------------------------------------------------------------


async def test_get_device_returns_registered_device(client: AsyncClient) -> None:
    device_id = "edge-device-get-test"
    await client.post(
        "/api/v1/devices/register",
        json={
            "device_id": device_id,
            "name": "Lookup Hub",
            "firmware_version": "3.0.1",
        },
    )
    response = await client.get(f"/api/v1/devices/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == device_id
    assert data["firmware_version"] == "3.0.1"


async def test_get_device_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get("/api/v1/devices/no-such-device-xyz")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/v1/cache/status
# ---------------------------------------------------------------------------


async def test_cache_status_returns_response(client: AsyncClient) -> None:
    response = await client.get("/api/v1/cache/status")
    assert response.status_code == 200
    data = response.json()
    assert "item_count" in data
    assert "disk_usage_bytes" in data
    assert "mode" in data
    assert isinstance(data["item_count"], int)


# ---------------------------------------------------------------------------
# POST /api/v1/sync/trigger — patch httpx so sync.py body is executed
# ---------------------------------------------------------------------------


async def test_sync_trigger_returns_202_when_akudemy_accepts(client: AsyncClient) -> None:
    """Exercise the actual trigger_cloud_sync body by patching its httpx call."""
    import httpx
    from unittest.mock import MagicMock

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"job_id": "akudemy-job-123", "message": "Sync accepted"}

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(return_value=mock_resp)

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post(
            "/api/v1/sync/trigger",
            json={"force": True, "scope": ["topic-abc"]},
        )

    assert response.status_code == 202
    data = response.json()
    assert data["accepted"] is True
    assert data["job_id"] == "akudemy-job-123"


async def test_sync_trigger_returns_202_when_hub_offline(client: AsyncClient) -> None:
    """When Akudemy is unreachable the service falls back gracefully."""
    import httpx

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(
        side_effect=httpx.RequestError("connection refused", request=None)
    )

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post(
            "/api/v1/sync/trigger",
            json={"force": False, "scope": []},
        )

    assert response.status_code == 202
    data = response.json()
    assert data["accepted"] is False
    assert "offline" in data["message"].lower()


async def test_sync_trigger_returns_202_when_akudemy_returns_error(
    client: AsyncClient,
) -> None:
    """When Akudemy returns an HTTP error the service returns accepted=False."""
    import httpx
    from unittest.mock import MagicMock

    mock_err_resp = MagicMock(spec=httpx.Response)
    mock_err_resp.status_code = 503
    mock_err_resp.text = "Service Unavailable"

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(
        side_effect=httpx.HTTPStatusError("error", request=None, response=mock_err_resp)
    )

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post("/api/v1/sync/trigger", json={})

    assert response.status_code == 202
    assert response.json()["accepted"] is False


# ---------------------------------------------------------------------------
# POST /api/v1/ai/infer — patch httpx so sync.relay_infer body executes
# ---------------------------------------------------------------------------


async def test_ai_infer_returns_relay_response(client: AsyncClient) -> None:
    """Exercise relay_infer by patching its httpx call."""
    import httpx
    from unittest.mock import MagicMock

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {
        "text": "Photosynthesis is the process by which plants make food.",
        "model": "gemma-2b",
        "finish_reason": "stop",
        "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
    }

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(return_value=mock_resp)

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post(
            "/api/v1/ai/infer",
            json={"prompt": "What is photosynthesis?", "max_tokens": 100},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Photosynthesis is the process by which plants make food."
    assert data["model"] == "gemma-2b"


async def test_ai_infer_returns_503_when_akuai_unreachable(client: AsyncClient) -> None:
    import httpx

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(
        side_effect=httpx.RequestError("connection refused", request=None)
    )

    with patch("app.services.sync.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post(
            "/api/v1/ai/infer",
            json={"prompt": "What is photosynthesis?"},
        )

    assert response.status_code == 503
