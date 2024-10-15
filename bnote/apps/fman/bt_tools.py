"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


import bluetooth
from enum import Enum
import re
import shlex
import subprocess
import time

# Sur PC
# sudo apt-get install libbluetooth-dev
# pip install PyBluez

# sur Rpi
# pi@raspberrypi:~$ sudo apt-get install libbluetooth-dev
# pi@raspberrypi:~$ sudo pip3.8 install PyBluez

# Setup the logger for this file
from debug.colored_log import ColoredLogger, BT_TOOLS_LOG
log = ColoredLogger(__name__)
log.setLevel(BT_TOOLS_LOG)


# https://www.bluetooth.com/specifications/assigned-numbers/Baseband/
class MajorServiceClass(Enum):
    Positioning = 0x00010000
    Networking = 0x00020000
    Rendering = 0x00040000
    Capturing = 0x00080000
    ObjectTransfer = 0x00100000
    Audio = 0x00200000
    Telephony = 0x00400000
    Information = 0x00800000


class MajorDeviceClass(Enum):
    Miscellaneous = 0x00000000
    Computer = 0x00000100
    Phone = 0x00000200
    AccessPoint = 0x00000300
    AudioVideo = 0x00000400
    Peripheral = 0x00000500
    Imaging = 0x00000600
    Wearable = 0x00000700
    Toy = 0x00000800
    Health = 0x00000900
    Uncategorized = 0x00001F00


class MinorDeviceForPhone(Enum):
    Uncategorized = 0x00000000
    Cellular = 0x00000004
    Cordless = 0x00000008
    Smartphone = 0x0000000d
    WiredModem = 0x00000010
    IsdnAccess = 0x00000014


class MinorDeviceForComputer(Enum):
    Uncategorized = 0x00000000
    Desktop = 0x00000004
    Server = 0x00000008
    Laptop = 0x0000000d
    HandledPc = 0x00000010
    PalmSizePc = 0x00000014
    WearableComputer = 0x00000018
    Tablet = 0x0000001d


class BtDevices:
    class BtDeviceIterator:
        def __init__(self, bt_devices):
            self.current = 0
            self._bt_devices = bt_devices

        def __iter__(self):
            return self

        def __next__(self):
            if self.current >= len(self._bt_devices):
                raise StopIteration
            ret = self._bt_devices.get_at(self.current)
            self.current += 1
            return ret

    def __init__(self):
        self.devices = []
        self.refresh_list()

    def __iter__(self):
        return BtDevices.BtDeviceIterator(self)

    def __len__(self):
        return len(self.devices)

    def get_at(self, index):
        if index in range(len(self.devices)):
            return self.devices[index]

    def refresh_list(self):
        self.devices = []
        devs = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
        print(f"devs={devs}")
        for dev in devs:
            print(f"dev={dev}")
            addr = dev[0]
            name = dev[1]
            device_class = dev[2]
            opush_channel = BtDevices.find_opush_channel(addr)
            bt_device = BtDevice(addr, name, device_class, opush_channel)
            self.devices.append(bt_device)

    # Remarque : Il faut que le PC sous W10 soit en mode réception de fichier Bluetooth
    # pour que le service OPUSH soit trouvé. (donc passer en réception fichier avant d'appeler find_opush_channel)
    @classmethod
    def find_opush_channel(cls, addr):
        command_line = "sdptool search --bdaddr {} OPUSH".format(addr)
        args = shlex.split(command_line)
        x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        x.wait()
        sdptool_results = x.stdout.read().decode("utf-8")

        pattern = re.compile('\"RFCOMM\" \(0x0003\)\n    Channel: (\d+)')
        search = pattern.search(sdptool_results)
        if search is not None:
            return int(search.group(1))


class BtDevice:
    def __init__(self, addr, name, device_class, opush_channel):
        self.addr = addr
        self.name = name
        self.device_class = device_class
        self.opush_channel = opush_channel

    def is_computer(self):
        return bool(self.device_class & MajorDeviceClass.Computer.value)

    def is_phone(self):
        return bool(self.device_class & MajorDeviceClass.Phone.value)

    def is_object_transfer_capable(self):
        return bool(self.device_class & MajorServiceClass.ObjectTransfer.value)


def discover_devices(lookup_names=True, lookup_class=True):
    return bluetooth.discover_devices(duration=20, lookup_names=lookup_names, lookup_class=lookup_class)
