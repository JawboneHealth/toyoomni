FROM python:2.7.15-slim-stretch

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install celery ipython redis && \
    mkdir /app

WORKDIR /app

COPY tick_worker.py .

CMD ["/usr/local/bin/celery", "-A", "tick_worker", "-Q", "tick_processors", "worker", "--loglevel=info"]
