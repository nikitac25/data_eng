#!/usr/bin/env bash
set -e

if ! command -v dos2unix >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y dos2unix
fi

docker-compose up -d --wait
timeout 120 docker-compose logs -f producer
docker-compose down