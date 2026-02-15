#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'USAGE'
Usage: scripts/verify_release.sh [--repo-root <path>]

Validates release completeness and safety checks.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      REPO_ROOT="${2:?missing value for --repo-root}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

ALLOWLIST_FILE="${REPO_ROOT}/config/include-skills.txt"
SKILLS_DIR="${REPO_ROOT}/skills"
X_POST_FILE="${REPO_ROOT}/posts/x-launch.md"
KLANG_FILE="${SKILLS_DIR}/kling-docs/SKILL.md"

errors=0

fail() {
  echo "ERROR: $1" >&2
  errors=$((errors + 1))
}

if [[ ! -f "$ALLOWLIST_FILE" ]]; then
  fail "Missing allowlist: $ALLOWLIST_FILE"
fi
if [[ ! -d "$SKILLS_DIR" ]]; then
  fail "Missing skills directory: $SKILLS_DIR"
fi

ALLOWLIST=()
while IFS= read -r skill; do
  ALLOWLIST+=("$skill")
done < <(grep -E '^[a-z0-9][a-z0-9-]*$' "$ALLOWLIST_FILE")
expected_count=${#ALLOWLIST[@]}

actual_count=$(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
if [[ "$actual_count" != "$expected_count" ]]; then
  fail "Skill count mismatch: expected $expected_count, found $actual_count"
fi

for skill in "${ALLOWLIST[@]}"; do
  if [[ ! -d "$SKILLS_DIR/$skill" ]]; then
    fail "Missing allowlisted skill dir: skills/$skill"
    continue
  fi
  if [[ ! -f "$SKILLS_DIR/$skill/SKILL.md" ]]; then
    fail "Missing SKILL.md: skills/$skill/SKILL.md"
  fi
  if ! find "$SKILLS_DIR/$skill" -maxdepth 1 -type f \( -name 'LICENSE' -o -name 'LICENSE.txt' -o -name 'license.txt' \) | grep -q .; then
    fail "Missing license file in skills/$skill"
  fi
done

EXCLUDED=(docx pdf pptx xlsx skill-seekers .system)
for skill in "${EXCLUDED[@]}"; do
  if [[ -e "$SKILLS_DIR/$skill" ]]; then
    fail "Excluded skill present in release: skills/$skill"
  fi
done

if find "$SKILLS_DIR" -type d -name '.git' | grep -q .; then
  fail "Nested .git directories found under skills/"
fi

if find "$SKILLS_DIR" -type f \( -name '.env' -o -name '.env.*' \) | grep -q .; then
  fail ".env files found under skills/"
fi

SECRET_PATTERN='(gh[pousr]_[A-Za-z0-9]{20,}|sk-(live|test|proj)-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'
if rg -n -S "$SECRET_PATTERN" "$REPO_ROOT" -g '!**/.git/**' >/tmp/release_secret_scan.txt; then
  fail "Possible secret-like tokens detected (see /tmp/release_secret_scan.txt)"
fi

if [[ ! -f "$KLANG_FILE" ]]; then
  fail "Missing KLING skill file: $KLANG_FILE"
else
  if rg -n '/Users/denoweb3/.codex/skills' "$KLANG_FILE" >/tmp/release_kling_path_scan.txt; then
    fail "Absolute local path found in kling-docs/SKILL.md"
  fi
fi

if [[ ! -f "$X_POST_FILE" ]]; then
  fail "Missing X post file: $X_POST_FILE"
else
  x_chars=$(wc -m < "$X_POST_FILE" | tr -d ' ')
  if (( x_chars > 280 )); then
    fail "X post exceeds 280 chars (found: $x_chars)"
  fi
fi

if (( errors > 0 )); then
  echo "Verification failed with $errors error(s)." >&2
  exit 1
fi

echo "Verification passed."
