"""Pydantic v2 schemas for AkuTutor session management."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class MessageRole(StrEnum):
    LEARNER = "learner"
    TUTOR = "tutor"
    SYSTEM = "system"


class Message(BaseModel):
    model_config = ConfigDict(frozen=True)

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------


class SessionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    learner_id: str = Field(..., min_length=1, description="Unique identifier for the learner")
    subject: str = Field(..., min_length=1, examples=["Mathematics", "Biology"])
    grade_level: str = Field(..., min_length=1, examples=["Grade 7", "JSS2", "Year 9"])


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    learner_id: str
    subject: str
    grade_level: str
    messages: list[Message] = Field(default_factory=list)
    created_at: datetime


class SessionSummary(BaseModel):
    """Lightweight session representation returned on creation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    learner_id: str
    subject: str
    grade_level: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Ask / Hint
# ---------------------------------------------------------------------------


class AskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(..., min_length=1, description="Learner's question")


class HintRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(..., min_length=1, description="Question for which a hint is requested")


class TutorResponse(BaseModel):
    """Single turn response returned to the learner."""

    session_id: UUID
    role: MessageRole = MessageRole.TUTOR
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------


class FeedbackCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    session_id: UUID = Field(..., description="Session being reviewed")
    learner_id: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 (poor) to 5 (excellent)")
    comment: str | None = Field(default=None, max_length=1000)


class FeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    learner_id: str
    rating: int
    comment: str | None
    created_at: datetime = Field(default_factory=datetime.utcnow)
