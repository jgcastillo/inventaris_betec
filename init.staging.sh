#!/bin/bash

enviroment="staging"

echo "Akonomi - $enviroment"

# Run Docker command
docker-compose -f docker-compose.st.yml $@
