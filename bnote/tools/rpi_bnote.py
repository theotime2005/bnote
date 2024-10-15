import platform


def is_running_on_rpi():
    return platform.node() == "raspberrypi"
