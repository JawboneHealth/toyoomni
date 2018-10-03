FROM python:2-alpine3.6

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache curl make bash g++

#
# Install Kafka library
#
RUN curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf - && \
    cd librdkafka-0.9.2-RC1/ && \
    ./configure --prefix=/usr && \
    make -j && \
    make install && \
    cd .. && \
    rm -r librdkafka-0.9.2-RC1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ticks.py .

ENV KAFKA_PRODUCER_TEST_BROKER=kafka:9092
ENV KAFKA_PRODUCER_TEST_TOPIC=ticks

CMD ["/usr/local/bin/python", "ticks.py"]
