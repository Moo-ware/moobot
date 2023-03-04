from threading import Thread
from utils.functions import GetWaitlist
import time

class marketwatch():
    def __init__(self):
        self.queue = {}
    
    def queueWatcher(self):
        while True:
            self.queue = GetWaitlist()
            time.sleep(25)


# Threads the marketwatcher instance
mpwatcher = marketwatch()
Thread(target=mpwatcher.queueWatcher).start()