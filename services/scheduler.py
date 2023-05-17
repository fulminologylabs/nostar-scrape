import schedule
import time as tm
from datetime import time, timedelta, datetime

def job():
    print("TEST SCRAPE JOB")

# Run job every day at specific HH:MM and next HH:MM:SS
schedule.every().days.at("11:30:00").do(job)

while True:
    schedule.run_pending()
    tm.sleep(1)
    #schedule.cancel_job()
    