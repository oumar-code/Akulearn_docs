"""Comprehensive API tests for AkuWorkspace workflow, context, and docs endpoints."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from httpx import AsyncClient

from app.main import app as _app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _workflow_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": "Test Workflow",
        "type": "DOC_GENERATION",
        "steps": [
            {
                "name": "Generate draft",
                "service": "akuai",
                "endpoint": "/api/v1/text/generate",
                "payload": {"prompt": "Write a lesson plan"},
            }
        ],
        "metadata": {},
    }
    payload.update(overrides)
    return payload


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# POST /api/v1/workflows — create
# ---------------------------------------------------------------------------


async def test_create_workflow_returns_201(client: AsyncClient) -> None:
    _app.state.workflow_store.clear()
    response = await client.post("/api/v1/workflows", json=_workflow_payload())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Workflow"
    assert data["type"] == "DOC_GENERATION"
    assert data["status"] == "PENDING"
    assert len(data["steps"]) == 1


async def test_create_workflow_rejects_empty_steps(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/workflows", json=_workflow_payload(steps=[])
    )
    assert response.status_code == 422


async def test_create_workflow_rejects_empty_name(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/workflows", json=_workflow_payload(name="")
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/workflows/{id}
# ---------------------------------------------------------------------------


async def test_get_workflow_returns_created_workflow(client: AsyncClient) -> None:
    _app.state.workflow_store.clear()
    create_resp = await client.post("/api/v1/workflows", json=_workflow_payload())
    workflow_id = create_resp.json()["id"]

    get_resp = await client.get(f"/api/v1/workflows/{workflow_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == workflow_id
    assert data["name"] == "Test Workflow"


async def test_get_workflow_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/workflows/{uuid4()}")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/workflows/{id}/run — mock orchestrator.run
# ---------------------------------------------------------------------------


async def test_run_workflow_returns_completed_result(client: AsyncClient) -> None:
    _app.state.workflow_store.clear()
    create_resp = await client.post(
        "/api/v1/workflows", json=_workflow_payload(type="DATA_QUERY")
    )
    workflow_id = create_resp.json()["id"]

    import httpx
    from unittest.mock import MagicMock

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"text": "Some output from AkuAI", "model": "gemma-2b"}

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(return_value=mock_resp)

    with patch("app.services.orchestrator.httpx.AsyncClient", return_value=mock_instance):
        run_resp = await client.post(
            f"/api/v1/workflows/{workflow_id}/run",
            json={"input": {"query": "list all students"}},
        )

    assert run_resp.status_code == 200
    data = run_resp.json()
    assert data["workflow_id"] == str(workflow_id)
    assert data["status"] == "COMPLETED"
    assert len(data["outputs"]) == 1


async def test_run_workflow_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/workflows/{uuid4()}/run",
        json={"input": {}},
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/docs/generate — mock orchestrator.generate_text
# ---------------------------------------------------------------------------


async def test_docs_generate_returns_document(client: AsyncClient) -> None:
    import httpx
    from unittest.mock import MagicMock

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {
        "text": "Here is your AI-generated lesson plan content.",
        "model": "gemma-2b",
        "usage": {"prompt_tokens": 20, "completion_tokens": 60, "total_tokens": 80},
    }

    mock_instance = AsyncMock()
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    mock_instance.post = AsyncMock(return_value=mock_resp)

    with patch("app.services.orchestrator.httpx.AsyncClient", return_value=mock_instance):
        response = await client.post(
            "/api/v1/docs/generate",
            json={
                "prompt": "Write a lesson plan for Grade 7 Mathematics",
                "max_tokens": 512,
                "temperature": 0.5,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["document"] == "Here is your AI-generated lesson plan content."
    assert data["model"] == "gemma-2b"


async def test_docs_generate_rejects_empty_prompt(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/docs/generate",
        json={"prompt": ""},
    )
    assert response.status_code == 422


async def test_docs_generate_rejects_max_tokens_below_minimum(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/docs/generate",
        json={"prompt": "Generate something", "max_tokens": 10},  # ge=64
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Context endpoints — use the fake Redis from conftest
# ---------------------------------------------------------------------------


async def test_get_context_returns_empty_for_unknown_user(client: AsyncClient) -> None:
    response = await client.get("/api/v1/context/unknown-user-abc")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "unknown-user-abc"
    assert data["data"] == {}
    assert data["updated_at"] is None


async def test_update_context_stores_entries(client: AsyncClient) -> None:
    user_id = f"user-{uuid4()}"

    update_resp = await client.post(
        f"/api/v1/context/{user_id}",
        json={
            "entries": [
                {"key": "last_topic", "value": "quadratic equations"},
                {"key": "grade", "value": "Grade 9"},
            ]
        },
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["user_id"] == user_id


async def test_update_context_rejects_empty_entries(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/context/some-user",
        json={"entries": []},
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Direct orchestrator unit tests for coverage
# ---------------------------------------------------------------------------


def test_orchestrator_config_base_url_for_known_services() -> None:
    from app.services.orchestrator import OrchestratorConfig

    cfg = OrchestratorConfig(
        aku_ai_url="http://akuai:8001/",
        aku_daas_url="http://daas:8002/",
        akudemy_url="http://akudemy:8003/",
        redis_url="redis://localhost",
    )
    assert cfg.base_url_for("akuai") == "http://akuai:8001"
    assert cfg.base_url_for("daas") == "http://daas:8002"
    assert cfg.base_url_for("akudemy") == "http://akudemy:8003"


def test_orchestrator_config_base_url_for_unknown_service_raises() -> None:
    import pytest
    from app.services.orchestrator import OrchestratorConfig

    cfg = OrchestratorConfig(
        aku_ai_url="http://akuai:8001",
        aku_daas_url="http://daas:8002",
        akudemy_url="http://akudemy:8003",
        redis_url="redis://localhost",
    )
    with pytest.raises(ValueError, match="Unknown service"):
        cfg.base_url_for("unknown-service")


async def test_orchestrator_run_doc_generation_with_mocked_http() -> None:
    import httpx
    from unittest.mock import MagicMock
    from uuid import uuid4 as _uuid4
    from app.services.orchestrator import OrchestratorConfig, WorkflowOrchestrator
    from app.schemas.workflows import WorkflowStep, WorkflowType

    cfg = OrchestratorConfig(
        aku_ai_url="http://akuai:8001",
        aku_daas_url="http://daas:8002",
        akudemy_url="http://akudemy:8003",
        redis_url="redis://localhost",
    )
    orch = WorkflowOrchestrator(cfg)

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"text": "Generated content", "model": "gemma-2b"}

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.post = AsyncMock(return_value=mock_resp)

    steps = [
        WorkflowStep(
            name="Generate",
            service="akuai",
            endpoint="/api/v1/text/generate",
            payload={"prompt": "Write a story"},
        )
    ]

    with patch("app.services.orchestrator.httpx.AsyncClient", return_value=mock_http):
        result = await orch.run(
            workflow_id=_uuid4(),
            workflow_type=WorkflowType.DOC_GENERATION,
            steps=steps,
            runtime_input={},
        )

    assert result.status.value == "COMPLETED"
    assert len(result.outputs) == 1


async def test_orchestrator_run_content_search_and_tutoring_assist() -> None:
    import httpx
    from unittest.mock import MagicMock
    from uuid import uuid4 as _uuid4
    from app.services.orchestrator import OrchestratorConfig, WorkflowOrchestrator
    from app.schemas.workflows import WorkflowStep, WorkflowType

    cfg = OrchestratorConfig(
        aku_ai_url="http://akuai:8001",
        aku_daas_url="http://daas:8002",
        akudemy_url="http://akudemy:8003",
        redis_url="redis://localhost",
    )
    orch = WorkflowOrchestrator(cfg)

    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"results": []}

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.post = AsyncMock(return_value=mock_resp)

    steps = [
        WorkflowStep(
            name="Search",
            service="akudemy",
            endpoint="/api/v1/content/search",
            payload={"query": "algebra"},
        )
    ]

    with patch("app.services.orchestrator.httpx.AsyncClient", return_value=mock_http):
        r1 = await orch.run(
            workflow_id=_uuid4(),
            workflow_type=WorkflowType.CONTENT_SEARCH,
            steps=steps,
            runtime_input={},
        )
        r2 = await orch.run(
            workflow_id=_uuid4(),
            workflow_type=WorkflowType.TUTORING_ASSIST,
            steps=steps,
            runtime_input={},
        )

    assert r1.status.value == "COMPLETED"
    assert r2.status.value == "COMPLETED"
