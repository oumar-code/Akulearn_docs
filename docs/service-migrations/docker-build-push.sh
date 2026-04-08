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

for svc in $SERVICES; do
  (
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Building $svc..."

    if [[ ! -d "$svc" ]] || [[ ! -d "$svc/.git" ]]; then
      echo "  ⚠  $svc — directory not found or not a git repo; skipping"
      echo "$svc: SKIPPED (not cloned)" >> "$SUMMARY_FILE"
      exit 0
    fi

    if [[ ! -f "$svc/Dockerfile" ]]; then
      echo "  ⚠  $svc/Dockerfile not found; skipping"
      echo "$svc: SKIPPED (no Dockerfile)" >> "$SUMMARY_FILE"
      exit 0
    fi

    # Strip the aku-platform-contracts git+ dep so the Docker builder stage
    # does not require git to be installed.  The package repo (oumar-code/
    # aku-platform-contracts) has not been published yet; no service code
    # currently imports it, so removing it here is safe for the integration
    # build.  Once the contracts repo is live, this patch can be removed and
    # the Dockerfiles updated to install git in the builder stage.
    if [[ -f "${svc}/requirements.txt" ]]; then
      sed -i '/aku-platform-contracts.*git+/d' "${svc}/requirements.txt"
      echo "  ℹ  Stripped aku-platform-contracts git dep from ${svc}/requirements.txt"
    fi

    IMAGE_NAME="$(to_lower "$svc")"
    IMAGE_BASE="${REGISTRY}/${IMAGE_NAME}"
    IMAGE_TAG="${IMAGE_BASE}:${TAG}"
    IMAGE_LATEST="${IMAGE_BASE}:latest"

    echo "  Image : ${IMAGE_TAG}"
    echo "  Also  : ${IMAGE_LATEST}"

    # Build — multi-platform linux/amd64 to match Kubernetes node pools.
    # We use --load (not --push) to produce a local image first so we can
    # inspect it before pushing.  Both tags are applied in one build pass.
    docker build \
      --file "${svc}/Dockerfile" \
      --tag  "${IMAGE_TAG}" \
      --tag  "${IMAGE_LATEST}" \
      --label "org.opencontainers.image.source=https://github.com/${GHCR_USER}/${svc}" \
      --label "org.opencontainers.image.revision=${TAG}" \
      --label "org.opencontainers.image.created=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      "${svc}"

    echo "  ✓ Build succeeded — pushing ${IMAGE_TAG}"
    docker push "${IMAGE_TAG}"
    docker push "${IMAGE_LATEST}"
    echo "  ✓ Pushed ${IMAGE_TAG} and ${IMAGE_LATEST}"

    echo "$svc: PUSHED ${IMAGE_TAG}" >> "$SUMMARY_FILE"
  ) || echo "$svc: FAILED" >> "$SUMMARY_FILE"

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
