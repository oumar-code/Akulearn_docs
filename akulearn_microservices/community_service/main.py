"""
Community Service
Handles compensation logic and community member data.
"""
from fastapi import FastAPI

app = FastAPI(title="Akulearn Community Service")

# Dummy data
community = [
    {"id": 1, "name": "Alice", "role": "Teacher", "aku": 120},
    {"id": 2, "name": "Bob", "role": "Student", "aku": 30}
]

@app.get("/compensation")
def get_compensation():
    return community
