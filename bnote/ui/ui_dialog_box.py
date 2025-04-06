"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_button import UiButton
from .ui_container import UiContainer

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG
from .ui_edit_box import UiEditBox
from .ui_label import UiLabel
from .ui_multi_lines_box import UiMultiLinesBox

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiDialogBox(UiContainer):

    def __init__(self, name, item_list, action_cancelable=None, extra_parameters=None):
        """
        Initialization
        :param name: str name of the dialog box.
        :param item_list: The list of ui_object in dialog box (ui_edit_box, ui_checkbox, ui_listbox, ui_button)
        :param action_cancelable: action to call on escape key
        :param extra_parameters: a dict (str name: objects) (default=None)
        When extra_parameters is defined, get_values return values of items of dialog box and this extra_parameter.
        """
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": action_cancelable,
            "ui_objects": item_list,
            "is_root": True,
            "focused_object": 0,
        }
        self.extra_parameters = extra_parameters
        super().__init__(**kwargs)
        # Determines use of ESC key.
        self.action_cancelable = action_cancelable
        if self.is_only_buttons_or_labels():
            # For auto focus dialog, set focus on first editable item and do action on in to enter in editing on editbox
            ui_object = self.set_first_focusable_object()
            if isinstance(ui_object, UiEditBox):
                ui_object.exec_action()
        # Construct braille display.
        self.ask_update_braille_display()

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        return super().get_data_line(force_refresh)

    def get_values(self):
        """
        Get all values in dialog box (Editbox, listbox or checkbox value).
        :return: The list of dict {'value name', value} of items with value in dialog box.
        """
        values = {}
        if self.extra_parameters:
            values = self.extra_parameters
        for ui_object in self.ui_objects:
            value_id, value = ui_object.get_value()
            if value_id:
                values[value_id] = value
        return values

    def set_value(self, value_id, value):
        for ui_object in self.ui_objects:
            object_value_id, object_value = ui_object.get_value()
            if value_id == object_value_id:
                ui_object.set_value(value)

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if stay in menu
        """
        treated = False
        in_menu = True
        if self.is_only_buttons_or_labels():
            if (modifier == 0) and (
                bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN
            ):
                ui_object = self.get_focused_object()
                if not (
                    isinstance(ui_object, UiButton)
                    or isinstance(ui_object, UiMultiLinesBox)
                    or (isinstance(ui_object, UiEditBox) and not ui_object.is_editing())
                ):
                    # Specific function for auto focus dialog box.
                    ui_object = self.set_next_focusable_object()
                    treated, in_menu = ui_object.exec_action()
                    if in_menu:
                        # No refresh if dialogbox is deactivate.
                        self.ask_update_braille_display()
        if not treated:
            # All other keys are treated as container's keys.
            in_menu = super().input_bramigraph(modifier, bramigraph)
        return in_menu

    def is_only_buttons_or_labels(self):
        """
        Check ui object to see if dialogbox is an autofocus dialog.
        :return: True if auto focus dialog.
        """
        is_auto = False
        for ui_object in self.ui_objects:
            if not (isinstance(ui_object, UiLabel) or isinstance(ui_object, UiButton)):
                is_auto = True
                break
        return is_auto

    def set_first_focusable_object(self):
        """
        Put focus on first auto-focus object
        :return:  focused UiObject (focused UiObject could change)
        """
        first_object = self.ui_objects[0]
        for ui_object in self.ui_objects:
            # if not (isinstance(ui_object, UiLabel) or isinstance(ui_object, UiButton)):
            if not (isinstance(ui_object, UiLabel)):
                first_object = ui_object
                break
        self.set_focus(first_object)
        return first_object

    def set_next_focusable_object(self):
        """
        Put focus on first auto-focus object
        :return: None (focused UiObject could change)
        """
        ui_focused_object = self.get_focused_object()
        find_focused = False
        next_focused_object = None
        for ui_object in self.ui_objects:
            if find_focused:
                if not isinstance(ui_object, UiLabel):
                    next_focused_object = ui_object
                    break
            else:
                if ui_object == ui_focused_object:
                    find_focused = True
        if next_focused_object:
            self.set_focus(next_focused_object)
            return next_focused_object
        else:
            return self.set_first_focusable_object()

    def _end_of_container(self, modifier) -> (bool, bool):
        """
        Call by bramigraph escape, exec action_cancelable and exit from dialog box.
        :return: (Treated, stay in menu)
        """
        if self.action_cancelable:
            self.action_cancelable()
            return True, False
        return True, True
