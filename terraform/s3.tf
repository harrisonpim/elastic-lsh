# Create images bucket 
resource "aws_s3_bucket" "images" {
  bucket = "elastic-lsh-images-${local.random_id}"
  force_destroy = true
}

# set ACL to only be readable within the VPC
resource "aws_s3_bucket_acl" "images_bucket_acl" {
  bucket = aws_s3_bucket.images.id
  acl    = "private"
}
