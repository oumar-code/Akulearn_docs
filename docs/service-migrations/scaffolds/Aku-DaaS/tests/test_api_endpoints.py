"""Comprehensive API tests for Aku-DaaS dataset, consent, and metadata endpoints."""

from __future__ import annotations

from uuid import uuid4

from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Test isolation — clear in-memory stores before each test
# ---------------------------------------------------------------------------


async def _reset_stores() -> None:
    import app.services.anonymisation as _anon
    import app.routers.consent as _consent

    _anon._dataset_store.clear()
    _consent._consent_store.clear()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Aku-DaaS"


# ---------------------------------------------------------------------------
# POST /api/v1/datasets/ingest (multipart file upload)
# ---------------------------------------------------------------------------


async def test_ingest_multipart_file_returns_201(client: AsyncClient) -> None:
    await _reset_stores()
    response = await client.post(
        "/api/v1/datasets/ingest",
        files={"file": ("students.csv", b"name,age\nAlice,15\nBob,16", "text/csv")},
        data={"name": "Student Scores Q1", "source_service": "Akudemy", "tags": "education,q1"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "dataset_id" in data
    assert data["name"] == "Student Scores Q1"
    assert data["status"] == "ingested"


async def test_ingest_multipart_uses_filename_when_name_is_blank(client: AsyncClient) -> None:
    await _reset_stores()
    response = await client.post(
        "/api/v1/datasets/ingest",
        files={"file": ("scores_q2.csv", b"a,b\n1,2", "text/csv")},
        data={"source_service": "AkuTutor"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "scores_q2.csv"


async def test_ingest_neither_file_nor_body_returns_422(client: AsyncClient) -> None:
    # Posting form data without a file → neither branch is taken → 422
    response = await client.post(
        "/api/v1/datasets/ingest",
        data={"name": "No file", "source_service": "Akudemy"},
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/datasets/{id}/status
# ---------------------------------------------------------------------------


async def test_get_status_returns_ingested(client: AsyncClient) -> None:
    await _reset_stores()
    ingest_resp = await client.post(
        "/api/v1/datasets/ingest",
        files={"file": ("data.csv", b"a,b\n1,2", "text/csv")},
        data={"name": "Test Dataset", "source_service": "AkuTutor"},
    )
    dataset_id = ingest_resp.json()["dataset_id"]

    status_resp = await client.get(f"/api/v1/datasets/{dataset_id}/status")
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["dataset_id"] == dataset_id
    assert data["status"] == "ingested"
    assert data["source_service"] == "AkuTutor"


async def test_get_status_404_for_unknown_id(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/datasets/{uuid4()}/status")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/datasets/{id}/anonymise
# ---------------------------------------------------------------------------


async def test_trigger_anonymise_returns_202(client: AsyncClient) -> None:
    await _reset_stores()
    ingest_resp = await client.post(
        "/api/v1/datasets/ingest",
        files={"file": ("anon.csv", b"name,age\nAlice,15", "text/csv")},
        data={"name": "Anon Test", "source_service": "Aku-DaaS"},
    )
    dataset_id = ingest_resp.json()["dataset_id"]

    anon_resp = await client.post(
        f"/api/v1/datasets/{dataset_id}/anonymise",
        json={"k_value": 5, "quasi_identifiers": ["age", "region"]},
    )
    assert anon_resp.status_code == 202
    data = anon_resp.json()
    assert data["dataset_id"] == dataset_id
    assert data["status"] == "anonymising"
    assert data["k_value"] == 5


async def test_trigger_anonymise_404_for_unknown_dataset(client: AsyncClient) -> None:
    response = await client.post(f"/api/v1/datasets/{uuid4()}/anonymise", json={})
    assert response.status_code == 404


async def test_trigger_anonymise_409_when_already_anonymising(client: AsyncClient) -> None:
    await _reset_stores()
    ingest_resp = await client.post(
        "/api/v1/datasets/ingest",
        files={"file": ("conflict.csv", b"id,score\n1,80", "text/csv")},
        data={"name": "Conflict Test", "source_service": "Aku-DaaS"},
    )
    dataset_id = ingest_resp.json()["dataset_id"]

    # Directly set the status to ANONYMISING to simulate an in-progress pipeline.
    # (The background task would normally do this asynchronously.)
    import app.services.anonymisation as _anon
    from app.schemas.datasets import DatasetStatus
    _anon._dataset_store[dataset_id]["status"] = DatasetStatus.ANONYMISING

    # Now triggering again should return 409
    second = await client.post(f"/api/v1/datasets/{dataset_id}/anonymise", json={})
    assert second.status_code == 409


# ---------------------------------------------------------------------------
# POST /api/v1/metadata/publish
# ---------------------------------------------------------------------------


async def test_publish_metadata_returns_201_without_ighub(client: AsyncClient) -> None:
    """When IGHUB_METADATA_PUBLISH_URL is not configured, the endpoint still
    returns 201 with ighub_acknowledged=False."""
    await _reset_stores()
    payload = {
        "dataset_id": str(uuid4()),
        "category": "EDUCATION",
        "payload": {"total_students": 120, "avg_score": 72.5},
        "tags": ["q1", "secondary"],
    }
    response = await client.post("/api/v1/metadata/publish", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "publish_id" in data
    assert data["ighub_acknowledged"] is False
    assert data["dataset_id"] == payload["dataset_id"]


# ---------------------------------------------------------------------------
# GET /api/v1/consent/{user_id}
# ---------------------------------------------------------------------------


async def test_get_consent_404_when_no_record(client: AsyncClient) -> None:
    await _reset_stores()
    response = await client.get("/api/v1/consent/unknown-user-xyz")
    assert response.status_code == 404


async def test_get_consent_returns_record_after_upsert(client: AsyncClient) -> None:
    await _reset_stores()
    user_id = f"user-{uuid4()}"
    await client.post(
        f"/api/v1/consent/{user_id}",
        json={"consent_given": True, "consent_for": ["analytics", "research"]},
    )
    get_resp = await client.get(f"/api/v1/consent/{user_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["consent_given"] is True
    assert set(data["consent_for"]) == {"analytics", "research"}
    assert data["is_new"] is False


# ---------------------------------------------------------------------------
# POST /api/v1/consent/{user_id}
# ---------------------------------------------------------------------------


async def test_upsert_consent_creates_new_record(client: AsyncClient) -> None:
    await _reset_stores()
    user_id = f"user-{uuid4()}"
    response = await client.post(
        f"/api/v1/consent/{user_id}",
        json={
            "consent_given": True,
            "consent_for": ["analytics", "personalisation"],
            "jurisdiction": "NG",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["consent_given"] is True
    assert data["is_new"] is True
    assert data["jurisdiction"] == "NG"
    assert set(data["consent_for"]) == {"analytics", "personalisation"}


async def test_upsert_consent_withdrawal_clears_purposes(client: AsyncClient) -> None:
    await _reset_stores()
    user_id = f"user-{uuid4()}"
    # Grant consent first
    await client.post(
        f"/api/v1/consent/{user_id}",
        json={"consent_given": True, "consent_for": ["analytics", "marketing"]},
    )
    # Withdraw
    withdraw_resp = await client.post(
        f"/api/v1/consent/{user_id}",
        json={"consent_given": False, "consent_for": ["analytics"]},
    )
    data = withdraw_resp.json()
    assert data["consent_given"] is False
    # Purposes should be cleared on withdrawal
    assert data["consent_for"] == []
    assert data["is_new"] is False


async def test_upsert_consent_rejects_invalid_jurisdiction(client: AsyncClient) -> None:
    user_id = f"user-{uuid4()}"
    response = await client.post(
        f"/api/v1/consent/{user_id}",
        json={"consent_given": True, "jurisdiction": "X"},  # too short
    )
    assert response.status_code == 422
