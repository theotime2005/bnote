"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import re
import unicodedata

# Setup the logger for this file
from .colored_log import ColoredLogger, FIND_PARAMETERS_LOG

log = ColoredLogger(__name__, level=FIND_PARAMETERS_LOG)


class FindParameters:
    # This line defines punctuation
    PUNCTUATIONS = ''' ,.\\{\\}\\[\\]<>!\\?;:\\(\\)'"/\\+\\*\\^~'''

    def __init__(self, find_seq, ignore_case, mask_accents, entire_word, replace_seq=""):
        self.edit_seq = find_seq
        self.__ignore_case = ignore_case
        self.__mask_accents = mask_accents
        self.__entire_word = entire_word
        self.replace_seq = replace_seq

        # Construct seq to find (lower case, no accent...) and check its validity.
        self.__find_seq = find_seq
        self.__invalid_seq = False
        if ignore_case:
            self.__find_seq = self.__convert_upper_case(self.__find_seq)
        if mask_accents:
            self.__find_seq = self.__convert_accents(self.__find_seq)
        if entire_word:
            # Check no separator in the word to search.
            matches = re.search("[{0}]".format(FindParameters.PUNCTUATIONS), self.__find_seq)
            if matches:
                log.warning("invalid seq.")
                self.__invalid_seq = True
        log.info(self.__find_seq)

    # Accessors
    def is_valid(self):
        return not self.__invalid_seq

    def is_ignore_case(self):
        return self.__ignore_case

    def is_mask_accents(self):
        return self.__mask_accents

    def is_entire_word(self):
        return self.__entire_word

    # Text reconditioning
    @staticmethod
    def __convert_upper_case(text):
        return text.lower()

    @staticmethod
    def __convert_accents(text):
        return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

    # Search the find.seq in text from index
    def find(self, text, index):

        res_index = -1
        seg = text[index: len(text)]
        if self.__ignore_case:
            seg = self.__convert_upper_case(seg)
        if self.__mask_accents:
            seg = self.__convert_accents(seg)
        if self.__entire_word:
            # This line defines punctuation
            matches = re.search('[{0}]({1})[{0}]'.format(FindParameters.PUNCTUATIONS, self.__find_seq), seg)
            if matches:
                # Add 1 to mark the first character of the word, not the separator before the word.
                res_index = matches.start() + 1
        else:
            res_index = seg.find(self.__find_seq)

        if res_index != -1:
            # Add index of search's start too the index of search in substring.
            res_index += index

        return res_index

    # For print()
    def __repr__(self):
        text = "Find Parameters"
        # Display all lines.
        text += "seq=<{}>".format(self.edit_seq)
        text += " ignore_upper_case<{}>".format(self.is_ignore_case())
        text += " mask accents<{}>".format(self.is_mask_accents())
        text += " entire word<{}>".format(self.is_entire_word())
        return text
