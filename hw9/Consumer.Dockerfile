FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "/"

COPY scripts/message_consumer.py .

RUN mkdir -p /app/output_archive

CMD ["python", "message_consumer.py"]
