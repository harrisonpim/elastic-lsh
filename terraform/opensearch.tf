# Define the service-linked role for OpenSearch
resource "aws_iam_service_linked_role" "opensearch_role" {
  aws_service_name = "opensearchservice.amazonaws.com"
}

resource "random_password" "opensearch" {
  length  = 64
  special = false
}

locals {
  opensearch_username = "admin"
}

resource "aws_opensearch_domain" "elastic_lsh" {
  domain_name = "elastic-lsh"

  engine_version = "Elasticsearch_7.10"
  cluster_config {
    instance_type = "t3.small.search"
  }

  vpc_options {
    subnet_ids = [
      aws_subnet.public.id
    ]

    security_group_ids = [aws_security_group.opensearch.id]
  }

  # Define the EBS volume for the EC2 instance
  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }

  # Set a master username and password
  advanced_security_options {
    enabled                        = false
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = local.opensearch_username
      master_user_password = random_password.opensearch.result

    }
  }

  # Define the access policy for the OpenSearch domain
  access_policies = <<CONFIG
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "es:*",
            "Principal": "*",
            "Effect": "Allow",
            "Resource": "arn:aws:es:eu-west-1:${data.aws_caller_identity.current.account_id}:domain/elastic-lsh/*"
        }
    ]
}
CONFIG
}
