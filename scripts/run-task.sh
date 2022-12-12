set -euo pipefail

# get the task name from the first argument
TASK_NAME=$1

# load environment variables from the .env file
source .env

# run the ecs task using the task name and the aws cli
aws ecs run-task --cluster $AWS_ECS_CLUSTER_ARN --task-definition $TASK_NAME

