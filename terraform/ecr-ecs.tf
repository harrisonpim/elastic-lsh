# Create an ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = "elastic-lsh"
}

# Create tasks definitions and repositories for each of the services
module "ecr_ecs_get_data" {
  source = "./modules/ecr-ecs"
  name   = "elastic-lsh-get-data"
  environment = {}
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
}

module "ecr_ecs_infer_features" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-infer-features"
  environment                 = {}
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
}

module "ecr_ecs_infer_hashes" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-infer-hashes"
  environment                 = {}
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
}

module "ecr_ecs_train_lsh_model" {
  source                      = "./modules/ecr-ecs"
  name                        = "elastic-lsh-train-lsh-model"
  environment                 = {}
  region                      = local.region
  ecs_task_execution_role_arn = aws_iam_role.ecs_execution.arn
  ecs_cluster_id              = aws_ecs_cluster.cluster.id
  security_group_ids          = [aws_security_group.ecs.id]
  subnet_ids                  = [aws_subnet.public.id]
}
