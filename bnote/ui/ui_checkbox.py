"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from ui.ui_list_box import UiListBox

# Setup the logger for this file
from debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiCheckBox(UiListBox):

    CHECKBOX_SEPARATOR = "-"

    def __init__(self, name, value):
        value_id, value_bool = value
        values = [_("yes"), _("no")]
        index = 1
        if isinstance(value_bool, bool):
            if value_bool:
                index = 0
        else:
            raise RuntimeError("invalid value for checkbox")

        super(UiCheckBox, self).__init__(name=name, value=(value_id, values), current_index=index)

    def get_value(self):
        return super(UiCheckBox, self).get_value()[0], (self.get_index() == 0)

    def get_str_value(self):
        return super(UiCheckBox, self).get_value()[0], super(UiCheckBox, self).get_value()[1]