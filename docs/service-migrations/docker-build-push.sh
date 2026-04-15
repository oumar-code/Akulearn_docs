#!/usr/bin/env bash
# docker-build-push.sh — Build and push Docker images for all Aku Platform services
#                        to the GitHub Container Registry (GHCR).
#
# Usage (run from the directory that CONTAINS all service repos as immediate
#        subdirectories — the same workspace layout as lint-format-tag.sh):
#
#   # Build and push all services at tag v0.1.1:
#   SERVICES_OVERRIDE="AkuAI Akudemy" TAG_OVERRIDE="v0.1.1" \
#     GHCR_USER="oumar-code" ./docker-build-push.sh
#
# Environment variables:
#   SERVICES_OVERRIDE  — space-separated list of repos to process (default: all 9)
#   TAG_OVERRIDE       — image tag to apply            (default: v0.1.1)
#   GHCR_USER          — GitHub username / org that owns the GHCR namespace
#                        (default: oumar-code)
#   GHCR_TOKEN         — GitHub PAT with packages:write scope (required for push)
#                        When running under GitHub Actions, set via $GH_PAT.
#
# Prerequisites:
#   - docker (with BuildKit support) installed and running
#   - GHCR_TOKEN exported (or passed via env)
#   - Each service directory must already be a git clone at the target tag

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

SERVICES="${SERVICES_OVERRIDE:-AkuAI AkuTutor AkuWorkspace Akudemy Aku-EdgeHub Aku-IGHub Aku-Telhone Aku-SuperHub Aku-DaaS}"
TAG="${TAG_OVERRIDE:-v0.1.1}"
GHCR_USER="${GHCR_USER:-oumar-code}"
REGISTRY="ghcr.io/${GHCR_USER}"

SUMMARY_FILE="$(mktemp)"
FAIL_COUNT=0

# ── Pre-flight: log in to GHCR ────────────────────────────────────────────────

if [[ -n "${GHCR_TOKEN:-}" ]]; then
  echo "Logging in to ${REGISTRY}..."
  echo "${GHCR_TOKEN}" | docker login ghcr.io --username "${GHCR_USER}" --password-stdin
else
  echo "⚠  GHCR_TOKEN not set — assuming docker is already authenticated to ghcr.io"
fi

echo ""

# ── Helper: lowercase ─────────────────────────────────────────────────────────
# GHCR requires image names to be lowercase.  Bash 4+ has ${var,,}; this helper
# works on Bash 3 as well (macOS ships Bash 3).
to_lower() { echo "$1" | tr '[:upper:]' '[:lower:]'; }

# ── Per-service build ─────────────────────────────────────────────────────────
# NOTE: Do NOT wrap service iterations in a subshell followed by `|| handler`
# (i.e., avoid the `( ... ) || catch` pattern).  Bash disables `set -e` for
# every command inside a subshell that is the left-hand side of `||`, so build
# or push failures are silently ignored and the summary falsely reports PUSHED.

for svc in $SERVICES; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Building $svc..."

  if [[ ! -d "$svc" ]]; then
    echo "  ⚠  $svc — directory not found; skipping"
    echo "$svc: SKIPPED (not cloned)" >> "$SUMMARY_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  if [[ ! -f "$svc/Dockerfile" ]]; then
    echo "  ⚠  $svc/Dockerfile not found; skipping"
    echo "$svc: SKIPPED (no Dockerfile)" >> "$SUMMARY_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  # Ensure git is available in the Dockerfile builder stage so that pip can
  # install git+ URL dependencies (e.g. aku-platform-contracts).  The standard
  # python:3.11-slim image does not include git; we patch any apt-get install
  # --no-install-recommends line in the Dockerfile to add it.  The grep check
  # makes the substitution idempotent: once git is already listed the sed is
  # skipped on subsequent runs.
  if ! grep -q 'apt-get install.*\bgit\b' "${svc}/Dockerfile" 2>/dev/null; then
    if grep -q 'apt-get install.*--no-install-recommends' "${svc}/Dockerfile" 2>/dev/null; then
      sed -i 's/\(apt-get install -y --no-install-recommends\)/\1 git/' \
        "${svc}/Dockerfile"
      echo "  ℹ  Patched ${svc}/Dockerfile: added git to builder apt-get install"
    else
      echo "  ⚠  ${svc}/Dockerfile has no apt-get install --no-install-recommends line — git may be unavailable"
    fi
  fi

  IMAGE_NAME="$(to_lower "$svc")"
  IMAGE_BASE="${REGISTRY}/${IMAGE_NAME}"
  IMAGE_TAG="${IMAGE_BASE}:${TAG}"
  IMAGE_LATEST="${IMAGE_BASE}:latest"

  echo "  Image : ${IMAGE_TAG}"
  echo "  Also  : ${IMAGE_LATEST}"

  # Build — both version tag and :latest applied in one pass.
  if ! docker build \
      --file "${svc}/Dockerfile" \
      --tag  "${IMAGE_TAG}" \
      --tag  "${IMAGE_LATEST}" \
      --label "org.opencontainers.image.source=https://github.com/${GHCR_USER}/${svc}" \
      --label "org.opencontainers.image.revision=${TAG}" \
      --label "org.opencontainers.image.created=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      "${svc}"; then
    echo "  ✗ Build FAILED for ${svc}"
    echo "$svc: FAILED (build error)" >> "$SUMMARY_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  echo "  ✓ Build succeeded — pushing ${IMAGE_TAG}"

  if ! docker push "${IMAGE_TAG}"; then
    echo "  ✗ Push FAILED for ${IMAGE_TAG}"
    echo "$svc: FAILED (push error)" >> "$SUMMARY_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  if ! docker push "${IMAGE_LATEST}"; then
    echo "  ✗ Push FAILED for ${IMAGE_LATEST}"
    echo "$svc: FAILED (push :latest error)" >> "$SUMMARY_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  echo "  ✓ Pushed ${IMAGE_TAG} and ${IMAGE_LATEST}"
  echo "$svc: PUSHED ${IMAGE_TAG}" >> "$SUMMARY_FILE"
  echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Docker build/push complete."
echo ""
echo "Summary:"
if [[ -f "$SUMMARY_FILE" ]]; then
  cat "$SUMMARY_FILE"
  rm -f "$SUMMARY_FILE"
else
  echo "(no services processed)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Exit non-zero if any service failed so CI marks the job as failed.
exit $FAIL_COUNT
