#!/usr/bin/env bash
set -e

echo "starting zookeeper & kafka"
docker-compose up -d zookeeper kafka >/dev/null

# small wait so broker is ready
sleep 8

BIN="/opt/bitnami/kafka/bin"
BROKER="kafka:9092"
TOPIC="${1:-tweets}"

echo "ensuring topic '$TOPIC' exists"
docker-compose exec -T kafka bash -lc \
  "$BIN/kafka-topics.sh --bootstrap-server $BROKER --create --if-not-exists --topic $TOPIC --partitions 1 --replication-factor 1" || true

echo "ready"
