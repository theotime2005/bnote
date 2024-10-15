"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from debug.colored_log import ColoredLogger, UI_LOG
from tools.keyboard import Keyboard
from ui.ui_list_box import UiListBox

# Setup the logger for this file
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

        super(UiFileNameListBox, self).__init__(name, (value_id, filename_value))
