#!/bin/bash
set -euo pipefail

IMAGE_TAG="${IMAGE_TAG:-$(git rev-parse --short HEAD)}"

if [[ -z "${AWS_REGION:-}" || -z "${AWS_ACCOUNT_ID:-}" ]]; then
  echo "ERROR: AWS_REGION and AWS_ACCOUNT_ID must be set in environment"
  exit 1
fi

echo "Using AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"
echo "AWS_REGION: $AWS_REGION"
echo "Image tag: $IMAGE_TAG"

# Authenticate to ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Find and process all Dockerfiles
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

echo "All images built and pushed successfully."