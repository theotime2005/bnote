"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import time
import threading
from bnote.apps.fman.file_manager import FileManager
from bnote.debug.colored_log import ColoredLogger, COPY_MOVE_THREAD_LOG

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(COPY_MOVE_THREAD_LOG)


class CopyMoveThread(threading.Thread):
    def __init__(
        self,
        files,
        to,
        copy=True,
        on_error=None,
        on_ask_replace=None,
        on_progress=None,
        on_end=None,
    ):
        threading.Thread.__init__(self)
        self.__running = False
        self.__wait = False
        self.__replace_answer_yes = False
        self.__replace_answer_to_all = False
        self.__files = files
        self.__destination = to
        self.__is_copy = copy
        self.__on_error = on_error
        self.__on_ask_replace = on_ask_replace
        self.__on_progress = on_progress
        self.__on_end = on_end

    def terminate(self):
        self.__running = False

    def replace_answer(self, yes, to_all):
        self.__replace_answer_yes = yes
        self.__replace_answer_to_all = to_all
        self.__wait = False

    def run(self) -> None:
        self.__running = True
        log.info("CopyMoveThread running...")
        count = FileManager.files_and_folders_count(self.__files)
        index = 0
        while self.__running:
            for file in self.__files:
                if self.__on_progress is not None:
                    index += 1
                    if self.__is_copy:
                        self.__on_progress(
                            operation="copy",
                            filename=file,
                            current_progress=index,
                            max_progress=count,
                        )
                    else:
                        self.__on_progress(
                            operation="move",
                            filename=file,
                            current_progress=index,
                            max_progress=count,
                        )

                dst_file = os.path.join(self.__destination, os.path.basename(file))

                if (
                    os.path.exists(dst_file)
                    and not self.__replace_answer_yes
                    and self.__replace_answer_to_all
                ):
                    # user already said he doesn't want to overwrite the files.
                    log.info(
                        "ignore copy/move for all the existing files {}".format(file)
                    )
                else:
                    if os.path.exists(dst_file) and not self.__replace_answer_to_all:
                        # Open a dialog box to ask replace yes / no / yes_to_all / no_to_all
                        self.__replace_answer_yes = False
                        self.__replace_answer_to_all = False
                        if self.__is_copy:
                            self.__on_ask_replace(
                                operation="copy", filename=dst_file, is_cancelable=False
                            )
                        else:
                            self.__on_ask_replace(
                                operation="move", filename=dst_file, is_cancelable=False
                            )
                        self.__wait = True
                        while self.__wait:
                            time.sleep(0.1)

                    # The copy/move can be done if destination file does not exists
                    # or if user has already answer Yes (you can replace it)
                    if not os.path.exists(dst_file) or self.__replace_answer_yes:
                        try:
                            # copy / move the file
                            if self.__is_copy:
                                FileManager.copy(file, dst_file, dirs_exist_ok=True)
                            else:
                                FileManager.move(file, dst_file)
                        except OSError as error:
                            log.warning("OSError={}".format(error))
                            pass

                index += 1

            if self.__on_end is not None:
                if self.__is_copy:
                    self.__on_end(operation="copy")
                else:
                    self.__on_end(operation="move")

            self.__running = False
