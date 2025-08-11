#!/usr/bin/env bash
set -euo pipefail
# Bring up Kafka stack
COMPOSE="${COMPOSE_FILE:-docker-compose.yml}"
docker compose -f "${COMPOSE}" up -d
echo "Waiting for broker to be healthy..."
sleep 10
docker exec broker bash -lc 'kafka-topics.sh --bootstrap-server broker:9092 --create --if-not-exists --topic tweets --partitions 1 --replication-factor 1 || true'
echo "Topics:"
docker exec broker bash -lc 'kafka-topics.sh --bootstrap-server broker:9092 --list'
