"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import logging

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
    FORMAT = "[%(levelname)-18s$BOLD:%(module)s:%(funcName)s$RESET]  %(message)s ($BOLD%(filename)s:%(lineno)d$RESET) pid:%(process)d tid:%(thread)d"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self.setLevel(level)
        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return

# Quand log == 0 => version de production très peu verbeuse (réglage par défaut sur ERROR)
# Quand log == 1 => version de developpement assez peu verbeuse (réglage par défaut sur WARNING)
# En WARNING, on place principalement les résultats des exceptions + la sortie afficheurs braille pour avoir un retour
# pour developpeur quand on ne se lance pas en service).

LOG = 0

if LOG == 0:
    # The log level for each project files => Configuration for application started as service.
    # Cette config ne doit pas être trop verbeuse pour ne pas surcharger /var/log/syslog
    # On règle tous les modules au niveau ERROR
    UI_LOG = logging.ERROR
    BNOTE_ESYS_LOG = logging.ERROR
    BNOTE_LOG = logging.ERROR
    TRANSLATE_LOG = logging.ERROR
    CLIPBOARD_LOG = logging.ERROR
    CRASH_REPORT_LOG = logging.ERROR
    BRAILLE_DEVICE_CHARACTERISTICS_LOG = logging.ERROR
    # bt
    BLUETOOTH_APP_LOG = logging.ERROR
    BT_PROTOCOL_LOG = logging.ERROR
    BT_THREAD_LOG = logging.ERROR
    # braille
    BRAILLE_CONVERTER_LOG = logging.ERROR
    # edt
    EDITOR_APP_LOG = logging.ERROR
    MARKERS_LOG = logging.ERROR
    PARAGRAPH_LOG = logging.ERROR
    PARAGRAPHS_LOG = logging.ERROR
    READ_FILE_LOG = logging.ERROR
    MUSIC_WRITE_FILE_LOG =  logging.ERROR
    # esys
    ESYS_COM_LOG = logging.ERROR
    ESYS_PROTOCOL_LOG = logging.ERROR
    # fman
    BT_TOOLS_LOG = logging.ERROR
    BT_UTIL_LOG = logging.ERROR
    COPY_MOVE_THREAD_LOG = logging.ERROR
    DELETE_THREAD_LOG = logging.ERROR
    FILE_MANAGER_LOG = logging.ERROR
    FILE_MANAGER_APP_LOG = logging.ERROR
    RESTORE_FROM_TRASH_THREAD_LOG = logging.ERROR
    SEND_TO_THREAD_LOG = logging.ERROR
    UNZIP_THREAD_LOG = logging.ERROR
    ZIP_THREAD_LOG = logging.ERROR
    # settings
    SETTING_APP_LOG = logging.ERROR
    # int
    BRAILLE_DISPLAY_LOG = logging.ERROR
    BRAILLE_LINE_LOG = logging.ERROR
    BRAILLE_MENUS_LOG = logging.ERROR
    BRAILLE_OBJECT_LOG = logging.ERROR
    INTERNAL_LOG = logging.ERROR
    KEYBOARD_LOG = logging.ERROR
    QUICK_SEARCH_LOG = logging.ERROR
    BNOTE_APP_LOG = logging.ERROR
    LOU_LOG = logging.ERROR
    UPDATE_LOG = logging.ERROR
    RADIO_LOG = logging.ERROR
    # stm32
    STM32_PROTOCOL_LOG = logging.ERROR
    STM32_THREAD_LOG = logging.ERROR
    # voice
    SYNTHESIS_LOG = logging.ERROR
    WAVE_LOG = logging.ERROR
    # generate_update
    GENERATE_UPDATE_LOG = logging.ERROR
    # math
    MATH_PARSER_LOG = logging.ERROR
    MATH_RESULT_LOG = logging.ERROR
    MATH_MODEL_LOG = logging.ERROR
    # agenda app
    AGENDA_APP_LOG = logging.DEBUG
    # Skeleton app
    SKELETON_APP_LOG = logging.DEBUG
    # braille_learning app
    WRITE_WORD_APP_LOG=logging.DEBUG
    OPERATION_APP_LOG = logging.DEBUG
    # mines app
    MINES_APP_LOG = logging.ERROR
    MASTERMIND_APP_LOG = logging.ERROR
    # radio app
    RADIO_APP_LOG = logging.ERROR
    # mp3 app
    MP3_APP_LOG = logging.ERROR
    # Timer
    TIMER_APP_LOG=logging.ERROR
    # Translator
    TRANSLATOR_APP_LOG = logging.ERROR
    # wifi
    WIFI_LOG = logging.ERROR
    # yaupdater
    YAUPDATER_LOG = logging.INFO

else:
    # The log level for each project files => Configuration for developer.
    UI_LOG = logging.WARNING
    BNOTE_ESYS_LOG = logging.WARNING
    BNOTE_LOG = logging.WARNING
    TRANSLATE_LOG = logging.WARNING
    CLIPBOARD_LOG = logging.WARNING
    CRASH_REPORT_LOG = logging.WARNING
    BRAILLE_DEVICE_CHARACTERISTICS_LOG = logging.WARNING
    # bt
    BLUETOOTH_APP_LOG = logging.WARNING
    BT_PROTOCOL_LOG = logging.WARNING
    BT_THREAD_LOG = logging.WARNING
    # braille
    BRAILLE_CONVERTER_LOG = logging.WARNING
    # edt
    EDITOR_APP_LOG = logging.WARNING
    MARKERS_LOG = logging.WARNING
    PARAGRAPH_LOG = logging.WARNING
    PARAGRAPHS_LOG = logging.WARNING
    READ_FILE_LOG = logging.WARNING
    # esys
    ESYS_COM_LOG = logging.WARNING
    ESYS_PROTOCOL_LOG = logging.WARNING
    # fman
    BT_TOOLS_LOG = logging.WARNING
    BT_UTIL_LOG = logging.WARNING
    COPY_MOVE_THREAD_LOG = logging.WARNING
    DELETE_THREAD_LOG = logging.WARNING
    FILE_MANAGER_LOG = logging.WARNING
    FILE_MANAGER_APP_LOG = logging.WARNING
    RESTORE_FROM_TRASH_THREAD_LOG = logging.WARNING
    SEND_TO_THREAD_LOG = logging.WARNING
    UNZIP_THREAD_LOG = logging.WARNING
    ZIP_THREAD_LOG = logging.WARNING
    # settings
    SETTING_APP_LOG = logging.WARNING
    # int
    BRAILLE_DISPLAY_LOG = logging.WARNING
    BRAILLE_LINE_LOG = logging.WARNING
    BRAILLE_MENUS_LOG = logging.WARNING
    BRAILLE_OBJECT_LOG = logging.WARNING
    INTERNAL_LOG = logging.WARNING
    KEYBOARD_LOG = logging.WARNING
    QUICK_SEARCH_LOG = logging.WARNING
    BNOTE_APP_LOG = logging.WARNING
    LOU_LOG = logging.WARNING
    UPDATE_LOG = logging.WARNING
    RADIO_LOG = logging.DEBUG
    # stm32
    STM32_PROTOCOL_LOG = logging.WARNING
    STM32_THREAD_LOG = logging.WARNING
    # voice
    SYNTHESIS_LOG = logging.WARNING
    WAVE_LOG = logging.ERROR
    # generate_update
    GENERATE_UPDATE_LOG = logging.WARNING
    MATH_PARSER_LOG = logging.WARNING
    MATH_RESULT_LOG = logging.WARNING
    MATH_MODEL_LOG = logging.WARNING
    # skeleton app
    SKELETON_APP_LOG = logging.WARNING
    # braille_learning app
    WRITE_WORD_APP_LOG = logging.WARNING
    OPERATION_APP_LOG=logging.WARNING
    # mines app
    MINES_APP_LOG = logging.WARNING
    MASTERMIND_APP_LOG = logging.WARNING
    # radio app
    RADIO_APP_LOG = logging.WARNING
    # mp3 app
    MP3_APP_LOG = logging.WARNING
    # Timer
    TIMER_APP_LOG = logging.WARNING
    # Translator
    TRANSLATOR_APP_LOG = logging.ERROR
    # wifi
    WIFI_LOG = logging.WARNING
    # yaupdater
    YAUPDATER_LOG = logging.INFO

