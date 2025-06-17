docker run -it --rm \
  -v "$(pwd)/scripts:/app" \
  -v "$(pwd)/datasources:/data" \
  -w /app \
  python:3.11 \
  bash -c "pip install pandas mysql-connector-python && \
           python locations.py /data/users.csv /data/campaigns.csv /data/ad_events.csv && \
           python advertisers.py /data/campaigns.csv && \
           python users.py /data/users.csv && \
           python campaigns.py /data/campaigns.csv && \
           python impressions.py /data/ad_events.csv && \
           python clicks.py /data/ad_events.csv"
