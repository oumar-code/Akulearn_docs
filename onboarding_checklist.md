# Aku Platform Service Onboarding Checklist

Use this checklist to get started with any of the 9 Aku Platform backend services (Python 3.11 / FastAPI).

## 1. Prerequisites
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Docker & Docker Compose installed
- [ ] Git installed
- [ ] GitHub CLI (`gh`) installed and authenticated

## 2. Clone the Repository
- [ ] Clone the repo: `git clone https://github.com/oumar-code/<service-name>`
- [ ] Enter the directory: `cd <service-name>`

## 3. Install Dependencies
- [ ] Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

## 4. Environment Setup
- [ ] Copy `.env.example` to `.env`: `cp .env.example .env`
- [ ] Fill in required environment variables in `.env` (DATABASE_URL, REDIS_URL, etc.)
- [ ] Never commit `.env` — it is in `.gitignore`

## 5. Lint & Test
- [ ] Run linting: `ruff check . && black --check . && isort --check .` (should pass with no errors)
- [ ] Run tests: `pytest` (all tests should pass)

## 6. Build & Run
- [ ] Build Docker image: `docker build -t <service-name>:latest .`
- [ ] Run locally (dev mode): `uvicorn app.main:app --reload`
- [ ] Or run with Docker Compose: `docker compose up`
- [ ] Visit `http://localhost:8000/health` to verify the service is running
- [ ] Visit `http://localhost:8000/docs` for the interactive Swagger UI

## 7. Multi-Service Orchestration (Optional)
- [ ] Use the Docker Compose files from the Akulearn_docs repo to run all services together
- [ ] All services expose port 8000 internally and ClusterIP port 80 in Kubernetes

## 8. CI/CD & Automation
- [ ] Review `.github/workflows/` for automation steps (lint, Docker build/push, integration tests)
- [ ] Review `docs/deployment/k8s/<service>.yaml` for the Kubernetes deployment manifest
- [ ] Ensure GitHub Actions are passing on your branch

## 9. Platform Contracts
- [ ] Import shared Pydantic schemas from `aku-platform-contracts`:
  ```sh
  pip install aku-platform-contracts  # from GitHub Packages (oumar-code)
  ```
- [ ] Use topic constants from `aku_platform_contracts.topics` for Kafka messaging

## 10. Documentation
- [ ] Read `docs/ecosystem-map.md` for the full platform architecture
- [ ] Read `docs/service-templates/python-fastapi-bootstrap.md` for the migration guide
- [ ] Read `docs/02-backend/api-specs.md` for API specifications

---

_Applies to: AkuAI, Akudemy, Aku-EdgeHub, Aku-IGHub, Aku-SuperHub, AkuTutor, AkuWorkspace, Aku-DaaS, Aku-Telhone_
