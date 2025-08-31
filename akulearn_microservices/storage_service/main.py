"""
Storage Service
Stores content in object storage and metadata in database.
"""
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Akulearn Storage Service")

@app.post("/store")
async def store_content(file: UploadFile = File(...), metadata: str = None):
    # TODO: Store file in IPFS/Filecoin, metadata in MongoDB
    return {"storage_id": "Qm..."}
