# FastAPI Hardware Integration microservice
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class EnvSensor(BaseModel):
    temperature: float
    air_quality: float
    light_level: float

@app.get("/env_status", response_model=EnvSensor)
def get_env_status():
    # Simulate sensor readings
    return EnvSensor(
        temperature=random.uniform(20, 35),
        air_quality=random.uniform(0, 100),
        light_level=random.uniform(100, 1000)
    )
