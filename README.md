# tq-backend

This repository contains the backend component for the Terra Quantum solution, which includes an optimization service using the `TTOpt` class.

## Table of Contents
- [tq-backend](#tq-backend)
  - [Table of Contents](#table-of-contents)
  - [Build the Docker Image](#build-the-docker-image)
  - [Run the Docker Container](#run-the-docker-container)
  - [Push the Docker Image to Docker Hub](#push-the-docker-image-to-docker-hub)
  - [API Reference](#api-reference)
  - [Requirements](#requirements)
  - [Scripts](#scripts)
    - [build\_backend\_docker\_image.sh](#build_backend_docker_imagesh)
    - [run\_backend\_docker\_image.sh](#run_backend_docker_imagesh)
    - [push\_backend\_docker\_image.sh](#push_backend_docker_imagesh)

## Build the Docker Image
To build the Docker image for the backend, run the following script:
```sh
./scripts/build_backend_docker_image.sh
```

## Run the Docker Container
To run the Docker container, use the following script:
```sh
./scripts/run_backend_docker_image.sh
```

## Push the Docker Image to Docker Hub
To push the Docker image to Docker Hub, execute the following script:
```sh
./scripts/push_backend_docker_image.sh
```

## API Reference
The API reference for the backend service can be found [here](docs/api_reference.md).

## Requirements
- Docker
- Docker Compose

## Scripts
### build_backend_docker_image.sh
This script builds the Docker image for the backend service.

### run_backend_docker_image.sh
This script runs the Docker container for the backend service.

### push_backend_docker_image.sh
This script pushes the Docker image to Docker Hub.
