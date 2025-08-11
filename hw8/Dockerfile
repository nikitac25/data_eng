#   docker build --build-arg PY_BASE=python:3.11 -t homework8/tweet-writer:latest .
ARG PY_BASE=python:3.11-slim
FROM ${PY_BASE}

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data ./data
COPY .env.example ./.env

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "src.producer"]