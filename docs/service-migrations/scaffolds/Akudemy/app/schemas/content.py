"""Pydantic v2 schemas for content domain."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ContentType(StrEnum):
    VIDEO = "video"
    DOCUMENT = "document"
    QUIZ = "quiz"
    INTERACTIVE = "interactive"


class ContentBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    title: str = Field(..., min_length=1, max_length=512)
    content_type: ContentType
    language_code: str = Field(default="en", pattern=r"^[a-z]{2}(-[A-Z]{2})?$")
    description: str | None = Field(default=None, max_length=2048)
    tags: list[str] = Field(default_factory=list)
    offline_available: bool = Field(default=True)
    size_bytes: int | None = Field(default=None, ge=0)


class ContentCreate(ContentBase):
    asset_url: HttpUrl
    lesson_id: UUID | None = None


class ContentUpdate(ContentBase):
    title: str | None = Field(default=None, min_length=1, max_length=512)
    content_type: ContentType | None = None
    asset_url: HttpUrl | None = None


class ContentRead(ContentBase):
    id: UUID
    lesson_id: UUID | None
    asset_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ContentSyncResponse(BaseModel):
    """Envelope returned by the offline-sync endpoint."""

    model_config = ConfigDict(from_attributes=True)

    since: datetime
    count: int
    items: list[ContentRead]
    next_sync_token: str | None = Field(
        default=None,
        description="Opaque cursor for the next sync window.",
    )


class LessonBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(..., min_length=1, max_length=512)
    subject: str
    grade_level: str | None = None
    duration_minutes: int | None = Field(default=None, ge=1)
    is_published: bool = Field(default=False)


class LessonCreate(LessonBase):
    pass


class LessonRead(LessonBase):
    id: UUID
    content_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
