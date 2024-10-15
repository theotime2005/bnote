"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import os
from pathlib import Path

from apps.fman.file_manager import Trash, FileManager
from apps.bnote_app import BnoteApp
from tools.keyboard import Keyboard
from tools.settings import Settings
from ui.ui_container import UiContainer
from ui.ui_file_manager_tools import UiFileManagerTools
from ui.ui_object import UiObject

# Setup the logger for this file
from debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiDocumentList(UiContainer):
    """
    Object container line of document list item.
    """

    def __init__(self, parent_name, parent_action, list_name, list_action):
        self.braille_type = Settings().data['system']['braille_type']

        log.info(f"<{list_name=}>")
        child = [UiListObject(name=list_name, action=list_action)]

        kwargs = {
            'braille_type': Settings().data['system']['braille_type'],
            'name': parent_name,
            'action': parent_action,
            'ui_objects': child,
            'focused_object': 0,
            'is_root': True,
            'no_grade': True
        }
        super(UiDocumentList, self).__init__(**kwargs)


class UiListObject(UiObject):
    """
    Object child of one file of file manager line
    """
    def __init__(self, name, action):
        kwargs = {
            'braille_type': Settings().data["system"]['braille_type'],
            'name': name,
            'action': action,
            'no_grade': True,
        }
        super(UiListObject, self).__init__(**kwargs)

