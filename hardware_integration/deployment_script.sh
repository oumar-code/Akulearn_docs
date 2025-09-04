#!/bin/bash
# Akulearn deployment script for Linux/Ubuntu

# Update system and install dependencies
sudo apt update
sudo apt install -y python3 python3-pip git build-essential docker.io
pip3 install fastapi uvicorn adafruit-circuitpython-ina219 adafruit-circuitpython-ds18x20 adafruit-circuitpython-onewire requests

# Clone repo
if [ ! -d "Akulearn_docs" ]; then
  git clone https://github.com/oumar-code/Akulearn_docs.git
fi
cd Akulearn_docs

# Build and run backend
cd akulearn_microservices/api_gateway
nohup uvicorn hardware_ws_api:app --host 0.0.0.0 --port 8000 &

# Run sensor code
cd ../../hardware_integration
nohup python3 sensor_code.py &

# Start frontend (Vue)
cd ../../unconnected_stack/frontend
npm install
nohup npm run serve &

# Print status
echo "Akulearn backend, hardware integration, and frontend are running."
