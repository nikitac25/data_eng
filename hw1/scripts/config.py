import os

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("ADMIN_USER"),
    "password": os.getenv("ADMIN_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}
