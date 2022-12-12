set -euo pipefail

# get the task name from the first argument
TASK_NAME=$1

# load environment variables from the .env file
source .env

# run the ecs task using the task name and the aws cli
aws ecs run-task \
  --cluster $AWS_ECS_CLUSTER_ARN \
  --task-definition elastic-lsh-$TASK_NAME \
  --profile $AWS_PROFILE \
  --region $AWS_REGION \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$AWS_ECS_SUBNET_ID],securityGroups=[$AWS_ECS_SECURITY_GROUP_ID],assignPublicIp=DISABLED}" \

