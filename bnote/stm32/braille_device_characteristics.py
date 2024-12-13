"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from enum import Enum
import threading
from bnote.stm32 import stm32_keys

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, BRAILLE_DEVICE_CHARACTERISTICS_LOG

log = ColoredLogger(__name__)
log.setLevel(BRAILLE_DEVICE_CHARACTERISTICS_LOG)


#
# The braille device characteristics.
#
#
#
class BrailleDeviceCharacteristics(object):
    class DeviceSubType(Enum):
        UNKNOWN = b""
        STANDARD = b"ST"  # batterie, bluetooth et fonctions internes complètes.
        LIGHT = b"LI"  # Sans clavier mais bluetooth et batterie
        BASIC = b"BA"  # Version USB seule, pas de batterie, pas de Pi (pas de bluetooth ni de dial. opérateur).
        BASIC_LIGHT = b"BL"  # Idem à basic mais sans clavier braille.
        KEYBOARD = b"KB"  # Connexion USB, pas de batterie ni de Pi pas plus que d’afficheur braille.
        # La langue du clavier sera définie par la fab.

    class UsbHidMode(Enum):
        UNKNOWN = b""
        KEYS_SEND_TO_SCREEN_READER = b"0"
        USB_HID_KEYBOARD_ACTIF = b"1"
        HYBRID_MODE = b"2"

    class RoutineMode(Enum):
        NONE = b"0"
        FORWARD_BACKWARD = b"1"
        CLIC = b"2"
        DOUBLE_CLIC = b"3"
        WINDOWS_KEY = b"4"
        APP_KEY = b"5"

    class KeyboardMode(Enum):
        UNKNOWN = b""
        STANDARD = b"0"
        UNIMANUEL_1 = b"1"
        UNIMANUEL_2 = b"2"
        UNIMANUEL_3 = b"3"
        UNIMANUEL_4 = b"4"

    class KeyboardB78(Enum):
        UNKNOWN = b""
        CHARACTER = b"0"
        FUNCTION = b"1"

    class BatteryState(Enum):
        UNKNOWN = b""
        INACTIVE = b"0"
        DISCHARGING = b"1"
        CHARGING = b"2"
        FAST_CHARGING = b"3"
        OUT_OF_ORDER = b"4"

    esytime_esys_iris_convert_country = {
        "ar_LB": "LB",
        "cs_CZ": "CZ",
        "da_DK": "DK",
        "de_CH": "GR",
        "de_DE": "GR",
        "el_GR": "GK",
        "en_GB": "UK",
        "en_US": "US",
        "es_ES": "SP",
        "fr_CH": "FR",
        "fr_FR": "FR",
        "he_IL": "IL",
        "hr_HR": "HR",
        "it_CH": "IT",
        "it_IT": "IT",
        "is_IS": "IS",
        "lt_LT": "LT",
        "nb_NO": "NO",
        "nl_BE": "NB",
        "nl_NL": "NL",
        "pl_PL": "PL",
        "pt_PT": "PT",
        "ru_RU": "RU",
        "sl_SI": "SI",
        "sv_SE": "SE",
    }

    def __init__(self):
        # __display_length stored as int.
        self.__display_length = 0
        #  Other data are strings
        self.__firmware_version = "the unknown version"  # FIXME replace with "unknown version" when firmware updated
        self.__serial_number = "00000000"
        self.__options = b"\x00\x00\x00\x00"
        self.__device_name = "unknown device"
        self.__device_sub_type = BrailleDeviceCharacteristics.DeviceSubType.UNKNOWN
        self.__device_keyboard_language_country = b"_"
        self.__device_message_language_country = b"_"
        self.__usb_hid_mode = [
            BrailleDeviceCharacteristics.UsbHidMode.UNKNOWN,
            BrailleDeviceCharacteristics.UsbHidMode.UNKNOWN,
        ]
        self.__device_keyboard_inversion = False
        self.__device_usb_simul_esys = False
        self.__device_keyboard_mode = BrailleDeviceCharacteristics.KeyboardMode.UNKNOWN
        self.__device_keyboard_b78 = BrailleDeviceCharacteristics.KeyboardB78.UNKNOWN
        self.__device_keyboard_routing_light_press = (
            BrailleDeviceCharacteristics.RoutineMode.NONE
        )
        self.__device_keyboard_routing_strong_press = (
            BrailleDeviceCharacteristics.RoutineMode.NONE
        )
        self.__device_keyboard_routing_consecutive_press = (
            BrailleDeviceCharacteristics.RoutineMode.NONE
        )
        self.__device_keyboard_routing_double_light_press = (
            BrailleDeviceCharacteristics.RoutineMode.NONE
        )
        self.__device_keyboard_routing_double_strong_press = (
            BrailleDeviceCharacteristics.RoutineMode.NONE
        )
        self.__battery_remaining_capacity = 0
        self.__battery_voltage = 0
        self.__battery_intensity = 0
        self.__battery_state = BrailleDeviceCharacteristics.BatteryState.UNKNOWN
        self.__standby_transport = "0"
        self.__standby_shutdown = "0"
        self.__mutex = threading.Lock()  # equal to threading.Semaphore(1)

        self.__device_usb_a_name = ""
        self.__device_usb_b_name = ""

    def is_init_done(self):
        with self.__mutex:
            if self.__serial_number != "00000000":
                return True
            return False

    def get_braille_display_length(self) -> int:
        with self.__mutex:
            if isinstance(self.__display_length, int):
                return self.__display_length
            elif isinstance(self.__display_length, bytes):
                return int.from_bytes(self.__display_length, "big")

    def set_braille_display_length(self, braille_display_length: bytes):
        with self.__mutex:
            self.__display_length = int.from_bytes(braille_display_length, "big")

    def get_braille_display_length_in_bytes(self) -> bytes:
        with self.__mutex:
            return self.__display_length.to_bytes(
                (self.__display_length.bit_length() + 7) // 8, "big"
            )

    def set_keyboard_language_country(self, language_country: bytes):
        with self.__mutex:
            self.__device_keyboard_language_country = language_country
            # >>> Patch compatibilité à retirer quand le protocole aura été modifié.
            if len(self.__device_keyboard_language_country) == 2:
                self.__device_keyboard_language_country = b"_".join(
                    (
                        self.__device_keyboard_language_country.lower(),
                        self.__device_keyboard_language_country.upper(),
                    )
                )
        # <<< Patch compatibilité à retirer quand le protocole aura été modifié.

    def get_keyboard_language_country(self) -> str:
        with self.__mutex:
            return self.__device_keyboard_language_country.decode()

    # Only for Esytime-Esys-Iris protocol
    def get_keyboard_language_country_in_bytes(self) -> bytes:
        return self.__device_keyboard_language_country

    #     with self.__mutex:
    #         if self.__device_keyboard_language_country in BrailleDeviceCharacteristics.esytime_esys_iris_convert_country.keys():
    #             return BrailleDeviceCharacteristics.esytime_esys_iris_convert_country[
    #                 self.__device_keyboard_language_country]
    #         else:
    #             # b'  ' Means international according to the Esytime-Esys-Iris protocol.
    #             return b'  '

    # FIXME 03/11/2020 : Pas utilisé, à conserver ?
    # def get_keyboard_language(self) -> str:
    #     with self.__mutex:
    #         if self.__device_keyboard_language_country.find(b'_') != -1:
    #             language, country = self.__device_keyboard_language_country.split(b'_')
    #             return language.decode()
    #         else:
    #             return ""
    #
    # def get_keyboard_country(self) -> str:
    #     with self.__mutex:
    #         if self.__device_keyboard_language_country.find(b'_') != -1:
    #             language, country = self.__device_keyboard_language_country.split(b'_')
    #             return country.decode()
    #         else:
    #             return ""

    def set_message_language_country(self, language_country: bytes):
        with self.__mutex:
            self.__device_message_language_country = language_country
            # >>> Patch compatibilité à retirer quand le protocole aura été modifié.
            if len(self.__device_message_language_country) == 2:
                self.__device_message_language_country = b"_".join(
                    (
                        self.__device_message_language_country.lower(),
                        self.__device_message_language_country.upper(),
                    )
                )
            # <<< Patch compatibilité à retirer quand le protocole aura été modifié.

    def get_message_language_country(self) -> str:
        with self.__mutex:
            return self.__device_message_language_country.decode()

    def set_options(self, options: bytes):
        with self.__mutex:
            log.info("options : {}".format(options))
            for value in options:
                log.info("val : {}".format(value))
            self.__options = bytearray(options)

    def get_options(self) -> bytes:
        if self.is_esysuite_option():
            return b"\x00\x00\x02\x00"
        else:
            return b"\x00\x00\x00\x00"

    def is_esysuite_option(self):
        if (
            self.__options
            and (len(self.__options) > 3)
            and ((self.__options[1] & 2) != 0)
        ):
            return True
        else:
            return False

    def set_serial_number(self, serial_number: bytes):
        with self.__mutex:
            self.__serial_number = serial_number.decode()

    def get_serial_number(self) -> str:
        with self.__mutex:
            return self.__serial_number

    def get_serial_number_raw_data(self) -> bytes:
        with self.__mutex:
            return self.__serial_number.encode()

    def set_firmware_version(self, data: bytes):
        with self.__mutex:
            self.__firmware_version = data.decode()

    def get_firmware_version(self) -> str:
        with self.__mutex:
            return self.__firmware_version

    def set_name(self, name: bytes):
        with self.__mutex:
            self.__device_name = name.decode()

    def get_name(self) -> str:
        with self.__mutex:
            return self.__device_name

    def get_name_raw_data(self) -> bytes:
        with self.__mutex:
            return self.__device_name.encode()

    def set_sub_type(self, data: bytes):
        with self.__mutex:
            try:
                value = BrailleDeviceCharacteristics.DeviceSubType(data)
                self.__device_sub_type = value
            except ValueError:
                self.__device_sub_type = (
                    BrailleDeviceCharacteristics.DeviceSubType.UNKNOWN
                )

    def get_sub_type(self):
        with self.__mutex:
            return self.__device_sub_type

    def set_usb_hid_mode_raw_data(self, data: bytes):
        with self.__mutex:
            try:
                data_list = [bytes([b]) for b in data]
                for index, data_value in enumerate(data_list):
                    value = BrailleDeviceCharacteristics.UsbHidMode(data_value)
                    self.__usb_hid_mode[index] = value
            except ValueError:
                self.__usb_hid_mode = [
                    BrailleDeviceCharacteristics.UsbHidMode.UNKNOWN,
                    BrailleDeviceCharacteristics.UsbHidMode.UNKNOWN,
                ]

    def set_usb_hid_mode(self, index, value: UsbHidMode):
        with self.__mutex:
            self.__usb_hid_mode[index] = value

    def get_usb_hid_mode(self, index) -> UsbHidMode:
        with self.__mutex:
            if len(self.__usb_hid_mode) > index:
                return self.__usb_hid_mode[index]
            else:
                return (
                    BrailleDeviceCharacteristics.UsbHidMode.KEYS_SEND_TO_SCREEN_READER
                )

    def get_usb_hid_mode_raw_data(self) -> bytes:
        with self.__mutex:
            return self.__usb_hid_mode[0].value + self.__usb_hid_mode[1].value

    def set_usb_simul_esys_raw_data(self, data: bytes):
        with self.__mutex:
            if data == b"1":
                self.__device_usb_simul_esys = True
            else:
                self.__device_usb_simul_esys = False

    def set_usb_simul_esys(self, value: bool):
        with self.__mutex:
            self.__device_usb_simul_esys = value

    def get_usb_simul_esys(self) -> bool:
        with self.__mutex:
            return self.__device_usb_simul_esys

    def get_usb_simul_esys_raw_data(self) -> bytes:
        with self.__mutex:
            if self.__device_usb_simul_esys:
                return b"1"
            else:
                return b"0"

    def set_keyboard_mode_raw_data(self, data: bytes):
        with self.__mutex:
            try:
                value = BrailleDeviceCharacteristics.KeyboardMode(data)
                self.__device_keyboard_mode = value
            except ValueError:
                self.__device_keyboard_mode = (
                    BrailleDeviceCharacteristics.KeyboardMode.UNKNOWN
                )

    def set_keyboard_mode(self, value: KeyboardMode):
        with self.__mutex:
            self.__device_keyboard_mode = value

    def get_keyboard_mode(self) -> KeyboardMode:
        with self.__mutex:
            return self.__device_keyboard_mode

    def get_keyboard_mode_raw_data(self) -> bytes:
        # keyboard_mode_dict = {BrailleDeviceCharacteristics.KeyboardMode.UNKNOWN: b'0',
        #                       BrailleDeviceCharacteristics.KeyboardMode.STANDARD: b'0',
        #                       BrailleDeviceCharacteristics.KeyboardMode.UNIMANUEL_1: b'1',
        #                       BrailleDeviceCharacteristics.KeyboardMode.UNIMANUEL_2: b'2',
        #                       BrailleDeviceCharacteristics.KeyboardMode.UNIMANUEL_3: b'3',
        #                       BrailleDeviceCharacteristics.KeyboardMode.UNIMANUEL_4: b'4'
        #                       }
        #
        with self.__mutex:
            log.info("keyboardmode : {}".format(self.__device_keyboard_mode.value))
            return self.__device_keyboard_mode.value

    def set_keyboard_b78_raw_data(self, data: bytes):
        with self.__mutex:
            try:
                value = BrailleDeviceCharacteristics.KeyboardB78(data)
                self.__device_keyboard_b78 = value
            except ValueError:
                self.__device_keyboard_b78 = (
                    BrailleDeviceCharacteristics.KeyboardB78.UNKNOWN
                )

    def get_keyboard_b78_raw_data(self) -> bytes:
        with self.__mutex:
            log.info("keyboard b78 : {}".format(self.__device_keyboard_b78.value))
            return self.__device_keyboard_b78.value

    def set_keyboard_b78(self, value: KeyboardB78):
        with self.__mutex:
            self.__device_keyboard_b78 = value

    def get_keyboard_b78(self) -> KeyboardB78:
        with self.__mutex:
            return self.__device_keyboard_b78

    def set_keyboard_inversion_raw_data(self, data: bytes):
        with self.__mutex:
            if data == b"1":
                self.__device_keyboard_inversion = True
            else:
                self.__device_keyboard_inversion = False

    def set_keyboard_inversion(self, value: bool):
        with self.__mutex:
            self.__device_keyboard_inversion = value

    def get_keyboard_inversion(self) -> bool:
        with self.__mutex:
            return self.__device_keyboard_inversion

    def get_keyboard_inversion_raw_data(self) -> bytes:
        with self.__mutex:
            if self.__device_keyboard_inversion:
                return b"1"
            else:
                return b"0"

    # def set_standby_raw_data(self, data):
    #     with self.__mutex:
    #         index_transport_start = data.index(stm32_keys.VALUE_STANDBY_TRANSPORT)
    #         index_shutdown_start = data.index(stm32_keys.VALUE_STANDBY_SHUTDOWN)
    #         if (index_transport_start == -1) or (index_shutdown_start == -1):
    #             # Invalid data
    #             return
    #         if index_transport_start > index_shutdown_start:
    #             index_transport_end = len(data)
    #             index_shutdown_end = index_transport_start
    #         else:
    #             index_transport_end = index_shutdown_start
    #             index_shutdown_end = len(data)
    #         print(data[index_transport_start + 1:index_transport_end])
    #         print(data[index_shutdown_start + 1:index_shutdown_end])
    #         self.set_standby_transport(data[index_transport_start + 1:index_transport_end])
    #         self.set_standby_shutdown(data[index_shutdown_start + 1:index_shutdown_end])

    def set_standby_transport(self, value):
        with self.__mutex:
            if isinstance(value, str):
                self.__standby_transport = value
            else:
                self.__standby_transport = value.decode()

    def get_standby_transport(self) -> str:
        with self.__mutex:
            return self.__standby_transport

    def get_standby_raw_data(self) -> bytes:
        with self.__mutex:
            return (
                stm32_keys.VALUE_STANDBY_TRANSPORT
                + self.__standby_transport.encode()
                + stm32_keys.VALUE_STANDBY_SHUTDOWN
                + self.__standby_shutdown.encode()
            )

    def set_standby_shutdown(self, value):
        with self.__mutex:
            if isinstance(value, str):
                self.__standby_shutdown = value
            else:
                self.__standby_shutdown = value.decode()

    def get_standby_shutdown(self) -> str:
        with self.__mutex:
            return self.__standby_shutdown

    def set_keyboard_routing_mode_raw_data(self, data: bytes):
        with self.__mutex:
            index = data.index(stm32_keys.VALUE_LIGHT_PRESS)
            try:
                # log.critical(f"data[index:index+1]={data[index+1:index+2]}")
                value = BrailleDeviceCharacteristics.RoutineMode(
                    data[index + 1 : index + 2]
                )
                self.__device_keyboard_routing_light_press = value
                # log.critical(f"self.__device_keyboard_routine1={self.__device_keyboard_routine1}")
            except ValueError:
                self.__device_keyboard_routing_light_press = (
                    BrailleDeviceCharacteristics.RoutineMode.NONE
                )

            index = data.index(stm32_keys.VALUE_STRONG_PRESS)
            try:
                value = BrailleDeviceCharacteristics.RoutineMode(
                    data[index + 1 : index + 2]
                )
                self.__device_keyboard_routing_strong_press = value
            except ValueError:
                self.__device_keyboard_routing_strong_press = (
                    BrailleDeviceCharacteristics.RoutineMode.NONE
                )

            index = data.index(stm32_keys.VALUE_CONSECUTIVE_PRESS)
            try:
                value = BrailleDeviceCharacteristics.RoutineMode(
                    data[index + 1 : index + 2]
                )
                self.__device_keyboard_routing_consecutive_press = value
            except ValueError:
                self.__device_keyboard_routing_consecutive_press = (
                    BrailleDeviceCharacteristics.RoutineMode.NONE
                )

            index = data.index(stm32_keys.VALUE_DOUBLE_LIGHT_PRESS)
            try:
                value = BrailleDeviceCharacteristics.RoutineMode(
                    data[index + 1 : index + 2]
                )
                self.__device_keyboard_routing_double_light_press = value
            except ValueError:
                self.__device_keyboard_routing_double_light_press = (
                    BrailleDeviceCharacteristics.RoutineMode.NONE
                )

            index = data.index(stm32_keys.VALUE_DOUBLE_STRONG_PRESS)
            try:
                value = BrailleDeviceCharacteristics.RoutineMode(
                    data[index + 1 : index + 2]
                )
                self.__device_keyboard_routing_double_strong_press = value
            except ValueError:
                self.__device_keyboard_routing_double_strong_press = (
                    BrailleDeviceCharacteristics.RoutineMode.NONE
                )

    def get_keyboard_routing_mode_raw_data(self) -> bytes:
        with self.__mutex:
            return b"".join(
                (
                    stm32_keys.VALUE_LIGHT_PRESS,
                    self.__device_keyboard_routing_light_press.value,
                    stm32_keys.VALUE_STRONG_PRESS,
                    self.__device_keyboard_routing_strong_press.value,
                    stm32_keys.VALUE_CONSECUTIVE_PRESS,
                    self.__device_keyboard_routing_consecutive_press.value,
                    stm32_keys.VALUE_DOUBLE_LIGHT_PRESS,
                    self.__device_keyboard_routing_double_light_press.value,
                    stm32_keys.VALUE_DOUBLE_STRONG_PRESS,
                    self.__device_keyboard_routing_double_strong_press.value,
                )
            )

    def set_keyboard_routing_light_press(self, value: RoutineMode):
        with self.__mutex:
            self.__device_keyboard_routing_light_press = value

    def get_keyboard_routing_light_press(self) -> RoutineMode:
        with self.__mutex:
            return self.__device_keyboard_routing_light_press

    def set_keyboard_routing_strong_press(self, value: RoutineMode):
        with self.__mutex:
            self.__device_keyboard_routing_strong_press = value

    def get_keyboard_routing_strong_press(self) -> RoutineMode:
        with self.__mutex:
            return self.__device_keyboard_routing_strong_press

    def set_keyboard_routing_consecutive_press(self, value: RoutineMode):
        with self.__mutex:
            self.__device_keyboard_routing_consecutive_press = value

    def get_keyboard_routing_consecutive_press(self) -> RoutineMode:
        with self.__mutex:
            return self.__device_keyboard_routing_consecutive_press

    def set_keyboard_routing_double_light_press(self, value: RoutineMode):
        with self.__mutex:
            self.__device_keyboard_routing_double_light_press = value

    def get_keyboard_routing_double_light_press(self) -> RoutineMode:
        with self.__mutex:
            return self.__device_keyboard_routing_double_light_press

    def set_keyboard_routing_double_strong_press(self, value: RoutineMode):
        with self.__mutex:
            self.__device_keyboard_routing_double_strong_press = value

    def get_keyboard_routing_double_strong_press(self) -> RoutineMode:
        with self.__mutex:
            return self.__device_keyboard_routing_double_strong_press

    def set_battery_raw_data(self, data: bytes):
        with self.__mutex:
            index_percent = data.index(stm32_keys.VALUE_BATTERY_PERCENT)
            index_intensity = data.index(stm32_keys.VALUE_BATTERY_INTENSITY)
            index_voltage = data.index(stm32_keys.VALUE_BATTERY_VOLTAGE)
            index_state = data.index(stm32_keys.VALUE_BATTERY_STATE)

            try:
                value = data[index_percent + 1 : index_intensity].decode()
                self.__battery_remaining_capacity = int(value)
            except ValueError:
                pass

            try:
                value = data[index_intensity + 1 : index_voltage].decode()
                self.__battery_intensity = int(value)
            except ValueError:
                pass

            try:
                value = data[index_voltage + 1 : index_state].decode()
                self.__battery_voltage = int(value)
            except ValueError:
                pass

            try:
                value = data[index_state + 1 :]
                self.__battery_state = BrailleDeviceCharacteristics.BatteryState(value)
            except ValueError:
                self.__battery_state = BrailleDeviceCharacteristics.BatteryState.UNKNOWN
                pass

    def get_battery_raw_data(self) -> bytes:
        with self.__mutex:
            return b"".join(
                (
                    stm32_keys.VALUE_BATTERY_PERCENT,
                    str(self.__battery_remaining_capacity).encode(),
                    stm32_keys.VALUE_BATTERY_INTENSITY,
                    str(self.__battery_intensity).encode(),
                    stm32_keys.VALUE_BATTERY_VOLTAGE,
                    str(self.__battery_voltage).encode(),
                    stm32_keys.VALUE_BATTERY_STATE,
                    self.__battery_state.value,
                )
            )

    def get_battery_remaining_capacity(self) -> int:
        with self.__mutex:
            return self.__battery_remaining_capacity

    def set_battery_remaining_capacity(self, value: int):
        with self.__mutex:
            self.__battery_remaining_capacity = value

    def get_battery_voltage(self) -> int:
        with self.__mutex:
            return self.__battery_voltage

    def set_battery_voltage(self, value: int):
        with self.__mutex:
            self.__battery_voltage = value

    def get_battery_intensity(self) -> int:
        with self.__mutex:
            return self.__battery_intensity

    def set_battery_intensity(self, value: int):
        with self.__mutex:
            self.__battery_intensity = value

    def get_battery_state(self) -> BatteryState:
        with self.__mutex:
            return self.__battery_state

    def set_battery_state(self, value: BatteryState):
        with self.__mutex:
            self.__battery_state = value

    def set_usb_app_name(self, usb_a_name, usb_b_name):
        self.__device_usb_a_name = usb_a_name
        self.__device_usb_b_name = usb_b_name

    def __str__(self):
        with self.__mutex:
            return "display_length={} serial_number={} device_name={} device_language={}".format(
                self.__display_length,
                self.__serial_number,
                self.__device_name,
                self.__device_keyboard_language_country,
            )


# Global instance of BrailleDeviceCharacteristics
braille_device_characteristics = BrailleDeviceCharacteristics()
