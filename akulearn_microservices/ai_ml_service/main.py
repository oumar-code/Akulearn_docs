"""
AI/ML Service
Provides adaptive learning recommendations, personalized quizzes, and powers the AI Tutor feature.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn AI/ML Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
