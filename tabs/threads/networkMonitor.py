import threading
import time


class NetworkMonitorThread(threading.Thread):
    def __init__(self, interval=1, *update_functions):
        super().__init__()
        self.update_functions = list(update_functions)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            for update_function in self.update_functions:
                update_function()

    def stop(self):
        self._stop_event.set()
