# FastAPI WebSocket backend for hardware status push updates
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import random

app = FastAPI()

# Simulated hardware status
status = {
    'sensor': {'voltage': 12.6, 'current': 2.1, 'temperature': 32.5},
    'solar': {'panel_output': 120, 'inverter_status': 'OK', 'charge_controller_status': 'Charging'}
}

@app.websocket('/ws/hardware')
async def hardware_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Simulate status change
        status['sensor']['voltage'] = round(random.uniform(11.5, 13.0), 2)
        status['sensor']['current'] = round(random.uniform(0, 10), 2)
        status['sensor']['temperature'] = round(random.uniform(20, 45), 2)
        status['solar']['panel_output'] = round(random.uniform(0, 200), 2)
        await websocket.send_json({'type': 'sensor', 'payload': status['sensor']})
        await websocket.send_json({'type': 'solar', 'payload': status['solar']})
        await asyncio.sleep(10)
