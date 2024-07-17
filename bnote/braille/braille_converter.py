"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from bnote.braille.lou import Lou
from bnote.tools.singleton_meta import SingletonMeta

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, BRAILLE_CONVERTER_LOG
log = ColoredLogger(__name__, level=BRAILLE_CONVERTER_LOG)


class BrailleConverter(metaclass=SingletonMeta):

    def __init__(self):
        self.lou = {}
        self.default_country = None

    def set_default_country(self, country):
        self.default_country = country

    def _instantiate(self, country):
        if not (country in self.lou.keys()):
            self.lou[country] = Lou(country)
        return self.lou[country]

    def instance(self, country):
        """
        Return the Lou instance according to the country ('fr_FR' for french)
        """
        return self._instantiate(country)

    def text_to_grade(self, text, braille_language, braille_type, cursor=0) -> (str, [int] or None, [int] or None, int):
        """
            Translate a text to braille text with 2 index list and an int.
            Args:
             text : (str) The string to convert
             braille_language : (str) 'fr_FR' for french translation
             braille_type : 'grade0', 'grade1', 'grade2' or 'math'
             cursor : (int) The cursor position (based 0)
            Returns:
             str the converted string
             [int] First index list is the position in converted string for each char in origianl string.
             [int] Second index is the position in original string of each char in converted string.
             int The position of input caret in converted string (based 0)
            Example : '¨bonjour chez vous !' cursor=5 return
             ('¨bj àz v „!',
             [0, 0, 0, 7, 8, 8, 12, 13, 17, 18, 18],
             [0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 6, 7, 7, 7, 7, 8, 9],
             6)
        """
        lou = self._instantiate(braille_language)
        return lou.text_to_grade(text, braille_type, cursor)

    def grade_to_text(self, braille_text, braille_language, braille_type, cursor=0) -> (str, [int] or None, [int] or None, int):
        """
            Translate a braille text to a text with 2 index list and an int.
            Args:
             braille_text: The braille text (ex: "abc")
             braille_language : (str) 'fr_FR' for french translation
             braille_type: 'grade0', 'grade1', 'grade2' or 'math'
             cursor: (int) The cursor position (based 0)
            Returns:
             str the converted string
             [int] First index list is the position in converted string for each char in origianl string.
             [int] Second index is the position in original string of each char in converted string.
             int The position of input caret in converted string (based 0)
        """
        lou = self._instantiate(braille_language)
        return lou.grade_to_text(braille_text, braille_type, cursor)

    def __lou_from_country(self, country):
        if country is None:
            country = self.default_country
        return self._instantiate(country)

    def to_dots_8(self, text, country=None) -> str:
        """
        For music only !
        """
        return self.braille_text_to_braille_u28xx(text, country, 'grade0')

    def to_text_8(self, braille, country=None) -> str:
        """
        For music only !
        """
        return self.braille_u28xx_to_braille_text(braille, country, 'grade0')

    def convert_text_to_braille_text(self, text, braille_country=None, braille_type=None, caret=None):
        """
        Translate a unicode text string into a braille text string.
        Args:
            text: string of text.
            braille_country: The language (like 'fr_FR')
            braille_type: the type grade0, grade1, grade2 or math.
            caret: tuple (start, end)
        Returns:
            string of braille text, each character corresponding to a braille comb.
            caret (start, end) on the string of braille text.
        """
        lou = self._instantiate(braille_country)
        return lou.convert_text_to_braille_text(text, braille_type, caret)

    def convert_braille_text_to_text(self, braille_text, braille_country=None, braille_type=None, caret=None):
        """
        Translate a braille text string into a unicode text string.
        Args:
            braille_text: string of braille text, each character corresponding to a braille comb.
            braille_country: The language (like 'fr_FR')
            braille_type: the type grade0, grade1, grade2 or math.
            caret: tuple (start, end)
        Returns:
            string of text.
            caret (start, end) on the string of text.
        """
        lou = self._instantiate(braille_country)
        return lou.convert_braille_text_to_text(braille_text, braille_type, caret)

    def braille_text_to_braille_u28xx(self, braille_text, braille_country=None, braille_type=None):
        """
        Convert a string of text to the braille forms (ex: "Abc" -> "'abc", "\u20c0\u2801\u2802\u2803" in french grade1)
        Args:
            braille_text: string of character for each braille cell.
            braille_country: the language (like "fr_FR")
            braille_type: the braille type ('grade0', 'grade1', 'grade2' or math)
        Returns:
            braille_dots: string of x28nn chars.
        """
        lou = self.__lou_from_country(braille_country)
        return lou.braille_text_to_braille_u28xx(braille_text, braille_type)

    def braille_u28xx_to_braille_text(self, braille, braille_country, braille_type):
        """
        Convert a unicode braille string (x28nn chars) into a string.
        Args:
            braille : string of x28nn chars.
            braille_country : the language (like "fr_FR")
            braille_type : the braille type ('grade0', 'grade1', 'grade2' or math)
        Returns:
            text : string of text where all 0x28xx are translated in their characters (0x2801 becomes 'a')
        """
        lou = self.__lou_from_country(braille_country)
        return lou.braille_u28xx_to_braille_text(braille, braille_type)

    def byte_to_unicode_braille(self, dots: bytearray):
        """
        Convert a bytearray of dots into unicode braille string.
        Args:
            dots : bytearray (example (b'\x01\x03\x00")
        Returns:
            str : Unicode string (example: "\u2801,\u2803\u2800"
        """
        lou = self._instantiate(None)
        return lou.byte_to_unicode_braille(dots)

    def unicode_braille_to_byte(self, unicode: str) -> bytearray:
        """
        Convert unicode braille string into a bytearray of dots.
        Args:
            unicode : str unicode string (example: "\u2801,\u2803\u2800"
        Returns:
            bytearray : (example (b'\x01\x03\x00")
        """
        lou = self._instantiate(None)
        return lou.unicode_braille_to_byte(unicode)
