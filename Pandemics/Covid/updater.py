from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.schedulers.base as base
from .tasks import *


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(write_world_daily, 'interval', minutes=60)
    scheduler.start()
    print("scheduling started")



