"""
Content Upload Service
Receives content submissions from authenticated users.
"""
from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI(title="Akulearn Content Upload Service")

@app.post("/upload")
async def upload_content(user: str = Form(...), file: UploadFile = File(...), metadata: str = Form(...)):
    # TODO: Authenticate user, forward to validation service
    return {"message": "Content received", "filename": file.filename}
