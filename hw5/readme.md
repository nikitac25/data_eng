In development process

## Setup Instructions

1. **Create a `.env` file** in the `hw5` directory with the following variables:

    ```env
   MYSQL_DATABASE=
   MYSQL_ROOT_PASSWORD=
   ADMIN_USER=a
   ADMIN_PASSWORD=
   MYSQL_HOST=mysqldb
    ```

2. **Prepare the CSV data file**:
    - Place your input CSV file in the `datasources` folder.
    - The repository includes a small sample file for demonstration.

3. **Build containers**:

    ```bash
    docker-compose up -d
    ```
