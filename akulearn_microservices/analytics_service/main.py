# FastAPI Analytics microservice
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProgressReport(BaseModel):
    student_id: str
    lesson_id: str
    score: float
    time_spent: int

reports = []

@app.post("/report_progress")
def report_progress(report: ProgressReport):
    reports.append(report)
    return {"status": "recorded"}

@app.get("/get_reports")
def get_reports():
    return reports
