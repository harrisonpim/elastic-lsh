#!/bin/bash
set -euo pipefail


# get the container name from the first argument
CONTAINER_NAME=$1

# load environment variables
source .env

AWS_ECR_URL=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/elastic-lsh
IMAGE_URL=$AWS_ECR_URL-$CONTAINER_NAME\:latest

# Log in to ECR
aws ecr get-login-password --region $AWS_REGION --profile $AWS_PROFILE | \
  docker login --username AWS \
  --password-stdin $AWS_ECR_URL

# Build, tag and push the Docker image to ECR
docker compose build $CONTAINER_NAME
docker tag $CONTAINER_NAME $IMAGE_URL
docker push $IMAGE_URL
