"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, QUICK_SEARCH_LOG

log = ColoredLogger(__name__)
log.setLevel(QUICK_SEARCH_LOG)

RESET_SEARCH_TIME_MS = 1000


# QuickSearch implements an incremental search :
#
# A call back function that will be used to do the search must be defined in __init__()
# This call back function receive self.__quick_search_value as parameter and must returns a tuple (bool, object()).
# The bool indicates success of the search and the object() is whatever you need.
# This tuple will be return by do_quick_search().
#
# - Call do_quick_search(character) from input_character to do an incremental quick search. The searched text is the
# accumulation of previous characters + the character (except if do_quick_search(character)
# is call after a time longer than self.__reset_search_time_ms. In this case the searched text is only character.
# This mechanism can be ignored with the param clear_quick_search_if_timeout=False
# - Call do_quick_search_again() to restart the same search (on F3 key for instance).
# - Call clear() to clear the current search (on ESC key for instance)
# - Call clear_time_previous_char() to set the self.__time_previous_char to a time older than
# current_time - self.__reset_search_time_ms. Thus the self.__quick_search_value will be empty on the next call to
# do_quick_search() but not to the next call to do_quick_search_again()


class QuickSearch:
    def __init__(
        self, quick_search_function, reset_search_time_ms=RESET_SEARCH_TIME_MS
    ):
        # The str that is passed to self.__quick_search_function for quick search
        self.__quick_search_value = ""
        # The quick search callback function to call.
        self.__quick_search_function = quick_search_function
        # Time when previous char has been input in ms
        self.__time_previous_char = int(time.time_ns() / 1000000)
        # The self.__quick_search_value is cleared if more than self.__reset_search_time_ms elapsed
        # since last do_quick_search().
        self.__reset_search_time_ms = reset_search_time_ms

    def clear(self) -> (bool, object()):
        self.__quick_search_value = ""
        return True, None

    def clear_time_previous_char(self):
        self.__time_previous_char = (
            int(time.time_ns() / 1000000) - self.__reset_search_time_ms
        )

    def do_quick_search(self, character, clear_quick_search_if_timeout=True) -> bool:
        new_time = int(time.time_ns() / 1000000)

        # Reset the quick search value after __quick_search_value sec
        if (
            clear_quick_search_if_timeout
            and new_time - self.__time_previous_char > self.__reset_search_time_ms
        ):
            self.__quick_search_value = ""

        self.__quick_search_value = "".join((self.__quick_search_value, character))
        self.__time_previous_char = new_time

        # Call the quick search call back function
        if self.__quick_search_function is not None:
            success = self.__quick_search_function(self.__quick_search_value)
            return success

        return False

    def do_quick_search_again(self) -> (bool, object()):
        return self.do_quick_search(character="", clear_quick_search_if_timeout=False)
