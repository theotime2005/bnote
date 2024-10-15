"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import datetime
from apps.edt.editor_base_app import EditorBaseApp
from stm32.braille_device_characteristics import braille_device_characteristics
from tools.settings import Settings
from ui.ui_menu_bar import UiMenuBar
from ui.ui_menu_item import UiMenuItem
from ui.ui_message_dialog_box import UiMessageDialogBox, UiInfoDialogBox
import apps.edt.edt as editor
import apps.edt.math_opy as math
# import apps.edt.math as math
from tools.keyboard import Keyboard
from apps.fman.file_manager import FileManager
from apps.bnote_app import BnoteApp, FunctionId
from pathlib import Path
import math as mathlib

# Setup the logger for this file
from debug.colored_log import ColoredLogger, EDITOR_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class EditorApp(EditorBaseApp):
    MATH_MENU_ID = object

    def __init__(self, put_in_function_queue, file_name=None, language=None):
        super(EditorApp, self).__init__(put_in_function_queue, file_name, language)

    @staticmethod
    def known_extension():
        return ".txt", ".mbe", ".docx", ".odt", ".pdf", ".rtf", ".brf", ".epub", ".xlsx"

    def _create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return UiMenuBar(
            name=_("editor"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                UiMenuBar(
                    name=_("&file"),
                    menu_item_list=[
                        UiMenuItem(name=_("&close"), action=self._exec_close,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                                   shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4),
                        UiMenuItem(name=_("&save"), action=self._exec_save,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='S'),
                        UiMenuItem(name=_("clean&up"), action=self._exec_cleanup),
                        UiMenuItem(name=_("sta&tistics"), action=self._exec_statistics),
                    ]),
                self.create_sub_menu_edit(),
                self.create_sub_menu_goto(),
                self.create_sub_menu_find(),
                UiMenuBar(
                    name=_("&insert"),
                    menu_item_list=[
                        UiMenuItem(name=_("&result"), action=self._exec_insert_result),
                        UiMenuItem(name=_("&date"), action=self._exec_insert_date),
                        UiMenuItem(name=_("&signature"), action=self._exec_insert_signature),
                    ]),
                self.create_sub_menu_bookmark(),
                UiMenuBar(
                    name=_("&math"), action=EditorApp.MATH_MENU_ID,
                    menu_item_list=[
                        UiMenuItem(name=_("&line evaluation"), action=self._exec_math_line_eval,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='M'),
                        UiMenuItem(name=_("&bloc evaluation"), action=self._exec_math_bloc_eval,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='T'),
                    ]),
                UiMenuBar(
                    name=_("&vocalize"),
                    menu_item_list=[
                        UiMenuItem(name=_("&document"), action=self._exec_read_document,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='D'),
                        UiMenuItem(name=_("&paragraph"), action=self._exec_read_paragraph,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='R'),
                        UiMenuItem(name=_("&volume"), action=self._exec_volume),
                        UiMenuItem(name=_("&speed"), action=self._exec_speed),
                    ]),
                UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        ui_math_menu = self._menu.get_object(EditorBaseApp.MATH_MENU_ID)
        line, start, end = self.editor.get_line()
        braille = BnoteApp.lou.to_dots_8(line)
        log.info(f"{line=}\n{braille=}")
        if self.is_math(braille) != (None, None):
            ui_math_menu.unhide()
        else:
            ui_math_menu.hide()

    @staticmethod
    def read_data_file(lou, full_file_name, language, add_line, ended, sheet_name=None):
        return editor.ReadFile(lou, full_file_name, language, add_line, ended, sheet_name)

    def write_data_file(self, lou, full_file_name, get_line, on_end, function):
        return editor.WriteFile(full_file_name, get_line, on_end, function)

    @staticmethod
    def is_math(braille):
        pos = braille.find(''.join([math.b6, math.b3]))
        if pos == 0:
            # braille mathematics
            return math.MathParser, math.MathBrailleTable
        else:
            pos = braille.find(''.join([math.b6, math.b2]))
            if pos == 0:
                # text mathematics
                return math.MathParser, math.MathTextTable
            else:
                pos = braille.find(''.join([math.b56, math.b56]))
                if pos == 0:
                    # braille nemeth mathematics
                    return math.MathNemethParser, math.MathNemethBrailleTable
        return None, None

    # >>> Key events
    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = super(EditorApp, self).input_command(data, modifier, key_id)
        if not done:
            # Specific commands treatment.
            pass
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        done = super(EditorApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # Specific commands treatment.
            pass
        return done
    # <<< End of key events.

    # >>> Specifics menu actions.
    def _exec_math_line_eval(self):
        line, start, end = self.editor.get_line()
        try:
            math_expression = self.compute_line(line)
            if math_expression:
                # Instantiate the class to display result.
                display_result = math.MathResult(
                    Settings().data['math']['format'],
                    Settings().data['math']['precision'],
                    Settings().data['math']['fraction'],
                    braille_device_characteristics.get_message_language_country(),
                )
                res = math_expression.compute()
                if mathlib.isnan(res):
                    raise math.MathException(start, math.MathException.ErrorCode.NOT_EVALUABLE, _("nan value"))
                if mathlib.isinf(res):
                    raise math.MathException(start, math.MathException.ErrorCode.INFINITE_VALUE, _("infinite value"))
                (is_fraction, result) = display_result.display_fraction(res)
                log.info("Result={}".format(result))
                self._math_result = result
                msg = _("result:{}").format(result)
                self._current_dialog = UiInfoDialogBox(message=msg, action=self._exec_cancel_dialog)
            else:
                self._current_dialog = UiInfoDialogBox(message=_("Error forgotten formula start marks"),
                                                       action=self._exec_cancel_dialog)
        except ValueError as er:
            self._current_dialog = UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        except TypeError as er:
            self._current_dialog = UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        except math.MathException as er:
            self._current_dialog = UiInfoDialogBox(message=_("Error:{} at pos:{}").format(er.__str__(), er.pos),
                                                   action=self._exec_cancel_dialog)

    def _exec_math_bloc_eval(self):
        # Determine the start of bloc.
        line, start, end = self.editor.get_line()
        braille = BnoteApp.lou.to_dots_8(line)
        if self.is_math(braille) != (None, None):
            while self.editor.function(editor.Editor.Functions.MOVE_UP, **{'shift': False, 'ctrl': False}):
                line, start, end = self.editor.get_line()
                braille = BnoteApp.lou.to_dots_8(line)
                if self.is_math(braille) == (None, None):
                    self.editor.function(editor.Editor.Functions.MOVE_DOWN, **{'shift': False, 'ctrl': False})
                    break
            # Compute bloc.
            continue_loop = True
            result = None
            try:
                while continue_loop:
                    line, start, end = self.editor.get_line()
                    math_expression = self.compute_line(line)
                    if math_expression:
                        result = math_expression.compute()
                        # Next line
                        continue_loop = self.editor.function(editor.Editor.Functions.MOVE_DOWN,
                                                             **{'shift': False, 'ctrl': False})
                    else:
                        # End of loop
                        continue_loop = False
                # Instantiate the class to display result.
                if result:
                    display_result = math.MathResult(
                        Settings().data['math']['format'],
                        Settings().data['math']['precision'],
                        Settings().data['math']['fraction'],
                        braille_device_characteristics.get_message_language_country(),
                    )
                    (is_fraction, result) = display_result.display_fraction(result)
                    log.info("Result={}".format(result))
                    self._math_result = result
                    msg = _("result:{}").format(result)
                    self._current_dialog = UiInfoDialogBox(message=msg, action=self._exec_cancel_dialog)
            except ValueError as er:
                self._current_dialog = UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
            except TypeError as er:
                self._current_dialog = UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
            except math.MathException as er:
                self._current_dialog = UiInfoDialogBox(message=_("Error:{} at pos:{}").format(er.__str__(), er.pos),
                                                       action=self._exec_cancel_dialog)
        else:
            self._current_dialog = UiInfoDialogBox(message=_("Error forgotten formula start marks"),
                                                   action=self._exec_cancel_dialog)

    def _exec_insert_result(self):
        """
        Insert result of the last computation
        This result is store in 'r' parameters
        :return:
        """
        line = 'r'
        parser = math.MathParser(math.MathTextTable, Settings().data['math']['angle'], BnoteApp.lou)
        if parser:
            math_expression = parser.execute(line)
            tree = math_expression.display_tree()
            log.info("{}".format(tree))
            if math_expression:
                try:
                    result = math_expression.compute()
                    if result:
                        display_result = math.MathResult(
                            Settings().data['math']['format'],
                            Settings().data['math']['precision'],
                            Settings().data['math']['fraction'],
                            braille_device_characteristics.get_message_language_country())
                        (is_fraction, result) = display_result.display_fraction(result)
                        log.info("Insert result={}".format(result))
                        with self.lock:
                            self.editor.function(editor.Editor.Functions.PUT_STRING, **{'text': "{}".format(result)})
                except math.MathException as er:
                    self._current_dialog = UiInfoDialogBox(message=_("no result"),
                                                           action=self._exec_cancel_dialog)

    def _exec_insert_date(self):
        log.warning("Insert date")
        # Reset LC_TIME parameters to take the current language system
        # locale.setlocale(locale.LC_TIME, '')
        d = datetime.datetime.now()
        with self.lock:
            self.editor.function(
                editor.Editor.Functions.PUT_STRING_BETWEEN_SPACES,
                **{'text': d.strftime(_("%A %d %B %Y"))})

    def _exec_insert_signature(self):
        log.warning("Insert signature")
        # Read file ~/signature.txt
        signature = None
        signature_file = None
        try:
            signature_file = open(FileManager.get_root_path() / Path('signature.txt'), 'r')
            signature = signature_file.read()
            log.info("signature:<{}>".format(signature))
        except FileNotFoundError:
            log.warning("Signature file not found.")
        finally:
            if signature_file:
                signature_file.close()
        if signature:
            with self.lock:
                self.editor.function(editor.Editor.Functions.PUT_STRING, **{'text': signature})
            return True, None
        else:
            self._current_dialog = UiInfoDialogBox(
                message=_("signature.txt not found."),
                action=self._exec_cancel_dialog,
            )

    # <<< End of specifics menu actions.

    def compute_line(self, line):
        parser = None
        math_expression = None
        # Usefull to remove fake space when the caret is at the end of the line.
        line = line.rstrip().lstrip()
        # Convert characters in a braille string
        braille = BnoteApp.lou.to_dots_8(line)
        braille = braille.replace("\u2800", " ")
        log.info(f"{line=}\n{braille=}")
        parser, table = self.is_math(braille)
        if table:
            # braille mathematics
            parser = parser(table, Settings().data['math']['angle'], BnoteApp.lou)
            if table == math.MathBrailleTable or table == math.MathNemethBrailleTable:
                # Remove math start mark from braille line.
                line = braille[2: len(line)]
            else:
                # Remove math start mark from text.
                text = self._transform_braille_to_text(line[2: len(line)])
                log.info(f"{text=}\n{line=}")
                line = text
        if parser:
            math_expression = parser.execute(line)
            tree = math_expression.display_tree()
            log.info("{}".format(tree))
        return math_expression

