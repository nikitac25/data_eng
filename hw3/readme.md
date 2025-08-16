In development process

## Setup Instructions

1. **Create a `.env` file** in the `hw3` directory with the following variables:

    ```env
   MONGO_USER=
   MONGO_PASSWORD=
   MONGO_DB=assessment_db
   MONGO_PORT=27017:27017
   MONGO_HOST=mongodb
   SESSION_GAP_MINUTES: 30
    ```

2. **Prepare the CSV data file**:
    - Place your input CSV file in the `datasources` folder.
    - The repository includes a small sample file for demonstration.

3. **Build containers**:

    ```bash
    docker-compose up -d
    ```
