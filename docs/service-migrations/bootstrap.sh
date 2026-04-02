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

#!/bin/bash
set -e

# Scaffold package structure
mkdir -p aku_contracts/{inference,content,credentials,clearing,esim,datasets,events,openapi}
touch aku_contracts/__init__.py
for d in inference content credentials clearing esim datasets events; do
  touch aku_contracts/$d/__init__.py
done

# Initial Pydantic schemas
cat > aku_contracts/inference/schemas.py <<EOF
from pydantic import BaseModel, Field

class InferenceRequest(BaseModel):
    model: str = Field(..., description="Model identifier, e.g. 'gemma-2b'")
    prompt: str = Field(..., max_length=8192)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    stream: bool = False

class InferenceResponse(BaseModel):
    model: str
    generated_text: str
    tokens_used: int
    latency_ms: float
EOF

cat > aku_contracts/content/schemas.py <<EOF
from pydantic import BaseModel, Field

class ContentItem(BaseModel):
    id: str
    title: str
    body: str
    subject: str
    tags: list[str] = []

class LessonSummary(BaseModel):
    lesson_id: str
    title: str
    summary: str

class SyncPayload(BaseModel):
    items: list[ContentItem]
    since: str
EOF

cat > aku_contracts/credentials/schemas.py <<EOF
from pydantic import BaseModel, Field

class CredentialRecord(BaseModel):
    id: str
    subject: str
    issued_at: str
    credential_type: str
    data: dict

class IssuanceRequest(BaseModel):
    subject: str
    credential_type: str
    data: dict

class VerifyResult(BaseModel):
    valid: bool
    reason: str | None = None
EOF

# Kafka topic constants
cat > aku_contracts/events/kafka_topics.py <<EOF
# Kafka topic name constants

INFERENCE_REQUESTED = "inference.requested"
CONTENT_SYNC_REQUESTED = "content.sync.requested"
CREDENTIAL_ISSUED = "credential.issued"
EOF

# pyproject.toml
cat > pyproject.toml <<EOF
[project]
name = "aku-platform-contracts"
version = "0.1.0"
description = "Shared Pydantic schemas and Kafka topic constants for Aku Platform services"
authors = [{name = "Platform Architecture"}]
dependencies = [
    "pydantic>=2.0.0"
]
EOF

# README.md
cat > README.md <<EOF
# aku-platform-contracts

Shared Pydantic schemas and Kafka topic constants for Aku Platform backend services.
EOF

# GitHub Actions workflow
mkdir -p .github/workflows
cat > .github/workflows/publish.yml <<EOF
name: Build and Publish

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install build tools
        run: pip install build
      - name: Build package
        run: python -m build
      - name: Publish to GitHub Packages
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://upload.pypi.org/legacy/
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: \${{ secrets.PYPI_API_TOKEN }}
EOF

# Initial commit and tag
git add .
git commit -m "feat: scaffold aku-platform-contracts package and CI"
git tag v0.1.0

echo "Scaffold complete. Review, push to GitHub, and publish the v0.1.0 release."