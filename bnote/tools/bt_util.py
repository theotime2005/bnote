"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


import os
import shlex
import subprocess
import threading

# Setup the logger for this file
from debug.colored_log import ColoredLogger, BT_UTIL_LOG
log = ColoredLogger(__name__)
log.setLevel(BT_UTIL_LOG)


class FindComputersThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = False
        self.paired_devices = dict()

    def is_running(self):
        return self.__running

    def terminate(self):
        self.__running = False

    def run(self) -> None:
        self.__running = True
        log.info("FindComputersThread running...")

        paired_devices = dict()
        x = subprocess.Popen(["bluetoothctl", "paired-devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # while self.__running:
        x.wait()
        # self.__running = False

        raw_paired_devices = x.stdout.read().decode("utf-8")
        log.debug("bluetoothctl paired-devices =>{}".format(raw_paired_devices))
        err = x.stderr.read().decode("utf-8")
        if err != "":
            log.warning("bluetoothctl paired-devices : error={}".format(err))

        lines_paired_devices = raw_paired_devices.split("\n")
        for device in lines_paired_devices:
            log.debug("device={}".format(device))
            device = device.replace("Device ", "")
            if len(device.split(" ")) >= 2:
                paired_devices[device.split(" ")[0]] = " ".join(device.split(" ")[1:])

        log.debug("paired_devices={}".format(paired_devices))
        self.paired_devices = paired_devices

        self.__running = False


def set_discoverable(discoverable=True):
    if discoverable:
        os.popen('sudo bluetoothctl discoverable on')
    else:
        os.popen('sudo bluetoothctl discoverable off')


def bluetooth_pretty_host_name():
    args = shlex.split("hostnamectl --pretty")
    x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    x.wait()
    return x.stdout.read().decode("utf-8").strip("\n")


def set_bluetooth_pretty_host_name(name):
    # Change le pretty hostname
    os.popen("sudo hostnamectl set-hostname \"{}\" --pretty".format(name))


# device is the mac adresse of the bluetooth device to remove.
def remove_paired_device(device):
    args = shlex.split("sudo bluetoothctl remove {}".format(device))
    x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    x.wait()
    result = x.stdout.read().decode("utf-8")
    # if result.find("Device has been removed") == -1:
    log.info("{} returns {}".format(args, result))


# Return a dict with "MAC address":"Adaptator's name".
def get_paired_devices():
    find_computers_thread = FindComputersThread()
    find_computers_thread.start()

    # Wait the computers list to be constructed...
    find_computers_thread.join(20)

    # Get the paired_devices
    return find_computers_thread.paired_devices
