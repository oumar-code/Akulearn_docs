from __future__ import annotations

import math
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.fleet import EdgeHub, EdgeHubHealth, HubHealthMetrics, HubStatus, PaginatedHubs

router = APIRouter(prefix="/api/v1/fleet", tags=["Fleet Management"])


# ---------------------------------------------------------------------------
# Stub helpers — replace with real DB calls in production
# ---------------------------------------------------------------------------

def _get_all_hubs() -> list[EdgeHub]:
    """Return all registered Edge Hub records from the data store."""
    raise NotImplementedError("Replace with real data-access layer")


def _get_hub_by_id(hub_id: UUID) -> EdgeHub | None:
    """Fetch a single hub by its UUID; returns None if not found."""
    raise NotImplementedError("Replace with real data-access layer")


def _get_hub_metrics(hub_id: UUID) -> HubHealthMetrics:
    """Retrieve live telemetry metrics for the given hub."""
    raise NotImplementedError("Replace with real telemetry collector")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=PaginatedHubs,
    summary="List Edge Hub devices",
    description=(
        "Return a paginated list of all Edge Hub devices registered to this "
        "SuperHub's region, sorted by registration date descending."
    ),
)
async def list_hubs(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    status_filter: HubStatus | None = Query(default=None, alias="status", description="Filter by hub status"),
) -> PaginatedHubs:
    all_hubs = _get_all_hubs()

    if status_filter is not None:
        all_hubs = [h for h in all_hubs if h.status == status_filter]

    total = len(all_hubs)
    pages = max(1, math.ceil(total / page_size))
    start = (page - 1) * page_size
    end = start + page_size

    return PaginatedHubs(
        items=all_hubs[start:end],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get(
    "/{hub_id}/health",
    response_model=EdgeHubHealth,
    summary="Get hub health status",
    description=(
        "Fetch the current health status and live telemetry metrics for a "
        "specific Edge Hub. Returns 404 if the hub is not registered."
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Hub not found"},
    },
)
async def get_hub_health(hub_id: UUID) -> EdgeHubHealth:
    hub = _get_hub_by_id(hub_id)
    if hub is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Edge Hub '{hub_id}' not found in this region.",
        )

    metrics = _get_hub_metrics(hub_id)

    alerts: list[str] = []
    if metrics.cpu_percent > 90.0:
        alerts.append(f"High CPU utilisation: {metrics.cpu_percent:.1f}%")
    if metrics.memory_percent > 85.0:
        alerts.append(f"High memory utilisation: {metrics.memory_percent:.1f}%")
    if metrics.disk_percent > 80.0:
        alerts.append(f"High disk utilisation: {metrics.disk_percent:.1f}%")

    return EdgeHubHealth(
        hub_id=hub.hub_id,
        status=hub.status,
        metrics=metrics,
        alerts=alerts,
    )
