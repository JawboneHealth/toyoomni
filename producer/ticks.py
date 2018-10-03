from uuid import uuid4
import datetime as dt
from confluent_kafka import Producer
import os, signal, sys
import json
from time import sleep, time

keep_running = True
def stop_running(signal_number, _):
    print "Stopping..."
    global keep_running
    keep_running= False


def main():
    signal.signal(signal.SIGINT, stop_running)

    broker = os.environ.get('KAFKA_BROKER', 'kafka:9092')
    topic = os.environ.get('KAFKA_TOPIC', 'ticks')

    producer = Producer({'bootstrap.servers': broker})

    global keep_running

    while keep_running:
        message_id = uuid4()
        created = time()
        created_dt = dt.datetime.fromtimestamp(created)

        print "Sending the ticks for {}".format(message_id)
        message = {'message_id' : str(message_id),
                   'created_date': created_dt.strftime("%Y-%m-%d %H:%M:%S.%f"),
                   'created': created}

        producer.produce(topic, value=json.dumps(message))
        print 'Sent: ' + json.dumps(message)
        sleep(0.3)
        print
        sys.stdout.flush()

    print "Clean shutdown"
    sys.stdout.flush()


if __name__ == "__main__":
    main()