In development process

## Setup Instructions

1. **Create a `.env` file** in the `hw9` directory with the following variables:

    ```env
    KAFKA_BROKER=kafka:9092
    KAFKA_TOPIC=tweets
    INPUT_CSV=/app/datasources/sample.csv
    RATE_PER_SEC=10
    CLIENT_ID=homework9-writer
    OUTPUT_DIR=/app/archive
    BATCH_SIZE=10
    ```

2. **Prepare the CSV data file**:
    - Place your input CSV file in the `datasources` folder.
    - The repository includes a small sample file for demonstration.

3. **Build containers**:

    ```bash
    docker compose build
    ```

4. **Start Kafka services and create the topic**:

    ```bash
    bash run_kafka.sh
    ```

5. **Run the consumer** :

    ```bash
    docker compose up message-consumer
    ```

6. **Run the producer**:

    ```bash
    docker compose up message-producer
    ```


7. **Check csv outputs**:
      ```bash
      ls output_archive
      ```