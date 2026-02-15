# Akulearn Backend - Main FastAPI Application
# Comprehensive API for Nigerian student learning platform

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
import os
import json
from typing import Dict, Optional, List
from datetime import datetime

# Import services
try:
    from auth_service import auth_service
    from questions_service import questions_service
    from progress_service import progress_service
    from content_service import content_service
except ImportError:
    print("WARNING: Services not imported. Make sure auth_service.py, questions_service.py, progress_service.py, content_service.py exist.")
    auth_service = None
    questions_service = None
    progress_service = None
    content_service = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Akulearn API",
    description="Learning platform API for Nigerian secondary students preparing for WAEC, NECO, JAMB",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration: Concurrency control for connected users
TOTAL_SLOTS = int(os.getenv("AKU_TOTAL_SLOTS", "10"))
PRIORITY_RESERVED = int(os.getenv("AKU_RESERVED_SLOTS", "4"))

# Ensure sensible defaults
if PRIORITY_RESERVED >= TOTAL_SLOTS:
    PRIORITY_RESERVED = max(1, TOTAL_SLOTS // 2)

PRIORITY_SEM = asyncio.Semaphore(PRIORITY_RESERVED)
GENERAL_SEM = asyncio.Semaphore(TOTAL_SLOTS - PRIORITY_RESERVED)

# Global app state
app_state = {
    "questions_loaded": False,
    "startup_time": None
}


# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize app: load questions data."""
    try:
        app_state["startup_time"] = datetime.utcnow().isoformat()
        
        if questions_service:
            logger.info("Loading exam questions...")
            result = questions_service.load_questions()
            
            if result.get("success"):
                logger.info(f"✓ Loaded {result['statistics']['total_questions']} exam questions")
                app_state["questions_loaded"] = True
            else:
                logger.warning(f"✗ Failed to load questions: {result.get('error')}")
        
        logger.info("✓ Akulearn backend started successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Akulearn backend...")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_connected_user(request: Request) -> bool:
    """Determine if request is from a connected-stack app user."""
    try:
        if request.headers.get("X-AKU-APP", "").lower() == "connected":
            return True
        if request.query_params.get("connected") == "1":
            return True
    except Exception:
        pass
    return False


def get_token_from_request(request: Request) -> Optional[str]:
    """Extract JWT token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def verify_token(token: str) -> Dict:
    """Verify JWT token using auth service."""
    if not auth_service:
        return {"success": False, "error": "Auth service not available"}
    
    return auth_service.verify_token(token)


async def get_current_user(request: Request) -> Dict:
    """Dependency: Get current authenticated user."""
    token = get_token_from_request(request)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token"
        )
    
    result = verify_token(token)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("error", "Invalid token")
        )
    
    return result.get("payload", {})


# ============================================================================
# HEALTH & METRICS
# ============================================================================

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "questions_loaded": app_state["questions_loaded"],
        "startup_time": app_state["startup_time"]
    }


@app.get("/api/metrics")
async def metrics(request: Request):
    """Runtime metrics (accessible to connected users)."""
    if not is_connected_user(request):
        raise HTTPException(status_code=403, detail="Connected users only")
    
    priority_available = getattr(PRIORITY_SEM, "_value", PRIORITY_RESERVED)
    general_available = getattr(GENERAL_SEM, "_value", TOTAL_SLOTS - PRIORITY_RESERVED)
    
    return {
        "total_slots": TOTAL_SLOTS,
        "reserved": PRIORITY_RESERVED,
        "priority_available": priority_available,
        "general_available": general_available,
        "active_questions": app_state["questions_loaded"],
        "questions_in_system": 1350
    }


# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.post("/api/auth/register")
async def register(request: Request):
    """Register a new student."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = auth_service.register(
        email=data.get("email"),
        password=data.get("password"),
        full_name=data.get("full_name"),
        phone=data.get("phone"),
        exam_board=data.get("exam_board"),
        target_subjects=data.get("target_subjects", [])
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {
        "user_id": result["user_id"],
        "email": result["email"],
        "message": result["message"],
        "verification_token": result["verification_token"]
    }


@app.post("/api/auth/verify-otp")
async def verify_otp(request: Request):
    """Verify OTP for email verification."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = auth_service.verify_otp(
        email=data.get("email"),
        otp=data.get("otp")
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {"verified": True, "message": result["message"]}


@app.post("/api/auth/resend-otp")
async def resend_otp(request: Request):
    """Resend OTP to user's email."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = auth_service.resend_otp(email=data.get("email"))
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return {"message": result["message"]}


@app.post("/api/auth/login")
async def login(request: Request):
    """Login with email and password."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = auth_service.login(
        email=data.get("email"),
        password=data.get("password")
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error"))
    
    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "user_id": result["user_id"],
        "email": result["email"],
        "full_name": result["full_name"],
        "expires_in": result["expires_in"]
    }


@app.post("/api/auth/refresh-token")
async def refresh_token(request: Request):
    """Refresh expired access token."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    result = auth_service.refresh_token(refresh_token=data.get("refresh_token"))
    
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error"))
    
    return {
        "access_token": result["access_token"],
        "expires_in": result["expires_in"]
    }


@app.post("/api/auth/logout")
async def logout(current_user: Dict = Depends(get_current_user)):
    """Logout user."""
    if not auth_service:
        raise HTTPException(status_code=500, detail="Auth service not available")
    
    return {"message": "Logged out successfully"}


# ============================================================================
# QUESTIONS & SEARCH
# ============================================================================

@app.get("/api/questions/search")
async def search_questions(
    request: Request,
    q: Optional[str] = None,
    exam_board: Optional[str] = None,
    subject: Optional[str] = None,
    topic: Optional[str] = None,
    year: Optional[int] = None,
    difficulty: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Search for exam questions with filters."""
    if not questions_service:
        raise HTTPException(status_code=500, detail="Questions service not available")
    
    if not app_state["questions_loaded"]:
        raise HTTPException(status_code=503, detail="Questions database not loaded yet")
    
    # Validate pagination
    limit = min(limit, 100)
    offset = max(offset, 0)
    
    result = questions_service.search(
        query=q,
        exam_board=exam_board,
        subject=subject,
        topic=topic,
        year=year,
        difficulty=difficulty,
        limit=limit,
        offset=offset
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/api/questions/{question_id}")
async def get_question(
    question_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get full question details (requires authentication)."""
    if not questions_service:
        raise HTTPException(status_code=500, detail="Questions service not available")
    
    result = questions_service.get_question(question_id, include_answer=True)
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail="Question not found")
    
    return result["question"]


@app.get("/api/questions/random")
async def get_random_questions(
    count: int = 15,
    exam_board: Optional[str] = None,
    subject: Optional[str] = None,
    difficulty: Optional[str] = None
):
    """Get random questions for quiz or readiness assessment."""
    if not questions_service:
        raise HTTPException(status_code=500, detail="Questions service not available")
    
    count = max(1, min(count, 50))
    
    result = questions_service.get_random_questions(
        count=count,
        exam_board=exam_board,
        subject=subject,
        difficulty=difficulty
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/api/questions/filters")
async def get_filters():
    """Get available filter options (exam boards, subjects, topics, etc.)."""
    if not questions_service:
        raise HTTPException(status_code=500, detail="Questions service not available")
    
    result = questions_service.get_filters()
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail="Failed to get filters")
    
    return result["filters"]


# ============================================================================
# USER ATTEMPTS & PROGRESS
# ============================================================================

@app.post("/api/questions/attempt")
async def record_attempt(request: Request, current_user: Dict = Depends(get_current_user)):
    """Record a user's answer to a question."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    user_id = current_user.get("user_id")
    
    result = progress_service.record_attempt(
        user_id=user_id,
        question_id=data.get("question_id"),
        user_answer=data.get("user_answer"),
        correct_answer=data.get("correct_answer"),
        time_taken_seconds=data.get("time_taken_seconds", 0),
        exam_board=data.get("exam_board"),
        subject=data.get("subject"),
        topic=data.get("topic")
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/api/user/progress")
async def get_progress(current_user: Dict = Depends(get_current_user)):
    """Get user's overall progress statistics."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    user_id = current_user.get("user_id")
    
    result = progress_service.get_progress(user_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/api/user/weak-topics")
async def get_weak_topics(current_user: Dict = Depends(get_current_user)):
    """Get topics where user is struggling."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    user_id = current_user.get("user_id")
    
    result = progress_service.get_weak_topics(user_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.post("/api/user/bookmarks")
async def bookmark_question(request: Request, current_user: Dict = Depends(get_current_user)):
    """Bookmark a question for later review."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    user_id = current_user.get("user_id")
    
    result = progress_service.bookmark_question(
        user_id=user_id,
        question_id=data.get("question_id")
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@app.get("/api/user/bookmarks")
async def get_bookmarks(current_user: Dict = Depends(get_current_user)):
    """Get all bookmarked questions."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    user_id = current_user.get("user_id")
    
    result = progress_service.get_bookmarks(user_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


# ============================================================================
# READINESS ASSESSMENT
# ============================================================================

@app.post("/api/readiness/start-assessment")
async def start_assessment(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Start a new readiness assessment (15 random questions)."""
    if not questions_service:
        raise HTTPException(status_code=500, detail="Questions service not available")
    
    try:
        data = await request.json() if request.method == "POST" else {}
    except:
        data = {}
    
    exam_board = data.get("exam_board")
    
    result = questions_service.get_random_questions(
        count=15,
        exam_board=exam_board
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    # Generate assessment ID
    import secrets
    assessment_id = f"assess_{secrets.token_hex(6)}"
    
    return {
        "assessment_id": assessment_id,
        "questions": result["questions"],
        "estimated_time_minutes": 15,
        "total_questions": 15
    }


@app.post("/api/readiness/submit-assessment")
async def submit_assessment(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Submit completed readiness assessment."""
    if not progress_service:
        raise HTTPException(status_code=500, detail="Progress service not available")
    
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    user_id = current_user.get("user_id")
    assessment_id = data.get("assessment_id")
    answers = data.get("answers", [])
    exam_board = data.get("exam_board")
    
    # Calculate score
    correct_count = sum(1 for answer in answers if answer.get("is_correct"))
    total_count = len(answers)
    
    # Record assessment
    result = progress_service.record_assessment(
        user_id=user_id,
        assessment_id=assessment_id,
        exam_board=exam_board,
        correct_count=correct_count,
        total_count=total_count,
        answers=answers
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    # Identify weak topics from assessment
    weak_topics_result = progress_service.get_weak_topics(user_id)
    weak_topics = weak_topics_result.get("weak_topics", [])
    
    return {
        "assessment_id": assessment_id,
        "score": result["score"],
        "total_questions": result["total_questions"],
        "accuracy_percent": result["accuracy_percent"],
        "pass_probability_percent": result["pass_probability_percent"],
        "weak_topics": weak_topics[:3],
        "next_steps": "Continue practicing weak topics. Take mock exams weekly."
    }


# ============================================================================
# CONTENT MANAGEMENT
# ============================================================================

@app.get("/api/content/subjects")
async def get_subjects():
    """Get list of all subjects with available content."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    subjects = content_service.get_subjects()
    return {
        "subjects": subjects,
        "count": len(subjects)
    }

@app.get("/api/content/{subject}/topics")
async def get_topics_by_subject(subject: str):
    """Get topics for a specific subject."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    topics = content_service.get_topics_by_subject(subject)
    return {
        "subject": subject,
        "topics": topics,
        "count": len(topics)
    }

@app.get("/api/content/{subject}/{topic}")
async def get_content_by_topic(subject: str, topic: str):
    """Get all content for a subject-topic combination."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    content_list = content_service.get_content_by_subject_topic(subject, topic)

    return {
        "subject": subject,
        "topic": topic,
        "content": [
            {
                "id": c.id,
                "title": c.title,
                "content_type": c.content_type.value,
                "difficulty": c.difficulty.value,
                "estimated_read_time": c.estimated_read_time,
                "tags": c.tags,
                "created_at": c.created_at.isoformat()
            }
            for c in content_list
        ],
        "count": len(content_list)
    }

@app.get("/api/content/{content_id}")
async def get_content_by_id(content_id: str, current_user: Dict = Depends(get_current_user)):
    """Get full content details by ID."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    content = content_service.get_content_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Track that user viewed this content
    user_id = current_user.get("user_id")

    return {
        "id": content.id,
        "title": content.title,
        "subject": content.subject,
        "topic": content.topic,
        "content_type": content.content_type.value,
        "difficulty": content.difficulty.value,
        "content": content.content,
        "estimated_read_time": content.estimated_read_time,
        "prerequisites": content.prerequisites,
        "related_questions": content.related_questions,
        "tags": content.tags,
        "author": content.author,
        "version": content.version,
        "created_at": content.created_at.isoformat(),
        "updated_at": content.updated_at.isoformat()
    }

@app.get("/api/content/search")
async def search_content(
    q: str,
    subject: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = 20
):
    """Search content by keyword."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")

    results = content_service.search_content(q.strip(), subject, content_type)

    # Limit results
    results = results[:limit]

    return {
        "query": q,
        "total": len(results),
        "limit": limit,
        "content": [
            {
                "id": c.id,
                "title": c.title,
                "subject": c.subject,
                "topic": c.topic,
                "content_type": c.content_type.value,
                "difficulty": c.difficulty.value,
                "estimated_read_time": c.estimated_read_time,
                "tags": c.tags,
                "preview": c.content[:200] + "..." if len(c.content) > 200 else c.content
            }
            for c in results
        ]
    }

@app.get("/api/content/recommendations")
async def get_recommendations(
    current_user: Dict = Depends(get_current_user),
    subject: Optional[str] = None,
    limit: int = 10
):
    """Get personalized content recommendations."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    user_id = current_user.get("user_id")
    recommendations = content_service.get_recommendations(user_id, subject, limit)

    return {
        "recommendations": [
            {
                "id": c.id,
                "title": c.title,
                "subject": c.subject,
                "topic": c.topic,
                "content_type": c.content_type.value,
                "difficulty": c.difficulty.value,
                "estimated_read_time": c.estimated_read_time,
                "tags": c.tags
            }
            for c in recommendations
        ],
        "count": len(recommendations)
    }

@app.post("/api/content/{content_id}/progress")
async def update_content_progress(
    content_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update user progress on content."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    user_id = current_user.get("user_id")
    time_spent = data.get("time_spent", 0)
    completed = data.get("completed", False)

    if time_spent < 0:
        raise HTTPException(status_code=400, detail="Time spent cannot be negative")

    content_service.update_progress(user_id, content_id, time_spent, completed)

    return {
        "success": True,
        "message": "Progress updated successfully"
    }

@app.get("/api/user/content-progress")
async def get_user_content_progress(current_user: Dict = Depends(get_current_user)):
    """Get user's content reading progress."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    user_id = current_user.get("user_id")
    progress = content_service.get_user_progress(user_id)

    return progress

@app.get("/api/content/stats")
async def get_content_stats():
    """Get content statistics."""
    if not content_service:
        raise HTTPException(status_code=500, detail="Content service not available")

    stats = content_service.get_content_stats()
    return stats


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# TESTING
# ============================================================================

@app.get("/api/test/db-status")
async def test_db_status():
    """Test endpoint to check database initialization."""
    if questions_service:
        filters = questions_service.get_filters()
        if filters.get("success"):
            return {
                "status": "healthy",
                "questions_loaded": True,
                "filters": filters["filters"]
            }
    
    return {
        "status": "not_ready",
        "questions_loaded": False
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
