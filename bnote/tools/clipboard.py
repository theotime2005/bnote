"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


from pathlib import Path
from apps.fman.file_manager import FileManager
from debug.colored_log import ColoredLogger, CLIPBOARD_LOG

log = ColoredLogger(__name__)
log.setLevel(CLIPBOARD_LOG)


CLIP_FILE = ".bnote_clipboard.txt"


def copy(text):
    file = None
    try:
        log.info("Clipboard copy : {}".format(text))
        file = open(FileManager.get_root_path() / Path(CLIP_FILE), 'w')
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
        file = open(FileManager.get_root_path() / Path(CLIP_FILE), 'r')
        text = file.read()
        log.info("Clipboard paste : {}".format(text))
    except IOError as error:
        log.warning("Write file IO exception:{}".format(error))
    finally:
        if file:
            file.close()
        return text
