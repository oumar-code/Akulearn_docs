"""
Projector Sync Service
Facilitates data synchronization between offline projector units and the central platform.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Projector Sync Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
