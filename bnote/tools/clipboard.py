"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from pathlib import Path
from bnote.apps.fman.file_manager import FileManager
from bnote.debug.colored_log import ColoredLogger, CLIPBOARD_LOG

log = ColoredLogger(__name__)
log.setLevel(CLIPBOARD_LOG)


CLIP_FILE = ".bnote_clipboard.txt"


def copy(text):
    file = None
    try:
        log.info("Clipboard copy : {}".format(text))
        file = open(FileManager.get_root_path() / Path(CLIP_FILE), "w")
        file.write(text)
    except IOError as error:
        log.warning("Write file IO exception:{}".format(error))
    finally:
        if file:
            file.close()


def paste():
    text = None
    file = None
    try:
        file = open(FileManager.get_root_path() / Path(CLIP_FILE), "r")
        text = file.read()
        log.info("Clipboard paste : {}".format(text))
    except IOError as error:
        log.warning("Write file IO exception:{}".format(error))
    finally:
        if file:
            file.close()
        return text
