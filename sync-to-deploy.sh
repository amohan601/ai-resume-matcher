#!/usr/bin/env bash
set -euo pipefail

SRC="/Users/amohan/personal/anj/personal-projects/agent-projects/resume-matcher"
DEST="/Users/amohan/personal/anj/personal-projects/agent-projects/amohan7ai/deploy-resume-matcher"

if [ "$SRC" = "$DEST" ]; then
  echo "Source and target are the same folder, aborting." >&2
  exit 1
fi
mkdir -p "$DEST"

DRY_RUN=""
if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN="-n"
  echo "DRY RUN - nothing will be copied or deleted"
fi

OUTPUT="$(rsync -a $DRY_RUN -i --delete \
  --exclude='/.git/' \
  --exclude='/.vercel/' \
  --exclude='/sync-to-deploy.sh' \
  --exclude='.env.local.dev' \
  --exclude='.env' \
  --exclude='.env.example' \
  --exclude='scratch-notes' \
  --filter=':- .gitignore' \
  "$SRC"/ "$DEST"/)"

echo "$OUTPUT" | awk '
  /^>f\+\+\+\+\+\+\+/ { sub(/^[^ ]+ /, ""); print "NEW      " $0; n++; next }
  /^>f/               { sub(/^[^ ]+ /, ""); print "CHANGED  " $0; c++; next }
  /^\*deleting/       { sub(/^\*deleting +/, ""); print "DELETED  " $0; d++; next }
  END { printf "\n%d new, %d changed, %d deleted\n", n, c, d }
'