# FastAPI Classroom Management microservice
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Attendance(BaseModel):
    student_id: str
    present: bool

attendance_log = []

@app.post("/mark_attendance")
def mark_attendance(att: Attendance):
    attendance_log.append(att)
    return {"status": "marked"}

@app.get("/get_attendance")
def get_attendance():
    return attendance_log
