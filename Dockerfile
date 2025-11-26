FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Команда запуска: через gunicorn (prod-режим)
# 'app:create_app()' мы ещё реализуем, либо можно сделать просто 'run:app'
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
