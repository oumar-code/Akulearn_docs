"""
User Profile Service
Stores and manages profiles for all user types and tracks individual progress.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn User Profile Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
