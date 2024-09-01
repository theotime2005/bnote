"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from bnote.apps.fman.file_manager import FileManager
from bnote.tools.speech_wrapper import speak
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
import bnote.ui as ui
# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, SKELETON_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(SKELETON_APP_LOG)


class SkeletonApp(BnoteApp):
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
        self._menu = self.__create_menu()
        # document refresh.
        self.__text = "----- Document area of skeleton application -----"
        self.set_data_line()

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("skeleton"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&group"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&menu_1"), action=self._exec_menu_1),
                        ui.UiMenuItem(name=_("&choose_file"), action=self._exec_choose_file_menu),
                    ]),
                ui.UiMenuItem(name=_("&say hello"), action=self._exec_say_hello),
                ui.UiMenuItem(name=_("&about"), action=self._exec_about,
                              shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                              shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1),
            ],
        )

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
    def _exec_menu_1(self):
        # Display a dialog box with many controls.
        self._current_dialog = ui.UiDialogBox(
            name=_("example"),
            item_list=[
                ui.UiMultiLinesBox(
                    name=_("&multilineseditbox"),
                    value=("message", "line 1\nline 2\nline 3"),
                    is_read_only=False),
                ui.UiMultiLinesBox(
                    name=_("&read_only_multilineseditbox"),
                    value=("message", "line 1\nline 2\nline 3"),
                    is_read_only=True),
                ui.UiEditBox(name=_("&editbox"), value=("editbox", "Text to edit")),
                ui.UiListBox(name=_("&listbox"), value=("line", ["line 1", "line 2", "line 3"]), current_index=1),
                ui.UiFileEditBox(name=_("&file name"), value=("file", "")),
                ui.UiLabel(name=_("this is a label")),
                ui.UiCheckBox(name=_("&checkbox"), value=("checkbox", True)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_sample_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_choose_file_menu(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert file"),
            item_list=[
                ui.UiFileBox(root=FileManager.get_root_path(), suffix_filter=(".txt", ".pdf")),
                ui.UiButton(name=_("&ok"), action=self._exec_choose_file),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_say_hello(self):
        speak(_("Hello bnote."))

    def _exec_about(self):
        # Display an information dialog box.
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("application skeleton V1.0.1"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    # --------------------
    # Dialogbox functions.

    def _exec_valid_sample_dialog(self):
        log.info("callback:_exec_valid_sample_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")

    def _exec_choose_file(self):
        log.info("callback:_exec_valid_sample_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        file_path = kwargs['file']
        if file_path is None:
            log.info("No file chosen")
        elif file_path.is_file():
            log.info(f"file:{file_path}")
        else:
            log.info(f"folder:{file_path}")

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
        done = super(SkeletonApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # TODO to complete
            pass
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
        done = super(SkeletonApp, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            # TODO to complete
            pass
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
        done = super(SkeletonApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # TODO to complete
            pass
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
        done = super(SkeletonApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
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
        done = super(SkeletonApp, self).input_function(*args, **kwargs)
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

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        braille_static = BnoteApp.lou.to_dots_8(self.__text)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(self.__text, braille_static, braille_blinking, 0)
