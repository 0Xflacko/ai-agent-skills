#!/usr/bin/env bash
set -euo pipefail

SOURCE="${HOME}/.codex/skills"
DEST_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: scripts/sync_skills.sh [--source <path>] [--dest <path>] [--dry-run]

Copies allowlisted skills from SOURCE into DEST/skills.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      SOURCE="${2:?missing value for --source}"
      shift 2
      ;;
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

if [[ ! -d "$SOURCE" ]]; then
  echo "Source directory not found: $SOURCE" >&2
  exit 1
fi
if [[ ! -f "$ALLOWLIST_FILE" ]]; then
  echo "Allowlist not found: $ALLOWLIST_FILE" >&2
  exit 1
fi

SKILLS=()
while IFS= read -r skill; do
  SKILLS+=("$skill")
done < <(grep -E '^[a-z0-9][a-z0-9-]*$' "$ALLOWLIST_FILE")
if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "Allowlist is empty: $ALLOWLIST_FILE" >&2
  exit 1
fi

EXCLUDED=(docx pdf pptx xlsx skill-seekers .system)
for banned in "${EXCLUDED[@]}"; do
  if printf '%s\n' "${SKILLS[@]}" | rg -qx "$banned"; then
    echo "Allowlist contains excluded skill: $banned" >&2
    exit 1
  fi
done

mkdir -p "$SKILLS_DEST_DIR"

echo "Syncing ${#SKILLS[@]} skills from $SOURCE to $SKILLS_DEST_DIR"

for skill in "${SKILLS[@]}"; do
  src="${SOURCE}/${skill}"
  dst="${SKILLS_DEST_DIR}/${skill}"

  if [[ ! -d "$src" ]]; then
    echo "Missing source skill directory: $src" >&2
    exit 1
  fi
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing required SKILL.md in source skill: $src" >&2
    exit 1
  fi

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
    "$src/" "$dst/"

  if [[ ! -f "$dst/SKILL.md" ]]; then
    echo "Sync failed, SKILL.md missing after copy: $dst" >&2
    exit 1
  fi

done

if [[ $DRY_RUN -eq 0 ]]; then
  CURRENT_DIRS=()
  while IFS= read -r dir_name; do
    CURRENT_DIRS+=("$dir_name")
  done < <(find "$SKILLS_DEST_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
  for existing in "${CURRENT_DIRS[@]}"; do
    if ! printf '%s\n' "${SKILLS[@]}" | rg -qx "$existing"; then
      rm -rf "${SKILLS_DEST_DIR}/${existing}"
      echo "Removed non-allowlisted skill from destination: $existing"
    fi
  done
  echo "Sync complete."
fi
