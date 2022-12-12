resource "null_resource" "create_env_file" {
  # every time terraform is applied, the local-exec provisioner will run
  # the script to create a local .env file
  provisioner "local-exec" {
    command = "$(git rev-parse --show-toplevel)/scripts/create-local-env-file.sh"
  }
  triggers = {
    always_run = "${timestamp()}"
  }
}
