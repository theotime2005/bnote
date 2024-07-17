"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from enum import Enum
from bnote.tools import bt_util as bt_util
from bnote.stm32 import stm32_keys


# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, STM32_PROTOCOL_LOG
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.tools.settings import Settings, BLUETOOTH_BASE_NAME

log = ColoredLogger(__name__)
log.setLevel(STM32_PROTOCOL_LOG)

# Event sent by protocol frame decoding
STM32_LANGUAGE_CHANGE = object()
STM32_BRAILLE_TABLE_CHANGE = object()
STM32_DATE_AND_TIME = object()
STM32_ENTER_INTERNAL = object()
STM32_EXIT_INTERNAL = object()
STM32_BRAILLE_KEY = object()
STM32_COMMAND_KEY = object()
STM32_INTERACTIVE_KEY = object()
STM32_SHUTDOWN_PI = object()
STM32_USB_APP_NAME_CHANGED = object()


STX = b'\x02'   # Start of Frame
ETX = b'\x03'   # End of Frame
ESC = b'\x1b'   # ESC is the escape char used to send STX, ETX, ESC when char is inside STX and ETX.

FRAME_MAX_LENGTH = 256  # The maximum length of the frame (excluding all the escape char ESC in the Frame)
STM32_MAX_BLUETOOTH_CHANNEL_NAME = 32  # The maximum length of the bluetooth adapter name send with KEY_BLUETOOTH_ACTIVATE_CHANNEL


class Stm32Frame(object):
    escaped_char = (STX, ETX, ESC)
    # Frame number (from 0 to 255)
    send_frame_number = b'\xFF'

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            # Only one arg, it is a buffer with key at first pos and data next.
            if isinstance(args[0], bytes):
                self._key = args[0][0:1]
                self._data = args[0][1:]
                return
        if not('key' in kwargs):
            # No args and no key => Error ?
            raise ValueError("Cannot init Frame without key")
        self._key = kwargs['key']
        self._data = None
        if 'data' in kwargs:
            if isinstance(kwargs['data'], int):
                self._data = kwargs['data'].to_bytes((kwargs['data'].bit_length() + 7) // 8, 'big')
            elif isinstance(kwargs['data'], bytes):
                self._data = kwargs['data']
            elif isinstance(kwargs['data'], bytearray):
                self._data = bytes(kwargs['data'])
            elif isinstance(kwargs['data'], str):
                # change encoding to utf-8
                self._data = kwargs['data'].encode()
            else:
                log.warning("Cannot init Frame with type(kwargs['data'])={}".format(type(kwargs['data'])))

    def key(self):
        return self._key

    def data(self):
        return self._data

    def cooked_frame_buffer(self):
        # Increase the frame number to send.
        Stm32Frame.send_frame_number = bytes([(int.from_bytes(Stm32Frame.send_frame_number, 'big') + 1) % 256])
        if self._data is None:
            # Return an escaped buffer that represent the Frame to send.
            return bytearray(b''.join((STX, self._escape_message(bytes(b''.join((Stm32Frame.send_frame_number,
                                                                                 self._key)))), ETX)))
        else:
            # Return an escaped buffer that represent the Frame to send.
            return bytearray(b''.join((STX, self._escape_message(bytes(b''.join((Stm32Frame.send_frame_number,
                                                                             self._key, self._data)))), ETX)))

    # Return message with usefull ESC byte
    def _escape_message(self, message):
        escaped_message = bytes()
        for value in message:
            if value.to_bytes(1, 'big') in Stm32Frame.escaped_char:
                escaped_message += ESC

            escaped_message += value.to_bytes(1, 'big')

        log.debug("message={} escaped_message={}".format(message, escaped_message))
        return escaped_message

    def __str__(self):
        return "key={} data={}".format(self._key, self._data)


#  https://docs.python.org/3/library/enum.html
class RxMode(Enum):
    WAIT_STX = 1
    WAIT_FRAME_NUMBER = 2
    WAIT_KEY = 3
    WAIT_DATA = 4


class Stm32Protocol:
    def __init__(self, queue_event):
        self._rx_escape_next_char = False
        self._rx_message_buffer = bytes()
        self._rx_frame_number = -1
        self._rx_mode = RxMode.WAIT_STX
        self._queue_event = queue_event

    def rx_treatment(self, byte):
        # log.info("byte={} type(byte)={}".format(byte, type(byte)))
        if ((self._rx_mode == RxMode.WAIT_STX) or not self._rx_escape_next_char) and byte == STX:
            self._rx_mode = RxMode.WAIT_FRAME_NUMBER
        elif self._rx_mode != RxMode.WAIT_STX:
            if not self._rx_escape_next_char and byte == ESC:
                self._rx_escape_next_char = True
            else:
                if self._rx_mode == RxMode.WAIT_FRAME_NUMBER:
                    frame_num = int.from_bytes(byte, 'big')
                    if self._rx_frame_number != -1 and (self._rx_frame_number + 1) % 256 != frame_num:
                        log.info("Error previous_frame_number={} received={}".format(self._rx_frame_number, frame_num))
                    self._rx_frame_number = frame_num
                    self._rx_mode = RxMode.WAIT_KEY
                elif self._rx_mode == RxMode.WAIT_KEY:
                    self._rx_message_buffer = bytes(byte)
                    self._rx_mode = RxMode.WAIT_DATA
                elif self._rx_mode == RxMode.WAIT_DATA:
                    if not self._rx_escape_next_char and byte == ETX:
                        # self._rx_frame_treatment()
                        self._rx_mode = RxMode.WAIT_STX
                        # When ETX is received a frame object is returned
                        return Stm32Frame(self._rx_message_buffer)
                    else:
                        if len(self._rx_message_buffer) < FRAME_MAX_LENGTH:
                            self._rx_message_buffer += byte
                        else:
                            log.warning("Received more byte that expected")

                self._rx_escape_next_char = False

    # def _rx_frame_treatment(self):
    #     log.info("received frame : {}".format(self._rx_message_buffer))

    def send_event(self, event_type, data):
        event = (event_type, data)
        self._queue_event.put(event)

    def _decode_frame(self, frame):
        log.info("{}".format(frame))
        if isinstance(frame, Stm32Frame):
            switcher = {
                stm32_keys.KEY_FIRMWARE_VERSION: self._treat_firmware_version,
                stm32_keys.KEY_DEVICE_NAME: self._treat_device_name,
                stm32_keys.KEY_DEVICE_SUB_TYPE: self._treat_device_sub_type,
                stm32_keys.KEY_DEVICE_LENGTH: self._treat_device_length,
                stm32_keys.KEY_SERIAL_NUMBER: self._treat_serial_number,
                stm32_keys.KEY_OPTIONS : self._treat_options,
                stm32_keys.KEY_DEVICE_LANGUAGE: self._treat_device_language,
                stm32_keys.KEY_KEYBOARD_LANGUAGE: self._treat_device_keyboard_language,
                stm32_keys.KEY_BRAILLE_KEYBOARD_B78: self._treat_device_keyboard_b78,
                stm32_keys.KEY_USB_HID_MODE: self._treat_device_usb_hid_mode,
                stm32_keys.KEY_USB_SIMUL_ESYS: self._treat_usb_simul_esys,
                stm32_keys.KEY_BRAILLE_KEYBOARD_MODE: self._treat_braille_keyboard_mode,
                stm32_keys.KEY_COMMAND_INVERTED_MODE: self._treat_command_inverted_mode,
                stm32_keys.KEY_INTERACTIVE_KEYS_MODE: self._treat_interactive_keys_mode,
                stm32_keys.KEY_DEVICE_DATE_AND_TIME: self._treat_device_date_and_time,
                stm32_keys.KEY_BATTERY: self._treat_battery,
                stm32_keys.KEY_STANDBY: self._treat_standby,
                stm32_keys.KEY_INTERNAL_FUNCTION_ENTER: self._treat_internal_function_enter,
                stm32_keys.KEY_INTERNAL_FUNCTION_EXIT: self._treat_internal_function_exit,
                stm32_keys.KEY_BRAILLE_KEYS: self._treat_braille_keys,
                stm32_keys.KEY_COMMAND_KEYS: self._treat_command_keys,
                stm32_keys.KEY_INTERACTIVE_KEYS: self._treat_interactive_keys,
                stm32_keys.KEY_SHUTDOWN_PI: self._treat_shutdown_pi,
                stm32_keys.KEY_SPEECH: self._treat_speech,
                stm32_keys.KEY_APP_NAME: self._treat_app_name,
            }
            func = switcher.get(frame.key(), None)
            if func is not None:
                func(frame.data())
            else:
                log.warning("No function defined for {}".format(frame.key()))
        else:
            log.warning("bad param. It should be Stm32Frame but it was {}".format(frame))


    @staticmethod
    def _treat_firmware_version(data):
        braille_device_characteristics.set_firmware_version(data)

    @staticmethod
    def _treat_device_name(data):
        braille_device_characteristics.set_name(data)

    @staticmethod
    def _treat_device_sub_type(data):
        braille_device_characteristics.set_sub_type(data)

    @staticmethod
    def _treat_device_length(data):
        braille_device_characteristics.set_braille_display_length(data)

    @staticmethod
    def _treat_serial_number(data):
        braille_device_characteristics.set_serial_number(data)
        if Settings().data['bluetooth']['bnote_name'] == "":
            if bt_util.bluetooth_pretty_host_name() != BLUETOOTH_BASE_NAME + braille_device_characteristics.get_serial_number():
                # Change le pretty hostname
                bt_util.set_bluetooth_pretty_host_name(
                    BLUETOOTH_BASE_NAME + braille_device_characteristics.get_serial_number())

    @staticmethod
    def _treat_options(data):
        braille_device_characteristics.set_options(data)

    def _treat_device_language(self, data):
        braille_device_characteristics.set_message_language_country(data)
        self.send_event(STM32_LANGUAGE_CHANGE, braille_device_characteristics.get_message_language_country())

    def _treat_device_keyboard_language(self, data):
        braille_device_characteristics.set_keyboard_language_country(data)
        self.send_event(STM32_BRAILLE_TABLE_CHANGE, braille_device_characteristics.get_keyboard_language_country())

    @staticmethod
    def _treat_device_keyboard_b78(data):
        braille_device_characteristics.set_keyboard_b78_raw_data(data)

    @staticmethod
    def _treat_device_usb_hid_mode(data):
        braille_device_characteristics.set_usb_hid_mode_raw_data(data)

    @staticmethod
    def _treat_usb_simul_esys(data):
        braille_device_characteristics.set_usb_simul_esys_raw_data(data)

    @staticmethod
    def _treat_braille_keyboard_mode(data):
        braille_device_characteristics.set_keyboard_mode_raw_data(data)

    @staticmethod
    def _treat_command_inverted_mode(data):
        braille_device_characteristics.set_keyboard_inversion_raw_data(data)

    @staticmethod
    def _treat_interactive_keys_mode(data):
        braille_device_characteristics.set_keyboard_routing_mode_raw_data(data)

    def _treat_device_date_and_time(self, data):
        self.send_event(STM32_DATE_AND_TIME, data)
        # self._change_date_and_time(str(data, "utf-8"))

    @staticmethod
    def _treat_battery(data):
        braille_device_characteristics.set_battery_raw_data(data)

    @staticmethod
    def _treat_standby(data):
        #braille_device_characteristics.set_standby_raw_data(data)
        index_transport_start = data.index(stm32_keys.VALUE_STANDBY_TRANSPORT)
        index_shutdown_start = data.index(stm32_keys.VALUE_STANDBY_SHUTDOWN)
        if (index_transport_start == -1) or (index_shutdown_start == -1):
            # Invalid data
            return
        if index_transport_start > index_shutdown_start:
            index_transport_end = len(data)
            index_shutdown_end = index_transport_start
        else:
            index_transport_end = index_shutdown_start
            index_shutdown_end = len(data)
        braille_device_characteristics.set_standby_transport(data[index_transport_start + 1:index_transport_end])
        braille_device_characteristics.set_standby_shutdown(data[index_shutdown_start + 1:index_shutdown_end])

    def _treat_internal_function_enter(self, data):
        log.info("Enter in internal function request : {}".format(data))
        self.send_event(STM32_ENTER_INTERNAL, data)
        # self._internal_mode = True
        # self._refresh_braille_from_internal(True)

    def _treat_internal_function_exit(self, data):
        log.info("Exit of internal function request : {}".format(data))
        self.send_event(STM32_EXIT_INTERNAL, data)
        # self._internal_mode = False

    def _treat_braille_keys(self, data):
        log.info("Braille key : {}".format(data))
        self.send_event(STM32_BRAILLE_KEY, data)

    def _treat_command_keys(self, data):
        log.info("Command key : {}".format(data))
        self.send_event(STM32_COMMAND_KEY, data)

    def _treat_interactive_keys(self, data):
        log.info("Interactive key : {}".format(data))
        self.send_event(STM32_INTERACTIVE_KEY, data)

    def _treat_shutdown_pi(self, data):
        log.info("Shutdown request : {}".format(data))
        self.send_event(STM32_SHUTDOWN_PI, data)

    def _treat_speech(self, data):
        log.info("Speech : {}".format(data))

    @staticmethod
    def __treat_app_name(data, index):
        name_len = data[index]
        index += 1
        if name_len > 0:
            name_str = data[index: index + name_len].decode("utf-8").lower().replace("/", "-com")
            index += name_len
        else:
            name_str = ""
        return name_str, index

    def _treat_app_name(self, data):
        index = 0
        usb_a_name = usb_b_name = ""
        if data[index].to_bytes(1, 'big') == b'1':
            index += 1
            usb_a_name, index = self.__treat_app_name(data, index)
            if data[index].to_bytes(1, 'big') == b'2':
                index += 1
                usb_b_name, index = self.__treat_app_name(data, index)
        log.info(f"_treat_app_name : {usb_a_name=} {usb_b_name=}")
        braille_device_characteristics.set_usb_app_name(usb_a_name, usb_b_name)
        self.send_event(STM32_USB_APP_NAME_CHANGED, (usb_a_name, usb_b_name))


# -----------------------------------------------
# Unitary test
def main():

    frame1 = Stm32Frame(b''.join((stm32_keys.KEY_CHARACTERISTICS, STX, b'A', ETX, ESC)))
    frame1_cooked_message = frame1.cooked_frame_buffer()
    log.info("frame1 = {}".format(frame1_cooked_message))


if __name__ == "__main__":
    main()
