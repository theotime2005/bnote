"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import time
import threading
from bnote.apps.fman.file_manager import FileManager, Trash

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, RESTORE_FROM_TRASH_THREAD_LOG

log = ColoredLogger(__name__)
log.setLevel(RESTORE_FROM_TRASH_THREAD_LOG)


class RestoreFromTrashThread(threading.Thread):
    def __init__(
        self, files, on_error=None, on_ask_replace=None, on_progress=None, on_end=None
    ):
        threading.Thread.__init__(self)
        self.__running = False
        self.__wait = False
        self.__replace_answer_yes = False
        self.__replace_answer_to_all = False
        self.__files = files
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
        log.info("RestoreFromTrashThread running...")
        count = FileManager.files_and_folders_count(self.__files)
        index = 0
        restore_from_trash_success = False
        while self.__running:
            for file in self.__files:
                original_file = Trash.original_file(file)
                if self.__on_progress is not None:
                    index += 1
                    self.__on_progress(
                        operation="restore_from_trash",
                        filename=original_file,
                        current_progress=index,
                        max_progress=count,
                    )

                # Separate path and filename
                head, tail = os.path.split(file)
                log.info("file={}".format(file))
                log.info("head={}".format(head))
                log.info("original_file={}".format(original_file))

                if os.path.isfile(file) and not os.path.exists(
                    os.path.dirname(original_file)
                ):
                    log.info(
                        "il faut créer le dossier {}".format(
                            os.path.dirname(original_file)
                        )
                    )
                    log.info(
                        "os.path.splitdrive()={}".format(
                            os.path.splitdrive(original_file)
                        )
                    )
                    dest_path = os.path.sep
                    for folder in os.path.dirname(original_file).split(os.path.sep):
                        dest_path = os.path.join(dest_path, folder)
                        log.info("folder={} dest_path={}".format(folder, dest_path))
                        if not os.path.exists(dest_path):
                            log.info("path not exist : {}".format(dest_path))
                            FileManager.create_folder(dest_path)

                if (
                    os.path.exists(original_file)
                    and not self.__replace_answer_yes
                    and self.__replace_answer_to_all
                ):
                    # user already said he does't want to overwrite the files.
                    log.info(
                        "ignore restore from trash for already existing file {}".format(
                            file
                        )
                    )
                else:
                    if (
                        os.path.exists(original_file)
                        and not self.__replace_answer_to_all
                    ):
                        # Open a dialog box to ask replace yes / no / yes_to_all / no_to_all
                        self.__replace_answer_yes = False
                        self.__replace_answer_to_all = False
                        self.__on_ask_replace(
                            operation="restore_from_trash",
                            filename=original_file,
                            is_cancelable=False,
                        )
                        self.__wait = True
                        while self.__wait:
                            time.sleep(0.1)

                    # The restore from trash can be done if destination file does not exists or if user has already
                    # answer Yes (you can replace it)
                    if not os.path.exists(original_file) or self.__replace_answer_yes:

                        # Restore the file
                        FileManager.move(file, original_file, dirs_exist_ok=True)

                        # Delete trashinfo if needed.
                        if not os.path.dirname(
                            str(file).replace(
                                str(Trash.get_trash_path()) + os.path.sep, ""
                            )
                        ):
                            log.info(
                                "Delete the trashinfo file {}".format(
                                    Trash.trash_info_file(file)
                                )
                            )
                            FileManager.delete_file(
                                Trash.trash_info_file(file), move_to_trash=False
                            )
                        else:
                            log.info("Pas de trashinfo à effacer....")

                index += 1

            restore_from_trash_success = True
            if self.__on_end is not None:
                self.__on_end(
                    operation="restore_from_trash", success=restore_from_trash_success
                )

            self.__running = False
