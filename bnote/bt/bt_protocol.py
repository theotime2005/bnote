"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from enum import Enum

from bnote.debug.colored_log import ColoredLogger, BT_PROTOCOL_LOG

log = ColoredLogger(__name__)
log.setLevel(BT_PROTOCOL_LOG)


class Message(object):
    """This class is used to instanciate a message involved in the protocol used between a screnreader and
        the Braille device.

    A message is defined by :
        a message length
        a key
        a sub key
        datas

    """

    #  Constant
    MESSAGE_LENGTH_INDEX = 0
    MESSAGE_KEY_INDEX = 2
    MESSAGE_SUBKEY_INDEX = 3
    MESSAGE_DATA_INDEX = 4
    MAX_LENGTH = 254  # The maximum length of the Message

    # Keys
    KEY_KEYBOARD = b"K"
    KEY_BRAILLE_DISPLAY = b"B"
    KEY_SYSTEM = b"S"

    # Subkeys
    SUBKEY_KEYBOARD_BRAILLE = b"B"
    SUBKEY_KEYBOARD_CURSOR_ROUTING = b"I"
    SUBKEY_KEYBOARD_COMMAND = b"C"
    SUBKEY_BRAILLE_DISPLAY_STATIC_DOT = b"S"
    SUBKEY_BRAILLE_DISPLAY_DYNAMIC_DOT = b"C"
    SUBKEY_SYSTEM_NAME = b"N"
    SUBKEY_SYSTEM_SHORT_NAME = b"H"
    SUBKEY_SYSTEM_SERIAL_NUMBER = b"S"
    SUBKEY_SYSTEM_COUNTRY_CODE = b"L"
    SUBKEY_SYSTEM_DEVICE_TYPE = b"T"
    SUBKEY_SYSTEM_DISPLAY_LENGTH = b"G"
    SUBKEY_SYSTEM_OPTIONS = b"O"
    SUBKEY_SYSTEM_SOFTWARE_VERSION = b"W"
    SUBKEY_SYSTEM_PROTOCOL_VERSION = b"P"
    SUBKEY_SYSTEM_MAX_FRAME_LENGTH = b"M"
    SUBKEY_SYSTEM_INFORMATION = b"I"
    SUBKEY_SYSTEM_BATTERY_STATE = b"B"

    # Data
    DATA_KEYBOARD_CURSOR_ROUTING_CLICK = 0x01
    DATA_KEYBOARD_CURSOR_ROUTING_REPEAT = 0x02
    DATA_KEYBOARD_CURSOR_ROUTING_DOUBLE_CLICK = 0x03

    def __init__(self, *args, **kwargs):
        log.debug("args={}".format(args))
        log.debug("kwargs=".format(kwargs))

        # if args[0] comes from reception from bluetooth (message are bytes)
        if len(args) == 1 and isinstance(args[0], bytes):
            # Check consistancy of message checking the length in the message and the real length of the message.
            if int.from_bytes(
                args[0][
                    Message.MESSAGE_LENGTH_INDEX : Message.MESSAGE_LENGTH_INDEX + 2
                ],
                byteorder="big",
                signed=False,
            ) == len(args[0]):
                self._length = len(
                    args[0]
                )  # 2 bytes for length + 1 byte for the key + 1 byte for the sub key +
                # x data bytes.
                self._key = args[0][
                    Message.MESSAGE_KEY_INDEX : Message.MESSAGE_KEY_INDEX + 1
                ]  # La clef
                self._subkey = args[0][
                    Message.MESSAGE_SUBKEY_INDEX : Message.MESSAGE_SUBKEY_INDEX + 1
                ]
                # Extract and convert the data
                self._data = args[0][Message.MESSAGE_DATA_INDEX : self._length]
        # key, sub key and data are passed as named parameters
        else:
            if "key" in kwargs and "subkey" in kwargs and "data" in kwargs:
                if isinstance(kwargs["data"], int):
                    # If data is an int, we must compute the number of bytes needed for its representation.
                    # FIXME The number of bytes is depending of value but protocol wait for a trame allways the same length.
                    self._length = (
                        4 + (kwargs["data"].bit_length() + 7) // 8
                    )  # 2 length bytes + 1 key byte
                    # + 1 subkey byte + x data bytes.
                else:
                    self._length = 4 + len(
                        kwargs["data"]
                    )  # 2 length bytes + 1 key byte +
                    # 1 subkey byte + x data bytes.
                self._key = kwargs["key"]
                self._subkey = kwargs["subkey"]
                self._data = kwargs["data"]
        log.debug(
            "key={} subkey={} data={} length={}".format(
                self._key, self._subkey, self._data, self._length
            )
        )

    def length(self):
        return bytes([self._length])

    def key(self):
        return self._key

    def subkey(self):
        return self._subkey

    def data(self):
        return self._data

    def message(self):
        # Length must be coded on 2 bytes.
        length = self._length.to_bytes(2, "big")

        data = bytes()
        # Convert datas into bytes.
        if isinstance(self._data, str):
            data = bytes(self._data, "utf-8")
        elif isinstance(self._data, int):
            data = self._data.to_bytes((self._data.bit_length() + 7) // 8, "big")
        elif isinstance(self._data, bytes):
            data = self._data
        elif isinstance(self._data, tuple):
            data = bytes(self._data)
        else:
            log.debug("type(data)={} data={}".format(type(self._data), self._data))
        # Return message
        return bytes().join((length, self._key, self._subkey, data))

    def __str__(self):
        return "key={} subkey={} length={} data={}".format(
            self._key, self._subkey, bytes([self._length]), self._data
        )


class Frame(object):
    STX = b"\x02"
    ETX = b"\x03"
    ACK = b"\x06"

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            # Frame built from received bytes.
            if isinstance(args[0], bytes):
                if args[0][0:1] == Frame.STX and args[0][-1:] == Frame.ETX:
                    self._message = Message(args[0][1:-1])
                else:
                    log.debug("args={}".format(args))
                    self._message = Message(args)
            # Frame built from a Message.
            elif isinstance(args[0], Message):
                self._message = args[0]

    def message(self):
        return self._message

    def frame(self):
        return b"".join((Frame.STX, self._message.message(), Frame.ETX))

    def __str__(self):
        return "message={}".format(self._message)


#  https://docs.python.org/3/library/enum.html
class RxMode(Enum):
    WAIT_STX = 1
    WAIT_MESSAGE_LENGTH = 2
    WAIT_KEY = 3
    WAIT_SUBKEY = 4
    WAIT_DATA = 5


class BtProtocol:
    def __init__(self):
        self._rx_message_buffer = bytes()
        self._rx_message_length = -1
        self._rx_mode = RxMode.WAIT_STX

    def rx_treatment(self, byte):
        # log.info("byte={} type(byte)={}".format(byte, type(byte)))
        if (self._rx_mode == RxMode.WAIT_STX) and (byte == Frame.STX):
            self._rx_message_buffer = bytes()
            self._rx_message_length = -1
            self._rx_mode = RxMode.WAIT_MESSAGE_LENGTH
        elif self._rx_mode != RxMode.WAIT_STX:
            if self._rx_mode == RxMode.WAIT_MESSAGE_LENGTH:
                self._rx_message_buffer += byte
                if len(self._rx_message_buffer) == 2:
                    self._rx_message_length = int.from_bytes(
                        self._rx_message_buffer, "big"
                    )
                    if self._rx_message_length > Message.MAX_LENGTH:
                        log.warning("Error length = {}".format(self._rx_message_length))
                    self._rx_mode = RxMode.WAIT_KEY
            elif self._rx_mode == RxMode.WAIT_KEY:
                self._rx_message_buffer += bytes(byte)
                self._rx_mode = RxMode.WAIT_SUBKEY
            elif self._rx_mode == RxMode.WAIT_SUBKEY:
                self._rx_message_buffer += bytes(byte)
                self._rx_mode = RxMode.WAIT_DATA
            elif self._rx_mode == RxMode.WAIT_DATA:
                if len(self._rx_message_buffer) < self._rx_message_length:
                    self._rx_message_buffer += bytes(byte)
                else:
                    if byte == Frame.ETX:
                        self._rx_mode = RxMode.WAIT_STX
                        log.debug("buffer = {}".format(self._rx_message_buffer))
                        message = Message(self._rx_message_buffer)
                        log.debug("message = {}".format(message))
                        return message
                    else:
                        log.warning("Error received {} instead of ETX".format(byte))
