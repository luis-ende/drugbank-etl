#!/bin/bash

DRUGBANK_CSV_PATH=$1
DB_PASSWORD=$2
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DOCKER_CONTEXT="${SCRIPT_DIR}"

# Build image first if it doesn't exist yet
drugbank_image=$( docker images -q drugbank/postgres:latest )
if [[ -z "${drugbank_image}" ]]; then
  echo "Building Docker image..."
  docker image build "$DOCKER_CONTEXT" -t drugbank/postgres
else
  echo "Removing currrent Docker container..."
  docker rm -f drugbank-postgres
fi

# DB Service will be available once the drugbank data has been loaded from the CSV directory
echo "Running new Docker container..."
docker run --name drugbank-postgres --restart=always \
  --mount type=bind,source="$DRUGBANK_CSV_PATH",target=/opt/drugbank-data \
  -p 7766:5432 \
  -e POSTGRES_PASSWORD="$DB_PASSWORD" -e POSTGRES_DB=drugbank \
  -d drugbank/postgres
