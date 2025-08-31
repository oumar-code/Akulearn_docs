"""
Transcoding Service
Converts videos to multiple resolutions/formats.
"""
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Akulearn Transcoding Service")

@app.post("/transcode")
async def transcode_video(file: UploadFile = File(...)):
    # TODO: Transcode video to multiple formats
    return {"message": "Video transcoded", "formats": ["720p", "480p"]}
