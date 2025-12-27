#!/usr/bin/env python3
"""
Wave 3 REST API
FastAPI-based REST API for dashboard, progress tracking, and content access
"""

from fastapi import FastAPI, HTTPException, Query, Path, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uvicorn

# Import our modules
from wave3_interactive_dashboard import Wave3Dashboard
from enhanced_progress_tracker import (
    EnhancedProgressTracker, QuizResult, LearningActivity,
    ActivityType, MasteryLevel
)
from cross_subject_expander import CrossSubjectExpander


# Pydantic models for API
class LessonSummaryModel(BaseModel):
    """Lesson summary response"""
    id: str
    subject: str
    title: str
    description: str
    duration_minutes: int
    difficulty_level: str
    num_objectives: int
    num_sections: int
    num_examples: int
    num_problems: int
    nerdc_codes: List[str]
    waec_topics: List[str]
    keywords: List[str]


class QuizResultModel(BaseModel):
    """Quiz result submission"""
    quiz_id: str
    lesson_id: str
    student_id: str
    score: float
    max_score: float
    time_taken_seconds: int
    questions_correct: int
    questions_total: int
    answers: List[Dict[str, Any]] = []


class ActivityModel(BaseModel):
    """Learning activity submission"""
    student_id: str
    lesson_id: str
    activity_type: str
    duration_seconds: int
    metadata: Dict[str, Any] = {}


class MasteryResponse(BaseModel):
    """Mastery metrics response"""
    lesson_id: str
    student_id: str
    mastery_level: str
    mastery_percentage: float
    total_time_spent_seconds: int
    activities_completed: int
    quiz_average: float
    problems_correct: int
    problems_attempted: int


class SearchQuery(BaseModel):
    """Search query parameters"""
    query: str = Field(..., min_length=1, max_length=200)
    search_type: str = Field(..., pattern="^(nerdc|waec|keyword)$")


class ProgressUpdate(BaseModel):
    """Student progress update"""
    student_id: str
    lesson_id: str
    status: str = Field(..., pattern="^(not_started|in_progress|completed)$")
    progress_percentage: float = Field(..., ge=0, le=100)
    time_spent_minutes: int = Field(default=0, ge=0)
    completed_problems: List[str] = []
    assessment_score: Optional[float] = Field(default=None, ge=0, le=100)


# Initialize FastAPI app
app = FastAPI(
    title="Akulearn Wave 3 API",
    description="REST API for Wave 3 SS1 curriculum content and progress tracking",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
dashboard = Wave3Dashboard(use_neo4j=True)
progress_tracker = EnhancedProgressTracker()
cross_subject = CrossSubjectExpander()


# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "neo4j_available": dashboard.neo4j_available,
        "version": "1.0.0"
    }


# Subjects endpoints
@app.get("/api/subjects", response_model=List[Dict[str, Any]])
async def get_subjects():
    """Get all subjects with lesson counts"""
    subjects = dashboard.get_subjects_overview()
    return subjects


@app.get("/api/subjects/{subject}/lessons", response_model=List[LessonSummaryModel])
async def get_lessons_by_subject(
    subject: str = Path(..., description="Subject name")
):
    """Get all lessons for a subject"""
    lessons = dashboard.get_lessons_by_subject(subject)
    return [lesson.__dict__ for lesson in lessons]


# Lesson endpoints
@app.get("/api/lessons/{lesson_id}")
async def get_lesson(
    lesson_id: str = Path(..., description="Lesson ID")
):
    """Get full lesson content"""
    content = dashboard.get_lesson_content(lesson_id)
    if not content:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return content


@app.get("/api/lessons/{lesson_id}/connections")
async def get_lesson_connections(
    lesson_id: str = Path(..., description="Lesson ID")
):
    """Get cross-subject connections for a lesson"""
    connections = dashboard.get_cross_subject_connections(lesson_id)
    return {"lesson_id": lesson_id, "connections": connections}


# Search endpoints
@app.post("/api/search")
async def search_lessons(query: SearchQuery):
    """Search lessons by NERDC code, WAEC topic, or keyword"""
    if query.search_type == "nerdc":
        lessons = dashboard.search_by_nerdc_code(query.query)
    elif query.search_type == "waec":
        lessons = dashboard.search_by_waec_topic(query.query)
    elif query.search_type == "keyword":
        lessons = dashboard.search_by_keyword(query.query)
    else:
        raise HTTPException(status_code=400, detail="Invalid search type")
    
    return {
        "query": query.query,
        "search_type": query.search_type,
        "results": [lesson.__dict__ for lesson in lessons],
        "count": len(lessons)
    }


@app.get("/api/search/nerdc/{code}")
async def search_by_nerdc(code: str):
    """Search lessons by NERDC code"""
    lessons = dashboard.search_by_nerdc_code(code)
    return {"code": code, "lessons": [lesson.__dict__ for lesson in lessons]}


@app.get("/api/search/waec/{topic}")
async def search_by_waec(topic: str):
    """Search lessons by WAEC topic"""
    lessons = dashboard.search_by_waec_topic(topic)
    return {"topic": topic, "lessons": [lesson.__dict__ for lesson in lessons]}


@app.get("/api/search/keyword/{keyword}")
async def search_by_keyword(keyword: str):
    """Search lessons by keyword"""
    lessons = dashboard.search_by_keyword(keyword)
    return {"keyword": keyword, "lessons": [lesson.__dict__ for lesson in lessons]}


# Progress tracking endpoints
@app.post("/api/progress/quiz")
async def submit_quiz_result(result: QuizResultModel):
    """Submit quiz result"""
    quiz_result = QuizResult(
        quiz_id=result.quiz_id,
        lesson_id=result.lesson_id,
        student_id=result.student_id,
        score=result.score,
        max_score=result.max_score,
        percentage=(result.score / result.max_score * 100) if result.max_score > 0 else 0,
        time_taken_seconds=result.time_taken_seconds,
        questions_correct=result.questions_correct,
        questions_total=result.questions_total,
        attempted_at=datetime.now().isoformat(),
        completed_at=datetime.now().isoformat(),
        answers=result.answers
    )
    
    progress_tracker.record_quiz_result(quiz_result)
    
    return {
        "status": "success",
        "quiz_id": result.quiz_id,
        "percentage": quiz_result.percentage
    }


@app.post("/api/progress/activity")
async def record_activity(activity: ActivityModel):
    """Record learning activity"""
    activity_obj = LearningActivity(
        activity_id=f"act_{datetime.now().timestamp()}",
        student_id=activity.student_id,
        lesson_id=activity.lesson_id,
        activity_type=ActivityType(activity.activity_type),
        duration_seconds=activity.duration_seconds,
        timestamp=datetime.now().isoformat(),
        metadata=activity.metadata
    )
    
    progress_tracker.record_learning_activity(activity_obj)
    
    return {
        "status": "success",
        "activity_id": activity_obj.activity_id
    }


@app.put("/api/progress/update")
async def update_progress(progress: ProgressUpdate):
    """Update student progress for a lesson"""
    dashboard.track_student_progress(
        student_id=progress.student_id,
        lesson_id=progress.lesson_id,
        status=progress.status,
        progress_percentage=progress.progress_percentage,
        time_spent_minutes=progress.time_spent_minutes,
        completed_problems=progress.completed_problems,
        assessment_score=progress.assessment_score
    )
    
    return {
        "status": "success",
        "student_id": progress.student_id,
        "lesson_id": progress.lesson_id
    }


@app.get("/api/progress/student/{student_id}")
async def get_student_progress(student_id: str):
    """Get all progress for a student"""
    progress_list = dashboard.get_student_progress(student_id)
    return {
        "student_id": student_id,
        "progress": [p.__dict__ for p in progress_list],
        "total_lessons": len(progress_list)
    }


@app.get("/api/progress/student/{student_id}/mastery/{lesson_id}")
async def get_mastery_metrics(student_id: str, lesson_id: str):
    """Get mastery metrics for a student and lesson"""
    metrics = progress_tracker.calculate_mastery_metrics(student_id, lesson_id)
    
    if not metrics:
        raise HTTPException(status_code=404, detail="No data found")
    
    return {
        "lesson_id": metrics.lesson_id,
        "student_id": metrics.student_id,
        "mastery_level": metrics.mastery_level.value,
        "mastery_percentage": metrics.mastery_percentage,
        "total_time_spent_seconds": metrics.total_time_spent_seconds,
        "activities_completed": metrics.activities_completed,
        "quiz_average": metrics.quiz_average,
        "problems_correct": metrics.problems_correct,
        "skill_scores": metrics.skill_scores
    }


@app.get("/api/progress/student/{student_id}/overview")
async def get_mastery_overview(student_id: str):
    """Get mastery overview for all lessons"""
    overview = progress_tracker.get_student_mastery_overview(student_id)
    return {
        "student_id": student_id,
        "mastery_data": [
            {
                "lesson_id": m.lesson_id,
                "mastery_level": m.mastery_level.value,
                "mastery_percentage": m.mastery_percentage,
                "time_spent_minutes": m.total_time_spent_seconds / 60
            }
            for m in overview
        ],
        "total_lessons": len(overview)
    }


@app.get("/api/progress/student/{student_id}/analytics")
async def get_time_analytics(
    student_id: str,
    days: int = Query(7, ge=1, le=90, description="Number of days to analyze")
):
    """Get time-on-task analytics"""
    analytics = progress_tracker.get_time_on_task_analytics(student_id, days=days)
    return analytics


@app.get("/api/progress/student/{student_id}/recommendations")
async def get_recommendations(student_id: str, count: int = Query(3, ge=1, le=10)):
    """Get recommended next lessons"""
    recommendations = progress_tracker.recommend_next_lessons(student_id, count=count)
    return {
        "student_id": student_id,
        "recommendations": recommendations,
        "count": len(recommendations)
    }


# Learning paths endpoints
@app.get("/api/learning-paths")
async def get_learning_paths():
    """Get all learning paths"""
    return {
        "paths": [
            {
                "path_id": path.path_id,
                "name": path.name,
                "description": path.description,
                "theme": path.theme,
                "duration_weeks": path.duration_weeks,
                "difficulty_level": path.difficulty_level,
                "lesson_count": len(path.lesson_sequence)
            }
            for path in cross_subject.learning_paths
        ]
    }


@app.get("/api/learning-paths/{path_id}")
async def get_learning_path(path_id: str):
    """Get detailed learning path information"""
    path = next((p for p in cross_subject.learning_paths if p.path_id == path_id), None)
    
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    return {
        "path_id": path.path_id,
        "name": path.name,
        "description": path.description,
        "theme": path.theme,
        "duration_weeks": path.duration_weeks,
        "difficulty_level": path.difficulty_level,
        "lesson_sequence": path.lesson_sequence,
        "skills_developed": [s.value for s in path.skills_developed],
        "prerequisites": path.prerequisites,
        "learning_outcomes": path.learning_outcomes
    }


@app.get("/api/learning-paths/student/{student_id}/recommendations")
async def get_path_recommendations(student_id: str):
    """Get recommended learning paths for a student"""
    recommendations = cross_subject.get_learning_path_recommendations(student_id)
    return {
        "student_id": student_id,
        "recommended_paths": recommendations
    }


# Export endpoints
@app.get("/api/export/lesson/{lesson_id}")
async def export_lesson(
    lesson_id: str,
    format: str = Query("json", pattern="^(json|markdown)$")
):
    """Export lesson for teacher use"""
    export_path = dashboard.export_lesson_for_teacher(lesson_id, format)
    
    if not export_path:
        raise HTTPException(status_code=404, detail="Export failed")
    
    return {
        "status": "success",
        "lesson_id": lesson_id,
        "format": format,
        "file_path": export_path
    }


@app.get("/api/export/report")
async def generate_report():
    """Generate dashboard report"""
    report = dashboard.generate_dashboard_report()
    return report


# Statistics endpoints
@app.get("/api/stats/overview")
async def get_statistics_overview():
    """Get overall statistics"""
    subjects = dashboard.get_subjects_overview()
    
    total_lessons = sum(s['lesson_count'] for s in subjects)
    total_duration = sum(s['lesson_count'] * s['avg_duration'] for s in subjects)
    
    return {
        "total_subjects": len(subjects),
        "total_lessons": total_lessons,
        "total_duration_minutes": total_duration,
        "total_duration_hours": total_duration / 60,
        "avg_lessons_per_subject": total_lessons / len(subjects) if subjects else 0,
        "subjects": subjects
    }


# Shutdown handler
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    dashboard.close()
    progress_tracker.close()
    cross_subject.close()


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Start the API server"""
    print("=" * 60)
    print("Akulearn Wave 3 REST API")
    print("=" * 60)
    print(f"\n🚀 Starting server on http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/api/docs")
    print(f"📖 ReDoc: http://{host}:{port}/api/redoc")
    print("\n" + "=" * 60)
    
    uvicorn.run(
        "wave3_rest_api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Wave 3 REST API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    start_server(host=args.host, port=args.port, reload=args.reload)
