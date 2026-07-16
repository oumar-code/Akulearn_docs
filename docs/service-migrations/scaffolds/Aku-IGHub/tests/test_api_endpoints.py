"""Endpoint coverage tests for Aku-IGHub routers."""

from __future__ import annotations

import uuid

from httpx import AsyncClient

AUTH_HEADERS = {"Authorization": "Bearer role:operator"}


async def test_issue_and_verify_credential(client: AsyncClient) -> None:
    issue_response = await client.post(
        "/api/v1/credentials/issue",
        headers=AUTH_HEADERS,
        json={
            "subject_did": "did:web:learner.akulearn.io",
            "credential_type": "SkillBadge",
            "claims": {"skill": "python", "level": "intermediate"},
        },
    )
    assert issue_response.status_code == 201
    issued = issue_response.json()
    assert issued["credential_id"]
    assert issued["credential_type"] == "SkillBadge"

    verify_response = await client.get(
        f"/api/v1/credentials/{issued['credential_id']}/verify",
        headers=AUTH_HEADERS,
    )
    assert verify_response.status_code == 200
    verified = verify_response.json()
    assert verified["valid"] is True


async def test_publish_and_get_metadata(client: AsyncClient) -> None:
    publish_response = await client.post(
        "/api/v1/metadata/publish",
        headers=AUTH_HEADERS,
        json={
            "category": "learning_activity",
            "payload": {"lesson_id": "math-101", "completion": 0.85},
            "tags": ["math", "progress"],
            "source_service": "Akudemy",
        },
    )
    assert publish_response.status_code == 201
    data = publish_response.json()
    metadata_id = data["metadata_id"]

    get_response = await client.get(f"/api/v1/metadata/{metadata_id}", headers=AUTH_HEADERS)
    assert get_response.status_code == 200
    record = get_response.json()
    assert record["metadata_id"] == metadata_id
    assert record["source_service"] == "Akudemy"


async def test_compliance_check_and_clearing_flow(client: AsyncClient) -> None:
    compliance_response = await client.post(
        "/api/v1/compliance/check",
        headers=AUTH_HEADERS,
        json={
            "operation": "credential.share",
            "source_jurisdiction": "DE",
            "target_jurisdiction": "US",
            "applicable_policies": ["GDPR"],
            "context": {"contains_personal_data": True},
        },
    )
    assert compliance_response.status_code == 200
    compliance_data = compliance_response.json()
    assert compliance_data["decision"] in {"ALLOWED", "BLOCKED", "REQUIRES_REVIEW"}

    idempotency_key = str(uuid.uuid4())
    settle_response = await client.post(
        "/api/v1/clearing/settle",
        headers={**AUTH_HEADERS, "Idempotency-Key": idempotency_key},
        json={
            "from_wallet": "wallet-a",
            "to_wallet": "wallet-b",
            "amount": "5.50",
            "currency": "AKU",
            "reference": "tuition-fee",
            "metadata": {"invoice": "INV-001"},
        },
    )
    assert settle_response.status_code == 201
    tx = settle_response.json()
    assert tx["idempotency_key"] == idempotency_key

    status_response = await client.get(
        f"/api/v1/clearing/{tx['tx_id']}",
        headers=AUTH_HEADERS,
    )
    assert status_response.status_code == 200
    status_payload = status_response.json()
    assert status_payload["tx_id"] == tx["tx_id"]
