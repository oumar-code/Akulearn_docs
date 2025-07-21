from fastapi import APIRouter, Depends, HTTPException
from src.backend.dependencies import get_db, is_guardian
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/guardian", tags=["Guardian"])

class StudentResponse(BaseModel):
    user_id: str
    first_name: str
    last_name: str

@router.get("/students", response_model=List[StudentResponse], dependencies=[Depends(is_guardian)])
def get_linked_students(guardian_id: str, db: Session = Depends(get_db)) -> List[StudentResponse]:
    # Replace with actual ORM query logic
    try:
        # Example: Fetch students where users.guardian_id == guardian_id
        # students = db.query(User).filter_by(guardian_id=guardian_id, role='student').all()
        # For demo, return placeholder
        return [
            StudentResponse(user_id="student1", first_name="Ada", last_name="Obi"),
            StudentResponse(user_id="student2", first_name="Bola", last_name="Adewale")
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Exam results endpoint
class ExamResult(BaseModel):
    exam_name: str
    score: int

class ExamResultsResponse(BaseModel):
    results: List[ExamResult]

@router.get("/user/exam_results/{user_id}", response_model=ExamResultsResponse)
def get_exam_results(user_id: str, db: Session = Depends(get_db)) -> ExamResultsResponse:
    # Replace with actual ORM query logic
    try:
        # For demo, return static data
        return ExamResultsResponse(results=[
            ExamResult(exam_name="JAMB", score=75),
            ExamResult(exam_name="WAEC", score=82)
        ])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
