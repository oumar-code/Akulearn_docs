"""TutorService — curriculum-aware prompt construction and AkuAI integration.

Responsibilities:
- Maintain in-memory session store (swap for a DB adapter in production).
- Build context-rich prompts that include subject and grade-level metadata.
- Delegate text generation to AkuAI via an async httpx client.
- Append every turn (learner + tutor) to the session message history.
"""

from __future__ import annotations

import logging
from datetime import datetime
from uuid import UUID, uuid4

import httpx

from app.schemas.sessions import (
    AskRequest,
    FeedbackCreate,
    FeedbackRead,
    HintRequest,
    Message,
    MessageRole,
    SessionCreate,
    SessionRead,
    SessionSummary,
    TutorResponse,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Internal in-memory store (replace with a database in production)
# ---------------------------------------------------------------------------

_sessions: dict[UUID, SessionRead] = {}
_feedback_store: dict[UUID, FeedbackRead] = {}


# ---------------------------------------------------------------------------
# AkuAI client helper
# ---------------------------------------------------------------------------


async def _call_aku_ai(aku_ai_url: str, prompt: str, timeout: float = 30.0) -> str:
    """POST to AkuAI /api/v1/text/generate and return the generated text."""
    endpoint = f"{aku_ai_url.rstrip('/')}/api/v1/text/generate"
    payload = {"prompt": prompt}

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()

    # AkuAI is expected to return {"text": "..."} or {"generated_text": "..."}
    return data.get("text") or data.get("generated_text") or ""


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------


def _build_ask_prompt(subject: str, grade_level: str, question: str) -> str:
    return (
        f"You are a tutor for {subject} at {grade_level} level. "
        f"Explain clearly and use age-appropriate language.\n\n"
        f"Student asks: {question}"
    )


def _build_hint_prompt(subject: str, grade_level: str, question: str) -> str:
    return (
        f"You are a tutor for {subject} at {grade_level} level. "
        f"Give a helpful hint (not the full answer) for the following question. "
        f"Guide the student towards the answer without revealing it.\n\n"
        f"Question: {question}"
    )


# ---------------------------------------------------------------------------
# TutorService
# ---------------------------------------------------------------------------


class TutorService:
    """Stateless service class; session state lives in the module-level store."""

    def __init__(self, aku_ai_url: str) -> None:
        self._aku_ai_url = aku_ai_url

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def create_session(self, payload: SessionCreate) -> SessionSummary:
        session = SessionRead(
            id=uuid4(),
            learner_id=payload.learner_id,
            subject=payload.subject,
            grade_level=payload.grade_level,
            messages=[],
            created_at=datetime.utcnow(),
        )
        _sessions[session.id] = session
        logger.info("Session created: id=%s learner=%s", session.id, session.learner_id)
        return SessionSummary(**session.model_dump())

    def get_session(self, session_id: UUID) -> SessionRead | None:
        return _sessions.get(session_id)

    def _append_messages(self, session_id: UUID, *messages: Message) -> None:
        session = _sessions[session_id]
        updated = session.model_copy(
            update={"messages": list(session.messages) + list(messages)}
        )
        _sessions[session_id] = updated

    # ------------------------------------------------------------------
    # Ask
    # ------------------------------------------------------------------

    async def ask(self, session_id: UUID, request: AskRequest) -> TutorResponse:
        session = _sessions[session_id]

        learner_msg = Message(
            role=MessageRole.LEARNER,
            content=request.question,
        )

        prompt = _build_ask_prompt(session.subject, session.grade_level, request.question)
        logger.debug("ask prompt: %s", prompt)

        generated = await _call_aku_ai(self._aku_ai_url, prompt)

        tutor_msg = Message(role=MessageRole.TUTOR, content=generated)
        self._append_messages(session_id, learner_msg, tutor_msg)

        return TutorResponse(
            session_id=session_id,
            content=generated,
            timestamp=tutor_msg.timestamp,
        )

    # ------------------------------------------------------------------
    # Hint
    # ------------------------------------------------------------------

    async def hint(self, session_id: UUID, request: HintRequest) -> TutorResponse:
        session = _sessions[session_id]

        learner_msg = Message(
            role=MessageRole.LEARNER,
            content=f"[hint request] {request.question}",
        )

        prompt = _build_hint_prompt(session.subject, session.grade_level, request.question)
        logger.debug("hint prompt: %s", prompt)

        generated = await _call_aku_ai(self._aku_ai_url, prompt)

        tutor_msg = Message(role=MessageRole.TUTOR, content=generated)
        self._append_messages(session_id, learner_msg, tutor_msg)

        return TutorResponse(
            session_id=session_id,
            content=generated,
            timestamp=tutor_msg.timestamp,
        )

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------

    def record_feedback(self, payload: FeedbackCreate) -> FeedbackRead:
        record = FeedbackRead(
            session_id=payload.session_id,
            learner_id=payload.learner_id,
            rating=payload.rating,
            comment=payload.comment,
        )
        _feedback_store[record.id] = record
        logger.info(
            "Feedback recorded: session=%s rating=%d", record.session_id, record.rating
        )
        return record
