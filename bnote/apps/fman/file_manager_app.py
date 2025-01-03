"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import datetime
import os
import threading
import time
from pathlib import Path
from bnote.apps.ai_assistant.ai_assistant_app import AiAssistantApp
from bnote.apps.edt.editor_app import EditorApp
from bnote.apps.eole.eole_api import EoleApi
from bnote.apps.eole.eole_crypto import EoleCrypto
from bnote.apps.eole.eole_search_dialog_box import EoleSearchDialogBox
from bnote.apps.media.mp3_app import Mp3App
from bnote.apps.music.music_app import MusicApp
from bnote.apps.daisy.daisy_app import DaisyApp
from bnote.tools import bt_util
from bnote.tools.io_util import Gpio
import bnote.ui as ui
from bnote.tools.clipboard import CLIP_FILE
from bnote.tools.keyboard import Keyboard
from bnote.apps.bnote_app import BnoteApp, FunctionId, MAX_EDITOR_APP
from bnote.tools.quick_search import QuickSearch

# from bnote.edt.editor import *
from bnote.apps.fman.file_manager import FileManager, Trash
from bnote.apps.fman.copy_move_tread import CopyMoveThread
from bnote.apps.fman.delete_thread import DeleteThread
from bnote.apps.fman.recent_file import RecentFile
from bnote.apps.fman.restore_from_trash_tread import RestoreFromTrashThread
from bnote.apps.fman.send_to_thread import SendToThread
from bnote.apps.fman.zip_thread import ZipThread
from bnote.apps.fman.unzip_thread import UnZipThread
from bnote.tools.yaupdater import YAUpdater
from bnote.tools.settings import SETTINGS_FILE, Settings
from bnote.apps.daisy.daisy import DaisyReader, DaisyReaderException

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, FILE_MANAGER_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(FILE_MANAGER_APP_LOG)


class FileManagerApp(BnoteApp):

    def __init__(self, put_in_function_queue, report_a_crash=False):
        super().__init__(put_in_function_queue)
        # The BrailleLine that will be "current_dir:self.__files[self.__focused_file]"
        self.__ui_line = None
        # The current folder
        self.__current_folder = FileManager.get_documents_path()
        # The selected files list
        self.__selected_files = []
        # If True the selection is extended.
        self.__extend_selection = False
        # The focused item that will be presented on the BrailleLine
        self.__focused_file_index = 0
        # The files list
        self.__files = None
        # Used with copy/cut/paste
        self.__copy_cut_paste_files = None
        self.__is_copy = False
        self.__is_cut = False
        # The thread for copy/move files
        self.__copy_move_thread = None
        # The thread for delete files
        self.__delete_thread = None
        # The thread for restore from trash
        self.__restore_from_trash_thread = None
        # The thread for send to files
        self.__send_to_thread = None
        # The thread for zip and backup files
        self.__zip_thread = None
        # The thread for unzip and restore files
        self.__unzip_thread = None
        # The list of file locked by editorApp (Useful to avoid file move on a locked file)
        self.__locked_filenames = []
        # The QuickSearch instance.
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)
        # Create the menu according to the current translation
        self.__create_menu()
        # construct the self.__files and the self.__files_braille_line
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)
        # For shutdown.
        self._shutdown_processing = False
        # Keep in mind the search eole dialog box while displaying a message (summary or download in progress)
        self.__eole_search__current_dialog = None
        # Open a simplified search dialog if True (or an advanced search dialog if False)
        self.__is_eole_simplified_search = True

        if report_a_crash:
            # If a crash append, alert user with a dialogbox.
            self._current_dialog = ui.UiInfoDialogBox(
                message=_(
                    "bnote restarts after a crash. More information available in crash folder."
                ),
                action=self._exec_cancel_dialog,
            )

    def translate_ui(self):
        self._in_menu = False
        self.__create_menu()
        self.__build_braille_line()

    def __create_file_manager_file_new_menu(self):
        return ui.UiMenuBar(
            name=_("&New"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("text(.&txt)"),
                    action=self._exec_new_text_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="N",
                ),
                ui.UiMenuItem(
                    name=_("music(.&bxml)"),
                    action=self._exec_new_bxml_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="B",
                ),
                ui.UiMenuItem(
                    name=_("music(.music&xml)"),
                    action=self._exec_new_musicxml_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="M",
                ),
                ui.UiMenuItem(
                    name=_("ai assistant(.&ai_txt)"),
                    action=self._exec_new_ai_assistant_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="I",
                ),
                ui.UiMenuItem(
                    name=_("&folder"),
                    action=self._exec_new_folder,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="D",
                ),
            ],
        )

    def __create_file_manager_eole_menu(self):
        return ui.UiMenuBar(
            name=_("&eole library"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&simplified search"),
                    action=self._exec_eole_simplified_search,
                ),
                ui.UiMenuItem(
                    name=_("&advanced search"), action=self._exec_eole_advanced_search
                ),
            ],
        )

    def __create_file_manager_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                self.__create_file_manager_file_new_menu(),
                ui.UiMenuItem(name=_("&send to"), action=self._exec_send_to),
                ui.UiMenuItem(
                    name=_("&rename"),
                    action=self._exec_rename,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("dele&te"),
                    action=self._exec_delete,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                ),
                ui.UiMenuItem(name=_("&zip"), action=self._exec_zip),
                ui.UiMenuItem(name=_("&unzip"), action=self._exec_unzip),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
                ui.UiMenuItem(
                    name=_("&open"),
                    action=self._exec_open,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(
                    name=_("o&pen to read"),
                    action=self._exec_read_only,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(name=_("re&cents"), action=self._exec_recent_file),
                ui.UiMenuItem(
                    name=_("fi&nd"),
                    action=self._exec_find_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="F",
                ),
                ui.UiMenuItem(
                    name=_("pro&perties"),
                    action=self._exec_properties,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1,
                ),
            ],
        )

    def __create_file_manager_with_usb_flash_drive_plugged_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                self.__create_file_manager_file_new_menu(),
                ui.UiMenuItem(
                    name=_("safely &unmount usb stick"),
                    action=self._exec_unmount_all_usb_flash_drives,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="U",
                ),
                ui.UiMenuItem(name=_("&send to"), action=self._exec_send_to),
                ui.UiMenuItem(
                    name=_("&rename"),
                    action=self._exec_rename,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("dele&te"),
                    action=self._exec_delete,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                ),
                ui.UiMenuItem(name=_("&zip"), action=self._exec_zip),
                ui.UiMenuItem(name=_("&unzip"), action=self._exec_unzip),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
                ui.UiMenuItem(
                    name=_("&open"),
                    action=self._exec_open,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(
                    name=_("o&pen to read"),
                    action=self._exec_read_only,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(name=_("re&cents"), action=self._exec_recent_file),
                ui.UiMenuItem(
                    name=_("fi&nd"),
                    action=self._exec_find_file,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="F",
                ),
            ],
        )

    def __create_file_manager_edit_menu(self):
        return ui.UiMenuBar(
            name=_("&edit"),
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
                ui.UiMenuItem(
                    name=_("select &all"),
                    action=self._exec_select_all,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="A",
                ),
            ],
        )

    def __create_file_manager_goto_menu(self):
        hide_v2_menu = not Gpio().gpio_hardware_v2()
        return ui.UiMenuBar(
            name=_("&goto"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("my &documents"), action=self._exec_goto_my_documents
                ),
                ui.UiMenuItem(
                    name=_("usb &key"),
                    action=self._exec_goto_usb_drives,
                    is_hide=hide_v2_menu,
                ),
                ui.UiMenuItem(name=_("&bluetooth"), action=self._exec_goto_bluetooth),
                ui.UiMenuItem(name=_("&trash"), action=self._exec_goto_trash),
                ui.UiMenuItem(name=_("my back&ups"), action=self._exec_goto_backup),
                ui.UiMenuItem(name=_("c&rash"), action=self._exec_goto_crash),
                ui.UiMenuItem(
                    name=_("p&arent directory"),
                    action=self._exec_goto_parent_directory,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE,
                ),
            ],
        )

    def __create_file_manager_tools_menu(self):
        return ui.UiMenuBar(
            name=_("back&up"),
            menu_item_list=[
                ui.UiMenuItem(name=_("back&up"), action=self._exec_backup),
                ui.UiMenuItem(name=_("&restore"), action=self._exec_restore),
            ],
        )

    def __create_trash_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&restore from trash"), action=self._exec_restore_from_trash
                ),
                ui.UiMenuItem(name=_("permanently &delete"), action=self._exec_delete),
                ui.UiMenuItem(
                    name=_("&empty the trash"), action=self._exec_empty_the_trash
                ),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    def __create_trash_edit_menu(self):
        return ui.UiMenuBar(
            name=_("&edit"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("start &selection"),
                    action=self._exec_start_selection,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F8,
                ),
                ui.UiMenuItem(
                    name=_("end &selection"),
                    action=self._exec_end_selection,
                    is_hide=True,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE,
                ),
                ui.UiMenuItem(
                    name=_("select &all"),
                    action=self._exec_select_all,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="A",
                ),
            ],
        )

    def __create_bluetooth_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("dele&te"),
                    action=self._exec_delete,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                ),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    def __create_bluetooth_edit_menu(self):
        return ui.UiMenuBar(
            name=_("&edit"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("start &selection"),
                    action=self._exec_start_selection,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F8,
                ),
                ui.UiMenuItem(
                    name=_("end &selection"),
                    action=self._exec_end_selection,
                    is_hide=True,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE,
                ),
                ui.UiMenuItem(
                    name=_("cu&t"),
                    action=self._exec_cut,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="X",
                ),
                ui.UiMenuItem(
                    name=_("select &all"),
                    action=self._exec_select_all,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="A",
                ),
            ],
        )

    def __create_usb_flash_drive_list_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("safely &unmount usb stick"),
                    action=self._exec_unmount_all_usb_flash_drives,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="U",
                ),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    # C'est le menu fichier quand la liste des clef usb est vide => il n'y a pas 'éjecter' mais seulement 'actualiser'.
    def __create_usb_flash_drive_empty_list_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    def __create_usb_flash_drive_file_menu(self):
        return ui.UiMenuBar(
            name=_("&file"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("safely &unmount usb stick"),
                    action=self._exec_unmount_all_usb_flash_drives,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key="U",
                ),
                self.__create_file_manager_file_new_menu(),
                ui.UiMenuItem(
                    name=_("&open"),
                    action=self._exec_open,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(
                    name=_("&open to read"),
                    action=self._exec_read_only,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(name=_("&send to"), action=self._exec_send_to),
                ui.UiMenuItem(
                    name=_("&rename"),
                    action=self._exec_rename,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                ),
                ui.UiMenuItem(
                    name=_("dele&te"),
                    action=self._exec_delete,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                ),
                ui.UiMenuItem(name=_("&zip"), action=self._exec_zip),
                ui.UiMenuItem(name=_("&unzip"), action=self._exec_unzip),
                ui.UiMenuItem(
                    name=_("&actualize"),
                    action=self._exec_actualize,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F5,
                ),
            ],
        )

    def __create_menu(self):
        # Build the regulars menus
        self._file_manager_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_file_manager_file_menu(),
                self.__create_file_manager_edit_menu(),
                self.__create_file_manager_eole_menu(),
                self.__create_file_manager_goto_menu(),
                self.__create_file_manager_tools_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        self._file_manager__with_usb_flash_drive_plugged_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_file_manager_with_usb_flash_drive_plugged_file_menu(),
                self.__create_file_manager_edit_menu(),
                self.__create_file_manager_eole_menu(),
                self.__create_file_manager_goto_menu(),
                self.__create_file_manager_tools_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        # 2024 : Build the menu for the new MAIN folder.
        self._file_manager_main_emplacement_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_file_manager_goto_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        # Build trash menu
        self._trash_main_menu = ui.UiMenuBar(
            name=_("trash"),
            is_root=True,
            menu_item_list=[
                self.__create_trash_file_menu(),
                self.__create_trash_edit_menu(),
                self.__create_file_manager_goto_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        # Build bluetooth menu

        self._bluetooth_main_menu = ui.UiMenuBar(
            name=_("bluetooth"),
            is_root=True,
            menu_item_list=[
                self.__create_bluetooth_file_menu(),
                self.__create_bluetooth_edit_menu(),
                self.__create_file_manager_goto_menu(),
                self.__create_file_manager_tools_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        # Build the USB flash drive menus (displayed inside a mounted usb flash drive)
        self._usb_flash_drive_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_usb_flash_drive_file_menu(),
                self.__create_file_manager_edit_menu(),
                self.__create_file_manager_goto_menu(),
                self.__create_file_manager_tools_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )
        # Build the USB flash drive menus (displayed inside the usb flash drive list with a mounted usb flash drive)
        self._usb_flash_drive_list_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_usb_flash_drive_list_file_menu(),
                self.__create_file_manager_goto_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )
        # Build the USB flash drive menus (displayed inside the usb flash drive list without a mounted usb flash drive)
        # Menus to use in flash drive folder when no usb flash drive is mounted.
        self._usb_flash_drive_empty_list_main_menu = ui.UiMenuBar(
            name=_("explorer"),
            is_root=True,
            menu_item_list=[
                self.__create_usb_flash_drive_empty_list_file_menu(),
                self.__create_file_manager_goto_menu(),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

        # Default menu for file manager with or without usb key plugged
        if len(FileManagerApp.__list_dir(FileManager.get_usb_flash_drive_path())):
            BnoteApp.set_menu(
                self, self._file_manager__with_usb_flash_drive_plugged_main_menu
            )
        else:
            BnoteApp.set_menu(self, self._file_manager_main_menu)

        # If a crash report file does not exist, hide the goto crash menu item.
        if not len(FileManager.listdir(FileManager.get_crash_path())):
            self._menu.get_object(self._exec_goto_crash).hide()

    def __reset_extend_selection(self):
        self.__extend_selection = False
        # usefull to have shortcut F8, Esc operational or not.
        self._update_menu_items()
        # Reset quick search parameters.
        self.__quick_search.clear()

    def __set_extend_selection(self):
        self.__extend_selection = True
        # usefull to have shortcut F8, Esc operational or not.
        self._update_menu_items()
        # Reset quick search parameters.
        self.__quick_search.clear()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        # Actualize menu according selection mode.
        start_selection_menu = self._menu.get_object(self._exec_start_selection)
        end_selection_menu = self._menu.get_object(self._exec_end_selection)
        if start_selection_menu and end_selection_menu:
            if self.__extend_selection:
                start_selection_menu.hide()
                end_selection_menu.unhide()
            else:
                start_selection_menu.unhide()
                end_selection_menu.hide()
        # Actualize paste function visibility.
        menu_paste = self._menu.get_object(self._exec_paste)
        if menu_paste:
            if self.__copy_cut_paste_files:
                menu_paste.unhide()
            else:
                menu_paste.hide()
        # Actualize menu open file
        menu_read_only = self._menu.get_object(self._exec_read_only)
        # if file can be open by editor, unhide read_only menu item.
        if menu_read_only is not None:
            if self.is_focused_file_is_editor_file():
                menu_read_only.unhide()
            else:
                menu_read_only.hide()

    def is_focused_file_is_editor_file(self):
        res = False
        # if invalid file returns false
        if self.__selected_files is not None and self.__files is not None:
            # If multiple selection returns false.
            if len(self.__selected_files) <= 1:
                focused_file = self.__files[self.__focused_file_index]
                # if not a file but a folder returns false
                if focused_file.is_file:
                    (shortname, extension) = self.split_filename_and_extension(
                        focused_file
                    )
                    if extension:
                        extension = extension.lower()
                        # if extension is not a editor file extension returns False
                        # (for music files returns false)
                        if extension in EditorApp.known_extension():
                            res = True
        return res

    def get_current_file(self):
        if self.__files[self.__focused_file_index].exists():
            return self.__files[self.__focused_file_index]

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each app if necessary.
        """
        self.refresh_current_item(True)

    """
    Menu execution
    """

    # File menu
    # Ancien code qui demontait seulement le dossier courant (il fallait faire l'opération autant de fois qu'il y avait
    # de volume monté)
    # def _exec_unmount_usb(self):
    #     current_file = self.get_current_file()
    #     if current_file:
    #         # Unmount usb key successfully.
    #         if FileManager.umount_safely_usb_flash_drive(current_file):
    #             self._current_dialog = ui.UiInfoDialogBox(
    #                 message=_("you can now unplug safely the usb flash disk."),
    #                 action=self._exec_goto_usb_drives
    #             )
    #             return
    #
    #     self._current_dialog = ui.UiInfoDialogBox(
    #         message=_("unable to unplug safely the usb flash disk."),
    #         action=self._exec_cancel_dialog
    #     )

    def _exec_unmount_all_usb_flash_drives(self):
        success = True
        usb_drive_list = FileManagerApp.__list_dir(
            FileManager.get_usb_flash_drive_path()
        )
        for current_file in usb_drive_list:
            # Unmount usb key successfully.
            if not FileManager.umount_safely_usb_flash_drive(current_file):
                success = False

        if success:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("you can now unplug safely the usb flash disk."),
                action=self._exec_goto_usb_drives,
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("unable to unplug safely the usb flash disk."),
                action=self._exec_cancel_dialog,
            )

    def _exec_new_bxml_file(self, **kwargs):
        self._exec_new_file(type=_(".bxml"))

    def _exec_new_text_file(self, **kwargs):
        self._exec_new_file(**{"type": _(".txt")})

    def _exec_new_musicxml_file(self, **kwargs):
        self._exec_new_file(**{"type": _(".musicxml")})

    def _exec_new_ai_assistant_file(self, **kwargs):
        self._exec_new_file(**{"type": _(".ai_txt")})

    def _exec_new_file(self, **kwargs):
        """
        Display the new file dialogBox
        :param kwargs:
            "filename" optional, if exist it is the filename displayed in dialog.
        :return: None
        """
        log.info("new_file in file manager")
        # Operation not allowed for Bluetooth or backup folder
        if str(self.__current_folder).startswith(
            str(FileManager.get_backup_path())
        ) or str(self.__current_folder).startswith(
            str(FileManager.get_bluetooth_path())
        ):
            self.__operation_not_allowed()
            return

        typename = kwargs["type"]
        filename = "".join([_("new file"), typename])
        extra_parameters = {"type": typename}
        if "filename" in kwargs:
            filename = kwargs["filename"]

        self._current_dialog = ui.UiDialogBox(
            name=_("new file"),
            item_list=[
                ui.UiFileEditBox(name=_("&name"), value=("filename", filename)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_new_file_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
            extra_parameters=extra_parameters,
        )

    def _exec_new_folder(self, **kwargs):
        """
        Display the new folder dialogBox
        :param kwargs:
            "folder_name" optional, if exist it is the folder nameilename displayed in dialog.
        :return: None
        """
        # Operation not allowed for Bluetooth or backup folder
        if str(self.__current_folder).startswith(
            str(FileManager.get_backup_path())
        ) or str(self.__current_folder).startswith(
            str(FileManager.get_bluetooth_path())
        ):
            self.__operation_not_allowed()
            return

        folder_name = _("new folder")
        if "folder_name" in kwargs:
            folder_name = kwargs["folder_name"]

        self._current_dialog = ui.UiDialogBox(
            name=_("new directory"),
            item_list=[
                ui.UiFileEditBox(name=_("&name"), value=("folder_name", folder_name)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_new_folder_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_open(self):
        log.info("_exec_open")
        self.__activate_child()

    def _exec_read_only(self):
        log.info("_exec_read_only")
        self.__activate_child(read_only=True)

    def _exec_send_to(self):
        # log.info("before get_paired_device")
        # paired_devices = bt_util.get_paired_devices()
        # log.info("after get_paired_device")

        # Get the paired_devices
        self.__paired_devices = bt_util.get_paired_devices()

        log.info("self.__paired_devices={}".format(self.__paired_devices))
        computers = []
        for key, value in self.__paired_devices.items():
            computers.append(value)

        log.info("computers={}".format(computers))

        if len(computers):
            self._current_dialog = ui.UiDialogBox(
                name=_("send to"),
                item_list=[
                    ui.UiListBox(name=_("co&mputer"), value=("computer", computers)),
                    ui.UiButton(name=_("&ok"), action=self._exec_valid_send_to_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("no bluetooth computer visible...")),
                action=self._exec_cancel_dialog,
            )
        return

    def _exec_rename(self, **kwargs):
        rename_name = self.__files[self.__focused_file_index]

        rename_name_value = rename_name.name
        if "rename_name" in kwargs:
            rename_name_value = kwargs["rename_name"]
        self._current_dialog = ui.UiDialogBox(
            name=_("rename"),
            item_list=[
                ui.UiFileEditBox(
                    name=_("&name"), value=("rename_name", rename_name_value)
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_rename_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_delete(self):
        if str(self.__current_folder).startswith(str(Trash.get_trash_path())):
            log.info("_exec_delete")
            # If no files selected do nothing...
            if len(self.__selected_files) == 0:
                return
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("delete"),
                message=_(
                    "do you confirm permanently deletion? if you delete, it will be permanently lost."
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"), action=self._exec_permanent_deletion_yes_dialog
                    ),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            self.__delete_files()

    def _exec_permanent_deletion_yes_dialog(self):
        self.__delete_files()

    def __delete_files(self):
        delete_files = []
        for file in self.__selected_files:
            delete_files.append(file)

        log.info("delete_files={}".format(delete_files))
        if len(delete_files):
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("deleting {}% {}").format("   ", "")
            )
            self.__delete_thread = DeleteThread(
                delete_files, on_progress=self.__on_progress, on_end=self.__end_delete
            )
            self.__delete_thread.start()

    def _exec_restore_from_trash(self):
        if str(self.__current_folder).startswith(str(Trash.get_trash_path())):
            __restore_from_trash_files = []
            for file in self.__selected_files:
                __restore_from_trash_files.append(file)
            # Reset extend selection (as if user has pressed ESC)
            self.__extend_selection = False

            self._current_dialog = ui.UiInfoDialogBox(
                message=_("restoring {}% {}").format("   ", "")
            )
            self.__restore_from_trash_thread = RestoreFromTrashThread(
                __restore_from_trash_files,
                None,
                self.__on_ask_replace,
                self.__on_progress,
                self.__end_restore_from_trash,
            )
            self.__restore_from_trash_thread.start()

    def __end_restore_from_trash(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.END_RESTORE_FROM_TRASH, *args, **kwargs)

    def _exec_empty_the_trash(self):
        if str(self.__current_folder).startswith(str(Trash.get_trash_path())):
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("delete"),
                message=_(
                    "do you want to empty the trash? all files will be permanently lost."
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"), action=self._exec_empty_the_trash_yes_dialog
                    ),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_empty_the_trash_yes_dialog(self):
        Trash.empty_the_trash()
        # Close current dialog box.
        self._current_dialog = None
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_zip(self, **kwargs):
        # Operation not allowed for bluetooth or backup folder
        if str(self.__current_folder).startswith(
            str(FileManager.get_backup_path())
        ) or str(self.__current_folder).startswith(
            str(FileManager.get_bluetooth_path())
        ):
            self.__operation_not_allowed()
            return
        # Construct zip file name
        if len(self.__selected_files) != 0:
            zip_name = self.__selected_files[0].resolve().name + ".zip"
            if "zip_name" in kwargs:
                zip_name = kwargs["zip_name"]
            self._current_dialog = ui.UiDialogBox(
                name=_("zip"),
                action_cancelable=self._exec_cancel_dialog,
                item_list=[
                    ui.UiFileEditBox(name=_("&name"), value=("zip_file", zip_name)),
                    ui.UiButton(name=_("&ok"), action=self._exec_zip_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
            )

    def _exec_unzip(self, **kwargs):
        # Operation not allowed for Bluetooth or backup folder
        if str(self.__current_folder).startswith(
            str(FileManager.get_backup_path())
        ) or str(self.__current_folder).startswith(
            str(FileManager.get_bluetooth_path())
        ):
            self.__operation_not_allowed()
            return

        if len(self.__selected_files) == 1:
            path, extension = os.path.splitext(self.__selected_files[0])
            log.info("path={} extension={}".format(path, extension))
            if self.__selected_files[0].suffix == ".zip":
                unzip_filename = self.__selected_files[0]
                unzip_to_folder = FileManager.create_generic_filename(
                    unzip_filename.parent / unzip_filename.stem, _("({})")
                )
                log.info("path={} unzip_to_folder={}".format(path, unzip_to_folder))
                if unzip_to_folder is None:
                    # FIXME : si plus de 99 dossiers génériques prévenir l'utilisateur
                    return
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("extracting {}% {}").format("   ", "")
                )
                # Create a folder with the archive name.
                if not unzip_to_folder.exists():
                    unzip_to_folder.mkdir()
                self.__unzip_thread = UnZipThread(
                    unzip_filename,
                    unzip_to_folder,
                    on_progress=self.__on_progress,
                    on_ask_replace=self.__on_ask_replace,
                    on_end=self.__end_unzip,
                )
                self.__unzip_thread.start()
        # Reset extend selection (as if user has pressed ESC)
        self.__reset_extend_selection()

    def _exec_find_file(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("find file"),
            item_list=[
                ui.UiFileEditBox(name=_("&file name"), value=("name", "")),
                ui.UiListBox(
                    name=_("find &in"),
                    value=("find", [_("current folder"), _("in the b.note")]),
                    current_index=0,
                ),
                ui.UiButton(name=_("fi&nd"), action=self._exec_valid_find_file),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_find_file(self):
        kwargs = self._current_dialog.get_values()
        if kwargs["find"] == _("current folder"):
            files_list = self._exec_find_in_folders(
                self.__current_folder, kwargs["name"]
            )
        else:
            files_list = {}
            # On parcour chaque dossier indépendemment
            backup = self._exec_find_in_folders(
                FileManager.get_backup_path(), kwargs["name"]
            )
            if backup:
                files_list.update(backup)
            bluetooth = self._exec_find_in_folders(
                FileManager.get_bluetooth_path(), kwargs["name"]
            )
            if bluetooth:
                files_list.update(bluetooth)
            crash = self._exec_find_in_folders(
                FileManager.get_crash_path(), kwargs["name"]
            )
            if crash:
                files_list.update(crash)
            documents = self._exec_find_in_folders(
                FileManager.get_documents_path(), kwargs["name"]
            )
            if documents:
                files_list.update(documents)
            usb = self._exec_find_in_folders(
                FileManager.get_usb_flash_drive_path(), kwargs["name"]
            )
            if usb:
                files_list.update(usb)
        if files_list:
            # On récupère les noms de fichier
            lst = []
            for element in files_list.keys():
                lst.append(element)
            self._current_dialog = ui.UiDialogBox(
                name=_("file found {}").format(len(lst)),
                item_list=[
                    ui.UiListBox(name=_("file"), value=("list", lst)),
                    ui.UiButton(
                        name=_("&show in folder"),
                        action=self._exec_show_in_folder,
                        action_param={"folder": files_list},
                    ),
                    ui.UiButton(
                        name=_("&open file"),
                        action=self._exec_show_in_folder,
                        action_param={"folder": files_list, "open": True},
                    ),
                    ui.UiButton(name=_("&close"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("no file found"), action=self._exec_cancel_dialog
            )

    def _exec_find_in_folders(self, arb, text_to_find):
        list_file = FileManagerApp.__list_dir(arb)
        text_to_find = text_to_find.lower()
        file_lst = {}
        for file in list_file:
            if file.is_file():
                if file.name.lower().find(text_to_find) >= 0:
                    file_lst[file.name] = file
            else:
                path = self._exec_find_in_folders(file, text_to_find)
                if path:
                    file_lst.update(path)
        if file_lst:
            return file_lst
        return False

    def _exec_properties(self):
        if not os.listdir(self.__current_folder) or self.__selected_files:
            return
        focused_file = self.__files[self.__focused_file_index]
        properties = focused_file.stat()

        # Calcul de la taille en Mo, Go
        size_bytes = properties.st_size
        if size_bytes < 1024:
            size_formatted = "".join((f"{size_bytes} ", _("bytes")))
        elif size_bytes < 1024**2:
            size_formatted = "".join((f"{size_bytes / 1024:.2f} ", _("Kb")))
        elif size_bytes < 1024**3:
            size_formatted = "".join((f"{size_bytes / 1024 ** 2:.2f} ", _("Mb")))
        else:
            size_formatted = "".join((f"{size_bytes / 1024 ** 3:.2f} ", _("Gb")))

        # Determined type
        extension = ""
        if focused_file.is_dir():
            item_type = _("folder")
        else:
            extension = focused_file.suffix
            if extension in EditorApp.known_extension():
                item_type = _("editor file")
            elif extension in Mp3App.known_extension():
                item_type = _("audio file")
            elif extension in MusicApp.known_extension():
                item_type = _("music file")
            else:
                item_type = _("file not suported")

        properties_infos = {
            "name": focused_file.name,
            "type": item_type if focused_file.is_dir() else f"{item_type} {extension}",
            "size": size_formatted,
            "last_modification": datetime.datetime.fromtimestamp(properties.st_mtime),
            "creation_date": datetime.datetime.fromtimestamp(properties.st_ctime),
        }
        translation = {
            "name": _("name"),
            "type": _("type"),
            "size": _("size"),
            "last_modification": _("last modification"),
            "creation_date": _("creation date"),
            "child_number": _("child"),
        }
        # Add child number if it's a folder
        if focused_file.is_dir():
            properties_infos["child_number"] = len(
                FileManagerApp.__list_dir(focused_file)
            )

        properties_documens = ""
        for item in properties_infos:
            properties_documens += f"{translation[item]}: {properties_infos[item]}\n"
        # Retirer le dernier \n du document
        properties_documens = properties_documens[:-1]
        self._current_dialog = ui.UiDialogBox(
            name=_("properties"),
            item_list=[
                ui.UiMultiLinesBox(
                    name=_("Click to show properties"),
                    value=("properties", properties_documens),
                    no_grade=True,
                    is_read_only=True,
                ),
                ui.UiButton(name=_("&close"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_show_in_folder(self, folder, open=False):
        kwargs = self._current_dialog.get_values()
        # Goto the folder
        self.__init_new_current_folder_and_build_braille_line(folder[kwargs["list"]])
        self._exec_activate_parent()
        self.__quick_search_move_call_back(kwargs["list"])
        if open:
            self._exec_activate_child()

    def _exec_actualize(self):
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_recent_file(self):
        lst = RecentFile().send_list()
        if not lst:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("not recent file"), action=self._exec_cancel_dialog
            )
            return False
        name_files = []
        for name in lst:
            name_files.append(name[0])
        self._current_dialog = ui.UiDialogBox(
            name=_("recent files"),
            item_list=[
                ui.UiListBox(
                    name=_("file list"), value=("file", name_files), current_index=0
                ),
                ui.UiButton(
                    name=_("&open"),
                    action=self._exec_open_recent_file,
                    action_param={"lst": lst},
                ),
                ui.UiButton(name=_("c&lear list"), action=RecentFile().delete_all),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_open_recent_file(self, lst):
        kwargs = self._current_dialog.get_values()
        for element in lst:
            if element[0] == kwargs["file"]:
                if not Path.exists(Path(element[2])):
                    self._current_dialog = ui.UiInfoDialogBox(
                        message=_(
                            "this file does not exist, it will be removed from the list."
                        ),
                        action=RecentFile().delete_file,
                        action_param={"name": kwargs["file"]},
                    )
                    return False
                self.__init_new_current_folder_and_build_braille_line(Path(element[2]))
                self._exec_activate_parent()
                self.__quick_search_move_call_back(kwargs["file"])
                extention = ".{}".format(kwargs["file"].split(".")[-1])
                print(
                    "mon extention: {}, supportées: {}".format(
                        extention, EditorApp.known_extension()
                    )
                )
                if extention in EditorApp.known_extension():
                    return self._exec_ask_open_editor_recent_file()
                return self._exec_activate_child()

    def _exec_ask_open_editor_recent_file(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("open"),
            item_list=[
                ui.UiCheckBox(name=_("&read only"), value=("mode", False)),
                ui.UiButton(
                    name=_("&open"), action=self._exec_valid_open_editor_recent_file
                ),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_open_editor_recent_file(self):
        kwargs = self._current_dialog.get_values()
        self.__activate_child(read_only=kwargs["mode"])

    def _exec_eole_simplified_search(self):
        self.__is_eole_simplified_search = True
        self._exec_eole_search()

    def _exec_eole_advanced_search(self):
        self.__is_eole_simplified_search = False
        self._exec_eole_search()

    def _exec_eole_search(self, ignore_token_validity=False):
        has_valid_token = False

        # If an access token exists used it.
        if (
            Settings().data["eole"]["token"] != ""
            and Settings().data["eole"]["user_name"] != ""
        ):
            if (
                EoleCrypto(Settings().data["eole"]["user_name"]).decrypt(
                    Settings().data["eole"]["token"]
                )
                != ""
            ):
                EoleApi().set_access_token(
                    EoleCrypto(Settings().data["eole"]["user_name"]).decrypt(
                        Settings().data["eole"]["token"]
                    )
                )
                has_valid_token = EoleApi().has_valid_token_access()

        # If access token is valid or ignore_token_validity, open the search dialog.
        if has_valid_token or ignore_token_validity:
            self._current_dialog = EoleSearchDialogBox(
                self.__is_eole_simplified_search,
                self._exec_summary_dialog,
                self._exec_want_to_download,
                self._exec_display_error_dialog,
                self._exec_cancel_dialog,
            )
        else:
            # Else ask user login / password (it will grab and save the access_token)
            self._exec_eole_login_dialog()

    def _exec_eole_login_dialog(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("eole"),
            action_cancelable=self._exec_cancel_dialog,
            item_list=[
                ui.UiEditBox(
                    name=_("login"),
                    value=("login", Settings().data["eole"]["user_name"]),
                ),
                ui.UiEditBox(name=_("password"), value=("password", "")),
                ui.UiButton(name=_("&ok"), action=self._exec_eole_grab_token),
                ui.UiButton(
                    name=_("&cancel"),
                    action=self._exec_eole_search_without_access_token_check,
                ),
            ],
        )

    def _exec_eole_grab_token(self):
        if self._current_dialog:
            # get parameters
            kwargs = self._current_dialog.get_values()
            user_name, password = "", ""
            if "login" in kwargs:
                user_name = kwargs["login"]
            if "password" in kwargs:
                password = kwargs["password"]

            success, error_success_message = (
                EoleApi().init_access_token_from_user_password(user_name, password)
            )
            if success:
                Settings().data["eole"]["user_name"] = user_name
                Settings().data["eole"]["token"] = EoleCrypto(user_name).encrypt(
                    EoleApi().access_token()
                )
                Settings().save()
                # Open the search dialog
                self._exec_eole_search()
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )
            else:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("unable to grab access token. error : {}").format(
                        error_success_message
                    ),
                    action=self._exec_eole_login_dialog,
                )
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )

    def _exec_eole_search_without_access_token_check(self):
        self._exec_eole_search(ignore_token_validity=True)

    def _exec_want_to_download(self):
        url_name, filename = None, None
        # First get the url and filename that user have selected.
        if isinstance(self._current_dialog, EoleSearchDialogBox):
            url_name, filename = self._current_dialog.get_download_info()
        # print(f"{url_name=}")
        # print(f"{filename=}")
        if url_name and filename:
            self.__exec_eole_do_prepare_download(
                **{
                    "url_name": url_name,
                    "filename": self.__current_folder / filename,
                    "no_test_existing": False,
                }
            )

    def __exec_eole_do_prepare_download(self, **kwargs):
        test_existing = True
        if "no_test_existing" in kwargs.keys() and kwargs["no_test_existing"]:
            test_existing = False

        if (
            "url_name" in kwargs
            and kwargs["url_name"]
            and "filename" in kwargs
            and kwargs["filename"]
        ):
            url_name = kwargs["url_name"]
            filename = kwargs["filename"]

            if test_existing and filename.exists():
                ui_filename = ui.UiFileManagerLine.friendly_file_name(filename)
                self.__eole_search__current_dialog = self._current_dialog
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("question"),
                    message=_("{} already exists. do you want to replace it?").format(
                        ui_filename
                    ),
                    buttons=[
                        ui.UiButton(
                            name=_("&yes"),
                            action=self.__exec_eole_do_prepare_download,
                            action_param={
                                "url_name": url_name,
                                "filename": filename,
                                "no_test_existing": True,
                            },
                        ),
                        ui.UiButton(
                            name=_("&no"),
                            action=self._exec_end_of_eole_information_dialog,
                        ),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )
                return

            self.__eole_search__current_dialog = self._current_dialog
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("download in progress...")
            )
            # Ask a refresh when self._current_dialog is changed.
            self._put_in_function_queue(
                FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
            )

            # Call self.__eole_download_thread_function in a thread.
            x = threading.Thread(
                target=self.__eole_download_thread_function,
                args=(url_name, filename, self.__eole_end_of_download),
            )
            x.start()

    @staticmethod
    def __eole_download_thread_function(url_name, filename, on_end=None):
        success = False
        error_message = _("unknown error")

        try:
            success, error_message = EoleApi().download(url_name, filename)

        except Exception as e:
            success = False
            error_message = str(e)
        finally:
            if on_end is not None:
                on_end(
                    **{
                        "success": success,
                        "error_message": error_message,
                        "filename": filename,
                    }
                )

    def __eole_end_of_download(self, *args, **kwargs):
        self._put_in_function_queue(
            FunctionId.FUNCTION_END_EOLE_DOWNLOAD, *args, **kwargs
        )

    def __end_eole_download_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs and "filename" in kwargs and "error_message" in kwargs:
            if kwargs["success"]:
                # Close the dialog box
                self._current_dialog = None
                self.__eole_search__current_dialog = None
                # Refresh the current folder and focus on the downloaded filename
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=kwargs["filename"]
                )
            else:
                error_message = _("error can't download the file. error is {}.").format(
                    kwargs["error_message"]
                )
                if kwargs["error_message"] == EoleApi().access_token():
                    error_message = _(
                        "unable to download the book, your access token is invalid, check your login password."
                    )

                self._current_dialog = ui.UiInfoDialogBox(
                    message=error_message,
                    action=self._exec_end_of_eole_information_dialog,
                )
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )
        return True

    def __refresh_dialog_in_dialog(self, *args, **kwargs) -> bool:
        self.refresh_app()
        return True

    def _exec_summary_dialog(self):
        if isinstance(self._current_dialog, EoleSearchDialogBox):
            summary = self._current_dialog.get_summary()
            if summary is not None:
                # The summary is displayed only if there is a valid result.
                self.__eole_search__current_dialog = self._current_dialog
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("summary"),
                    buttons=[
                        ui.UiButton(
                            name=_("&ok"),
                            action=self._exec_end_of_eole_information_dialog,
                        )
                    ],
                    message=summary,
                    action_cancelable=self._exec_end_of_eole_information_dialog,
                )
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )

    def _exec_display_error_dialog(self, error_message=None):
        if isinstance(self._current_dialog, EoleSearchDialogBox):
            if error_message is not None:
                # The error_message is displayed only if there is a valid error_message.
                self.__eole_search__current_dialog = self._current_dialog
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("error"),
                    buttons=[
                        ui.UiButton(
                            name=_("&ok"),
                            action=self._exec_end_of_eole_information_dialog,
                        )
                    ],
                    message=error_message,
                    action_cancelable=self._exec_end_of_eole_information_dialog,
                )
                # Ask a refresh when self._current_dialog is changed.
                self._put_in_function_queue(
                    FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG
                )

    def _exec_end_of_eole_information_dialog(self):
        # print(f"_exec_end_of_eole_information_dialog")
        self._current_dialog = self.__eole_search__current_dialog
        self.__eole_search__current_dialog = None
        # Ask a refresh when self._current_dialog is changed.
        self._put_in_function_queue(FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG)

    # Edition menu
    def _exec_start_selection(self):
        log.info("--- _exec_start_selection")
        self.__set_extend_selection()
        # Add the current file in the selection.
        self.__update_selected_files()
        # The current file/folder has changed of presentation.
        self.__build_braille_line()

    def _exec_end_selection(self):
        log.info("--- _exec_end_selection")
        self.__reset_extend_selection()
        # The current file/folder has changed of presentation.
        self.__build_braille_line()

    def _exec_cut(self):
        self.__copy_cut_paste_files = []
        for file in self.__selected_files:
            self.__copy_cut_paste_files.append(file)
        self.__is_copy = False
        self.__is_cut = True
        # Reset extend selection (as if user has pressed ESC)
        self.__reset_extend_selection()
        return

    def _exec_copy(self):
        self.__copy_cut_paste_files = []
        for file in self.__selected_files:
            self.__copy_cut_paste_files.append(file)
        self.__is_copy = True
        self.__is_cut = False
        # Reset extend selection (as if user has pressed ESC)
        self.__reset_extend_selection()
        log.info("self.__selected_files={}".format(self.__selected_files))
        log.info("self.__copy_cut_paste_files={}".format(self.__copy_cut_paste_files))
        return

    def _exec_paste(self):
        if self.__copy_cut_paste_files is not None:
            if self.__is_cut:
                if self.__is_open_in_editor(self.__copy_cut_paste_files):
                    # Error message
                    self._current_dialog = ui.UiInfoDialogBox(
                        message=(_("unable to move the opened file in the editor.")),
                        action=self._exec_cancel_dialog,
                    )
                    return

            if str(self.__current_folder).startswith(
                str(FileManager.get_backup_path())
            ):
                paste_ok = True
                for file in self.__copy_cut_paste_files:
                    file_name, file_extension = os.path.splitext(file)
                    if file_extension != ".zip":
                        paste_ok = False
                        break
                if not paste_ok:
                    # Operation not allowed in backup folder if no zip file.
                    # DP FIXME Il suffit de sélectionner un zip dans la liste des fichiers à copier pour que cela soit ok ?
                    self.__operation_not_allowed()
                    return

            if str(self.__current_folder).startswith(
                str(FileManager.get_bluetooth_path())
            ):
                # Operation not allowed in bluetooth folder.
                self.__operation_not_allowed()
                return

            if self.__is_cut:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("moving {}% {}").format("   ", "")
                )
                self.__copy_move_thread = CopyMoveThread(
                    self.__copy_cut_paste_files,
                    self.__current_folder,
                    False,
                    None,
                    self.__on_ask_replace,
                    self.__on_progress,
                    self.__end_paste,
                )
                self.__copy_move_thread.start()
            elif self.__is_copy:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("copying {}% {}").format("   ", "")
                )
                self.__copy_move_thread = CopyMoveThread(
                    self.__copy_cut_paste_files,
                    self.__current_folder,
                    True,
                    None,
                    self.__on_ask_replace,
                    self.__on_progress,
                    self.__end_paste,
                )
                self.__copy_move_thread.start()

    def __end_paste(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_PASTE, *args, **kwargs)

    def __end_paste_dlg(self, *args, **kwargs) -> bool:
        sync_file_name = None
        if len(self.__copy_cut_paste_files):
            sync_file_name = self.__current_folder / Path(
                self.__copy_cut_paste_files[0].name
            )
        if self.__is_cut:
            # File(s) can be cut and past only 1 time (because after past operation, it disappears from origin).
            self.__copy_cut_paste_files = None
            self.__is_cut = False
        # Close current dialog box.
        self._current_dialog = None
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(
            self.__current_folder, focused_file=sync_file_name
        )
        return True

    def _exec_select_all(self):
        self.__selected_files = []
        for file in self.__files:
            # Do not append simlink used for Bluetooth and backup
            if file.exists() and not file.is_symlink():
                self.__selected_files.append(file)
        log.info("selected_files={}".format(self.__selected_files))
        if len(self.__selected_files):
            self.__set_extend_selection()
        # Refresh the braille display to update the current presented item
        self.__build_braille_line()

    # Goto menu
    def _exec_goto_bluetooth(self):
        log.info("_exec_goto_bluetooth in file manager")
        # change current folder.
        self.__current_folder = FileManager.get_bluetooth_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_trash(self):
        # change current folder.
        self.__current_folder = Trash.get_trash_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_backup(self):
        # change current folder.
        self.__current_folder = FileManager.get_backup_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_crash(self):
        # change current folder.
        self.__current_folder = FileManager.get_crash_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_my_documents(self):
        # change current folder.
        self.__current_folder = FileManager.get_documents_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_usb_drives(self):
        # change current folder.
        self.__current_folder = FileManager.get_usb_flash_drive_path()
        # Refresh the current folder
        self.__init_new_current_folder_and_build_braille_line(self.__current_folder)

    def _exec_goto_parent_directory(self):
        self.__activate_parent()

    #
    def _exec_backup(self, **kwargs):
        d = datetime.datetime.now()
        zip_name = d.strftime(_("backup %Y %m %d.zip"))
        if "zip_name" in kwargs:
            zip_name = kwargs["zip_name"]
        self._current_dialog = ui.UiDialogBox(
            name=_("backup"),
            action_cancelable=self._exec_cancel_dialog,
            item_list=[
                ui.UiFileEditBox(name=_("&name"), value=("backup_file", zip_name)),
                ui.UiButton(name=_("&ok"), action=self._exec_backup_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
        )

    def _exec_restore(self):
        backup_files = FileManager.listdir(FileManager.get_backup_path())
        if len(backup_files) == 0:
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("no backup files to restore !")),
                action=self._exec_cancel_dialog,
            )
        else:
            self._current_dialog = ui.UiDialogBox(
                name=_("restore"),
                action_cancelable=self._exec_cancel_dialog,
                item_list=[
                    ui.UiFileNameListBox(
                        name=_("&name"), value=("backup_file", backup_files)
                    ),
                    ui.UiButton(name=_("&ok"), action=self._exec_restore_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
            )

    def _exec_application(self):
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    """
    DIALOG CALLBACKS
    """

    def _exec_valid_new_file_dialog(self):
        log.info("callback:_exec_valid_new_file_dialog")
        kwargs = self._current_dialog.get_values()
        self.__new_file(**kwargs)

    def __new_file(self, **kwargs):
        """
        Create a new file.
        :param kwargs:
            filename = filename to create.
            type = the type of the file.
            no_test_existing = if true, do not ask to replace existing file.
        :return: None
        """
        log.info(f"{kwargs=}")
        filename = kwargs["filename"]
        test_existing = True
        if "no_test_existing" in kwargs.keys() and kwargs["no_test_existing"]:
            test_existing = False
        # # https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
        # Reject an empty filename
        if not filename or filename.startswith("."):
            # Return to the dialog box new file.
            self._exec_new_file(filename=filename, type=kwargs["type"])
            return
        # Append .txt extension if missing.
        path, extension = os.path.splitext(filename)
        log.info("path={} extension={}".format(path, extension))
        if extension != kwargs["type"]:
            filename += kwargs["type"]
        # Check if invalids characters.
        if not FileManager.is_valid_filename(filename):
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("the following characters are invalid ") + '<>"/\\|?*'),
                action=self._exec_new_file,
                action_param={"type": kwargs["type"], "filename": filename},
            )
            return
        if test_existing and (self.__current_folder / filename).exists():
            ui_filename = ui.UiFileManagerLine.friendly_file_name(filename)
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("question"),
                message=_("file {} exists. do you want to replace it?").format(
                    ui_filename
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"),
                        action=self.__new_file,
                        action_param={
                            "filename": filename,
                            "type": kwargs["type"],
                            "no_test_existing": True,
                        },
                    ),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
        # Create the file
        res = FileManager.create_file(self.__current_folder / filename, test_existing)
        log.info(
            "create_file({}) returns {}".format(self.__current_folder / filename, res)
        )
        # Close the dialog box
        self._current_dialog = None
        # Refresh the current folder and focus on filename
        self.__init_new_current_folder_and_build_braille_line(
            self.__current_folder, focused_file=self.__current_folder / filename
        )
        return

    def _exec_valid_new_folder_dialog(self):
        log.info("callback:_exec_valid_new_file_dialog")
        kwargs = self._current_dialog.get_values()
        self.__new_folder(**kwargs)

    def __new_folder(self, **kwargs):
        """
        Create a new folder.
        :param kwargs:
          "folder_name" : The folder name
        :return:
        """
        log.info(f"{kwargs=}")
        folder = kwargs["folder_name"]
        # Reject an empty folder
        if not folder:
            # Return to the dialog box new folder.
            self._exec_new_folder()
            return
        # Check if invalids characters.
        if not FileManager.is_valid_filename(folder):
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("the following characters are invalid ") + '<>"/\\|?*'),
                action=self._exec_new_folder,
                action_param={"folder_name": folder},
            )
            return
        # Check if folder exists.
        if (self.__current_folder / folder).exists():
            # Display folder already exists...
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("folder {} already exists.").format(folder),
                action=self._exec_new_folder,
                action_param={"folder_name": folder},
            )
            return
        res = FileManager.create_folder(self.__current_folder / folder)
        log.info(
            "create_folder({}) returns {}".format(self.__current_folder / folder, res)
        )
        # Close the dialog box
        self._current_dialog = None
        # Refresh the current folder and focus on folder
        self.__init_new_current_folder_and_build_braille_line(
            self.__current_folder, focused_file=self.__current_folder / folder
        )

    def _exec_valid_rename_dialog(self, **kwargs):
        log.info("callback:_exec_valid_rename_dialog")
        kwargs = self._current_dialog.get_values()
        self.__rename(**kwargs)

    def __rename(self, **kwargs):
        filename = kwargs["rename_name"]
        if not filename or filename.startswith("."):
            # Return to rename dialog box.
            self._exec_rename()
        # Check if invalids characters.
        if not FileManager.is_valid_filename(filename):
            self.__new_rename_name = filename
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("the following characters are invalid ") + '<>"/\\|?*'),
                action=self._exec_rename,
                action_param={"rename_name": filename},
            )
            return
        # Check if rename file already exists.
        if (self.__current_folder / filename).exists():
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("{} already exists.").format(filename)),
                action=self._exec_rename,
                action_param={"rename_name": filename},
            )
            return
        FileManager.rename(
            self.__current_folder / self.__files[self.__focused_file_index],
            self.__current_folder / filename,
        )
        # Close the dialog box
        self._current_dialog = None
        # Refresh the current folder and focus on renamed item
        self.__init_new_current_folder_and_build_braille_line(
            self.__current_folder, focused_file=self.__current_folder / filename
        )

    def _exec_valid_send_to_dialog(self):
        kwargs = self._current_dialog.get_values()
        log.info("callback:_exec_valid_send_to_dialog {kwargs}")
        send_to_machine = kwargs["computer"]
        # Find mac address of selected machine.
        send_to_mac_address = None
        for key, value in self.__paired_devices.items():
            log.info("key={} value={} computer={}".format(key, value, send_to_machine))
            if value == send_to_machine:
                send_to_mac_address = key
                break
        log.info(
            "__send_to_mac_address={} __send_to_machine={}".format(
                send_to_mac_address, send_to_machine
            )
        )
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("question"),
            message=_("put {} into Bluetooth reception mode (Windows 10 only).").format(
                send_to_machine
            ),
            buttons=[
                ui.UiButton(
                    name=_("&ok"),
                    action=self.__send_to,
                    action_param={
                        "machine": send_to_machine,
                        "mac_address": send_to_mac_address,
                    },
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __send_to(self, **kwargs):
        machine = kwargs["machine"]
        send_to_mac_address = kwargs["mac_address"]
        send_to_files = []
        for file in self.__selected_files:
            send_to_files.append(file)
        log.info("self.__selected_files={}".format(self.__selected_files))
        if send_to_mac_address is not None:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("sending {}").format("")
            )
            self.__is_send_to = True
            self.__send_to_thread = SendToThread(
                send_to_files,
                machine,
                send_to_mac_address,
                None,
                self.__on_progress,
                self.__end_send_to,
            )
            self.__send_to_thread.start()
        return

    def __end_send_to(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_SEND_TO, *args, **kwargs)

    def __end_send_to_dlg(self, *args, **kwargs) -> bool:
        send_to_machine = kwargs["machine"]
        filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"])
        if kwargs["send_to_success"]:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("{} successfully sent to {}.").format(
                    filename, send_to_machine
                ),
                action=self._exec_cancel_dialog,
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("error can't be sent {} to {}.").format(
                    filename, send_to_machine
                ),
                action=self._exec_cancel_dialog,
            )
        self.__send_to_thread = None
        return True

    def _exec_zip_dialog(self):
        kwargs = self._current_dialog.get_values()
        log.info(f"callback:_exec_zip_dialog <{kwargs}>")
        self.__zip(**kwargs)

    def __zip(self, **kwargs):
        filename = kwargs["zip_file"]
        log.info("Filename=#{}#".format(filename))
        test_existing = True
        if "no_test_existing" in kwargs.keys() and kwargs["no_test_existing"]:
            test_existing = False
        # Reject an empty filename
        if not filename or filename.startswith("."):
            # Return to the dialog box new file.
            self._exec_zip(zip_name=filename)
            return
        # Append .zip extension if missing.
        path, extension = os.path.splitext(filename)
        log.info("path={} extension={}".format(path, extension))
        if extension != ".zip":
            filename += ".zip"
        # Check if invalids characters.
        if not FileManager.is_valid_filename(filename):
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("the following characters are invalid ") + '<>"/\\|?*'),
                action=self._exec_zip,
                action_param={"zip_name": filename},
            )
            return
        # Test if file exists.
        if test_existing and (self.__current_folder / filename).exists():
            ui_filename = ui.UiFileManagerLine.friendly_file_name(filename)
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("question"),
                message=_("{} already exists. do you want to replace it?").format(
                    ui_filename
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"),
                        action=self.__zip,
                        action_param={"zip_file": filename, "no_test_existing": True},
                    ),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
        zip_files = []
        for file in self.__selected_files:
            zip_files.append(file)
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("compressing {}% {}").format("   ", "")
        )
        self.__zip_thread = ZipThread(
            zip_files,
            self.__current_folder / filename,
            base_folder=self.__current_folder,
            on_progress=self.__on_progress,
            on_end=self.__end_zip,
            zip_hidden_file=True,
        )
        self.__zip_thread.start()
        # Reset extend selection (as if user has pressed ESC)
        self.__reset_extend_selection()

    def _exec_backup_dialog(self):
        kwargs = self._current_dialog.get_values()
        log.info(f"callback:_exec_backup_dialog <{kwargs}>")
        self.__backup(**kwargs)

    def __backup(self, **kwargs):
        filename = kwargs["backup_file"]
        test_existing = True
        if "no_test_existing" in kwargs.keys() and kwargs["no_test_existing"]:
            test_existing = False
        # Reject an empty filename
        if not filename or filename.startswith("."):
            # Return to the dialog box new file.
            self._exec_backup(zip_name=filename)
            return
        # Append .zip extension if missing.
        path, extension = os.path.splitext(filename)
        log.info("path={} extension={}".format(path, extension))
        if extension != ".zip":
            filename += ".zip"
        # Check if invalids characters.
        if not FileManager.is_valid_filename(filename):
            self._current_dialog = ui.UiInfoDialogBox(
                message=(_("the following characters are invalid ") + '<>"/\\|?*'),
                action=self._exec_backup,
                action_param={"zip_name": filename},
            )
            return
        # Test if file exists.
        if test_existing and (FileManager.get_backup_path() / filename).exists():
            ui_filename = ui.UiFileManagerLine.friendly_file_name(filename)
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("question"),
                message=_("{} already exists. do you want to replace it?").format(
                    ui_filename
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"),
                        action=self.__backup,
                        action_param={
                            "backup_file": filename,
                            "no_test_existing": True,
                        },
                    ),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
        zip_files = list()
        zip_files.append(FileManager.get_documents_path())

        self._current_dialog = ui.UiInfoDialogBox(
            message=_("backuping {}% {}").format("   ", "")
        )

        self.__zip_thread = ZipThread(
            zip_files,
            FileManager.get_backup_path() / filename,
            base_folder=FileManager.get_documents_path(),
            on_progress=self.__on_progress,
            on_end=self.__end_backup,
            zip_hidden_file=True,
            exclude_files=(
                FileManager.get_documents_path() / CLIP_FILE,
                FileManager.get_usb_flash_drive_path(),
            ),
            operation="backup",
        )
        self.__zip_thread.start()

    def __end_backup_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs and "filename" in kwargs:
            filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"], True)
            if kwargs["success"]:
                # Close the dialog box
                self._current_dialog = None
                # Refresh the current folder and focus on filename
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=kwargs["filename"]
                )
            else:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("error backup can't be created to {}.").format(filename),
                    action=self._exec_cancel_dialog,
                )
        self.__zip_thread = None
        return True

    def __end_backup(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_BACKUP, *args, **kwargs)

    def _exec_restore_dialog(self):
        kwargs = self._current_dialog.get_values()
        log.info(f"callback:_exec_backup_dialog <{kwargs}>")
        self.__restore(**kwargs)

    def __restore(self, **kwargs):
        backup_filename = kwargs["backup_file"]

        self._current_dialog = ui.UiInfoDialogBox(
            message=_("restoring {}% {}").format("   ", "")
        )
        self.__unzip_thread = UnZipThread(
            FileManager.get_backup_path() / backup_filename,
            FileManager.get_documents_path(),
            on_progress=self.__on_progress,
            on_ask_replace=self.__on_ask_replace,
            on_end=self.__end_restore,
        )
        self.__unzip_thread.start()

    def __on_ask_replace(self, *args, **kwargs):
        log.info(f"__on_ask_replace {kwargs=}")
        self._put_in_function_queue(FunctionId.FUNCTION_ON_ASK_REPLACE, *args, **kwargs)

    def __end_restore(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_RESTORE, *args, **kwargs)

    def __end_zip(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_ZIP, *args, **kwargs)

    def __end_unzip(self, *args, **kwargs):
        self._put_in_function_queue(FunctionId.FUNCTION_END_UNZIP, *args, **kwargs)

    def __end_restore_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs and "filename" in kwargs:
            filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"])
            if kwargs["success"]:
                filename = None
                if self.__focused_file_index in range(len(self.__files)):
                    filename = self.__files[self.__focused_file_index].name
                # Close the dialog box
                self._current_dialog = None
                # Refresh the current folder and focus on filename
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=filename
                )
            else:
                error = None
                if "error" in kwargs:
                    error = kwargs["error"]
                self._current_dialog = ui.UiInfoDialogBox(
                    message="{} ({})".format(error, filename),
                    action=self._exec_cancel_dialog,
                )
        self.__unzip_thread = None
        return True

    def __end_zip_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs and "filename" in kwargs:
            filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"])
            if kwargs["success"]:
                # Close the dialog box
                self._current_dialog = None
                # Refresh the current folder and focus on filename
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=kwargs["filename"]
                )
            else:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("error can't compress files in {}.").format(filename),
                    action=self._exec_cancel_dialog,
                )
        self.__zip_thread = None
        return True

    def __end_unzip_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs and "filename" in kwargs:
            filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"])
            if kwargs["success"]:
                file_to_focus = None
                if "destination" in kwargs:
                    file_to_focus = kwargs["destination"]
                # Close the dialog box
                self._current_dialog = None
                # Refresh the current folder with the zipped file focused
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=file_to_focus
                )
            else:
                error = None
                if "error" in kwargs:
                    error = kwargs["error"]
                self._current_dialog = ui.UiInfoDialogBox(
                    message="{} ({})".format(error, filename),
                    action=self._exec_cancel_dialog,
                )
        self.__unzip_thread = None
        return True

    def __end_restore_from_trash_dlg(self, *args, **kwargs) -> bool:
        if "success" in kwargs:
            if kwargs["success"]:
                filename = None
                if self.__focused_file_index + 1 in range(len(self.__files)):
                    filename = self.__files[self.__focused_file_index + 1]
                elif self.__focused_file_index - 1 in range(len(self.__files)):
                    filename = self.__files[self.__focused_file_index - 1]
                # Close the dialog box
                self._current_dialog = None
                # Refresh the current folder and focus on filename
                self.__init_new_current_folder_and_build_braille_line(
                    self.__current_folder, focused_file=filename
                )
            else:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("error during restoration from trash."),
                    action=self._exec_cancel_dialog,
                )
        self.__restore_from_trash_thread = None
        return True

    def __ask_replace_file_dlg(self, *args, **kwargs) -> bool:
        operation = kwargs["operation"]
        filename = ui.UiFileManagerLine.friendly_file_name(kwargs["filename"])
        if "is_cancelable" in kwargs:
            is_cancelable = kwargs["is_cancelable"]
        else:
            is_cancelable = True
        action_cancelable = None
        if is_cancelable:
            action_cancelable = self._exec_cancel_dialog
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("question"),
            message=_("file {} exists. do you want to replace it?").format(filename),
            buttons=[
                ui.UiButton(
                    name=_("&yes"),
                    action=self.__ask_replace_yes,
                    action_param={"operation": operation},
                ),
                ui.UiButton(
                    name=_("&no"),
                    action=self.__ask_replace_no,
                    action_param={"operation": operation},
                ),
                ui.UiButton(
                    name=_("yes for &all"),
                    action=self.__ask_replace_yes_for_all,
                    action_param={"operation": operation},
                ),
                ui.UiButton(
                    name=_("no for a&ll"),
                    action=self.__ask_replace_no_for_all,
                    action_param={"operation": operation},
                ),
            ],
            action_cancelable=action_cancelable,
        )
        return True

    def __replace_answer(self, operation, yes, to_all):
        thread = None
        if operation == "unzip" or operation == "restore":
            thread = self.__unzip_thread
        if operation == "copy" or operation == "move":
            thread = self.__copy_move_thread
        if operation == "restore_from_trash":
            thread = self.__restore_from_trash_thread
        if thread:
            thread.replace_answer(yes, to_all)
        else:
            log.error("No thread running")
            # Close the dialog box
            self._current_dialog = None

    def __ask_replace_yes(self, operation):
        self.__replace_answer(operation, True, False)

    def __ask_replace_no(self, operation):
        self.__replace_answer(operation, False, False)

    def __ask_replace_yes_for_all(self, operation):
        self.__replace_answer(operation, True, True)

    def __ask_replace_no_for_all(self, operation):
        self.__replace_answer(operation, False, True)

    def refresh_current_item(self, rebuild_all=False):
        if rebuild_all:
            self.__init_new_current_folder_and_build_braille_line(
                self.__current_folder,
                focused_file=self.__files[self.__focused_file_index],
            )
        self.__build_braille_line()

    # Key events

    def input_function(self, *args, **kwargs) -> bool:
        log.info("args={} kwargs={}".format(args, kwargs))
        if len(args):
            function_id = args[0]
            if function_id == FunctionId.FUNCTION_IN_PROGRESS:
                log.info("update in progress dialog box")
                return self.__in_progress_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_DELETE:
                log.info("update in progress dialog box")
                return self.__end_delete_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_BACKUP:
                return self.__end_backup_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_RESTORE:
                return self.__end_restore_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_ZIP:
                return self.__end_zip_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_UNZIP:
                return self.__end_unzip_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_SEND_TO:
                return self.__end_send_to_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_PASTE:
                return self.__end_paste_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_END_EOLE_DOWNLOAD:
                return self.__end_eole_download_dlg(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_FORCE_REFRESH_DIALOG_IN_DIALOG:
                return self.__refresh_dialog_in_dialog(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_ON_ASK_REPLACE:
                return self.__ask_replace_file_dlg(*args, **kwargs)
            elif function_id == FunctionId.END_RESTORE_FROM_TRASH:
                return self.__end_restore_from_trash_dlg(*args, **kwargs)
            else:
                return super(FileManagerApp, self).input_function(*args, **kwargs)

    def input_command(self, data, modifier, key_id) -> bool:
        done = False
        if key_id != Keyboard.KeyId.KEY_NONE:
            log.info("key_id={}".format(key_id))

            # Pass the command to DialogBox / Menu / BrailleDisplay
            done = super(FileManagerApp, self).input_command(data, modifier, key_id)
            log.info(f"BnoteApp.input_command returns {done=}")

            # Decoding key command for file manager document
            if not done and (modifier == 0):
                if key_id == Keyboard.KeyId.KEY_START_DOC:
                    self.__first_item()
                    done = True
                elif key_id == Keyboard.KeyId.KEY_END_DOC:
                    self.__last_item()
                    done = True
                elif key_id == Keyboard.KeyId.KEY_CARET_DOWN:
                    self.__next_item()
                    done = True
                elif key_id == Keyboard.KeyId.KEY_CARET_UP:
                    self.__previous_item()
                    done = True
                elif key_id == Keyboard.KeyId.KEY_CARET_LEFT:
                    self.__activate_parent()
                    done = True
                elif key_id == Keyboard.KeyId.KEY_CARET_RIGHT:
                    self.__enter_in_folder()
                    done = True
            if not done:
                done = self.__ui_line.input_command(modifier, key_id)
                log.info(f"self.__files_braille_line.input_command returns {done=}")
        return done

    def input_character(self, modifier, character, data) -> bool:
        # log.info("modifier={} character={} time.time_ns()={}".format(modifier, character, time.time_ns()))
        log.info("Call BnoteApp.input_character({},{})".format(modifier, character))
        done = super(FileManagerApp, self).input_character(modifier, character, data)
        # Check if a function must be done
        if not done:
            if modifier == 0:
                self.__quick_search.do_quick_search(character)
                done = True

        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))

        done = super(FileManagerApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            functions = {
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_F8): self.__do_F8,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE): self.__do_ESC,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_F2): self.__rename_dialog,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_F3): self.__quick_search.do_quick_search_again,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_DELETE): self.__do_delete,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE,
                ): self.__handle_bramigraph_space,
                # (Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,  Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE):
                #     self.__activate_parent,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_UP,
                ): self.__previous_item,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_DOWN,
                ): self.__next_item,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_LEFT,
                ): self.__activate_parent,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT,
                ): self.__enter_in_folder,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_HOME,
                ): self.__first_item,
                (
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    Keyboard.BrailleFunction.BRAMIGRAPH_END,
                ): self.__last_item,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_F5): self.__do_F5,
            }
            func = functions.get((modifier, bramigraph), None)
            if func:
                func()
                done = True
            else:
                done = self.__ui_line.input_bramigraph(modifier, bramigraph)

        return done

    def __handle_bramigraph_space(self) -> bool:
        # This code will toggle the selected attribut of the BrailleObject for Bramigraph is SIMPLE_SPACE
        self.__ui_line.input_bramigraph(
            Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
            Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE,
        )
        # This code will update the selected file list according to the new selected BrailleObject attribute
        # keep in mind the selected state of the current file
        self.__update_selected_files()
        # The current file/folder has changed of presentation.
        self.__build_braille_line()
        return True

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {position=} {key_type=}")
        done = super(FileManagerApp, self).input_interactive(
            modifier, position, key_type
        )
        if not done:
            # interactive key treatment for file manager.
            if modifier == 0:
                # Exec function on the files_braille_line to activate parent or child item
                done = self.__ui_line.input_interactive(modifier, position, key_type)
        return done

    def refresh_document(self):
        """
        Overload base class. Call when menu or dialogbox are closed.
        :return: None
        """
        # Do not try to refresh the braille display if we are in menu or document
        # (because braille_display is the same for all ui).
        if self.in_menu_or_in_dialog():
            return
        # Because braille_display is the same for all ui, we need to reconstruct it.
        self.__ui_line._update_braille_display()

    def get_data_line(self, force_refresh=False) -> (str, str, str, bool):
        """
        Overload get_data_line of BnoteApp
        Get the braille line of the document area.
        :param force_refresh:
        :return:
          (static_text, static_dots, dynamic_dots) if something changed since the last call or if force_refresh=True
          else return (None, None, None)
        """
        if self.in_menu_or_in_dialog():
            return BnoteApp.get_data_line(self, force_refresh)

        return self.__ui_line.get_data_line(force_refresh)

    def __operation_not_allowed(self):
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("operation not allowed in this directory."),
            action=self._exec_cancel_dialog,
        )

    def __quick_search_move_call_back(self, text_to_find) -> bool:
        log.info(f"{text_to_find=}")
        text_to_find = text_to_find.lower()

        # If we search on the BONOTE_MAIN_FOLDER, we want to search for the localized file name instead of the real
        # filename.
        use_friendly_file_name = False
        if self.__current_folder == FileManager.get_main_folder_path():
            use_friendly_file_name = True

        # Search from self.__focused_file_index to end of list
        for index, file in enumerate(self.__files):
            log.info("file={} index={}".format(file, index))
            file_name = file.name.lower()
            if use_friendly_file_name:
                file_name = ui.UiFileManagerTools.friendly_file_name(file, True)
            if (
                file_name.lower().find(text_to_find) == 0
                and index > self.__focused_file_index
            ):
                if self.__extend_selection is True:
                    # keep in mind the selected state of the current file
                    self.__update_selected_files()
                else:
                    self.__selected_files = []
                # Focus the wanted item
                self.__focused_file_index = index
                # Refresh the braille display
                self.__build_braille_line()
                return True

        # Search from 0 to self.__focused_file_index in the list
        for index, file in enumerate(self.__files):
            log.info("file={} index={}".format(file, index))
            file_name = file.name.lower()
            if use_friendly_file_name:
                file_name = ui.UiFileManagerTools.friendly_file_name(file, True)
            if (
                file_name.lower().find(text_to_find) == 0
                and index < self.__focused_file_index
            ):
                if self.__extend_selection is True:
                    # keep in mind the selected state of the current file
                    self.__update_selected_files()
                else:
                    self.__selected_files = []
                # Focus the wanted item
                self.__focused_file_index = index
                # Refresh the braille display
                self.__build_braille_line()
                return True

        return False

    def __update_selected_files(self):
        ui_object = self.__ui_line.displayed_file()
        if ui_object:
            # keep in mind the selected state of the current file
            if ui_object.selected():
                if not self.__files[self.__focused_file_index] in self.__selected_files:
                    # Do not append simlink used for Bluetooth and backup
                    if (
                        self.__files[self.__focused_file_index].exists()
                        and not self.__files[self.__focused_file_index].is_symlink()
                    ):
                        self.__selected_files.append(
                            self.__files[self.__focused_file_index]
                        )
            else:
                if self.__files[self.__focused_file_index] in self.__selected_files:
                    self.__selected_files.remove(
                        self.__files[self.__focused_file_index]
                    )

    # Get the list dir for the wanted path.
    @staticmethod
    def __list_dir(path, hide_hidden_file=True):
        user_files = []

        # 2024 : Exclude file list is no more necessary.
        exclude_list = []
        # We want to hide only the crash folder if no crash report.
        if not len(FileManager.listdir(FileManager.get_crash_path())):
            exclude_list.append(FileManager.get_crash_path())

        files = FileManager.listdir(path, hide_hidden_file=hide_hidden_file)
        if files is not None:
            for file in files:
                if file not in exclude_list:
                    if file.is_dir():
                        user_files.append(file)
                    elif file.is_file():
                        user_files.append(file)

        return user_files

    def __enter_in_folder(self):
        focused_file = self.__files[self.__focused_file_index]
        if focused_file.is_dir():
            self.__init_new_current_folder_and_build_braille_line(focused_file)

    @staticmethod
    def split_filename_and_extension(filename):
        (shortname, extension) = os.path.splitext(filename)
        if extension:
            extension = extension.lower()
        return shortname, extension

    def __activate_child(self, read_only=False):
        if len(self.__selected_files) > 1:
            # Multiple files selection. Runs only for mp3 files.
            for filename in self.__selected_files:
                (short_name, extension) = self.split_filename_and_extension(filename)
                if extension in Mp3App.known_extension():
                    self.__activate_mp3_apps(**{"filenames": self.__selected_files})
                    break
        else:
            # A file alone is selected.
            focused_file = self.__files[self.__focused_file_index]
            log.info("focused_file = {}".format(focused_file))

            if focused_file.is_dir():
                self.__init_new_current_folder_and_build_braille_line(focused_file)
            elif focused_file.is_file():
                if str(focused_file).endswith(".whl.zip"):
                    bnote_whl_file, version = YAUpdater.get_version(focused_file)
                    if version != "":
                        self._current_dialog = ui.UiMessageDialogBox(
                            name=_("information"),
                            message=_("do you want to install the version {} ?").format(
                                version
                            ),
                            buttons=[
                                ui.UiButton(
                                    name=_("&yes"),
                                    action=self._exec_install_version_with_yaupdater,
                                    action_param={"file": focused_file},
                                ),
                                ui.UiButton(
                                    name=_("&no"), action=self._exec_cancel_dialog
                                ),
                            ],
                            action_cancelable=self._exec_cancel_dialog,
                        )
                        return
                elif (
                    str(self.__current_folder).startswith(
                        str(FileManager.get_bluetooth_path())
                    )
                    or str(self.__current_folder).startswith(
                        str(FileManager.get_backup_path())
                    )
                    or str(self.__current_folder).startswith(
                        str(Trash.get_trash_path())
                    )
                ):
                    self._current_dialog = ui.UiInfoDialogBox(
                        message=_(
                            "unable to open file in this directory. move it in document directory."
                        ),
                        action=self._exec_cancel_dialog,
                    )
                    return
                (shortname, extension) = self.split_filename_and_extension(focused_file)
                if extension:
                    extension = extension.lower()
                if (
                    extension in EditorApp.known_extension()
                    or extension in MusicApp.known_extension()
                    or extension in AiAssistantApp.known_extension()
                    or (
                        extension in DaisyApp.known_extension()
                        and DaisyReader.daisy_zip_check(focused_file)
                    )
                ):
                    RecentFile().add_file_to_list(focused_file.name, focused_file)
                    log.info("SI LE FICHIER EST DE TYPE CONNU ON LE PASSE A l'EDITEUR")

                    # Check if user has not already opened too many documents
                    if len(self.__locked_filenames) < MAX_EDITOR_APP:
                        # Check if .brf extension, in this case, ask for language.
                        if extension == ".brf":
                            self._current_dialog = ui.UiDialogBox(
                                name=_("langue"),
                                action_cancelable=self._exec_cancel_dialog,
                                item_list=[
                                    ui.UiListBox(
                                        name=_("langue"),
                                        value=("language", ["FR", "US"]),
                                        current_index=0,
                                    ),
                                    ui.UiButton(
                                        name=_("&ok"),
                                        action=self._exec_brf_type_dialog,
                                        action_param={"filename": focused_file},
                                    ),
                                    ui.UiButton(
                                        name=_("&cancel"),
                                        action=self._exec_cancel_dialog,
                                    ),
                                ],
                            )
                        else:
                            # It is important to be not US, in "ES" version the .mat
                            # will be read with current liblouis instance.
                            self._put_in_function_queue(
                                FunctionId.OPEN_THE_FILE_PLEASE,
                                **{
                                    "filename": focused_file,
                                    "language": "FR",
                                    "read_only": read_only,
                                },
                            )
                            return
                    else:
                        self._current_dialog = ui.UiInfoDialogBox(
                            message=_("you cannot open more documents."),
                            action=self._exec_cancel_dialog,
                        )
                elif extension in Mp3App.known_extension():
                    RecentFile().add_file_to_list(focused_file.name, focused_file)
                    self.__activate_mp3_apps(**{"filename": focused_file})
                elif extension == ".zip":
                    self._current_dialog = ui.UiMessageDialogBox(
                        name=_("unzip"),
                        message=_("Unzip file {}?").format(focused_file.name),
                        buttons=[
                            ui.UiButton(name=_("&yes"), action=self._exec_unzip),
                            ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                        ],
                        action_cancelable=self._exec_cancel_dialog,
                    )
                # Settings
                elif extension == ".bnote":
                    self._current_dialog = ui.UiMessageDialogBox(
                        name=_("warning"),
                        message=_(
                            "this file will be replace the existing settings file, do you want to continue?"
                        ),
                        buttons=[
                            ui.UiButton(name=_("&yes"), action=self.__import_settings),
                            ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                        ],
                        action_cancelable=self._exec_cancel_dialog,
                    )

    def __activate_mp3_apps(self, **kwargs):
        if Settings().data["system"]["app_mp3"] != "invisible":
            self._put_in_function_queue(FunctionId.OPEN_THE_MP3_FILE_PLEASE, **kwargs)
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_(
                    "please, switch audio application visible in menu in settings to play audio file."
                ),
                action=self._exec_cancel_dialog,
            )

    def _exec_brf_type_dialog(self, **kwargs):
        filename = kwargs["filename"]
        values = self._current_dialog.get_values()
        language = values["language"]
        self._put_in_function_queue(
            FunctionId.OPEN_THE_FILE_PLEASE,
            **{"filename": filename, "language": language},
        )

    def _exec_install_version_with_yaupdater(self, file):
        log.info(f"!!!_exec_install_version_with_yaupdater{threading.get_ident()=}")
        # Check current date.
        year = datetime.datetime.now().year
        if year < 2024:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_(_(f"set the date and time before updating bnote.")),
                action=self._exec_cancel_dialog,
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("installation in progres...")
            )
            # Refresh the braille display
            self.__build_braille_line()
            YAUpdater(
                f"file://{file}",
                "/home/pi/all_bnotes/",
                self.refresh_install_message,
                self.yaupdater_ended,
            )

    def refresh_install_message(self, msg):
        log.info(f"!!!refresh_install_message:{threading.get_ident()=}-{msg=}")
        self._put_in_function_queue(
            FunctionId.ASK_TO_REFRESH_MESSAGE_DIALOG, **{"msg": msg}
        )
        # To let ui thread running
        time.sleep(0.01)

    def _unable_to_update_info_dialog(self):
        """
        Call when execution of update bnote application failed.
        """
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("unable to update."),
            action=self._exec_cancel_dialog,
        )

    def yaupdater_ended(self, result):
        if not result:
            # Open an info dialog box to inform user.
            self._put_in_function_queue(FunctionId.UNABLE_TO_UPDATE)
        else:
            # Change message and restart service to restart the new bnoteapp.
            self.refresh_install_message("install done, restart new version...")
            self._put_in_function_queue(
                FunctionId.ASK_TERMINATE_BNOTE_AND_RESTART_SERVICE
            )

    def __import_settings(self):
        file = str(self.__files[self.__focused_file_index])
        settings = Settings().import_settings(file)
        if not settings:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("failed to import the file, check the source and try again."),
                action=self._exec_cancel_dialog,
            )
            return
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("imported settings."), action=self._exec_cancel_dialog
        )
        # for section, section_data in Settings().data.items():
        #     for key in section_data:
        #         self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{'section': section, 'key': key})

    def __activate_parent(self, *args, **kwargs):
        # User must stay in his user space.
        if self.__current_folder == FileManager.get_main_folder_path():
            return
        # Separate path and filename
        if self.__current_folder.parent.is_dir():
            self.__init_new_current_folder_and_build_braille_line(
                self.__current_folder.parent, focused_file=self.__current_folder
            )

    def __next_item(self):
        log.info("__next_item")
        # That can be done only if the child is focused.
        if self.__focused_file_index + 1 in range(1, len(self.__files)):
            if self.__extend_selection is True:
                # keep in mind the selected state of the current file
                self.__update_selected_files()
            else:
                self.__selected_files = []

            # Focus the next item
            self.__focused_file_index += 1
            # Refresh the braille display
            self.__build_braille_line()

    def __previous_item(self):
        log.info("__previous_item")
        if self.__focused_file_index - 1 in range(len(self.__files)):
            if self.__extend_selection is True:
                # keep in mind the selected state of the current file
                self.__update_selected_files()
            else:
                self.__selected_files = []

            # Focus the previous item
            self.__focused_file_index -= 1
            # Refresh the braille display
            self.__build_braille_line()

    def __last_item(self):
        log.info("__last_item")
        # That can be done only if the child is focused.
        if len(self.__files):
            if self.__extend_selection is True:
                # keep in mind the selected state of the current file
                self.__update_selected_files()
            else:
                self.__selected_files = []

            # Focus the last item
            self.__focused_file_index = len(self.__files) - 1
            # Refresh the braille display
            self.__build_braille_line()

    def __first_item(self):
        log.info("__first_item")
        # That can be done only if the child is focused.
        if self.__extend_selection is True:
            # keep in mind the selected state of the current file
            self.__update_selected_files()
        else:
            self.__selected_files = []

        # Focus the first item
        self.__focused_file_index = 0
        # Refresh the braille display
        self.__build_braille_line()

    # parent_dir must be a real path
    def __init_new_current_folder_and_build_braille_line(
        self, parent_dir, focused_file=None
    ):
        # Clear the time_prvious_char to be sure that next call to self.__quick_search.do_quick_search()
        # will start with a new empty search buffer but not self.__quick_search.do_quick_search_again()
        self.__quick_search.clear_time_previous_char()
        # If something is wrong (maybe user remove some folders from outside bnote app), we must recover situation
        if not os.path.exists(parent_dir):
            parent_dir = FileManager.get_documents_path()

        # Init the current folder
        self.__current_folder = parent_dir

        log.debug(f"Trash.get_trash_path() = {Trash.get_trash_path()}")
        log.debug(f"self.__current_folder = {self.__current_folder}")
        log.debug(f"self.__current_folder.parents={self.__current_folder.parents}")
        for part in self.__current_folder.parents:
            log.debug(f"part={part}")

        log.debug(
            f"self.__current_folder.startswith("
            f"Trash.get_trash_path())={str(self.__current_folder).startswith(str(Trash.get_trash_path()))}"
        )
        # Change the menus according to current folder
        if str(self.__current_folder) == str(FileManager.get_main_folder_path()):
            BnoteApp.set_menu(self, self._file_manager_main_emplacement_main_menu)
        elif str(self.__current_folder).startswith(str(Trash.get_trash_path())):
            BnoteApp.set_menu(self, self._trash_main_menu)
        elif str(self.__current_folder).startswith(
            str(FileManager.get_bluetooth_path())
        ):
            BnoteApp.set_menu(self, self._bluetooth_main_menu)
        elif str(self.__current_folder) == str(FileManager.get_usb_flash_drive_path()):
            # This case is for Usb flash drive list (we can have a hub with more than one usb stick)
            if len(FileManagerApp.__list_dir(self.__current_folder)):
                # When current folder is the list of USB flash drive list and at least 1 usb flash disk is plugged
                # (we can have a hub with more than one usb stick)
                # The file menu contains "File>unplug usb flash drive" menu item
                # (we don't allow user to create file in /media)
                BnoteApp.set_menu(self, self._usb_flash_drive_list_main_menu)
            else:
                # empty list means "No usb flask drive mounted" (so we show a File menu with only actualize)
                BnoteApp.set_menu(self, self._usb_flash_drive_empty_list_main_menu)
        elif str(self.__current_folder).startswith(
            str(FileManager.get_usb_flash_drive_path())
        ):
            # Special File menu with "File>unplug usb flash drive" menu item is displayed in an usb stick subfolder.
            BnoteApp.set_menu(self, self._usb_flash_drive_main_menu)
        else:
            # Default menu for file manager with or without usb key plugged
            if len(FileManagerApp.__list_dir(FileManager.get_usb_flash_drive_path())):
                BnoteApp.set_menu(
                    self, self._file_manager__with_usb_flash_drive_plugged_main_menu
                )
            else:
                BnoteApp.set_menu(self, self._file_manager_main_menu)
        # Clear the selected files list
        self.__selected_files = []
        # When user changes the current folder the self.__extend_selection must be set to the False value.
        self.__extend_selection = False

        try:
            # Build the files list
            self.__files = FileManagerApp.__list_dir(self.__current_folder)
        except IOError:
            # Fix le crash si l'utilisateur a arraché une clef USB sans avoir fait "ejecter la clef"
            self.__files = []
        if len(self.__files) == 0:
            self.__files.append(Path(_("empty directory...")))

        # Reset the focused item that will be presented on the BrailleLine
        self.__focused_file_index = 0

        # If we have a filename to focused, search it in the file list.
        if focused_file is not None:
            p = Path(focused_file)
            for index, file in enumerate(self.__files):
                if p == file:
                    # Focus the wanted item
                    self.__focused_file_index = index
                    break

        # Reset the start_name for quick search
        self.__start_name_quick_search = ""

        # The BrailleLine that will be "current_dir:self.__files[self.__focused_file]"
        self.__build_braille_line()
        # Update shortcuts visibilities.
        self._update_menu_items()

    def __build_braille_line(self):
        # The BrailleLine that will be "current_dir:self.__files[self.__focused_file]"
        if not self.__extend_selection:
            # if not in selection mode, the selected list contains allways the displayed file.
            if not self.__files[self.__focused_file_index] in self.__selected_files:
                # Do not append simlink used for Bluetooth and backup
                if (
                    self.__files[self.__focused_file_index].exists()
                    and not self.__files[self.__focused_file_index].is_symlink()
                ):
                    self.__selected_files = [self.__files[self.__focused_file_index]]

        self.__ui_line = ui.UiFileManagerLine(
            parent_name=self.__current_folder,
            parent_action=self._exec_activate_parent,
            file_name=self.__files[self.__focused_file_index],
            file_action=self._exec_activate_child,
            selected=self.__files[self.__focused_file_index] in self.__selected_files,
            is_selectable=self.__extend_selection,
        )

    def _exec_activate_parent(self):
        self.__activate_parent()

    def _exec_activate_child(self):
        self.__activate_child()

    def clean_uo_locked_file(self):
        self.__locked_filenames = []

    def append_locked_file(self, file):
        log.debug("file to lock {}".format(file))
        if file:
            self.__locked_filenames.append(file)

    def remove_locked_file(self, file) -> bool:
        log.debug("file to remove {}".format(file))
        log.debug("files list {}".format(self.__locked_filenames))
        if file and (file in self.__locked_filenames):
            self.__locked_filenames.remove(file)
            return True
        return False

    def synch_to_file(self, file):
        file = Path(file)
        if file.parent == self.__current_folder:
            self.__init_new_current_folder_and_build_braille_line(
                self.__current_folder, focused_file=file
            )

    def __is_open_in_editor(self, files):
        for file in self.__locked_filenames:
            if file in files:
                return True
        return False

    def __on_progress(self, *args, **kwargs):
        log.info("_on_progress() called ! args={} kwargs={}".format(args, kwargs))
        self._put_in_function_queue(FunctionId.FUNCTION_IN_PROGRESS, *args, **kwargs)

    def __in_progress_dlg(self, *args, **kwargs) -> bool:
        operation = kwargs["operation"]
        filename = kwargs["filename"]
        cur_progress = kwargs["current_progress"]
        max_progress = kwargs["max_progress"]
        try:
            percent_progress = "%3d" % (100 * cur_progress / max_progress)
        except TypeError:
            percent_progress = "???"
        except ZeroDivisionError:
            percent_progress = "???"

        if operation == "delete":
            msg = _("deleting {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "unzip":
            msg = _("extracting {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "zip":
            msg = _("compressing {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "move":
            msg = _("moving {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "copy":
            msg = _("copying {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "backup":
            msg = _("backuping {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "restore":
            msg = _("restoring {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        elif operation == "send to":
            msg = _("sending {}% {}").format(
                percent_progress, os.path.basename(filename)
            )
        else:
            msg = _("in progress {}%").format(percent_progress)
        self._update_in_progress(msg)
        log.info(msg)
        return True

    def __end_delete_dlg(self, *args, **kwargs) -> bool:
        success = kwargs["success"]
        if success:
            filename = None
            if self.__focused_file_index + 1 in range(len(self.__files)):
                filename = self.__files[self.__focused_file_index + 1]
            elif self.__focused_file_index - 1 in range(len(self.__files)):
                filename = self.__files[self.__focused_file_index - 1]

            # Close current dialog box.
            self._current_dialog = None
            # Refresh the current folder and focus on filename
            self.__init_new_current_folder_and_build_braille_line(
                self.__current_folder, focused_file=filename
            )
        else:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("error during deletion."), action=self._exec_cancel_dialog
            )
        # End of thread.
        self.__delete_thread = None
        return True

    def _update_in_progress(self, label):
        if self._current_dialog:
            if isinstance(self._current_dialog, ui.UiInfoDialogBox):
                self._current_dialog.change_label(label)
            else:
                # Need to re-instanciate ui.UiInfoDialogBox after a "yes / no" ui.UiMessageDialogBox
                self._current_dialog = ui.UiInfoDialogBox(message=label)

    def __end_delete(self, *args, **kwargs):
        log.info("_end_delete() called !")
        self._put_in_function_queue(FunctionId.FUNCTION_END_DELETE, *args, **kwargs)

    # Called when shutdown occurs.
    # Unmount the USB flash drive if there is one that has been mounted.
    def shutdown(self, focused):
        self._shutdown_processing = True
        FileManagerApp.unmount_all_usb_flash_drive()
        if Settings().data["explorer"]["empty_bluetooth_shutdown"]:
            os.system("sudo rm {}/*".format(FileManager.get_bluetooth_path()))
        if Settings().data["explorer"]["empty_trash_shutdown"]:
            self._exec_empty_the_trash_yes_dialog()
        self._shutdown_processing = False

    def shutdown_ended(self):
        # By default : shutdown process is ended for application.
        return not self._shutdown_processing

    @staticmethod
    def unmount_all_usb_flash_drive() -> bool:
        usb_drives = FileManagerApp.__list_dir(FileManager.get_usb_flash_drive_path())
        if len(usb_drives):
            for usb_drive in usb_drives:
                FileManager.umount_safely_usb_flash_drive(usb_drive)
        return (
            len(FileManagerApp.__list_dir(FileManager.get_usb_flash_drive_path())) == 0
        )

    def on_timer(self):
        # Auto refresh only when the usb stick list is displayed
        if str(self.__current_folder) == str(FileManager.get_usb_flash_drive_path()):
            # Do nothing in menu or dialogbox
            if self._current_dialog is None and not self._in_menu:
                old_usb_stick = self.__files[self.__focused_file_index]
                old_usb_stick_list = self.__files
                old_start_pos = self.__ui_line.braille_display.get_start_pos()
                # Rebuild the list file (ie the list of the usb stick). Note that after this function
                # the self.__focused_file_index = 0 and the braille offset will be on the start of the folder name.
                self._exec_actualize()

                # If a new stick is detected show it
                if len(old_usb_stick_list) < len(self.__files):
                    # Set self.__focused_file_index to the new detected usb stick
                    for index, usb_stick in enumerate(self.__files):
                        if usb_stick not in old_usb_stick_list:
                            self.__focused_file_index = index
                            # Offset the braille line to the name of the usb stick (-1 is invalid value and will have no
                            # effect when self.__ui_line.braille_display.set_start_pos(old_start_pos) will be called.
                            old_start_pos = -1
                            break
                # self._exec_actualize() set self.__focused_file_index to 0, but we want to the user to be able to
                # read the usb stick info (if more than 1 usb stick plugged)
                else:
                    # Set self.__focused_file_index to the correct usb stick
                    for index, usb_stick in enumerate(self.__files):
                        if usb_stick == old_usb_stick:
                            self.__focused_file_index = index
                            break

                # Build the braille line (according to self.__focused_file_index)
                self.__build_braille_line()
                # Set the old braille offset
                self.__ui_line.braille_display.set_start_pos(old_start_pos)
