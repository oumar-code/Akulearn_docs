#!/usr/bin/env bash
# integrate-contracts.sh — Add aku-platform-contracts dependency to all 9 Aku Platform services
#                          and tag each repo at v0.1.1
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/integrate-contracts.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/integrate-contracts.sh --all --dry-run
#
#   # Apply to all 9 services
#   ./docs/service-migrations/integrate-contracts.sh --all
#
#   # Apply to a single service
#   ./docs/service-migrations/integrate-contracts.sh AkuAI
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - bash 4+
#   - oumar-code/aku-platform-contracts exists and has a v0.1.0 tag
#
# What this script does for each service repo:
#   1. Clones the repo (shallow)
#   2. Adds aku-platform-contracts as a pip dependency in requirements.txt
#   3. Commits on a new branch
#   4. Pushes the branch and opens a PR
#   5. Tags the repo HEAD (main) as v0.1.1

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

GITHUB_ORG="oumar-code"
CONTRACTS_REPO="aku-platform-contracts"
CONTRACTS_REF="v0.1.0"
CONTRACTS_DEP="aku-platform-contracts @ git+https://github.com/${GITHUB_ORG}/${CONTRACTS_REPO}.git@${CONTRACTS_REF}"

BRANCH_NAME="feat/add-platform-contracts"
COMMIT_MSG="feat: add aku-platform-contracts shared dependency"
TAG_VERSION="v0.1.1"
TAG_MSG="Release ${TAG_VERSION} — adds shared aku-platform-contracts dependency"

PR_TITLE="feat: add aku-platform-contracts shared dependency"
PR_BODY="## Summary

Adds the shared \`aku-platform-contracts\` package as a dependency so that
all Aku Platform services consume the same Pydantic schemas, OpenAPI models,
and Kafka topic constants from one source of truth.

## Changes
- \`requirements.txt\`: added \`${CONTRACTS_DEP}\`

## References
- Contracts repo: https://github.com/${GITHUB_ORG}/${CONTRACTS_REPO}
- Ecosystem map: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
- Contracts proposal: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/aku-platform-contracts.md
"

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
  echo "Usage: $0 --all [--dry-run]  |  $0 <ServiceName>" >&2
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

# ── Pre-flight checks ──────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Aku Platform — Contracts Integration"
if [[ "$DRY_RUN" == true ]]; then
  echo "  MODE: DRY RUN (no changes will be made)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if ! command -v gh &>/dev/null; then
  echo "Error: gh CLI is not installed. Install from https://cli.github.com" >&2
  exit 1
fi

if ! command -v git &>/dev/null; then
  echo "Error: git is not installed." >&2
  exit 1
fi

if [[ "$DRY_RUN" == false ]]; then
  if ! gh auth status &>/dev/null; then
    echo "Error: gh CLI is not authenticated. Run: gh auth login" >&2
    exit 1
  fi
fi

echo "Services: ${SERVICES[*]}"
echo "Contracts dep: ${CONTRACTS_DEP}"
echo "Tag: ${TAG_VERSION}"
echo ""

# ── Per-service function ───────────────────────────────────────────────────────

SUCCEEDED=()
FAILED=()
SKIPPED=()

integrate_service() {
  local service="$1"
  local repo_url="https://github.com/${GITHUB_ORG}/${service}.git"
  local work_dir
  work_dir="$(mktemp -d)"

  echo "┌─ ${service} ─────────────────────────────────────────"
  echo "│  Repo: ${GITHUB_ORG}/${service}"
  echo "│"

  # 1. Clone (shallow, main branch only)
  echo "│  Step 1: Clone"
  if ! run git clone --depth 1 "${repo_url}" "${work_dir}"; then
    echo "│  ✗ Clone failed — skipping"
    echo "└──────────────────────────────────────────────────────"
    SKIPPED+=("${service}")
    return
  fi

  # 2. Check requirements.txt exists
  if [[ "$DRY_RUN" == false ]]; then
    if [[ ! -f "${work_dir}/requirements.txt" ]]; then
      echo "│  ✗ requirements.txt not found — is the Python/FastAPI migration merged? Skipping."
      echo "└──────────────────────────────────────────────────────"
      SKIPPED+=("${service}")
      rm -rf "${work_dir}"
      return
    fi

    # 3. Idempotency — skip if dep already present
    if grep -qF "${CONTRACTS_REPO}" "${work_dir}/requirements.txt"; then
      echo "│  ℹ  aku-platform-contracts already in requirements.txt — skipping dep update"
    else
      echo "│  Step 2: Add contracts dependency to requirements.txt"
      # Append after the last non-empty line
      printf '\n# Shared Aku Platform contracts (Pydantic schemas + Kafka topics)\n%s\n' \
        "${CONTRACTS_DEP}" >> "${work_dir}/requirements.txt"
    fi
  else
    echo "  [dry-run] check/append '${CONTRACTS_DEP}' to ${work_dir}/requirements.txt"
  fi

  # 4. Create branch, commit, push
  echo "│  Step 3: Create branch and commit"
  if [[ "$DRY_RUN" == false ]]; then
    pushd "${work_dir}" > /dev/null

    # Bail out cleanly if branch already exists remotely
    if git ls-remote --exit-code --heads origin "${BRANCH_NAME}" &>/dev/null; then
      echo "│  ℹ  Branch ${BRANCH_NAME} already exists on origin — skipping commit/push"
    else
      git checkout -b "${BRANCH_NAME}"
      git add requirements.txt
      git commit -m "${COMMIT_MSG}" || { echo "│  ℹ  Nothing to commit"; git checkout main; }

      echo "│  Step 4: Push branch"
      git push origin "${BRANCH_NAME}"

      echo "│  Step 5: Open pull request"
      gh pr create \
        --repo "${GITHUB_ORG}/${service}" \
        --base main \
        --head "${BRANCH_NAME}" \
        --title "${PR_TITLE}" \
        --body "${PR_BODY}" || echo "│  ⚠  PR already exists or could not be created"
    fi

    popd > /dev/null
  else
    echo "  [dry-run] git checkout -b ${BRANCH_NAME}"
    echo "  [dry-run] git add requirements.txt && git commit -m '${COMMIT_MSG}'"
    echo "  [dry-run] git push origin ${BRANCH_NAME}"
    echo "  [dry-run] gh pr create --repo ${GITHUB_ORG}/${service} --title '${PR_TITLE}'"
  fi

  # 6. Tag the main branch HEAD as v0.1.1
  echo "│  Step 6: Tag ${TAG_VERSION} on main"
  if [[ "$DRY_RUN" == false ]]; then
    pushd "${work_dir}" > /dev/null
    git checkout main 2>/dev/null || true

    if git ls-remote --exit-code --tags origin "${TAG_VERSION}" &>/dev/null; then
      echo "│  ℹ  Tag ${TAG_VERSION} already exists on origin — skipping"
    else
      git tag -a "${TAG_VERSION}" -m "${TAG_MSG}"
      git push origin "${TAG_VERSION}"
    fi

    popd > /dev/null
  else
    echo "  [dry-run] git tag -a ${TAG_VERSION} -m '${TAG_MSG}' && git push origin ${TAG_VERSION}"
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
  integrate_service "$svc" || FAILED+=("$svc")
  echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Contracts Integration Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#SUCCEEDED[@]} -gt 0 ]] && echo "  ✅ Succeeded (${#SUCCEEDED[@]}): ${SUCCEEDED[*]}"
[[ ${#SKIPPED[@]}  -gt 0 ]] && echo "  ⚠️  Skipped   (${#SKIPPED[@]}):  ${SKIPPED[*]}"
[[ ${#FAILED[@]}   -gt 0 ]] && echo "  ❌ Failed    (${#FAILED[@]}):   ${FAILED[*]}"

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo "  Dry-run complete. Re-run without --dry-run to apply."
else
  echo "  Next: merge the opened PRs in each service repo, then update"
  echo "  automation_progress.md Contracts Repo Status to ✅ Done."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ ${#FAILED[@]} -gt 0 ]] && exit 1
exit 0
