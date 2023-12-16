#!/bin/bash

# Set default values
local_output_path=$(pwd)
container_output_path="/app/output"
image_name="delphi"

# Build the Docker image
docker build -t "$image_name" .

# Run the Docker container with volume mounts
docker run --rm -v "$local_output_path":"$container_output_path" "$image_name"
