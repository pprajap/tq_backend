#!/bin/bash

# Stop all running containers
if [ "$(docker ps -aq)" ]; then
    docker stop $(docker ps -aq)
fi

# Remove all containers
if [ "$(docker ps -aq)" ]; then
    docker rm $(docker ps -aq)
fi

# Remove all images
if [ "$(docker images -q)" ]; then
    docker rmi $(docker images -q)
fi

# Remove all networks
if [ "$(docker network ls -q)" ]; then
    docker network rm $(docker network ls -q)
fi

# Remove all volumes
if [ "$(docker volume ls -q)" ]; then
    docker volume rm $(docker volume ls -q)
fi

# Remove dangling images, containers, volumes, and networks
docker system prune -a --volumes -f