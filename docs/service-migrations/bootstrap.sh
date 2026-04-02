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

DEPENDENCY='aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts@v0.1.0'

find . -type f -name 'requirements*.txt' | while read reqfile; do
  # Get the repo root for this requirements file
  reporoot=$(git -C "$(dirname "$reqfile")" rev-parse --show-toplevel 2>/dev/null || true)
  [ -z "$reporoot" ] && continue

  # Add dependency if not present
  if ! grep -qxF "$DEPENDENCY" "$reqfile"; then
    echo "$DEPENDENCY" >> "$reqfile"
    echo "Added to $reqfile"

    # Commit and push if inside a git repo
    cd "$reporoot"
    git add "$reqfile"
    git commit -m "chore: add aku-platform-contracts to $reqfile"
    git push
    cd - >/dev/null
  fi
done
