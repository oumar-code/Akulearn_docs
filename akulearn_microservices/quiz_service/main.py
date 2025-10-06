from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Quiz Service")

class Quiz(BaseModel):
    id: int
    question: str
    options: List[str]
    answer: int

quizzes_db: List[Quiz] = []

@app.post("/quiz/add")
def add_quiz(quiz: Quiz):
    quizzes_db.append(quiz)
    return {"message": "Quiz added", "quiz": quiz}

@app.get("/quiz/list")
def list_quizzes():
    return quizzes_db
