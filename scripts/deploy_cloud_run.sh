#!/usr/bin/env bash
# Simple deploy helper for Cloud Run (managed)
# Usage: ./scripts/deploy_cloud_run.sh <PROJECT_ID> [REGION] [IMAGE_TAG]

set -euo pipefail

PROJECT_ID=${1:-}
REGION=${2:-us-central1}
IMAGE_TAG=${3:-latest}

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: $0 <PROJECT_ID> [REGION] [IMAGE_TAG]"
  exit 1
fi

IMAGE=gcr.io/${PROJECT_ID}/agent-reliability-guardian:${IMAGE_TAG}

echo "Building container image ${IMAGE}..."
docker build -t ${IMAGE} .

echo "Pushing image to Container Registry..."
docker push ${IMAGE}

echo "Deploying to Cloud Run in ${REGION}..."
gcloud run deploy agent-reliability-guardian \
  --image=${IMAGE} \
  --platform=managed \
  --region=${REGION} \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --set-env-vars "GOOGLE_API_KEY=$GOOGLE_API_KEY,GOOGLE_CLOUD_PROJECT=${PROJECT_ID}"

echo "Deployment finished."
