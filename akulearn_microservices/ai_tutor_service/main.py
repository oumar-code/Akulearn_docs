# FastAPI AI Tutor microservice
from fastapi import FastAPI, Query
from pydantic import BaseModel
import random

app = FastAPI()

class TutorRequest(BaseModel):
    question: str
    context: str = ""

class TutorResponse(BaseModel):
    answer: str
    hints: list[str]

@app.post("/ask", response_model=TutorResponse)
def ask_tutor(req: TutorRequest):
    # Placeholder: Replace with real AI model integration
    answer = f"AI answer to: {req.question}"
    hints = ["Think about the main concept.", "Review your notes."]
    return TutorResponse(answer=answer, hints=hints)
