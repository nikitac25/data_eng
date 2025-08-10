import os

MONGO_CONFIG = {
    "host": os.getenv("MONGO_HOST"),
    "port": os.getenv("MONGO_PORT"),
    "username": os.getenv("MONGO_ROOT_USER"),
    "password": os.getenv("MONGO_ROOT_PASSWORD"),
    "database": os.getenv("MONGO_DB")
}