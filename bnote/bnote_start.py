"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import subprocess
import sys
import threading
import time
import queue
import shutil
from pathlib import Path
import pkg_resources

import bnote.apps.edt.edt as edt
import bnote.apps.edt.math_opy as math
from bnote.debug.colored_log import ColoredLogger
from bnote.tools import bt_util
from bnote.apps.internal import Internal
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
import bnote.tools.crash_report as crash_report
from bnote.bt.bt_thread import bluetooth_thread_pool
import bnote.stm32.stm32_protocol as stm32_protocol
from bnote.stm32.stm32_thread import Stm32Thread
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.braille.lou import Lou
from bnote.tools.settings import Settings
from bnote.tools.swap_file import do_update_swap_file
from bnote.tools.translate import Translate
from bnote.apps.fman.file_manager import BNOTE_FOLDER, DOCUMENTS_FOLDER
from bnote.tools.yaupdater import YAUpdater

# logging.setLoggerClass(ColoredLogger)
# Add ColoredLogger for the comtypes logger (used to log sapi low level API)
edt.logger.addHandler(ColoredLogger(""))
math.logger.addHandler(ColoredLogger(""))
# comtypes.logger.setLevel(logging.DEBUG)
# edt.logger.setLevel(logging.ERROR)

from bnote.debug.colored_log import ColoredLogger, BNOTE_LOG

log = ColoredLogger(__name__)
log.setLevel(BNOTE_LOG)


class BnoteThread(threading.Thread):
    def __init__(self, debug):
        threading.Thread.__init__(self)
        self.debug = debug
        self._running = False
        self._must_restart_service_after_installation = False
        # Create Stm32Thread
        self._stm32_thread = Stm32Thread()
        # Init can be done after Braille device info received from Serial.
        self._bluetooth_init = False
        # True when Braille is in internal mode (file manager, editor, etc...)
        self._internal_mode = False
        # The internal instance
        self._internal = None
        # Init can be done after Braille device info received from Serial.
        self._internal_init = False
        # function queue from application to internal.py module
        self._function_queue = queue.Queue()

    def terminate(self):
        self._running = False

    # call by applications to put function for internal.py module
    def _put_in_function_queue(self, *args, **kwargs):
        log.info("args={} kwargs={}".format(args, kwargs))
        # Pack and put in the queue the tuple args ans the dict kwargs
        self._function_queue.put((args, kwargs))

    def run(self):
        self._running = True
        log.info("OririsThread starts running...")

        # Start communication with stm32
        self._start_stm32_thread()

        while self._running:
            try:
                time.sleep(0.01)

                # Decode a frame from STM32
                if not self._stm32_thread.empty_rx_frame_queue():
                    self._decode_event(self._stm32_thread.get_from_rx_frame_queue())

                # Decode a frame from Bluetooth thread pool and send it to STM32
                if self._bluetooth_init and self._internal_init:
                    # Deal with add / remove Bluetooth link (screen reader can connect / disconnect when it wants.)
                    # self._treat_add_remove_channel(self._bluetooth_thread_pool.get_add_remove_channel())
                    add_remove_channel_data = (
                        bluetooth_thread_pool.get_add_remove_channel()
                    )
                    if add_remove_channel_data is not None:
                        log.info(
                            "add_remove_channel_data={}".format(add_remove_channel_data)
                        )
                        (id_, add, name) = (
                            add_remove_channel_data[0],
                            add_remove_channel_data[1],
                            add_remove_channel_data[2],
                        )
                        if add:
                            self._internal.input_function(
                                FunctionId.FUNCTION_APPEND_BLUETOOTH, id=id_, name=name
                            )
                        else:
                            self._internal.input_function(
                                FunctionId.FUNCTION_REMOVE_BLUETOOTH, id=id_, name=name
                            )

                # Display something in internal mode if needed
                if self._internal_mode:
                    self._refresh_braille_from_internal()

                # Init internal once Braille device characteristics are received.
                if (
                    braille_device_characteristics.is_init_done()
                    and BnoteApp.lou
                    and not self._internal_init
                ):
                    log.info("init internal")
                    # Once the connection between RPi and STM32 is done, update the swap size if needed.
                    do_update_swap_file()

                    self._internal = Internal(
                        BnoteApp.lou,
                        self._put_in_function_queue,
                        self._stm32_thread.put_in_tx_frame_queue,
                    )
                    self._internal_init = True

                # Init bluetooth once Braille device characteristics are received.
                if (
                    braille_device_characteristics.is_init_done()
                    and not self._bluetooth_init
                ):
                    log.info("init bt")
                    # bluetooth_thread_pool = BluetoothThreadPool()
                    self._bluetooth_init = True

                # Execute function ask by application to internal.py module
                if self._internal:
                    if not self._function_queue.empty():
                        (args, kwargs) = self._function_queue.get()
                        log.info(
                            "command from app. args={} kwarg={}".format(args, kwargs)
                        )
                        self._input_function(*args, **kwargs)
            except KeyboardInterrupt:
                self._stm32_thread.terminate_all()
                if bluetooth_thread_pool:
                    bluetooth_thread_pool.terminate_all()
                os.popen("sudo rfcomm release all")
                break

            except Exception as e:
                log.critical("crash...")
                if self.debug:
                    # Running on dev. PC, raise the exception.
                    raise
                # Running on Pi.
                # generate the crash report
                crash_report.generate_report()

                if self._internal:
                    self._internal.cancel_one_second_timer()
                    self._internal.stop_speaking_if_crash()
                    # self._internal.stop_midi_thread()

                self._stm32_thread.terminate_all()

                if bluetooth_thread_pool:
                    bluetooth_thread_pool.terminate_all()

                os.popen("sudo rfcomm release all")
                break

        print("fin du run")

    def cleanup_all(self):
        # Terminate internal stuff
        self._internal.terminate_bnote()
        # Terminate bluetooth
        if bluetooth_thread_pool:
            bluetooth_thread_pool.terminate_all()
        os.popen("sudo rfcomm release all")
        # Release the stm32 serial port
        self._stm32_thread.terminate_all()

    def _input_function(self, *args, **kwargs):
        function_id = args[0]
        if function_id == FunctionId.USB:
            # Send exit Pi to stm32.
            self._stm32_thread.send_internal_exit(kwargs["channel"])
        elif function_id == FunctionId.ASK_SHUTDOWN:
            # Send shutdown request to stm32.
            self._stm32_thread.send_ask_shutown_or_transport(False)
        elif function_id == FunctionId.ASK_TRANSPORT:
            # Send transport request to stm32.
            self._stm32_thread.send_ask_shutown_or_transport(True)
        elif function_id == FunctionId.ASK_TERMINATE_BNOTE_AND_RESTART_SERVICE:
            # print("receive ASK_TERMINATE_BNOTE_AND_RESTART_SERVICE")
            self.cleanup_all()
            self.terminate()
        else:
            self._internal.input_function(*args, **kwargs)
            # Display something in internal mode if needed
        # self._refresh_braille_from_internal()

    def _start_stm32_thread(self):
        # Start Stm32Thread instance
        self._stm32_thread.start()
        # Add "Ask characteristics" in the tx queue.
        self._stm32_thread.send_ask_characteristics()
        # Add "Ask characteristics" in the tx queue. (Sent another frame if the first is misinterpreted)
        self._stm32_thread.send_ask_characteristics()

    def _refresh_braille_from_internal(self, force_refresh=False):
        # force_refresh = True
        static_text, static_dots, dynamic_dots = self._internal.get_data_line(
            force_refresh
        )
        if static_text is not None:
            log.warning(f"{static_text}")
        if static_dots is not None:
            self._stm32_thread.put_display(static_dots, dynamic_dots, static_text)
            # For debug, display the braille.
            if self.debug:
                # Launch from dev. system => Trace allways the braille display.
                print("<{}>-<{}>-<{}>".format(static_text, static_dots, dynamic_dots))
            else:
                log.warning(
                    "<{}>-<{}>-<{}>".format(static_text, static_dots, dynamic_dots)
                )

    def _decode_event(self, event):
        key, data = event
        switcher = {
            stm32_protocol.STM32_LANGUAGE_CHANGE: self._change_language,
            stm32_protocol.STM32_BRAILLE_TABLE_CHANGE: self._change_braille_table,
            stm32_protocol.STM32_DATE_AND_TIME: self._change_date_and_time,
            stm32_protocol.STM32_ENTER_INTERNAL: self._enter_internal,
            stm32_protocol.STM32_EXIT_INTERNAL: self._exit_internal,
            stm32_protocol.STM32_BRAILLE_KEY: self._braille_key,
            stm32_protocol.STM32_COMMAND_KEY: self._command_key,
            stm32_protocol.STM32_INTERACTIVE_KEY: self._interactive_key,
            stm32_protocol.STM32_SHUTDOWN_PI: self._shutdown_pi,
            stm32_protocol.STM32_USB_APP_NAME_CHANGED: self._usb_app_name_changed,
        }
        func = switcher.get(key, None)
        if func is not None:
            func(data)
        else:
            log.warning("No function defined for {}".format(event[0]))

    def _change_language(self, language):
        if isinstance(language, bytes):
            # For old firmware compatibility (Esys firmware). Useless for bnote.
            language = language.decode()
        Translate().install_translation(language)
        # translate and refresh application
        self.__translate_and_refresh()
        # Change the current language for speech
        # if language in SpeechManager().available_speech_languages():
        #    Settings().data['speech']['language'] = language
        #    Settings().save()

    def _change_braille_table(self, language):
        # lib louis (braille transcoding)
        BnoteApp.lou = Lou(language)
        # translate and refresh application
        self.__translate_and_refresh()

    def __translate_and_refresh(self):
        if self._internal is not None:
            self._internal.translate_ui()
            self._refresh_braille_from_internal(True)

    # date_and_time is like "2016-5-24 09:10:00"
    # must be set with "sudo date 052409102016.00" (sudo date MMDDhhmmYYYY.ss)
    def _change_date_and_time(self, data):
        date_and_time = str(data, "utf-8")
        log.info("Change date and time:{}".format(date_and_time))
        # Quand le composant horloge relié au stm32 n'est plus alimenté il fournit un date qui commence par "200-1-1"
        if date_and_time.startswith("200-1-1"):
            # date en echec on utilise 01 décembre 2020 8:30:00
            os.popen("sudo -S date '120108302020.00'")
            return

        if date_and_time.count(" ") == 1:
            wanted_date, wanted_time = date_and_time.split(" ")
            if wanted_time.count(":") == 2 and wanted_date.count("-") == 2:
                hour, minute, second = wanted_time.split(":")
                hour, minute, second = int(hour), int(minute), int(second)
                year, month, day = wanted_date.split("-")
                year, month, day = int(year), int(month), int(day)

                # https://forums.commentcamarche.net/forum/affich-5695150-changer-l-heure-sous-debian
                # date[-u | --utc | --universal][MMDDhhmm[[CC]YY][.ss]]
                log.info(
                    "set date '{:02d}{:02d}{:02d}{:02d}{:04d}.{:02d}'".format(
                        month, day, hour, minute, year, second
                    )
                )
                os.popen(
                    "sudo -S date '{:02d}{:02d}{:02d}{:02d}{:04d}.{:02d}'".format(
                        month, day, hour, minute, year, second
                    )
                )
                if self._internal:
                    # Si on ne met pas le sleep le timer se bloque quand la nouvelle heure < ancienne heure.
                    time.sleep(1)
                    self._internal.start_one_second_timer()

    def _enter_internal(self, data):
        if self._internal:
            self._internal_mode = True
            self._internal.reset_app_menu()
            self._refresh_braille_from_internal(True)

    def _exit_internal(self, data):
        self._internal_mode = False

    def _braille_key(self, data):
        log.info(
            "Braille key : {} self._internal_mode={} self._bluetooth_init={}".format(
                data, self._internal_mode, self._bluetooth_init
            )
        )
        if self._internal_mode:
            done = self._internal.input_braille(data)
            # self._refresh_braille_from_internal(done)
        else:
            log.warning("not in internal mode nor in BT")

    def _command_key(self, data):
        log.info("Command key : {}".format(data))
        if self._internal_mode:
            modifier, key_id = BnoteApp.keyboard.decode_command(data)
            # data is send for bluetooth apps.
            done = self._internal.input_command(data, modifier, key_id)
            # self._refresh_braille_from_internal(done)
        else:
            log.warning("not in internal mode nor in BT")

    def _interactive_key(self, data):
        log.info("Interactive key : {}".format(data))
        if self._internal_mode:
            log.info("internal mode")
            done = self._internal.input_interactive(data)
            # self._refresh_braille_from_internal(done)
        else:
            log.warning("not in internal mode nor in BT")

    def _shutdown_pi(self, data):
        log.info("Shutdown request : {}".format(data))
        if self._internal_mode:
            log.info("internal mode, notify applications...")
            self._internal.shutdown_apps()
        os.popen("/usr/sbin/shutdown -h now")

    def _usb_app_name_changed(self, data):
        # usb_a_name, usb_b_name = data
        # log.error(f"usb name changed {usb_a_name=} {usb_b_name=}")
        if self._internal:
            self._internal.usb_app_name_changed(data)
