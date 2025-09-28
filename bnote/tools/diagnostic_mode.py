import time
import threading
from math import trunc

from bnote.apps.fman.file_manager import BNOTE_FOLDER
from bnote.stm32.braille_device_characteristics import braille_device_characteristics


class DiagnosticMode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_active = False
        self.data = []
        self.file = "{}/diagnostic_mode.txt".format(BNOTE_FOLDER)
        self.waiting_time = 60

    def get_capacity(self):
        return braille_device_characteristics.get_battery_remaining_capacity()

    def get_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def get_status(self):
        self.data.append({"time": self.get_time(), "capacity": self.get_capacity()})

    def run(self):
        print("Starting diagnostic mode...")
        self.is_active = True
        while self.is_active:
            self.get_status()
            time.sleep(self.waiting_time)

    def write_data(self):
        file = open(self.file, "a", encoding="utf-8")
        for d in self.data:
            file.write("{} - {}\n".format(d["time"], d["capacity"]))
        file.close()

    def stop(self):
        self.is_active = False
        self.write_data()
        print("Stopping diagnostic mode...")
