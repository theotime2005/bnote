"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from pathlib import Path

from bnote.apps.fman.file_manager import BNOTE_FOLDER
from bnote.apps.games.high_scores import HighScores
from bnote.apps.games.mines import Mines
import bnote.ui as ui
# Set up the logger for this file
from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, MINES_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(MINES_APP_LOG)


class MinesApp(BnoteApp):
    """
    Skeleton application.
    """

    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super().__init__(put_in_function_queue)
        # menu creation.
        self.level_msg = {}
        self._menu = self.__create_menu()
        # document refresh.
        self._mines = Mines(8, 8, 10)
        # instantiate high score.
        self._high_scores = HighScores(BNOTE_FOLDER / Path(".high_scores_mines"))
        # Current line displayed.
        self._current_line = 0
        self._current_column = 0
        # Current timer
        self._current_name = ""
        self._current_level = 'level_1'
        self._timer_paused = False
        self._timer_seconds = 0

        self.set_data_line()

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        self.level_msg = {
            'level_1': _("(8 x 8, 10 mines)"),
            'level_2': _("(16 x 16, 40 mines)"),
            'level_3': _("(32 x 16, 99 mines)")
        }
        return ui.UiMenuBar(
            name=_("mines"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&new"),
                    menu_item_list=[
                        ui.UiMenuItem(name="{}".format(self.level_msg['level_1']), action=self._exec_new_1),
                        ui.UiMenuItem(name="{}".format(self.level_msg['level_2']), action=self._exec_new_2),
                        ui.UiMenuItem(name="{}".format(self.level_msg['level_3']), action=self._exec_new_3),
                    ]),
                ui.UiMenuBar(
                    name=_("&scores"),
                    menu_item_list=[
                        ui.UiMenuBar(
                            name=_("&view"),
                            menu_item_list=[
                                ui.UiMenuItem(name="{}".format(self.level_msg['level_1']), action=self._exec_view_1),
                                ui.UiMenuItem(name="{}".format(self.level_msg['level_2']), action=self._exec_view_2),
                                ui.UiMenuItem(name="{}".format(self.level_msg['level_3']), action=self._exec_view_3),
                            ]),
                        ui.UiMenuItem(name=_("&delete"), action=self._exec_delete_high_scores),
                    ]),
            ],
        )

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        self.set_data_line()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        self.set_data_line()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        pass

    # ---------------
    # Menu functions.
    def _exec_new_1(self):
        self._current_level = 'level_1'
        self._mines = Mines(8, 8, 10)
        self.__start_game()
        self.set_data_line()

    def _exec_new_2(self):
        self._current_level = 'level_2'
        self._mines = Mines(16, 16, 40)
        self.__start_game()
        self.set_data_line()

    def _exec_new_3(self):
        self._current_level = 'level_3'
        self._mines = Mines(30, 16, 99)
        self.__start_game()
        self.set_data_line()

    def _exec_view_1(self):
        self.__display_scores('level_1')

    def _exec_view_2(self):
        self.__display_scores('level_2')

    def _exec_view_3(self):
        self.__display_scores('level_3')

    def _exec_delete_high_scores(self):
        # Ask confirmation to delete scores of one level.
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("are you sure to delete high score for {}").format(self.level_msg[self._current_level]),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_valid_delete_scores),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __start_game(self):
        self._current_line = 0
        self._current_column = 0
        self._timer_seconds = 0
        self._timer_paused = False

    # --------------------
    # Dialogbox functions.

    def _exec_valid_win_dialog(self):
        if self._high_scores.is_better_score(self._current_level, self._timer_seconds) != -1:
            self._current_dialog = ui.UiDialogBox(
                name=_("new score"),
                item_list=[
                    ui.UiFileEditBox(name=_("&name"), value=('name', self._current_name)),
                    ui.UiButton(name=_("&ok"), action=self._exec_valid_win_name_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            self._exec_cancel_dialog()

    def _exec_valid_win_name_dialog(self):
        kwargs = self._current_dialog.get_values()
        self._current_name = kwargs['name']
        self._high_scores.add_score(self._current_level, self._current_name, self._timer_seconds)
        self.__display_scores(self._current_level)

    def _exec_valid_delete_scores(self):
        self._high_scores.delete_score(self._current_level)
        self._exec_cancel_dialog()

    def __display_scores(self, level):
        self._current_dialog = ui.UiDialogBox(
            name=_("scores"),
            item_list=[
                ui.UiListBox(name=_("&score"), value=('score', self._high_scores.scores_list(level))),
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

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
        done = super(MinesApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            command_switcher = {
                Keyboard.KeyId.KEY_CARET_UP: self.__previous_line,
                Keyboard.KeyId.KEY_CARET_DOWN: self.__next_line,
                Keyboard.KeyId.KEY_CARET_RIGHT: self.__next_column,
                Keyboard.KeyId.KEY_CARET_LEFT: self.__previous_column,
                Keyboard.KeyId.KEY_START_DOC: self.__first_pos,
                Keyboard.KeyId.KEY_END_DOC: self.__last_pos,
            }
            function = command_switcher.get(key_id, None)
            if function:
                # Execute the function
                done = function()
                if done:
                    # Refresh
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
        done = super(MinesApp, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            if character == 'b':
                # Mark a bomb.
                done = self.__mark_bomb()
            elif character == 't':
                # discover all for test high score
                done = self.__force_win()
            if done:
                # Refresh
                self.set_data_line()
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        bramigraph_switcher = {
            Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE: self.__discover,
            Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: self.__next_column,
            Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: self.__previous_column,
            Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: self.__next_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_UP: self.__previous_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self.__first_pos,
            Keyboard.BrailleFunction.BRAMIGRAPH_END: self.__last_pos,
        }
        done = super(MinesApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            function = bramigraph_switcher.get(bramigraph, None)
            if function:
                done = function()
                # Refresh
                self.set_data_line()
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
        done = super(MinesApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            position -= 3 + 1
            log.info(f"{position=}")
            if position in range(0, self._mines.nb_column()):
                self._current_column = position
                self.set_data_line()
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
        done = super(MinesApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        if not self._timer_paused:
            self._timer_seconds += 1
            self.set_data_line()

    # --------------------
    # Document functions.
    def __previous_line(self) -> bool:
        if self._current_line > 0:
            self._current_line -= 1
            return True
        return False

    def __next_line(self) -> bool:
        if self._current_line < self._mines.nb_line() - 1:
            self._current_line += 1
            return True
        return False

    def __next_column(self):
        if self._current_column < self._mines.nb_column() - 1:
            self._current_column += 1
            return True
        return False

    def __previous_column(self):
        if self._current_column > 0:
            self._current_column -= 1
            return True
        return False

    def __first_line(self):
        if self._current_line != 0:
            self._current_line = 0
            return True
        return False

    def __last_line(self):
        if self._current_line != self._mines.nb_line() - 1:
            self._current_line = self._mines.nb_line() - 1
            return True
        return False

    def __first_pos(self):
        if (self._current_line != 0) or (self._current_column != 0):
            self._current_line = 0
            self._current_column = 0
            return True
        return False

    def __last_pos(self):
        if (self._current_line != self._mines.nb_line() - 1) or (self._current_column != self._mines.nb_column() - 1):
            self._current_line = self._mines.nb_line() - 1
            self._current_column = self._mines.nb_column() - 1
            return True
        return False

    def __discover(self) -> bool:
        if not self._timer_paused:
            log.info(self._mines.print_tables())
            res = self._mines.discovered_pos(self._current_line, self._current_column)
            log.info(self._mines.print_tables())
            if res == -1:
                # Aie ! A mine is discovered.
                self._current_dialog = ui.UiInfoDialogBox(message=_("boum !"),
                                                          action=self._exec_cancel_dialog)
                self.__lost_game()
            elif self._mines.is_all_discovered():
                # All game discovered except mines.
                self.__win()
        self.__next_column()
        return True

    def __force_win(self):
        self._mines.discovered_all()
        self.__win()
        return True

    def __win(self):
        # All game discovered except mines.
        self.__lost_game()
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("you win in {} seconds").format(self._timer_seconds),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_valid_win_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __mark_bomb(self) -> bool:
        res = self._mines.bomb_at_pos(self._current_line, self._current_column)
        if res == -1:
            # Aie ! A mine is discovered.
            self._current_dialog = ui.UiInfoDialogBox(message=_("no bomb here !"),
                                                      action=self._exec_cancel_dialog)
            self.__lost_game()
        return True

    def __lost_game(self):
        self._mines.discovered_all()
        self._timer_paused = True
        pass

    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        line = ''.join([
            "{:2d} ".format(self._current_line + 1),
            self._mines.display_line(self._current_line),
            " {:3d}".format(self._timer_seconds)
        ])
        braille_static = BnoteApp.lou.to_dots_8(line)
        braille_blinking = "".join([
            "\u2800" * (3 + self._current_column),
            "\u28C0",
            "\u2800" * (len(braille_static) - (4 + self._current_column)),
        ])
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)
