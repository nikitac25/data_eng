import csv
import json
import os
import time
from datetime import datetime
from kafka import KafkaProducer

BOOTSTRAP = os.getenv("KAFKA_BROKER")
TOPIC = os.getenv("KAFKA_TOPIC")
INPUT_CSV = os.getenv("INPUT_CSV")
RATE = float(os.getenv("RATE_PER_SEC"))

def now_iso() -> str:
    return datetime.now().isoformat()

def open_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        key_serializer=lambda s: s.encode("utf-8") if s is not None else None,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
        acks="all",
        retries=3,
        compression_type="gzip",
    )

def stream():
    if not os.path.exists(INPUT_CSV):
        print(f"input not found: {INPUT_CSV}")
        return

    delay = 1.0 / max(1.0, RATE)
    sent = 0

    producer = open_producer()
    print(f"stream -> topic='{TOPIC}' bootstrap='{BOOTSTRAP}' rate={RATE}/s file='{INPUT_CSV}'")

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = time.time()

            # skip empty texts (dataset-specific, safe no-op otherwise)
            if not (row.get("text") or "").strip():
                continue

            # overwrite timestamp
            row["created_at"] = now_iso()

            # build key (author_id if present)
            key = row.get("author_id")
            try:
                # send & wait a bit so we know it actually went out
                producer.send(TOPIC, key=key, value=row).get(timeout=10)
                sent += 1
                print(f"produced: {row.get('tweet_id', '')} | {row['created_at']}")
            except Exception as e:
                print(f"send error: {e}")

            # simple pacing
            elapsed = time.time() - start
            sleep_for = delay - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    producer.flush()
    producer.close()
    print(f"done. sent={sent}")

if __name__ == "__main__":
    stream()
