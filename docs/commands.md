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

### Destroy AWS infrastructure

To destroy the AWS infrastructure, run:

```sh
terraform destroy
```

### Environment variables

Applying the terraform runs the `scripts/create-local-env-file.sh` script, which creates a `.env` file in the root of the repository. This file contains the environment variables that are used by the pipeline. The script uses the terraform outputs to populate the variables.

## Building the pipeline services

```sh
docker compose build
```

To build a production version of the app (without local environment variables built in), run:

```sh
docker compose -f docker-compose.prod.yml build
```

## Running a container locally

```sh
docker compose run <service>
```

You should replace `<service>` with the name of the pipeline step that you want to run. NB this will run the local version of the app, which will require a `.env` file to be present in the root of the repository (see the [environment variables section](#environment-variables) for more details).

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
