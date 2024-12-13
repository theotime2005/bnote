"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.settings import Settings
from .ui_container import UiContainer
from .ui_object import UiObject

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiDocumentList(UiContainer):
    """
    Object container line of document list item.
    """

    def __init__(self, parent_name, parent_action, list_name, list_action):
        self.braille_type = Settings().data["system"]["braille_type"]

        log.info(f"<{list_name=}>")
        child = [UiListObject(name=list_name, action=list_action)]

        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": parent_name,
            "action": parent_action,
            "ui_objects": child,
            "focused_object": 0,
            "is_root": True,
            "no_grade": True,
        }
        super().__init__(**kwargs)


class UiListObject(UiObject):
    """
    Object child of one file of file manager line
    """

    def __init__(self, name, action):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": action,
            "no_grade": True,
        }
        super().__init__(**kwargs)
