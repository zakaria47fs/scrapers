import schedule 
import time
from datetime import datetime


def run_main():
    exec(open("main.py").read())

schedule.every(1).seconds.do(run_main)

while 1:
    schedule.run_pending()
    time.sleep(1)
