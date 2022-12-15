# Useful commands for working with the repository

## Deploy AWS infrastructure

First, `cd` into the `terraform` directory. Then, run the following commands:

```sh
terraform init
terraform plan
terraform apply
```

This will create a set of resources in AWS that will be used by the pipeline. The resources include:

- An ECR repository for storing the pipeline images
- An ECS cluster for running the pipeline
- An ECS task definition for each pipeline step
- An ECS service for each pipeline step
- An S3 bucket for storing the pipeline artifacts
- An Opensearch domain for storing hashes and running the image similarity queries

See [the architecture documentation](architecture.md) for more details.

## Building the pipeline services

```sh
docker compose build
```

## Running a container locally

```sh
docker compose -f docker-compose.local.yml run <service>
```

You should replace `<service>` with the name of the pipeline step that you want to run. Specifying `-f docker-compose.local.yml` will instruct docker to use the local environment variables in `.env` to run the container.

## Push a container image to ECR

```sh
sh ./scripts/push-image-to-ecr.sh <service>
```

Again, you should replace `<service>` with the name of the pipeline step that you want to push.

## Run a pipeline step in AWS

```sh
sh ./scripts/run-task.sh <service>
```

Again, you should replace `<service>` with the name of the pipeline step that you want to run.

## Watching the pipeline logs

```sh
sh ./scripts/watch-logs.sh <service>
```

Again, you should replace `<service>` with the name of the pipeline step that you want to watch.
