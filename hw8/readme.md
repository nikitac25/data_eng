## Setup Instructions

1. **Create a `.env` file** in the `hw8` directory with the following variables:

    ```env
    KAFKA_BROKER=kafka:9092
    KAFKA_TOPIC=tweets
    INPUT_CSV=/app/datasources/sample.csv
    RATE_PER_SEC=10
    CLIENT_ID=homework8-writer
    ```


2. **Prepare the CSV data file**:
    - Upload CSV in the `datasources` folder. 
   (The repository includes only small sample files for demonstration)

3. **Build containers**:

    ```bash
    docker-compose build
    ```

4. **Start Kafka services and create the topic**:

    ```bash
    bash run_kafka.sh
    ```

5. **Run the message producer**:

    ```bash
    docker-compose up message-producer
    ```


6. **Verify the topic contents using the Kafka console client**:

    ```bash
    docker-compose exec kafka bash -lc '/opt/bitnami/kafka/bin/kafka-console-consumer.sh \
      --bootstrap-server kafka:9092 \
      --topic tweets \
      --from-beginning \
      --property print.timestamp=true \
      --property print.key=true'
    ```
