"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from enum import Enum
import threading
from bnote.tools.keyboard import Keyboard

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, BRAILLE_DISPLAY_LOG
from bnote.stm32.braille_device_characteristics import braille_device_characteristics

log = ColoredLogger(__name__)
log.setLevel(BRAILLE_DISPLAY_LOG)


class BrailleDisplay:
    """
    This class keeps the data of a full line of text associated to fixed dots, statics dots and dynamics dots line.
    This class provides the information to display on a physical Braille display output of 'length' Braille cells using
    get_data_line() that returns (static_text, static_dots, dynamic_dots)
    This class can decode command Key into function to move the Braille display on the line
    """

    class FunctionId(Enum):
        FORWARD = object()
        BACKWARD = object()
        RIGHT = object()  # first param is the offset wanted value (default value is 1)
        LEFT = object()  # first param is the offset wanted value (default value is 1)
        START = object()
        END = object()
        FAKE_FUNCTION_ID_NOT_DECODED = object()

    def exec_function(self, *arg, **kwargs) -> bool:
        """
        Exec the wanted FunctionId and returns the result
        :param arg:
        :param kwargs:
            FunctionId is passed using the parameter 'func_id'
        :return: None, True or False
            None means the BrailleDisplay don't known what to do with key_func_id.
            True means something has changed and a Braille refresh is needed on the Braille device.
            False means nothing has changed.
        """
        switcher = {
            BrailleDisplay.FunctionId.BACKWARD: self.backward,
            BrailleDisplay.FunctionId.FORWARD: self.forward,
            BrailleDisplay.FunctionId.RIGHT: self._right,
            BrailleDisplay.FunctionId.LEFT: self._left,
            BrailleDisplay.FunctionId.START: self._start,
            BrailleDisplay.FunctionId.END: self._end,
        }

        if 'func_id' in kwargs:
            func = switcher.get(kwargs['func_id'], None)
            if func is not None:
                log.info("Call function={}".format(func))
                return func(*arg, **kwargs)
            else:
                log.warning("No function defined for {}".format(kwargs['func_id']))
        else:
            log.warning("This function must be called with a 'func_id=' parameter.")

    def input_command(self, modifier, key_id) -> bool:
        """
            # Decode the key_id command and do its associated function and returns the (refresh, None).

        :param modifier: command modifier
        :param key_id: command value
        :return: True if command treated, otherwise False
        """
        func_id = self._decode_command(key_id=key_id)
        done = self.exec_function(func_id=func_id)
        return done

    @staticmethod
    def _decode_command(*arg, **kwargs) -> bool:
        """
            # Decode the keyId and return a functionId. Return None if nothing found.
            # FunctionId is passed using the parameter 'func_id'

        :param arg:
        :param kwargs:
        :return:
            True if start position has changed.
            False if start position was already in the last part of the line.
        """
        switcher = {
            Keyboard.KeyId.KEY_BACKWARD: BrailleDisplay.FunctionId.BACKWARD,
            Keyboard.KeyId.KEY_FORWARD: BrailleDisplay.FunctionId.FORWARD,
        }

        if 'key_id' in kwargs:
            func = switcher.get(kwargs['key_id'], None)
            if func is not None:
                return func
            else:
                log.warning("No function defined for {}".format(kwargs['key_id']))
        else:
            log.warning("This function must be called with a 'key_id=' parameter.")
        return False

    def __init__(self):
        self._text_line = ""  # The full line of text
        self._static_dots_line = ""  # The statics dots line of data
        self._dynamic_dots_line = ""  # The dynamics dots line of data
        self._start_pos = 0
        self._mutex = threading.Lock()  # equal to threading.Semaphore(1)

        # Tell that buffers have been updated and must be sent to Braille device.
        self.new_data_available_event = threading.Event()

    def get_start_pos(self):
        with self._mutex:
            return self._start_pos

    def set_start_pos(self, start):
        with self._mutex:
            log.info("self._start_pos={} start={} self._text_line={}".format(self._start_pos, start, self._text_line))
            if start in range(0, len(self._text_line)):
                self._start_pos = start
            log.info("self._start_pos={}".format(self._start_pos))

    def set_data_line(self, text, static_dots, dynamic_dots, start):
        """
        text: (str) the text to viewer display and trace
        static_dots: (str) generally the braille translation of the text
        dynamic_dots: (str) the blinking dots
        start: offset position to start the display
        """
        with self._mutex:
            self._text_line = text
            self._start_pos = 0
            # if text:
            #     if start in range(0, len(text)):
            #         self._start_pos = start
            # elif static_dots:
            if static_dots:
                if start in range(0, len(static_dots)):
                    self._start_pos = start

            self._static_dots_line = static_dots
            self._dynamic_dots_line = dynamic_dots

            self.new_data_available_event.set()

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        """
            Return the (static_text, fixed_dots, static_dots, dynamic_dots) if something changed since the last call
            or if force_refresh=True,
            else return (None, None, None)
        """
        braille_display_length = braille_device_characteristics.get_braille_display_length()
        with self._mutex:
            (text, static_dots, dynamic_dots) = (None, None, None)
            if self.new_data_available_event.is_set() or force_refresh:
                self.new_data_available_event.clear()
                if self._text_line:
                    text = self._text_line[self._start_pos:self._start_pos + braille_display_length]
                else:
                    text = " "
                if self._static_dots_line:
                    static_dots = self._static_dots_line[self._start_pos:self._start_pos + braille_display_length]
                else:
                    static_dots = "\u2800"
                if self._dynamic_dots_line:
                    dynamic_dots = self._dynamic_dots_line[self._start_pos:self._start_pos + braille_display_length]
                else:
                    dynamic_dots = "\u2800"

            # Return data (can be None)
            return text, static_dots, dynamic_dots

    def forward(self, *arg, **kwargs) -> bool:
        """
        Do braille display forward.
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already in the last part of the line.
        """
        braille_display_length = braille_device_characteristics.get_braille_display_length()
        return self._move_right(braille_display_length)

    def backward(self, *arg, **kwargs) -> bool:
        """
        Do braille display backward.
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already 0.
        """
        braille_display_length = braille_device_characteristics.get_braille_display_length()
        return self._move_left(braille_display_length)

    def _right(self, offset=1, *arg, **kwargs) -> bool:
        """
        Do right.
        :param offset: length of move, default is 1
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already.
        """
        return self._move_right(offset)

    def _left(self, offset=1, *arg, **kwargs) -> bool:
        """
        Do left.
        :param offset: length of move, default is 1
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already 0.
        """
        return self._move_left(offset)

    def _start(self, *arg, **kwargs) -> bool:
        """
        Move Braille display at the begin of the line.
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already 0.
        """
        return self._move_left(self.get_start_pos())

    def _end(self, *arg, **kwargs) -> bool:
        """
        Move Braille display at the end of the line
        :param arg: None
        :param kwargs: None
        :return:
            True if start position has changed.
            False if start position was already in the last part of the line.
        """
        return self._move_right(
            len(self._text_line) - self.get_start_pos() - braille_device_characteristics.get_braille_display_length())

    def _move_right(self, offset) -> bool:
        """
        Move the Braille display 'offset' char on the right.
        :param offset: length of move
        :return:
            True if start position has changed
            False if start position was already in the last part of the line.
        """
        if offset == 0:
            return False
        if ((self._text_line and self._start_pos + offset in range(0, len(self._text_line))) or
                (self._static_dots_line and self._start_pos + offset in range(0, len(self._static_dots_line)))):
            self._start_pos += offset
            log.info("next start = {}".format(self._start_pos))
            self.new_data_available_event.set()
            return True

        return False

    def _move_left(self, offset) -> bool:
        """
        Move the Braille display 'offset' char on the left
        :param offset: length of move
        :return:
            True if start position has changed.
            False if start position was already 0.
        """
        if self._start_pos == 0 or offset == 0:
            return False

        if ((self._text_line and (self._start_pos - offset in range(0, len(self._text_line)))) or
                (self._static_dots_line and (self._start_pos - offset in range(0, len(self._static_dots_line))))):
            self._start_pos -= offset
        else:
            self._start_pos = 0

        self.new_data_available_event.set()
        return True

    def center(self, position):
        """
        Define an offset for braille display where position is at the middle of display.
        :param position: caret
        :return: None
        """
        braille_display_length = braille_device_characteristics.get_braille_display_length()
        half_display_length = braille_display_length >> 1
        if position <= half_display_length:
            self._start_pos = 0
        elif len(self._text_line) < braille_display_length:
            self._start_pos = 0
        elif position > len(self._text_line) - half_display_length:
            self._start_pos = len(self._text_line) - braille_display_length
        else:
            self._start_pos = position - half_display_length
