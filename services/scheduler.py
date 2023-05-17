import time
import queue
import threading
from schedule import every, repeat, run_pending
# Inspo reference: https://schedule.readthedocs.io/en/stable/parallel-execution.html
# TODO Consider error handling here

JOB_BATCH_INTERVAL = 30 # minutes

# TODO This should be replaced with a Proces factory
# that returns a Daily or Bulk Process object depending on
# the tasks loaded from the DB to the job queue
def job():
    print("Im working.")

job_queue = queue.Queue()

def worker():
    while True:
        job_func = job_queue.get()
        job_func()
        job_queue.task_done()

worker_thread = threading.Thread(target=worker)
worker_thread.start()

@repeat(every(JOB_BATCH_INTERVAL).minutes)
def load_batch():
    # TODO Add jobs to jobqueue from DB
    pass

while True:
    run_pending()
    time.sleep(1)
