#!/bin/bash
set -euo pipefail

# === CONFIG ===
REPO_OWNER="${REPO_OWNER:-}"
GH_TOKEN="${GH_TOKEN:-}"
TARGET_REPO="caz-conf"
EVENT_TYPE="start-deployment"

# === INPUTS ===
ENVIRONMENT="${1:-dev}"
SERVICE_NAME="${2:-}"

# === VALIDATION ===
if [[ -z "$REPO_OWNER" || -z "$GH_TOKEN" ]]; then
  echo "REPO_OWNER and GH_TOKEN Required"
  exit 1
fi

# === BUILD PAYLOAD ===
if [[ -n "$SERVICE_NAME" ]]; then
  PAYLOAD=$(jq -n \
    --arg env "$ENVIRONMENT" \
    --arg svc "$SERVICE_NAME" \
    '{
      event_type: "start-deployment",
      client_payload: {
        environment: $env,
        service_name: $svc
      }
    }')
else
  PAYLOAD=$(jq -n \
    --arg env "$ENVIRONMENT" \
    '{
      event_type: "start-deployment",
      client_payload: {
        environment: $env
      }
    }')
fi

# === DISPATCH ===
echo "Sending Dispatch: $REPO_OWNER/$TARGET_REPO..."
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/$REPO_OWNER/$TARGET_REPO/dispatches \
  -d "$PAYLOAD"

echo "Dispatch Sent: ENV=$ENVIRONMENT ${SERVICE_NAME:+service=$SERVICE_NAME}"