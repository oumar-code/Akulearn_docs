from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="School Management Service")

class Student(BaseModel):
    id: int
    name: str
    grade: str
    attendance: int = 0
    health_record: Optional[str] = None

class Staff(BaseModel):
    id: int
    name: str
    role: str
    email: str

class TimetableEntry(BaseModel):
    id: int
    class_name: str
    teacher: str
    time: str

students_db: List[Student] = []
staff_db: List[Staff] = []
timetable_db: List[TimetableEntry] = []

@app.post("/students/add")
def add_student(student: Student):
    students_db.append(student)
    return {"message": "Student added", "student": student}

@app.get("/students/list")
def list_students():
    return students_db

@app.post("/staff/add")
def add_staff(staff: Staff):
    staff_db.append(staff)
    return {"message": "Staff added", "staff": staff}

@app.get("/staff/list")
def list_staff():
    return staff_db

@app.post("/timetable/add")
def add_timetable(entry: TimetableEntry):
    timetable_db.append(entry)
    return {"message": "Timetable entry added", "entry": entry}

@app.get("/timetable/list")
def list_timetable():
    return timetable_db
