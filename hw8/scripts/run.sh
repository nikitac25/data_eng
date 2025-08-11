#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SCRIPT_DIR}/.."
IMAGE_NAME="homework8/tweet-writer:latest"

# Use same docker network as the compose stack
NET="homework8-kafka-net"
docker network create "${NET}" >/dev/null 2>&1 || true

# Ensure compose services are on the network
# If you used docker-compose up in ROOT, they will be on a default network, so we connect them:
docker network connect "${NET}" broker >/dev/null 2>&1 || true
docker network connect "${NET}" zookeeper >/dev/null 2>&1 || true

# Run producer
docker run --rm --name tweet-writer \
  --network "${NET}" \
  -e KAFKA_BROKER="broker:9092" \
  -e KAFKA_TOPIC="tweets" \
  -e RATE_PER_SEC="${RATE_PER_SEC:-12}" \
  -v "${ROOT}/data:/app/data:ro" \
  "${IMAGE_NAME}" --broker broker:9092 --topic tweets --input /app/data/sample.csv --rate "${RATE_PER_SEC:-12}"
