#!/bin/bash

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove all networks
docker network rm $(docker network ls -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Remove dangling images, containers, volumes, and networks
docker system prune -a --volumes -f