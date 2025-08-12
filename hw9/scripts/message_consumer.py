import os
import json
from datetime import datetime
import pandas as pd
from kafka import KafkaConsumer

BOOTSTRAP = os.getenv("KAFKA_BROKER")
TOPIC = os.getenv("KAFKA_TOPIC")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))

COLUMNS = ["author_id", "created_at", "text"]


def open_consumer():
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id="tweet-group",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
    )


def file_for_minute(dt):
    return os.path.join(OUTPUT_DIR, f"tweets_{dt.strftime('%d_%m_%Y_%H_%M')}.csv")


def flush(buffer, path):
    if not buffer:
        return
    df = pd.DataFrame(buffer, columns=COLUMNS)
    write_header = not os.path.exists(path)
    df.to_csv(path, mode="a", header=write_header, index=False)
    buffer.clear()


def consume():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    consumer = open_consumer()
    print(f"consume -> topic='{TOPIC}' bootstrap='{BOOTSTRAP}' out='{OUTPUT_DIR}'")

    current_min = None
    current_path = None
    buffer = []

    try:
        for msg in consumer:
            rec = msg.value or {}
            created_at = rec.get("created_at") or datetime.now().isoformat()
            try:
                dt = datetime.fromisoformat(created_at)
            except Exception:
                # if created_at is weird, use now but keep original in the row
                dt = datetime.now()

            min_key = dt.strftime("%d_%m_%Y_%H_%M")
            if current_min is None:
                current_min = min_key
                current_path = file_for_minute(dt)

            if min_key != current_min:
                flush(buffer, current_path)
                current_min = min_key
                current_path = file_for_minute(dt)

            row = {
                "author_id": rec.get("author_id", ""),
                "created_at": created_at,
                "text": rec.get("text", ""),
            }
            buffer.append(row)

            if len(buffer) >= BATCH_SIZE:
                flush(buffer, current_path)

            print(f"received: {rec.get('tweet_id', '')} | {created_at}")
            consumer.commit()
    except KeyboardInterrupt:
        pass
    finally:
        flush(buffer, current_path or file_for_minute(datetime.now()))
        try:
            consumer.close()
        except Exception:
            pass


if __name__ == "__main__":
    consume()
