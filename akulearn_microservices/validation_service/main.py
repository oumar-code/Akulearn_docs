"""
Validation Service
Checks file types, sizes, and basic compliance.
"""
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Akulearn Validation Service")

@app.post("/validate")
async def validate_file(file: UploadFile = File(...)):
    # TODO: Validate file type, size, compliance
    return {"valid": True, "reason": "File is valid"}
