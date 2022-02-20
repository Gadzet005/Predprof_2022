# Для обновления значения ИПЦ

import schedule
import time
from threading import Thread
from .utils import CPI
from django.conf import settings

# Поток
class MyThread(Thread):
    def __init__(self, function, args: dict = None):
        Thread.__init__(self)
        self.function = function
        if args is None:
            args = {}
        self.args = args

    def run(self):
        """Запуск параллельного потока"""
        self.function(**self.args)

def time_manager():
    schedule.every().day.at("03:00").do(update_func)
    while True:
        schedule.run_pending()
        time.sleep(3600)

def update_func():
    CPI.updateCPI()

# Мешает при разработке, так что включено только при нормальной работе
if not settings.DEBUG:
    TimeManager = MyThread(time_manager)
    TimeManager.start()
