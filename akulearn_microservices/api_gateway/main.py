"""
API Gateway Microservice
Acts as the central entry point for all client requests, handles routing, authentication, authorization, and rate-limiting.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn API Gateway")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
