"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import logging

MATH_LOG = logging.ERROR
MATH_RESULT_LOG = logging.ERROR

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
WHITE_SEQ = "\033[0;97m"

def formatter_message(message, use_color = True):
    if use_color:
        #message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
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
    def __init__(self, msg, use_color = True):
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
            message_color = level_color + message + RESET_SEQ
            record.msg = message_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):

    # FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    # FORMAT = "[%(levelname)-18s$BOLD:%(module)s:%(funcName)s$RESET]  %(message)s ($BOLD%(filename)s:%(lineno)d$RESET)"
    FORMAT = "[math%(levelname)-18s$BOLD:%(module)s:%(funcName)s$RESET]  %(message)s ($BOLD%(filename)s:%(lineno)d$RESET) pid:%(process)d tid:%(thread)d"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self.setLevel(level)
        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

