"""Smoke tests for the AkuWorkspace /health endpoint."""

from __future__ import annotations

from httpx import AsyncClient


async def test_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_response_body(client: AsyncClient) -> None:
    response = await client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    # service_name defaults to "akuworkspace" unless overridden via SERVICE_NAME env var
    assert "service" in data


async def test_openapi_schema_accessible(client: AsyncClient) -> None:
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "AkuWorkspace"
