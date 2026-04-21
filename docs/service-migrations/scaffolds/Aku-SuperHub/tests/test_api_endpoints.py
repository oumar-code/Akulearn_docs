"""Comprehensive API tests for Aku-SuperHub endpoints.

Note: fleet and analytics routers raise NotImplementedError for their
data-access stubs, so those tests confirm the expected HTTP 500 error
until a real data layer is wired in. The models/finetune endpoint is
fully implemented and is the main focus of the positive-path tests.
"""

from __future__ import annotations

from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Aku-SuperHub"


# ---------------------------------------------------------------------------
# POST /api/v1/models/finetune
# ---------------------------------------------------------------------------


async def test_finetune_returns_202_with_queued_status(client: AsyncClient) -> None:
    payload = {
        "base_model_id": "gemma-2b",
        "dataset_window_hours": 168,
        "max_steps": 500,
        "learning_rate": 2e-5,
    }
    response = await client.post("/api/v1/models/finetune", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "QUEUED"
    assert data["base_model_id"] == "gemma-2b"
    assert "message" in data


async def test_finetune_accepts_custom_hyperparams(client: AsyncClient) -> None:
    payload = {
        "base_model_id": "facebook/bart-large-mnli",
        "dataset_window_hours": 48,
        "max_steps": 1000,
        "learning_rate": 1e-4,
        "notes": "Experiment: high LR with smaller window",
    }
    response = await client.post("/api/v1/models/finetune", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["base_model_id"] == "facebook/bart-large-mnli"
    assert data["status"] == "QUEUED"


async def test_finetune_rejects_empty_base_model_id(client: AsyncClient) -> None:
    payload = {
        "base_model_id": "",
        "dataset_window_hours": 24,
        "max_steps": 100,
        "learning_rate": 1e-5,
    }
    response = await client.post("/api/v1/models/finetune", json=payload)
    assert response.status_code == 422


async def test_finetune_rejects_max_steps_out_of_range(client: AsyncClient) -> None:
    payload = {
        "base_model_id": "gemma-2b",
        "dataset_window_hours": 24,
        "max_steps": 0,  # ge=1 constraint
        "learning_rate": 1e-5,
    }
    response = await client.post("/api/v1/models/finetune", json=payload)
    assert response.status_code == 422


async def test_finetune_rejects_window_over_limit(client: AsyncClient) -> None:
    payload = {
        "base_model_id": "gemma-2b",
        "dataset_window_hours": 9000,  # le=8760 constraint
        "max_steps": 500,
        "learning_rate": 1e-5,
    }
    response = await client.post("/api/v1/models/finetune", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/fleet — stub raises NotImplementedError (propagates in tests)
# ---------------------------------------------------------------------------


async def test_list_hubs_stub_raises_not_implemented(client: AsyncClient) -> None:
    """The fleet data-access stub raises NotImplementedError until a real
    database layer is wired in."""
    import pytest

    with pytest.raises(NotImplementedError, match="data-access layer"):
        await client.get("/api/v1/fleet")


# ---------------------------------------------------------------------------
# POST /api/v1/analytics/aggregate — stub raises NotImplementedError
# ---------------------------------------------------------------------------


async def test_aggregate_analytics_stub_raises_not_implemented(
    client: AsyncClient,
) -> None:
    from uuid import uuid4
    from datetime import datetime, timezone
    import pytest

    payload = {
        "events": [
            {
                "event_id": str(uuid4()),
                "hub_id": str(uuid4()),
                "learner_id": str(uuid4()),
                "event_type": "SESSION_START",
                "occurred_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    }
    with pytest.raises(NotImplementedError, match="data-access layer"):
        await client.post("/api/v1/analytics/aggregate", json=payload)


# ---------------------------------------------------------------------------
# GET /api/v1/analytics/summary — stub raises NotImplementedError
# ---------------------------------------------------------------------------


async def test_analytics_summary_stub_raises_not_implemented(
    client: AsyncClient,
) -> None:
    import pytest

    with pytest.raises(NotImplementedError, match="aggregation query"):
        await client.get("/api/v1/analytics/summary")


# ---------------------------------------------------------------------------
# OpenAPI schema sanity checks
# ---------------------------------------------------------------------------


async def test_openapi_schema_reachable(client: AsyncClient) -> None:
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Aku-SuperHub"
    paths = schema.get("paths", {})
    assert "/api/v1/models/finetune" in paths
    assert "/api/v1/fleet" in paths
    assert "/api/v1/analytics/aggregate" in paths
