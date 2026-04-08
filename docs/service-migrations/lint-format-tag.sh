#!/usr/bin/env bash
# lint-format-tag.sh — For each Aku Platform service repo that is already cloned as a
#                       sibling directory, this script:
#                         1. Adds aku-platform-contracts to requirements.txt (idempotent)
#                         2. Removes local class definitions superseded by contracts
#                         3. Rewrites imports to use aku_contracts.*
#                         4. Installs dependencies
#                         5. Formats with Black (matching the running Python version)
#                         6. Lints with flake8 (excluding node_modules, --max-line-length 120)
#                         7. Runs unittest discover
#                         8. Generates openapi.yaml if FastAPI is present
#                         9. Commits and pushes (idempotent — skips empty commits)
#                        10. Creates an annotated tag (skips if already exists on origin)
#
# Usage (run from the directory that CONTAINS all service repos):
#   chmod +x lint-format-tag.sh
#   ./lint-format-tag.sh
#
# Prerequisites:
#   - git installed
#   - Python 3.x installed (py on Windows, python3 on Linux/macOS)
#   - Each service directory must already be a git clone
#
# Migration tracker: docs/service-migrations/index.md

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

# These can be overridden by environment variables so that a CI workflow (or a
# one-off manual invocation) can target a subset of services or a different tag:
#   SERVICES_OVERRIDE="AkuAI Akudemy" TAG_OVERRIDE="v0.1.2" ./lint-format-tag.sh
SERVICES="${SERVICES_OVERRIDE:-AkuAI AkuTutor AkuWorkspace Akudemy Aku-EdgeHub Aku-IGHub Aku-Telhone Aku-SuperHub Aku-DaaS}"
CONTRACT_DEP="aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts@v0.1.0"
TAG="${TAG_OVERRIDE:-v0.1.1}"
TAG_MSG="Release ${TAG} — migrates to aku-platform-contracts"
SUMMARY=""
SUMMARY_FILE="$(mktemp)"

# ── Detect Python binary ───────────────────────────────────────────────────────
# On Windows Git Bash the launcher is 'py'; on Linux/macOS it is 'python3'.

if command -v py &>/dev/null; then
  PYTHON="py"
elif command -v python3 &>/dev/null; then
  PYTHON="python3"
elif command -v python &>/dev/null; then
  PYTHON="python"
else
  echo "Error: Python not found. Install Python 3 and ensure it is on PATH." >&2
  exit 1
fi
echo "Using Python binary: $PYTHON ($($PYTHON --version 2>&1))"

# Derive Black --target-version flag from the running Python version,
# e.g. Python 3.12 → "--target-version py312"
PY_TARGET="py$(${PYTHON} -c 'import sys; print(f"{sys.version_info.major}{sys.version_info.minor}")')"
echo "Black target version: $PY_TARGET"
echo ""

# ── Per-service processing ─────────────────────────────────────────────────────

for svc in $SERVICES; do
  # Skip directories that are not cloned git repos
  if [[ ! -d "$svc" ]] || [[ ! -d "$svc/.git" ]]; then
    echo "⚠  Skipping $svc — directory not found or not a git repo"
    continue
  fi

  # Use pushd/popd so we always return to the original directory, even if a
  # later command fails.  We wrap the whole per-service block in a subshell so
  # an unexpected error does not abort the outer loop.
  (
    reqfile="$svc/requirements.txt"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing $svc..."

    # 1. Add contracts dependency (append; skip if already present) ─────────────
    if [[ ! -f "$reqfile" ]]; then
      echo "  ⚠  requirements.txt not found in $svc — skipping"
      exit 0
    fi
    cp "$reqfile" "$reqfile.bak"
    if ! grep -qxF "$CONTRACT_DEP" "$reqfile"; then
      # FIX: use >> (append) not > (overwrite)
      echo "$CONTRACT_DEP" >> "$reqfile"
      echo "  ✓ Added aku-platform-contracts to $reqfile"
    else
      echo "  ℹ  aku-platform-contracts already in $reqfile"
    fi

    # 2. Remove local class definitions superseded by the contracts package ──────
    for cls in InferenceRequest InferenceResponse ContentItem CredentialRecord; do
      find "$svc" -type f -name "*.py" \
        -exec sed -i.bak "/class ${cls}/,/^$/d" {} +
    done

    # 3. Rewrite imports to aku_contracts.* ─────────────────────────────────────
    #    Match only intra-package imports (relative "from ." or project-local
    #    paths) so that legitimate third-party imports are never touched.
    find "$svc" -type f -name "*.py" -exec sed -i.bak \
      -e 's|from \(\.\|app\|schemas\|models\)[^ ]* import InferenceRequest|from aku_contracts.inference.schemas import InferenceRequest|' \
      -e 's|from \(\.\|app\|schemas\|models\)[^ ]* import InferenceResponse|from aku_contracts.inference.schemas import InferenceResponse|' \
      -e 's|from \(\.\|app\|schemas\|models\)[^ ]* import ContentItem|from aku_contracts.content.schemas import ContentItem|' \
      -e 's|from \(\.\|app\|schemas\|models\)[^ ]* import CredentialRecord|from aku_contracts.credentials.schemas import CredentialRecord|' \
      {} +

    # Clean up sed backup files
    find "$svc" -type f -name "*.bak" -delete

    # 4. Install dependencies ────────────────────────────────────────────────────
    echo "  Installing dependencies..."
    pushd "$svc" > /dev/null
    $PYTHON -m pip install --upgrade pip -q
    $PYTHON -m pip install -r requirements.txt -q

    # 5. Format with Black ───────────────────────────────────────────────────────
    #    --target-version is set to the running Python so Black's safety check
    #    does not warn about a version mismatch.
    echo "  Formatting with Black (target: $PY_TARGET)..."
    $PYTHON -m pip install black -q || true
    $PYTHON -m black --target-version "$PY_TARGET" .

    # 6. Lint with flake8 ────────────────────────────────────────────────────────
    #    --exclude=node_modules prevents scanning third-party JS artefacts.
    #    --max-line-length 120 avoids noise from lines that Black already wraps.
    echo "  Linting with flake8..."
    $PYTHON -m pip install flake8 -q || true
    $PYTHON -m flake8 . \
      --exclude=node_modules,__pycache__,.git,.tox,.venv \
      --max-line-length 120 \
      || echo "  ⚠  Linting failed in $svc (non-fatal)"

    # 7. Run tests ───────────────────────────────────────────────────────────────
    echo "  Running tests..."
    TEST_RESULT="FAIL"
    if $PYTHON -m unittest discover 2>&1; then
      TEST_RESULT="PASS"
    fi

    # 8. Generate OpenAPI YAML (FastAPI only, non-fatal) ─────────────────────────
    if grep -q "fastapi" requirements.txt; then
      echo "  Generating openapi.yaml..."
      $PYTHON -c "
from app.main import app
import yaml
openapi = app.openapi()
with open('openapi.yaml', 'w') as f:
    yaml.dump(openapi, f)
" 2>/dev/null || echo "  ⚠  OpenAPI generation failed in $svc (non-fatal)"
    fi

    # 9. Commit and push ─────────────────────────────────────────────────────────
    git add .
    # Skip commit gracefully if nothing changed (idempotent re-runs)
    if git diff --cached --quiet; then
      echo "  ℹ  Nothing to commit in $svc"
    else
      git commit -m "chore: migrate to aku-platform-contracts, lint, format, test, and update OpenAPI"
      git push
    fi

    # 10. Create annotated tag (skip if already exists on origin) ───────────────
    #     FIX: check remote before tagging to prevent "already exists" fatal error.
    if git ls-remote --exit-code --tags origin "refs/tags/${TAG}" &>/dev/null; then
      echo "  ℹ  Tag ${TAG} already exists on origin — skipping"
    else
      git tag -a "$TAG" -m "$TAG_MSG"
      git push origin "$TAG"
      echo "  ✓ Tagged and pushed $TAG"
    fi

    popd > /dev/null
    echo "  ✓ Done — Test=${TEST_RESULT}"
    # Append to summary (written to a temp file so it survives the subshell)
    echo "$svc: Test=${TEST_RESULT}" >> "$SUMMARY_FILE"
  ) || echo "  ❌ Error in $svc — see output above"

  echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "All service repos processed and tagged ${TAG}."
echo ""
echo "Summary:"
if [[ -f "$SUMMARY_FILE" ]]; then
  cat "$SUMMARY_FILE"
  rm -f "$SUMMARY_FILE"
else
  echo "(no services processed)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
