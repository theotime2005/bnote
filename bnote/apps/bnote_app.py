"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


from enum import Enum
from pathlib import Path
import pkg_resources
from bnote.braille.braille_display import BrailleDisplay
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, BNOTE_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(BNOTE_APP_LOG)

# The number of document that can be opened simultaneously
MAX_EDITOR_APP = 5


class FunctionId(Enum):
    # Function for agenda
    FUNCTION_AGENDA_SAME_DAY = object()
    FUNCTION_AGENDA_NEXT_DAY = object()
    FUNCTION_RESTOR_AFTER_AGENDA=object()
    APPLICATIONS = object()
    USB = object()
    FUNCTION_SETTINGS_CHANGE = object()
    OPEN_THE_FILE_PLEASE = object()
    OPEN_THE_MP3_FILE_PLEASE = object()
    FUNCTION_CLOSE_EDITOR = object()
    FUNCTION_CLOSE_DIALOG_BOX = object()
    FUNCTION_SELECT_SHEET_DIALOG_BOX = object()
    FUNCTION_DISPLAY_LAST_ERROR = object()
    FUNCTION_DISPLAY_LAST_ERROR_AND_CLOSE_EDITOR = object()
    FUNCTION_CHANGE_LOCKED_FILE = object()
    FUNCTION_SAVE_AND_DELETE_ORIGINAL = object()
    FUNCTION_DELETE_ORIGINAL = object()
    FUNCTION_EDITOR_BRAILLE_REFRESH = object()
    FUNCTION_APPEND_BLUETOOTH = object()
    FUNCTION_REMOVE_BLUETOOTH = object()
    FUNCTION_ONE_SECOND_TIMER_ELAPSED = object()
    FUNCTION_CANCEL_ONE_SECOND_TIMER = object()
    FUNCTION_EDITOR_RESIZE_LINE_LENGTH = object()
    FUNCTION_INTERNAL_CLOSE_ALL_EDITOR = object()
    FUNCTION_RE_TRANSLATE_UI = object()
    FUNCTION_INTERNAL_NEXT_APP = object()
    FUNCTION_INTERNAL_PREVIOUS_APP = object()
    FUNCTION_IN_PROGRESS = object()
    FUNCTION_END_DELETE = object()
    FUNCTION_END_RESTORE = object()
    FUNCTION_END_BACKUP = object()
    FUNCTION_END_ZIP = object()
    FUNCTION_END_UNZIP = object()
    FUNCTION_END_SEND_TO = object()
    FUNCTION_END_PASTE = object()
    FUNCTION_ON_ASK_REPLACE = object()
    FUNCTION_END_EOLE_DOWNLOAD = object()
    FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG = object()
    END_RESTORE_FROM_TRASH = object()
    RESTART_PLEASE = object()
    ASK_TERMINATE_BNOTE_AND_RESTART_SERVICE = object()
    ASK_SHUTDOWN = object()
    ASK_TRANSPORT = object()
    SHUTDOWN = object()
    FUNCTION_END_SCAN_WIFI = object()
    FUNCTION_END_TIMER = object()
    FUNCTION_OPEN_BLUETOOTH = object()
    FUNCTION_BLUETOOTH_WRITE = object()
    FUNCTION_CHECK_UPDATE = object()
    FUNCTION_CHECK_UPDATE_ENDED = object()
    FUNCTION_TRANSLATOR = object()
    FUNCTION_ASK_LANGUAGE = object()
    FUNCTION_OPEN_TRANSLATOR = object()
    FUNCTION_TRANSLATE_COPY = object()
    FUNCTION_DAISY_SUMMARY_ENDED = object()
    FUNCTION_DAISY_TIME_OUT = object()
    FUNCTION_WIKIPEDIA_TIME_OUT = object()
    FUNCTION_OPEN_WIKIPEDIA_DIALOG = object()
    FUNCTION_CLOSE_WIKIPEDIA = object()
    ASK_TO_REFRESH_MESSAGE_DIALOG = object()
    UNABLE_TO_UPDATE = object()

class BnoteApp:
    keyboard = Keyboard()
    lou = None
    one_second_timer = None
    bluetooth_devices = dict()

    def __init__(self, put_in_function_queue):
        # call back to call an Internal.py function
        self._put_in_function_queue = put_in_function_queue
        self._braille_display = BrailleDisplay()
        # All applications have a menu, here the corresponding flag.
        self._in_menu = False
        self._menu = None
        # Usefull when menu function needs to ask something to user.
        self._current_dialog = None

    def refresh_app(self):
        """
        Call when enter or re-enter in application.
        """
        # Exit menu when re-enter in application
        self._in_menu = False
        if self._current_dialog:
            self._current_dialog.ask_update_braille_display()
        # elif self._in_menu and self._menu:
        #     self._menu.ask_update_braille_display()
        else:
            self.rebuild_document()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        pass

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        pass

    def _update_menu_items(self):
        """
        This function could be overloaded by application to update menu before its display.
        :return: None
        """
        pass

    def translate_ui(self):
        """
        This function must be overloaded by application to change menu's labels.
        Do the translation according to the current translation
        """
        log.error(f"Application must overload translate_ui {self.__class__}")

    @staticmethod
    def braille_form(text):
        braille_type = Settings().data['system']['braille_type']
        if braille_type == 'grade1':
            braille_text, index1, index2, new_shortcut_pos = BnoteApp.lou.text_to_grade1(text)
            # print(f"to grade 1 {text}->{braille_text}->{BnoteApp.lou.grade1_to_text(braille_text)[0]}")
        elif braille_type == 'grade2':
            braille_text, index1, index2, new_shortcut_pos = BnoteApp.lou.text_to_grade2(text)
            # print(f"to grade 2 {text}->{braille_text}->{BnoteApp.lou.grade2_to_text(braille_text)[0]}")
        else:
            # text unchanged
            braille_text = text
        return braille_text

    @staticmethod
    def text_form(braille):
        braille_type = Settings().data['system']['braille_type']
        if braille_type == 'grade1':
            text, index1, index2, new_shortcut_pos = BnoteApp.lou.grade1_to_text(braille)
            # print(f"to grade 1 {braille}->{text}->{BnoteApp.lou.text_to_grade1(text)[0]}")
        elif braille_type == 'grade2':
            text, index1, index2, new_shortcut_pos = BnoteApp.lou.grade2_to_text(braille)
            # print(f"to grade 2 {braille}->{text}->{BnoteApp.lou.text_to_grade2(text)[0]}")
        else:
            # text unchanged
            text = braille
        return text

    def in_menu_or_in_dialog(self):
        return self._in_menu or self._current_dialog is not None

    def input_function(self, *args, **kwargs):
        log.info("function to treat args={} kwargs={}".format(args, kwargs))
        if len(args):
            function_id = args[0]
            if function_id == FunctionId.FUNCTION_CLOSE_DIALOG_BOX:
                # Exit from dialog box.
                self._current_dialog = None
                # Force refresh.
                self._braille_display.new_data_available_event.set()
                return True
            elif function_id == FunctionId.ASK_TO_REFRESH_MESSAGE_DIALOG:
                return self._update_in_progress(kwargs['msg'])
            elif function_id == FunctionId.UNABLE_TO_UPDATE:
                return self._unable_to_update_info_dialog()

    def _input_braille(self, braille, data):
        done = False
        log.info("Braille key in file_manager.py ={}".format(braille))
        (braille_type, braille_modifier, braille_value) = braille
        if braille_type == Keyboard.BrailleType.CHARACTER:
            done = self.input_character(braille_modifier, str(braille_value), data)
        elif braille_type == Keyboard.BrailleType.FUNCTION:
            done = self.input_bramigraph(braille_modifier, braille_value)
        return done

    def input_braille(self, data) -> bool:
        return self._input_braille(BnoteApp.keyboard.decode_braille(BnoteApp.lou, data), data)

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param character: unicode char
        :param data: brut braille comb. for advanced treatment
        :return: True if command treated, otherwise False
        """
        if self._current_dialog is not None:
            save_dialog = self._current_dialog
            in_dialog = self._current_dialog.input_character(modifier, character, data)
            if not in_dialog and (save_dialog == self._current_dialog):
                # If end of dialog and no new dialog box installed, close dialog
                self.close_dialog()
            return True
        elif self._in_menu:
            in_menu = self._menu.input_character(modifier, character, data)
            if not in_menu:
                # Exit from main menu
                self.close_menu()
            return True
        else:
            if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_ALT and character == chr(0):
                # double Alt bramigraph key.
                self.input_command(None, Keyboard.BrailleModifier.BRAILLE_FLAG_NONE, Keyboard.KeyId.KEY_MENU)
                return True
            elif modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_ALT:
                # menu shortcut in Alt+_
                in_menu = self._menu.input_alt_shortcut(character)
                if in_menu:
                    # Activate the menu
                    self._in_menu = True
                    return True
                else:
                    return False
            else:
                # menu shortcut Ctrl+_...
                done = self._menu.exec_menu_item_key(modifier, character)
                if done:
                    self.refresh_document()
                return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        if self._current_dialog is not None:
            save_dialog = self._current_dialog
            in_dialog = self._current_dialog.input_bramigraph(modifier, bramigraph)
            if not in_dialog and ((self._current_dialog is None) or (save_dialog == self._current_dialog)):
                # If end of dialog and no new dialog box installed, close dialog
                self.close_dialog()
            return True
        elif self._in_menu:
            in_menu = self._menu.input_bramigraph(modifier, bramigraph)
            if not in_menu:
                # Exit from main menu
                self.close_menu()
            return True
        elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_MENU:
            # Enter in application's menu.
            self._enter_in_menu()
            return True
        elif modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL and\
                bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_TAB:
            self._put_in_function_queue(FunctionId.FUNCTION_INTERNAL_NEXT_APP)
            return True
        elif modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL and\
                bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB:
            self._put_in_function_queue(FunctionId.FUNCTION_INTERNAL_PREVIOUS_APP)
            return True
        else:
            # menu shortcut Fn, Ctrl+_...
            done = self._menu.exec_menu_item_key(modifier, bramigraph)
            if done:
                self.refresh_document()
            return done

    def _enter_in_menu(self):
        self._in_menu = True
        # Update menu if necessary
        self._update_menu_items()
        # Cleanup menu state
        self._menu.reset_container()

    def close_dialog(self):
        # Close the dialogbox
        self._current_dialog = None
        if not self._in_menu:
            self.refresh_document()

    def close_menu(self):
        # Close the menu
        self._in_menu = False
        if self._current_dialog is None:
            self.refresh_document()

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        if key_id != Keyboard.KeyId.KEY_NONE:
            # Master function : Go back to firmware
            if (modifier == 0) and key_id == Keyboard.KeyId.KEY_APPLICATIONS:
                self._put_in_function_queue(FunctionId.APPLICATIONS)
                return True
            # DialogBox object
            elif self._current_dialog:
                save_dialog = self._current_dialog
                in_dialog = self._current_dialog.input_command(modifier=modifier, key_id=key_id)
                if not in_dialog and (save_dialog == self._current_dialog):
                    # If end of dialog and no new dialog box installed, close dialog
                    self.close_dialog()
                return True
            # Menus object
            elif self._in_menu:
                in_menu = self._menu.input_command(modifier=modifier, key_id=key_id)
                if not in_menu:
                    self.close_menu()
                return True
            # if not in menu mode and Keyboard.KeyId.KEY_MENU enters in menu mode
            elif modifier == 0:
                if key_id == Keyboard.KeyId.KEY_MENU:
                    self._enter_in_menu()
                    return True
        return False

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        if self._current_dialog is not None:
            save_dialog = self._current_dialog
            in_dialog = self._current_dialog.input_interactive(modifier, position, key_type)
            if not in_dialog and (save_dialog == self._current_dialog):
                # If end of dialog and no new dialog box installed, close dialog
                self.close_dialog()
            return True
        elif self._in_menu:
            in_menu = self._menu.input_interactive(modifier, position, key_type)
            if not in_menu:
                self.close_menu()
            return True
        return False

    def set_menu(self, menu):
        self._menu = menu

    def set_braille_display_line(self, text, dots, blink, start):
        # self._braille_display.set_dynamic_dots_line(dots)
        # self._braille_display.set_text_line(text, start)
        self._braille_display.set_data_line(text, dots, blink, start)

    def set_braille_display_dots_line(self, dots, blink, start):
        self._braille_display.set_data_line(None, dots, blink, start)

    # Return the (static_text, fixed_dots, static_dots, dynamic_dots) if something changed since the last call
    # or if force_refresh=True,
    # else return (None, None, None, None)
    def get_data_line(self, force_refresh=False) -> (str, bytes, bytes, bytes, bool):
        if self._current_dialog is not None:
            return self._current_dialog.get_data_line(force_refresh)
        elif self._in_menu:
            return self._menu.get_data_line(force_refresh)
        else:
            return self._braille_display.get_data_line(force_refresh)

    def on_close(self):
        """
        Call just before the application removing from internal menu.
        Overload by editor_app to delete associated context file.
        """
        pass

    def on_delete(self):
        """
        Call during execution of reset function from settings_app
        Overload by editor_app to delete associated context file.
        """
        pass

    def shutdown(self, focused):
        """
        By default : Application do nothing on shutdown notification.
        Some application overload this function
        """
        pass

    def shutdown_ended(self):
        # By default : shutdown process is ended for application.
        return True

    # This method wil be called from input
    def on_timer(self):
        pass

    def _update_in_progress(self, label):
        """
        Update the message of the current UiInfoDialogbox or create one if necessary.
        """
        # DP FIXME The dialogbox display cannot be done here because circular import with BnoteApp.lou (to move in BnoteStart ?)
        log.error("_update_in_progress not overloaded")
        # if self._current_dialog:
        #     if isinstance(self._current_dialog, ui.UiInfoDialogBox):
        #         self._current_dialog.change_label(label)
        #     else:
        #         # Need to re-instanciate ui.UiInfoDialogBox after a "yes / no" ui.UiMessageDialogBox
        #         self._current_dialog = ui.UiInfoDialogBox(message=label)

    def _unable_to_update_info_dialog(self):
        """
        Call during execution of update bnote application
        Must be overload by filemanager_app and settings_app to display a dialogbox.
        """
        # DP FIXME The dialogbox display cannot be done here because circular import with BnoteApp.lou (to move in BnoteStart ?)
        log.error("_unable_to_update_info_dialog not overloaded")
        # self._current_dialog = ui.UiInfoDialogBox(
        #     message=_("unable to update."),
        #     action=self._exec_cancel_dialog,
        # )

    def _exec_cancel_dialog(self):
        log.info("callback:_exec_cancel_dialog")

    def get_apps_folder(self):
        # if self.debug:
        #     return Path('bnote/apps')
        # else:
        #     return Path(pkg_resources.resource_filename('bnote', 'apps'))
        return Path(pkg_resources.resource_filename('bnote', 'apps'))






