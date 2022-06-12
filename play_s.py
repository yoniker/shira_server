import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def print_something():
    print('something!')

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_something, trigger="interval", seconds=10)
scheduler.start()


while True:
    time.sleep(1000)