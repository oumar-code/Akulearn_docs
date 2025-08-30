#!/bin/bash
# Build Vue PWA
cd ../frontend
npm install
npm run build

# Start FastAPI backend
cd ../backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Nginx (assumes nginx is installed and config is in deployment/nginx.conf)
sudo nginx -c $(pwd)/../deployment/nginx.conf
