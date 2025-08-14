## Setup Instructions

1. **Create a `.env` file** in the `hw10` directory using the example provided below. Save it as `hw10/.env`:

    ```env
    # Zookeeper
    ALLOW_ANONYMOUS_LOGIN=yes
    # Kafka
    ALLOW_PLAINTEXT_LISTENER=yes
    KAFKA_CFG_NODE_ID=0
    KAFKA_CFG_PROCESS_ROLES=controller,broker
    KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
    KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
    KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
    KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
    BOOTSTRAP_SERVERS=kafka:9092
    KAFKA_TOPIC=page_events
    # Cassandra
    CASSANDRA_CLUSTER_NAME=wikipedia_cluster
    CASSANDRA_DATACENTER=wikipedia_datacenter
    CASSANDRA_KEYSPACE=wikipedia
    CASSANDRA_HOST=cassandra
    CASSANDRA_PORT=9042
    CASSANDRA_TABLE=wiki_snippet
    # Producer
    WIKIPEDIA_ENDPOINT=https://stream.wikimedia.org/v2/stream/page-create
    # Spark
    SPARK_MASTER_URL=spark://spark:7077
    ```

2. **Run the stack** using the simple runner script, or run the same commands manually:
      ```bash
      bash runner.sh
      ```