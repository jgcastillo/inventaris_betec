#!/bin/bash

enviroment="local"

echo "Inventaris - $enviroment"

architecture=$(arch)

if [ $architecture == 'arm64' ]; then
    source backend/.env
    ARCH=$ARCH_ARM
else
    source backend/.env
    ARCH=$ARCH_AMD

fi

export ARCH

# Run Docker command
docker compose -f docker-compose.local.yml $@