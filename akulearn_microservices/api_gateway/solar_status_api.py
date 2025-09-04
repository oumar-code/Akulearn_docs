# FastAPI endpoint to expose solar status to frontend apps
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class SolarStatus(BaseModel):
    battery_level: float
    panel_output: float
    inverter_status: str
    charge_controller_status: str

@app.get("/solar/status", response_model=SolarStatus)
def get_solar_status():
    # Replace with real hardware integration
    return SolarStatus(
        battery_level=random.uniform(10, 100),
        panel_output=random.uniform(0, 200),
        inverter_status="OK",
        charge_controller_status="Charging"
    )
