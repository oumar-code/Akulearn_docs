# Python / FastAPI Service Bootstrap Guide

This guide is the step-by-step playbook for migrating every Aku Platform backend service from its current Node.js stub to **Python 3.11 / FastAPI**. Follow this guide for each service repo: `Aku-EdgeHub`, `Aku-SuperHub`, `Aku-IGHub`, `Akudemy`, `AkuAI`, `AkuTutor`, `AkuWorkspace`, `Aku-DaaS`, `Aku-Telhone`.

---

## Why Python / FastAPI?

- Aligns with the AI/ML tooling ecosystem (PyTorch, HuggingFace Transformers, LangChain, llama-cpp-python)
- Consistent with documented backend stack in `docs/02-backend/index.md` and `docs/05-cross-cutting/coding-standards.md`
- Async-first: FastAPI is built on Starlette + ASGI, making it natural for I/O-heavy microservices
- First-class Pydantic support: automatic request validation and OpenAPI generation
- Matches the `requirements.txt` and Python scripts (`team.py`, `supabase_provision.py`) already used in this monorepo

---

## Standard Project Structure

Every service must follow this layout:

```
<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory, startup/shutdown events
│   ├── config.py            # Pydantic Settings (reads from env vars)
│   ├── dependencies.py      # Shared FastAPI dependencies (db session, auth)
│   ├── models/              # SQLAlchemy ORM models
│   │   └── __init__.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   └── __init__.py
│   ├── routers/             # APIRouter modules (one per domain)
│   │   └── __init__.py
│   ├── services/            # Business logic (no direct HTTP in here)
│   │   └── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py       # Async SQLAlchemy engine & session factory
│   │   └── base.py          # Declarative Base
│   └── middleware/          # Custom Starlette middleware
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py          # Pytest fixtures (test DB, test client)
│   ├── test_health.py
│   └── test_<domain>.py
├── .env.example             # Documented env vars (no secrets)
├── .gitignore
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Local dev stack (app + postgres + redis)
├── requirements.txt         # Pinned production deps
├── requirements-dev.txt     # Dev/test deps
├── alembic.ini
├── pyproject.toml           # Ruff, Black, isort config
└── README.md
```

---

## Step 1 — Scaffold the Project

```bash
# From the service repo root
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install fastapi uvicorn[standard] pydantic-settings \
    sqlalchemy[asyncio] asyncpg alembic redis \
    python-jose[cryptography] passlib[bcrypt] \
    confluent-kafka httpx

pip install --dev pytest pytest-asyncio pytest-cov httpx \
    ruff black isort

pip freeze > requirements.txt
```

---

## Step 2 — Application Factory (`app/main.py`)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.routers import health, v1_router
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.service_name,
        version=settings.version,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(v1_router, prefix="/api/v1")
    return app


app = create_app()
```

---

## Step 3 — Config (`app/config.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "aku-service"
    version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://aku:aku@localhost:5432/aku_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # Service discovery (used when calling other Aku services)
    aku_ai_url: str = "http://localhost:3001"
    aku_ighub_url: str = "http://localhost:3002"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"


settings = Settings()
```

---

## Step 4 — Database Session (`app/db/session.py`)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

---

## Step 5 — Health Check Router (`app/routers/health.py`)

```python
from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": settings.version,
    }
```

---

## Step 6 — JWT Auth Dependency (`app/dependencies.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import settings

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

---

## Step 7 — Dockerfile (Multi-Stage)

```dockerfile
# syntax=docker/dockerfile:1

# ── Build stage ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Production stage ───────────────────────────────────────────────────────
FROM python:3.11-slim AS production
WORKDIR /app

LABEL org.opencontainers.image.source="https://github.com/oumar-code/<service-name>"
LABEL org.opencontainers.image.version="0.1.0"

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from build stage
COPY --from=builder /install /usr/local

# Non-root user
RUN useradd --uid 1001 --create-home aku
USER aku

COPY --chown=aku:aku app/ ./app/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Step 8 — Docker Compose (Local Dev)

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: aku
      POSTGRES_PASSWORD: aku
      POSTGRES_DB: aku_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aku"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Step 9 — GitHub Actions CI (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: aku
          POSTGRES_PASSWORD: aku
          POSTGRES_DB: aku_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Configure git credentials for private packages
        run: git config --global url."https://${{ secrets.GH_PAT }}@github.com/".insteadOf "https://github.com/"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint (Ruff)
        run: ruff check .

      - name: Format check (Black)
        run: black --check .

      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://aku:aku@localhost:5432/aku_test
          JWT_SECRET_KEY: test-secret-key
        run: pytest --cov=app --cov-report=xml -v

  docker:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t aku/<service-name>:${{ github.sha }} .
```

---

## Step 10 — pyproject.toml (Linting Config)

```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501"]

[tool.black]
line-length = 100

[tool.isort]
profile = "black"
line_length = 100

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## Migration Checklist (per service repo)

- [ ] Delete all existing Node.js files (`package.json`, `index.js`, `src/`)
- [ ] Scaffold project structure from Step 1
- [ ] Implement `app/main.py`, `app/config.py`, `app/db/session.py`
- [ ] Add health check endpoint
- [ ] Port domain logic from the service spec in `docs/services/` or `docs/02-backend/`
- [ ] Add Dockerfile (multi-stage, non-root)
- [ ] Add `docker-compose.yml` for local dev
- [ ] Add `.github/workflows/ci.yml` (lint + test + docker build)
- [ ] Add `.env.example` with all documented env vars
- [ ] Update `README.md` with Python/FastAPI getting started instructions
- [ ] Add service to the automation tracking in `Akulearn_docs/automation_progress.md`

---

## Service-Specific Notes

### Aku-EdgeHub
- Add endpoints for: local content cache status, sync trigger, device registration, offline AI relay
- Uses SQLite (`aiosqlite`) for local offline store — swap `asyncpg` for `aiosqlite` in the offline-only container
- See `docs/01-architecture/index.md` for the Edge Hub architecture

### Aku-IGHub
- Add Aku Coin clearing endpoints (POST `/api/v1/clearing/settle`)
- Add credential registry endpoints (POST `/api/v1/credentials/issue`, GET `/api/v1/credentials/{id}/verify`)
- Add anonymised metadata exchange endpoints (POST `/api/v1/metadata/publish`)
- See `docs/components/aku-ig-hub.md` and `docs/services/aku-daas.md` for the IG-Hub ↔ DaaS flow

### Aku-Telhone (eSIM — domain realignment required)
- Remove generic telephony (calls/SMS) CRUD — that is not Telhone's domain
- Implement eSIM provisioning: `POST /api/v1/esim/provision`, `PATCH /api/v1/esim/{iccid}/switch-network`, `DELETE /api/v1/esim/{iccid}`
- Add OTA push agent (background task via `asyncio.create_task`)
- See `docs/services/aku-esim.md` for the full spec

### Aku-DaaS
- Remove "device management" routes — that was an error in the stub
- Implement dataset ingestion (POST `/api/v1/datasets/ingest`), anonymisation pipeline, IG-Hub metadata publishing
- See `docs/services/aku-daas.md` for the `curl` examples and data governance requirements

### AkuAI
- This service is the **shared inference layer** for the entire platform
- Expose: `POST /api/v1/inference`, `POST /api/v1/text/generate`, `POST /api/v1/text/classify`, `POST /api/v1/text/summarize`
- Add a Gemma local inference endpoint for Edge Hub use
- All other services (AkuTutor, AkuWorkspace, Akudemy) call AkuAI via its REST API; they do NOT bundle their own models
- See `docs/ai_tutor.md` and `docs/ml_training_pipeline.md` for full AI service spec

### AkuTutor
- Consumes AkuAI via `settings.aku_ai_url`; does NOT run its own model
- Focus on curriculum-aware prompt construction, session management, feedback loop
- See `docs/ai_tutor.md`

### AkuWorkspace
- Consumes AkuAI for NL understanding, Aku-DaaS for datasets, Akudemy for content
- Focus on workflow orchestration and the AI Assistant abstraction layer
- See `docs/services/aku-workspace.md`

### Akudemy (Aku Learn)
- Offline-first: implement content sync API that Edge Hubs can call (GET `/api/v1/content/sync?since=<timestamp>`)
- Blockchain credential issuance: POST `/api/v1/credentials/issue` → calls Polygon via `docs/tech_stack.md` PolygonService
- See `docs/services/aku-learn.md` for the complete service spec
