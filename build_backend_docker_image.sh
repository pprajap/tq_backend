#!/bin/bash

echo "Building tq-backend image..."
# build tq-backend image
docker build -f Dockerfile -t tq-backend .
echo "Image build completed."
