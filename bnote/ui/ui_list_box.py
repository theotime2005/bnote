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

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiListBox(UiObject):
    """

    """

    LISTBOX_SEPARATOR = "-"

    def __init__(self, name, value, current_index=0, extra_parameters=None):
        """
        Initialization.
        :param name: str the name of the list
        :param value: a tupple
            ('str value name', list of str value') or ('str value name', dict of str value: str translated value')
        :param current_index: the selected value in the list (default=0)
        :param extra_parameters: any object(s) (default=None)
        When extra_parameters is defined, get_value return current_index instead of the selected value.
        """
        kwargs = {
            'braille_type': Settings().data['system']['braille_type'],
            'name': name,
            'action': None,
        }
        self._value_id, values = value
        self.__value = None
        self.__dict_values = None
        self._current_index = -1
        self.set_list(values, current_index)
        # Handle extra parameters of value, any object
        self.extra_parameters = extra_parameters
        super().__init__(**kwargs)

    def __set_index(self, current_index):
        if len(self.__value) == 0:
            return -1
        elif current_index < len(self.__value):
            return current_index
        else:
            return 0

    def set_list(self, values, current_index):
        if isinstance(values, dict):
            self.__dict_values = values
            self.__value = list(values.values())
            self._current_index = self.__set_index(current_index)
        elif isinstance(values, list):
            self.__value = values
            self._current_index = self.__set_index(current_index)
        else:
            self._value_id = self.__value = None
            self._current_index = -1
            raise RuntimeError("invalid value for listbox")

    def get_presentation(self):
        """
        Construct presentation for an object
        :return: (name in text, name in braille, braille blinking, list of id of braille length)
        """
        text_objects, braille_objects, braille_blinking, id_array_objects = super().get_presentation()
        if self._current_index == -1:
            value = _("empty list")
        else:
            value = self.__value[self._current_index]
        value, braille_value, pos = BnoteApp.lou.convert_to_braille(self._braille_type, value)
        text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(self._braille_type, UiListBox.LISTBOX_SEPARATOR)
        text_objects = text_separator.join([text_objects, value])
        if self._is_modified_value:
            self._presentation_offset = len(braille_separator) + len(braille_objects)
        else:
            self._presentation_offset = 0
        # Replace the space by braille dot 8
        if not Settings().data['system']['spaces_in_label']:
            braille_value = braille_value.replace("\u2800", "\u2880")
        braille_objects = braille_separator.join([braille_objects, braille_value])
        braille_blinking = "\u2800".join([braille_blinking, "\u2800" * len(braille_value)])
        id_array_objects = [*id_array_objects, *([self._ui_id] * len(braille_separator)), *([self._ui_id] * len(braille_value))]
        return text_objects, braille_objects, braille_blinking, id_array_objects

    # -------------------------------------
    # Notification

    # -------------------------------------
    # Event
    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: keyboard modifiers
        :param character: character
        :param data: data from protocol
        :return: (Treated, stay in menu)
        """
        log.info("modifier={} character={}".format(modifier, character))
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            if character == " ":
                # Space do next value.
                self.__next()
                self.ask_update_braille_display()
            else:
                # Find if first character in list.
                index = self.__find_item(character)
                if index is not None:
                    self._current_index = index
                    self.ask_update_braille_display()
            return True, True
        return False, True

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this bramigraph key.
        :param modifier: keyboard modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        kwargs = Keyboard.decode_modifiers(modifier)
        if kwargs['alt']:
            # alt+key not treated.
            return False, True
        switcher = {
            Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: self.__next,
            Keyboard.BrailleFunction.BRAMIGRAPH_UP: self.__previous,
            Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self.__first,
            Keyboard.BrailleFunction.BRAMIGRAPH_END: self.__last,
            Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: self.__next,
        }
        func = switcher.get(bramigraph, None)
        if func is not None:
            treated, in_menu = func()
            self.ask_update_braille_display()
            return treated, in_menu
        log.warning("No function for bramigraph editbox defined for {}".format(bramigraph))
        return super().exec_bramigraph(modifier, bramigraph)

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        log.info(f"input_command on edit box {self._name}")
        switcher = {
            Keyboard.KeyId.KEY_CARET_UP: self.__previous,
            Keyboard.KeyId.KEY_CARET_DOWN: self.__next,
        }
        func = switcher.get(key_id, None)
        if func is not None:
            treated, in_menu = func()
            self.ask_update_braille_display()
            return treated, in_menu
        log.warning("No function for spinbox defined for {}".format(key_id))
        return False, True

    def exec_interactive(self, modifier, pos, key_type) -> (bool, bool):
        """
        Exec on interactive clic
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param pos: pos in object (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: (Treated, stay in menu)
        """
        log.info(f"Clic on objet {self._name}, {pos=}")
        treated, in_menu = self.__next()
        self.ask_update_braille_display()
        return treated, in_menu

    def __previous(self) -> (bool, bool):
        if self._current_index != -1:
            # Not empty list.
            if self._current_index > 0:
                self._current_index -= 1
            else:
                # back to the first item.
                self._current_index = len(self.__value) - 1
        self._is_modified_value = True
        return True, True

    def __next(self) -> (bool, bool):
        if self._current_index != -1:
            # Not empty list.
            self._current_index += 1
            if self._current_index >= len(self.__value):
                # back to the first item.
                self._current_index = 0
        self._is_modified_value = True
        return True, True

    def __first(self) -> (bool, bool):
        if self._current_index != -1:
            # Not empty list.
            self._current_index = 0
        self._is_modified_value = True
        return True, True

    def __last(self) -> (bool, bool):
        if self._current_index != -1:
            # Not empty list.
            self._current_index = len(self.__value) - 1
        self._is_modified_value = True
        return True, True

    def __find_item(self, text):
        text = text.lower()
        if self._current_index == -1:
            # Empty list
            return None
        # Search from current position
        for index, value in enumerate(self.__value[(self._current_index + 1): len(self.__value)]):
            if value.lower().find(text) == 0:
                return self._current_index + 1 + index
        # Search form begin of the list
        for index, value in enumerate(self.__value[0: self._current_index]):
            if value.lower().find(text) == 0:
                return index
        # Not found.
        return None

    def get_index(self):
        return self._current_index

    def get_value_at_index(self):
        if self._current_index == -1:
            return None
        else:
            return self.__value[self._current_index]

    def get_extra_parameters(self):
        return self.extra_parameters

    def get_value(self):
        if self._current_index == -1:
            # Empty list.
            if self.extra_parameters:
                # When extra parameter defined, return ui object itself.
                return self._value_id, self
            else:
                return self._value_id, None
        if self.extra_parameters:
            # When extra parameter defined, return ui object itself.
            return self._value_id, self
        else:
            if self.__dict_values is None:
                return self._value_id, self.__value[self._current_index]
            else:
                return self._value_id, list(self.__dict_values.keys())[self._current_index]
