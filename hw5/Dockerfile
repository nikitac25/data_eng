FROM python:3.11-slim

WORKDIR /scripts

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/python/ .

CMD ["sh", "-c", "\
    python locations.py /data/users.csv /data/campaigns.csv /data/ad_events.csv && \
    python advertisers.py /data/campaigns.csv && \
    python users.py /data/users.csv && \
    python campaigns.py /data/campaigns.csv && \
    python impressions.py /data/ad_events.csv && \
    python clicks.py /data/ad_events.csv \
"]