FROM python:3.13.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
 && rm -rf /var/lib/apt/lists/*

COPY requirements /requirements

RUN pip install --upgrade pip && \
    pip install -r /requirements/development.txt

COPY . /app

RUN chmod +x /app/compose/development/start

WORKDIR /app/core
