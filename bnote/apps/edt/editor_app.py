"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import datetime
import time
from bnote.apps.edt.editor_base_app import EditorBaseApp
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.tools.settings import Settings
import bnote.ui as ui
import bnote.apps.edt.edt as editor
import bnote.apps.edt.math_opy as math
# import bnote.apps.edt.math as math
from bnote.tools.keyboard import Keyboard
from bnote.apps.fman.file_manager import FileManager
from bnote.apps.bnote_app import BnoteApp, FunctionId
from pathlib import Path
import math as mathlib

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG, logging

log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class EditorApp(EditorBaseApp):
    MATH_MENU_ID = object
    INSERT_MENU_ID = object

    def __init__(self, put_in_function_queue, file_name=None, language=None, read_only=False):
        log.info(f"Create EditorApp with {read_only=}")
        super().__init__(put_in_function_queue, file_name, language, read_only)

    @staticmethod
    def known_extension():
        return ".txt", ".mbe", ".docx", ".odt", ".pdf", ".rtf", ".brf", ".epub", ".xlsx"

    def _create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        app_name = _("editor")
        if self.read_only_from_opening:
            app_name = "{}({})".format(app_name, _("read only"))
        return ui.UiMenuBar(
            name=app_name,
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&file"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&close"), action=self._exec_close,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                                   shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4),
                        ui.UiMenuItem(name=_("&save"), action=self._exec_save,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='S'),
                        ui.UiMenuItem(name=_("clean&up"), action=self._exec_cleanup),
                        ui.UiMenuItem(name=_("sta&tistics"), action=self._exec_statistics),
                        ui.UiMenuItem(name=_("&export to .brf"), action=self._exec_export_brf),
                        ui.UiMenuItem(name=_("send se&lection to"), action=self._exec_send_to),
                        # FIXME Pas de traduction à la seconde exécution, on se retrouve avec None comme language ?
                        # ui.UiMenuItem(name=_("&translate selection"), action=self._exec_translate)
                    ]),
                self.create_sub_menu_edit(),
                self.create_sub_menu_goto(),
                self.create_sub_menu_find_replace(),
                ui.UiMenuBar(
                    name=_("&insert"), action=EditorApp.INSERT_MENU_ID,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&result"), action=self._exec_insert_result),
                        ui.UiMenuItem(name=_("&date"), action=self._exec_insert_date),
                        ui.UiMenuItem(name=_("&signature"), action=self._exec_insert_signature),
                    ]),
                self.create_sub_menu_bookmark(),
                ui.UiMenuBar(
                    name=_("&math"), action=EditorApp.MATH_MENU_ID,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&line evaluation"), action=self._exec_math_line_eval,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='M'),
                        ui.UiMenuItem(name=_("&bloc evaluation"), action=self._exec_math_bloc_eval,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='T'),
                    ]),
                self.create_sub_menu_vocalize(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        ui_math_menu = self._menu.get_object(EditorBaseApp.MATH_MENU_ID)
        line, start, end = self.editor.get_line()
        braille = BnoteApp.lou.to_dots_8(line)
        if EDITOR_APP_LOG <= logging.INFO:
            log.info(f"{line=}\n{braille=}")
        if self.is_math(braille) != (None, None):
            ui_math_menu.unhide()
        else:
            ui_math_menu.hide()
        # On traîte l'insertion de l'éditeur
        ui_cleanup = self._menu.get_object(self._exec_cleanup)
        ui_insert = self._menu.get_object(EditorApp.INSERT_MENU_ID)
        if self.editor.read_only:
            ui_cleanup.hide()
            ui_insert.hide()
        else:
            ui_cleanup.unhide()
            ui_insert.unhide()

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

    def _exec_export_brf(self):
        if not self.__dialog_is_reading_file():
            self._current_dialog = ui.UiDialogBox(
                name=_("export to braille"),
                item_list=[
                    ui.UiListBox(name=_("language &encoding"), value=("language", ["FR", "US"]), current_index=0),
                    ui.UiListBox(name=_("&braille type"), value=("braille", [_("grade 1"), _("grade 2")]), current_index=0),
                    ui.UiEditBox(name=_("line &length"), value=("line", "32")),
                    ui.UiEditBox(name=_("lines by &page"), value=("page", "21")),
                    ui.UiEditBox(name=_("&pages by &file"), value=("file", "100")),
                    ui.UiMultiLinesBox(name=_("click &here to enter the first page"), value=("first_page", "")),
                    ui.UiButton(name=_("&export"), action=self._exec_valid_export_brf),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
                ],
                action_cancelable=self._exec_cancel_dialog
            )

    def _exec_valid_export_brf(self, force=False):
        kwargs = self._current_dialog.get_values()
        language_dict = {"FR": "fr_FR", "US": "en_US"}
        braille_dict = {_("grade 1"): 'grade1', _("grade 2"): 'grade2'}
        braille_type = braille_dict[kwargs['braille']]
        language_encoding = language_dict[kwargs['language']]
        if language_encoding == braille_device_characteristics.get_keyboard_language_country():
            braille_language = language_encoding
        else:
            braille_language = braille_device_characteristics.get_keyboard_language_country()
        self._current_dialog = ui.UiInfoDialogBox(_("exporting..."))
        try:
            line_length = int(kwargs['line'])
            page_line = int(kwargs['page'])
            file = int(kwargs['file'])
            first_page = kwargs['first_page']
        except ValueError:
            return self._exec_end_export(activity="failed")
        export = editor.WriteBrfFile(self._get_line, str(self._original_file_name), braille_language, braille_type, line_length, page_line, file, first_page, language_encoding, self._exec_end_export)
        export.start()

    def _exec_end_export(self, activity):
        messages = {'failed': _("the value of character per line, line per page and page per file must be an integer."), 'success': _("exporting was successful."), 'exist': _("an element of the same name already exists, remove it and try again.")}
        self._current_dialog = ui.UiInfoDialogBox(message=messages[activity], action=self._exec_cancel_dialog)

    def _exec_send_to(self):
        if not self.__dialog_is_reading_file():
            if not len(BnoteApp.bluetooth_devices):
                self._current_dialog = ui.UiInfoDialogBox(message=_("not device connected"), action=self._exec_cancel_dialog)
                return
            elif self.editor.selection() is None:
                self._current_dialog = ui.UiInfoDialogBox(message=_("you must select text to send"), action=self._exec_cancel_dialog)
                return
            bluetooth_list = list(BnoteApp.bluetooth_devices.values())
            self._current_dialog = ui.UiDialogBox(
                name=_("send text to"),
                item_list=[
                    ui.UiListBox(name=_("&device"), value=("device_list", bluetooth_list), current_index=0),
                    ui.UiButton(name=_("&ok"), action=self._exec_valid_send_to),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_valid_send_to(self):
        kwargs = self._current_dialog.get_values()
        id_ = None
        for device in BnoteApp.bluetooth_devices:
            if BnoteApp.bluetooth_devices[device] == kwargs['device_list']:
                id_ = device
                break
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("check that the braille type of the document corresponds to the braille type of the screen reader."),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._send_to,
                         action_param={'id_': id_}),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_translate(self):
        # On limite pour le moment la traduction en braille informatique
        if Settings().data['editor']['braille_type'] != "dot-8":
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("you must be in computer braille to use the translation."),
                action=self._exec_cancel_dialog)
            return
        self._put_in_function_queue(FunctionId.FUNCTION_OPEN_TRANSLATOR, **{'source': self.editor.selection()})

    def _send_to(self, id_):
        selection=self.editor.selection().replace("’", "'")
        self._put_in_function_queue(FunctionId.FUNCTION_OPEN_BLUETOOTH, **{'device': id_, 'text': selection, 'encoding': braille_device_characteristics.get_keyboard_language_country()})

    # >>> Key events
    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = super().input_command(data, modifier, key_id)
        if not done:
            # Specific commands treatment.
            pass
        return done

    def input_braille(self, data) -> bool:
        """
        Overload input_braille of bnote_app to do a correct translation of braille to char in dot 6 or 8
        """
        return self._input_braille(
            BnoteApp.keyboard.decode_braille(
                BnoteApp.lou,
                data,
                (self.braille_type == 'grade1') or (self.braille_type == 'grade2')
            ),
            data
        )

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        done = super().input_bramigraph(modifier, bramigraph)
        if not done:
            # Specific commands treatment.
            pass
        return done
    # <<< End of key events.

    def input_function(self, *args, **kwargs) -> bool:
        """
        Function from elf._function_queue of bnote_start.py
        :param args:
        :param kwargs:
        :return: True if function done
        """
        if not len(args):
            return False
        function_id = args[0]
        # Call base class decoding.
        done = super().input_function(*args, **kwargs)
        return done


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
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("result={}".format(result))
                self._math_result = result
                msg = _("result:{}").format(result)
                self._current_dialog = ui.UiInfoDialogBox(message=msg, action=self._exec_cancel_dialog)
            else:
                self._current_dialog = ui.UiInfoDialogBox(message=_("Error forgotten formula start marks"),
                                                       action=self._exec_cancel_dialog)
        except ValueError as er:
            self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        except TypeError as er:
            self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        except math.MathException as er:
            self._current_dialog = ui.UiInfoDialogBox(message=_("Error:{} at pos:{}").format(er.__str__(), er.pos),
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
                    if EDITOR_APP_LOG <= logging.INFO:
                        log.info("Result={}".format(result))
                    self._math_result = result
                    msg = _("result:{}").format(result)
                    self._current_dialog = ui.UiInfoDialogBox(message=msg, action=self._exec_cancel_dialog)
            except ValueError as er:
                self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
            except TypeError as er:
                self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
            except math.MathException as er:
                self._current_dialog = ui.UiInfoDialogBox(message=_("error:{} at pos:{}").format(er.__str__(), er.pos),
                                                       action=self._exec_cancel_dialog)
        else:
            self._current_dialog = ui.UiInfoDialogBox(message=_("error forgotten formula start marks"),
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
            if EDITOR_APP_LOG <= logging.INFO:
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
                        if EDITOR_APP_LOG <= logging.INFO:
                            log.info("Insert result={}".format(result))
                        with self.lock:
                            self.editor.function(editor.Editor.Functions.PUT_STRING, **{'text': "{}".format(result)})
                except math.MathException as er:
                    self._current_dialog = ui.UiInfoDialogBox(message=_("no result"),
                                                           action=self._exec_cancel_dialog)

    def _exec_insert_date(self):
        # Reset LC_TIME parameters to take the current language system
        # locale.setlocale(locale.LC_TIME, '')
        d = datetime.datetime.now()
        with self.lock:
            self.editor.function(
                editor.Editor.Functions.PUT_STRING_BETWEEN_SPACES,
                **{'text': d.strftime(_("%A %d %B %Y"))})

    def _exec_insert_signature(self):
        # Read file ~/signature.txt
        signature = None
        signature_file = None
        try:
            signature_file = open(FileManager.get_root_path() / Path('signature.txt'), 'r')
            signature = signature_file.read()
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("signature:<{}>".format(signature))
        except FileNotFoundError:
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning("Signature file not found.")
        finally:
            if signature_file:
                signature_file.close()
        if signature:
            with self.lock:
                self.editor.function(editor.Editor.Functions.PUT_STRING, **{'text': signature})
            return True, None
        else:
            self._current_dialog = ui.UiInfoDialogBox(
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
        if EDITOR_APP_LOG <= logging.INFO:
            log.info(f"{line=}\n{braille=}")
        parser, table = self.is_math(braille)
        if table:
            # braille mathematics
            parser = parser(table, Settings().data['math']['angle'], BnoteApp.lou)
            if table == math.MathBrailleTable or table == math.MathNemethBrailleTable:
                # Remove math start mark from bnote.braille line.
                line = braille[2: len(line)]
            else:
                # Remove math start mark from text.
                text = self._transform_braille_to_text(line[2: len(line)])
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info(f"{text=}\n{line=}")
                line = text
        if parser:
            math_expression = parser.execute(line)
            tree = math_expression.display_tree()
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("{}".format(tree))
        return math_expression

