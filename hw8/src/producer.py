import argparse
import json
import logging
import os
import signal
from datetime import datetime, timezone
from typing import Optional

from kafka import KafkaProducer
from dotenv import load_dotenv

from io_utils import read_csv_as_dicts, pick_timestamp_field, serialize_record
from rate import PaceController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
)
log = logging.getLogger("tweet-writer")

shutdown = False
def _handle_sigterm(signum, frame):
    global shutdown
    shutdown = True
    log.info("Received signal %s, shutting down gracefully...", signum)

signal.signal(signal.SIGTERM, _handle_sigterm)
signal.signal(signal.SIGINT, _handle_sigterm)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_producer(broker: str, client_id: Optional[str] = None) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[broker],
        acks="all",
        client_id=client_id or "homework8-writer",
        linger_ms=50,
        value_serializer=lambda v: v,  # already bytes
        key_serializer=lambda k: k.encode("utf-8") if k is not None else None,
        retries=5,
        max_in_flight_requests_per_connection=5,
    )

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Stream CSV tweets into Kafka as JSON.")
    parser.add_argument("--broker", default=os.getenv("KAFKA_BROKER", "localhost:9092"))
    parser.add_argument("--topic", default=os.getenv("KAFKA_TOPIC", "tweets"))
    parser.add_argument("--input", default=os.getenv("INPUT_FILE", "data/sample.csv"))
    parser.add_argument("--rate", type=int, default=int(os.getenv("RATE_PER_SEC", "12")))
    parser.add_argument("--key-column", default=os.getenv("KEY_COLUMN", None),
                        help="Optional CSV column to use as Kafka message key.")
    args = parser.parse_args()

    log.info("Starting producer to broker=%s topic=%s input=%s rate=%s/s",
             args.broker, args.topic, args.input, args.rate)

    pc = PaceController(args.rate)
    producer = build_producer(args.broker, os.getenv("CLIENT_ID"))

    # Peek first row to decide timestamp field
    rows = read_csv_as_dicts(args.input)
    first_row = None
    buffer = []
    for row in rows:
        first_row = row
        buffer.append(row)
        break

    if first_row is None:
        log.error("Input file is empty: %s", args.input)
        return 2

    ts_field = pick_timestamp_field(first_row) or "timestamp"
    log.info("Using '%s' as timestamp field (will be overwritten).", ts_field)

    # Process first row plus the rest
    def _iter_rows():
        yield first_row
        for r in read_csv_as_dicts(args.input):
            yield r

    sent = 0
    for row in _iter_rows():
        if shutdown:
            break
        # Overwrite or add timestamp
        row[ts_field] = now_iso()
        key = str(row.get(args.key_column)) if args.key_column and args.key_column in row else None
        try:
            producer.send(args.topic, value=serialize_record(row), key=key)
            sent += 1
            if sent % 100 == 0:
                log.info("Sent %d messages", sent)
        except Exception as e:
            log.exception("Send failed: %s", e)
        pc.sleep_next()

    log.info("Flushing producer...")
    producer.flush(10)
    log.info("Done. Sent %d messages.", sent)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
