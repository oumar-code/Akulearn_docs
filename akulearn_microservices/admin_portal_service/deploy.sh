#!/bin/bash
# Deploy Aku Admin Portal Service (FastAPI)

# Build and run with uvicorn
pip install -r requirements.txt
nohup uvicorn main:app --host 0.0.0.0 --port 8080 &
echo "Admin portal service running on port 8080."
