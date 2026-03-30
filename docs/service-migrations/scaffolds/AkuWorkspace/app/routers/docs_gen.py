"""Docs-generation router — AI-assisted document creation via AkuAI."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.schemas.workflows import DocGenerateRequest, DocGenerateResponse
from app.services.orchestrator import WorkflowOrchestrator

router = APIRouter(prefix="/api/v1/docs", tags=["Document Generation"])


# ---------------------------------------------------------------------------
# Dependency helpers
# ---------------------------------------------------------------------------


def get_orchestrator(request: Request) -> WorkflowOrchestrator:
    return request.app.state.orchestrator


OrchestratorDep = Annotated[WorkflowOrchestrator, Depends(get_orchestrator)]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "/generate",
    response_model=DocGenerateResponse,
    summary="AI-assisted document generation",
    description=(
        "Forwards the prompt (and optional context) to AkuAI "
        "``POST /api/v1/text/generate`` and returns the generated document "
        "text along with model metadata."
    ),
)
async def generate_document(
    body: DocGenerateRequest,
    orchestrator: OrchestratorDep,
) -> DocGenerateResponse:
    """Generate a document using AkuAI's text-generation endpoint.

    The ``context`` field is merged into the upstream request so that
    AkuAI can personalise the output based on user or session state.
    """
    raw = await orchestrator.generate_text(
        prompt=body.prompt,
        context=body.context,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
    )

    return DocGenerateResponse(
        document=raw.get("text") or raw.get("document") or "",
        model=raw.get("model"),
        usage=raw.get("usage"),
    )
