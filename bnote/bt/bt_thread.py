"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.stm32.braille_device_characteristics import braille_device_characteristics
import os
import queue
import re
import serial
import subprocess
import time
import threading
from pathlib import Path
import bnote.bt.bt_protocol as bt_protocol

from bnote.debug.colored_log import ColoredLogger, BT_THREAD_LOG
from bnote.tools.settings import Settings

log = ColoredLogger(__name__)
log.setLevel(BT_THREAD_LOG)


#
# The bluetooth thread pool.
#
class BluetoothThreadPool:
    # Size of the thread pool (the number of bluetooth connexion).
    THREAD_POOL_SIZE = 4
    THREAD_PREFIX = "Thread-BT-"
    DEVICE_PREFIX = "/dev/rfcomm"

    def __init__(self, *args, **kwargs):
        # Bluetooth threads pool.
        self._threads = []
        # active_thread is the BluetoothThread that talks with the stm32.
        self.active_thread = None
        # Ce dictionnaire permet de retrouver le thread à utiliser pour un id de canal
        self._thread_ids = dict()
        # First port index for bluetooth port
        self._first_port_index = 0
        # Ajoute 1 thread dans la liste de thread
        self.add_thread()

    def add_thread(self):
        # log.error(f"len(self._threads) = {len(self._threads)}")
        # Retire les threads qui ne tournent plus de la liste des threads .
        for bt_thread in self._threads:
            if not bt_thread.is_alive():
                self._threads.remove(bt_thread)
        # log.error(f"après nettoyage len(self._threads) = {len(self._threads)}")

        # Construit une liste avec les index associé à chaque thread déja lancé.
        # l'index correspond au X de BluttothThreadPool.device_prefix
        indexes = []
        for bt_thread in self._threads:
            index = int(bt_thread._port.replace(BluetoothThreadPool.DEVICE_PREFIX, ""))
            indexes.append(index)

        # Trouve le premier indice disponible.
        first_available_rfcomm_index = 0
        while first_available_rfcomm_index in indexes:
            first_available_rfcomm_index = first_available_rfcomm_index + 1

        log.info(
            "call os.popen(sudo -S rfcomm listen {})".format(
                BluetoothThreadPool.DEVICE_PREFIX + str(first_available_rfcomm_index)
            )
        )
        os.popen(
            "sudo -S rfcomm listen "
            + BluetoothThreadPool.DEVICE_PREFIX
            + str(first_available_rfcomm_index)
        )

        # Create the Bluetooth threads and queues
        # Create the first Bluetooth thread and append it in the pool.
        bt_thread = BluetoothThread(
            port=BluetoothThreadPool.DEVICE_PREFIX + str(first_available_rfcomm_index),
            add_thread=self.add_thread,
        )
        bt_thread.setName(
            BluetoothThreadPool.THREAD_PREFIX + str(first_available_rfcomm_index)
        )
        self._threads.append(bt_thread)
        # Start the first Bluetooth thread.
        bt_thread.start()

    def terminate_all(self):
        # Terminate all Bluetooth threads
        for bt_thread in self._threads:
            bt_thread.terminate()

    def get_add_remove_channel(self):
        for i, bt_thread in enumerate(self._threads):
            info = bt_thread.get_add_remove_channel()
            if info is not None:
                log.info("i={} info={} [i] + info={}".format(i, info, [i] + info))
                (id_bt, add, name) = info
                if add is True:
                    # Ajoute id:thread dans le dictionnaire
                    self._thread_ids[id_bt] = bt_thread
                else:
                    # Retire id:thread du dictionnaire
                    log.info("_threads_ids delete index {}".format(i))
                    log.info("_threads_ids : {}".format(i))
                    if self._thread_ids.get(id_bt):
                        # Delete element if exists.
                        del self._thread_ids[id_bt]
                return info

        return None

    def activate_channel(self, channel_id):
        if channel_id in self._thread_ids:
            self.active_thread = self._thread_ids[channel_id]
            return True

        return False

    def deactivate_all_channel(self):
        self.active_thread = None

    # Récupère les points Braille statiques à afficher sur la plage Braille.
    def get_static_dots(self, force_refresh=False):
        if self.active_thread is not None:
            if self.active_thread.static_dots_event_is_set() or force_refresh:
                return self.active_thread.get_static_dots()

    # Récupère les points Braille dynamiques à afficher sur la plage Braille.
    def get_dynamic_dots(self, force_refresh=False):
        if self.active_thread is not None:
            if self.active_thread.dynamic_dots_event_is_set() or force_refresh:
                return self.active_thread.get_dynamic_dots()

    # Place les messages du stm 32 dans la file de sortie du port série bluetooth actif.
    def put_message_in_tx_queue(self, message):
        if self.active_thread is not None:
            self.active_thread.put_message_in_tx_queue(message)

    def get_active_thread(self):
        return self.active_thread

    def get_active_thread_id(self):
        for id_, bt_thread in self._thread_ids.items():
            if self.active_thread == bt_thread:
                return id_


#
# The bluetooth thread.
#
class BluetoothThread(threading.Thread):
    TYPE_ESYS_12 = 7
    TYPE_ESYS_40 = 8
    TYPE_BNOTE = 18

    # ---------------------------------------------------------
    class SerialInput(threading.Thread):
        def __init__(
            self,
            serial_port,
            protocol,
            port,
            tx_message_queue,
            add_remove_channel_queue,
            mac_and_friendly_bluetooth_name,
        ):
            threading.Thread.__init__(self)

            self._serial = serial_port
            self._bt_protocol = protocol
            self._port = port
            self._tx_message_queue = tx_message_queue
            self._add_remove_channel_queue = add_remove_channel_queue
            self.mac_and_friendly_bluetooth_name = mac_and_friendly_bluetooth_name
            self._running = False
            self._stop = False
            self.is_connected = False  # True when screen reader have accepted answer to its SI message and send a first

            self._static_dots_mutex = (
                threading.Lock()
            )  # equal to threading.Semaphore(1)
            self._static_dots = b""
            self._dynamic_dots_mutex = (
                threading.Lock()
            )  # equal to threading.Semaphore(1)
            self._dynamic_dots = b""
            # Tell that the static_dots buffer have been updated.
            self._static_dots_event = threading.Event()
            # Tell that the dynamic_dots buffer have been updated.
            self.dynamic_dots_event = threading.Event()

        def run(self):
            self._running = True
            log.info("BT serial inut starts running...")

            byte = b""
            while not self._stop:
                try:
                    # Read one byte from serial
                    byte = self._serial.read()
                    log.debug("BT serialInput : running")
                except serial.SerialException:
                    log.info("BT serial exception dans SerialInput")
                    # Stop the thread.
                    self._stop = True

                if byte:
                    log.debug("{}".format(byte))
                    message = self._bt_protocol.rx_treatment(byte)
                    if message:
                        log.debug("message received is {}".format(message))
                        self._handle_message(message)

            # End of loop
            log.info("SerialInput : end of run...")
            self._running = False

        def is_running(self):
            return self._running

        def terminate(self):
            self._stop = True

        def _handle_message(self, message):
            if (
                message.key() == bt_protocol.Message.KEY_SYSTEM
                and message.subkey() == bt_protocol.Message.SUBKEY_SYSTEM_INFORMATION
            ):
                self._handle_identity_request()
            elif (
                message.key() == bt_protocol.Message.KEY_BRAILLE_DISPLAY
                and message.subkey()
                == bt_protocol.Message.SUBKEY_BRAILLE_DISPLAY_STATIC_DOT
            ):
                with self._static_dots_mutex:
                    self._static_dots = message.data()
                    # log.info("len(self._static_dots)={} self._static_dots={}".format(len(self._static_dots), self._static_dots))
                    self._static_dots_event.set()
            elif (
                message.key() == bt_protocol.Message.KEY_BRAILLE_DISPLAY
                and message.subkey()
                == bt_protocol.Message.SUBKEY_BRAILLE_DISPLAY_DYNAMIC_DOT
            ):
                with self._dynamic_dots_mutex:
                    dots = message.data()
                    log.info("len(dots)={} dots={}".format(len(dots), dots))
                    # Get the static Braille dots part.
                    with self._static_dots_mutex:
                        self._static_dots = dots[0 : int(len(dots) / 2)]
                        self._static_dots_event.set()
                        log.debug(
                            "len(dots)={} int(len(dots)/2)={}".format(
                                len(dots), int(len(dots) / 2)
                            )
                        )
                        log.debug(
                            "len(self._static_dots)={} self._static_dots={}".format(
                                len(self._static_dots), self._static_dots
                            )
                        )

                    # Get the dynamic Braille dots part.
                    self._dynamic_dots = dots[int(len(dots) / 2) :]
                    log.debug(
                        "len(self._dynamic_dots)={} self._dynamic_dots={}".format(
                            len(self._dynamic_dots), self._dynamic_dots
                        )
                    )
                    self.dynamic_dots_event.set()

        def _handle_identity_request(self):
            log.info("_handle_identity_request")
            self.is_connected = True
            # To inform stm32 that a new channel is activated
            self._add_remove_channel_queue.put(
                [
                    int(re.sub("/dev/rfcomm", "", self._port)),
                    True,
                    self.mac_and_friendly_bluetooth_name,
                ]
            )

            # Add messages to answer to SI request in the tx queue
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_NAME,
                        data=braille_device_characteristics.get_name_raw_data(),
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_SHORT_NAME,
                        data="osi",
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_DISPLAY_LENGTH,
                        data=braille_device_characteristics.get_braille_display_length_in_bytes(),
                    )
                )
            )
            if not Settings().data["bluetooth"]["bt_simul_esys"]:
                # Send type b.note
                self._tx_message_queue.put(
                    bt_protocol.Frame(
                        bt_protocol.Message(
                            key=bt_protocol.Message.KEY_SYSTEM,
                            subkey=bt_protocol.Message.SUBKEY_SYSTEM_DEVICE_TYPE,
                            data=BluetoothThread.TYPE_BNOTE,
                        )
                    )
                )
            else:
                # Simul type esys 12 or 40
                if braille_device_characteristics.get_braille_display_length() < 40:
                    self._tx_message_queue.put(
                        bt_protocol.Frame(
                            bt_protocol.Message(
                                key=bt_protocol.Message.KEY_SYSTEM,
                                subkey=bt_protocol.Message.SUBKEY_SYSTEM_DEVICE_TYPE,
                                data=BluetoothThread.TYPE_ESYS_12,
                            )
                        )
                    )
                else:
                    self._tx_message_queue.put(
                        bt_protocol.Frame(
                            bt_protocol.Message(
                                key=bt_protocol.Message.KEY_SYSTEM,
                                subkey=bt_protocol.Message.SUBKEY_SYSTEM_DEVICE_TYPE,
                                data=BluetoothThread.TYPE_ESYS_40,
                            )
                        )
                    )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_OPTIONS,
                        data=bytes(braille_device_characteristics.get_options()),
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_COUNTRY_CODE,
                        data=braille_device_characteristics.get_keyboard_language_country_in_bytes(),
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_PROTOCOL_VERSION,
                        data="1.10test 10.16.2019",
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_SOFTWARE_VERSION,
                        data="V0 10.16.2019",
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_SERIAL_NUMBER,
                        data=braille_device_characteristics.get_serial_number_raw_data(),
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_MAX_FRAME_LENGTH,
                        data=255,
                    )
                )
            )
            self._tx_message_queue.put(
                bt_protocol.Frame(
                    bt_protocol.Message(
                        key=bt_protocol.Message.KEY_SYSTEM,
                        subkey=bt_protocol.Message.SUBKEY_SYSTEM_INFORMATION,
                        data="",
                    )
                )
            )

            log.info("_handle_identity_request info added in queue")

    # ---------------------------------------------------------
    class SerialOutput(threading.Thread):
        def __init__(self, serial_port, protocol, tx_message_queue):
            threading.Thread.__init__(self)

            self._serial = serial_port
            self._stm32_protocol = protocol
            self._tx_frame_queue = tx_message_queue
            self._running = False
            self._stop = False

        def run(self):
            self._running = True
            log.info("BT serial output starts running...")

            byte = b""
            while not self._stop:
                try:
                    # If a message is pending in the sending queue, send it.
                    frame = self._tx_frame_queue.get(timeout=1)
                    log.info("get message from tx queue {}".format(frame))
                    try:
                        self._serial.write(frame.frame())
                    except serial.SerialException as e:
                        log.info("!!!!!!!! serial exception pour {}".format(e))
                        self._stop = True
                except queue.Empty:
                    log.debug("BT serial output : Queue empty !")
                    continue

            # End of loop
            log.info("BT serial output : end of run...")
            self._running = False

        def is_running(self):
            return self._running

        def terminate(self):
            self._stop = True

    # ---------------------------------------------------------
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._running = False
        self._is_open = False
        # Braille buffer.
        self._add_thread = None  # Callback pour ajouter un nouveau thread BT suite à une connexion réussie.
        if "add_thread" in kwargs:
            self._add_thread = kwargs["add_thread"]
        self._port = (
            BluetoothThreadPool.DEVICE_PREFIX + "0"
        )  # Le port série bluetooth à utiliser avec ce thread.
        if "port" in kwargs:
            self._port = kwargs["port"]
        # serial port reading timeout
        self._serial = serial.Serial(timeout=1)
        # The _port (/dev/rfcommx") cannot be put in constructor because it does not yet exist.
        self._serial.port = self._port
        log.info("port={}".format(self._serial.port))

        self._serial_input = None
        self._serial_output = None
        self._tx_message_queue = queue.Queue()  # The frame to send queue
        self._add_remove_channel_queue = (
            queue.Queue()
        )  # Queue to inform bnote that bt channel is open or closed
        self._bt_protocol = bt_protocol.BtProtocol()

    def terminate(self):
        self._running = False

    def run(self):
        self._running = True
        log.info(
            "BluetoothThread {} listening {} starts running...".format(self, self._port)
        )
        while self._running:
            # If port is not open, we try to open it.
            if not self._is_open:
                try:
                    self._serial.open()
                    self._is_open = True
                    log.info(
                        ">>>>>>>>>>>>> self._is_open = True pour {}".format(self._port)
                    )
                    log.info(
                        "BT name={}".format(self._get_mac_and_friendly_bluetooth_name())
                    )
                    # Quand on arrive à ouvrir un port série, on démarre un thread pour le "rfcomm listen suivant" ...
                    if self._add_thread:
                        self._add_thread()

                except serial.SerialException as e:
                    # Fail to open rfcommx
                    # Next try in 100ms
                    time.sleep(0.1)

            # If port is open, we try to read something.
            if self._is_open:
                if self._serial:
                    self._serial_input = self.SerialInput(
                        self._serial,
                        self._bt_protocol,
                        self._port,
                        self._tx_message_queue,
                        self._add_remove_channel_queue,
                        self._get_mac_and_friendly_bluetooth_name(),
                    )
                    self._serial_output = self.SerialOutput(
                        self._serial, self._bt_protocol, self._tx_message_queue
                    )
                    self._serial_input.start()
                    self._serial_output.start()
                    log.info("serial threads running")
                    while (
                        self._running
                        and self._serial_input.is_running()
                        and self._serial_output.is_running()
                    ):
                        # Checks each second that serial communication is all right.
                        time.sleep(1)

                    self._serial_input.terminate()
                    self._serial_output.terminate()
                    log.info(
                        "Avant while self._serial_input.is_running() or self._serial_output.is_running():"
                    )
                    while (
                        self._serial_input.is_running()
                        or self._serial_output.is_running()
                    ):
                        time.sleep(0.01)
                    log.info(
                        "APRES while self._serial_input.is_running() or self._serial_output.is_running():"
                    )
                    self._serial.close()
                    if self._serial_input.is_connected:
                        self._put_remove_channel()
                        # Il faut attendre que bnote_start ait lu le message de retrait du bluetooth
                        while self._add_remove_channel_queue.empty():
                            time.sleep(0.01)

                    self._running = False

        # Ferme le serial proprement
        log.info("BluetoothThread listening on {} ended".format(self._port))

    def _get_bluetooth_mac_address(self):
        # get a dict with "rfcommX" "MAC address".
        rfcomm_info = self._get_rfcomm_info()
        # find the "rfcommX" for the current thread.
        current_rfcomm = re.sub("/dev/", "", self._port)
        if current_rfcomm in rfcomm_info:
            return rfcomm_info[current_rfcomm]
        return ""

    def _get_mac_and_friendly_bluetooth_name(self):
        # Get a dict with "MAC address" "Adaptator's name".
        paired_devices = self._get_paired_devices()
        # Get a dict with "rfcommX" "MAC address".
        rfcomm_info = self._get_rfcomm_info()
        # Find "rfcommX" for the current thread.
        current_rfcomm = re.sub("/dev/", "", self._port)

        log.debug("paired_devices={}".format(paired_devices))
        log.debug("rfcomm_info={}".format(rfcomm_info))
        log.debug("current_rfcomm={}".format(current_rfcomm))

        if current_rfcomm in rfcomm_info:
            if rfcomm_info[current_rfcomm] in paired_devices:
                # Return the name of the screen reader bluetooth adaptor
                log.debug(
                    "bluetooth name:{}".format(
                        paired_devices[rfcomm_info[current_rfcomm]]
                    )
                )
                return " ".join(
                    (
                        rfcomm_info[current_rfcomm],
                        paired_devices[rfcomm_info[current_rfcomm]],
                    )
                )
            else:
                # Return the MAC address
                log.debug("bluetooth name:{}".format(rfcomm_info[current_rfcomm]))
                return " ".join(
                    (rfcomm_info[current_rfcomm], rfcomm_info[current_rfcomm])
                )

        # Return the thread name
        log.debug("bluetooth name:{}".format(self.getName()))
        return " ".join(("00:00:00:00:00:00", self.getName()))

    # Return a dict with "rfcommX" "MAC address".
    def _get_rfcomm_info(self):
        rfcomm_info = dict()
        x = subprocess.Popen(
            ["rfcomm", "-a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        x.wait()
        out = x.stdout.read().decode("utf-8")
        log.debug("rfcomm -a =>{}".format(out))
        err = x.stderr.read().decode("utf-8")
        if err != "":
            log.info("rfcomm -a : error={}".format(err))

        lines = out.split("\n")
        pattern_mac = re.compile("(?:[0-9a-fA-F]:?){12}")
        pattern_rfcomm = re.compile("rfcomm\d+:")
        for line in lines:
            log.debug("rfcomm={}".format(line))
            log.debug(
                "rfcomm.find(re.sub('/dev/', "
                ", self._port)={}".format(line.find(re.sub("/dev/", "", self._port)))
            )
            if line.find(re.sub("/dev/", "", self._port)) == 0:
                rfcomm = re.findall(pattern_rfcomm, line)
                macs = re.findall(pattern_mac, line)
                if len(rfcomm) == 1 and len(macs) == 2:
                    rfcomm_info[re.sub(":", "", rfcomm[0])] = macs[1]

        return rfcomm_info

    # Return a dict with "MAC address" "Adaptator's name".
    def _get_paired_devices(self):
        paired_devices = dict()
        x = subprocess.Popen(
            ["bluetoothctl", "devices", "Paired"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        x.wait()
        raw_paired_devices = x.stdout.read().decode("utf-8")
        log.debug("bluetoothctl devices Paired =>{}".format(raw_paired_devices))
        err = x.stderr.read().decode("utf-8")
        if err != "":
            log.info("bluetoothctl devices Paired: error={}".format(err))

        lines_paired_devices = raw_paired_devices.split("\n")
        for device in lines_paired_devices:
            log.debug("device={}".format(device))
            device = device.replace("Device ", "")
            if len(device.split(" ")) >= 2:
                paired_devices[device.split(" ")[0]] = " ".join(device.split(" ")[1:])

        log.debug("paired_devices={}".format(paired_devices))
        return paired_devices

    def get_static_dots(self):
        if self._serial_input:
            with self._serial_input._static_dots_mutex:
                self._serial_input._static_dots_event.clear()
                return self._serial_input._static_dots

    def get_dynamic_dots(self):
        if self._serial_input:
            with self._serial_input._dynamic_dots_mutex:
                self._serial_input.dynamic_dots_event.clear()
                return self._serial_input._dynamic_dots

    def static_dots_event_is_set(self):
        if self._serial_input:
            return self._serial_input._static_dots_event.is_set()
        else:
            return False

    def dynamic_dots_event_is_set(self):
        if self._serial_input:
            return self._serial_input.dynamic_dots_event.is_set()
        else:
            return False

    def get_add_remove_channel(self):
        try:
            if not self._add_remove_channel_queue.empty():
                return self._add_remove_channel_queue.get()
        except queue.Empty:
            pass
        return None

    def _put_remove_channel(self):
        try:
            log.info("remove_channel")
            self._add_remove_channel_queue.put(
                [
                    int(re.sub("/dev/rfcomm", "", self._port)),
                    False,
                    self._get_mac_and_friendly_bluetooth_name(),
                ]
            )
        except queue.Full:
            log.warning("_add_remove_channel_queue is full !")
            pass

    def put_message_in_tx_queue(self, message):
        try:
            self._tx_message_queue.put(message)
        except queue.Full:
            log.warning("_tx_message_queue is full !")
            pass


bluetooth_thread_pool = BluetoothThreadPool()
