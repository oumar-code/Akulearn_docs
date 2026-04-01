"""Workflow router — CRUD + execution for AI-native workflows."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.schemas.workflows import (
    WorkflowCreate,
    WorkflowRead,
    WorkflowRunRequest,
    WorkflowRunResult,
    WorkflowStatus,
)
from app.services.orchestrator import WorkflowOrchestrator

router = APIRouter(prefix="/api/v1/workflows", tags=["Workflows"])


# ---------------------------------------------------------------------------
# Dependency helpers
# ---------------------------------------------------------------------------


def get_orchestrator(request: Request) -> WorkflowOrchestrator:
    """Retrieve the orchestrator singleton attached to app state."""
    return request.app.state.orchestrator


def get_workflow_store(request: Request) -> dict[str, Any]:
    """Retrieve the in-process workflow store (replace with DB in production)."""
    return request.app.state.workflow_store


OrchestratorDep = Annotated[WorkflowOrchestrator, Depends(get_orchestrator)]
WorkflowStoreDep = Annotated[dict[str, Any], Depends(get_workflow_store)]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=WorkflowRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI workflow",
)
async def create_workflow(
    body: WorkflowCreate,
    store: WorkflowStoreDep,
) -> WorkflowRead:
    """Persist a workflow definition.

    The workflow is not executed here — call ``POST /{id}/run`` to trigger
    execution.
    """
    now = datetime.now(tz=timezone.utc)
    workflow = WorkflowRead(
        id=uuid.uuid4(),
        name=body.name,
        type=body.type,
        status=WorkflowStatus.PENDING,
        steps=body.steps,
        metadata=body.metadata,
        created_at=now,
        updated_at=now,
    )
    store[str(workflow.id)] = workflow
    return workflow


@router.get(
    "/{workflow_id}",
    response_model=WorkflowRead,
    summary="Retrieve a workflow by ID",
)
async def get_workflow(
    workflow_id: uuid.UUID,
    store: WorkflowStoreDep,
) -> WorkflowRead:
    workflow = store.get(str(workflow_id))
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )
    return workflow


@router.post(
    "/{workflow_id}/run",
    response_model=WorkflowRunResult,
    summary="Execute an existing workflow",
    description=(
        "Orchestrates sequential calls to AkuAI, Aku-DaaS, and/or Akudemy "
        "according to the workflow's step definitions. Each step's response "
        "is merged into the context passed to the next step."
    ),
)
async def run_workflow(
    workflow_id: uuid.UUID,
    body: WorkflowRunRequest,
    store: WorkflowStoreDep,
    orchestrator: OrchestratorDep,
) -> WorkflowRunResult:
    workflow: WorkflowRead | None = store.get(str(workflow_id))
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found.",
        )

    # Mark as running
    workflow = workflow.model_copy(
        update={"status": WorkflowStatus.RUNNING, "updated_at": datetime.now(tz=timezone.utc)}
    )
    store[str(workflow_id)] = workflow

    result = await orchestrator.run(
        workflow_id=workflow.id,
        workflow_type=workflow.type,
        steps=workflow.steps,
        runtime_input=body.input,
    )

    # Persist final status
    final_status = result.status
    store[str(workflow_id)] = workflow.model_copy(
        update={"status": final_status, "updated_at": datetime.now(tz=timezone.utc)}
    )

    return result
