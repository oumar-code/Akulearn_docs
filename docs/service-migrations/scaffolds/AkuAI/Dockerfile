# syntax=docker/dockerfile:1
#
# AkuAI — Shared Inference Layer
# Multi-stage build:
#   builder   — compiles C extensions (llama-cpp-python) and installs all deps
#   runtime   — minimal production image (model weights mounted at runtime)
#
# Image size: ~3-4 GB (dominated by torch — intentionally not baked in).
# Dev note: stubs in services/inference.py mean ML libs are never imported
#           until startup() is replaced with real model-loading code.
#           Runtime RAM stays well within the 512 MB dev mem_limit.

# ── Stage 1: build ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Build tools needed for llama-cpp-python (C++) and asyncpg (C)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        git \
        cmake \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifests only — maximises layer cache
COPY requirements.txt requirements-extra.txt ./

RUN pip install --upgrade pip --no-cache-dir \
 && pip install --prefix=/install --no-cache-dir \
        -r requirements.txt \
        -r requirements-extra.txt

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.source="https://github.com/oumar-code/AkuAI"
LABEL org.opencontainers.image.version="0.1.1"
LABEL org.opencontainers.image.description="AkuAI — shared inference layer for the Aku Platform"

# Runtime libs: libpq5 for asyncpg, libgomp1 for PyTorch OpenMP threading
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for security hardening
RUN groupadd --gid 1001 aku \
 && useradd --uid 1001 --gid aku --no-create-home --shell /sbin/nologin aku

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=aku:aku app/ ./app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Model paths — override these when mounting real weights
    MODEL_DIR="" \
    GEMMA_GGUF_PATH=""

USER aku

EXPOSE 8000

# Healthcheck uses stdlib only (no extra deps needed)
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
