"""Pytest configuration and shared fixtures for AkuWorkspace tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.orchestrator import OrchestratorConfig, WorkflowOrchestrator


def _build_fake_redis() -> MagicMock:
    """Return a minimal async Redis mock suitable for context endpoint tests."""
    redis = MagicMock()
    _store: dict[bytes, bytes] = {}

    async def fake_hgetall(key: str) -> dict[bytes, bytes]:
        return _store

    async def fake_hset(key: str, mapping: dict) -> None:
        for k, v in mapping.items():
            _store[k.encode() if isinstance(k, str) else k] = (
                v.encode() if isinstance(v, str) else v
            )

    async def fake_expire(key: str, ttl: int) -> None:
        pass

    async def fake_execute() -> None:
        pass

    redis.hgetall = AsyncMock(side_effect=fake_hgetall)
    redis.aclose = AsyncMock()

    pipeline_mock = MagicMock()
    pipeline_mock.hset = AsyncMock(side_effect=fake_hset)
    pipeline_mock.expire = AsyncMock(side_effect=fake_expire)
    pipeline_mock.execute = AsyncMock(side_effect=fake_execute)
    redis.pipeline = MagicMock(return_value=pipeline_mock)

    return redis


@pytest.fixture
async def client() -> AsyncClient:
    """Async HTTP test client bound to the AkuWorkspace ASGI app.

    Initialises the app state that is normally set up by the lifespan,
    so tests don't require a live Redis or downstream services.
    """
    cfg = OrchestratorConfig(
        aku_ai_url="http://akuai:8001",
        aku_daas_url="http://aku-daas:8002",
        akudemy_url="http://akudemy:8003",
        redis_url="redis://localhost:6379/0",
    )
    app.state.orchestrator = WorkflowOrchestrator(cfg)
    app.state.workflow_store = {}
    app.state.redis = _build_fake_redis()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
