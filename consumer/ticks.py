import datetime as dt
from confluent_kafka import Consumer, KafkaError
import os
import json
from time import sleep
import signal
import sys
from celery import Celery

app = Celery('tick_worker', broker='redis://message-broker:6379/0')

keep_running = True


def stop_running(signal_number, _):
    print "Stopping..."
    global keep_running
    keep_running= False


def main():
    signal.signal(signal.SIGINT, stop_running)

    app.conf.task_routes = {'tick_worker.process_ticks': {'queue': 'tick_processors'}}
    task = app.signature('tick_worker.process_ticks')

    broker = os.environ.get('KAFKA_BROKER', 'kafka:9092')
    topic = os.environ.get('KAFKA_TOPIC', 'ticks')

    consumer = Consumer({'bootstrap.servers': broker,
                         'group.id': 'tick_consumer',
                         'enable.auto.commit': False,
                         'default.topic.config': {
                             'auto.offset.reset': 'smallest'}
                         })

    consumer.subscribe([topic])

    global keep_running
    while keep_running:
        print "Waiting..."
        sys.stdout.flush()
        msg = consumer.poll(5)
        print "Checking the hook..."
        sys.stdout.flush()

        if msg is None:
            print "We got nuttin"
            sys.stdout.flush()
            continue

        if msg.error():
            print "Oh, we got an error"
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print "Found partition EOF"
                print msg.value()
                sys.stdout.flush()
                continue
            else:
                print "And it's a bad error"
                print msg.error()
                sys.stdout.flush()
                break

        print "We got a message!"
        sys.stdout.flush()
        message = json.loads(msg.value())
        message_id = message['message_id']

        #Simulate an exception that kills the consumer
        # if random.random() < 0.1:
        #     print "Oops!  Something threw an execption!  (it was us)"
        #     print message_id
        #     print
        #     sys.stdout.flush()
        #     raise Exception('Generic general exception of doom')
        # elif random.random() < 0.1:
        #     print "For no good reason, we're going to re-process this message later"
        #     print message_id
        #     print
        #     sys.stdout.flush()
        #     continue

        task.delay(message)
        #process_ticks.delay(message)
        print 'Successfully handled message {}'.format(message_id)
        consumer.commit(msg)
        print
        sys.stdout.flush()
        sleep(1)

    consumer.close()
    print "Exiting cleanly"
    exit(0)

if __name__ == "__main__":
    main()