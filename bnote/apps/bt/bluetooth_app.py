"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


from apps.bnote_app import BnoteApp, FunctionId
import bt.bt_protocol as bt_protocol
from braille.louis.lou import Lou
from bt.bt_thread import bluetooth_thread_pool
from stm32 import stm32_keys
from stm32.braille_device_characteristics import braille_device_characteristics
from stm32.stm32_protocol import Stm32Frame
import stm32.stm32_protocol as stm32_protocol
from tools.keyboard import Keyboard

# Setup the logger for this file
from debug.colored_log import ColoredLogger, BLUETOOTH_APP_LOG
from tools.settings import Settings

log = ColoredLogger(__name__)
log.setLevel(BLUETOOTH_APP_LOG)


class BluetoothApp(BnoteApp):

    def __init__(self, put_in_function_queue, put_in_stm32_tx_queue, bluetooth_id):
        BnoteApp.__init__(self, put_in_function_queue)
        self._put_in_stm32_tx_queue = put_in_stm32_tx_queue
        self._bluetooth_id = bluetooth_id
        # Set default braille display.
        static_dots = BnoteApp.lou.to_dots_8(_("bluetooth listening"))
        self.set_braille_display_dots_line(static_dots, "\u2800" * len(static_dots), 0)

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        # Nothing to do
        pass

    def input_function(self, *args, **kwargs):
        return False

    def input_braille(self, data) -> (bool, object()):
        bluetooth_thread_pool.put_message_in_tx_queue(bt_protocol.Frame(bt_protocol.Message(
            key=bt_protocol.Message.KEY_KEYBOARD, subkey=bt_protocol.Message.SUBKEY_KEYBOARD_BRAILLE,
            data=data[0:2])))
        return False

    def input_command(self, data, modifiers, key_id) -> (bool, object()):
        print(f"{data=} {data[1]} {data[2]}")
        print(f"{type(data)=} {type(data[1])=}")
        # Déblocage de la touche menu pour utilisation en bluetooth.
        # Utile par exemple dans Esysuite pour ouvrir la barre de menu.
        # if key_id == Keyboard.KeyId.KEY_MENU or key_id == Keyboard.KeyId.KEY_APPLICATIONS:
        if key_id == Keyboard.KeyId.KEY_APPLICATIONS:
            self._put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BLUETOOTH_FUNCTION_EXIT, data=b''))
            self._put_in_function_queue(FunctionId.APPLICATIONS)
            return True

        if not Settings().data['bluetooth']['bt_simul_esys']:
            # If type Esys the virtual key Forward and backward display become JLL and JRR
            if data[1] & 0x01:
                data = b''.join((data[0].to_bytes(1, 'big'),
                                 data[1].to_bytes(1, 'big'),
                                 (data[2] | 0x40).to_bytes(1, 'big')))
            if data[1] & 0x02:
                data = b''.join((data[0].to_bytes(1, 'big'),
                                 data[1].to_bytes(1, 'big'),
                                 (data[2] | 0x80).to_bytes(1, 'big')))
            data = b''.join((data[0].to_bytes(1, 'big'),
                             b'\x00',
                             data[2].to_bytes(1, 'big')))
        # L'ordre semble inversé par rapport à la doc protocol 2007DEV14.
        # Ici on place dans kc_data_pc_protocol "J1 J2 Reserved Switch"
        # mais la doc 2007DEV14 indique que l'ordre pour un esys doit êre "Switch Reserved J2 J1"
        kc_data_pc_protocol = b''.join(((data[2] & 0x0F).to_bytes(1, 'big'),
                                        (data[2] >> 4).to_bytes(1, 'big'),
                                        b'\x00', data[1].to_bytes(1, 'big')))

        log.info("kc_data_pc_protocol={}".format(kc_data_pc_protocol))
        bluetooth_thread_pool.put_message_in_tx_queue(bt_protocol.Frame(bt_protocol.Message(
            key=bt_protocol.Message.KEY_KEYBOARD, subkey=bt_protocol.Message.SUBKEY_KEYBOARD_COMMAND,
            data=kc_data_pc_protocol)))

        return False

    def input_character(self, modifier, character, data) -> bool:
        return False

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        return False

    def exec_interactive(self, data) -> bool:
        bluetooth_thread_pool.put_message_in_tx_queue(bt_protocol.Frame(bt_protocol.Message(
            key=bt_protocol.Message.KEY_KEYBOARD, subkey=bt_protocol.Message.SUBKEY_KEYBOARD_CURSOR_ROUTING,
            data=data[1:3])))
        return False

    def set_braille_display_dots_line(self, dots, blink, start):
        self._braille_display.set_data_line(None, dots, blink, start)

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        bt_active_thread_id = bluetooth_thread_pool.get_active_thread_id()
        if bt_active_thread_id == self._bluetooth_id:
            static_dots = bluetooth_thread_pool.get_static_dots(force_refresh)
            dynamic_dots = bluetooth_thread_pool.get_dynamic_dots(force_refresh)
            # log.error(f"{static_dots=} {dynamic_dots=}")
            # Convert static_dots to string.
            if static_dots:
                str_static_dots = Lou.byte_to_unicode_braille(static_dots)
            else:
                str_static_dots = ""
            # Convert dynamic_dots to string.
            if dynamic_dots:
                str_dynamic_dots = Lou.byte_to_unicode_braille(dynamic_dots)
            else:
                str_dynamic_dots = ""
            # log.error(f"{str_static_dots=} {str_dynamic_dots=}")
            return None, str_static_dots, str_dynamic_dots

        return self._braille_display.get_data_line(force_refresh=force_refresh)

    def activate_channel(self):
        return bluetooth_thread_pool.activate_channel(self._bluetooth_id)

    def get_bluetooth_id(self):
        return self._bluetooth_id
