variable "name" {
  type = string
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "region" {
  type = string
}

variable "ecs_task_execution_role_arn" {
  type = string
}

variable "ecs_cluster_id" {
  type = string
}

variable "security_group_ids" {
  type    = list(string)
  default = []
}

variable "subnet_ids" {
  type    = list(string)
  default = []
}

resource "aws_ecr_repository" "repo" {
  name         = var.name
  force_delete = true # this is required to delete the repository if it has images in it
}

resource "aws_cloudwatch_log_group" "ecs_task" {
  name = "/ecs/${var.name}"
}

resource "aws_ecs_task_definition" "ecs_task" {
  family                   = var.name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = var.ecs_task_execution_role_arn
  container_definitions    = <<DEFINITION
[
  {
    "name": "${var.name}",
    "image": "${aws_ecr_repository.repo.repository_url}",
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ],
    "environment": [
      ${join(", ", [for k, v in var.environment : "{ \"name\": \"${k}\", \"value\": \"${v}\" }"])}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${aws_cloudwatch_log_group.ecs_task.name}",
        "awslogs-region": "${var.region}",
        "awslogs-stream-prefix": "${var.name}"
      }
    }
  }
]
DEFINITION
}

# Create an ECS FARGATE service to run the task
resource "aws_ecs_service" "get_data" {
  name            = var.name
  task_definition = aws_ecs_task_definition.ecs_task.arn
  cluster         = var.ecs_cluster_id
  launch_type     = "FARGATE"

  # Configure the service to use the VPC and security group
  network_configuration {
    security_groups = var.security_group_ids
    subnets         = var.subnet_ids
  }
}
