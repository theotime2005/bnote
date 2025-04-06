"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import threading
import zipfile
from bnote.apps.fman.file_manager import FileManager, Trash

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, ZIP_THREAD_LOG

log = ColoredLogger(__name__)
log.setLevel(ZIP_THREAD_LOG)


class ZipThread(threading.Thread):
    def __init__(
        self,
        files,
        zip_file_name,
        base_folder=None,
        on_error=None,
        on_progress=None,
        on_end=None,
        zip_hidden_file=False,
        exclude_files=(),
        operation="zip",
    ):
        threading.Thread.__init__(self)
        self.__running = False
        # FIXME : Vérifier que c'est une liste de fichier
        log.info("type(files)={}".format(type(files)))
        self.__files = files
        self.__exclude_files = exclude_files  # Les fichiers à exclure du zip
        self.__zip_file_name = zip_file_name
        self.__zip_file = None
        self.__base_folder = base_folder
        if self.__base_folder is None:
            self.__base_folder = FileManager.get_root_path()
        self.__on_error = on_error
        self.__on_progress = on_progress
        self.__on_end = on_end
        self.__zip_hidden_file = zip_hidden_file
        self.__operation = operation
        self.__count = FileManager.files_and_folders_count(
            self.__files, self.__exclude_files
        )
        log.info(f"count{self.__count}")
        self.__index = 0

    def terminate(self):
        self.__running = False

    def run(self) -> None:
        self.__running = True
        log.info("ZipThread running...")
        zip_success = False
        try:
            self.__zip_file = zipfile.ZipFile(self.__zip_file_name, "w")
            while self.__running:
                for file in self.__files:
                    if file not in self.__exclude_files and (
                        file != self.__zip_file_name
                    ):
                        self.__append_to_zip_file(file)

                self.__zip_file.close()
                self.__running = False

            zip_success = True
        except FileNotFoundError:
            pass
        finally:
            if self.__on_end is not None:
                self.__on_end(
                    operation=self.__operation,
                    success=zip_success,
                    filename=self.__zip_file_name,
                )

    def __append_to_zip_file(self, filename):
        # The bluetooth symlink must be ignored.
        if filename == FileManager.get_bluetooth_path():
            return
        # The backup symlink must be ignored.
        if filename == FileManager.get_backup_path():
            return
        # The trash symlink must be ignored.
        if filename == Trash.get_trash_path():
            return
        # The crash symlink must be ignored.
        if filename == FileManager.get_crash_path():
            return
        # The usb_flash_drive symlink must be ignored.
        if filename == FileManager.get_usb_flash_drive_path():
            return

        if self.__on_progress is not None:
            self.__index += 1
            self.__on_progress(
                operation=self.__operation,
                filename=filename,
                current_progress=self.__index,
                max_progress=self.__count,
            )

        arc_filename = str(filename).replace(str(self.__base_folder), "")
        # log.info("filename = {} arc_filename = {}".format(filename, arc_filename))
        # time.sleep(1)
        if arc_filename != "":
            self.__zip_file.write(filename, arcname=arc_filename)
        if os.path.isdir(filename):
            files = FileManager.listdir(
                filename, hide_hidden_file=not self.__zip_hidden_file
            )
            for file in files:
                if file not in self.__exclude_files:
                    self.__append_to_zip_file(file)
