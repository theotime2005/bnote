"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_container import UiContainer

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiMenuBar(UiContainer):

    def __init__(self, name, menu_item_list, is_root=False, action=None):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": action,
            "ui_objects": menu_item_list,
            "is_root": is_root,
            "focused_object": 0,
        }
        super().__init__(**kwargs)

    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier:
        :param character:
        :return: (Treated, stay in menu)
        """
        treated, in_menu = False, True
        if self.is_root():
            # Check shortcut key.
            if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
                ui_object = self.get_shortcut_char_in_label(character)
                if ui_object:
                    # Find shortcut => set focus and execute action on this object.
                    self._set_focused_object(ui_object)
                    treated, in_menu = self._action_on_focused_object(modifier)
        return treated, in_menu

    def exec_action(self) -> (bool, bool):
        """
        Overload exec_action of ui_object
        :return:
        """
        log.info(f"exec_action of a menu bar {self.name()=}")
        # Activate sub-menu
        if self._parent:
            if self._parent.is_root():
                log.info("object becomes root")
                self._parent.set_root(False)
                self.becomes_root_menu()
                return True, True
            else:
                # Action on title of menu bar
                log.info("action on title")
                return self.switch_to_parent(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
        else:
            log.info("no parent")
            # Exit of menu bar
            return True, False

    def becomes_root_menu(self):
        self._set_focused_object_to_first()
        self.set_as_root()

    def switch_to_parent(self, modifier) -> (bool, bool):
        """
        Overload switch_to_parent() of ui_container to allow exit from menu when method is called on root menu bar.
        Call when the parent menu bar become the root menu bar
        :return: (Treated, stay in menu)
        """
        if self._switch_to_parent(modifier):
            return True, True
        else:
            # End of menu because switch_to_parent on root menu.
            return True, False

    def _end_of_container(self, modifier) -> (bool, bool):
        """
        Call by bramigraph escape, exit from menu
        :return: (Treated, stay in menu)
        """
        return True, False
