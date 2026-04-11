#!/usr/bin/env bash
# bootstrap.sh — Aku Platform contracts dependency injector
#
# Usage (run from THIS docs repo root — it finds every requirements*.txt
# under the current directory and adds the shared contracts pin):
#
#   ./bootstrap.sh
#
# For the full Python/FastAPI service scaffold (app/, tests/, Dockerfile,
# docker-compose.yml, ci.yml, pyproject.toml, requirements.txt, etc.)
# follow the step-by-step guide at:
#   docs/service-templates/python-fastapi-bootstrap.md
#
# Migration tracker: docs/service-migrations/index.md

set -e

DEPENDENCY='aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts.git@v0.1.1'

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
