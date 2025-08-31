"""
Authentication Service
Manages user registration, login, JWT issuance, and role-based access control.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Auth Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
