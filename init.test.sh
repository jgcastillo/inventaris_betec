#!/bin/bash

enviroment="test"

echo "Akonomi - $enviroment"

# Run Docker command
docker-compose -f docker-compose.test.yml $@
