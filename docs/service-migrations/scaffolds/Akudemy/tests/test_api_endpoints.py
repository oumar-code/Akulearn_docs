"""Comprehensive API tests for Akudemy content and credential endpoints."""

from __future__ import annotations

from uuid import uuid4

from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Test isolation
# ---------------------------------------------------------------------------


async def _reset_stores() -> None:
    import app.services.content as _content
    import app.routers.credentials as _creds

    _content._CONTENT_STORE.clear()
    _creds._CREDENTIAL_STORE.clear()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# GET /api/v1/content/sync
# ---------------------------------------------------------------------------


async def test_sync_content_returns_envelope(client: AsyncClient) -> None:
    # Use a very early timestamp so the pre-seeded item is returned
    response = await client.get(
        "/api/v1/content/sync",
        params={"since": "2020-01-01T00:00:00Z"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["count"] == len(data["items"])


async def test_sync_content_requires_since_param(client: AsyncClient) -> None:
    response = await client.get("/api/v1/content/sync")
    assert response.status_code == 422


async def test_sync_content_future_since_returns_empty(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/content/sync",
        params={"since": "2099-01-01T00:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert response.json()["items"] == []


# ---------------------------------------------------------------------------
# POST /api/v1/content — create
# ---------------------------------------------------------------------------


async def test_create_content_returns_201(client: AsyncClient) -> None:
    await _reset_stores()
    payload = {
        "title": "Introduction to Algebra",
        "content_type": "document",
        "language_code": "en",
        "asset_url": "https://cdn.akulearn.example/algebra-intro.pdf",
        "offline_available": True,
        "tags": ["math", "algebra"],
    }
    response = await client.post("/api/v1/content", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Introduction to Algebra"
    assert data["content_type"] == "document"


async def test_create_content_rejects_invalid_language_code(client: AsyncClient) -> None:
    payload = {
        "title": "Bad Language",
        "content_type": "video",
        "asset_url": "https://cdn.akulearn.example/test.mp4",
        "language_code": "TOOLONG",
    }
    response = await client.post("/api/v1/content", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/content/{id}
# ---------------------------------------------------------------------------


async def test_get_content_returns_item_after_create(client: AsyncClient) -> None:
    await _reset_stores()
    create_resp = await client.post(
        "/api/v1/content",
        json={
            "title": "Lookup Test",
            "content_type": "quiz",
            "asset_url": "https://cdn.akulearn.example/quiz-1.json",
        },
    )
    content_id = create_resp.json()["id"]

    get_resp = await client.get(f"/api/v1/content/{content_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == content_id
    assert data["title"] == "Lookup Test"


async def test_get_content_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/content/{uuid4()}")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/v1/lessons
# ---------------------------------------------------------------------------


async def test_list_lessons_returns_list(client: AsyncClient) -> None:
    response = await client.get("/api/v1/lessons")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # At least the seeded lesson is present
    assert len(data) >= 1
    lesson = data[0]
    assert "id" in lesson
    assert "title" in lesson
    assert "subject" in lesson


# ---------------------------------------------------------------------------
# POST /api/v1/credentials/issue
# ---------------------------------------------------------------------------


_VALID_ISSUE_PAYLOAD = {
    "learner_id": str(uuid4()),
    "learner_wallet_address": "0xAbCd1234567890aBcD1234567890AbCd12345678",
    "credential_type": "course_completion",
    "course_id": str(uuid4()),
}


async def test_issue_credential_returns_202(client: AsyncClient) -> None:
    await _reset_stores()
    response = await client.post("/api/v1/credentials/issue", json=_VALID_ISSUE_PAYLOAD)
    assert response.status_code == 202
    data = response.json()
    assert "credential_id" in data
    assert "tx_hash" in data
    assert data["status"] == "pending"
    assert data["tx_hash"].startswith("0x")


async def test_issue_credential_rejects_invalid_wallet_address(client: AsyncClient) -> None:
    payload = {**_VALID_ISSUE_PAYLOAD, "learner_wallet_address": "not-a-wallet"}
    response = await client.post("/api/v1/credentials/issue", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/credentials/{id}/verify
# ---------------------------------------------------------------------------


async def test_verify_credential_returns_issued_status(client: AsyncClient) -> None:
    await _reset_stores()
    issue_resp = await client.post("/api/v1/credentials/issue", json=_VALID_ISSUE_PAYLOAD)
    credential_id = issue_resp.json()["credential_id"]

    verify_resp = await client.get(f"/api/v1/credentials/{credential_id}/verify")
    assert verify_resp.status_code == 200
    data = verify_resp.json()
    assert data["credential_id"] == credential_id
    assert data["on_chain_verified"] is True
    assert data["status"] == "issued"


async def test_verify_credential_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/credentials/{uuid4()}/verify")
    assert response.status_code == 404
