# Architecture

The terraform for this project provisions the following services in AWS:

![architecture](./diagrams/architecture/architecture-light.png#gh-light-mode-only)
![architecture](./diagrams/architecture/architecture-dark.png#gh-dark-mode-only)

## Services

1. An s3 bucket which stores raw images and model weights
2. An ECR repository which stores docker images for training and inference
3. An ECS cluster which runs the training docker image and:
    - fetches images from s3
    - learns to divide the images' feature space to generate lsh hashes
    - posts the resulting model weights to s3
4. An ECS cluster which runs that docker image and:
    - fetches images from s3
    - generates LSH hashes for each one, and
    - posts the results to elasticsearch
5. An elasticsearch cluster which stores the LSH hashes
6. A publicly accessible webapp which allows users to search for similar images through an API or a web interface
