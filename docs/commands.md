# Useful commands for working with the repository

## Build infrastructure

```sh
terraform init
terraform plan
terraform apply
```

## Creating a local .env file

```sh
sh ./scripts/create-local-env-file.sh
```

This is also run every time the terraform is applied (`terraform apply`).

## Push a container image to ECR

```sh
sh ./scripts/push-image-to-ecr.sh
```
