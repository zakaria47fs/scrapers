import schedule 
import time
from datetime import datetime


def run_main():
    exec(open("run_walmart.py").read())

schedule.every().day.at('00:00').do(run_main)

while 1:
    schedule.run_pending()
    time.sleep(1)
