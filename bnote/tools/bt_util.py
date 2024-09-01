"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import shlex
import subprocess
import threading
import re
from enum import Enum

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, BT_UTIL_LOG

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
        x = subprocess.Popen(["bluetoothctl", "devices", "Paired"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # while self.__running:
        x.wait()
        # self.__running = False
        raw_paired_devices = x.stdout.read().decode("utf-8")
        log.debug("bluetoothctl Paired =>{}".format(raw_paired_devices))
        err = x.stderr.read().decode("utf-8")
        if err != "":
            log.error("bluetoothctl Paired : error={}".format(err))
        lines_paired_devices = raw_paired_devices.split("\n")
        for device in lines_paired_devices:
            log.info("device={}".format(device))
            device = device.replace("Device ", "")
            if len(device.split(" ")) >= 2:
                paired_devices[device.split(" ")[0]] = " ".join(device.split(" ")[1:])
            # Just for test device class acquisition.
            # get_device_class(device.split(" ")[0])
        log.info("paired_devices={}".format(paired_devices))
        self.paired_devices = paired_devices
        self.__running = False


def set_discoverable(discoverable=True):
    if discoverable:
        os.popen('bluetoothctl discoverable on')
    else:
        os.popen('bluetoothctl discoverable off')


def bluetooth_on_off(on=None):
    """
            Bluetooth on/off function.
            no param : return bluetooth state
            on : True to activate Bluetooth device, False to deactivate.
            Return : Bluetooth state or execution confirmation.
            """
    if on is None:
        args = shlex.split("hciconfig hci0")
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as x:
            x.wait()
            lines = x.stdout.read().decode("utf-8").strip("\n")
            # A line start with '\tUP' if bluetooth on, '\tDOWN' otherwise.
            pattern = r'\tUP'
            resultats = re.findall(pattern, lines)
            x.kill()
            if resultats:
                return True
            else:
                return False
    else:
        arg = 'up'
        if not on:
            arg = 'down'
        args = (shlex.split("sudo hciconfig hci0"))
        args.append(arg)
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as x:
            x.wait()
            x.kill()
            return on


def bluetooth_pretty_host_name():
    args = shlex.split("hostnamectl --pretty")
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as x:
        x.wait()
        x.kill()
        return x.stdout.read().decode("utf-8").strip("\n")


def set_bluetooth_pretty_host_name(name):
    # Change le pretty hostname
    os.popen("echo 'PRETTY_HOSTNAME=\"{}\"' | sudo tee /etc/machine-info".format(name))


# device is the mac adresse of the bluetooth device to remove.
def remove_paired_device(device):
    args = shlex.split("bluetoothctl remove {}".format(device))
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


# Remarque : Il faut que le PC sous W10 soit en mode réception de fichier Bluetooth
# pour que le service OPUSH soit trouvé. (donc passer en réception fichier avant d'appeler find_opush_channel)
def find_opush_channel(addr):
    command_line = "sdptool search --bdaddr {} OPUSH".format(addr)
    args = shlex.split(command_line)
    x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    x.wait()
    sdptool_results = x.stdout.read().decode("utf-8")
    pattern = re.compile('\"RFCOMM\" \(0x0003\)\n    Channel: (\d+)')
    search = pattern.search(sdptool_results)
    if search is not None:
        return int(search.group(1))

# def get_device_class(device):
#     """
#      device is the mac adresse of the bluetooth device
#     """
#     x = subprocess.Popen(["bluetoothctl", "info", device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     x.wait()
#     raw_paired_devices = x.stdout.read().decode("utf-8")
#     print(f"bluetoothctl info for {device}: {raw_paired_devices}")
#     regex = r'Class:\s(0x[0-9a-fA-F]+)'
#     expression = re.search(regex, raw_paired_devices)
#     if expression:
#         value = expression.group(1)
#         print("Valeur extraite :", value)
#         print(f"{is_computer(int(value, 16))=}")
#         print(f"{is_phone(int(value, 16))=}")
#         print(f"{is_object_transfer_capable(int(value, 16))=}")
#     else:
#         print("No value ???")
#
#
# def is_computer(device_class):
#     return bool(device_class & MajorDeviceClass.Computer.value)
#
#
# def is_phone(device_class):
#     return bool(device_class & MajorDeviceClass.Phone.value)
#
#
# def is_object_transfer_capable(device_class):
#     return bool(device_class & MajorServiceClass.ObjectTransfer.value)
#
#
# # https://www.bluetooth.com/specifications/assigned-numbers/Baseband/
# class MajorServiceClass(Enum):
#     Positioning = 0x00010000
#     Networking = 0x00020000
#     Rendering = 0x00040000
#     Capturing = 0x00080000
#     ObjectTransfer = 0x00100000
#     Audio = 0x00200000
#     Telephony = 0x00400000
#     Information = 0x00800000
#
#
# class MajorDeviceClass(Enum):
#     Miscellaneous = 0x00000000
#     Computer = 0x00000100
#     Phone = 0x00000200
#     AccessPoint = 0x00000300
#     AudioVideo = 0x00000400
#     Peripheral = 0x00000500
#     Imaging = 0x00000600
#     Wearable = 0x00000700
#     Toy = 0x00000800
#     Health = 0x00000900
#     Uncategorized = 0x00001F00
#
#
# class MinorDeviceForPhone(Enum):
#     Uncategorized = 0x00000000
#     Cellular = 0x00000004
#     Cordless = 0x00000008
#     Smartphone = 0x0000000d
#     WiredModem = 0x00000010
#     IsdnAccess = 0x00000014
#
#
# class MinorDeviceForComputer(Enum):
#     Uncategorized = 0x00000000
#     Desktop = 0x00000004
#     Server = 0x00000008
#     Laptop = 0x0000000d
#     HandledPc = 0x00000010
#     PalmSizePc = 0x00000014
#     WearableComputer = 0x00000018
#     Tablet = 0x0000001d
