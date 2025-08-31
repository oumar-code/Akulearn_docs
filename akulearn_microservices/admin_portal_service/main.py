"""
Admin Portal Service
Supports user management for administrators and content uploads to the CMS.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Admin Portal Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
