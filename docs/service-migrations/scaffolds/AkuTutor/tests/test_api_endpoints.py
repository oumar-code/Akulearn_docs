"""Comprehensive API tests for AkuTutor sessions and feedback endpoints."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Helper — mock AkuAI text generation
# ---------------------------------------------------------------------------

_MOCK_AI_RESPONSE = "This is a helpful tutor answer from AkuAI."


def _patch_aku_ai():
    """Patch the internal AkuAI httpx call so tests don't hit the network."""
    return patch(
        "app.services.tutor._call_aku_ai",
        new=AsyncMock(return_value=_MOCK_AI_RESPONSE),
    )


# ---------------------------------------------------------------------------
# Test isolation — clear module-level stores before every test
# ---------------------------------------------------------------------------


async def _reset_stores() -> None:
    import app.services.tutor as _svc

    _svc._sessions.clear()
    _svc._feedback_store.clear()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


# ---------------------------------------------------------------------------
# POST /api/v1/sessions — create session
# ---------------------------------------------------------------------------


async def test_create_session_returns_201_with_id(client: AsyncClient) -> None:
    await _reset_stores()
    payload = {
        "learner_id": "learner-001",
        "subject": "Mathematics",
        "grade_level": "Grade 7",
    }
    response = await client.post("/api/v1/sessions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["learner_id"] == "learner-001"
    assert data["subject"] == "Mathematics"
    assert data["grade_level"] == "Grade 7"


async def test_create_session_rejects_missing_fields(client: AsyncClient) -> None:
    response = await client.post("/api/v1/sessions", json={"learner_id": "x"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/sessions/{id} — retrieve session
# ---------------------------------------------------------------------------


async def test_get_session_returns_full_history(client: AsyncClient) -> None:
    await _reset_stores()
    create_resp = await client.post(
        "/api/v1/sessions",
        json={"learner_id": "learner-002", "subject": "Biology", "grade_level": "JSS2"},
    )
    session_id = create_resp.json()["id"]

    get_resp = await client.get(f"/api/v1/sessions/{session_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == session_id
    assert data["learner_id"] == "learner-002"
    assert isinstance(data["messages"], list)


async def test_get_session_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/sessions/{uuid4()}")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/sessions/{id}/ask
# ---------------------------------------------------------------------------


async def test_ask_returns_tutor_response(client: AsyncClient) -> None:
    await _reset_stores()
    create_resp = await client.post(
        "/api/v1/sessions",
        json={"learner_id": "learner-ask", "subject": "Physics", "grade_level": "Year 9"},
    )
    session_id = create_resp.json()["id"]

    with _patch_aku_ai():
        ask_resp = await client.post(
            f"/api/v1/sessions/{session_id}/ask",
            json={"question": "What is Newton's second law?"},
        )

    assert ask_resp.status_code == 200
    data = ask_resp.json()
    assert data["session_id"] == session_id
    assert data["role"] == "tutor"
    assert data["content"] == _MOCK_AI_RESPONSE


async def test_ask_appends_messages_to_history(client: AsyncClient) -> None:
    await _reset_stores()
    create_resp = await client.post(
        "/api/v1/sessions",
        json={"learner_id": "learner-hist", "subject": "Chemistry", "grade_level": "SS2"},
    )
    session_id = create_resp.json()["id"]

    with _patch_aku_ai():
        await client.post(
            f"/api/v1/sessions/{session_id}/ask",
            json={"question": "What is an atom?"},
        )

    get_resp = await client.get(f"/api/v1/sessions/{session_id}")
    messages = get_resp.json()["messages"]
    # Expect one learner message and one tutor message
    assert len(messages) == 2
    roles = {m["role"] for m in messages}
    assert roles == {"learner", "tutor"}


async def test_ask_404_for_unknown_session(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/sessions/{uuid4()}/ask",
        json={"question": "Any question"},
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/sessions/{id}/hint
# ---------------------------------------------------------------------------


async def test_hint_returns_tutor_response(client: AsyncClient) -> None:
    await _reset_stores()
    create_resp = await client.post(
        "/api/v1/sessions",
        json={"learner_id": "learner-hint", "subject": "Mathematics", "grade_level": "Grade 9"},
    )
    session_id = create_resp.json()["id"]

    with _patch_aku_ai():
        hint_resp = await client.post(
            f"/api/v1/sessions/{session_id}/hint",
            json={"question": "How do I solve quadratic equations?"},
        )

    assert hint_resp.status_code == 200
    data = hint_resp.json()
    assert data["session_id"] == session_id
    assert data["content"] == _MOCK_AI_RESPONSE


async def test_hint_404_for_unknown_session(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/sessions/{uuid4()}/hint",
        json={"question": "Any hint question"},
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/feedback
# ---------------------------------------------------------------------------


async def test_submit_feedback_returns_201(client: AsyncClient) -> None:
    await _reset_stores()
    session_id = str(uuid4())
    payload: dict[str, Any] = {
        "session_id": session_id,
        "learner_id": "learner-feedback",
        "rating": 4,
        "comment": "Very helpful session!",
    }
    response = await client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["session_id"] == session_id
    assert data["rating"] == 4
    assert data["comment"] == "Very helpful session!"


async def test_submit_feedback_without_comment(client: AsyncClient) -> None:
    await _reset_stores()
    payload: dict[str, Any] = {
        "session_id": str(uuid4()),
        "learner_id": "learner-no-comment",
        "rating": 5,
    }
    response = await client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 201
    assert response.json()["comment"] is None


async def test_submit_feedback_rejects_out_of_range_rating(client: AsyncClient) -> None:
    payload: dict[str, Any] = {
        "session_id": str(uuid4()),
        "learner_id": "learner-bad",
        "rating": 6,
    }
    response = await client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 422


async def test_submit_feedback_rejects_rating_zero(client: AsyncClient) -> None:
    payload: dict[str, Any] = {
        "session_id": str(uuid4()),
        "learner_id": "learner-zero",
        "rating": 0,
    }
    response = await client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 422
