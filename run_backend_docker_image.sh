#!/bin/bash

echo "Running tq-backend image..."
# run the Docker container
docker run -it --rm -p 5000:5000 tq-backend
