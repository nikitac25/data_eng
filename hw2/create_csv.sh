docker run -it --rm \
  --env-file .env \
  -v "$(pwd)/scripts:/app" \
  -v "$(pwd)/sql:/sql" \
  -v "$(pwd)/output:/output" \
  -w /app \
  python:3.11 \
  bash -c "pip install pandas mysql-connector-python python-dotenv && \
           python csv_output.py"
