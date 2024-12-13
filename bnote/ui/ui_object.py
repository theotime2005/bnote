"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import unicodedata
from pathlib import Path

from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiObject:
    """
    Base class of user's interface object
    Characteristics:
        - id
        - braille_type
        - name in text
        - braille_name in braille
        - shortcut character or function key
        - action, it is a callback function (self.action)
        - is_focusable flag, always True in this class
    """

    def __init__(self, **kwargs):
        # **kwargs treatment.
        self._is_default_action = False
        # ui_id is defined after object creation.
        self._ui_id = None
        # ui_id is defined by container after object creation.
        self._parent = None
        # by default, object is unhidden
        self._is_hide = False
        # by default, ui_object is not a container
        self._is_root = False
        # by default, action have no params associated
        self._action_param = None
        # sub attributes of name
        self._name = None
        self.shortcut = None
        self._braille_name = None
        self._braille_type = None
        # shortcut key
        self._shortcut_modifier = None
        self._shortcut_key = None
        # grade1 or grade2 auto conversion
        self.__no_grade = False
        # close dialog box or menu when action is done on object
        self._is_auto_close = True
        parameters = {
            "braille_type": self.set_braille_type,
            "no_grade": self.__set_no_grade,
            "shortcut_modifier": self.__set_shortcut_modifier,
            "shortcut_key": self.__set_shortcut_key,
            "name": self.set_name,
            "action": self.__set_action,
            "action_param": self.__set_action_param,
            "is_root": self.set_root,
            "is_hide": self.__set_hide,
            "is_auto_close": self.__auto_close,
        }
        for name, value in parameters.items():
            # log.info(f"{name=}, {value=}")
            if name in kwargs:
                value(kwargs[name])

        # others characteristics
        self._is_focused = False
        # Set when value of object is modified by user
        # or user has tried to modify the value. (usefull for listbox, editbox...)
        self._is_modified_value = False
        # Current display offset on object (updated by get_presentation)
        self._presentation_offset = 0

    def presentation_offset(self):
        return self._presentation_offset

    def set_braille_type(self, ui_type):
        self._braille_type = ui_type

    def __set_no_grade(self, no_grade):
        self.__no_grade = no_grade

    def name(self):
        return self._name

    def _set_shortcut(self, name):
        # '&' treatment, use '\u2800' as temporary character.
        name = name.replace("&&", "\u2800")
        pos = name.find("&")
        if pos >= 0:
            try:
                self.shortcut = self._unaccented_text(name[pos + 1])
            except IndexError:
                # car '&' alone at the end of the name ?
                pos = -1
        name = name.replace("&", "")
        name = name.replace("\u2800", "&")
        return name, pos

    def set_name(self, name):
        if name is None or len(name) == 0:
            # Ultimate protection to avoid crash, if object has no name, replace it by "?".
            name = "?"
        name, pos = self._set_shortcut(name)
        self._set_name_without_shortcut(name, pos)

    def _set_name_without_shortcut(self, new_name, pos=-1):
        # braille conversion
        self._name, self._braille_name, pos = BnoteApp.lou.convert_to_braille(
            self._braille_type, new_name, pos, self.__no_grade
        )
        # Replace space in name by dot 8.
        if not Settings().data["system"]["spaces_in_label"]:
            self._braille_name = self._braille_name.replace("\u2800", "\u2880")
        # add dot 8 under shortcut character.
        if pos >= 0:
            self._braille_name = "".join(
                [
                    self._braille_name[0:pos],
                    chr(ord(self._braille_name[pos]) + 0x80),
                    self._braille_name[pos + 1 :],
                ]
            )
        # log.info(f"{self._name=}-{self.braille_name=}")

    def __set_shortcut_modifier(self, shortcut_modifier):
        self._shortcut_modifier = shortcut_modifier

    def __set_shortcut_key(self, shortcut_key):
        if isinstance(shortcut_key, str):
            self._shortcut_key = self._unaccented_text(shortcut_key)
        else:
            self._shortcut_key = shortcut_key

    def __set_action(self, action):
        self._action = action

    def __set_action_param(self, action_param):
        self._action_param = action_param

    def action(self):
        return self._action

    def set_root(self, ui_is_root):
        self._is_root = ui_is_root

    def __set_hide(self, ui_is_hide):
        self._is_hide = ui_is_hide

    def __auto_close(self, ui_is_auto_close):
        self._is_auto_close = ui_is_auto_close

    def is_hide(self):
        return self._is_hide

    def hide(self):
        self._is_hide = True
        # self.ask_update_braille_display()

    def unhide(self):
        self._is_hide = False
        # self.ask_update_braille_display()

    def is_root(self):
        return self._is_root

    def is_focused(self):
        return self._is_focused

    # -------------------------------------
    # Accessors
    def set_id(self, ui_id):
        self._ui_id = ui_id

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def get_value(self):
        """
        Get the value of checkbox, editbox, spinbox...
        :return: value_id, value
        """
        return None, None

    def get_id(self):
        return self._ui_id

    def get_action(self):
        return self._action

    def get_presentation(self):
        """
        Construct presentation for an object
        :return: (name in text, name in braille, braille blinking dots,  list of id of braille length
        """
        if self._is_hide or (len(self._braille_name) <= 0):
            return None, None, None, None
        else:
            if not self._is_focused:
                blinking_braille = "\u2800" * len(self._braille_name)
            else:
                blinking_braille = "".join(
                    ["\u28C0", "\u2800" * (len(self._braille_name) - 1)]
                )
            return (
                self._name,
                self._braille_name,
                blinking_braille,
                [self._ui_id] * len(self._braille_name),
            )

    def check_menu_item_key(self, modifier, key):
        if self._is_hide:
            return False
        else:
            if isinstance(key, str):
                return (self._shortcut_modifier == modifier) and (
                    self._shortcut_key == self._unaccented_text(key)
                )
            else:
                return (self._shortcut_modifier == modifier) and (
                    self._shortcut_key == key
                )

    # -------------------------------------
    # Notification

    # -------------------------------------
    # Event
    def on_focus(self, with_speaking):
        """
        ui object focused event
        """
        log.info(f"on_focus {self._name} id:{self._ui_id}")
        # Change focused object state.
        self._is_focused = True
        # FIXME : il faut mettre with_speaking à True dans le bon appel
        # speak(self.name())
        # Speak event
        if with_speaking:
            # Say object name
            # speak(self.name())
            pass

    def on_focus_lost(self, with_speaking):
        """
        ui object focused event
        """
        log.info(f"on_focus lost {self._name} id:{self._ui_id}")
        # Change focused object state.
        self._is_focused = False
        # Presentation offset on value are reset if focus lost
        self._is_modified_value = 0
        self._presentation_offset = 0
        # Speak event
        if with_speaking:
            # Say object name
            pass

    def exec_interactive(self, modifier, relative_pos, key_type) -> (bool, bool):
        """
        Exec on interactive clic
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param relative_pos: pos in object (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: Do exec_action for button, menu...
        This function is overload for object with a value.
        """
        log.info(f"Clic on objet {self._name}, {relative_pos=}")
        return self.exec_action()

    def exec_action(self) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if self._action:
            log.info(f"Execution action on <{self._name}>")
            if self._action_param:
                self._action(**self._action_param)
            else:
                self._action()
            if self._is_auto_close:
                # Always exit from menu or dialog box when action is done on object.
                return True, False
            else:
                # stay in menu or dialog box
                self.ask_update_braille_display()
                return True, True
        # stay in menu or dialog box
        self.ask_update_braille_display()
        return True, True

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        return False, True

    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: keyboard modifiers
        :param character: character
        :param data: data from protocol
        :return: (Treated, stay in menu)
        """
        return False, True

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this command key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        if modifier == 0:
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE:
                return self.exec_character(modifier, " ", b"\x00\x00\x00\x00\x00 ")
            elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
                return self.exec_action()
        return False, True

    def rename_without_shortcut(self, name):
        self._set_name_without_shortcut(name)
        self.ask_update_braille_display()

    def ask_update_braille_display(self):
        if self._parent:
            self._parent.ask_update_braille_display()

    @staticmethod
    def _unaccented_text(character):
        text = character.lower()
        return "".join(
            (
                c
                for c in unicodedata.normalize("NFD", text)
                if unicodedata.category(c) != "Mn"
            )
        )
