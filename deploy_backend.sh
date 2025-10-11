#!/bin/bash
# Deploy all Aku Mesh backend microservices

set -e

# Deploy Tier 1 Edge Node (Go)
echo "Starting Mesh Agent (Edge Node)..."
cd akulearn_microservices/mesh_agent
nohup go run main.go &
cd ../../

# Deploy Tier 2 Super Hub (Python)
echo "Starting Super Hub Service..."
cd akulearn_microservices/super_hub_service
nohup uvicorn main:app --host 0.0.0.0 --port 8082 &
cd ../../

# Deploy Tier 3 IG-Hub (Python)
echo "Starting IG-Hub Service..."
cd akulearn_microservices/ig_hub_service
nohup uvicorn main:app --host 0.0.0.0 --port 8083 &
cd ../../

# Deploy DaaS Service (Python)
echo "Starting DaaS Service..."
cd akulearn_microservices/daas_service
nohup uvicorn main:app --host 0.0.0.0 --port 8084 &
cd ../../

echo "All backend services started."
