# Create bucket 
resource "aws_s3_bucket" "elastic_lsh" {
  bucket        = "elastic-lsh-${local.random_id}"
  force_destroy = true
}

# set ACL to only be readable within the VPC
resource "aws_s3_bucket_acl" "elastic_lsh_bucket_acl" {
  bucket = aws_s3_bucket.elastic_lsh.id
  acl    = "private"
}
