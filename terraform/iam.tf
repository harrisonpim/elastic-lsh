# Create an IAM role for the ECS tasks
resource "aws_iam_role" "ecs" {
  name = "ecs-role"

  # Add trust policy for the ECS tasks
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach the opensearch access policy to the role
resource "aws_iam_policy_attachment" "ecs_es" {
  name       = "ecs-es-policy-attachment"
  roles      = [aws_iam_role.ecs.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonOpenSearchServiceFullAccess"
}

# Attach the s3 access policy to the role
resource "aws_iam_policy_attachment" "ecs_s3" {
  name       = "ecs-s3-policy-attachment"
  roles      = [aws_iam_role.ecs.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Create an IAM role for the ECS task execution
resource "aws_iam_role" "ecs_execution" {
  name = "ecs-execution-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach the ECS task execution policy to the role
resource "aws_iam_policy_attachment" "ecs_execution" {
  name       = "ecs-execution-policy-attachment"
  roles      = [aws_iam_role.ecs_execution.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# Create an IAM role for accessing s3 and opensearch from local machine
resource "aws_iam_role" "local" {
  name               = "local-role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

# Attach the opensearch access policy to the role
resource "aws_iam_policy_attachment" "local_es" {
  name       = "local-es-policy-attachment"
  roles      = [aws_iam_role.local.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonOpenSearchServiceFullAccess"
}

# Attach the s3 access policy to the role
resource "aws_iam_policy_attachment" "local_s3" {
  name       = "local-s3-policy-attachment"
  roles      = [aws_iam_role.local.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
