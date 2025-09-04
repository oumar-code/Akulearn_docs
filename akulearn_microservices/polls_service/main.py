# FastAPI Live Polls/Q&A microservice
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import asyncio

app = FastAPI()

class Poll(BaseModel):
    question: str
    options: list[str]

polls = []
results = {}

@app.post("/create_poll")
def create_poll(poll: Poll):
    poll_id = len(polls)
    polls.append(poll)
    results[poll_id] = [0] * len(poll.options)
    return {"poll_id": poll_id}

@app.websocket("/ws/poll/{poll_id}")
async def poll_ws(websocket: WebSocket, poll_id: int):
    await websocket.accept()
    while True:
        await websocket.send_json({"results": results.get(poll_id, [])})
        await asyncio.sleep(2)
