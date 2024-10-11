"""
 bnote project
 Author : Eurobraille
 Date : 2024-08-05
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from enum import Enum, auto

"""
The class UiParamList is used with a ParamDescriptor and current values for a collection of parameters.
Below an initilisation example:

        current_values = {
            'name': 'josephine',
            'is_girl': True,
            'hair length': 'short',
            'hair color': 'black',
            'eyes size': 'small',
            'eyes color': 'blue',
        }

        values = {
            'name': (ParamType.STRING, "default"),
            'is_girl': (ParamType.BOOL, (True, False)),
            'hair': (ParamType.TITLE, ),
            'hair length': (ParamType.TUPLE, ('short', 'to shoulder', 'to lower back')),
            'hair color': (ParamType.TUPLE, ('black', 'blonde', 'venitian', 'brown')),
            'eyes': (ParamType.TITLE, ),
            'eyes size': (ParamType.TUPLE, ('big', 'small')),
            'eyes color': (ParamType.TUPLE, ('blue', 'green', 'gray', 'brown')),
        }

        translation_keys = {
            'name': _("name"),
            'is_girl': _("is grirl"),
            'hair': _("hair"),
            'length': _("length"),
            'color': _("color"),
            'eyes': _("eyes"),
            'size': _("size"),
        }

        translation_values = {
            'yes': _("yes"),
            'no': _("no"),
            'black': _("black"),
            'blonde': _("blonde"),
            'venitian': _("venitian"),
            'brown': _("brown"),
            'blue': _("blue"),
            'green': _("green"),
            'gray': _("gray"),
            'big': _('big'),
            'small': _('small'),
            'short': _("short"),
            'to shoulder': _("to shoulder"),
            'to lower back': _("to lower back"),
        }

    param_descriptor = ParamDescriptor(values, translation_keys, translation_values)
    UiParamList(param_descriptor, values, fn_change_dialog_box, fn_valid, fn_cancel)
    
    def fn_change_dialog_box(self, dialog_box):
        old_current_dialog = self._current_dialog
        self._current_dialog = dialog_box
        return old_current_dialog
    
    def _exec_valid_parameters(self):
        kwargs = self._current_dialog.get_values()
        print(f"_exec_valid_parameters {kwargs}")

"""

from . import UiDialogBox, UiMultiLinesBox, UiEditBox, UiButton, UiCheckBox, UiListBox
from ..tools.keyboard import Keyboard
import copy

class ParamType(Enum):
    TITLE = auto()
    BOOL = auto()
    TUPLE = auto()
    STRING = auto()

class ParamDescriptor:
    def __init__(self, values, translation_keys, translation_values):
        self.values = values
        self.translation_keys = translation_keys
        self.translation_values = translation_values


class UiParamList(UiMultiLinesBox):

    def __init__(self, name, param_descriptor, values, fn_change_dialog_box, fn_valid, fn_cancel):
        self.param_descriptor = param_descriptor
        self.__value_id, input_values = values
        self.values = copy.deepcopy(input_values)
        self.fn_change_dialog_box = fn_change_dialog_box
        self.fn_valid = fn_valid
        self.fn_cancel = fn_cancel
        self.current_dialog = None
        self.root_dialog = None
        text, self.lines = self._parameters_doc()
        super().__init__(name, ("", text), no_grade=False, is_read_only=True,)

    @staticmethod
    def _add_text(param_descriptor, key, value):
        return ''.join((param_descriptor.translation_keys[key], '=', param_descriptor.translation_values[value], '\n'))

    def __short_key(self, key, section):
        if section is None:
            return key
        else:
            return key.replace(section + ' ', '')

    def _parameters_doc(self):
        text = ""
        lines = []
        section = None
        for key, args in self.param_descriptor.values.items():
            param_type = args[0]
            short_key = self.__short_key(key, section)
            if param_type == ParamType.TITLE:
                if text != "":
                    text = ''.join((text, '\n', self.param_descriptor.translation_keys[key], '\n'))
                    lines.append((None, None, False))
                    lines.append((None, key, True))
                else:
                    text = ''.join((self.param_descriptor.translation_keys[key], '\n'))
                    lines.append((None, key, True))
                section = key
            elif param_type == ParamType.BOOL:
                # print(f"{key=} is bool")
                value = self.values[key]
                if value:
                    text = ''.join((text, self._add_text(self.param_descriptor, short_key, 'yes')))
                else:
                    text = ''.join((text, self._add_text(self.param_descriptor, short_key, 'no')))
                lines.append((key, section, section is None))
            elif param_type == ParamType.TUPLE:
                # print(f"{key=} is tuple")
                value = self.values[key]
                text = ''.join((text, self._add_text(self.param_descriptor, short_key, value)))
                lines.append((key, section, section is None))
            elif param_type == ParamType.STRING:
                # print(f"{key=} is str")
                value = self.values[key]
                text = ''.join((text, self.param_descriptor.translation_keys[short_key], '=', value, '\n'))
                lines.append((key, section, section is None))
            else:
                raise KeyError
        text = ''.join((text, "\n", _("ok"), "\n", _("cancel")))
        lines.append((None, None, False))
        lines.append(("__ok__", None, True))
        lines.append(("__cancel__", None, True))
        return text, lines

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        if not self._editing:
            return super().exec_command(modifier, key_id)
        elif key_id == Keyboard.KeyId.KEY_CARET_LEFT:
            self._previous_section()
            return True, True
        elif key_id == Keyboard.KeyId.KEY_CARET_RIGHT:
            self._next_section()
            return True, True
        else:
            return super().exec_command(modifier, key_id)

    def _next_section(self):
        index = self._editor.current_paragraph_index()
        index += 1
        while index < len(self.lines):
            key, section, is_title = self.lines[index]
            if is_title:
                self._editor.set_caret_on_paragraph(index)
                self._update_braille_display()
                break
            index += 1

    def _previous_section(self):
        index = self._editor.current_paragraph_index()
        index -= 1
        while index >= 0:
            key, section, is_title = self.lines[index]
            if is_title:
                self._editor.set_caret_on_paragraph(index)
                self._update_braille_display()
                break
            index -= 1

    def do_interactive(self, modifier, relative_pos, key_type) -> (bool, bool):
        """
        Exec on interactive clic
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param relative_pos: pos in object (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: (Treated, stay in menu)
        """
        if self._editing and key_type == Keyboard.InteractiveKeyType.CLIC:
            return self.__exec_action_on_line()
        return super().do_interactive(modifier, relative_pos, key_type)

    def __exec_action_on_line(self):
        index = self._editor.current_paragraph_index()
        try:
            key, section, is_title = self.lines[index]
            if key == "__ok__":
                self.fn_valid()
                return True, False
            elif key == "__cancel__":
                self.fn_cancel()
                return True, False
            else:
                short_key = self.__short_key(key, section)
                if key not in self.values.keys():
                    # Action on title
                    return True, True
        except IndexError:
            return self.exec_bramigraph(0, Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE)
        self.current_dialog = self._param_dialog(key, short_key)
        self.root_dialog = self.fn_change_dialog_box(self.current_dialog)
        return True, True

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this bramigraph key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        if not self._editing:
            return super().exec_bramigraph(modifier, bramigraph)
        elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
            return self.__exec_action_on_line()
        else:
            return super().exec_bramigraph(modifier, bramigraph)

    def _param_dialog(self, key, short_key):
        # print(f"{key=}")
        value = self.values[key]
        param_type = self.param_descriptor.values[key][0]
        if param_type == ParamType.BOOL:
            return UiDialogBox(
                name=_("parameter"),
                item_list=[
                    UiCheckBox(name=self.param_descriptor.translation_keys[short_key], value=(key, self.values[key])),
                    UiButton(name=_("&ok"), action=self._exec_valid_dialog),
                    UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif param_type == ParamType.TUPLE:
            return UiDialogBox(
                name=_("parameter"),
                item_list=[
                    UiListBox(name=self.param_descriptor.translation_keys[short_key],
                              value=(key, {key: self.param_descriptor.translation_values[key] for key in self.param_descriptor.values[key][1]}),
                              current_index=(self.param_descriptor.values[key][1]).index(self.values[key])),
                    UiButton(name=_("&ok"), action=self._exec_valid_dialog),
                    UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif param_type == ParamType.STRING:
            return UiDialogBox(
                name=_("parameter"),
                item_list=[
                    UiEditBox(name=self.param_descriptor.translation_keys[short_key], value=(key, self.values[key])),
                    UiButton(name=_("&ok"), action=self._exec_valid_dialog),
                    UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_valid_dialog(self):
        # print("_exec_valid_dialog")
        kwargs = self.current_dialog.get_values()
        # print(f"{kwargs=}")
        if len(kwargs) == 1:
            key, value = list(kwargs.items())[0]
        else:
            raise ValueError("kwargs is not one element object.")
        self.values[key] = value
        text, self.lines = self._parameters_doc()
        self.replace_text(text)
        self.current_dialog = None
        self.fn_change_dialog_box(self.root_dialog)
        self._update_braille_display()

    def _exec_cancel_dialog(self):
        # print("_exec_cancel_dialog")
        self.current_dialog = None
        self.fn_change_dialog_box(self.root_dialog)
        self._update_braille_display()

    def get_value(self):
        return self.__value_id, self.values
