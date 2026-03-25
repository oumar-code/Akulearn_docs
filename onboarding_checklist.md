# AkuAI, AkuTutor, AkuWorkspace Onboarding Checklist

Use this checklist to get started with any of the core Node.js microservices.

## 1. Prerequisites
- [ ] Node.js 20+ installed
- [ ] Docker & Docker Compose installed
- [ ] Git installed

## 2. Clone the Repository
- [ ] Clone the repo: `git clone <repo-url>`
- [ ] Enter the directory: `cd <repo-folder>`

## 3. Install Dependencies
- [ ] Run `npm install`

## 4. Environment Setup
- [ ] Copy `.env.example` to `.env` (if present)
- [ ] Fill in required environment variables in `.env`

## 5. Lint & Test
- [ ] Run `npm run lint` (should pass with no errors)
- [ ] Run `npm test` (all tests should pass)

## 6. Build & Run
- [ ] Build Docker image: `docker build -t <service-name>:latest .`
- [ ] Run locally: `npm run dev` or `npm start`
- [ ] Or run with Docker: `docker run -p 8080:8080 <service-name>:latest`

## 7. Multi-Service Orchestration (Recommended)
- [ ] Use Docker Compose if running multiple services together
- [ ] Ensure ports do not conflict (default: 8080)

## 8. Access the Service
- [ ] Visit `http://localhost:8080/` to verify the service is running

## 9. CI/CD & Automation
- [ ] Review `.github/workflows/ci.yml` for automation steps
- [ ] Ensure GitHub Actions are passing on your branch

## 10. Documentation
- [ ] Review `README.md` and `skills.md` for project details

---

_Repeat for AkuAI, AkuTutor, and AkuWorkspace as needed._
