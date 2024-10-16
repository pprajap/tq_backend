#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Treat unset variables as an error
set -u

./build_backend_docker_image.sh

# Docker login
docker login

# fetch user name from docker login
export DOCKER_USERNAME=$(docker info | grep Username | awk '{print $2}')

# push above to docker hub
docker tag tq-backend:latest  $DOCKER_USERNAME/tq-backend:latest
docker push $DOCKER_USERNAME/tq-backend:latest
