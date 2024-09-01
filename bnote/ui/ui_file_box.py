"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from pathlib import Path

from bnote.apps.fman.file_manager import FileManager, Trash
from bnote.debug.colored_log import ColoredLogger, UI_LOG
# Set up the logger for this file
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_file_manager_tools import UiFileManagerTools
from .ui_list_box import UiListBox

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiFileBox(UiListBox, UiFileManagerTools):
    """
    This object allows to navigate in a file tree.
    """

    def __init__(self, root, suffix_filter, folder_only=None):
        """
        root is the default folder.
        suffix_filter is the list of file extension allowed ( example : (".txt", ".pdf") )
            if None all files are displayed.
        folder_only is True indicates only folders will be displayed.
        """
        self.braille_type = Settings().data['system']['braille_type']
        self.root = Path(root)
        self.__current_folder = self.root
        self.suffix_filter = suffix_filter
        self.folder_only = folder_only
        self.__focused_file_index = 0
        super().__init__(
            name=self._ui_file_name(self.braille_type, self.__current_folder),
            value=('file', [_("empty directory...")]),
            current_index=self.__focused_file_index
        )
        self.__create_ui_list()

    def __create_ui_list(self, focused_folder=None):
        """
        Update the ui list.
        """
        self.__files = self.__create_items_list()
        file_names = []
        focused_index = 0
        for index, (file_path, file) in enumerate(self.__files):
            if file_path == focused_folder:
                focused_index = index
            file_names.append(file)
        if len(file_names) == 0:
            focused_index = -1
        self.__focused_file_index = focused_index
        self.set_list(file_names, focused_index)

    def __create_items_list(self):
        """
        Construct the list of folders/files of self.current_folder
        Returns (file_path, file_name)
        """
        # Reset the focused item that will be presented on the BrailleLine
        self.__focused_file_index = 0
        # If something is wrong (maybe user remove some folders from outside bnote app), we must recover situation
        if not self.__current_folder.exists():
            self.__current_folder = FileManager.get_root_path()
        try:
            # Build the files list
            files = self.__list_dir(self.__current_folder)
        except IOError:
            # Fix le crash si l'utilisateur a arraché une clef USB sans avoir fait "ejecter la clef"
            files = []
        # if len(files) == 0:
        #     files.append((Path(_("empty directory...")), _("empty directory...")))
        return files

    # Get the list dir for the wanted path.
    def __list_dir(self, path, hide_hidden_file=True):
        user_files = []

        exclude_list = [FileManager.get_root_path(), FileManager.get_backup_path(), FileManager.get_bluetooth_path(),
                        Trash.get_trash_path(), FileManager.get_crash_path(), FileManager.get_usb_flash_drive_path()]

        files = FileManager.listdir(path, hide_hidden_file=hide_hidden_file)
        if files is not None:
            for file in files:
                if file not in exclude_list:
                    if file.is_dir():
                        user_files.append((file, self._ui_file_name(self.braille_type, file)))
                    elif file.is_file():
                        log.info(f"{file.name=}-{file.suffix=}")
                        if not self.folder_only and (self.suffix_filter is None or file.suffix in self.suffix_filter):
                            # Add to list only the file with suffix in suffix_filter list.
                            user_files.append((file, self._ui_file_name(self.braille_type, file)))
        return user_files

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        log.info(f"input_command on edit box {self._name}")
        switcher = {
            Keyboard.KeyId.KEY_CARET_RIGHT: self.__child,
            Keyboard.KeyId.KEY_CARET_LEFT: self.__parent,
        }
        func = switcher.get(key_id, None)
        if func is not None:
            treated, in_menu = func()
            self.ask_update_braille_display()
            return treated, in_menu
        log.warning("No command defined for {}".format(key_id))
        return super().exec_command(modifier, key_id)

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this bramigraph key.
        :param modifier: keyboard modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        kwargs = Keyboard.decode_modifiers(modifier)
        if kwargs['alt']:
            # alt+key not treated.
            return False, True
        switcher = {
            Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: self.__child,
            Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: self.__parent,
        }
        func = switcher.get(bramigraph, None)
        if func is not None:
            treated, in_menu = func()
            self.ask_update_braille_display()
            return treated, in_menu
        log.warning("No function for bramigraph file defined for {}".format(bramigraph))
        return super().exec_bramigraph(modifier, bramigraph)

    def __parent(self):
        if self.__current_folder != self.root:
            focused_folder = self.__current_folder
            self.__current_folder = self.__current_folder.parent
            self.__create_ui_list(focused_folder)
        return True, True

    def __child(self):
        if self._current_index != -1:
            # Not empty list.
            file_path, file = self.__files[self._current_index]
            if not file_path.is_file():
                # Update
                self.__current_folder = file_path
                self.__create_ui_list()
        return True, True

    def get_value(self):
        if self._current_index == -1:
            # Empty list.
            if self.extra_parameters:
                # When extra parameter defined, return ui object itself.
                return self._value_id, self
            else:
                return self._value_id, None
        file_path, file = self.__files[self._current_index]
        if self.extra_parameters:
            # When extra parameter defined, return ui object itself.
            return self._value_id, self
        else:
            return self._value_id, file_path
