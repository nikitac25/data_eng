## Setup Instructions

1. **Create a `.env` file** in the `hw2` directory by the following template:

    ```env

    MYSQL_ROOT_PASSWORD= #insert_root_password
    ADMIN_USER= #insert_user_name
    ADMIN_PASSWORD= #insert_password
    MYSQL_DATABASE= #insert_database_name
    MYSQL_HOST=host.docker.internal
    ```

2. **(Optional)**: Replace the CSV files in the `datasources` folder with full datasets.  
   The repository includes only small sample files for demonstration.

3. **Run the following commands** to set up MySQL and load the data:

    ```bash
    bash start_mysql.sh
    bash insert_data.sh