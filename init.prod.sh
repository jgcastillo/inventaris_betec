#!/bin/bash

enviroment="Producción"

echo "Akonomi - $enviroment"

# Run Docker command
docker-compose -f docker-compose.prod.yml $@