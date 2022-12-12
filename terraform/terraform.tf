locals {
  region    = "eu-west-1"
  random_id = "4e77b4b9253b4a5d"
}

provider "aws" {
  profile = "harrisonpim"
  region  = local.region
}

terraform {
  required_version = ">= 0.13"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
