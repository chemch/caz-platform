#!/bin/bash
set -euo pipefail

# === Inputs ===
ENVIRONMENT="${1:-}"
SERVICE_NAME="${2:-}"  # Optional

if [[ -z "$ENVIRONMENT" ]]; then
  echo "Usage: $0 <environment> [service_name]"
  echo "Example: $0 dev"
  exit 1
fi

# === Image tag generation ===
: "${TIMESTAMP:=$(date +%Y%m%d%H%M)}"
: "${IMAGE_TAG:=${ENVIRONMENT}_${TIMESTAMP}}"
ENVIRONMENT_TAG="${ENVIRONMENT}"

# === Validate AWS vars ===
if [[ -z "${AWS_REGION:-}" || -z "${AWS_ACCOUNT_ID:-}" ]]; then
  echo "ERROR: AWS_REGION and AWS_ACCOUNT_ID must be set in environment"
  exit 1
fi

echo "AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"
echo "AWS_REGION: $AWS_REGION"
echo "ENVIRONMENT: $ENVIRONMENT"
echo "IMAGE_TAG: $IMAGE_TAG"
echo "SERVICE_NAME: ${SERVICE_NAME:-<all>}"

# === Log in to ECR ===
aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# === Build and Push Logic ===
build_and_push() {
  local dir="$1"
  local svc_name
  svc_name=$(basename "$dir" | tr '_' '-')

  BASE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$svc_name"
  IMAGE_URI="$BASE_URI:$IMAGE_TAG"
  LATEST_URI="$BASE_URI:latest"
  ENV_URI="$BASE_URI:$ENVIRONMENT_TAG"

  echo "🚧 Building image for service: $svc_name"
  docker build -t "$IMAGE_URI" "$dir"

  echo "🔖 Tagging $svc_name with latest and $ENVIRONMENT"
  docker tag "$IMAGE_URI" "$LATEST_URI"
  docker tag "$IMAGE_URI" "$ENV_URI"

  echo "📤 Pushing $svc_name images to ECR..."
  docker push "$IMAGE_URI" &
  docker push "$LATEST_URI" &
  docker push "$ENV_URI" &

  # Print nice report
  echo ""
  echo "🖼️ Tags pushed for $svc_name:"
  echo "    → $IMAGE_TAG"
  echo "    → latest"
  echo "    → $ENVIRONMENT"
  echo ""
}

# === Single service or all ===
if [[ -n "$SERVICE_NAME" ]]; then
  TARGET_DIR=$(find . -type d -name "$SERVICE_NAME" -print -quit)
  if [[ -z "$TARGET_DIR" ]]; then
    echo "ERROR: Service directory for $SERVICE_NAME not found"
    exit 1
  fi
  build_and_push "$TARGET_DIR"
else
  # Safer find with -print0 and xargs -0
  find . -name "Dockerfile" -print0 | xargs -0 -I{} dirname "{}" | while read -r dir; do
    build_and_push "$dir"
  done
fi

# Wait for all background pushes to finish
wait

echo ""
echo "🚀 All image builds complete (tags: $IMAGE_TAG, latest, $ENVIRONMENT_TAG)"