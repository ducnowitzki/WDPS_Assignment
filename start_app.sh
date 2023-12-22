#!/bin/bash

# Set default values
local_output_path=$(pwd)
container_output_path="/app/output"
image_name="wdps_group2"

echo "Building Docker image '$image_name'..."
# Build the Docker image
docker build -t "$image_name" .

# Parse command line arguments
if [ "$1" == "-d" ]; then
    echo "Running in debug mode..."
    docker run --rm -v "$local_output_path":"$container_output_path" -e DEBUG=1 "$image_name" 
else
    echo "Running..."
    docker run --rm -v "$local_output_path":"$container_output_path" -e DEBUG=0 "$image_name" 
fi
