"""
Content Management Service (CMS)
Manages ingestion, storage, and delivery of curriculum-aligned educational content.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn CMS Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
