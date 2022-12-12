#!/bin/bash
set -euo pipefail

GIT_ROOT=$(git rev-parse --show-toplevel)
DOTENV_PATH=$GIT_ROOT/.env

# remove the old .env file
rm -f $DOTENV_PATH

# create a new $DOTENV_PATH file
touch $DOTENV_PATH

# add the environment variables to the .env file
echo "AWS_PROFILE=harrisonpim" >> $DOTENV_PATH

# add the terraform outputs to the .env file, without whitespace
terraform output -json \
  | jq -r 'to_entries[] | "\(.key)=\(.value.value)"' \
  >> $DOTENV_PATH
