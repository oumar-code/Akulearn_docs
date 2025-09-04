# Akulearn Hardware Integration Guide

## 1. Hardware Block Diagram
See `akulearn_hardware_block_diagram.png` for a visual overview of the system:
- Solar Panel → Charge Controller → Battery → Inverter → Smart Board/TV/Projector Hub
- Sensors (voltage, current, temperature) connect to PCB, which interfaces with the backend via API.

## 2. Wiring & Assembly
- Follow the wiring diagram in `solar_power_wiring_diagram.md`.
- Use fuses/breakers as specified for safety.
- Mount all hardware in the enclosure (`akulearn_enclosure_cad.step`).

## 3. Sensor Code & Backend Connection
- Install dependencies:
  ```sh
  pip install adafruit-circuitpython-ina219 adafruit-circuitpython-ds18x20 adafruit-circuitpython-onewire requests
  ```
- Connect sensors to PCB as per schematic (`akulearn_sensor_pcb.sch`).
- Run `sensor_code.py` to read sensors and POST data to backend (`sensor_api.py`).

## 4. Backend API Setup
- Start FastAPI backend with endpoints for sensor and solar status.
- Example endpoints:
  - `/sensor/data` (POST): Receives sensor readings
  - `/pcb/status` (GET): Returns latest sensor status
  - `/solar/status` (GET): Returns solar system status

## 5. Dashboard Integration
- Use `dashboard_hardware_status.vue` in your frontend to display real-time hardware data.
- Fetch data from backend endpoints and show warnings for low battery, faults, etc.

## 6. Maintenance & Troubleshooting
- Follow `maintenance_checklist.pdf` for regular system checks.
- Use diagnostic scripts to test hardware and API connectivity.
- Refer to troubleshooting guides for common issues.

---

This guide ensures a consistent, safe, and maintainable integration of all Akulearn hardware and software components.
