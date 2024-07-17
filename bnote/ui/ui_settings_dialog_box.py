"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from .ui_button import UiButton
from .ui_checkbox import UiCheckBox
from .ui_dialog_box import UiDialogBox
from .ui_edit_box import UiEditBox
from .ui_label import UiLabel

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG
from .ui_list_box import UiListBox

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiSettingsDialogBox(UiDialogBox):
    def __init__(self, dialog_name, value_name, value, valid_values, action_validation, action_cancelable=None):
        log.info(f"{dialog_name=} {value_name=} {value=} {valid_values=} {action_validation=} {action_cancelable=}")

        objects_list = []

        if isinstance(value, bool):
            objects_list.append(UiCheckBox(value_name, ("value_bool", value)))

        elif isinstance(value, str) or isinstance(value, int):
            if isinstance(value, int):
                value = str(value)
            if isinstance(valid_values, tuple) or isinstance(valid_values, list):
                objects_list.append(UiListBox(value_name, ("value_str", list(valid_values)), valid_values.index(value)))
            else:
                objects_list.append(UiEditBox(value_name, ("value_str", value)))


        # Append Ok and Cancel buttons.
        objects_list.append(UiButton(name=_("&ok"), action=self.do_validation))
        objects_list.append(UiButton(name=_("&cancel"), action=action_cancelable))

        kwargs = {
            'name': dialog_name,
            "item_list": objects_list,
            "action_cancelable": action_cancelable,
        }
        super().__init__(**kwargs)
        self.action_validation = action_validation

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        return super().get_data_line(force_refresh)

    def do_validation(self, **kwargs):
        log.info(f"{kwargs=}")

        values = self.get_values()
        new_value = None
        if "value_bool" in values:
            new_value = values["value_bool"]
        elif "value_str" in values:
            new_value = values["value_str"]

        self.action_validation(new_value)
