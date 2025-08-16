## Setup Instructions

1. **Create a `.env` file** in the `hw2` directory by the following template:

    ```env

    MYSQL_ROOT_PASSWORD=
    ADMIN_USER=
    ADMIN_PASSWORD=
    MYSQL_DATABASE=
    MYSQL_HOST=host.docker.internal
    ```

2. **(Optional)**: Replace the CSV files in the `datasources` folder with full datasets.  
   The repository includes only small sample files for demonstration.

3. **Run the following commands** to set up MySQL and load the data:

    ```bash
    bash start_mysql.sh
    bash insert_data.sh