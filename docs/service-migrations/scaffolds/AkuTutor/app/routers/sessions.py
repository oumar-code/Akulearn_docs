"""Session router — manages tutoring session lifecycle and learner interactions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.sessions import (
    AskRequest,
    HintRequest,
    SessionCreate,
    SessionRead,
    SessionSummary,
    TutorResponse,
)
from app.services.tutor import TutorService
from app.dependencies import get_tutor_service  # noqa: F401 — wired in app factory

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


# ---------------------------------------------------------------------------
# POST /api/v1/sessions
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=SessionSummary,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new tutoring session",
)
async def create_session(
    payload: SessionCreate,
    service: TutorService = Depends(get_tutor_service),
) -> SessionSummary:
    """Create a new tutoring session for a learner.

    The caller supplies `subject`, `grade_level`, and `learner_id`.
    Returns a `SessionSummary` containing the new session `id` to use in
    subsequent requests.
    """
    return service.create_session(payload)


# ---------------------------------------------------------------------------
# GET /api/v1/sessions/{id}
# ---------------------------------------------------------------------------


@router.get(
    "/{session_id}",
    response_model=SessionRead,
    summary="Retrieve session history",
)
async def get_session(
    session_id: UUID,
    service: TutorService = Depends(get_tutor_service),
) -> SessionRead:
    """Return the full message history for a session."""
    session = service.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found.",
        )
    return session


# ---------------------------------------------------------------------------
# POST /api/v1/sessions/{id}/ask
# ---------------------------------------------------------------------------


@router.post(
    "/{session_id}/ask",
    response_model=TutorResponse,
    summary="Submit a question to the tutor",
)
async def ask(
    session_id: UUID,
    payload: AskRequest,
    service: TutorService = Depends(get_tutor_service),
) -> TutorResponse:
    """Send a learner question to AkuAI and receive a curriculum-aware answer.

    The prompt is enriched with `subject` and `grade_level` context from the
    session before being forwarded to AkuAI `/api/v1/text/generate`.
    """
    _require_session(session_id, service)
    return await service.ask(session_id, payload)


# ---------------------------------------------------------------------------
# POST /api/v1/sessions/{id}/hint
# ---------------------------------------------------------------------------


@router.post(
    "/{session_id}/hint",
    response_model=TutorResponse,
    summary="Request a hint for a question",
)
async def hint(
    session_id: UUID,
    payload: HintRequest,
    service: TutorService = Depends(get_tutor_service),
) -> TutorResponse:
    """Request a guiding hint (not the full answer) from AkuAI.

    The prompt instructs AkuAI to scaffold the learner towards the solution
    without revealing it directly.
    """
    _require_session(session_id, service)
    return await service.hint(session_id, payload)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _require_session(session_id: UUID, service: TutorService) -> None:
    if service.get_session(session_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found.",
        )
