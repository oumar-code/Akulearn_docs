#!/usr/bin/env python3
"""Phase 4 Assets API Router - Practice Questions

Provides endpoints for:
- Phase 4: Practice questions (MCQ, True/False, Fill-blank, Matching, Short Answer)
- Answer validation and scoring
- Question retrieval by subject, topic, type, difficulty
- Statistics and analytics
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel
import logging

from src.backend.phase4_asset_loader import (
    initialize_phase4_loader,
    get_phase4_loader,
    Phase4AssetLoader
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assets/phase4", tags=["Phase 4 Questions"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QuestionInfo(BaseModel):
    id: str
    subject: str
    topic: str
    grade: str
    question_type: str
    difficulty: str
    points: int
    estimated_time: int
    tags: List[str]

class QuestionDetail(BaseModel):
    id: str
    subject: str
    topic: str
    grade: str
    question_type: str
    difficulty: str
    question_data: Dict[str, Any]
    points: int
    estimated_time: int
    tags: List[str]

class AnswerSubmission(BaseModel):
    question_id: str
    user_answer: Union[int, bool, str, Dict[str, int]]

class AnswerValidation(BaseModel):
    valid: bool
    correct: Optional[bool] = None
    user_answer: Optional[Any] = None
    correct_answer: Optional[Any] = None
    explanation: Optional[str] = None
    points_earned: Optional[float] = None
    points_possible: Optional[int] = None
    error: Optional[str] = None
    requires_manual_grading: Optional[bool] = None
    sample_answer: Optional[str] = None
    marking_criteria: Optional[List[str]] = None
    correct_count: Optional[int] = None
    total_pairs: Optional[int] = None
    note: Optional[str] = None

class Phase4Summary(BaseModel):
    total_questions: int
    question_types: int
    subjects: int
    total_points: int
    total_time_minutes: int
    type_breakdown: Dict[str, int]
    difficulty_breakdown: Dict[str, int]
    subject_breakdown: Dict[str, int]
    generated_at: Optional[str] = None

class SubjectStats(BaseModel):
    subject: str
    total_questions: int
    total_points: Optional[int] = None
    total_time_minutes: Optional[int] = None
    type_breakdown: Optional[Dict[str, int]] = None
    difficulty_breakdown: Optional[Dict[str, int]] = None
    error: Optional[str] = None


# ============================================================================
# HELPERS
# ============================================================================

def ensure_phase4_loader_initialized() -> Optional[Phase4AssetLoader]:
    """Ensure Phase 4 loader is initialized."""
    loader = get_phase4_loader()
    if loader is None:
        try:
            loader = initialize_phase4_loader()
        except FileNotFoundError as e:
            logger.warning(f"Phase 4 loader initialization failed: {e}")
            return None
    return loader


def question_asset_to_info(asset) -> QuestionInfo:
    """Convert QuestionAsset to QuestionInfo."""
    return QuestionInfo(
        id=asset.question_id,
        subject=asset.subject,
        topic=asset.topic,
        grade=asset.grade,
        question_type=asset.question_type,
        difficulty=asset.difficulty,
        points=asset.points,
        estimated_time=asset.estimated_time,
        tags=asset.tags
    )


def question_asset_to_detail(asset) -> QuestionDetail:
    """Convert QuestionAsset to QuestionDetail."""
    return QuestionDetail(
        id=asset.question_id,
        subject=asset.subject,
        topic=asset.topic,
        grade=asset.grade,
        question_type=asset.question_type,
        difficulty=asset.difficulty,
        question_data=asset.question_data,
        points=asset.points,
        estimated_time=asset.estimated_time,
        tags=asset.tags
    )


# ============================================================================
# ENDPOINTS - STATISTICS
# ============================================================================

@router.get("/summary", response_model=Phase4Summary)
def get_phase4_summary():
    """Get Phase 4 overall statistics."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    stats = loader.get_phase4_stats()
    return Phase4Summary(**stats)


@router.get("/stats/subject/{subject}", response_model=SubjectStats)
def get_subject_statistics(subject: str):
    """Get statistics for a specific subject."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    stats = loader.get_subject_stats(subject)
    return SubjectStats(**stats)


# ============================================================================
# ENDPOINTS - QUESTION RETRIEVAL
# ============================================================================

@router.get("/question/{question_id}", response_model=QuestionDetail)
def get_question_by_id(question_id: str):
    """Get a specific question by ID."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    question = loader.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail=f"Question not found: {question_id}")
    
    return question_asset_to_detail(question)


@router.get("/questions/lesson/{lesson_id}", response_model=List[QuestionInfo])
def get_questions_for_lesson(
    lesson_id: str,
    limit: Optional[int] = Query(None, description="Maximum number of questions to return")
):
    """Get all questions for a specific lesson/topic."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    questions = loader.get_questions_for_lesson(lesson_id, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for lesson: {lesson_id}")
    
    return [question_asset_to_info(q) for q in questions]


@router.get("/questions/subject/{subject}", response_model=List[QuestionInfo])
def get_questions_by_subject(
    subject: str,
    limit: Optional[int] = Query(None, description="Maximum number of questions to return")
):
    """Get all questions for a specific subject."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    questions = loader.get_questions_by_subject(subject, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for subject: {subject}")
    
    return [question_asset_to_info(q) for q in questions]


@router.get("/questions/type/{question_type}", response_model=List[QuestionInfo])
def get_questions_by_type(
    question_type: str,
    limit: Optional[int] = Query(10, description="Maximum number of questions to return")
):
    """Get questions of a specific type."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    questions = loader.get_questions_by_type(question_type, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for type: {question_type}")
    
    return [question_asset_to_info(q) for q in questions]


@router.get("/questions/difficulty/{difficulty}", response_model=List[QuestionInfo])
def get_questions_by_difficulty(
    difficulty: str,
    limit: Optional[int] = Query(None, description="Maximum number of questions to return")
):
    """Get questions of a specific difficulty level."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    questions = loader.get_questions_by_difficulty(difficulty, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for difficulty: {difficulty}")
    
    return [question_asset_to_info(q) for q in questions]


@router.get("/questions/random", response_model=List[QuestionDetail])
def get_random_questions(
    count: int = Query(10, description="Number of random questions to return"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty")
):
    """Get random questions with optional filters."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    questions = loader.get_random_questions(count=count, subject=subject, difficulty=difficulty)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available with specified filters")
    
    return [question_asset_to_detail(q) for q in questions]


# ============================================================================
# ENDPOINTS - ANSWER VALIDATION
# ============================================================================

@router.post("/validate", response_model=AnswerValidation)
def validate_answer(submission: AnswerSubmission):
    """Validate a user's answer to a question."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    result = loader.validate_answer(submission.question_id, submission.user_answer)
    
    if not result.get("valid"):
        raise HTTPException(status_code=400, detail=result.get("error", "Invalid answer submission"))
    
    return AnswerValidation(**result)


@router.post("/validate/batch", response_model=List[AnswerValidation])
def validate_answers_batch(submissions: List[AnswerSubmission]):
    """Validate multiple answers at once."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    results = []
    for submission in submissions:
        result = loader.validate_answer(submission.question_id, submission.user_answer)
        results.append(AnswerValidation(**result))
    
    return results


# ============================================================================
# ENDPOINTS - QUIZ GENERATION
# ============================================================================

@router.get("/quiz/generate", response_model=List[QuestionDetail])
def generate_quiz(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    question_count: int = Query(10, description="Number of questions in quiz"),
    include_types: Optional[str] = Query(None, description="Comma-separated list of question types to include")
):
    """Generate a quiz with random questions based on criteria."""
    loader = ensure_phase4_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 4 loader not available")
    
    # Get random questions
    questions = loader.get_random_questions(count=question_count, subject=subject, difficulty=difficulty)
    
    # Filter by question types if specified
    if include_types:
        types = [t.strip() for t in include_types.split(",")]
        questions = [q for q in questions if q.question_type in types]
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available for quiz generation")
    
    return [question_asset_to_detail(q) for q in questions]


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
def health_check():
    """Health check endpoint."""
    loader = get_phase4_loader()
    
    if loader is None:
        return {
            "status": "not_initialized",
            "message": "Phase 4 loader not initialized"
        }
    
    try:
        stats = loader.get_phase4_stats()
        return {
            "status": "healthy",
            "total_questions": stats.get("total_questions", 0),
            "loader_initialized": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "loader_initialized": True
        }
