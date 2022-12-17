
locals {
  opensearch_username = "admin"
}

resource "random_password" "opensearch" {
  length           = 64
  min_upper        = 1
  min_lower        = 1
  min_numeric      = 1
  min_special      = 1
  override_special = "!#$%&*()-_+[]{}<>:?" # don't use =
}

resource "aws_opensearch_domain" "elastic_lsh" {
  domain_name    = "elastic-lsh"
  engine_version = "Elasticsearch_7.10"
  cluster_config {
    instance_type = "t3.small.search"
  }

  # Define the EBS volume for the EC2 instance
  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }

  # Set a master username and password
  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = local.opensearch_username
      master_user_password = random_password.opensearch.result

    }
  }
  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }
  encrypt_at_rest {
    enabled = true
  }
  node_to_node_encryption {
    enabled = true
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
