# Contribution Guidelines for All Aku Platform Services

Thank you for your interest in contributing to the Aku platform! Please follow these guidelines for all service repositories (Telhone, IGHub, SuperHub, AkuWorkspace, DaaS, AkuAI, AkuTutor, Akudemy, etc.).

---

## Tech Stack Decision

**All Aku Platform backend services use Python 3.11 / FastAPI.**

This is the official, final decision. Every service repo that was scaffolded in Node.js/Express must be migrated to the Python/FastAPI stack. See the full migration guide:

> 📖 [`docs/service-templates/python-fastapi-bootstrap.md`](docs/service-templates/python-fastapi-bootstrap.md)

Key libraries:

| Layer | Library |
|-------|---------|
| Framework | FastAPI |
| ASGI server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Auth | python-jose (JWT) |
| Async messaging | confluent-kafka-python |
| Testing | Pytest + pytest-asyncio + httpx |
| Linting | Ruff + Black + isort |

---

## Source of Truth References

| What | Where |
|------|-------|
| Ecosystem map (all repos, roles, status) | [`docs/ecosystem-map.md`](docs/ecosystem-map.md) |
| Python/FastAPI bootstrap guide | [`docs/service-templates/python-fastapi-bootstrap.md`](docs/service-templates/python-fastapi-bootstrap.md) |
| API specs & database schemas | `docs/02-backend/` |
| Architecture (tiers, components) | `docs/01-architecture/`, `docs/components/` |
| Service specs (Aku Learn, eSIM, DaaS, Workspace) | `docs/services/` |
| Coding standards | `docs/05-cross-cutting/coding-standards.md` |
| Containerisation guide | `docs/05-cross-cutting/containerization.md` |

All specifications and contracts live in the **`Akulearn_docs` monorepo**. The service repos are implementations — when in doubt, the docs here win.

---

## Frontend Source of Truth

The canonical frontend is **`akulearn-dashboard/` inside the `Akulearn_docs` monorepo**:
- All new dashboard pages and marketing changes go into `akulearn-dashboard/`
- It is deployed via Vercel (`.github/workflows/vercel-deploy.yml`)
- Do **not** start new frontend work in `Akudemy-frontend`, `akulearn-dashB`, or `Akulearn-dashboard` — those repos are being archived

---

## Mobile (KMP)

The Kotlin Multiplatform module is being migrated from `KOTLIN MULTIPLATFORM/` in this monorepo to a dedicated `oumar-code/Aku-Mobile` repository. New mobile work should target the new `Aku-Mobile` repo once it is live. See `docs/ecosystem-map.md` for the KMP migration checklist.

---

## Getting Started (per service repo)

1. Fork the repository and clone your fork locally.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```
3. Copy `.env.example` to `.env` and fill in local values.
4. Start the local stack:
   ```bash
   docker compose up -d postgres redis
   uvicorn app.main:app --reload
   ```
5. Create a new feature branch for your changes.
6. Keep commits focused and atomic. Write clear, descriptive commit messages.

---

## Code Style & Quality

- **Linting:** `ruff check .`
- **Formatting:** `black .` and `isort .`
- **Type checking:** use Python type hints on all public functions and class attributes
- **Docstrings:** PEP 257 for all public modules, classes, and functions
- **Tests:** `pytest --cov=app -v` — all PRs must maintain or improve coverage

---

## Environment Variables

- Never commit secrets or `.env` files. See `ENVIRONMENT.md` for details.
- Document every env var in `.env.example` with a comment explaining its purpose.

---

## Opening a Pull Request

- Sync with the latest `main` branch before pushing.
- Open a Pull Request against `main`.
- Fill out the PR template (if available) and describe your changes.
- CI must pass (lint + tests + Docker build) before merging.

---

## What NOT to Commit

- Secrets, `.env` files, or credentials
- Build artifacts or virtual environments (`__pycache__/`, `.venv/`, `dist/`, `site/`)
- IDE/editor config files not required by the project (`node_modules/` if any residual Node files remain during migration)

---

## Questions

Open an issue or discussion in the relevant repository if you have questions, or refer to [`docs/ecosystem-map.md`](docs/ecosystem-map.md) for the full platform picture.
