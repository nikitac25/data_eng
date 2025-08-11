FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data ./data
COPY .env.example ./.env

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.local/bin:${PATH}"

# Entrypoint uses env vars or args
ENTRYPOINT ["python", "-m", "src.producer"]
