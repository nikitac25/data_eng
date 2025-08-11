set -euo pipefail

# Usage: ./consume.sh [SECONDS]
# If SECONDS=0 -> stream until Ctrl+C

DURATION="${1:-30}"

# pick compose command
if docker compose version >/dev/null 2>&1; then
  DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
else
  echo "ERROR: docker compose / docker-compose not found." >&2
  exit 1
fi

# resolve repo root and compose file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPOSE_PATH="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.yml}"

if [[ ! -f "$COMPOSE_PATH" ]]; then
  echo "ERROR: compose file not found at: $COMPOSE_PATH" >&2
  echo "Hint: COMPOSE_FILE=../docker-compose.yml ./consume.sh" >&2
  exit 1
fi

KAFKA_BIN="/opt/bitnami/kafka/bin"
CONSUMER="$KAFKA_BIN/kafka-console-consumer.sh"
CMD="$CONSUMER --bootstrap-server broker:9092 --topic tweets --from-beginning --property print.key=true --property print.timestamp=true"

if [[ "${DURATION}" -eq 0 ]]; then
  echo "Consuming from 'tweets' (Ctrl+C to stop)..."
  # -T = no pseudo-TTY (plays nicer with pipes/timeout)
  $DC -f "$COMPOSE_PATH" exec -T broker bash -lc "$CMD"
else
  echo "Consuming from 'tweets' for ${DURATION}s... (Ctrl+C to stop early)"
  # if timeout is missing (e.g., macOS), users can Ctrl+C instead
  if command -v timeout >/dev/null 2>&1; then
    timeout "${DURATION}" $DC -f "$COMPOSE_PATH" exec -T broker bash -lc "$CMD" || true
  else
    echo "Note: 'timeout' not found. Streaming until you Ctrl+C."
    $DC -f "$COMPOSE_PATH" exec -T broker bash -lc "$CMD"
  fi
fi
