"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.debug.colored_log import ColoredLogger, UI_LOG
from bnote.tools.keyboard import Keyboard
from .ui_list_box import UiListBox

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiFileNameListBox(UiListBox):
    """
    This class describe a list of files displayed with their not decorated name.
    (Used to select the backup file by example)
    """

    def __init__(self, name, value):
        # print(f"{value=}")
        # unpack value_id and value.
        value_id, self.__value_list_of_path = value
        # keep only the filename (not the full path) to build the UiListBox.
        filename_value = [filename.name for filename in self.__value_list_of_path]

        super().__init__(name, (value_id, filename_value))
