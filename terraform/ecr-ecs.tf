# Create an ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = "elastic-lsh"
}

# Create tasks definitions and repositories for each of the services
module "ecr_ecs_get_data" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-get-data"
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_task_role_arn           = aws_iam_role.ecs.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
  environment = {
    "STORAGE_ENVIRONMENT" = "s3",
    "S3_BUCKET_ID"        = aws_s3_bucket.elastic_lsh.id,
  }
}

module "ecr_ecs_infer_features" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-infer-features"
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_task_role_arn           = aws_iam_role.ecs.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
  environment = {
    "STORAGE_ENVIRONMENT" = "s3",
    "S3_BUCKET_ID"        = aws_s3_bucket.elastic_lsh.id,
  }
}

module "ecr_ecs_train_lsh_model" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-train-lsh-model"
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_task_role_arn           = aws_iam_role.ecs.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
  environment = {
    "STORAGE_ENVIRONMENT" = "s3",
    "S3_BUCKET_ID"        = aws_s3_bucket.elastic_lsh.id,
  }
}

module "ecr_ecs_infer_hashes" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-infer-hashes"
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_task_role_arn           = aws_iam_role.ecs.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
  environment = {
    "STORAGE_ENVIRONMENT"     = "s3",
    "S3_BUCKET_ID"            = aws_s3_bucket.elastic_lsh.id,
    "AWS_OPENSEARCH_ENDPOINT" = aws_opensearch_domain.elastic_lsh.endpoint
    "AWS_OPENSEARCH_USERNAME" = local.opensearch_username
    "AWS_OPENSEARCH_PASSWORD" = random_password.opensearch.result
  }
}
