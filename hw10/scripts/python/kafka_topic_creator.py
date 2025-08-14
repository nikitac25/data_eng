import time
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
import constants

BOOTSTRAP = constants.BOOTSTRAP_SERVERS
TOPIC = constants.KAFKA_TOPIC

# connect to kafka (quick retry loop)
admin = None
for _ in range(30):
    try:
        admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP)
        break
    except NoBrokersAvailable:
        time.sleep(2)
if not admin:
    raise RuntimeError("Kafka not available")

try:
    admin.create_topics([NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)])
    print(f"topic created: {TOPIC}")
except TopicAlreadyExistsError:
    print(f"topic exists: {TOPIC}")
finally:
    admin.close()
