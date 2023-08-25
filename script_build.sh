#!/bin/bash

# Variables
docker_repo_name="tki"
docker_image_name="image-compress"
docker_tag="latest"

# Step 2: Build Docker image
echo "docker build -t "$docker_repo_name/$docker_image_name:$docker_tag" ."
docker build -t "$docker_repo_name/$docker_image_name:$docker_tag" .

# Step 3: Create Docker tag for image (auto generate tag)
# Assuming you want to tag the image with a timestamp
timestamp=$(date +%Y%m%d%H%M%S)
echo "$docker_repo_name/$docker_image_name:$docker_tag" "$docker_repo_name/$docker_image_name:$docker_tag-$timestamp"
docker tag "$docker_repo_name/$docker_image_name:$docker_tag" "$docker_repo_name/$docker_image_name:$docker_tag-$timestamp"
