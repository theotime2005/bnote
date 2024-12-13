"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import shlex
import subprocess
import threading
import time
from bnote.apps.fman.file_manager import FileManager
from bnote.apps.fman.zip_thread import ZipThread
from bnote.tools.bt_util import find_opush_channel
from bnote.debug.colored_log import ColoredLogger, SEND_TO_THREAD_LOG

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(SEND_TO_THREAD_LOG)


class SendToThread(threading.Thread):
    def __init__(
        self,
        files,
        machine,
        to_mac_address,
        on_error=None,
        on_progress=None,
        on_end=None,
    ):
        threading.Thread.__init__(self)
        self.__running = False
        self.__wait = False
        self.__replace_answer_yes = False
        self.__replace_answer_to_all = False
        # FIXME : Vérifier que c'est une liste de fichier
        log.info("type(files)={}".format(type(files)))
        self.__files = files
        self.__machine = machine
        self.__to_mac_address = to_mac_address
        self.__on_error = on_error
        self.__on_progress = on_progress
        self.__on_end = on_end

    def terminate(self):
        self.__running = False

    def run(self) -> None:
        self.__running = True
        log.info("SendToThread running...")
        count = len(self.__files)
        send_to_success = False
        zip_file = None
        while self.__running:
            file_to_send = self.__files[0].resolve()
            if count > 1 or (count == 1 and self.__files[0].is_dir()):
                file_to_send = FileManager.get_tmp_path() / (
                    self.__files[0].resolve().name + ".zip"
                )
                zip_thread = ZipThread(self.__files, file_to_send)
                zip_thread.start()
                zip_thread.join()

            if self.__on_progress is not None:
                self.__on_progress(
                    operation="send to",
                    filename=file_to_send,
                    current_progress=50,
                    max_progress=100,
                )

            # Get the channel for OPUSH service.
            channel = find_opush_channel(self.__to_mac_address)

            # Ligne de commande pour un W10
            command_line = 'obexftp -b {} -B {} -p "{}"'.format(
                self.__to_mac_address, channel, file_to_send
            )
            obexftp_results, error = self.send(command_line)
            log.info("obexftp =>{}".format(obexftp_results))

            if error.find("failed: send UUID") != -1:
                time.sleep(2)
                # Ligne de commande pour un système android ou W7
                command_line = 'obexftp -b {} --uuid none -B {} -p "{}"'.format(
                    self.__to_mac_address, channel, file_to_send
                )
                obexftp_results, error = self.send(command_line)
                log.info("obexftp =>{}".format(obexftp_results))

            # Si l'utilisateur n'est pas en mode "Recevoir un fichier" sur le PC sous W10, on obtient :
            # [INFO: send_to_thread:run]  obexftp =>
            # [INFO: send_to_thread:run]  obexftp: error = Connecting...failed: connect
            # The user may have rejected the transfer: Connection refused
            # Sinon, on obtient (juste avant que l'utilisateur ne voit la BDD "Enregistrer sous" sur le PC):
            # [INFO: send_to_thread:run]  obexftp =>
            # [INFO: send_to_thread:run]  obexftp: error = Connecting..\done
            # Sending "/home/pi/bnote-documents/bluetooth/test1.txt"... / done
            # Disconnecting.. - done

            # log.info("type(err)={}".format(type(err)))
            if error.count("done") == 3:
                send_to_success = True

            log.info("err.count(done) => {}".format(error.count("done")))
            log.info("send_to_success={}".format(send_to_success))

            # Remarque : Il n'est pas possible d'enchainer la copie de plusieurs fichiers...
            # Il faudra peut être fournir une fonction "zip & send to" quand plusieurs fichiers sont sélectionnés...

            # Si un fichier zip a été créé, on le supprime...
            if zip_file is not None:
                os.remove(file_to_send)

            if self.__on_end is not None:
                self.__on_end(
                    operation="send to",
                    machine=self.__machine,
                    send_to_success=send_to_success,
                    filename=file_to_send,
                )

            self.__running = False

    def send(self, command_line):
        log.info("command_line={}".format(command_line))
        args = shlex.split(command_line)
        log.info("args={}".format(args))
        x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        x.wait()
        obexftp_results = x.stdout.read().decode("utf-8")
        log.info("obexftp =>{}".format(obexftp_results))
        error = x.stderr.read().decode("utf-8")
        if error != "":
            log.info("obexftp : error={}".format(error))
            x.terminate()

        return obexftp_results, error
