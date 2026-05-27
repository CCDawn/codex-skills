#!/usr/bin/env bash
set -euo pipefail

# Development convenience only. The formal install flow for this repository is
# copying real directories into ~/.codex/skills via install_codex_library.py.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${HOME}/.claude/skills"

if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST resolves into this repo ($resolved)." >&2
      echo "Remove it and re-run so the script can create a real directory." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -print0 |
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  target="$DEST/$name"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    rm -rf "$target"
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
