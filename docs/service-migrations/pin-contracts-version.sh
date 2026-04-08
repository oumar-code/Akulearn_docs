#!/usr/bin/env bash
# pin-contracts-version.sh — Update aku-platform-contracts to an explicit pinned
#                            version in every Aku Platform service's requirements.txt.
#
# Background:
#   The lint-format-tag.sh script adds the contracts package as a floating git+ ref:
#     aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts@v0.1.0
#   This script replaces that ref with a pinned version tag so that:
#     a) pip install is reproducible (no silent upgrades on re-installs), and
#     b) deliberate version bumps are explicit commits in each service repo.
#
# Usage (run from the directory that CONTAINS all service repos):
#
#   # Pin all 9 services to v0.1.1:
#   PIN_VERSION="v0.1.1" ./pin-contracts-version.sh
#
#   # Pin a subset:
#   SERVICES_OVERRIDE="AkuAI Akudemy" PIN_VERSION="v0.1.1" ./pin-contracts-version.sh
#
# Environment variables:
#   SERVICES_OVERRIDE  — space-separated list of service repos (default: all 9)
#   PIN_VERSION        — version tag to pin to  (default: v0.1.1)
#   GITHUB_ORG         — GitHub org             (default: oumar-code)
#   DRY_RUN            — set to 'true' to preview without writing files (default: false)

set -euo pipefail

# ── Constants ──────────────────────────────────────────────────────────────────

SERVICES="${SERVICES_OVERRIDE:-AkuAI AkuTutor AkuWorkspace Akudemy Aku-EdgeHub Aku-IGHub Aku-Telhone Aku-SuperHub Aku-DaaS}"
PIN_VERSION="${PIN_VERSION:-v0.1.1}"
GITHUB_ORG="${GITHUB_ORG:-oumar-code}"
CONTRACTS_REPO="aku-platform-contracts"
DRY_RUN="${DRY_RUN:-false}"

# The exact new line to place in requirements.txt
NEW_DEP="aku-platform-contracts @ git+https://github.com/${GITHUB_ORG}/${CONTRACTS_REPO}.git@${PIN_VERSION}"

SUMMARY_FILE="$(mktemp)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Aku Platform — Pin Contracts Version"
echo "  Target version : ${PIN_VERSION}"
[[ "$DRY_RUN" == "true" ]] && echo "  MODE           : DRY RUN (no changes written)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Per-service update ─────────────────────────────────────────────────────────

for svc in $SERVICES; do
  (
    echo "Processing $svc..."
    reqfile="$svc/requirements.txt"

    if [[ ! -d "$svc/.git" ]]; then
      echo "  ⚠  $svc — not a git repo, skipping"
      echo "$svc: SKIPPED (not a git repo)" >> "$SUMMARY_FILE"
      exit 0
    fi

    if [[ ! -f "$reqfile" ]]; then
      echo "  ⚠  $svc/requirements.txt not found, skipping"
      echo "$svc: SKIPPED (no requirements.txt)" >> "$SUMMARY_FILE"
      exit 0
    fi

    # Check if the contracts package is referenced at all
    if ! grep -q "${CONTRACTS_REPO}" "$reqfile"; then
      echo "  ⚠  aku-platform-contracts not in $reqfile — run lint-format-tag.sh first"
      echo "$svc: SKIPPED (contracts not in requirements.txt)" >> "$SUMMARY_FILE"
      exit 0
    fi

    # Check if it's already pinned to the target version
    if grep -qF "${NEW_DEP}" "$reqfile"; then
      echo "  ℹ  Already pinned to ${PIN_VERSION}"
      echo "$svc: ALREADY PINNED (${PIN_VERSION})" >> "$SUMMARY_FILE"
      exit 0
    fi

    # Show what would change
    OLD_LINE=$(grep "${CONTRACTS_REPO}" "$reqfile" | head -1)
    echo "  Replacing: ${OLD_LINE}"
    echo "  With     : ${NEW_DEP}"

    if [[ "$DRY_RUN" == "true" ]]; then
      echo "  [dry-run] skipping file write"
      echo "$svc: WOULD PIN (${PIN_VERSION})" >> "$SUMMARY_FILE"
      exit 0
    fi

    # Perform in-place replacement — replace any existing aku-platform-contracts
    # reference (any version/ref) with the new pinned line.
    # We use a temp file to avoid platform differences with sed -i.
    TMPFILE="$(mktemp)"
    while IFS= read -r line; do
      if echo "$line" | grep -q "${CONTRACTS_REPO}"; then
        echo "${NEW_DEP}"
      else
        echo "$line"
      fi
    done < "$reqfile" > "$TMPFILE"
    mv "$TMPFILE" "$reqfile"

    # Verify the replacement worked
    if grep -qF "${NEW_DEP}" "$reqfile"; then
      echo "  ✓ Updated requirements.txt"
    else
      echo "  ❌ Replacement verification failed — check $reqfile manually"
      echo "$svc: FAILED (replacement verification)" >> "$SUMMARY_FILE"
      exit 1
    fi

    # Commit and push
    pushd "$svc" > /dev/null
    git add requirements.txt
    if git diff --cached --quiet; then
      echo "  ℹ  Nothing to commit (file unchanged)"
    else
      git commit -m "chore: pin aku-platform-contracts to ${PIN_VERSION}"
      git push
      echo "  ✓ Committed and pushed"
    fi
    popd > /dev/null

    echo "$svc: PINNED (${PIN_VERSION})" >> "$SUMMARY_FILE"
  ) || echo "$svc: FAILED" >> "$SUMMARY_FILE"

  echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Pin contracts version complete."
echo ""
echo "Summary:"
if [[ -f "$SUMMARY_FILE" ]]; then
  cat "$SUMMARY_FILE"
  rm -f "$SUMMARY_FILE"
else
  echo "(no services processed)"
fi
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
  echo "Dry-run complete. Re-run with DRY_RUN=false to apply."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
