# Create a VPC
resource "aws_vpc" "elastic_lsh" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

# Create a public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.elastic_lsh.id
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
  cidr_block              = "10.0.1.0/24"
}

# Create a security group for the opensearch cluster
resource "aws_security_group" "opensearch" {
  name        = "opensearch-security-group"
  description = "Security group for opensearch cluster"
  vpc_id      = aws_vpc.elastic_lsh.id

  # Allow inbound traffic on port 9200 and 9300
  ingress {
    from_port   = 9200
    to_port     = 9200
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9300
    to_port     = 9300
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a security group for the ECS cluster
resource "aws_security_group" "ecs" {
  name        = "ecs-security-group"
  description = "Security group for ECS cluster"
  vpc_id      = aws_vpc.elastic_lsh.id

  # Allow inbound traffic on port 22
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic to the Internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a security group for the s3 bucket
resource "aws_security_group" "s3" {
  name        = "s3-security-group"
  description = "Security group for s3 bucket"
  vpc_id      = aws_vpc.elastic_lsh.id

  # Allow inbound traffic on port 443
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
