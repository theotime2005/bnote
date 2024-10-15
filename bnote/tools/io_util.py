from tools.rpi_bnote import is_running_on_rpi

if is_running_on_rpi():
    import RPi.GPIO as GPIO

from tools.settings import Settings
from tools.singleton_meta import SingletonMeta


class Gpio(metaclass=SingletonMeta):

    # output pin

    # Input pin
    __head_phone_pin = 5
    __hardware_v2 = 6

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Gpio.__head_phone_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Gpio.__hardware_v2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    @staticmethod
    def gpio_head_phone():
        return not GPIO.input(Gpio.__head_phone_pin) == 1

    @staticmethod
    def gpio_hardware_v2():
        return GPIO.input(Gpio.__hardware_v2) == 1

    @staticmethod
    def is_head_phone():
        # Return always True is generation 1
        return Gpio.gpio_head_phone() or not Gpio().gpio_hardware_v2()
