from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Placeholder for AI inference endpoint
def run_local_ai_inference(input_data):
    # TODO: Integrate TensorFlow Lite or PyTorch Mobile
    return {"result": "AI response"}

@app.post("/api/infer")
def infer(data: dict):
    return run_local_ai_inference(data)

# SQLite example
@app.get("/api/students")
def get_students():
    conn = sqlite3.connect("akulearn.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return {"students": students}
