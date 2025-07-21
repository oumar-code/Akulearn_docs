from fastapi import APIRouter, Depends, HTTPException
from src.backend.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["Learning"])

class LastAccessedTopicResponse(BaseModel):
    topic_id: str
    topic_name: str
    last_accessed_at: str

@router.get("/last_accessed_topic", response_model=LastAccessedTopicResponse)
def get_last_accessed_topic(user_id: str, db: Session = Depends(get_db)):
    # Replace with actual ORM query logic
    try:
        # Example: Fetch from user_progress table
        # progress = db.query(UserProgress).filter_by(user_id=user_id).order_by(UserProgress.last_accessed_at.desc()).first()
        # For demo, return placeholder
        return LastAccessedTopicResponse(
            topic_id="topic123",
            topic_name="Algebra Basics",
            last_accessed_at="2025-07-21T10:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
