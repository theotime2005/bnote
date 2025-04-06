"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import datetime
import time
from os import path
import threading

from bnote.speech.speech import SpeechManager
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.tools.io_util import Gpio
from bnote.tools.settings import Settings
from bnote.tools.volume import Volume
from bnote.tools.volume_speed_dialog_box import VolumeDialogBox, SpeedDialogBox
import bnote.ui as ui
import bnote.apps.edt.edt as editor
from bnote.tools.keyboard import Keyboard
from bnote.tools.quick_search import QuickSearch
from bnote.apps.fman.file_manager import FileManager, BNOTE_MAIN_FOLDER
from bnote.apps.bnote_app import BnoteApp, FunctionId
from pathlib import Path

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG, logging

log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class EditorBaseApp(BnoteApp):
    MATH_MENU_ID = object

    def __init__(
        self,
        put_in_function_queue,
        file_name=None,
        language=None,
        read_only=False,
        no_context=False,
    ):
        super().__init__(put_in_function_queue)
        self.next_refresh_disable = False
        # call back to call an Internal.py function
        self._put_in_function_queue = put_in_function_queue
        self._original_file_name = file_name
        # The file name to write, equal to _original_file_name for txt file.
        self._file_name = None
        # Usefull when reading document
        self.channel = "speech"
        self.caret_from_specific = None
        self.markers_from_specific = None
        self.read_only_from_specific = None
        self.read_only_from_opening = read_only
        self.lines_count = 0
        self.reader = None
        self.wait_dialog = False
        #
        self._language = language
        # Editor instance, not yet defined
        self.editor = None
        # lines access protection.
        self.lock = threading.Lock()
        # set by read_context() if editor was application with focus during shutdown.
        self.is_focused = False
        # Killed, to indicate the end of editor instance life by File>Close
        self._killed = False
        # The current braille type for this editor instance.
        # If the settings change this document keep its braille type.
        self.braille_type = Settings().data["editor"]["braille_type"]
        # grade 2 display.
        self._is_forward_grade2 = False
        self.grade2_paragraph_index = -1
        self.grade2_index_text = None
        # caret for forward and backward display function.
        self.is_moving_display = False
        self.moving_display_caret = None
        # True when the autoscroll for braille display is engaged.
        self._is_autoscroll = False
        self._autoscroll_timeout = Settings().data["editor"]["autoscroll"]
        # For shutdown.
        self._shutdown_processing = False
        # incremental search.
        self.is_editing = True
        # last find and replace parameters
        self._replace_parameters = editor.FindParameters(
            find_seq="",
            ignore_case=True,
            mask_accents=True,
            entire_word=False,
            replace_seq="",
        )
        # last error
        self.last_error = None
        # The QuickSearch instance.
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)

        # Create the menus.
        self._menu = self._create_menu()

        # Vocal
        self.__is_speaking = False

        if not file_name:
            # Try to restore a document saved during shutdown.
            if not no_context and not self.read_context():
                return
            # Just for test, Editor is always opened with an associated filename, at least an empty file.
            # lines = ["",]
            # self.editor = self._create_editor(lines)
        else:
            # Read the  file
            self.read_file(file_name, language, self.read_file_ended)
        self.refresh_document()

    def _create_menu(self):
        """
        Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        MUST BE OVERLOAD BY CHILD CLASS !
        """
        raise ValueError("create_menu not defined.")

    def create_sub_menu_edit(self):
        return ui.UiMenuBar(
            name=_("&edit"),
            menu_item_list=[
                *[
                    ui.UiMenuItem(
                        name=_("&undo"),
                        action=self._exec_undo,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                        shortcut_key="Z",
                    ),
                    ui.UiMenuItem(
                        name=_("&redo"),
                        action=self._exec_redo,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                        shortcut_key="Y",
                    ),
                ],
                *self.create_sub_menu_selection(),
                *[
                    ui.UiMenuItem(name=_("curs&or"), action=self._exec_cursor),
                    ui.UiMenuItem(
                        name=_("forward in grade2 braille"),
                        action=self._toggle_grade2_from_menu,
                    ),
                ],
            ],
        )

    def create_sub_menu_selection(self):
        return [
            ui.UiMenuBar(
                name=_("&selection"),
                menu_item_list=[
                    ui.UiMenuItem(
                        name=_("&start selection"),
                        action=self._exec_start_selection,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                        shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F8,
                    ),
                    ui.UiMenuItem(
                        name=_("&end selection"),
                        action=self._exec_end_selection,
                        is_hide=True,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                        shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE,
                    ),
                    ui.UiMenuItem(
                        name=_("to the s&tart of doc"),
                        action=self._exec_select_beginning,
                    ),
                    ui.UiMenuItem(
                        name=_("to the e&nd of doc"), action=self._exec_select_ending
                    ),
                    ui.UiMenuItem(
                        name=_("select &all"),
                        action=self._exec_select_all,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                        shortcut_key="A",
                    ),
                ],
            ),
            ui.UiMenuItem(
                name=_("cu&t"),
                action=self._exec_cut,
                shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                shortcut_key="X",
            ),
            ui.UiMenuItem(
                name=_("&copy"),
                action=self._exec_copy,
                shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                shortcut_key="C",
            ),
            ui.UiMenuItem(
                name=_("&paste"),
                action=self._exec_paste,
                shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                shortcut_key="V",
            ),
        ]

    def create_sub_menu_find(self):
        return ui.UiMenuBar(
            name=_("fi&nd"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("fi&nd"),
                    action=self._exec_find,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="F",
                ),
                ui.UiMenuItem(
                    name=_("ne&xt"),
                    action=self._exec_next,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F3,
                ),
                ui.UiMenuItem(
                    name=_("&previous"),
                    action=self._exec_previous,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F3,
                ),
            ],
        )

    def create_sub_menu_find_replace(self):
        return ui.UiMenuBar(
            name=_("fi&nd"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("fi&nd"),
                    action=self._exec_find,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="F",
                ),
                ui.UiMenuItem(
                    name=_("&replace"),
                    action=self._exec_replace,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="H",
                ),
                ui.UiMenuItem(
                    name=_("ne&xt"),
                    action=self._exec_next,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F3,
                ),
                ui.UiMenuItem(
                    name=_("replace and n&ext"),
                    action=self._exec_replace_and_next,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4,
                ),
                ui.UiMenuItem(
                    name=_("&previous"),
                    action=self._exec_previous,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F3,
                ),
                ui.UiMenuItem(
                    name=_("replace and pre&vious"),
                    action=self._exec_replace_and_previous,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4,
                ),
                ui.UiMenuItem(
                    name=_("replace &all"),
                    action=self._exec_replace_all,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    def create_sub_menu_goto(self):
        return ui.UiMenuBar(
            name=_("&goto"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&beginning of document"),
                    action=self._exec_beginning_document,
                ),
                ui.UiMenuItem(
                    name=_("&end of document"), action=self._exec_end_document
                ),
                ui.UiMenuItem(
                    name=_("&previous paragraphe"), action=self._exec_preview_paragraphe
                ),
                ui.UiMenuItem(
                    name=_("&next paragraphe"), action=self._exec_next_paragraphe
                ),
            ],
        )

    def create_sub_menu_bookmark(self):
        return ui.UiMenuBar(
            name=_("&bookmark"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&insert/delete"),
                    action=self._exec_marker_insert_delete,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("ne&xt"),
                    action=self._exec_marker_next,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("&previous"),
                    action=self._exec_marker_previous,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("clear &all"),
                    action=self._exec_marker_clear_all,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
            ],
        )

    def create_sub_menu_vocalize(self):
        return ui.UiMenuBar(
            name=_("&vocalize"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&document"),
                    action=self._exec_read_document,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="D",
                ),
                ui.UiMenuItem(
                    name=_("&paragraph"),
                    action=self._exec_read_paragraph,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="R",
                ),
                ui.UiMenuItem(name=_("&volume"), action=self._exec_volume),
                ui.UiMenuItem(name=_("&speed"), action=self._exec_speed),
            ],
        )

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self._create_menu()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        pass

    def __is_reading_file(self):
        """
        Returns True while reading file thread is active.
        """
        return self.reader is not None

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each app if necessary.
        """
        self._refresh_center_braille_display()

    def refresh_document(self):
        """
        Overload base class. Call when menu or dialogbox are closed.
        :return: None
        """
        # On s'occupe des fonction d'écriture globale
        # Fichier
        ui_save = self._menu.get_object(self._exec_save)
        # Edition
        ui_cut = self._menu.get_object(self._exec_cut)
        ui_past = self._menu.get_object(self._exec_paste)
        # Remplacer
        ui_replace = self._menu.get_object(self._exec_replace)
        ui_next_replace = self._menu.get_object(self._exec_replace_and_next)
        ui_previous_replace = self._menu.get_object(self._exec_replace_and_previous)
        ui_replace_all = self._menu.get_object(self._exec_replace_all)
        # On cache
        if self.editor and self.editor.read_only:
            if ui_save is not None:
                ui_save.hide()
            if ui_cut is not None:
                ui_cut.hide()
            if ui_past is not None:
                ui_past.hide()
            if ui_replace is not None:
                ui_replace.hide()
                ui_next_replace.hide()
                ui_previous_replace.hide()
                ui_replace_all.hide()
        else:
            if ui_save is not None:
                ui_save.unhide()
            if ui_cut is not None:
                ui_cut.unhide()
            if ui_past is not None:
                ui_past.unhide()
            if ui_replace is not None:
                ui_replace.unhide()
                ui_next_replace.unhide()
                ui_previous_replace.unhide()
                ui_replace_all.unhide()
        self._refresh_center_braille_display()

    @staticmethod
    def editor_line_length():
        return Settings().data["editor"]["line_length"]

    def get_filename(self):
        return self._file_name

    def get_display_filename(self):
        """
        Return the filename without root folders '/home/pi'.
        """
        file_name = str(self._file_name).replace(str(BNOTE_MAIN_FOLDER) + "/", "")
        return file_name

    def get_original_filename(self):
        return self._original_file_name

    def was_focused(self):
        return self.is_focused

    # Called when shutdown occurs.
    # Save the current opened file in a descriptor file named .edt_context#.ctx :
    # First line contains "Modified" or "Not modified", it indicates if file is modified or not
    # The next line contains the filename as "Filename=/home/pi/.../file.txt"
    # if modified another line indicates the name of the file saved "Save=/home/pi/.../.doc_context{}.ctx#
    def shutdown(self, focused):
        self._shutdown_processing = True
        # Save file parameters
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("editor.shutdown()")

        if self.editor.is_modified():
            if self.__is_reading_file():
                # DP FIXME Lost the changes if file is not completely read.
                # Le code commenté ne fonctionne pas car l'application n'a pas le focus lors de l'extinction...
                self._shutdown_processing = False
                return
                # The file is not completely read.
                # self._current_dialog = ui.UiMessageDialogBox(
                #     name=_("warning"),
                #     message=_("the file is not completely read, do you want to lost the changes ?"),
                #     buttons=[
                #         ui.UiButton(name=_("&yes"), action=self._exec_force_shutdown, action_param={'focused':focused}),
                #         ui.UiButton(name=_("&no"), action=self._exec_cancel_shutdown),
                #     ],
                #     action_cancelable=self._exec_cancel_shutdown,
                # )
            else:
                if self._file_name is None:
                    self._shutdown_processing = False
                    return
                file_name, file_extension = path.splitext(self._file_name)
                if file_extension != ".txt":
                    # DP FIXME No context restauration for other file than *.txt
                    self._shutdown_processing = False
                    return
                context_file = editor.Context.free_context_file()
                doc_file = editor.Context.free_doc_file(file_extension)
                if doc_file:
                    # Save context file name
                    editor.Context.write_context_file(
                        context_file, True, focused, self._file_name, doc_file
                    )
                    # Save the file
                    write_file = self.write_data_file(
                        BnoteApp.lou,
                        doc_file,
                        self._get_line,
                        self._end_context_save,
                        doc_file,
                    )
                    write_file.start()
                    # Wait saving and close dialog box (SEE _end_context_save(self))
        else:
            self._exec_force_shutdown(focused)

    def _exec_force_shutdown(self, focused):
        if self._file_name is None or self.__is_reading_file:
            self._shutdown_processing = False
            return
        file_name, file_extension = path.splitext(self._file_name)
        if file_extension != ".txt":
            self._shutdown_processing = False
            return
        context_file = editor.Context.free_context_file()
        # Save the file name.
        editor.Context.write_context_file(
            context_file, False, focused, self._file_name, None
        )
        # Write specific file associated to document.
        self._end_context_save(None, self._file_name)

    # def _exec_cancel_shutdown(self):
    #     self._shutdown_processing = False
    #     self._exec_cancel_dialog()

    def _end_context_save(self, error, doc_file):
        kwargs = {
            "markers": self.editor.markers(),
            "caret": self.editor.caret(),
            "read_only": self.editor.read_only,
        }
        self._common_end_context_save(error, doc_file, **kwargs)

    def _common_end_context_save(self, error, doc_file, **kwargs):
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("End of saving")
        if error is None:
            if self._file_name is not None and path.exists(doc_file):
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("Save specific files for {}".format(doc_file))
                with self.lock:
                    # Write specific file associated to the text file written (if this file exists).
                    write_specific_file = editor.ReadWriteSpecificFile(doc_file)
                    write_specific_file.write_specific_file(**kwargs)
                    self._shutdown_processing = False
        else:
            # Error during write file => Display an error dialog box
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning("file save error : {}".format(error))
            self.last_error = error
            self._put_in_function_queue(FunctionId.FUNCTION_DISPLAY_LAST_ERROR)

    def shutdown_ended(self):
        # By default : shutdown process is ended for application.
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("editor.shutdown_ended() returns True.")
        return not self._shutdown_processing

    def read_context(self):
        # Search context filename.
        context_file = editor.Context.first_context_file()
        if context_file is None:
            # No context file available.
            return False
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("context file found is {}".format(context_file.as_posix()))

        is_modified, is_focused, file_name, save_name = (
            editor.Context.parse_context_file(context_file)
        )
        self.is_focused = is_focused
        self._original_file_name = file_name
        self._file_name = self._original_file_name
        if not is_modified:
            # Restore a not modified file.
            self.read_file(self._file_name, None, self.read_context_not_modified_ended)
        else:
            # Restore a modified file
            self.read_file(save_name, None, self.read_context_modified_ended)
        # Delete context file.
        context_file.unlink()
        return True

    def read_file(self, file_name, language, read_file_ended, sheet_name=None):
        # Read specific file.
        read_specific_file = editor.ReadWriteSpecificFile(file_name)
        params = read_specific_file.read_specific_file()
        md5_from_specific = params["md5"]
        if md5_from_specific is not None:
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning("Specific file found")
            md5_file = editor.checksum(file_name)
            # The file to open is not corresponding to the specific file
            self.caret_from_specific = None
            self.markers_from_specific = None
            self.read_only_from_specific = None
            try:
                if int(md5_from_specific) == md5_file:
                    self.caret_from_specific = params["caret"]
                    self.markers_from_specific = params["markers"]
                    self.read_only_from_specific = params["read_only"]
                    # Read extra parameters (for derived class)
                    self.get_extra_parameters(params)
            except ValueError:
                pass
        else:
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning("no specific file found")

        # Read the file
        # Launch reading thread for others extensions
        # Display an information dialog box.
        self._current_dialog = ui.UiInfoDialogBox(message=_("reading..."))
        self.wait_dialog = True
        self.lines_count = 0
        self.reader = self.read_data_file(
            BnoteApp.lou,
            file_name,
            language,
            self.read_file_add_line,
            read_file_ended,
            sheet_name=sheet_name,
        )
        self.reader.start()

    def get_extra_parameters(self, params):
        """
        To overload by child class
        """
        pass

    @staticmethod
    def read_data_file(lou, full_file_name, language, add_line, ended, sheet_name=None):
        """
        To overload by child class
        """
        raise ValueError("read_data_file not defined.")

    def read_context_not_modified_ended(self, error, file_name, sheet_list=None):
        # Close "Reading..." dialog box, in this case application is not focused,
        # we call directly the dialog box
        self.reader = None
        self.wait_dialog = False
        self._current_dialog = None
        # Force refresh.
        self._refresh_center_braille_display()
        self._braille_display.new_data_available_event.set()

        if error is None:
            # Ask to add the file to locked file (necessary if file re-opens after start-up)
            if EDITOR_APP_LOG <= logging.ERROR:
                log.error(f"locked file {self._original_file_name=}-{self._file_name=}")
            self._put_in_function_queue(
                FunctionId.FUNCTION_CHANGE_LOCKED_FILE,
                **{
                    "app": self,
                    "old_file": self._original_file_name,
                    "new_file": self._original_file_name,
                },
            )
        else:
            self.read_ended_error(error)

    def read_context_modified_ended(self, error, file_name, sheet_list=None):
        # Close "Reading..." dialog box, in this case application is not focused,
        # we call directly the dialog box
        self.reader = None
        self.wait_dialog = False
        self._current_dialog = None
        self.editor.set_is_modified(True)
        # Force refresh.
        self._refresh_center_braille_display()
        self._braille_display.new_data_available_event.set()

        if error is None:
            # Delete the context files.
            Path(file_name).unlink()
            specific_file = editor.ReadWriteSpecificFile(file_name)
            Path(specific_file.compute_specific_file()).unlink()
            # re-arm is_modified flag
            self.editor.set_is_modified(True)
            # Ask to add the file to locked file (necessary if file re-opens after start-up)
            if EDITOR_APP_LOG <= logging.ERROR:
                log.error(f"locked file {self._original_file_name=}-{self._file_name=}")
            self._put_in_function_queue(
                FunctionId.FUNCTION_CHANGE_LOCKED_FILE,
                **{
                    "app": self,
                    "old_file": self._original_file_name,
                    "new_file": self._original_file_name,
                },
            )

        else:
            self.read_ended_error(error)

    def _create_editor(self, lines):
        """
        To overload if editor is not editor.Editor
        """
        # Convert lines according to the type of braille chosen.
        braille_lines = list()
        for line in lines:
            braille_lines.append(self._transform_text_to_braille(line))
        editor_instance = editor.Editor(self.editor_line_length(), braille_lines)
        if self.read_only_from_specific is not None:
            editor_instance.read_only = self.read_only_from_specific
        else:
            editor_instance.read_only = self.read_only_from_opening
        return editor_instance

    def read_file_add_line(self, line, marker=False):
        if self._killed:
            # The reading file is linked to an dead editor => Ignore action
            return
        # Acquire editor ressources
        with self.lock:
            if not self.editor:
                index = 0
                # Create editor instance.
                lines = list()
                lines.append(line)
                # The editor line length is defined here. Actually it is a param_setting
                # but it could be an independant param of each document.
                self.editor = self._create_editor(lines)
            else:
                index = self.editor.paragraphs_count()
                self.editor.append_paragraph(self._transform_text_to_braille(line))
            if marker:
                # Put marker on the line.
                self.editor.set_caret_on_paragraph(index)
                # Put a marker at the beginning of the new paragraph
                self.editor.function(editor.Editor.Functions.MARKER, **{"ctrl": True})
                # Replace caret at the start of document (Ctrl+Home function)
                self.editor.function(
                    editor.Editor.Functions.MOVE_HOME, **{"ctrl": True}
                )
        # Wait until the caret line has been read.
        not_reach = False
        if self.caret_from_specific is not None:
            not_reach = True
            with self.lock:
                self.lines_count += self.editor.last_paragraph_lines_count()
            # print("Read line {}".format(lines_count))
            # End of wait if cursor position is reached or if complete document is read.
            if self.caret_from_specific.end.y < self.lines_count:
                not_reach = False
            elif self.reader.state == editor.ReadFile.STATE_ENDED:
                # Reading thread ended but the cursor line is not found ???
                not_reach = False
                # Lose reference on reader thread.
                self.reader = None

            if not not_reach:
                # print("!!! Reading caret line !!!)")
                # Put caret at saved position.
                if self.wait_dialog:
                    self.wait_dialog = False
                    with self.lock:
                        self.editor.set_caret(self.caret_from_specific)
                    if self.markers_from_specific is not None:
                        with self.lock:
                            self.editor.set_markers(self.markers_from_specific)
                    if self.read_only_from_specific is not None:
                        self.editor.read_only = self.read_only_from_specific
                    else:
                        self.editor.read_only = self.read_only_from_opening
                    # Ask main thread to close dialog box.
                    self._refresh_center_braille_display()
                    self._put_in_function_queue(
                        FunctionId.FUNCTION_CLOSE_DIALOG_BOX, **{"app": self}
                    )
        else:
            if self.wait_dialog:
                # Ask main thread to close dialog box.
                self.wait_dialog = False
                self._refresh_center_braille_display()
                self._put_in_function_queue(
                    FunctionId.FUNCTION_CLOSE_DIALOG_BOX, **{"app": self}
                )

    def read_file_ended(self, error, file_name, sheet_list, score=None):
        self.reader = None
        # score parameters is not used, it is just to have the same footprint as read_file_ended of music_app.
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("File name for writing operation is {}".format(file_name))
        if self._killed:
            # The reading file is linked to an dead editor => Ignore action
            return
        if error is None:
            # Create an empty editor if no lines read from file
            self.__create_empty_editor_if_none()
            if self.wait_dialog:
                # Ask main thread to close dialog box.
                self.wait_dialog = False
            self._file_name = file_name
            if self._file_name != self._original_file_name:
                # Ask main thread to launch the document saving.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_SAVE_AND_DELETE_ORIGINAL, **{"app": self}
                )
            self._refresh_center_braille_display()
            self._put_in_function_queue(
                FunctionId.FUNCTION_CLOSE_DIALOG_BOX, **{"app": self}
            )
        else:
            self.read_ended_error(error)

    def __create_empty_editor_if_none(self):
        with self.lock:
            if not self.editor:
                # Create editor instance.
                lines = list()
                lines.append("")
                self.editor = editor.Editor(self.editor_line_length(), lines)
                self.editor.read_only = self.read_only_from_opening

    def read_ended_error(self, error):
        if EDITOR_APP_LOG <= logging.WARNING:
            log.warning("Error reading file:{}".format(error))
        # Display a dialogbox and close editor.
        self.last_error = error
        if isinstance(error, editor.SelectSheet):
            self._put_in_function_queue(FunctionId.FUNCTION_SELECT_SHEET_DIALOG_BOX)
        else:
            # Create an empty editor if no lines read from file
            self.__create_empty_editor_if_none()
            # Display error and close editor.
            self._put_in_function_queue(
                FunctionId.FUNCTION_DISPLAY_LAST_ERROR_AND_CLOSE_EDITOR
            )

    def _transform_text_to_braille(self, line):
        """
        Transform the line to a text line in grade1 or grade2 according to the parameter.
        """
        if self.braille_type == "grade1":
            braille = BnoteApp.lou.text_to_grade1(line)
            return braille[0]
        elif self.braille_type == "grade2":
            braille = BnoteApp.lou.text_to_grade2(line)
            return braille[0]
        else:
            return line

    def _transform_braille_to_text(self, line):
        """
        Transform the line in text grade1 or grade2 to text according to the parameter.
        """
        if line is None:
            return None
        if self.braille_type == "grade1":
            text = BnoteApp.lou.grade1_to_text(line)
            return text[0]
        elif self.braille_type == "grade2":
            text = BnoteApp.lou.grade2_to_text(line)
            return text[0]
        else:
            return line

    # ---------------
    # Menu functions.

    def _exec_close(self):
        if self.editor.is_modified():
            if not self._dialog_is_reading_file():
                # Ask confirmation.
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_("do you want to save the document before closing?"),
                    buttons=[
                        ui.UiButton(name=_("&yes"), action=self._exec_close_yes_dialog),
                        ui.UiButton(name=_("&no"), action=self._exec_close_no_dialog),
                        ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
        else:
            self._killed = True
            self._put_in_function_queue(
                FunctionId.FUNCTION_CLOSE_EDITOR, **{"app": self}
            )

    def _exec_save(self, function=FunctionId.FUNCTION_CLOSE_DIALOG_BOX):
        if not self._dialog_is_reading_file():
            # Write editor in a file
            if self._file_name is not None:
                # Display save in progress...
                self._current_dialog = ui.UiInfoDialogBox(message=_("saving..."))
                if self.editor.is_modified() or not path.exists(self._file_name):
                    write_file = self.write_data_file(
                        BnoteApp.lou,
                        self._file_name,
                        self._get_line,
                        self._end_save,
                        function,
                    )
                    write_file.start()
                    # Wait saving and close dialog box
                    # SEE _end_save()
                else:
                    # Document not modified, save specific file and continue.
                    # Simulate end of save document.
                    self._end_save(None, function)
            else:
                if EDITOR_APP_LOG <= logging.WARNING:
                    log.warning(
                        "no file name associated to document !, reading not ended ?"
                    )

    def _exec_cleanup(self):
        if not self._dialog_is_reading_file():
            # Remove all consecutive empty paragraph of the document.
            self._current_dialog = ui.UiInfoDialogBox(message=_("cleanup..."))
            self.wait_dialog = True
            # Call in a thread "_thread_cleanup" with 1 as name argument.
            x = threading.Thread(target=self._thread_cleanup, args=(1,))
            x.start()

    def _thread_cleanup(self, name):
        with self.lock:
            res = self.editor.clean_up()
        # Ask main thread to launch the document saving.
        self.wait_dialog = False
        self._current_dialog = None
        # Exit from dialog box.
        self._refresh_center_braille_display()
        self._put_in_function_queue(FunctionId.FUNCTION_EDITOR_BRAILLE_REFRESH)

    def _exec_statistics(self):
        with self.lock:
            (paragraphs_count, words_count, characters_count) = self.editor.statistics()
        self._current_dialog = ui.UiDialogBox(
            name=_("statistics"),
            item_list=[
                ui.UiEditBox(
                    name=_("filename"),
                    value=("", BnoteApp.braille_form(self.get_display_filename())),
                ),
                ui.UiEditBox(
                    name=_("paragraphs"),
                    value=("", BnoteApp.braille_form(str(paragraphs_count))),
                ),
                ui.UiEditBox(
                    name=_("words"), value=("", BnoteApp.braille_form(str(words_count)))
                ),
                ui.UiEditBox(
                    name=_("characters"),
                    value=("", BnoteApp.braille_form(str(characters_count))),
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_start_selection(self):
        self.editor.function(
            editor.Editor.Functions.SELECTION_MODE_ON, **{"shift": False}
        )
        # Synchronize menu to run F8, Esc correctly.
        self._menu.get_object(self._exec_start_selection).hide()
        self._menu.get_object(self._exec_end_selection).unhide()

    def _exec_end_selection(self):
        self.editor.function(
            editor.Editor.Functions.SELECTION_MODE_OFF, **{"shift": False}
        )
        # Synchronize menu to run F8, Esc correctly.
        self._menu.get_object(self._exec_start_selection).unhide()
        self._menu.get_object(self._exec_end_selection).hide()

    def _exec_cut(self):
        self.editor.function(editor.Editor.Functions.CUT, **{"shift": False})

    def _exec_copy(self):
        self.editor.function(editor.Editor.Functions.COPY, **{"shift": False})

    def _exec_paste(self):
        self.editor.function(editor.Editor.Functions.PASTE, **{"shift": False})

    def _exec_select_all(self):
        self.editor.function(editor.Editor.Functions.SELECT_ALL, **{"shift": False})

    def _exec_undo(self):
        self.editor.function(editor.Editor.Functions.UNDO, **{"shift": False})

    def _exec_redo(self):
        self.editor.function(editor.Editor.Functions.REDO, **{"shift": False})

    def _exec_cursor(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("cursor"),
            item_list=[
                ui.UiEditBox(
                    name=_("line"),
                    value=(
                        "line",
                        self._transform_text_to_braille(
                            f"{self.editor.caret().end.y + 1}"
                        ),
                    ),
                ),
                ui.UiEditBox(
                    name=_("column"),
                    value=(
                        "column",
                        self._transform_text_to_braille(
                            f"{self.editor.caret().end.x + 1}"
                        ),
                    ),
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_cursor_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_beginning_document(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_HOME, **{"shift": False, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _exec_end_document(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_END, **{"shift": False, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _exec_preview_paragraphe(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_UP, **{"shift": False, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _exec_next_paragraphe(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_DOWN, **{"shift": False, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _exec_select_beginning(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_HOME, **{"shift": True, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _exec_select_ending(self):
        self.editor.function(
            editor.Editor.Functions.MOVE_END, **{"shift": True, "ctrl": True}
        )
        # Refresh braille display (useful after caret move)
        self._refresh_braille_display(self._braille_display.get_start_pos())

    def _dialog_is_reading_file(self):
        """
        Display a dialog box and returns True if reading file is in progress.
        """
        if self.__is_reading_file():
            # The file is not completely read.
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("the file is not completely read"),
                action=self._exec_cancel_dialog,
            )
            return True
        else:
            return False

    def _exec_find(self):
        if not self._dialog_is_reading_file():
            # Do a copy to allow cancel without degrading find's parameters
            self._current_dialog = ui.UiDialogBox(
                name=_("find"),
                item_list=[
                    ui.UiEditBox(
                        name=_("find"),
                        value=("find", self._replace_parameters.edit_seq),
                    ),
                    ui.UiButton(
                        name=_("&next"), action=self._exec_valid_next_find_dialog
                    ),
                    ui.UiButton(
                        name=_("&previous"),
                        action=self._exec_valid_previous_find_dialog,
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                    ui.UiCheckBox(
                        name=_("&ignore upper case"),
                        value=(
                            "ignore_case",
                            self._replace_parameters.is_ignore_case(),
                        ),
                    ),
                    ui.UiCheckBox(
                        name=_("&mask accent"),
                        value=(
                            "mask_accent",
                            self._replace_parameters.is_mask_accents(),
                        ),
                    ),
                    ui.UiCheckBox(
                        name=_("&entire word"),
                        value=(
                            "entire_word",
                            self._replace_parameters.is_entire_word(),
                        ),
                    ),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_replace(self):
        if not self._dialog_is_reading_file():
            # Do a copy to allow cancel without degrading find's parameters
            self._current_dialog = ui.UiDialogBox(
                name=_("replace"),
                item_list=[
                    ui.UiEditBox(
                        name=_("find"),
                        value=("find", self._replace_parameters.edit_seq),
                    ),
                    ui.UiEditBox(
                        name=_("replace"),
                        value=("replace", self._replace_parameters.replace_seq),
                    ),
                    ui.UiButton(
                        name=_("&next"), action=self._exec_valid_next_find_dialog
                    ),
                    ui.UiButton(
                        name=_("replace and n&ext"),
                        action=self._exec_valid_next_replace_dialog,
                    ),
                    ui.UiButton(
                        name=_("&previous"),
                        action=self._exec_valid_previous_find_dialog,
                    ),
                    ui.UiButton(
                        name=_("replace and p&revious"),
                        action=self._exec_valid_previous_replace_dialog,
                    ),
                    ui.UiButton(
                        name=_("replace &all"),
                        action=self._exec_valid_replace_all_dialog,
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                    ui.UiCheckBox(
                        name=_("&ignore upper case"),
                        value=(
                            "ignore_case",
                            self._replace_parameters.is_ignore_case(),
                        ),
                    ),
                    ui.UiCheckBox(
                        name=_("&mask accent"),
                        value=(
                            "mask_accent",
                            self._replace_parameters.is_mask_accents(),
                        ),
                    ),
                    ui.UiCheckBox(
                        name=_("&entire word"),
                        value=(
                            "entire_word",
                            self._replace_parameters.is_entire_word(),
                        ),
                    ),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_next(self):
        if not self._dialog_is_reading_file():
            self._find_exec(editor.Editor.Functions.FIND, False)

    def _exec_replace_and_next(self):
        if not self._dialog_is_reading_file():
            self._replace_exec(editor.Editor.Functions.REPLACE_AND_FIND, False)

    def _exec_previous(self):
        if not self._dialog_is_reading_file():
            self._find_exec(editor.Editor.Functions.FIND, True)

    def _exec_replace_and_previous(self):
        if not self._dialog_is_reading_file():
            self._replace_exec(editor.Editor.Functions.REPLACE_AND_FIND, False)

    def _exec_replace_all(self):
        if not self._dialog_is_reading_file():
            self._replace_exec(editor.Editor.Functions.REPLACE_ALL, False)

    def _exec_marker_insert_delete(self):
        if not self._dialog_is_reading_file():
            self.editor.function(editor.Editor.Functions.MARKER, **{"ctrl": True})

    def _exec_marker_next(self):
        if not self._dialog_is_reading_file():
            self.editor.function(editor.Editor.Functions.MARKER, **{"shift": False})

    def _exec_marker_previous(self):
        if not self._dialog_is_reading_file():
            self.editor.function(editor.Editor.Functions.MARKER, **{"shift": True})

    def _exec_marker_clear_all(self):
        if not self._dialog_is_reading_file():
            self.editor.function(
                editor.Editor.Functions.MARKER, **{"ctrl": True, "shift": True}
            )

    def _exec_read_document(self):
        self._exec_read_paragraph(read_full_document=True)

    def _exec_read_paragraph(self, read_full_document=False, purge_before_speak=True):
        SpeechManager().deregister_voice_event_callback("EndStream")
        index = self.editor.current_paragraph_index()
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("paragraph index {}".format(index))
        paragraph = self.editor.paragraph_text(index)
        if len(paragraph) != 0:
            paragraph_to_speak = self._transform_braille_to_text(paragraph)
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("speak with . added {}".format(paragraph_to_speak))
            if read_full_document:
                SpeechManager().register_voice_event_callback(
                    "EndStream", self._on_speaker_end_reading_doc
                )
            self.__is_speaking = True
            headphone = Gpio().is_head_phone()
            if headphone:
                volume = Settings().data["speech"]["volume_headphone"]
            else:
                volume = Settings().data["speech"]["volume_hp"]
            SpeechManager().speak(
                paragraph_to_speak,
                lang_id=Settings().data["speech"]["language"],
                synthesis=Settings().data["speech"]["synthesis"],
                voice=Settings().data["speech"]["voice"],
                headphone=headphone,
                volume=volume,
                speed=Settings().data["speech"]["speed"],
                purge_before_speak=purge_before_speak,
            )
        elif read_full_document:
            current_paragraph = self.editor.current_paragraph_index()
            if self.editor.function(
                editor.Editor.Functions.MOVE_DOWN, **{"shift": False, "ctrl": True}
            ):
                index = self.editor.current_paragraph_index()
                if index != current_paragraph:
                    self._exec_read_paragraph(read_full_document, purge_before_speak)

    def _on_speaker_end_reading_doc(self, **kwargs):
        if EDITOR_APP_LOG <= logging.WARNING:
            log.warning("callback finishing")
        with self.lock:
            current_paragraph = self.editor.current_paragraph_index()
            # Move to next paragraph.
            if self.editor.function(
                editor.Editor.Functions.MOVE_DOWN, **{"shift": False, "ctrl": True}
            ):
                index = self.editor.current_paragraph_index()
                if index != current_paragraph:
                    # We use NEXT_PARAGRAPH function but this function put caret on the last paragraph char.
                    # if caret is already someway in the paragraph.
                    self._exec_read_paragraph(read_full_document=True)
                    self._put_in_function_queue(
                        FunctionId.FUNCTION_EDITOR_BRAILLE_REFRESH
                    )
                    return
            # End of document.
            SpeechManager().deregister_voice_event_callback("EndStream")
            self.__is_speaking = False

    def _stop_speaking(self):
        SpeechManager().deregister_voice_event_callback("EndStream")
        SpeechManager().stop()
        self.__is_speaking = False

    def _exec_volume(self):
        self._current_dialog = VolumeDialogBox(
            _("volume"), _("&value"), self.__save_the_new_volume, self.channel
        )

    # Appelé depuis input_command
    def __volume_down_from_shortcut(self):
        level = VolumeDialogBox.volume_down(
            channel=self.channel, with_voice_feedback=(self.channel == "speech")
        )
        self.__save_the_new_volume(level)

    def __volume_up_from_shortcut(self):
        level = VolumeDialogBox.volume_up(
            channel=self.channel, with_voice_feedback=(self.channel == "speech")
        )
        self.__save_the_new_volume(level)

    def __save_the_new_volume(self, volume):
        # Save the new Volume in settings.
        Volume().set_volume(volume, self.channel)
        Settings().save()
        # Alert internal about settings change.
        headphone = Gpio().is_head_phone()
        if headphone:
            key = "volume_headphone"
        else:
            key = "volume_hp"
        self._put_in_function_queue(
            FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": self.channel, "key": key}
        )

    def _exec_speed(self):
        self._current_dialog = SpeedDialogBox(
            _("speed"),
            _("&value"),
            self.__save_the_new_speed,
            Settings().data["speech"]["speed"],
            Settings().VALID_VALUES["speech"]["speed"],
        )

    def __speed_down_from_shortcut(self):
        current_speed = Settings().data["speech"]["speed"]
        new_speed = SpeedDialogBox.speed_down(
            current_speed, Settings().VALID_VALUES["speech"]["speed"]
        )
        if new_speed != current_speed:
            Settings().data["speech"]["speed"] = new_speed
            Settings().save()
            self.refresh_document()

    def __speed_up_from_shortcut(self):
        current_speed = Settings().data["speech"]["speed"]
        new_speed = SpeedDialogBox.speed_up(
            current_speed, Settings().VALID_VALUES["speech"]["speed"]
        )
        if new_speed != current_speed:
            Settings().data["speech"]["speed"] = new_speed
            Settings().save()
            self.refresh_document()

    def __save_the_new_speed(self, new_speed):
        # Save the new speed in settings.
        try:
            Settings().data["speech"]["speed"] = int(new_speed)
            Settings().save()

            # Alert internal about settings change.
            self._put_in_function_queue(
                FunctionId.FUNCTION_SETTINGS_CHANGE,
                **{"section": "speech", "key": "speed"},
            )
        except ValueError:
            pass

    def _exec_application(self):
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    # ---------------
    # DialogBox validation functions.
    def _exec_valid_cursor_dialog(self):
        # get parameters
        kwargs = self._current_dialog.get_values()
        # Close dialog box.
        self._current_dialog = None
        if EDITOR_APP_LOG <= logging.INFO:
            log.info(f"cursor dialog box validation {kwargs=}")
        line = -1
        column = -1
        # Validate new cursor.
        try:
            # line is based zero in editor
            line = int(kwargs["line"]) - 1
            if line < 0:
                raise ValueError
        except ValueError:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("invalid line number."),
                action=self._exec_cancel_dialog,
            )
        try:
            # column is based zero in editor
            column = int(kwargs["column"]) - 1
            if column < 0:
                raise ValueError
        except ValueError:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("invalid column number."),
                action=self._exec_cancel_dialog,
            )
        if line != -1 and column != -1:
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("Validate new cursor y:{} x:{}".format(line, column))
            with self.lock:
                res = self.editor.function(
                    editor.Editor.Functions.PUT_CARET,
                    **{"shift": False, "ctrl": False, "pos": editor.Pos(column, line)},
                )
            if not res:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("coordinates apart from document."),
                    action=self._exec_cancel_dialog,
                )

    def _exec_close_yes_dialog(self):
        self._killed = True
        self._save(FunctionId.FUNCTION_CLOSE_EDITOR)

    def _exec_close_no_dialog(self):
        self._killed = True
        self._put_in_function_queue(FunctionId.FUNCTION_CLOSE_EDITOR, **{"app": self})

    def _exec_valid_next_find_dialog(self):
        self._find_exec(editor.Editor.Functions.FIND, False)

    def _exec_valid_previous_find_dialog(self):
        self._find_exec(editor.Editor.Functions.FIND, True)

    def _exec_valid_next_replace_dialog(self):
        self._replace_exec(editor.Editor.Functions.REPLACE_AND_FIND, False)

    def _exec_valid_previous_replace_dialog(self):
        self._replace_exec(editor.Editor.Functions.REPLACE_AND_FIND, True)

    def _exec_valid_replace_all_dialog(self):
        self._replace_exec(editor.Editor.Functions.REPLACE_ALL, False)

    def _find_exec(self, editor_function, shift):
        if self._current_dialog:
            # get parameters
            kwargs = self._current_dialog.get_values()
            replace_seq = ""
            if "replace" in kwargs:
                replace_seq = kwargs["replace"]
            if EDITOR_APP_LOG <= logging.INFO:
                log.info(f"find previous dialog box validation {kwargs=}")
            find_parameter = editor.FindParameters(
                find_seq=kwargs["find"],
                ignore_case=kwargs["ignore_case"],
                mask_accents=kwargs["mask_accent"],
                entire_word=kwargs["entire_word"],
                replace_seq=replace_seq,
            )
        else:
            find_parameter = self._replace_parameters
        if not find_parameter.is_valid():
            # Invalid parameters, abort function.
            # Open dialog box to indicate invalid parameters.
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("the string found is not a word !"),
                action=self._exec_cancel_dialog,
            )
        else:
            self._replace_parameters = find_parameter
            self._find_replace_end(editor_function, shift)

    def _replace_exec(self, editor_function, shift):
        if self._current_dialog:
            # get parameters
            kwargs = self._current_dialog.get_values()
            if EDITOR_APP_LOG <= logging.INFO:
                log.info(f"find previous dialog box validation {kwargs=}")
            replace_parameter = editor.FindParameters(
                find_seq=kwargs["find"],
                ignore_case=kwargs["ignore_case"],
                mask_accents=kwargs["mask_accent"],
                entire_word=kwargs["entire_word"],
                replace_seq=kwargs["replace"],
            )
        else:
            replace_parameter = self._replace_parameters
        if not replace_parameter.is_valid():
            # Invalid parameters, abort function.
            # Open dialog box to indicate invalid parameters.
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("replacement can not be done."),
                action=self._exec_cancel_dialog,
            )
        else:
            self._replace_parameters = replace_parameter
            if EDITOR_APP_LOG <= logging.INFO:
                log.info(f"After edit box {self._replace_parameters=}")
            self._find_replace_end(editor_function, shift)

    def _find_replace_end(self, editor_function, shift):
        res = self.editor.function(
            editor_function,
            **{"shift": shift, "replace_parameters": self._replace_parameters},
        )
        if not res:
            # Open dialog box to indicate that research failed.
            if shift:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("start of document reached, string not found."),
                    action=self._exec_cancel_dialog,
                )
            else:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("end of document reached, string not found."),
                    action=self._exec_cancel_dialog,
                )
        else:
            # In case of research successfully, editor has a new selection of text.
            # Close dialog box.
            self._current_dialog = None
            # Selection change, if forward display command is hit, it starts from cursor position.
            self.is_moving_display = False
            # Refresh braille display
            self._refresh_center_braille_display()

    def _get_line(self, line_number):
        with self.lock:
            line = self.editor.paragraph_text(line_number)
        return self._transform_braille_to_text(line)

    def _end_save(self, error, function):
        if EDITOR_APP_LOG <= logging.WARNING:
            log.warning("_end_save() called !")
        if error is None:
            self.editor.set_is_modified(False)
            if function == FunctionId.FUNCTION_DELETE_ORIGINAL:
                # add filename as argument
                self._put_in_function_queue(
                    function, **{"filename": self._original_file_name}
                )
            elif (
                function == FunctionId.FUNCTION_CLOSE_DIALOG_BOX
                or function == FunctionId.FUNCTION_CLOSE_EDITOR
            ):
                self._put_in_function_queue(function, **{"app": self})
            else:
                self._put_in_function_queue(function)
        else:
            # Error during write file => Display an error dialog box
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning("file save error : {}".format(error))
            self.last_error = error
            self._put_in_function_queue(FunctionId.FUNCTION_DISPLAY_LAST_ERROR)

    def _save(self, function=FunctionId.FUNCTION_CLOSE_DIALOG_BOX):
        if EDITOR_APP_LOG <= logging.WARNING:
            log.warning("Save file")
        # Write editor in a file
        if self._file_name is not None:
            # Display save in progress...
            self._current_dialog = ui.UiInfoDialogBox(message=_("saving..."))
            if self.editor.is_modified() or not path.exists(self._file_name):
                write_file = self.write_data_file(
                    BnoteApp.lou,
                    self._file_name,
                    self._get_line,
                    self._end_save,
                    function,
                )
                write_file.start()
                # Wait saving and close dialog box
                # SEE _end_save(self)
            else:
                # Document not modified, save specific file and continue.
                # Simulate end of save document.
                self._end_save(None, function)
        else:
            if EDITOR_APP_LOG <= logging.WARNING:
                log.warning(
                    "No file name associated to document !, reading not ended ?"
                )

    def write_data_file(self, lou, full_file_name, get_line, on_end, function):
        """
        To overload by child class
        """
        raise ValueError("write_data_file not defined.")

    def _select_sheet(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("editor"),
            item_list=[
                ui.UiListBox(
                    name=_("&sheet"), value=("sheet_name", self.last_error.sheet_list)
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_ok_select_sheet_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_ok_select_sheet_dialog(self):
        # Get xlsx sheet_name.
        kwargs = self._current_dialog.get_values()
        sheet_name = kwargs["sheet_name"]
        if EDITOR_APP_LOG <= logging.WARNING:
            log.warning(f"panel:{sheet_name}")
        # Read the file.
        # Launch reading thread for others extensions
        self._current_dialog = ui.UiInfoDialogBox(message=_("reading..."))
        self.wait_dialog = True
        self.lines_count = 0
        self.reader = editor.ReadFile(
            BnoteApp.lou,
            self._original_file_name,
            self._language,
            self.read_file_add_line,
            self.read_file_ended,
            sheet_name=sheet_name,
        )
        self.reader.start()

    # ---------------
    # Key event functions.

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
        done = False
        if function_id == FunctionId.FUNCTION_SAVE_AND_DELETE_ORIGINAL:
            self._save(FunctionId.FUNCTION_DELETE_ORIGINAL)
            done = True
        elif function_id == FunctionId.FUNCTION_SELECT_SHEET_DIALOG_BOX:
            self._select_sheet()
            done = True
        elif function_id == FunctionId.FUNCTION_DISPLAY_LAST_ERROR:
            # Display error.
            text = _("unknown error")
            if self.last_error:
                text = "{}".format(self.last_error)
            self._current_dialog = ui.UiInfoDialogBox(
                message=text, action=self._exec_cancel_dialog
            )
            done = True
        elif function_id == FunctionId.FUNCTION_DISPLAY_LAST_ERROR_AND_CLOSE_EDITOR:
            # Display error and close close editor function on ok button.
            text = _("unknown error")
            if self.last_error:
                text = "{}".format(self.last_error)
            self._current_dialog = ui.UiInfoDialogBox(
                message=text, action=self._exec_close
            )
            done = True
        elif function_id == FunctionId.FUNCTION_EDITOR_BRAILLE_REFRESH:
            self._refresh_braille_display()
            # Force refresh.
            self._braille_display.new_data_available_event.set()
            done = True
        else:
            # Call base class decoding.
            done = super(EditorBaseApp, self).input_function(*args, **kwargs)
        return done

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = False
        if key_id == Keyboard.KeyId.KEY_NONE:
            # Ignore keys up event.
            return False

        # Stop speech
        self._stop_speaking()
        # Kill braille display autoscroll.
        self._is_autoscroll = False

        if EDITOR_APP_LOG <= logging.INFO:
            log.info("key_id={}".format(key_id))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(EditorBaseApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            if (modifier == 0) and (key_id == Keyboard.KeyId.KEY_BACKWARD):
                self._backward_display()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_FORWARD):
                self._forward_display()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_TOGGLE_GRADE2):
                self._toggle_grade2()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_AUTOSCROLL):
                self._autocroll()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_SPEECH_VOLUME_DOWN):
                self.__volume_down_from_shortcut()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_SPEECH_VOLUME_UP):
                self.__volume_up_from_shortcut()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_SPEECH_SPEED_DOWN):
                self.__speed_down_from_shortcut()
                done = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_SPEECH_SPEED_UP):
                self.__speed_up_from_shortcut()
                done = True
            else:
                # command treatment for document.
                kwargs = BnoteApp.keyboard.decode_modifiers(modifier)
                # Get the function from switcher dictionnary
                (editor_function, new_kwargs) = EditorBaseApp.command_switcher.get(
                    key_id, (None, None)
                )
                if editor_function:
                    # Execute the function
                    if new_kwargs:
                        # Overload shift and ctrl parameters
                        kwargs.update(new_kwargs)
                    with self.lock:
                        self.editor.function(editor_function, **kwargs)
                    # Refresh braille display
                    self._refresh_center_braille_display()
                    done = True
        return done

    command_switcher = {
        Keyboard.KeyId.KEY_CARET_UP: (editor.Editor.Functions.MOVE_UP, None),
        Keyboard.KeyId.KEY_CARET_DOWN: (editor.Editor.Functions.MOVE_DOWN, None),
        Keyboard.KeyId.KEY_CARET_RIGHT: (editor.Editor.Functions.MOVE_RIGHT, None),
        Keyboard.KeyId.KEY_CARET_LEFT: (editor.Editor.Functions.MOVE_LEFT, None),
        Keyboard.KeyId.KEY_START_DOC: (
            editor.Editor.Functions.MOVE_HOME,
            {"shift": False, "ctrl": True},
        ),
        Keyboard.KeyId.KEY_END_DOC: (
            editor.Editor.Functions.MOVE_END,
            {"shift": False, "ctrl": True},
        ),
    }

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param character: unicode char
        :param data: brut braille comb. for advanced treatment
        :return: True if command treated, otherwise False
        """
        if EDITOR_APP_LOG <= logging.INFO:
            log.info(f"{modifier=} {character=}")
        # Stop speech
        self._stop_speaking()
        # Kill grade2 mode
        self._is_forward_grade2 = False
        # Kill moving display without caret mode.
        self.is_moving_display = False
        # Kill braille display autoscroll.
        self._is_autoscroll = False

        done = BnoteApp.input_character(self, modifier, character, data)
        if not done:
            kwargs = super(EditorBaseApp, self).keyboard.decode_modifiers(modifier)
            if kwargs["alt"] or kwargs["ctrl"]:
                # No treatment on character with alt or ctrl
                return False
            # Document input character treatment.
            # stop if edition is False
            if (
                modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_INS
                and character == "f"
            ):
                # Switch to incremental search
                self.is_editing = False
                # Refresh to erase message 'ins...'
                self._refresh_center_braille_display()
                # Reset quick search buffer.
                self.__quick_search.clear()
                done = True
            elif self.is_editing:
                # Input character in editor.
                with self.lock:
                    # Modifiers could be transmitted ?
                    self.editor.function(
                        editor.Editor.Functions.PUT_STRING, **{"text": character}
                    )
                # Refresh braille display
                self._refresh_center_braille_display()
                done = True
            elif modifier == 0:
                # Incremental search, put caracter in quick search.
                return self.__quick_search.do_quick_search(character)
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        # Stop speech
        self._stop_speaking()
        # Kill braille display autoscroll.
        self._is_autoscroll = False

        if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE:
            # End of incremental search, Escape key can have other action with menu shortcut.
            self.is_editing = True
        done = super().input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # command treatment for document.
            kwargs = BnoteApp.keyboard.decode_modifiers(modifier)
            # Get the function from switcher dictionnary
            editor_function = EditorBaseApp.bramigraph_switcher.get(bramigraph, None)
            if editor_function:
                # Execute the function
                with self.lock:
                    self.editor.function(editor_function, **kwargs)
                # Refresh braille display
                self._refresh_center_braille_display()
                done = True
        return done

    bramigraph_switcher = {
        # Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: Editor.Functions.SELECTION_MODE_OFF,
        Keyboard.BrailleFunction.BRAMIGRAPH_TAB: editor.Editor.Functions.TAB,
        Keyboard.BrailleFunction.BRAMIGRAPH_HOME: editor.Editor.Functions.MOVE_HOME,
        Keyboard.BrailleFunction.BRAMIGRAPH_END: editor.Editor.Functions.MOVE_END,
        Keyboard.BrailleFunction.BRAMIGRAPH_PRIOR: editor.Editor.Functions.PAGE_UP,
        Keyboard.BrailleFunction.BRAMIGRAPH_NEXT: editor.Editor.Functions.PAGE_DOWN,
        Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: editor.Editor.Functions.MOVE_LEFT,
        Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: editor.Editor.Functions.MOVE_RIGHT,
        Keyboard.BrailleFunction.BRAMIGRAPH_UP: editor.Editor.Functions.MOVE_UP,
        Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: editor.Editor.Functions.MOVE_DOWN,
        Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: editor.Editor.Functions.DELETE,
        # Keyboard.BrailleFunction.BRAMIGRAPH_F2: editor.Editor.Functions.MARKER,
        # Keyboard.BrailleFunction.BRAMIGRAPH_F3: editor.Editor.Functions.FIND,
        # Keyboard.BrailleFunction.BRAMIGRAPH_F4: editor.Editor.Functions.REPLACE_AND_FIND,
        # Keyboard.BrailleFunction.BRAMIGRAPH_F5: editor.Editor.Functions.REPLACE_ALL,
        Keyboard.BrailleFunction.BRAMIGRAPH_F8: editor.Editor.Functions.SELECTION_MODE_ON,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: editor.Editor.Functions.BACKSPACE,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE: editor.Editor.Functions.SPACE,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: editor.Editor.Functions.CARRIAGE_RETURN,
    }

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        if EDITOR_APP_LOG <= logging.INFO:
            log.info(f"{modifier=} {position=} {key_type=}")
        # Stop speech
        self._stop_speaking()
        # Kill braille display autoscroll.
        self._is_autoscroll = False

        done = super(EditorBaseApp, self).input_interactive(
            modifier, position, key_type
        )
        if not done:
            # interactive key treatment for editor.
            if key_type == Keyboard.InteractiveKeyType.DOUBLE_CLIC:
                # Kill grade2 mode
                # DP FIXME Something to do when interactive key press on grade2 braille display.
                self._is_forward_grade2 = False
                # Kill moving display without caret mode.
                self.is_moving_display = False
                with self.lock:
                    self.editor.function(
                        editor.Editor.Functions.SELECT_WORD,
                        **{
                            "pos": editor.Pos(
                                self._braille_display.get_start_pos() + position - 1,
                                self.editor.caret().end.y,
                            )
                        },
                    )
            else:
                with self.lock:
                    # if not self.is_moving_display:
                    #     self.moving_display_caret = self.editor.caret()
                    #     self.is_moving_display = True
                    # Kill grade2 mode
                    # DP FIXME Something to do when interactive key press on grade2 braille display.
                    self._is_forward_grade2 = False
                    if self.is_moving_display:
                        # Kill moving display without caret mode.
                        self.is_moving_display = False
                        line = self.moving_display_caret.end.y
                    else:
                        line = self.editor.caret().end.y
                    self.editor.function(
                        editor.Editor.Functions.PUT_CARET,
                        **{
                            "pos": editor.Pos(
                                self._braille_display.get_start_pos() + position - 1,
                                line,
                            )
                        },
                    )
            # Refresh braille display (useful after caret move)
            self._refresh_braille_display(self._braille_display.get_start_pos())
            done = True
        else:
            # DP FIXME Something to do when interactive key press on grade2 braille display.
            self._is_forward_grade2 = False
            # Kill moving display without caret mode.
            self.is_moving_display = False
        return done

    # ---------------
    # braille display functions.
    def _convert_line_to_dots(self, line):
        """
        Convert the text line to braille according to braille type.
        This method is overload by music editor.
        """
        if self.braille_type and (
            (self.braille_type == "grade1") or (self.braille_type == "grade2")
        ):
            return BnoteApp.lou.to_dots_6(line)
        else:
            static_dots = BnoteApp.lou.to_dots_8(line)
            # Mask dot 78 if hide parameter is set.
            return self._mask_dot_78(static_dots)

    @staticmethod
    def _mask_dot_78(static_dots):
        # Mask dot 78 if hide parameter is set.
        if not Settings().data["editor"]["dot78_visible"]:
            masked_dots = ""
            for b in static_dots:
                masked_dots = "".join([masked_dots, chr(ord(b) & 0xFF3F)])
            static_dots = masked_dots
        return static_dots

    def _refresh_braille_display(self, offset=0, line_index=None):
        """
        Refresh braille display
        :param offset:
        :param line_index:
        :return:
        """
        if self.editor:
            with self.lock:
                (line, dots) = self.editor.editor_braille_line(line_index)
            blink_dots = BnoteApp.lou.byte_to_unicode_braille(dots)
            static_dots = self._convert_line_to_dots(line)
            BnoteApp.set_braille_display_line(
                self, line, static_dots, blink_dots, offset
            )
            if self._is_autoscroll:
                self._find_best_autoscroll_timeout(line, offset)

    # Algo to reduce self._autoscroll_timeout according to the texte displayed on braille.
    # FIXME : pour connaitre le contenu réel des cellules affichées sur la plage braille il faudrait analyser
    #  static_dots, blink_dots au lieu de line (qui est le text de la ligne)
    def _find_best_autoscroll_timeout(self, line, offset):
        braille_display_length = (
            braille_device_characteristics.get_braille_display_length()
        )
        remaining_line_len = len(line) - offset
        new_value = (
            Settings().data["editor"]["autoscroll"] * remaining_line_len
        ) / float(braille_display_length)
        optimized_autoscroll_timeout = self._autoscroll_timeout
        if new_value < Settings().VALID_VALUES["editor"]["autoscroll"].start:
            optimized_autoscroll_timeout = (
                Settings().VALID_VALUES["editor"]["autoscroll"].start
            )
        elif new_value > Settings().data["editor"]["autoscroll"]:
            optimized_autoscroll_timeout = Settings().data["editor"]["autoscroll"]
        else:
            optimized_autoscroll_timeout = int(new_value)
        if EDITOR_APP_LOG <= logging.ERROR:
            log.error(
                f"{remaining_line_len=} {self._autoscroll_timeout=} {optimized_autoscroll_timeout=}"
            )
        self._autoscroll_timeout = optimized_autoscroll_timeout

    def _refresh_center_braille_display(self):
        if self.next_refresh_disable:
            # Used when grade2 reading is activate via menu, to avoid to return to normal reading when exit from menu.
            return
        if self.editor:
            self._refresh_braille_display()
            self._braille_display.center(self.editor.caret().end.x)

    # braille_offset is offset on grade0
    def _grade2_refresh_braille_display(self, braille_offset):
        with self.lock:
            paragraph_text = self.editor.paragraph_text(self.grade2_paragraph_index)

        if paragraph_text:
            braille = None
            if self.braille_type == "grade1":
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("grade0:{}, {}".format(paragraph_text, braille_offset))
                (text_grade2, index1_origin, self.grade2_index_text, pos) = (
                    BnoteApp.lou.grade1_to_text(paragraph_text, braille_offset)
                )
                if text_grade2:
                    braille = BnoteApp.lou.to_dots_8(text_grade2)
            elif self.braille_type == "grade2":
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("grade0:{}, {}".format(paragraph_text, braille_offset))
                (text_grade2, index1_origin, self.grade2_index_text, pos) = (
                    BnoteApp.lou.grade2_to_text(paragraph_text, braille_offset)
                )
                if text_grade2:
                    braille = BnoteApp.lou.to_dots_8(text_grade2)
            else:
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("grade0:{}, {}".format(paragraph_text, braille_offset))
                (text_grade2, index1_origin, self.grade2_index_text, pos) = (
                    BnoteApp.lou.text_to_grade2(paragraph_text, braille_offset)
                )
                if text_grade2:
                    if EDITOR_APP_LOG <= logging.INFO:
                        log.info(
                            "grade2:{}, {}, {}, {}".format(
                                text_grade2, index1_origin, self.grade2_index_text, pos
                            )
                        )
                    braille = BnoteApp.lou.to_dots_6(text_grade2)
            if text_grade2 and braille:
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("braille:{}".format(braille))
                # dots = BnoteApp.lou.unicode_braille_to_byte(braille)
                # if EDITOR_APP_LOG <= logging.INFO:
                #     log.info("dots:{}".format(dots))
                blink = "\u2800" * len(braille)
                # BnoteApp.set_braille_display_dots_line(self, dots, blink, pos)
                BnoteApp.set_braille_display_line(
                    self, text_grade2, braille, blink, pos
                )

    def __quick_search_move_call_back(self, text_to_find) -> (bool, object()):
        if text_to_find and (text_to_find != ""):
            if EDITOR_APP_LOG <= logging.INFO:
                log.info(f"Quick search with <{text_to_find}>")
            self._replace_parameters = editor.FindParameters(
                text_to_find, ignore_case=True, mask_accents=True, entire_word=False
            )
            res = True
            with self.lock:
                res = self.editor.function(
                    editor.Editor.Functions.FIND,
                    **{"shift": False, "replace_parameters": self._replace_parameters},
                )
            if res:
                # In case of research successfully, editor has a new selection of text.
                # Refresh braille display
                self._refresh_center_braille_display()
        return True, None

    def _backward_display(self):
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("backward display")
        if self._is_forward_grade2:
            # Backward in grade2
            if self._braille_display.backward():
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("backward on paragraph")
            elif self.grade2_paragraph_index > 0:
                self.grade2_paragraph_index -= 1
                self._grade2_refresh_braille_display(0)
        else:
            # Backward in grade0
            if self.editor.caret().is_selection_empty():
                # Move caret if no selection.
                self._backward_display_with_caret_moving()
            else:
                if not self.is_moving_display:
                    self.moving_display_caret = self.editor.caret()
                    self.is_moving_display = True

                save_caret = editor.Caret(self.editor.caret())
                self.editor.set_caret(self.moving_display_caret)
                self._backward_display_with_caret_moving(save_caret)

    def _backward_display_with_caret_moving(self, save_caret=None):
        if self._braille_display.backward():
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("backward on line")
            with self.lock:
                self.editor.function(
                    editor.Editor.Functions.PUT_CARET,
                    **{
                        "shift": False,
                        "ctrl": False,
                        "pos": editor.Pos(
                            self._braille_display.get_start_pos(),
                            self.editor.caret().end.y,
                        ),
                    },
                )
        elif self.editor.caret().end.y != 0:
            # line change only if it is not the first line.
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("backward on line change => goto start of the new line")
            with self.lock:
                self.editor.function(
                    editor.Editor.Functions.MOVE_UP, **{"shift": False, "ctrl": False}
                )
                self.editor.function(
                    editor.Editor.Functions.MOVE_HOME, **{"shift": False, "ctrl": False}
                )
            # Compute braille offset position
            with self.lock:
                (line, dots) = self.editor.editor_braille_line(
                    self.editor.caret().end.y
                )
            offset = 0
            braille_display_length = (
                braille_device_characteristics.get_braille_display_length()
            )
            if line and (len(line) > braille_display_length):
                offset = len(line) - braille_display_length
            with self.lock:
                self.editor.function(
                    editor.Editor.Functions.PUT_CARET,
                    **{
                        "shift": False,
                        "ctrl": False,
                        "pos": editor.Pos(offset, self.editor.caret().end.y),
                    },
                )
            self._braille_display.set_start_pos(offset)
        # Refresh braille display (useful after caret move)
        if EDITOR_APP_LOG <= logging.DEBUG:
            log.debug("Backward offset{}".format(self._braille_display.get_start_pos()))
        self.__end_move_display(save_caret, self._braille_display.get_start_pos())

    def _toggle_grade2_from_menu(self):
        self._toggle_grade2()
        # Cut next refresh to avoid a return in grade0 forward mode.
        self.next_refresh_disable = True

    def _toggle_grade2(self):
        if self._is_forward_grade2:
            # Switch forward-backward to grade0
            self._is_forward_grade2 = False
            grade2_offset = self._braille_display.get_start_pos()
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("grade2_offset:{}".format(grade2_offset))
            grade0_offset = 0
            for offset in self.grade2_index_text:
                if offset == grade2_offset:
                    grade0_offset = offset
                    break
                if offset > grade2_offset:
                    break
                grade0_offset = offset
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("grade0_offset:{}".format(grade0_offset))
            with self.lock:
                pos = self.editor.paragraph_pos(
                    self.grade2_paragraph_index, grade0_offset
                )
                caret = editor.Caret()
                caret.start = pos
                caret.end = pos
                caret.old_x = pos.x
                self.editor.set_caret(caret)
            self._refresh_braille_display(grade0_offset)
        else:
            # Switch forward-backward to braille Grade 2
            self._is_forward_grade2 = True
            # braille_offset = self._braille_display.get_start_pos()
            with self.lock:
                # Get current paragraph from editor.
                pos = self.editor.current_paragraph_and_line_index()
            self.grade2_paragraph_index = pos.x
            if EDITOR_APP_LOG <= logging.DEBUG:
                log.debug(
                    "Convert to grade2 paragraph {} line index {}".format(pos.x, pos.y)
                )
            self._grade2_refresh_braille_display(pos.y)

    def _forward_display(self):
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("forward display")
        if self._is_forward_grade2:
            # forward in grade2 if braille_type is dot8
            if self._braille_display.forward():
                if EDITOR_APP_LOG <= logging.INFO:
                    log.info("forward on paragraph")
            elif self.grade2_paragraph_index < self.editor.paragraphs_count() - 1:
                self.grade2_paragraph_index += 1
                paragraph_text = ""
                with self.lock:
                    paragraph_text = self.editor.paragraph_text(
                        self.grade2_paragraph_index
                    ).replace(" ", "")
                if paragraph_text == "":
                    self._forward_display()
                else:
                    self._grade2_refresh_braille_display(0)
        else:
            # Forward in grade0
            if self.editor.caret().is_selection_empty():
                # Move caret if no selection.
                self._forward_display_with_caret_moving()
            else:
                # if selection, create a moving_display_caret
                if not self.is_moving_display:
                    self.moving_display_caret = self.editor.caret()
                    self.is_moving_display = True

                save_caret = editor.Caret(self.editor.caret())
                self.editor.set_caret(self.moving_display_caret)
                self._forward_display_with_caret_moving(save_caret)

    def _forward_display_with_caret_moving(self, save_caret=None):
        braille_offset = self._braille_display.get_start_pos()
        if self._braille_display.forward():
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("Forward on line")
            braille_offset = self._braille_display.get_start_pos()
            # Put caret at the start of display.
            with self.lock:
                self.editor.function(
                    editor.Editor.Functions.PUT_CARET,
                    **{
                        "shift": False,
                        "ctrl": False,
                        "pos": editor.Pos(braille_offset, self.editor.caret().end.y),
                    },
                )
        else:
            # line change.
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("Forward on line change")
            with self.lock:
                while True:
                    if self.editor.function(
                        editor.Editor.Functions.MOVE_DOWN,
                        **{"shift": False, "ctrl": False},
                    ):
                        # Move to the start of the line
                        self.editor.function(
                            editor.Editor.Functions.MOVE_HOME,
                            **{"shift": False, "ctrl": False},
                        )
                        braille_offset = 0
                        (new_line, dots) = self.editor.editor_braille_line(
                            self.editor.caret().end.y
                        )
                        new_line = new_line.replace(" ", "")
                        if (
                            Settings().data["editor"]["forward_display_mode"]
                            == "normal"
                        ) or new_line != "":
                            # Line not empty, it is the right one.
                            break
                    else:
                        break

        # Refresh braille display
        if EDITOR_APP_LOG <= logging.DEBUG:
            log.debug("Forward offset{}".format(braille_offset))
        self.__end_move_display(save_caret, braille_offset)

    def __end_move_display(self, save_caret, braille_offset):
        line_index = None
        if save_caret:
            self.moving_display_caret = editor.Caret(self.editor.caret())
            line_index = self.editor.caret().end.y
            if EDITOR_APP_LOG <= logging.INFO:
                log.info("line to display is {}".format(line_index))
            self.editor.set_caret(save_caret)
        self._refresh_braille_display(braille_offset, line_index)

    # Call just before the application removing from internal menu.
    def on_close(self):
        self.save_specific_file(**{})

    def save_specific_file(self, **kwargs):
        if EDITOR_APP_LOG <= logging.INFO:
            log.info("on_close() => Save cursor and markers.")
        if self._file_name is not None and path.exists(self._file_name):
            file_name, file_extension = path.splitext(self._file_name)
            if file_extension:
                file_extension = file_extension.lower()
            if file_extension:
                # log.critical("try to lock editor")
                kwargs["markers"] = self.editor.markers()
                kwargs["caret"] = self.editor.caret()
                kwargs["read_only"] = "none"
                with self.lock:
                    # log.critical(f"editor locked {self._file_name=}")
                    # Write specific file associated to the text file written (if this file exists).
                    write_specific_file = editor.ReadWriteSpecificFile(self._file_name)
                    write_specific_file.write_specific_file(**kwargs)
        # log.critical("on_close of editor base ended")

    def on_delete(self):
        write_specific_file = editor.ReadWriteSpecificFile(self._file_name)
        if self._file_name is not None:
            write_specific_file.delete_specific_file()

    def _autocroll(self):
        self._autoscroll_timeout = 1
        self._is_autoscroll = True

    def on_timer(self):
        if self._is_autoscroll:
            if self._autoscroll_timeout > 1:
                self._autoscroll_timeout -= 1
            else:
                self._autoscroll_timeout = Settings().data["editor"]["autoscroll"]
                self._forward_display()
