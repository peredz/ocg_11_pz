import time
import schedule
from bot import send_mailings


def f():
    schedule.every().hour.at(":00").do(send_mailings)

    while True:
        schedule.run_pending()
        time.sleep(1)