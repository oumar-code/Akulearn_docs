# Aku Platform AI Tutor Microservice
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TutorRequest(BaseModel):
    question: str
    context: str = ""

class TutorResponse(BaseModel):
    answer: str
    hints: List[str]

@app.post("/ask", response_model=TutorResponse)
def ask_tutor(req: TutorRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail="Question required")
    # Placeholder: Replace with real AI model integration
    answer = f"AI answer to: {req.question}"
    hints = ["Think about the main concept.", "Review your notes."]
    return TutorResponse(answer=answer, hints=hints)
