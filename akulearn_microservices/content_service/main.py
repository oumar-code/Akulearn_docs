from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Content Service")

class Content(BaseModel):
    id: int
    title: str
    type: str
    url: str

content_db: List[Content] = []

@app.post("/content/add")
def add_content(content: Content):
    content_db.append(content)
    return {"message": "Content added", "content": content}

@app.get("/content/list")
def list_content():
    return content_db
