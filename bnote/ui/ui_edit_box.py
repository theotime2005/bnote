"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_object import UiObject
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.tools.clipboard import copy, paste

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class Caret:
    def __init__(self, caret=None):
        if caret:
            self.start = caret.start
            self.end = caret.end
        else:
            self.start = 0
            self.end = 0

    # For print()
    def __str__(self):
        return "Caret start[{}] end[{}]".format(self.start, self.end)

    # Check if a selection is done.
    def is_selection_empty(self):
        if self.start == self.end:
            return True
        else:
            return False

    # clear selection from the end of selection according to its direction.
    def clear_selection_from_last(self):
        self.start = self.last()
        self.end = self.start

    # clear selection from the first coordinate.
    def clear_selection_from_first(self):
        self.start = self.first()
        self.end = self.start

    # return the first caret pos
    def first(self):
        if self.start > self.end:
            return self.end
        else:
            return self.start

    # return the last caret pos
    def last(self):
        if self.start > self.end:
            return self.start
        else:
            return self.end


class UiEditBox(UiObject):
    """
    EditBox dialog.
    The value will be converted to braille during instantiotion.
    The braille value is editing and will be converted to text for STM32 sending
     and by get_value.

    Exemple for a find edit box:
     UiFileEditBox(name=_("&find"), action=self._exec_valid_find_dialog, value=("find_string_id", "last text to find")),

    NOTE: When the value_id of an edit box is "", this editbox is not editable.
    """

    EDIT_BOX_SEPARATOR = "-"

    def __init__(self, name, value, no_grade=False):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": None,
        }
        self._no_grade = no_grade
        # Call base class.
        super().__init__(**kwargs)
        # manage value.
        self._value_id, self._value = value
        if isinstance(self._value, str):
            # Convert text to braille, it is the editing data.
            text, self.braille_value, pos = BnoteApp.lou.convert_to_braille(
                self._braille_type, self._value, -1, self._no_grade
            )
        else:
            self._value_id = None
            self._value = None
            raise RuntimeError("Invalid value for editbox")
        self._caret = Caret()
        self._caret.end = len(self.braille_value)
        self._editing = False

    def set_value(self, value):
        self._value = value
        # compute new braille_value.
        text, self.braille_value, pos = BnoteApp.lou.convert_to_braille(
            self._braille_type, self._value, -1, self._no_grade
        )
        # Set caret to selected complete value.
        self._caret = Caret()
        self._caret.end = len(self.braille_value)

    def get_presentation(self):
        """
        Construct presentation for an object
        :return: (name in text, name in braille, braille blinking dots list of id of braille length
        """
        if self._is_hide:
            return None, None, None, None
        else:
            # Convert braille to text.
            text_objects, braille_objects, braille_blinking, id_array_objects = (
                super().get_presentation()
            )
            # Add a space to braille_value if cart is at the end.
            braille_value = self.braille_value
            if self._editing:
                # if self._caret.last() == len(self.braille_value):
                # Add always one separator to present the caret at the end or put caret with interactive keys.
                braille_value = "".join([self.braille_value, "\u2800"])

            text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(
                self._braille_type, UiEditBox.EDIT_BOX_SEPARATOR
            )
            if self._editing and self._is_modified_value:
                value_offset = self.__center_display(
                    self._caret.last() + 1, braille_value
                )
                self._presentation_offset = (
                    len(braille_separator) + len(braille_objects) + value_offset
                )
            else:
                self._presentation_offset = 0
            self._value, pos = BnoteApp.lou.convert_to_text(
                self._braille_type, self.braille_value, -1, True
            )
            text_objects = text_separator.join([text_objects, self._value])
            # Replace the space by braille dot 8
            if not Settings().data["system"]["spaces_in_label"]:
                braille_value = braille_value.replace("\u2800", "\u2880")
            braille_objects = braille_separator.join([braille_objects, braille_value])

            if self._editing:
                begin_not_blinking = "\u2800" * (
                    len(braille_separator) + self._caret.first()
                )
                blinking = "\u28C0" * (self._caret.last() + 1 - self._caret.first())
                end_not_blinking = "\u2800" * (
                    len(braille_value) - (self._caret.last() + 1)
                )
                braille_blinking = "".join(
                    [braille_blinking, begin_not_blinking, blinking, end_not_blinking]
                )
                log.info(
                    f"length {len(begin_not_blinking)=}={len(blinking)=}={len(end_not_blinking)=}"
                )
            else:
                blinking = "\u2800" * (len(braille_separator) + len(braille_value))
                braille_blinking = "".join([braille_blinking, blinking])
            id_array_objects = [
                *id_array_objects,
                *([self._ui_id] * len(braille_separator)),
                *([self._ui_id] * len(braille_value)),
            ]
            log.info(
                f"length {len(braille_objects)=}={len(braille_blinking)}={len(id_array_objects)}"
            )
            return text_objects, braille_objects, braille_blinking, id_array_objects

    def __center_display(self, position, value):
        """
        Define an offset for braille display where position is at the middle of display.
        :param position: caret
        :return: None
        """
        braille_display_length = (
            braille_device_characteristics.get_braille_display_length()
        )
        half_display_length = braille_display_length >> 1
        if position <= half_display_length:
            start_pos = 0
        elif len(value) < braille_display_length:
            start_pos = 0
        elif position > len(value) - half_display_length:
            start_pos = len(value) - braille_display_length
        else:
            start_pos = position - half_display_length
        return start_pos

    def get_value(self):
        value, pos = BnoteApp.lou.convert_to_text(
            self._braille_type, self.braille_value, -1, self._no_grade
        )
        return self._value_id, value

    def exec_action(self) -> (bool, bool):
        self._switch_edit_mode()
        return True, True

    def is_editing(self):
        return self._editing

    def on_focus_lost(self, with_speaking):
        """
        When edit box lost the focus, it turns off also editing mode.
        :param with_speaking:
        :return:
        """
        # edit mode turn off
        self._editing = False
        super().on_focus_lost(with_speaking)

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        log.info(f"input_command on edit box {self._name}")
        if self._editing:
            kwargs = Keyboard.decode_modifiers(modifier)
            if kwargs["alt"]:
                # alt+key not treated.
                return False, True

            switcher = {
                Keyboard.KeyId.KEY_CARET_RIGHT: self._right,
                Keyboard.KeyId.KEY_CARET_LEFT: self._left,
            }
            func = switcher.get(key_id, None)
            if func is not None:
                treated, in_menu = func(**kwargs)
                self.ask_update_braille_display()
                return treated, in_menu
        log.warning("No function for editbox defined for {}".format(key_id))
        return False, True

    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: keyboard modifiers
        :param character: character
        :param data: data from protocol
        :return: (Treated, stay in menu)
        """
        log.info(f"{modifier=} {character=} {data=}")
        if self._editing:
            kwargs = Keyboard.decode_modifiers(modifier)
            if kwargs["alt"]:
                # Let alt+c to change focus on dialog box.
                return False, True
            if kwargs["ctrl"]:
                # Shortcut Ctrl+... decoding.
                return self.__exec_ctrl_character(kwargs, character)
            if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
                self._input_char(BnoteApp.lou.byte_to_unicode_braille(data[1:2]))
                return True, True
        return False, True

    def __exec_ctrl_character(self, kwargs, character):
        """
        Treat Ctrl+char shortcuts.
        :return: (Treated, stay in menu)
        """
        character_switcher = {
            "a": self.exec_select_all,
            "c": self.__exec_copy,
            "v": self.__exec_paste,
            "x": self.__exec_cut,
        }
        # Get the function from switcher dictionnary
        function = character_switcher.get(character.lower(), None)
        if function:
            # Execute the function
            function(**kwargs)
            self.ask_update_braille_display()
        return True, True

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this bramigraph key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        kwargs = Keyboard.decode_modifiers(modifier)
        if kwargs["alt"]:
            # alt+key not treated.
            return False
        if self._editing:
            switcher = {
                Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: self._right,
                Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: self._left,
                Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self._home,
                Keyboard.BrailleFunction.BRAMIGRAPH_END: self._end,
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: self._backspace,
                Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: self._delete,
            }
            func = switcher.get(bramigraph, None)
            if func is not None:
                treated, in_menu = func(**kwargs)
                self.ask_update_braille_display()
                return treated, in_menu
        log.warning(
            "No function for bramigraph editbox defined for {}".format(bramigraph)
        )
        return super().exec_bramigraph(modifier, bramigraph)

    def exec_interactive(self, modifier, relative_pos, key_type) -> (bool, bool):
        """
        Exec on interactive clic
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param relative_pos: pos in object (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: (Treated, stay in menu)
        """
        log.info(f"Clic on objet {self._name}, {relative_pos=}")
        # Compute relative pos
        text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(
            self._braille_type, UiEditBox.EDIT_BOX_SEPARATOR
        )
        before_value = len(self._braille_name) + len(braille_separator)
        log.info(f"{before_value=}")
        if relative_pos > before_value:
            # Clic on value.
            if self._editing:
                log.info("put_caret at {relative_pos - before_value}")
                self._put_caret(relative_pos - before_value, modifier)
                self.ask_update_braille_display()
                return True, True
        log.info(f"switch edit mode from {self._editing=}")
        # Clic on object name.
        self._switch_edit_mode()
        return True, True

    def exec_select_all(self, **kwargs):
        self._caret = Caret()
        self._caret.end = len(self.braille_value)

    def __exec_copy(self, **kwargs):
        braille_value_selection = self.braille_value[
            self._caret.first() : self._caret.last()
        ]
        log.info(f"{braille_value_selection=}")
        copy(braille_value_selection)

    def __exec_paste(self, **kwargs):
        if not self._caret.is_selection_empty():
            self.__delete_selection()
        # Paste text from clipboard, if the bloc is multilines, paste only the first.
        lines = paste().split("\n")
        if lines[0]:
            text_grade, braille, pos = BnoteApp.lou.convert_to_braille(
                self._braille_type, lines[0]
            )
            log.info(f"{lines[0]=} {braille}")
            # Insert character in the braille string value.
            self.braille_value = "".join(
                [
                    self.braille_value[0 : self._caret.end],
                    braille,
                    self.braille_value[self._caret.end : len(self.braille_value)],
                ]
            )
            # Increment caret position.
            self._caret.end += len(lines[0])
            self._caret.start = self._caret.end
            self._is_modified_value = True

    def __exec_cut(self, **kwargs):
        self.__exec_copy(**kwargs)
        self.__delete_selection()

    def _put_caret(self, pos, modifier):
        """
        Put the caret at a position (answer to interactive clic)
        :param pos: position where put the caret(based 1)
        :param modifier: see Keyboard.BrailleModifier
        :return: No return but Caret position changed.
        """
        log.info(f"{pos=}")
        kwargs = Keyboard.decode_modifiers(modifier)
        log.info(f"{self._caret.is_selection_empty()=}")
        log.info(f"{kwargs=}")
        if self._caret.is_selection_empty() and not kwargs["shift"]:
            # No selection and no shift => put the caret to one position
            log.info("Set caret without selection")
            self._caret.end = pos - 1
            self._caret.start = self._caret.end
        else:
            self._caret.end = pos - 1
            if not kwargs["shift"]:
                # Without shift => caret.start follows.
                self._caret.start = self._caret.end

    def _right(self, **kwargs) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        log.info(f"caret right with {kwargs=}")
        if not self._caret.is_selection_empty() and not kwargs["shift"]:
            self._caret.clear_selection_from_last()
        else:
            # With shift=
            if self._caret.end < len(self.braille_value):
                self._caret.end += 1
            if not kwargs["shift"]:
                self._caret.start = self._caret.end
        self._is_modified_value = True
        return True, True

    def _left(self, **kwargs):
        """
        :return: (Treated, stay in menu)
        """
        log.info(f"caret left with {kwargs=}")
        if not self._caret.is_selection_empty() and not kwargs["shift"]:
            self._caret.clear_selection_from_first()
        else:
            if self._caret.end > 0:
                self._caret.end -= 1
            if not kwargs["shift"]:
                self._caret.start = self._caret.end
        self._is_modified_value = True
        return True, True

    def _home(self, **kwargs):
        """
        :return: (Treated, stay in menu)
        """
        log.info(f"caret home with {kwargs=}")
        if not self._caret.is_selection_empty():
            self._caret.clear_selection_from_first()
        else:
            self._caret.start = 0
            self._caret.end = self._caret.start
        self._is_modified_value = True
        return True, True

    def _end(self, **kwargs):
        """
        :return: (Treated, stay in menu)
        """
        log.info(f"caret end with {kwargs=}")
        if not self._caret.is_selection_empty():
            self._caret.clear_selection_from_last()
        else:
            self._caret.start = len(self.braille_value)
            self._caret.end = self._caret.start
        self._is_modified_value = True
        return True, True

    def _switch_edit_mode(self):
        # Switch edit mode.
        if self._value_id:
            # Enter in edit mode only if value_id is not empty.
            self._editing = not self._editing
            self.ask_update_braille_display()
        if not self._editing:
            self._is_modified_value = False

    def __delete_selection(self):
        self.braille_value = "".join(
            [
                self.braille_value[0 : self._caret.first()],
                self.braille_value[self._caret.last() :],
            ]
        )
        log.info(f"delete selection, new {self.braille_value}")
        self._caret.start = self._caret.first()
        self._caret.end = self._caret.start

    def _backspace(self, **kwargs) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if not self._caret.is_selection_empty():
            self.__delete_selection()
        else:
            if self._caret.end > 0:
                # Remove character in the braille string value.
                self.braille_value = "".join(
                    [
                        self.braille_value[0 : self._caret.end - 1],
                        self.braille_value[self._caret.end : len(self.braille_value)],
                    ]
                )
                self._caret.end -= 1
                self._caret.start = self._caret.end
        self._is_modified_value = True
        return True, True

    def _input_char(self, braille_char):
        if not self._caret.is_selection_empty():
            self.__delete_selection()
        # Insert character in the braille string value.
        self.braille_value = "".join(
            [
                self.braille_value[0 : self._caret.end],
                braille_char,
                self.braille_value[self._caret.end : len(self.braille_value)],
            ]
        )
        # Increment caret position.
        self._caret.end += 1
        self._caret.start = self._caret.end
        self._is_modified_value = True
        # Refresh braille construction
        self.ask_update_braille_display()

    def _delete(self, **kwargs) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if not self._caret.is_selection_empty():
            self.__delete_selection()
            self._is_modified_value = True
        else:
            if self._caret.end < len(self.braille_value):
                # Remove character in the braille string value.
                self.braille_value = "".join(
                    [
                        self.braille_value[0 : self._caret.end],
                        self.braille_value[
                            self._caret.end + 1 : len(self.braille_value)
                        ],
                    ]
                )
                if (self._caret.end < len(self.braille_value)) and (
                    self._caret.end > 0
                ):
                    self._caret.end -= 1
                    self._caret.start = self._caret.end
                self._is_modified_value = True
        return True, True
