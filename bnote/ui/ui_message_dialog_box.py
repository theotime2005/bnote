"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from .ui_button import UiButton
from .ui_dialog_box import UiDialogBox
from .ui_label import UiLabel

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiMessageDialogBox(UiDialogBox):
    """
    Dialog box with the following children :
        A buttons list at begin and end of children list
        A message
    """

    def __init__(
        self, name, message, buttons, action_cancelable=None, extra_parameters=None
    ):
        # Duplicate buttons before and after other items.
        if buttons:
            objects_list = buttons + [UiLabel(name=message)] + buttons
        else:
            objects_list = [UiLabel(name=message)]
        kwargs = {
            "name": name,
            "action_cancelable": action_cancelable,
            "item_list": objects_list,
            "extra_parameters": extra_parameters,
        }
        super().__init__(**kwargs)

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        return super().get_data_line(force_refresh)


class UiInfoDialogBox(UiMessageDialogBox):
    """
    Information dialog box with the following children :
        A message
        A button 'ok', its action is the same as cancel.
    """

    def __init__(self, message, action=None, action_param=None, extra_parameters=None):
        if action:
            super().__init__(
                name=_("information"),
                message=message,
                buttons=[
                    UiButton(name=_("&ok"), action=action, action_param=action_param),
                ],
                action_cancelable=action,
                extra_parameters=extra_parameters,
            )
        else:
            super().__init__(
                name=_("information"),
                message=message,
                buttons=None,
                action_cancelable=None,
            )

    def change_label(self, new_label):
        ui_label = None
        for ui_object in self.ui_objects:
            if isinstance(ui_object, UiLabel):
                ui_label = ui_object
                break
        if ui_label:
            ui_label.set_name(new_label)
        self.ask_update_braille_display()
