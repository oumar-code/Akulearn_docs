#!/bin/bash
# Deploy Aku Mesh Network frontend (React)

set -e

cd web
npm install
npm run build
nohup npm start &
cd ..

echo "Frontend deployed and running."
