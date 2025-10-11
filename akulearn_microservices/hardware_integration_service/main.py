# FastAPI Hardware Integration microservice
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class EnvSensor(BaseModel):
    temperature: float
    air_quality: float
    light_level: float

class SensorData(BaseModel):
    product_type: str
    voltage: float
    current: float
    temperature: float
    wind_speed: Optional[float] = None

@app.get("/env_status", response_model=EnvSensor)
def get_env_status():
    # Simulate sensor readings
    return EnvSensor(
        temperature=random.uniform(20, 35),
        air_quality=random.uniform(0, 100),
        light_level=random.uniform(100, 1000)
    )

@app.post("/sensor/data")
def ingest_sensor_data(data: SensorData):
    # Store or process sensor data (stub)
    return {"status": "success", "received": data.dict()}

@app.get("/pcb/status")
def get_pcb_status():
    # Return latest sensor status (stub)
    return {"status": "ok", "details": "PCB status placeholder"}

@app.get("/solar/status")
def get_solar_status():
    # Return solar system status (stub)
    return {"status": "ok", "details": "Solar status placeholder"}

@app.get("/wind/status")
def get_wind_status():
    # Return wind system status (stub)
    return {"status": "ok", "details": "Wind status placeholder"}
