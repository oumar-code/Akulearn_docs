"""Aku-SuperHub regional analytics aggregation service — stub."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Aggregates telemetry and analytics data from Edge Hubs in the region.

    TODO: Replace stub methods with real Kafka consumer + TimescaleDB writes.
    """

    async def ingest(self, hub_id: str, payload: dict) -> dict:
        """Ingest analytics payload from a single Edge Hub."""
        # TODO: write to TimescaleDB or Kafka topic
        logger.info("Analytics ingested from hub_id=%s payload_keys=%s", hub_id, list(payload.keys()))
        return {
            "hub_id": hub_id,
            "accepted": True,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        }

    async def summary(self, region: str | None = None) -> dict:
        """Return a regional analytics summary."""
        # TODO: aggregate from TimescaleDB / data warehouse
        return {
            "region": region or "global",
            "total_hubs": 0,
            "active_hubs": 0,
            "avg_cpu_percent": 0.0,
            "avg_memory_percent": 0.0,
            "learner_sessions_last_24h": 0,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


analytics_service = AnalyticsService()
