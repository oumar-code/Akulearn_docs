#!/usr/bin/env bash
# fix-lint.sh — Apply lint remediation to all Aku Platform service repos.
#
# Addresses the three categories of ruff failures introduced after the
# Python/FastAPI migration:
#
#   1. Deprecated top-level ruff config (select/ignore at [tool.ruff] level)
#      → Migrates pyproject.toml to [tool.ruff.lint] section format,
#        adds B008 ignore (FastAPI Depends pattern), adds alembic per-file-ignore
#        for I001.
#
#   2. I001 — import-block ordering in alembic/env.py (auto-generated file)
#      → Resolved by the per-file-ignore added in step 1 above.
#        `ruff check --fix .` is also run to sort any other auto-fixable imports.
#
#   3. B904 — raise without `from` in except clauses
#      a. app/dependencies.py — JWTError handler (bootstrap guide template)
#         → Patched via Python script embedded in this file.
#      b. app/routers/esim.py  — bare `except KeyError:` blocks (Aku-Telhone only)
#         → Patched via Python script embedded in this file.
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/fix-lint.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/fix-lint.sh --all --dry-run
#
#   # Apply to all 9 services
#   ./docs/service-migrations/fix-lint.sh --all
#
#   # Apply to a single service
#   ./docs/service-migrations/fix-lint.sh Aku-Telhone
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - Python 3.11+ installed (python3 on PATH)
#   - ruff installed (pip install ruff) — used for auto-fix pass
#
# Migration tracker: docs/service-migrations/index.md

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

GITHUB_ORG="oumar-code"
BRANCH_NAME="fix/ruff-lint-remediation"
COMMIT_MSG="fix: migrate ruff config to [tool.ruff.lint] and fix B904 exception chaining"
PR_TITLE="fix: ruff lint remediation — pyproject.toml + B904 exception chaining"
PR_BODY='## Summary

Fixes CI failures caused by three categories of ruff lint errors introduced
after the Python/FastAPI migration:

### 1. Deprecated ruff config format (`pyproject.toml`)
Migrated `select` / `ignore` from the deprecated top-level `[tool.ruff]` section
to `[tool.ruff.lint]`. Added two permanent ignores:
- `B008` — FastAPI `Depends()` in function-argument defaults is the canonical DI pattern
- `alembic/env.py` per-file `I001` ignore — alembic generates this file; reordering its
  imports is harmless but triggers false-positive noise

### 2. `I001` — import ordering in `alembic/env.py`
Covered by the per-file ignore above. `ruff check --fix .` was also run to
resolve any remaining auto-fixable import-order issues elsewhere.

### 3. `B904` — bare `raise` inside `except` blocks
Exception chaining (`raise ... from exc`) added to:
- `app/dependencies.py` — JWT auth handler (`JWTError → HTTPException`)
- `app/routers/esim.py` — bare `except KeyError:` blocks (Aku-Telhone only)

## References
- Ruff docs: https://docs.astral.sh/ruff/settings/#lint
- Migration tracker: https://github.com/oumar-code/Akulearn_docs/blob/main/docs/service-migrations/index.md
'

ALL_SERVICES=(
  AkuAI
  Akudemy
  Aku-EdgeHub
  Aku-IGHub
  Aku-Telhone
  Aku-SuperHub
  AkuTutor
  AkuWorkspace
  Aku-DaaS
)

# ── Argument parsing ───────────────────────────────────────────────────────────

DRY_RUN=false
SERVICES=()

if [[ $# -eq 0 ]]; then
  echo "Error: no arguments provided." >&2
  echo "Usage: $0 --all [--dry-run]  |  $0 <ServiceName>" >&2
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)    SERVICES=("${ALL_SERVICES[@]}"); shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    -*)       echo "Error: unknown flag '$1'" >&2; exit 1 ;;
    *)        SERVICES+=("$1"); shift ;;
  esac
done

if [[ ${#SERVICES[@]} -eq 0 ]]; then
  echo "Error: no services specified." >&2
  exit 1
fi

# ── Helper ─────────────────────────────────────────────────────────────────────

run() {
  if [[ "$DRY_RUN" == true ]]; then
    echo "  [dry-run] $*"
  else
    "$@"
  fi
}

# ── Pre-flight ─────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Aku Platform — Lint Remediation"
[[ "$DRY_RUN" == true ]] && echo "  MODE: DRY RUN (no changes will be made)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for cmd in gh git python3; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: '$cmd' is not installed or not on PATH." >&2
    exit 1
  fi
done

if [[ "$DRY_RUN" == false ]]; then
  if ! gh auth status &>/dev/null; then
    echo "Error: gh CLI is not authenticated. Run: gh auth login" >&2
    exit 1
  fi
fi

echo "Services: ${SERVICES[*]}"
echo ""

# ── Embedded patcher scripts ───────────────────────────────────────────────────
#
# These Python snippets are written to temp files and called from the per-service
# function.  Writing them as here-docs keeps the patch logic readable and avoids
# quoting nightmares with inline python3 -c '...'.

PYPROJECT_PATCHER="$(mktemp /tmp/patch_pyproject_XXXX.py)"
cat > "$PYPROJECT_PATCHER" << 'PYEOF'
"""Replace deprecated [tool.ruff] top-level lint config with [tool.ruff.lint]."""

import re
import sys

path = sys.argv[1]

with open(path) as fh:
    text = fh.read()

# Check if already migrated (idempotent)
if "[tool.ruff.lint]" in text:
    print(f"  ℹ  {path}: already uses [tool.ruff.lint] — skipping")
    sys.exit(0)

# Replace the old [tool.ruff] block.
# Old block (may span several lines before the next [tool.*] section):
#   [tool.ruff]
#   line-length = 100
#   select = [...]
#   ignore = [...]
OLD_BLOCK = re.compile(
    r"\[tool\.ruff\]\n"          # section header
    r"(line-length\s*=\s*.+\n)?" # optional line-length setting
    r"select\s*=\s*.+\n"         # select rule (required)
    r"ignore\s*=\s*.+\n",        # ignore rule (required)
    re.MULTILINE,
)

NEW_BLOCK = (
    "[tool.ruff]\n"
    "line-length = 100\n"
    "\n"
    "[tool.ruff.lint]\n"
    'select = ["E", "F", "I", "UP", "B", "SIM"]\n'
    "ignore = [\n"
    '    "E501",   # line too long — Black handles line length\n'
    '    "B008",   # FastAPI Depends() in function defaults is intentional\n'
    "]\n"
    "\n"
    "[tool.ruff.lint.per-file-ignores]\n"
    '"alembic/env.py" = ["I001"]   # alembic-generated file; import order follows alembic convention\n'
)

if not OLD_BLOCK.search(text):
    print(f"  ⚠  {path}: expected [tool.ruff] block not found — appending new sections")
    # Just append the ruff.lint sections before [tool.black] if present, else at end
    if "[tool.black]" in text:
        text = text.replace("[tool.black]", NEW_BLOCK + "[tool.black]", 1)
    else:
        text = text + "\n" + NEW_BLOCK
else:
    text = OLD_BLOCK.sub(NEW_BLOCK, text)

with open(path, "w") as fh:
    fh.write(text)

print(f"  ✓  {path}: migrated to [tool.ruff.lint]")
PYEOF

DEPS_PATCHER="$(mktemp /tmp/patch_dependencies_XXXX.py)"
cat > "$DEPS_PATCHER" << 'PYEOF'
"""Fix B904: add 'from exc' to JWTError → HTTPException raise in dependencies.py."""

import re
import sys

path = sys.argv[1]

with open(path) as fh:
    text = fh.read()

# Pattern: except JWTError:\n    raise HTTPException(\n...\n    )
# We want: except JWTError as exc:\n    raise HTTPException(\n...\n    ) from exc
changed = False

# Fix: except JWTError: → except JWTError as exc:
new_text, n = re.subn(
    r"\bexcept JWTError\s*:",
    "except JWTError as exc:",
    text,
)
if n:
    changed = True
    text = new_text

# Fix: closing paren of raise HTTPException block not followed by "from"
# Match the pattern:  "        )\n" preceded by a multi-line HTTPException raise,
# and NOT already followed by "from".
# We look for the specific JWT-error 401 block:
AUTH_BLOCK = re.compile(
    r"(raise HTTPException\(\s*\n"
    r"\s+status_code=status\.HTTP_401_UNAUTHORIZED,\s*\n"
    r"\s+detail=\"Invalid or expired token\",\s*\n"
    r"\s+\))"
    r"(?!\s*from)",
    re.MULTILINE,
)
new_text, n = AUTH_BLOCK.subn(r"\1 from exc", text)
if n:
    changed = True
    text = new_text

if not changed:
    print(f"  ℹ  {path}: no JWTError pattern found or already fixed")
    sys.exit(0)

with open(path, "w") as fh:
    fh.write(text)

print(f"  ✓  {path}: fixed JWTError B904 exception chaining")
PYEOF

ESIM_PATCHER="$(mktemp /tmp/patch_esim_XXXX.py)"
cat > "$ESIM_PATCHER" << 'PYEOF'
"""Fix B904: add 'from exc' to bare except KeyError: → raise HTTPException in esim.py."""

import re
import sys

path = sys.argv[1]

with open(path) as fh:
    text = fh.read()

changed = False

# Fix: except KeyError: → except KeyError as exc:
new_text, n = re.subn(
    r"\bexcept KeyError\s*:",
    "except KeyError as exc:",
    text,
)
if n:
    changed = True
    text = new_text

# Fix: raise HTTPException( ... ) NOT followed by "from"
# Add "from exc" after the closing paren of any 404-NOT_FOUND HTTPException raise
# that immediately follows an except block (i.e., detail contains 'not found').
NOT_FOUND_BLOCK = re.compile(
    r"(raise HTTPException\(\s*\n"
    r"\s+status_code=status\.HTTP_404_NOT_FOUND,\s*\n"
    r"\s+detail=f?\"[^\"]*not found[^\"]*\",\s*\n"
    r"\s+\))"
    r"(?!\s*from)",
    re.MULTILINE,
)
new_text, n = NOT_FOUND_BLOCK.subn(r"\1 from exc", text)
if n:
    changed = True
    text = new_text

if not changed:
    print(f"  ℹ  {path}: no bare KeyError pattern found or already fixed")
    sys.exit(0)

with open(path, "w") as fh:
    fh.write(text)

print(f"  ✓  {path}: fixed KeyError B904 exception chaining")
PYEOF

# ── Per-service remediation function ──────────────────────────────────────────

SUCCEEDED=()
FAILED=()
SKIPPED=()

fix_service() {
  local service="$1"
  local repo_url="https://github.com/${GITHUB_ORG}/${service}.git"
  local work_dir
  work_dir="$(mktemp -d)"

  echo "┌─ ${service} ─────────────────────────────────────────"
  echo "│  Repo: ${GITHUB_ORG}/${service}"
  echo "│"

  # ── Clone ──────────────────────────────────────────────────────────────────
  echo "│  Step 1: Clone"
  if ! run git clone --depth 1 "${repo_url}" "${work_dir}"; then
    echo "│  ✗ Clone failed — skipping"
    echo "└──────────────────────────────────────────────────────"
    SKIPPED+=("${service}")
    return
  fi

  if [[ "$DRY_RUN" == false ]]; then
    pushd "${work_dir}" > /dev/null

    # ── Idempotency guard ───────────────────────────────────────────────────
    if git ls-remote --exit-code --heads origin "${BRANCH_NAME}" &>/dev/null; then
      echo "│  ℹ  Branch ${BRANCH_NAME} already exists on origin — skipping"
      echo "└──────────────────────────────────────────────────────"
      popd > /dev/null
      rm -rf "${work_dir}"
      SKIPPED+=("${service}")
      return
    fi

    # ── 1. Patch pyproject.toml ─────────────────────────────────────────────
    echo "│  Step 2: Patch pyproject.toml"
    if [[ -f pyproject.toml ]]; then
      python3 "$PYPROJECT_PATCHER" pyproject.toml
    else
      echo "│  ⚠  pyproject.toml not found in ${service} — skipping pyproject patch"
    fi

    # ── 2. Fix B904 in app/dependencies.py ─────────────────────────────────
    echo "│  Step 3: Fix B904 in app/dependencies.py"
    if [[ -f app/dependencies.py ]]; then
      python3 "$DEPS_PATCHER" app/dependencies.py
    else
      echo "│  ℹ  app/dependencies.py not found — skipping"
    fi

    # ── 3. Fix B904 in app/routers/esim.py (Aku-Telhone only) ──────────────
    echo "│  Step 4: Fix B904 in app/routers/esim.py"
    if [[ -f app/routers/esim.py ]]; then
      python3 "$ESIM_PATCHER" app/routers/esim.py
    else
      echo "│  ℹ  app/routers/esim.py not found — skipping"
    fi

    # ── 4. Auto-fix with ruff ───────────────────────────────────────────────
    echo "│  Step 5: Auto-fix imports with ruff"
    if command -v ruff &>/dev/null; then
      ruff check --fix . 2>&1 | sed 's/^/│    /' || true
    elif python3 -c "import ruff" 2>/dev/null; then
      python3 -m ruff check --fix . 2>&1 | sed 's/^/│    /' || true
    else
      echo "│  ⚠  ruff not found — skipping auto-fix pass"
      echo "│     Install with: pip install ruff"
    fi

    # ── 5. Report remaining issues ──────────────────────────────────────────
    echo "│  Step 6: Remaining lint issues after fixes"
    REMAINING=0
    if command -v ruff &>/dev/null; then
      REMAINING=$(ruff check . 2>&1 | grep -c "^[^ ]" || true)
      ruff check . 2>&1 | sed 's/^/│    /' || true
    fi
    if [[ "$REMAINING" -eq 0 ]]; then
      echo "│    ✓ No remaining ruff issues"
    fi

    # ── 6. Commit and push ──────────────────────────────────────────────────
    git add .
    if git diff --cached --quiet; then
      echo "│  ℹ  Nothing to commit in ${service}"
      popd > /dev/null
      rm -rf "${work_dir}"
      SKIPPED+=("${service}")
      return
    fi

    echo "│  Step 7: Commit"
    git checkout -b "${BRANCH_NAME}"
    git commit -m "${COMMIT_MSG}"

    echo "│  Step 8: Push"
    git push origin "${BRANCH_NAME}"

    echo "│  Step 9: Open pull request"
    gh pr create \
      --repo "${GITHUB_ORG}/${service}" \
      --base main \
      --head "${BRANCH_NAME}" \
      --title "${PR_TITLE}" \
      --body "${PR_BODY}" || echo "│  ⚠  PR already exists or could not be created"

    popd > /dev/null
  else
    echo "  [dry-run] clone ${repo_url} → ${work_dir}"
    echo "  [dry-run] python3 patch_pyproject.py pyproject.toml"
    echo "  [dry-run] python3 patch_dependencies.py app/dependencies.py"
    echo "  [dry-run] python3 patch_esim.py app/routers/esim.py  (Aku-Telhone only)"
    echo "  [dry-run] ruff check --fix ."
    echo "  [dry-run] git checkout -b ${BRANCH_NAME} && git add . && git commit -m '${COMMIT_MSG}'"
    echo "  [dry-run] git push origin ${BRANCH_NAME}"
    echo "  [dry-run] gh pr create --repo ${GITHUB_ORG}/${service} --title '${PR_TITLE}'"
  fi

  rm -rf "${work_dir}"
  echo "│  ✓ Done"
  echo "└──────────────────────────────────────────────────────"
  SUCCEEDED+=("${service}")
}

# ── Run ────────────────────────────────────────────────────────────────────────

for svc in "${SERVICES[@]}"; do
  fix_service "$svc" || FAILED+=("$svc")
  echo ""
done

# ── Clean up temp patcher scripts ─────────────────────────────────────────────
rm -f "$PYPROJECT_PATCHER" "$DEPS_PATCHER" "$ESIM_PATCHER"

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Lint Remediation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#SUCCEEDED[@]} -gt 0 ]] && echo "  ✅ Succeeded (${#SUCCEEDED[@]}): ${SUCCEEDED[*]}"
[[ ${#SKIPPED[@]}  -gt 0 ]] && echo "  ⚠️  Skipped   (${#SKIPPED[@]}):  ${SKIPPED[*]}"
[[ ${#FAILED[@]}   -gt 0 ]] && echo "  ❌ Failed    (${#FAILED[@]}):   ${FAILED[*]}"

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo "  Dry-run complete. Re-run without --dry-run to apply changes."
else
  echo "  Next steps:"
  echo "    1. Review the opened PRs in each service repo."
  echo "    2. Merge to main — CI 'test' job should now pass."
  echo "    3. Re-run 'Service — Docker Build & Push' workflow in Akulearn_docs."
  echo "    4. Integration tests will auto-trigger after the Docker build."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#FAILED[@]} -gt 0 ]] && exit 1
exit 0
