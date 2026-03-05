#!/usr/bin/env bash
set -euo pipefail

DEST_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: scripts/sync_skills.sh [--dest <path>] [--dry-run]

Copies allowlisted skills from multiple local source directories into DEST/skills.

Sources (searched in order):
  1. ~/.codex/skills           (Codex skills)
  2. ~/.cursor/skills-cursor   (Cursor-authored skills)
  3. ~/.cursor/plugins/cache/cursor-public/*/  (Cursor plugin skills, latest version)
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      DEST_REPO="${2:?missing value for --dest}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
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

ALLOWLIST_FILE="${DEST_REPO}/config/include-skills.txt"
SKILLS_DEST_DIR="${DEST_REPO}/skills"

if [[ ! -f "$ALLOWLIST_FILE" ]]; then
  echo "Allowlist not found: $ALLOWLIST_FILE" >&2
  exit 1
fi

SOURCES=("${HOME}/.codex/skills" "${HOME}/.cursor/skills-cursor")

for plugin_dir in "${HOME}/.cursor/plugins/cache/cursor-public"/*/; do
  [[ -d "$plugin_dir" ]] || continue
  latest=$(ls -td "${plugin_dir}"*/skills 2>/dev/null | head -1)
  if [[ -n "$latest" && -d "$latest" ]]; then
    SOURCES+=("$latest")
  fi
done

echo "Source directories:"
for src in "${SOURCES[@]}"; do
  echo "  $src"
done

SKILLS=()
while IFS= read -r skill; do
  SKILLS+=("$skill")
done < <(grep -E '^[a-z0-9][a-z0-9-]*$' "$ALLOWLIST_FILE")
if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "Allowlist is empty: $ALLOWLIST_FILE" >&2
  exit 1
fi

EXCLUDED=(docx pdf pptx xlsx .system)
for banned in "${EXCLUDED[@]}"; do
  if printf '%s\n' "${SKILLS[@]}" | grep -qx "$banned"; then
    echo "Allowlist contains excluded skill: $banned" >&2
    exit 1
  fi
done

find_skill_source() {
  local skill="$1"
  for src_dir in "${SOURCES[@]}"; do
    if [[ -d "${src_dir}/${skill}" && -f "${src_dir}/${skill}/SKILL.md" ]]; then
      echo "${src_dir}/${skill}"
      return 0
    fi
  done
  return 1
}

MIT_LICENSE_TEXT='MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'

mkdir -p "$SKILLS_DEST_DIR"

echo ""
echo "Syncing ${#SKILLS[@]} skills to $SKILLS_DEST_DIR"

for skill in "${SKILLS[@]}"; do
  src=$(find_skill_source "$skill") || {
    echo "No source found for skill: $skill" >&2
    exit 1
  }
  dst="${SKILLS_DEST_DIR}/${skill}"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY-RUN] rsync $src -> $dst"
    continue
  fi

  rm -rf "$dst"
  mkdir -p "$dst"

  rsync -a \
    --exclude '.git/' \
    --exclude '.env' \
    --exclude '.env.*' \
    --exclude '.DS_Store' \
    --exclude '__pycache__/' \
    --exclude 'node_modules/' \
    "$src/" "$dst/"

  if [[ ! -f "$dst/SKILL.md" ]]; then
    echo "Sync failed, SKILL.md missing after copy: $dst" >&2
    exit 1
  fi

  if ! find "$dst" -maxdepth 1 -type f \( -name 'LICENSE' -o -name 'LICENSE.txt' -o -name 'license.txt' \) | grep -q .; then
    echo "$MIT_LICENSE_TEXT" > "$dst/LICENSE.txt"
    echo "  + Added default MIT LICENSE.txt to $skill"
  fi

  echo "  synced: $skill <- $src"
done

if [[ $DRY_RUN -eq 0 ]]; then
  CURRENT_DIRS=()
  while IFS= read -r dir_name; do
    CURRENT_DIRS+=("$dir_name")
  done < <(find "$SKILLS_DEST_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
  for existing in "${CURRENT_DIRS[@]}"; do
    if ! printf '%s\n' "${SKILLS[@]}" | grep -qx "$existing"; then
      rm -rf "${SKILLS_DEST_DIR}/${existing}"
      echo "  removed: $existing (not in allowlist)"
    fi
  done
  echo ""
  echo "Sync complete: ${#SKILLS[@]} skills."
fi
