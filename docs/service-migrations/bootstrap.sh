#!/usr/bin/env bash
# bootstrap.sh — Aku Platform Python/FastAPI migration scaffold
#
# Usage (run from the target service repo root):
#   ./bootstrap.sh <service-name>
#
# Example:
#   ./bootstrap.sh AkuAI
#
# What it generates:
#   app/  tests/  alembic/  Dockerfile  docker-compose.yml
#   .github/workflows/ci.yml  pyproject.toml  requirements.txt
#   requirements-dev.txt  alembic.ini  .env.example  .gitignore
#
# Full playbook: docs/service-templates/python-fastapi-bootstrap.md
# Migration tracker: docs/service-migrations/index.md

set -euo pipefail

# ── Arguments ─────────────────────────────────────────────────────────────────
SERVICE_NAME="${1:-}"
if [[ -z "$SERVICE_NAME" ]]; then
  echo "Error: service name is required." >&2
  echo "Usage: ./bootstrap.sh <service-name>" >&2
  exit 1
fi

SERVICE_SLUG="${SERVICE_NAME,,}"   # lowercase
SERVICE_SLUG="${SERVICE_SLUG//_/-}"  # underscores → hyphens

echo "→ Bootstrapping Python/FastAPI project for: ${SERVICE_NAME}"

# ── Directory layout ──────────────────────────────────────────────────────────
mkdir -p app/{models,schemas,routers,services,db,middleware}
mkdir -p alembic/versions
mkdir -p tests
mkdir -p .github/workflows

# ── app/__init__.py ───────────────────────────────────────────────────────────
cat > app/__init__.py << 'EOF'
EOF

# ── app/main.py ───────────────────────────────────────────────────────────────
cat > app/main.py << EOF
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
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
    return app


app = create_app()
EOF

# ── app/config.py ─────────────────────────────────────────────────────────────
cat > app/config.py << EOF
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "${SERVICE_SLUG}"
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

    # Service discovery
    aku_ai_url: str = "http://localhost:3001"
    aku_ighub_url: str = "http://localhost:3002"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"


settings = Settings()
EOF

# ── app/dependencies.py ───────────────────────────────────────────────────────
cat > app/dependencies.py << 'EOF'
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
EOF

# ── app/db/base.py ────────────────────────────────────────────────────────────
cat > app/db/__init__.py << 'EOF'
EOF
cat > app/db/base.py << 'EOF'
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
EOF

# ── app/db/session.py ─────────────────────────────────────────────────────────
cat > app/db/session.py << 'EOF'
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
EOF

# ── app/routers/ ──────────────────────────────────────────────────────────────
cat > app/routers/__init__.py << 'EOF'
EOF
cat > app/routers/health.py << 'EOF'
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
EOF

# ── Stub __init__.py files ────────────────────────────────────────────────────
for pkg in app/models app/schemas app/services app/middleware; do
    cat > "${pkg}/__init__.py" << 'EOF'
EOF
done

# ── tests/ ────────────────────────────────────────────────────────────────────
cat > tests/conftest.py << 'EOF'
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
EOF

cat > tests/test_health.py << 'EOF'
import pytest


@pytest.mark.anyio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
EOF

# ── alembic.ini ───────────────────────────────────────────────────────────────
cat > alembic.ini << 'EOF'
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql+asyncpg://aku:aku@localhost:5432/aku_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF

# ── alembic/env.py ────────────────────────────────────────────────────────────
cat > alembic/env.py << 'EOF'
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.db.base import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(connection=conn, target_metadata=target_metadata)
        )
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
EOF

# ── requirements.txt ──────────────────────────────────────────────────────────
cat > requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic-settings==2.4.0
sqlalchemy[asyncio]==2.0.35
asyncpg==0.29.0
alembic==1.13.2
redis==5.0.8
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
confluent-kafka==2.5.0
httpx==0.27.2
EOF

# ── requirements-dev.txt ──────────────────────────────────────────────────────
cat > requirements-dev.txt << 'EOF'
pytest==8.3.2
pytest-asyncio==0.24.0
anyio[trio]==4.6.0
pytest-cov==5.0.0
ruff==0.6.9
black==24.8.0
isort==5.13.2
EOF

# ── pyproject.toml ────────────────────────────────────────────────────────────
cat > pyproject.toml << EOF
[project]
name = "${SERVICE_SLUG}"
version = "0.1.0"
requires-python = ">=3.11"

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
EOF

# ── .env.example ──────────────────────────────────────────────────────────────
cat > .env.example << EOF
# ${SERVICE_NAME} — environment variables
# Copy to .env and fill in values before running

SERVICE_NAME=${SERVICE_SLUG}
VERSION=0.1.0
ENVIRONMENT=development
DEBUG=false

DATABASE_URL=postgresql+asyncpg://aku:aku@localhost:5432/aku_db
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

AKU_AI_URL=http://localhost:3001
AKU_IGHUB_URL=http://localhost:3002

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
EOF

# ── .gitignore ────────────────────────────────────────────────────────────────
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/
.eggs/

# Environment
.env

# Testing
.pytest_cache/
.coverage
coverage.xml
htmlcov/

# IDE
.idea/
.vscode/
*.iml

# Docker
*.log
EOF

# ── Dockerfile ────────────────────────────────────────────────────────────────
cat > Dockerfile << EOF
# syntax=docker/dockerfile:1

# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \\
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Production stage ───────────────────────────────────────────────────────────
FROM python:3.11-slim AS production
WORKDIR /app

LABEL org.opencontainers.image.source="https://github.com/oumar-code/${SERVICE_NAME}"
LABEL org.opencontainers.image.version="0.1.0"

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \\
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

RUN useradd --uid 1001 --create-home aku
USER aku

COPY --chown=aku:aku app/ ./app/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# ── docker-compose.yml ────────────────────────────────────────────────────────
cat > docker-compose.yml << EOF
version: "3.9"
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
EOF

# ── .github/workflows/ci.yml ──────────────────────────────────────────────────
cat > .github/workflows/ci.yml << EOF
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
        run: docker build -t aku/${SERVICE_SLUG}:\${{ github.sha }} .
EOF

echo ""
echo "✅ Scaffold complete for: ${SERVICE_NAME}"
echo ""
echo "Next steps:"
echo "  1. cd into the service repo and review the generated files"
echo "  2. Add service-specific domain endpoints (see docs/service-migrations/index.md)"
echo "  3. git checkout -b feat/python-fastapi-migration"
echo "  4. git add . && git commit -m 'feat: migrate to Python 3.11 / FastAPI'"
echo "  5. git push origin feat/python-fastapi-migration"
echo "  6. Open a PR, then update docs/service-migrations/index.md status to ✅ Done"
