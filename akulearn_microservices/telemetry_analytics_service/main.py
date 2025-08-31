"""
Telemetry & Analytics Service
Collects usage data and device health metrics from all parts of the system.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Telemetry & Analytics Service")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
