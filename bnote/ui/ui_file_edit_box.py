"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.apps.bnote_app import BnoteApp
from .ui_edit_box import UiEditBox
from .ui_file_manager_tools import UiFileManagerTools

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiFileEditBox(UiEditBox, UiFileManagerTools):

    def __init__(self, name, value):
        super().__init__(name, value)
        # Overload menu Split filename and type.
        braille_name, self.braille_value = self._convert_file_name_to_braille(
            self._braille_type, value[1]
        )
        # Select only the name
        self._caret.end = len(braille_name)

    def get_value(self):
        text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(
            self._braille_type, "."
        )
        pos = self.braille_value.rfind(braille_separator)
        if pos != -1:
            text_name, ret_pos = BnoteApp.lou.convert_to_text(
                self._braille_type, self.braille_value[0:pos]
            )
            text_suffix, ret_pos = self._convert_suffix_to_text(
                self._braille_type,
                self.braille_value[pos + 1 : len(self.braille_value)],
            )
        else:
            text_name, ret_pos = BnoteApp.lou.convert_to_text(
                self._braille_type, self.braille_value
            )
            text_suffix = ""
        if text_suffix != "":
            value = "".join([text_name, ".", text_suffix])
        else:
            value = text_name
        return self._value_id, value
