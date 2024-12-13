"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_object import UiObject

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiMenuItem(UiObject):

    def __init__(
        self,
        name,
        action,
        action_param=None,
        is_hide=False,
        shortcut_modifier=None,
        shortcut_key=None,
    ):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "shortcut_modifier": shortcut_modifier,
            "shortcut_key": shortcut_key,
            "action": action,
            "action_param": action_param,
            "is_hide": is_hide,
        }
        super().__init__(**kwargs)

    def set_name(self, name):
        if name is None or len(name) == 0:
            # Ultimate protection to avoid crash, if object has no name, replace it by "?".
            name = "?"
        name, pos = self._set_shortcut(name)
        if (
            Settings().data["system"]["shortcuts_visible"]
            and self._shortcut_modifier is not None
        ):
            modifier_str = ""
            modifier = Keyboard.decode_modifiers(self._shortcut_modifier)
            if modifier["shift"]:
                modifier_str = "".join((modifier_str, "shift+"))
            if modifier["ctrl"]:
                modifier_str = "".join((modifier_str, "ctrl+"))
            if modifier["alt"]:
                modifier_str = "".join((modifier_str, "alt+"))
            if modifier["win"]:
                modifier_str = "".join((modifier_str, "win+"))
            # log.error(f"{type(self._shortcut_key)}-{self._shortcut_key}")
            if isinstance(self._shortcut_key, Keyboard.BrailleFunction):
                shortcut_str = Keyboard().BrailleFunction.get_bramigraph_label(
                    self._shortcut_key
                )
            else:
                shortcut_str = str(self._shortcut_key)
            name = "-".join((name, f"{modifier_str}{shortcut_str}"))
        self._set_name_without_shortcut(name, pos)
