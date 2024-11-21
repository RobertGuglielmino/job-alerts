#!/bin/bash

echo "Starting Docker Desktop..."
open -a "Docker"

check_docker() {
    while ! docker ps > /dev/null 2>&1; do
        echo "Waiting for Docker to be ready..."
        sleep 10
    done
}

check_docker

echo "Docker is ready. Starting containers..."
cd "$HOME/job-alerts"
if docker-compose up -d; then
    echo "$(date) - Successfully started container" >> ~/Scripts/docker-startup.log
else
    echo "$(date) - Failed to start container. Error code: $?" >> ~/Scripts/docker-startup.log
fi