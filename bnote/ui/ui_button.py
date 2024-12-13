"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.settings import Settings
from .ui_object import UiObject

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiButton(UiObject):

    def __init__(self, name, action, action_param=None, is_auto_close=True):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": action,
            "action_param": action_param,
            "is_auto_close": is_auto_close,
        }
        super().__init__(**kwargs)
