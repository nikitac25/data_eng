import json, time, requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import constants

URL = constants.WIKIPEDIA_ENDPOINT
TOPIC = constants.KAFKA_TOPIC
BOOTSTRAP = constants.BOOTSTRAP_SERVERS
ALLOWED = {"en.wikipedia.org", "www.wikidata.org", "commons.wikimedia.org"}

# connect to kafka (quick retry loop)
producer = None
for i in range(30):
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        break
    except NoBrokersAvailable:
        time.sleep(2)
if not producer:
    raise RuntimeError("Kafka not available")

print(f"stream: {URL}")
print(f"topic:  {TOPIC}")

resp = requests.get(URL, stream=True)
for line in resp.iter_lines(decode_unicode=True):
    if not line or not line.startswith("data: "):
        continue
    try:
        event = json.loads(line[6:])
        domain = event.get("meta", {}).get("domain")
        perf = event.get("performer", {}) or {}
        if domain in ALLOWED and not perf.get("user_is_bot", False):
            msg = {
                "user_id": perf.get("user_id"),
                "domain": domain,
                "created_at": event.get("meta", {}).get("dt"),
                "page_title": event.get("page_title"),
            }
            producer.send(TOPIC, msg)
            print(f"{domain} -> {msg['page_title']}")
    except json.JSONDecodeError:
        continue
