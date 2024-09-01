"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import os
from pathlib import Path

from bnote.apps.fman.file_manager import FileManager
from bnote.apps.braille_learning.operation import Operation
from bnote.apps.braille_learning.level_manage import ManageLevel, ManageScore
from bnote.apps.braille_learning import app_version
from bnote.tools.audio_player import AudioPlayer
from bnote.tools.speech_wrapper import speak
from bnote.tools.settings import Settings
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
import bnote.ui as ui
# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, OPERATION_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(OPERATION_APP_LOG)


class OperationApp(BnoteApp):
    """
    App to learn braille with operation
    """

    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super().__init__(put_in_function_queue)
        # Game class
        self.operation = Operation(Path(self.get_apps_folder() / Path("braille_learning")))
        # menu creation.
        self._menu = self.__create_menu()
        # document refresh.
        self.position = 1
        self.expression = ""
        self.my_expression = ""
        self.game = False
        self.score = 0  # Cette valeur changera en fonction du niveau choisi
        # Traitement du chargement du niveau
        self.table = ManageLevel().get_level("operation")
        if self.table == False:
            self._exec_select_table()
        else:
            self.initialize()

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("math game"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&score"), action=self._exec_score,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&show to this table"), action=self._exec_show_score),
                        ui.UiMenuItem(name=_("&delete to this table"), action=self._exec_delete_score),
                    ]
                ),
                ui.UiMenuItem(name=_("&table"), action=self._exec_select_table),
                ui.UiMenuItem(name=_("&reset application"), action=self._exec_reset_application),
                ui.UiMenuItem(name=_("&about"), action=self._exec_about,
                              shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                              shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_applications),
            ],
        )

    def _exec_score(self):
        pass

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self.__create_menu()
        # self.__update_document()
        # self.set_data_line()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        delete = self._menu.get_object(self._exec_reset_application)
        score = self._menu.get_object(self._exec_score)
        braille_type = Settings().data['system']['braille_type']
        if self.game:
            delete.unhide()
            score.unhide()
            self._menu.rename_item(_("&change to table"), braille_type, self._exec_select_table)
        else:
            delete.hide()
            score.hide()
            self._menu.rename_item(_("&select table"), braille_type, self._exec_select_table)
        self.set_data_line()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        self.set_data_line()
        if self.game and Settings().data['braille_learning']['use_vocal'] != "no":
            speak(self.expression)

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        self.set_data_line()

    def initialize(self):
        # On s'occupe du score
        t = ManageScore().get_score_level("operation", self.table)
        if t != False:
            self.score = t
        else:
            self.score = 0
        self.expression = ""
        self.my_expression = ""
        self.position = 1
        operation = self.operation.load_file(self.table)
        if not operation:
            self.game = False
            return False
        self.expression = self.operation.get_expression()
        self.game = True
        self.refresh_document()
        if Settings().data['braille_learning']['use_vocal'] == "auto":
            speak(text=self.expression)

    # ---------------
    # Menu functions.
    def _exec_what_is_result(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("the result was {}").format(self.operation.lst_expression[self.expression]),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self.initialize),
            ],
            action_cancelable=self.initialize,
        )

    def _exec_select_table(self):
        lst_table = self.operation.get_list_tables()
        lst_table.append(_("all tables"))
        if not self.table:
            index = lst_table.index(_("all tables"))
        else:
            index = lst_table.index(self.table)
        self._current_dialog = ui.UiDialogBox(
            name=_("select table"),
            item_list=[
                ui.UiListBox(name=_("&table to"), value=("table", lst_table), current_index=index),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_select_table),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_delete_score(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to erase the score of this table?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_delete_score),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_reset_application(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to reset the application?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_reset_application),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        # Display an information dialog box.
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("Application {} version {}. {} Theotime Berthod").format(_("math game"), app_version,
                                                                               "Copyright (C)2023"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_applications(self):
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    # --------------------
    # Dialogbox functions.

    def _exec_test_operation(self):
        if Settings().data['braille_learning']['keep_spaces']:
            self.my_expression = self.my_expression.strip(" ")
        test = self.operation.test_expression(self.my_expression)
        if test:
            audio = AudioPlayer()
            audio.file_play(str(Path(self.get_apps_folder() / Path("braille_learning/tada.wav"))), 0)
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("good, the result is {}").format(self.operation.lst_expression[self.expression]),
                action=self.initialize)
            self.score += 1
            ManageScore().add_score("operation", self.table, self.score)
        else:
            audio = AudioPlayer()
            audio.file_play(str(Path(self.get_apps_folder() / Path("braille_learning/warning.wav"))), 0)
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_("no, it's not the good result. Try again"),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ui.UiButton(name=_("&see the solution"), action=self._exec_what_is_result)
                ]
            )

    def _exec_valid_select_table(self):
        kwargs = self._current_dialog.get_values()
        if kwargs['table'] == _("all tables"):
            kwargs['table'] = ""
        self.table = kwargs['table']
        self.initialize()

    def _exec_show_score(self):
        if self.table == "":
            name = _("all tables")
        else:
            name = self.table
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("for the table of {}, the score is {}").format(name, self.score), action=self._exec_cancel_dialog)

    def _exec_valid_delete_score(self):
        ManageScore().delete_score("operation", self.table)

    def _exec_valid_reset_application(self):
        self.expression = ""
        self.my_expression = ""
        self.table = False
        self.game = False
        self.score = 0
        ManageLevel().delete_app("operation")
        ManageScore().delete_app("operation")
        self.refresh_document()

    def message(self, message_type):
        AudioPlayer().file_play(BRAILLE_LEARNING_APP_FOLDER + "{}.wav".format(message_type), 0)

    # --------------------
    # Key event functions.

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key.
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = False
        if key_id == Keyboard.KeyId.KEY_NONE:
            # Ignore keys up event.
            return False
        log.info("key_id={}".format(key_id))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(OperationApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # TODO to complete
            if self.game and Settings().data['braille_learning']['write_all']:
                if key_id == Keyboard.KeyId.KEY_CARET_LEFT and self.position > 1:
                    self.position -= 1
                    self.set_data_line()
                elif key_id == Keyboard.KeyId.KEY_CARET_RIGHT and self.position <= len(self.my_expression):
                    self.position += 1
                    self.set_data_line()
        return done

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param character: unicode char
        :param data: brut braille comb. for advanced treatment
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {character=}")
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(OperationApp, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            # TODO to complete
            if self.game:
                if not Settings().data['braille_learning']['write_all'] and \
                        self.operation.lst_expression[self.expression][self.position - 1] != character:
                    return self.message("error")
                elif not Settings().data['braille_learning']['write_all']:
                    self.message("ok")
                self.my_expression = self.my_expression[:self.position] + character + self.my_expression[self.position:]
                self.position += 1
                self.set_data_line()
                if not Settings().data['braille_learning']['write_all'] and len(self.my_expression) == len(
                        self.operation.lst_expression[self.expression]):
                    self._exec_test_operation()
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(OperationApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # TODO to complete
            if self.game:
                if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE:
                    if not Settings().data['braille_learning']['write_all'] and \
                            self.operation.lst_expression[self.expression][self.position - 1] != " ":
                        return self.message("error")
                    elif not Settings().data['braille_learning']['write_all']:
                        self.message("ok")
                    self.my_expression = self.my_expression[:self.position] + " " + self.my_expression[self.position:]
                    self.position += 1
                    self.set_data_line()
                    if not Settings().data['braille_learning']['write_all'] and len(self.my_expression) == len(
                            self.operation.lst_expression[self.expression]):
                        self._exec_test_operation()
                elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE and self.position > 1 and \
                        Settings().data['braille_learning']['write_all']:
                    self.my_expression = self.my_expression[:self.position - 2] + self.my_expression[self.position:]
                    self.position -= 1
                    self.set_data_line()
                elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN and \
                        Settings().data['braille_learning']['write_all']:
                    self._exec_test_operation()
        return done

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {position=} {key_type=}")
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(OperationApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            if position > len(self.expression) + 1 and position <= len(self.expression) + 1 + len(
                    self.my_expression) + 1 and Settings().data['braille_learning']['write_all']:
                self.position = position - len(self.expression) - 1
                self.set_data_line()
            elif position <= len(self.expression) and Settings().data['braille_learning']['use_vocal'] != _("no"):
                speak(self.expression)
            done = True
        return done

    def input_function(self, *args, **kwargs) -> bool:
        """
        Call when function is not treated by base class of this class.
        :param args[0]: The function id
        :param kwargs:
        :return: True if function treated.
        """
        log.info("args={} kwargs={}".format(args, kwargs))
        function_id = args[0]
        # Here treat the specific FunctionId added by this application.
        # else call base class decoding.
        done = super(OperationApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        pass

    def shutdown(self, focused):
        ManageLevel().add_level("operation", self.table)

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if not self.game:
            line = _("you must select a table from the menu")
            braille_static = BnoteApp.lou.to_dots_8(line)
            braille_blinking = "\u2800" * len(braille_static)
        else:
            line = "".join([
                "{}=".format(self.expression),
                "{}".format(self.my_expression)
            ])
            braille_static = BnoteApp.lou.to_dots_8(line)
            braille_blinking = "".join([
                "\u2800" * (len(self.expression) + self.position),
                "\u28C0",
                "\u2800" * (len(braille_static) - (len(self.expression) + len(self.my_expression) - self.position))
            ])
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)
