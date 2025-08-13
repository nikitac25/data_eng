if ! command -v dos2unix >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y dos2unix
fi

set -e

echo "starting zookeeper & kafka"
docker-compose up -d zookeeper kafka >/dev/null

sleep 10

BIN="/opt/bitnami/kafka/bin"
BROKER="kafka:9092"
TOPIC="${1:-tweets}"

echo "ensuring topic '$TOPIC' exists"
docker-compose exec -T kafka bash -lc \
  "$BIN/kafka-topics.sh --bootstrap-server $BROKER --create --if-not-exists --topic $TOPIC --partitions 1 --replication-factor 1" || true

echo "ready"
