# Aku Platform Polls/Q&A Microservice
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import asyncio

app = FastAPI()

class Poll(BaseModel):
    question: str
    options: List[str]

polls: List[Poll] = []
results: Dict[int, List[int]] = {}

@app.post("/create_poll")
def create_poll(poll: Poll):
    poll_id = len(polls)
    polls.append(poll)
    results[poll_id] = [0] * len(poll.options)
    return {"poll_id": poll_id}

@app.post("/vote/{poll_id}")
def vote_poll(poll_id: int, option_index: int):
    if poll_id >= len(polls) or option_index >= len(polls[poll_id].options):
        raise HTTPException(status_code=404, detail="Poll or option not found")
    results[poll_id][option_index] += 1
    return {"status": "vote recorded"}

@app.websocket("/ws/poll/{poll_id}")
async def poll_ws(websocket: WebSocket, poll_id: int):
    await websocket.accept()
    while True:
        await websocket.send_json({"results": results.get(poll_id, [])})
        await asyncio.sleep(2)
