"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import logging

EDITOR_LOG = logging.ERROR
FIND_PARAMETERS_LOG = logging.ERROR
EDITOR_MARKERS_LOG = logging.ERROR
EDITOR_PARAGRAPH_LOG = logging.ERROR
EDITOR_UNDO_REDO_LOG = logging.ERROR
EDITOR_WRITE_FILE_LOG = logging.ERROR
ODT_LOG = logging.ERROR
MBE_LOG = logging.ERROR
READ_FILE_LOG = logging.ERROR
READ_BRF_FILE_LOG = logging.ERROR
READ_DOCX_FILE_LOG = logging.ERROR
READ_EPUB_FILE_LOG = logging.ERROR
READ_ODT_FILE_LOG = logging.ERROR
READ_PDF_FILE_LOG = logging.ERROR
READ_MBE_FILE_LOG = logging.ERROR
READ_WRITE_SPECIFIC_FILE_LOG = logging.ERROR
READ_XLSX_FILE_LOG = logging.ERROR
EDITOR_DAISY_LOG = logging.ERROR

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
WHITE_SEQ = "\033[0;97m"


def formatter_message(message, use_color=True):
    if use_color:
        # message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", WHITE_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        level_color = None
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            level_color = COLOR_SEQ % (30 + COLORS[levelname])
            levelname_color = level_color + levelname + RESET_SEQ
            record.levelname = levelname_color
        message = record.msg
        if self.use_color and level_color:
            message_color = ''.join((level_color, str(message), RESET_SEQ))
            record.msg = message_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    # FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    # FORMAT = "[%(levelname)-18s$BOLD:%(module)s:%(funcName)s$RESET]  %(message)s ($BOLD%(filename)s:%(lineno)d$RESET)"
    FORMAT = "[edt%(levelname)-18s$BOLD:%(module)s:%(funcName)s$RESET]  %(message)s ($BOLD%(filename)s:%(lineno)d$RESET) pid:%(process)d tid:%(thread)d"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self.setLevel(level)
        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return
