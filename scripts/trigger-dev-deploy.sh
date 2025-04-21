#!/bin/bash
set -euo pipefail

# === CONFIG ===
# Required:
REPO_OWNER="${REPO_OWNER:-}"
GH_TOKEN="${GH_TOKEN:-}"
TARGET_REPO="caz-conf"
EVENT_TYPE="start-deployment"
REF="develop"
SHA=$(git rev-parse HEAD)

# === VALIDATION ===
if [[ -z "$GH_TOKEN" ]]; then
  echo "GH_TOKEN not set. Export it or pass in via env."
  exit 1
fi

# === DISPATCH ===
echo "Sending dispatch to $REPO_OWNER/$TARGET_REPO..."
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/$REPO_OWNER/$TARGET_REPO/dispatches \
  -d "{
    \"event_type\": \"$EVENT_TYPE\",
    \"client_payload\": {
      \"ref\": \"$REF\",
      \"sha\": \"$SHA\"
    }
  }"

echo "Dispatch sent!!!"