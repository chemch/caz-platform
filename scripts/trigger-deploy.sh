#!/bin/bash
set -euo pipefail

# === CONFIG ===
REPO_OWNER="${REPO_OWNER:-}"        # e.g. chemch
GH_TOKEN="${GH_TOKEN:-}"            # GitHub PAT
TARGET_REPO="caz-conf"
EVENT_TYPE="start-deployment"
REF="develop"
SHA=$(git rev-parse HEAD)

# === INPUTS ===
ENVIRONMENT="${1:-dev}"             # default to 'dev' if not passed
TAG="${2:-latest}"                  # default to 'latest' if not passed
SERVICE_NAME="${3:-detection-svc}"  # optional 3rd param

# === VALIDATION ===
if [[ -z "$REPO_OWNER" || -z "$GH_TOKEN" ]]; then
  echo "REPO_OWNER and GH_TOKEN must be set"
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
      \"environment\": \"$ENVIRONMENT\",
      \"tag\": \"$TAG\",
      \"service_name\": \"$SERVICE_NAME\",
      \"ref\": \"$REF\",
      \"sha\": \"$SHA\"
    }
  }"

echo "Dispatch sent: env=$ENVIRONMENT tag=$TAG service=$SERVICE_NAME"