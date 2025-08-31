"""
Notification Service
Alerts users on submission status and review outcomes.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Notification Service")

@app.post("/notify")
async def notify_user(user_id: str, message: str):
    # TODO: Send notification to user
    return {"notified": True}
