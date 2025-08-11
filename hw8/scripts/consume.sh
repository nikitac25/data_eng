#!/usr/bin/env bash
set -euo pipefail
DURATION="${1:-30}"
echo "Consuming from 'tweets' for ${DURATION}s... (Ctrl+C to stop)"
timeout "${DURATION}" docker exec -it broker bash -lc 'kafka-console-consumer.sh --bootstrap-server broker:9092 --topic tweets --from-beginning --property print.key=true --property print.timestamp=true' || true
