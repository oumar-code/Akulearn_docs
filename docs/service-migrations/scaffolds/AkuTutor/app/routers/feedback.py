"""Feedback router — collects learner ratings and comments on sessions."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.schemas.sessions import FeedbackCreate, FeedbackRead
from app.services.tutor import TutorService
from app.dependencies import get_tutor_service  # noqa: F401 — wired in app factory

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])


# ---------------------------------------------------------------------------
# POST /api/v1/feedback
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=FeedbackRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback for a tutoring session",
)
async def submit_feedback(
    payload: FeedbackCreate,
    service: TutorService = Depends(get_tutor_service),
) -> FeedbackRead:
    """Record learner feedback (1–5 rating + optional comment) for a session.

    Feedback is stored and can be used to evaluate tutor quality and inform
    curriculum improvements.
    """
    return service.record_feedback(payload)
