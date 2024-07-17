"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from .ui_list_box import UiListBox

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

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

        super().__init__(name=name, value=(value_id, values), current_index=index)

    def get_value(self):
        return super().get_value()[0], (self.get_index() == 0)

    def get_str_value(self):
        return super().get_value()[0], super().get_value()[1]