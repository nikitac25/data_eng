docker run -it --rm \
  -v "$(pwd)/python:/app" \
  -v "$(pwd)/datasources:/data" \
  -w /app \
  python:3.11 \
  bash -c "pip install pandas mysql-connector-python && \
           python users.py /data/users.csv && \
           python advertisers.py /data/campaigns.csv && \
           python campaigns.py /data/campaigns.csv && \
           python impressions.py /data/ad_events.csv && \
           python clicks.py /data/ad_events.csv"
