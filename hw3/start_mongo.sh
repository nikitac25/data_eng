#!/bin/bash

if ! command -v dos2unix >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y dos2unix
fi
dos2unix .env 2>/dev/null

set -a
source .env
set +a

mkdir -p hw_3_mongo
cd hw_3_mongo || exit

docker run -d \
  --name mongo-db \
  -v "$(pwd)/../mongo_scripts:/mongo_scripts" \
  -e MONGO_INITDB_ROOT_USERNAME="$MONGO_ROOT_USER" \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_ROOT_PASSWORD" \
  -p 27017:27017 \
  mongo:8

sleep 15

docker exec -i mongo-db mongosh \
  -u "$MONGO_ROOT_USER" -p "$MONGO_ROOT_PASSWORD" \
  --authenticationDatabase admin \
  "$MONGO_DB" /mongo_scripts/user_ad_interactions.js

docker exec -i mongo-db mongosh \
  -u "$MONGO_ROOT_USER" -p "$MONGO_ROOT_PASSWORD" \
  --authenticationDatabase admin \
  "$MONGO_DB" /mongo_scripts/sessions.js
