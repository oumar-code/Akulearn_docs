# Akulearn Deployment Guide

## Backend Microservices
- Use Docker or systemd to run FastAPI microservices (ai_tutor_service, polls_service, etc.)
- Example Docker Compose:
  ```yaml
  version: '3'
  services:
    ai_tutor:
      build: ./akulearn_microservices/ai_tutor_service
      ports:
        - "8001:8000"
    polls:
      build: ./akulearn_microservices/polls_service
      ports:
        - "8002:8000"
    # Add other services similarly
  ```

## Frontend
- Build and deploy Vue app from `unconnected_stack/frontend`
- Example:
  ```sh
  npm install
  npm run build
  # Deploy dist/ to your web server
  ```

## Systemd Service Example
- For Linux/Ubuntu, create a unit file for each service:
  ```ini
  [Unit]
  Description=Akulearn AI Tutor Service
  After=network.target

  [Service]
  ExecStart=/usr/bin/python3 /path/to/ai_tutor_service/main.py
  Restart=always
  User=akulearn

  [Install]
  WantedBy=multi-user.target
  ```

## OTA Updates
- Use `ota_update.sh` to pull latest code and restart services.

---
See individual microservice and frontend docs for more details.
