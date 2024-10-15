#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Treat unset variables as an error
set -u

echo "Starting cleanup..."
# call ./cleanup.sh to remove all images and containers
./cleanup.sh
echo "Cleanup completed."

echo "Building tq-backend image..."
# build tq-backend image
docker build -f tq_backend/Dockerfile -t tq-backend .
echo "Image build completed."

# Docker login
if [ -z "${DOCKER_USERNAME:-}" ] || [ -z "${DOCKER_PASSWORD:-}" ]; then
  echo "DOCKER_USERNAME and DOCKER_PASSWORD must be set"
  exit 1
fi

echo "Logging into Docker..."
echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin
echo "Docker login successful."

echo "Tagging and pushing the image to Docker Hub..."
# push above to docker hub
docker tag tq-backend:latest  $DOCKER_USERNAME/tq-backend:latest
docker push $DOCKER_USERNAME/tq-backend:latest
echo "Image pushed to Docker Hub successfully."
