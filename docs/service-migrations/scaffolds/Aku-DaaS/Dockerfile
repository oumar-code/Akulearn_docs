# syntax=docker/dockerfile:1
#
# Aku-DaaS — Data governance & anonymisation pipelines
# Multi-stage build:
#   builder   — installs all deps (including pandas/pyarrow C extensions)
#   runtime   — minimal production image

# ── Stage 1: build ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-extra.txt ./

RUN pip install --upgrade pip --no-cache-dir \
 && pip install --prefix=/install --no-cache-dir \
        -r requirements.txt \
        -r requirements-extra.txt

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.source="https://github.com/oumar-code/Aku-DaaS"
LABEL org.opencontainers.image.version="0.1.1"
LABEL org.opencontainers.image.description="Aku-DaaS — data governance and anonymisation pipelines for the Aku Platform"

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1001 aku \
 && useradd --uid 1001 --gid aku --no-create-home --shell /sbin/nologin aku

WORKDIR /app

COPY --from=builder /install /usr/local

COPY --chown=aku:aku app/ ./app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER aku

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python - <<'EOF'
import urllib.request, sys
try:
    urllib.request.urlopen("http://localhost:8000/health", timeout=4)
    sys.exit(0)
except Exception:
    sys.exit(1)
EOF

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
