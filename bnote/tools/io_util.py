"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.yaupdater import YAUpdaterFinder
import RPi.GPIO as GPIO

from bnote.tools.settings import Settings
from bnote.stm32.braille_device_characteristics import braille_device_characteristics

from bnote.tools.singleton_meta import SingletonMeta


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
        current_raw_firmware_version = (
            braille_device_characteristics.get_firmware_version()
        )
        is_bnote_plus = YAUpdaterFinder.is_first_str_version_greater_or_equal(
            current_raw_firmware_version, "4.0.0"
        )
        if is_bnote_plus:
            # Firmware V4.0.0 and upper run on hardware bnote64 and bnote80 -> Allways with HP and USB port.
            return True
        else:
            return GPIO.input(Gpio.__hardware_v2) == 1

    @staticmethod
    def is_head_phone():
        # Return always True is generation 1
        return Gpio.gpio_head_phone() or not Gpio().gpio_hardware_v2()
