"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
from pathlib import Path

from bnote.apps.fman.file_manager import Trash, FileManager
from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_container import UiContainer
from .ui_file_manager_tools import UiFileManagerTools
from .ui_object import UiObject

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiFileManagerLine(UiContainer, UiFileManagerTools):
    """
    Object container line of file manager document.
    """

    def __init__(
        self,
        parent_name,
        parent_action,
        file_name,
        file_action,
        selected,
        is_selectable,
    ):
        self.braille_type = Settings().data["system"]["braille_type"]

        log.info(f"<{file_name=}>-<{selected=}>-<{is_selectable=}>")
        child = [
            UiFileManagerObject(
                filename="not yet defined",
                name="not yet defined",
                action=file_action,
                selected=selected,
                is_selectable=is_selectable,
            )
        ]

        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": "not yet defined",
            "action": parent_action,
            "ui_objects": child,
            "focused_object": 0,
            "is_root": True,
            "no_grade": True,
        }
        super().__init__(**kwargs)
        # Overload file name
        friendly_parent_name = self._convert_file_to_braille_text(
            self.braille_type, UiFileManagerLine.friendly_file_name(parent_name)
        )
        friendly_child_name = self._ui_file_name(self.braille_type, file_name)
        self.rename_without_shortcut(friendly_parent_name)
        self.get_focused_object().rename_without_shortcut(friendly_child_name)

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        done = False
        if modifier == 0:
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE:
                ui_object = self.get_focused_object()
                if ui_object and ui_object._is_selectable:
                    ui_object._selected = not ui_object._selected
                    self.ask_update_braille_display()
                    return True
        return super().input_bramigraph(modifier, bramigraph)

    def displayed_file(self) -> str:
        return self.get_focused_object()

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        return super().get_data_line(force_refresh)


class UiFileManagerObject(UiObject, UiFileManagerTools):
    """
    Object child of one file of file manager line
    """

    def __init__(self, filename, name, action, selected, is_selectable):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": action,
            "no_grade": True,
        }
        self._filename = filename
        self._selected = selected
        self._is_selectable = is_selectable

        super().__init__(**kwargs)
        # Overload braille name
        braille_file_name, self.braille_name = self._convert_file_name_to_braille(
            self._braille_type, filename
        )

    def filename(self):
        return self._filename

    def selected(self):
        return self._selected

    def get_presentation(self):
        """
        Construct presentation for an object (overload get_presentation of UiObject)
        :return: (name in text, name in braille, braille blinking dots list of id of braille length
        """
        if self._is_hide:
            return None, None, None, None
        else:
            if self._is_selectable:
                # Add selection indicator.
                if self._selected:
                    indicator = _("s")
                else:
                    indicator = _("n")
                # braille conversion
                text_indicator, braille_indicator, pos = (
                    BnoteApp.lou.convert_to_braille(self._braille_type, indicator, 0)
                )
                name = "".join([indicator, self._name])
                braille_name = "".join([braille_indicator, self._braille_name])
            else:
                # Nothing to add.
                name = self._name
                braille_name = self._braille_name
            return (
                name,
                braille_name,
                "\u2800" * len(braille_name),
                [self._ui_id] * len(braille_name),
            )
