from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Classroom Device Service")

class Device(BaseModel):
    id: int
    name: str
    status: str
    classroom: str

devices_db: List[Device] = []

@app.post("/devices/register")
def register_device(device: Device):
    devices_db.append(device)
    return {"message": "Device registered", "device": device}

@app.get("/devices/list")
def list_devices():
    return devices_db

@app.post("/devices/update_status")
def update_status(id: int, status: str):
    for device in devices_db:
        if device.id == id:
            device.status = status
            return {"message": "Status updated", "device": device}
    raise HTTPException(status_code=404, detail="Device not found")
