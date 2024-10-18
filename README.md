# tq-backend

This repository contains the backend component for the Terra Quantum solution, which includes an optimization service using the `TTOpt` class.

## Table of Contents
- [tq-backend](#tq-backend)
  - [Table of Contents](#table-of-contents)
  - [Build the Docker Image](#build-the-docker-image)
  - [Run the Docker Container](#run-the-docker-container)
  - [API Reference](#api-reference)
  - [Requirements](#requirements)

## Build the Docker Image
To build the Docker image for the backend, run the following script:
```sh
docker build -t tq-backend .
```

## Run the Docker Container
To run the Docker container, use the following script:
```sh
docker run -it --rm -p 5000:5000 tq-backend
```

## API Reference
The API reference for the backend service can be found [here](docs/api_reference.md).

## Requirements
- Docker
- Docker Compose

