set -euo pipefail

# Pick compose command (Docker Desktop v2 or legacy)
if docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  DOCKER_COMPOSE="docker-compose"
else
  echo "ERROR: docker compose / docker-compose not found." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

COMPOSE_PATH="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.yml}"

if [[ ! -f "$COMPOSE_PATH" ]]; then
  echo "ERROR: compose file not found at: $COMPOSE_PATH" >&2
  echo "Hint: run with: COMPOSE_FILE=../docker-compose.yml ./setup_kafka.sh" >&2
  exit 1
fi

echo "Using compose file: $COMPOSE_PATH"
$DOCKER_COMPOSE -f "$COMPOSE_PATH" up -d

echo "Waiting for broker to initialize..."
sleep 10

echo "Creating topic 'tweets' (idempotent)..."
docker exec broker bash -lc 'kafka-topics.sh --bootstrap-server broker:9092 --create --if-not-exists --topic tweets --partitions 1 --replication-factor 1 || true'

echo "Topics:"
docker exec broker bash -lc 'kafka-topics.sh --bootstrap-server broker:9092 --list'

