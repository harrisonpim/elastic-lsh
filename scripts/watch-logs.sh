set -euo pipefail

# get the task name from the first argument
TASK_NAME=$1

# load environment variables from the .env file
source .env

# watch the cloudwatch logs for the task
AWS_PROFILE=harrisonpim aws logs tail \
  --follow \
  --region $AWS_REGION \
  /ecs/elastic-lsh-$TASK_NAME
