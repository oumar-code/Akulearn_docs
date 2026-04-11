#!/usr/bin/env bash
# migrate-to-aku-smartboard.sh — Copy akulearn-linux-app/ to oumar-code/Aku-SmartBoard
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/migrate-to-aku-smartboard.sh
#
#   # Show this help
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh --help
#
#   # Scaffold-only — push CI/release workflow + systemd unit to Aku-SmartBoard (no local app source needed)
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only
#
#   # Scaffold-only dry-run
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only --dry-run
#
#   # Full migration — clones Aku-SmartBoard, copies app source, applies CI workflow, opens PR
#   # ⚠️  MUST RUN FROM LOCAL MACHINE — requires akulearn-linux-app/ present locally (gitignored)
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh
#
#   # Full migration dry-run
#   ./docs/service-migrations/migrate-to-aku-smartboard.sh --dry-run
#
# Prerequisites (full migration):
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - akulearn-linux-app/ present locally (gitignored in Akulearn_docs)
#
# Prerequisites (--scaffold-only, can run in CI):
#   - gh CLI installed and authenticated — or GH_TOKEN/GH_PAT env var set
#   - git installed
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Aku-SmartBoard"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CI_SCAFFOLD="${SCRIPT_DIR}/scaffolds/Aku-SmartBoard"

# ── Flag parsing ──────────────────────────────────────────────────────────────

DRY_RUN=false
SCAFFOLD_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --help|-h)
      cat << 'HELP'
migrate-to-aku-smartboard.sh — Migrate akulearn-linux-app/ to oumar-code/Aku-SmartBoard

MODES
  (no flags)          Full migration — copies Kotlin source + scaffold to Aku-SmartBoard.
                      ⚠️  MUST RUN FROM LOCAL MACHINE — requires akulearn-linux-app/ locally.

  --scaffold-only     Scaffold-only — pushes CI/release workflow + systemd unit to
                      Aku-SmartBoard WITHOUT needing akulearn-linux-app/ locally.
                      Can be run from any machine or GitHub Actions (set GH_PAT env var).

  --dry-run           Preview every step without making any changes (works with both modes).
  --help, -h          Show this help message.

USAGE EXAMPLES
  # Scaffold-only (no local source needed — can run in CI):
  ./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only

  # Scaffold-only dry-run:
  ./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only --dry-run

  # Full migration (run from local machine with akulearn-linux-app/ present):
  ./docs/service-migrations/migrate-to-aku-smartboard.sh

  # Full migration dry-run:
  ./docs/service-migrations/migrate-to-aku-smartboard.sh --dry-run

LOCAL MACHINE SETUP (full migration only)
  1. Ensure akulearn-linux-app/ is present in your local Akulearn_docs clone
     (it is gitignored — restore from your local drive or team storage)
  2. Install gh CLI:  https://cli.github.com
  3. Authenticate:    gh auth login
  4. Run:             ./docs/service-migrations/migrate-to-aku-smartboard.sh

MIGRATION TRACKER
  https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md
HELP
      exit 0
      ;;
    --scaffold-only) SCAFFOLD_ONLY=true ;;
    --dry-run)       DRY_RUN=true ;;
    *)
      echo "❌ Unknown flag: $arg  (use --help for usage)" >&2
      exit 1
      ;;
  esac
done

if $SCAFFOLD_ONLY; then
  BRANCH_NAME="feat/ci-workflow-scaffold"
  COMMIT_MSG="feat: add CI/release workflow and systemd unit scaffold"
  PR_TITLE="feat: add CI/release workflow and systemd service unit to Aku-SmartBoard"
  PR_BODY="Adds the GitHub Actions CI/release workflow and systemd service unit to Aku-SmartBoard.

## What's included
- \`.github/workflows/release.yml\` — builds \`./gradlew build\` on tag push → attaches \`.kexe\` binary + systemd unit to a GitHub Release
- \`systemd/akulearn-smartboard.service\` — ready-to-install systemd unit for the classroom client

## What's NOT included yet
The Kotlin application source (\`akulearn-linux-app/\`) has not been copied yet — it is gitignored
in the Akulearn_docs monorepo and must be pushed separately from a local machine.

Run \`./docs/service-migrations/migrate-to-aku-smartboard.sh\` (full migration, local machine) once
the source is restored locally to complete the migration.

## Next steps
1. Merge this PR to get CI/release pipeline in place
2. Run the full migration from a local machine to add the Kotlin source
3. Push a \`v0.1.0\` tag → CI will publish the \`.kexe\` binary as a Release artifact

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"
else
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
fi

if $DRY_RUN; then
  echo "🔍 DRY-RUN mode — no changes will be made"
fi
$SCAFFOLD_ONLY && echo "🔧 SCAFFOLD-ONLY mode — skipping Kotlin source copy"

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

if ! $SCAFFOLD_ONLY; then
  APP_SRC="${MONOREPO_ROOT}/akulearn-linux-app"
  if [[ ! -d "$APP_SRC" ]]; then
    cat >&2 << 'LOCAL_MACHINE_ERR'

❌ MUST RUN FROM LOCAL MACHINE
─────────────────────────────────────────────────────────────────────────────
akulearn-linux-app/ was not found at the expected location.

This directory is gitignored and exists only on a developer's local machine.
The full migration CANNOT run in a fresh git clone or CI environment.

TO RUN THE FULL MIGRATION:
  1. Restore akulearn-linux-app/ to your local Akulearn_docs clone
     (copy from your local drive or team file storage)
  2. Install and authenticate the gh CLI:
       gh auth login
  3. Run from the Akulearn_docs repo root:
       ./docs/service-migrations/migrate-to-aku-smartboard.sh

ALTERNATIVE — push just the CI/release scaffold (no local source needed):
  ./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only
  Or trigger the "Aku-SmartBoard — Apply CI/Release Scaffold" GitHub Actions
  workflow from the Akulearn_docs Actions tab (requires GH_PAT secret).
─────────────────────────────────────────────────────────────────────────────
LOCAL_MACHINE_ERR
    exit 1
  fi
  echo "✅ Source directory confirmed: ${APP_SRC}"
fi

# ── Clone target repo ─────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
TARGET_CLONE="${WORK_DIR}/${TARGET_REPO}"
echo ""
echo "📁 Cloning ${GITHUB_ORG}/${TARGET_REPO} into ${TARGET_CLONE}..."
run gh repo clone "${GITHUB_ORG}/${TARGET_REPO}" "${TARGET_CLONE}"

cd "${TARGET_CLONE}"
run git checkout -b "${BRANCH_NAME}"

# ── Copy app source to repo root ─────────────────────────────────────────────

if ! $SCAFFOLD_ONLY; then
  echo ""
  echo "📂 Copying akulearn-linux-app/ contents to repo root..."
  if $DRY_RUN; then
    echo "[dry-run] cp -r ${APP_SRC}/. ${TARGET_CLONE}/"
  else
    # Copy contents of the app directory to repo root (not a subdirectory)
    cp -r "${APP_SRC}/." "${TARGET_CLONE}/"
    echo "   Copied $(find "${APP_SRC}" -type f | wc -l) files"
  fi
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
if $SCAFFOLD_ONLY; then
  echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
  echo "   2. Merge this PR to get the CI/release pipeline in place"
  echo "   3. Run the full migration from a local machine (with akulearn-linux-app/ present)"
  echo "      to add the Kotlin source"
  echo "   4. Push tag v0.1.0 → CI will publish the .kexe binary as a Release artifact"
else
  echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
  echo "   2. Verify ./gradlew build succeeds in CI"
  echo "   3. Create tag v0.1.0 → CI will publish the .kexe binary as a Release artifact"
  echo "   4. Merge the PR, then remove akulearn-linux-app/ from Akulearn_docs"
  echo "   5. Update docs/ecosystem-map.md migration checklist"
fi
