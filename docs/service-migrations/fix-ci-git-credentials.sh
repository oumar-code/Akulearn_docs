#!/usr/bin/env bash
# fix-ci-git-credentials.sh — Patch .github/workflows/ci.yml in all 9 Aku Platform
#                              service repos to configure git credentials before pip
#                              installs so that private VCS dependencies
#                              (aku-platform-contracts) can be fetched.
#
# The patch inserts the following step immediately before "Install dependencies":
#
#   - name: Configure git credentials for private packages
#     run: git config --global url."https://${{ secrets.GH_PAT }}@github.com/".insteadOf "https://github.com/"
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/fix-ci-git-credentials.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/fix-ci-git-credentials.sh --all --dry-run
#
#   # Apply to all 9 services
#   ./docs/service-migrations/fix-ci-git-credentials.sh --all
#
#   # Apply to a single service
#   ./docs/service-migrations/fix-ci-git-credentials.sh AkuAI
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - python3 installed (used for safe multi-line YAML patching)
#   - bash 4+

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

GITHUB_ORG="oumar-code"
BRANCH_NAME="fix/ci-git-credentials-for-pip"
COMMIT_MSG="fix: configure git credentials before pip install in CI"

PR_TITLE="fix: configure git credentials before pip install in CI"
PR_BODY='## Problem

`pip install -r requirements.txt` fails in CI because the
`aku-platform-contracts` dependency is a private VCS reference:

```
aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts.git@v0.1.1
```

pip delegates the clone to git, which has no credentials configured in the
runner environment, causing:

```
fatal: could not read Username for '"'"'https://github.com'"'"': No such device or address
```

## Fix

Add a step **before** `pip install` that rewrites the GitHub HTTPS remote URL
to include the `GH_PAT` secret:

```yaml
- name: Configure git credentials for private packages
  run: git config --global url."https://${{ secrets.GH_PAT }}@github.com/".insteadOf "https://github.com/"
```

This makes git (and therefore pip) authenticate automatically when cloning the
contracts package from `github.com/oumar-code/aku-platform-contracts`.

## References

- Strategy doc: `docs/service-templates/python-fastapi-bootstrap.md` Step 9
- Automation: `docs/service-migrations/fix-ci-git-credentials.sh`
'

# All 9 backend service repos in priority order
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
  echo "Usage: $0 --all [--dry-run]  |  $0 <ServiceName> [--dry-run]" >&2
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      SERVICES=("${ALL_SERVICES[@]}")
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -*)
      echo "Error: unknown flag '$1'" >&2
      exit 1
      ;;
    *)
      SERVICES+=("$1")
      shift
      ;;
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

# Patch the ci.yml file in-place using Python for safe multi-line YAML editing.
# Inserts the git-credentials step right before the "Install dependencies" step.
patch_ci_yml() {
  local ci_file="$1"

  python3 - "$ci_file" <<'PYEOF'
import sys, re

path = sys.argv[1]
content = open(path).read()

MARKER = "      - name: Install dependencies"
INSERT = (
    "      - name: Configure git credentials for private packages\n"
    "        run: git config --global "
    'url."https://${{ secrets.GH_PAT }}@github.com/".insteadOf "https://github.com/"\n'
    "\n"
)

if INSERT.strip() in content:
    print("  ℹ  Step already present — nothing to do")
    sys.exit(0)

if MARKER not in content:
    print(f"  ✗  Marker '{MARKER}' not found in {path}")
    sys.exit(1)

patched = content.replace(MARKER, INSERT + MARKER, 1)
open(path, "w").write(patched)
print("  ✓  Patched ci.yml")
PYEOF
}

# ── Pre-flight checks ──────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Aku Platform — Fix CI git credentials"
if [[ "$DRY_RUN" == true ]]; then
  echo "  MODE: DRY RUN (no changes will be made)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for cmd in gh git python3; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: '$cmd' is not installed." >&2
    exit 1
  fi
done

if [[ "$DRY_RUN" == false ]]; then
  if ! gh auth status &>/dev/null; then
    echo "Error: gh CLI is not authenticated. Run: gh auth login" >&2
    exit 1
  fi
fi

echo "Services : ${SERVICES[*]}"
echo "Branch   : ${BRANCH_NAME}"
echo ""

# ── Per-service function ───────────────────────────────────────────────────────

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

  # 1. Clone (shallow, main branch only)
  echo "│  Step 1: Clone"
  if [[ "$DRY_RUN" == false ]]; then
    if ! git clone --depth 1 "${repo_url}" "${work_dir}" 2>&1 | sed 's/^/│  /'; then
      echo "│  ✗ Clone failed — skipping (repo may not exist yet)"
      echo "└──────────────────────────────────────────────────────"
      SKIPPED+=("${service}")
      return
    fi
  else
    echo "  [dry-run] git clone --depth 1 ${repo_url} ${work_dir}"
  fi

  # 2. Locate ci.yml
  local ci_file="${work_dir}/.github/workflows/ci.yml"
  if [[ "$DRY_RUN" == false ]]; then
    if [[ ! -f "${ci_file}" ]]; then
      echo "│  ✗ .github/workflows/ci.yml not found — Python/FastAPI migration not merged yet, skipping"
      echo "└──────────────────────────────────────────────────────"
      SKIPPED+=("${service}")
      rm -rf "${work_dir}"
      return
    fi
  fi

  # 3. Check if branch already exists remotely
  if [[ "$DRY_RUN" == false ]]; then
    if git -C "${work_dir}" ls-remote --exit-code --heads origin "${BRANCH_NAME}" &>/dev/null; then
      echo "│  ℹ  Branch ${BRANCH_NAME} already exists on origin — skipping"
      echo "└──────────────────────────────────────────────────────"
      SKIPPED+=("${service}")
      rm -rf "${work_dir}"
      return
    fi
  fi

  # 4. Apply the patch
  echo "│  Step 2: Patch .github/workflows/ci.yml"
  if [[ "$DRY_RUN" == false ]]; then
    if ! patch_output=$(patch_ci_yml "${ci_file}" 2>&1); then
      echo "│  ✗ Patch failed:"
      echo "${patch_output}" | sed 's/^/│    /'
      echo "└──────────────────────────────────────────────────────"
      FAILED+=("${service}")
      rm -rf "${work_dir}"
      return
    fi
    echo "${patch_output}" | sed 's/^/│  /'

    # If already present, skip
    if echo "${patch_output}" | grep -q "already present"; then
      echo "└──────────────────────────────────────────────────────"
      SKIPPED+=("${service}")
      rm -rf "${work_dir}"
      return
    fi
  else
    echo "  [dry-run] Insert 'Configure git credentials' step before 'Install dependencies' in ${ci_file}"
  fi

  # 5. Create branch, commit, push
  echo "│  Step 3: Commit and push"
  if [[ "$DRY_RUN" == false ]]; then
    pushd "${work_dir}" > /dev/null
    git checkout -b "${BRANCH_NAME}"
    git add .github/workflows/ci.yml
    git commit -m "${COMMIT_MSG}"
    git push origin "${BRANCH_NAME}"
    popd > /dev/null
  else
    echo "  [dry-run] git checkout -b ${BRANCH_NAME}"
    echo "  [dry-run] git add .github/workflows/ci.yml && git commit -m '${COMMIT_MSG}'"
    echo "  [dry-run] git push origin ${BRANCH_NAME}"
  fi

  # 6. Open pull request
  echo "│  Step 4: Open pull request"
  if [[ "$DRY_RUN" == false ]]; then
    gh pr create \
      --repo "${GITHUB_ORG}/${service}" \
      --base main \
      --head "${BRANCH_NAME}" \
      --title "${PR_TITLE}" \
      --body "${PR_BODY}" \
      2>&1 | sed 's/^/│  /' \
      || echo "│  ⚠  PR already exists or could not be created"
  else
    echo "  [dry-run] gh pr create --repo ${GITHUB_ORG}/${service} --title '${PR_TITLE}'"
  fi

  # 7. Clean up
  if [[ "$DRY_RUN" == false ]]; then
    rm -rf "${work_dir}"
  fi

  echo "│  ✓ Done"
  echo "└──────────────────────────────────────────────────────"
  SUCCEEDED+=("${service}")
}

# ── Run ────────────────────────────────────────────────────────────────────────

for svc in "${SERVICES[@]}"; do
  fix_service "$svc" || FAILED+=("$svc")
  echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Fix CI git credentials — Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#SUCCEEDED[@]} -gt 0 ]] && echo "  ✅ Succeeded (${#SUCCEEDED[@]}): ${SUCCEEDED[*]}"
[[ ${#SKIPPED[@]}  -gt 0 ]] && echo "  ⚠️  Skipped   (${#SKIPPED[@]}):  ${SKIPPED[*]}"
[[ ${#FAILED[@]}   -gt 0 ]] && echo "  ❌ Failed    (${#FAILED[@]}):   ${FAILED[*]}"

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo "  Dry-run complete. Re-run without --dry-run to apply."
else
  echo "  Next: review and merge the opened PRs in each service repo."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#FAILED[@]} -gt 0 ]] && exit 1
exit 0
