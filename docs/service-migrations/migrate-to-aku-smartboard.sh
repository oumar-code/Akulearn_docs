#!/usr/bin/env bash
# migrate-to-aku-smartboard.sh — Copy akulearn-linux-app/ to oumar-code/Aku-SmartBoard
#
# Usage (run from the Akulearn_docs repo root — must have local akulearn-linux-app/ present):
#   chmod +x docs/service-migrations/migrate-to-aku-smartboard.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh --dry-run
#
#   # Live run — clones Aku-SmartBoard, copies app source, applies CI workflow, opens PR
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - akulearn-linux-app/ present locally (gitignored in Akulearn_docs)
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Aku-SmartBoard"
BRANCH_NAME="feat/initial-kmp-app-migration"
COMMIT_MSG="feat: migrate KMP Compose Desktop app from Akulearn_docs"
PR_TITLE="feat: migrate KMP Compose Desktop app from Akulearn_docs monorepo"
PR_BODY="Automated migration of \`akulearn-linux-app/\` (Kotlin Multiplatform / Compose Desktop) from the Akulearn_docs monorepo.

## What's included
- Full KMP linuxX64 application source (Kotlin 1.9.10, Compose 1.5.0)
  - \`src/linuxMain/kotlin/Main.kt\` — Facilitator Dashboard entry point
  - \`src/client_app/Main.kt\` — Full classroom client (syncs from hub.local:8000)
- \`build.gradle.kts\` — Gradle build file
- \`DEPLOYMENT.md\` — JDK17+, systemd service setup
- \`.github/workflows/release.yml\` — builds \`./gradlew build\` → attaches \`.kexe\` binary + systemd unit as GitHub Release assets

## Next steps
1. Verify \`./gradlew build\` succeeds (requires JDK 17+)
2. Create first GitHub Release tag (e.g. \`v0.1.0\`) — CI will attach the \`.kexe\` binary automatically
3. Merge this PR, then remove \`akulearn-linux-app/\` from Akulearn_docs
4. Update docs/ecosystem-map.md migration checklist accordingly

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CI_SCAFFOLD="${SCRIPT_DIR}/scaffolds/Aku-SmartBoard"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🔍 DRY-RUN mode — no changes will be made"
fi

run() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# ── Validate prerequisites ────────────────────────────────────────────────────

echo "✅ Checking prerequisites..."
command -v gh  >/dev/null || { echo "❌ gh CLI not found. Install: https://cli.github.com"; exit 1; }
command -v git >/dev/null || { echo "❌ git not found"; exit 1; }

MONOREPO_ROOT="$(git rev-parse --show-toplevel)"
APP_SRC="${MONOREPO_ROOT}/akulearn-linux-app"

[[ -d "$APP_SRC" ]] || { echo "❌ akulearn-linux-app/ not found at ${APP_SRC}. Ensure it is present locally."; exit 1; }

echo "✅ Source directory confirmed: ${APP_SRC}"

# ── Clone target repo ─────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
TARGET_CLONE="${WORK_DIR}/${TARGET_REPO}"
echo ""
echo "📁 Cloning ${GITHUB_ORG}/${TARGET_REPO} into ${TARGET_CLONE}..."
run gh repo clone "${GITHUB_ORG}/${TARGET_REPO}" "${TARGET_CLONE}"

cd "${TARGET_CLONE}"
run git checkout -b "${BRANCH_NAME}"

# ── Copy app source to repo root ─────────────────────────────────────────────

echo ""
echo "📂 Copying akulearn-linux-app/ contents to repo root..."
if $DRY_RUN; then
  echo "[dry-run] cp -r ${APP_SRC}/. ${TARGET_CLONE}/"
else
  # Copy contents of the app directory to repo root (not a subdirectory)
  cp -r "${APP_SRC}/." "${TARGET_CLONE}/"
  echo "   Copied $(find "${APP_SRC}" -type f | wc -l) files"
fi

# ── Apply CI/release workflow scaffold ───────────────────────────────────────

echo ""
echo "📂 Applying GitHub Actions CI/release workflow..."
run mkdir -p "${TARGET_CLONE}/.github/workflows"

if [[ -d "$CI_SCAFFOLD" ]]; then
  run cp -r "${CI_SCAFFOLD}/." "${TARGET_CLONE}/"
  echo "   Applied scaffold from ${CI_SCAFFOLD}"
else
  echo "⚠️  Scaffold directory not found at ${CI_SCAFFOLD} — writing inline workflow"
  if ! $DRY_RUN; then
    mkdir -p "${TARGET_CLONE}/.github/workflows"
    cat > "${TARGET_CLONE}/.github/workflows/release.yml" << 'WORKFLOW_EOF'
name: Build & Release

on:
  push:
    tags:
      - 'v*.*.*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Cache Gradle packages
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: ${{ runner.os }}-gradle-

      - name: Build linuxX64 binary
        run: ./gradlew build

      - name: Find .kexe binary
        id: find_binary
        run: |
          BINARY=$(find build -name "*.kexe" | head -1)
          echo "binary=${BINARY}" >> "$GITHUB_OUTPUT"
          echo "Found binary: ${BINARY}"

      - name: Create GitHub Release
        if: startsWith(github.ref, 'refs/tags/')
        uses: softprops/action-gh-release@v2
        with:
          files: |
            ${{ steps.find_binary.outputs.binary }}
            systemd/akulearn-smartboard.service
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
WORKFLOW_EOF
    echo "   Written: .github/workflows/release.yml"
  fi
fi

# ── Create .gitignore if absent ───────────────────────────────────────────────

if [[ ! -f "${TARGET_CLONE}/.gitignore" ]] && ! $DRY_RUN; then
  cat > "${TARGET_CLONE}/.gitignore" << 'EOF'
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
*.kexe

# IDE
.idea/
*.iml
.DS_Store
EOF
  echo "   Written: .gitignore"
fi

# ── Commit and push ───────────────────────────────────────────────────────────

echo ""
echo "📤 Committing and pushing..."
run git add .
run git commit -m "${COMMIT_MSG}"
run git push -u origin "${BRANCH_NAME}"

# ── Open PR ───────────────────────────────────────────────────────────────────

echo ""
echo "🔀 Opening pull request..."
run gh pr create \
  --repo "${GITHUB_ORG}/${TARGET_REPO}" \
  --base main \
  --head "${BRANCH_NAME}" \
  --title "${PR_TITLE}" \
  --body "${PR_BODY}"

echo ""
echo "✅ Migration script complete!"
echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
echo "   2. Verify ./gradlew build succeeds in CI"
echo "   3. Create tag v0.1.0 → CI will publish the .kexe binary as a Release artifact"
echo "   4. Merge the PR, then remove akulearn-linux-app/ from Akulearn_docs"
echo "   5. Update docs/ecosystem-map.md migration checklist"
