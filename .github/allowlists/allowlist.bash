#!/usr/bin/env bash
set -euo pipefail

ALLOWLIST_FILE_DEFAULT="${GITHUB_WORKSPACE:-$(pwd)}/.github/allowlists/repos.env"
ALLOWLIST_FILE="${ALLOWLIST_FILE:-$ALLOWLIST_FILE_DEFAULT}"

if [[ ! -f "$ALLOWLIST_FILE" ]]; then
  echo "Allowlist file not found: $ALLOWLIST_FILE" >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$ALLOWLIST_FILE"

normalize_space_list() {
  echo "$*" | tr '\n\t' '  ' | xargs
}

repo_in_list() {
  local repo="$1"
  local allowed="$2"
  for item in $allowed; do
    if [[ "$item" == "$repo" ]]; then
      return 0
    fi
  done
  return 1
}

resolve_allowed_repos() {
  local requested_raw="${1:-}"
  local allowed_raw="${2:-}"
  local lane="${3:-allowlist}"

  local requested allowed resolved
  requested="$(normalize_space_list "$requested_raw")"
  allowed="$(normalize_space_list "$allowed_raw")"

  if [[ -z "$allowed" ]]; then
    echo "[$lane] allowed list is empty" >&2
    return 1
  fi

  if [[ -z "$requested" ]]; then
    echo "$allowed"
    return 0
  fi

  resolved=""
  for repo in $requested; do
    if ! repo_in_list "$repo" "$allowed"; then
      echo "[$lane] repo '$repo' is out of scope. Allowed: $allowed" >&2
      return 1
    fi
    resolved+=" $repo"
  done

  normalize_space_list "$resolved"
}
