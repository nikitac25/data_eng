## Setup Instructions

1. **Create a `.env` file** in the `hw2` directory with the following variables:

    ```env
    MYSQL_USER=yourusername
    MYSQL_PASSWORD=yourpassword
    MYSQL_DATABASE=assessment_db
    MYSQL_HOST=host.docker.internal
    ```

2. **Run the following commands** to set up MySQL, load the data and upload outputs:

    ```bash
    bash start_mysql.sh
    bash insert_data.sh
    bash create_csv.sh
    ```
