"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import threading
import time
import zipfile
from bnote.apps.fman.file_manager import FileManager
from bnote.debug.colored_log import ColoredLogger, UNZIP_THREAD_LOG

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(UNZIP_THREAD_LOG)


class UnZipThread(threading.Thread):
    def __init__(
        self,
        zip_file_name,
        to,
        on_error=None,
        on_progress=None,
        on_ask_replace=None,
        on_end=None,
    ):
        threading.Thread.__init__(self)
        self.__running = False
        self.__wait = False
        self.__replace_answer_yes = False
        self.__replace_answer_to_all = False
        self.__zip_file_name = zip_file_name
        self.__zip_file = None
        self.__destination = to
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
        log.info("ZipThread running...")
        unzip_success = False
        zip_error = None
        try:
            self.__zip_file = zipfile.ZipFile(self.__zip_file_name, "r")
            info_list = self.__zip_file.infolist()
            log.info("infolist={}".format(info_list))
            index = 0
            count = len(info_list)
            for zip_info in info_list:
                if self.__on_progress is not None:
                    index += 1
                    self.__on_progress(
                        operation="unzip",
                        filename=zip_info.filename,
                        current_progress=index,
                        max_progress=count,
                    )

                if not FileManager.file_to_unzip_already_exists(
                    zip_info.filename, self.__destination
                ) or (self.__replace_answer_yes and self.__replace_answer_to_all):
                    self.__zip_file.extract(zip_info, self.__destination)
                elif (
                    self.__replace_answer_yes is False
                ) and self.__replace_answer_to_all:
                    # user already said he wants not to overwrite file.
                    log.info(
                        "ignore extract for already existing file {}".format(
                            zip_info.filename
                        )
                    )
                else:
                    # Open a dialog box to ask replace yes / no / yes_to_all / no_to_all
                    self.__replace_answer_yes = False
                    self.__replace_answer_to_all = False
                    self.__on_ask_replace(
                        operation="unzip",
                        filename=zip_info.filename,
                        is_cancelable=False,
                    )
                    self.__wait = True
                    while self.__wait:
                        time.sleep(0.1)

                    # If answer is yes copy the file (overwrite it)
                    if self.__replace_answer_yes is True:
                        self.__zip_file.extract(zip_info, self.__destination)

            self.__running = False
            unzip_success = True
        except zipfile.BadZipFile as error:
            zip_error = error
        except OSError as error:
            zip_error = error

        finally:
            if self.__on_end is not None:
                self.__on_end(
                    operation="unzip",
                    success=unzip_success,
                    filename=self.__zip_file_name,
                    destination=self.__destination,
                    error=zip_error,
                )
