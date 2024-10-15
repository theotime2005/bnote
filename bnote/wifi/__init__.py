import os
from .wpa_supplicant import WpaSupplicant
from .scan import Cell, InterfaceError


def interface():
    return 'wlan0'


def activate():
    """
    Disconnect/Connect to the network as configured in this scheme.
    https://forums.raspberrypi.com/viewtopic.php?t=198274
    """
    process = os.popen(f"wpa_cli -i {interface()} reconfigure")
    # process = os.popen(f"sudo ip link set dev {interface()} down")
    # Wait execution
    process.read()
    # os.popen(f"sudo ip link set dev {interface()} up")
    # Wait execution
    # process.read()
