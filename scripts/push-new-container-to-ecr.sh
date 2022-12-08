set -e

# Log in to the ECR registry
aws ecr get-login-password --region REGION | \
  docker login --username AWS \
  --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com

# Build and push the Docker image
docker build -t container-image .
docker tag container-image:latest \
  ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/container-repository:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/container-repository:latest
