output "AWS_OPENSEARCH_ENDPOINT" {
  value = aws_opensearch_domain.elastic_lsh.endpoint
}
output "AWS_OPENSEARCH_PASSWORD" {
  value     = random_password.opensearch.result
  sensitive = true
}
output "AWS_OPENSEARCH_USERNAME" {
  value = local.opensearch_username
}
output "AWS_S3_BUCKET_ID" {
  value = aws_s3_bucket.elastic_lsh.id
}
output "AWS_LOCAL_ROLE_ARN" {
  value = aws_iam_role.local.arn
}
output "AWS_REGION" {
  value = local.region
}
output "AWS_ACCOUNT_ID" {
  value = data.aws_caller_identity.current.account_id
}
output "AWS_ECS_CLUSTER_ARN" {
  value = aws_ecs_cluster.cluster.arn
}
output "AWS_ECS_SUBNET_ID" {
  value = aws_subnet.public.id
}
output "AWS_ECS_SECURITY_GROUP_ID" {
  value = aws_security_group.ecs.id
}
