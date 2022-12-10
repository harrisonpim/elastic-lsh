# this script is used to generate a local .env file for docker-compose to use

# remove the old .env file
rm -f .env

# create a new .env file
touch .env

# add the environment variables to the .env file
echo "AWS_PROFILE=harrisonpim" >> .env
echo "COMPUTE_ENVIRONMENT=local" >> .env
echo "STORAGE_ENVIRONMENT=s3" >> .env
echo "DATA_DIR=/data/raw" >> .env

# add the terraform outputs to the .env file, without whitespace
docker compose build terraform
docker compose run terraform output -json \
  | jq -r 'to_entries[] | "\(.key)=\(.value.value)"' \
  >> .env
