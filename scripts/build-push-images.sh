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

# === Force Image Tag ===
TIMESTAMP=$(date +%Y%m%d%H%M)
IMAGE_TAG="${ENVIRONMENT}_${TIMESTAMP}"
ENVIRONMENT_TAG="${ENVIRONMENT}"

# === Validate AWS Vars ===
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

# === Build and Push ===
build_and_push() {
  local dir="$1"
  local svc_name
  svc_name=$(basename "$dir" | tr '_' '-')

  BASE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$svc_name"
  IMAGE_URI="$BASE_URI:$IMAGE_TAG"
  ENV_URI="$BASE_URI:$ENVIRONMENT_TAG"

  echo "Building image for service: $svc_name"

  # Build ONLY ONCE (with timestamped tag)
  docker build -t "$IMAGE_URI" "$dir"

  # Tag for environment (qa, uat, prod)
  echo "Tagging image as ${ENVIRONMENT_TAG}"
  docker tag "$IMAGE_URI" "$ENV_URI"

  # Push all tags
  echo "Pushing all tags for $svc_name..."
  docker push "$IMAGE_URI"
  docker push "$ENV_URI"

  echo ""
  echo "Tags pushed for $svc_name:"
  echo "    → $IMAGE_TAG"
  echo "    → $ENVIRONMENT_TAG"
  echo ""
}

# === Single or All Services ===
if [[ -n "$SERVICE_NAME" ]]; then
  TARGET_DIR=$(find . -type d -name "$SERVICE_NAME" -print -quit)
  if [[ -z "$TARGET_DIR" ]]; then
    echo "ERROR: Service Directory for $SERVICE_NAME Unavailable"
    exit 1
  fi
  build_and_push "$TARGET_DIR"
else
  find . -name "Dockerfile" -print0 | xargs -0 -I{} dirname "{}" | while read -r dir; do
    build_and_push "$dir"
  done
fi

# Wait for all background pushes to finish
wait

echo ""
echo "All Images Built (tags: $IMAGE_TAG, $ENVIRONMENT_TAG)"