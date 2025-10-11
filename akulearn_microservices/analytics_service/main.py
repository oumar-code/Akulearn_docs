# Aku Platform Analytics Microservice
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class ProgressReport(BaseModel):
    student_id: str
    lesson_id: str
    score: float
    time_spent: int

reports: List[ProgressReport] = []

@app.post("/report_progress")
def report_progress(report: ProgressReport):
    if not report.student_id or not report.lesson_id:
        raise HTTPException(status_code=400, detail="Missing required fields")
    reports.append(report)
    return {"status": "recorded"}

@app.get("/get_reports")
def get_reports():
    return reports
