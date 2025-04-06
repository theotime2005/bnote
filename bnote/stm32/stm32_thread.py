"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import queue
import serial
import sys
import time
import threading

import bnote.stm32.stm32_protocol as stm32_protocol

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, STM32_THREAD_LOG

log = ColoredLogger(__name__)
log.setLevel(STM32_THREAD_LOG)


#
# The thread that talk with stm32.
#


class Stm32Thread(threading.Thread):
    TIME_OUT_TO_READ = 0.05
    TIME_OUT_TO_WRITE = 0.05
    TIME_OUT_TO_CHECK = 0.05

    TIME_BETWEEN_OUTPUT_FRAMES = 0.01

    # ---------------------------------------------------------
    class SerialInput(threading.Thread):
        def __init__(self, serial_port, protocol, frame_queue):
            threading.Thread.__init__(self)

            self._serial = serial_port
            self._stm32_protocol = protocol
            self._rx_frame_queue = frame_queue
            self._running = False
            self._stop = False

        def run(self):
            self._running = True
            log.info("Stm32Thread starts running...")

            byte = b""
            while not self._stop:
                try:
                    # Read one byte from serial
                    byte = self._serial.read()
                    log.debug("SerialInput : running")
                except serial.SerialException:
                    log.critical("serial exception dans SerialInput")
                    pass

                if byte:
                    log.debug("{}".format(byte))
                    frame = self._stm32_protocol.rx_treatment(byte)
                    if frame:
                        log.info("frame received is {}".format(frame))
                        # Treat frame
                        self._stm32_protocol._decode_frame(frame)

            # End of loop
            log.info("SerialInput : end of run...")
            self._running = False

        def is_running(self):
            return self._running

        def terminate(self):
            self._stop = True

    # ---------------------------------------------------------
    class SerialOutput(threading.Thread):
        def __init__(self, serial_port, protocol, frame_queue):
            threading.Thread.__init__(self)

            self._serial = serial_port
            self._stm32_protocol = protocol
            self._tx_frame_queue = frame_queue
            self._running = False
            self._stop = False

        def run(self):
            self._running = True
            log.info("Stm32Thread starts running...")

            byte = b""
            while not self._stop:
                try:
                    # If a message is pending in the sending queue, send it.
                    frame = self._tx_frame_queue.get(
                        timeout=Stm32Thread.TIME_OUT_TO_WRITE
                    )
                    if isinstance(frame, stm32_protocol.Stm32Frame):
                        buffer = frame.cooked_frame_buffer()
                        log.debug("buffer to send = {}".format(buffer))
                        try:
                            self._serial.write(buffer)
                            time.sleep(Stm32Thread.TIME_BETWEEN_OUTPUT_FRAMES)
                        except serial.SerialException:
                            log.critical("serial exception dans write")
                            pass
                except queue.Empty:
                    log.debug("SerialOutput : Queue empty !")
                    continue

            # End of loop
            log.info("SerialOutput : end of run...")
            self._running = False

        def is_running(self):
            return self._running

        def terminate(self):
            self._stop = True

    # ---------------------------------------------------------
    def __init__(self):
        threading.Thread.__init__(self)
        self._serial = None
        self._serial_input = None
        self._serial_output = None
        self._running = False
        self._stop = False

        self._tx_frame_queue = queue.Queue()  # The frame to send queue
        self._rx_frame_queue = queue.Queue()  # The frame received queue
        self._stm32_protocol = stm32_protocol.Stm32Protocol(self._rx_frame_queue)

        self._display_mutex = threading.Lock()
        self._static_dots = None
        self._dynamic_dots = None
        self._static_text = None
        self._display_to_send = 0

    def run(self):
        self._running = True

        while not self._stop:
            # cf https://pythonhosted.org/pyserial/pyserial_api.html
            # Open serial from RPi from TXD (pin 8) RXD (pin 10) of the 20 pins connector.
            # cf https://pythonhosted.org/pyserial/pyserial_api.html
            # Open serial from RPi from TXD (pin 8) RXD (pin 10) of the 20 pins connector.
            self._serial = serial.Serial(
                "/dev/serial0", 57600, timeout=Stm32Thread.TIME_OUT_TO_READ
            )
            log.info("serial={}".format(self._serial))
            if self._serial:
                self._serial_input = self.SerialInput(
                    self._serial, self._stm32_protocol, self._rx_frame_queue
                )
                self._serial_output = self.SerialOutput(
                    self._serial, self._stm32_protocol, self._tx_frame_queue
                )
                self._serial_input.start()
                self._serial_output.start()
                log.info("serial threads running")
                while (
                    not self._stop
                    and self._serial_input.is_running()
                    and self._serial_output.is_running()
                ):
                    # Checks each second that serial communication is all right.
                    time.sleep(Stm32Thread.TIME_OUT_TO_CHECK)
                    if True:  # self._tx_frame_queue.empty():
                        with self._display_mutex:
                            if self._display_to_send != 0:
                                # if (self._display_to_send == 3) and self._dynamic_dots:
                                #     self.put_in_tx_frame_queue(
                                #         stm32_protocol.Stm32Frame(key=stm32_protocol.KEY_DISPLAY_BLINKINGS_DOTS,
                                #                                   data=self._dynamic_dots))
                                # self._display_to_send -= 1
                                # if (self._display_to_send == 2) and self._static_dots:
                                #     self.put_in_tx_frame_queue(
                                #         stm32_protocol.Stm32Frame(key=stm32_protocol.KEY_DISPLAY_STATICS_DOTS,
                                #                                   data=self._static_dots))
                                # self._display_to_send -= 1
                                # if (self._display_to_send == 1) and self._static_text:
                                #     self.put_in_tx_frame_queue(
                                #         stm32_protocol.Stm32Frame(key=stm32_protocol.KEY_DEBUG_TEXT,
                                #                                   data=self._static_text))
                                if self._display_to_send == 3:
                                    if self._dynamic_dots:
                                        self.put_in_tx_frame_queue(
                                            stm32_protocol.Stm32Frame(
                                                key=stm32_protocol.stm32_keys.KEY_DISPLAY_BLINKINGS_DOTS,
                                                data=self._dynamic_dots,
                                            )
                                        )
                                    if self._static_dots:
                                        self.put_in_tx_frame_queue(
                                            stm32_protocol.Stm32Frame(
                                                key=stm32_protocol.stm32_keys.KEY_DISPLAY_STATICS_DOTS,
                                                data=self._static_dots,
                                            )
                                        )
                                    if self._static_text:
                                        self.put_in_tx_frame_queue(
                                            stm32_protocol.Stm32Frame(
                                                key=stm32_protocol.stm32_keys.KEY_DEBUG_TEXT,
                                                data=self._static_text,
                                            )
                                        )

                                self._display_to_send -= 1

                self._serial_input.terminate()
                self._serial_output.terminate()
                while (
                    self._serial_input.is_running() or self._serial_output.is_running()
                ):
                    time.sleep(0.01)
                self._serial.close()
                self._running = False

            else:
                log.info("Fail to open serial port")

    def terminate_all(self):
        log.info("Serial com stop")
        self._stop = True

    def send_ask_characteristics(self):
        """
        Send ask characteristics request to stm32.
        """
        self.put_in_tx_frame_queue(
            stm32_protocol.Stm32Frame(key=stm32_protocol.stm32_keys.KEY_CHARACTERISTICS)
        )

    def send_ask_shutown_or_transport(self, is_transport):
        """
        Send transport or shutdown request to stm32.
        :param is_transport: True if transport request otherwise shutdown request.
        :return:
        """
        if is_transport:
            self.put_in_tx_frame_queue(
                stm32_protocol.Stm32Frame(
                    key=stm32_protocol.stm32_keys.KEY_ASK_SHUTDOWN_OR_TRANSPORT,
                    data=b"1",
                )
            )
        else:
            self.put_in_tx_frame_queue(
                stm32_protocol.Stm32Frame(
                    key=stm32_protocol.stm32_keys.KEY_ASK_SHUTDOWN_OR_TRANSPORT,
                    data=b"0",
                )
            )

    def send_internal_exit(self, channel):
        """
        Send exit Pi to stm32.
        :param channel: (int) 1 or 2 - usb channel selected
        """
        if channel == 1:
            usb_index = b"0"
        elif channel == 2:
            usb_index = b"1"
        self.put_in_tx_frame_queue(
            stm32_protocol.Stm32Frame(
                key=stm32_protocol.stm32_keys.KEY_INTERNAL_EXIT, data=usb_index
            )
        )

    def put_in_tx_frame_queue(self, data):
        self._tx_frame_queue.put(data)

    def empty_rx_frame_queue(self):
        return self._rx_frame_queue.empty()

    def get_from_rx_frame_queue(self):
        if not self._rx_frame_queue.empty():
            return self._rx_frame_queue.get()
        return None

    def put_display(self, static_dots, dynamic_dots, static_text):
        log.info(f"{static_dots=}, {dynamic_dots=} {static_text=}")
        if static_dots or dynamic_dots or static_text:
            new_static_dots = bytearray()
            # Convert /u28xx comb. to 8 bits.
            for character in static_dots:
                byt = ord(character[0]).to_bytes(2, byteorder="big")
                new_static_dots.append(byt[1])
            new_dynamic_dots = bytearray()
            for character in dynamic_dots:
                byt = ord(character[0]).to_bytes(2, byteorder="big")
                new_dynamic_dots.append(byt[1])

            with self._display_mutex:
                self._static_dots = new_static_dots
                self._dynamic_dots = new_dynamic_dots
                self._static_text = static_text
                self._display_to_send = 3


# -----------------------------------------------
# Unitary test
def main():
    stm32_thread = Stm32Thread()
    stm32_thread.start()
    stm32_thread.put_in_tx_frame_queue(
        stm32_protocol.Stm32Frame(stm32_protocol.KEY_CHARACTERISTICS)
    )
    time.sleep(5)
    stm32_thread.put_in_tx_frame_queue(
        stm32_protocol.Stm32Frame(stm32_protocol.KEY_CHARACTERISTICS)
    )
    stm32_thread.put_in_tx_frame_queue(b"\x0d")

    while True:
        try:
            time.sleep(1)
            pass

        # Exit from while if CTRL+C
        except KeyboardInterrupt:
            log.info("Halt by keyboard")
            stm32_thread.terminate_all()
            break


if __name__ == "__main__":
    main()
