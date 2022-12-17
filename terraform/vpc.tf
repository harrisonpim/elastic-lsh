# Create a VPC
resource "aws_vpc" "elastic_lsh" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

# Create a public subnet
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.elastic_lsh.id
  availability_zone = "eu-west-1a"
  cidr_block        = "10.0.1.0/24"
}

# Create a security group for the ECS cluster
resource "aws_security_group" "ecs" {
  name        = "ecs-security-group"
  description = "Security group for ECS cluster"
  vpc_id      = aws_vpc.elastic_lsh.id

  # Allow inbound traffic on port 80
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  # Allow outbound traffic on all ports
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

}
