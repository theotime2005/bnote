"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from tools.settings import Settings
from ui.ui_object import UiObject

# Setup the logger for this file
from debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiLabel(UiObject):

    def __init__(self, name):
        kwargs = {
            'braille_type': Settings().data['system']['braille_type'],
            'name': name,
            'action': None,
        }
        super(UiLabel, self).__init__(**kwargs)