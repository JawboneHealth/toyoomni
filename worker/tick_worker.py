from celery import Celery
from time import sleep, time
import sys
import random

app = Celery('tick_worker', broker='redis://message-broker:6379/0')


#@app.task()
@app.task(bind=True, retry_limit=3, default_retry_delay=3)
def process_ticks(self, ticks):
    success = random.randint(0,1) > 0
    print "Processing ticks!!"
    mid = ticks.get('message_id', 'missing id')
    #logger.debug("Working on message {}".format(mid))
    print "Working on message {}".format(mid)
    sys.stdout.flush()
    sleep(2)
    start = ticks.get('created', 0)
    end = time()
    duration = end - start
    if not success:
        print "For some reason we failed."
        sys.stdout.flush()
        self.retry()
    elif duration == end:
        #logger.debug("Could not calculate duration")
        print "Could not calculate duration"
        self.retry()
        sys.stdout.flush()
    else:
        #logger.debug("Completed {}.  Took {}s".format(mid, duration))
        print "Completed {}.  Took {}s".format(mid, duration)
        sys.stdout.flush()


