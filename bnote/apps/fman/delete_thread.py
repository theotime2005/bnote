"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import threading
from bnote.apps.fman.file_manager import FileManager
from bnote.debug.colored_log import ColoredLogger, DELETE_THREAD_LOG

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(DELETE_THREAD_LOG)


class DeleteThread(threading.Thread):
    def __init__(self, files, on_error=None, on_progress=None, on_end=None):
        threading.Thread.__init__(self)
        self.__running = False
        self.__wait = False
        self.__files = files
        self.__on_error = on_error
        self.__on_progress = on_progress
        self.__on_end = on_end
        self.__delete_success = True
        self.__count = FileManager.files_and_folders_count(self.__files)
        self.__index = 0

    def terminate(self):
        self.__running = False

    def continue_deletion(self):
        self.__wait = False

    def run(self) -> None:
        self.__running = True
        log.info("DeleteThread running...")
        self.__delete_success = True

        while self.__running:
            for file in self.__files:
                log.info("file={}".format(file))
                try:
                    # time.sleep(1)
                    self.__delete_file(file)

                except OSError as err:
                    log.warning("Error : {}".format(err))

            self.__running = False

        if self.__on_end is not None:
            self.__on_end(operation="deletion", success=self.__delete_success)

    def __delete_file(self, filename):
        # The bluetooth symlink must be ignored.
        if filename == FileManager.get_bluetooth_path():
            return
        # The backup symlink must be ignored.
        if filename == FileManager.get_backup_path():
            return

        if self.__on_progress is not None:
            self.__index += 1
            self.__on_progress(
                operation="delete",
                filename=filename,
                current_progress=self.__index,
                max_progress=self.__count,
            )
            # time.sleep(1)

        if FileManager.delete_file(filename) is False:
            log.info("ERROR with FileManager.delete_file({})".format(filename))
            self.__delete_success = False
