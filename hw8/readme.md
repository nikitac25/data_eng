## Setup Instructions

1. **Create a `.env` file** in the `hw2` directory with the following variables:

    ```env

    MYSQL_USER=        # insert_your_username
    MYSQL_PASSWORD=    # insert_your_password
    MYSQL_DATABASE=assessment_db
    MYSQL_HOST=host.docker.internal
    ```

2. **(Optional)**: Replace the CSV files in the `datasources` folder with full datasets.  
   The repository includes only small sample files for demonstration.

3. Run docker-compose build and wait till the end of the building process
4. Run command bash run_kafka.sh and wait when container is ready
5. Run docker-compose up message-producer

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


6. **Verify the topic contents using the Kafka console client** *(requirement #3)*:

    ```bash
    docker-compose exec kafka bash -lc '/opt/bitnami/kafka/bin/kafka-console-consumer.sh \
      --bootstrap-server kafka:9092 \
      --topic tweets \
      --from-beginning \
      --property print.timestamp=true \
      --property print.key=true'
    ```
