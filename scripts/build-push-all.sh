#!/bin/bash
set -euo pipefail

# Accept environment as first argument, required
ENVIRONMENT="${1:-}"
if [[ -z "$ENVIRONMENT" ]]; then
  echo "Usage: $0 <environment>"
  echo "Example: $0 dev"
  exit 1
fi

# Dynamically generate image tag: e.g. dev_202504231920
TIMESTAMP=$(date +%Y%m%d%H%M)
IMAGE_TAG="${ENVIRONMENT}_${TIMESTAMP}"

# Require AWS_REGION and AWS_ACCOUNT_ID to be set
if [[ -z "${AWS_REGION:-}" || -z "${AWS_ACCOUNT_ID:-}" ]]; then
  echo "ERROR: AWS_REGION and AWS_ACCOUNT_ID must be set in environment"
  exit 1
fi

echo "Using AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"
echo "AWS_REGION: $AWS_REGION"
echo "Image tag: $IMAGE_TAG"

echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build and push all Dockerfiles
find . -name "Dockerfile" | while read -r dockerfile; do
  dir=$(dirname "$dockerfile")
  service_name=$(basename "$dir" | tr '_' '-')

  echo "Building image for service: $service_name (found in $dir)"

  IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$service_name:$IMAGE_TAG"
  LATEST_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$service_name:latest"

  echo "Building image: $IMAGE_URI"
  docker build -t "$IMAGE_URI" "$dir"

  echo "Tagging as latest: $LATEST_URI"
  docker tag "$IMAGE_URI" "$LATEST_URI"

  echo "Pushing to ECR..."
  docker push "$IMAGE_URI"
  docker push "$LATEST_URI"

  echo "Done with $service_name"
done

echo "All images built and pushed successfully with tag: $IMAGE_TAG"