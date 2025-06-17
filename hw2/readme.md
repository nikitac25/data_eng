## Setup Instructions

1. **Create a `.env` file** in the `hw2` directory with the following variables:

    ```env
    MYSQL_USER=replace_with_your_username
    MYSQL_PASSWORD=replace_with_your_password
    MYSQL_DATABASE=assessment_db
    MYSQL_HOST=host.docker.internal
    ```

2. **(Optional)**: Replace the CSV files in the `datasources` folder with full datasets.  
   The repository includes only small sample files for demonstration.

3. **Run the following commands** to set up MySQL and load the data:

    ```bash
    bash start_mysql.sh
    bash insert_data.sh
    bash create_csv.sh
    ```
