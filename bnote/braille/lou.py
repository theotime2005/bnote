"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import threading

from collections import namedtuple

from bnote.braille.louis import liblouis

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, LOU_LOG

log = ColoredLogger(__name__)
log.setLevel(LOU_LOG)


class Lou:
    # [grade1, grade2, dots-8, dots-6]
    language_dict = {
        'ar_LB': (b'ar-ar-g1.utb', b'ar-ar-g2.ctb', b'ar-ar-comp8.utb', b'ar-ar-g1.utb'),
        'fr_FR': (b'fr-bfu-comp6.utb', b'fr-bfu-g2.ctb', b'fr-bfu-comp8.utb', b'fr-bfu-comp6.utb'),
        'el_GR': (b'el.ctb', None, b'el.ctb', b'el.ctb'),
        'en_GB': (b'en-gb-g1.utb', b'en-GB-g2.ctb', b'en-gb-comp8.ctb', b'en-gb-g1.utb'),
        'en_US': (b'en-us-g1.ctb', b'en-us-g2.ctb', b'en-us-comp8.ctb', b'en-us-comp6.ctb'),
        'he_IL': (b'he-IL.utb', None, b'he-IL-comp8.utb', b'he-IL.utb'),
        'sv_SE': (b'Se-Se-g1.utb', None, b'se-se.ctb', b'se-se.ctb'),
        'nb_NO': (b'no-no-g1.ctb', b'no-no-g2.ctb', b'no-no-8dot.utb', b'no-no-g0.utb'),
        'nl_NL': (b'nl-NL-g0.utb', None, b'nl-comp8.utb', b'nl-NL-g0.utb'),
        'nl_BE': (b'nl-NL-g0.utb', None, b'nl-comp8.utb', b'nl-NL-g0.utb'),
        'is_IS': (b'is.tbl', None, b'is.ctb', b'is.tbl'),
        'it_IT': (b'it-it-comp6.utb', None, b'it-it-comp8.utb', b'it-it-comp6.utb'),
        'cs_CZ': (b'cs-g1.ctb', None, b'cs-comp8.utb', b'cs-g1.ctb'),
        'sl_SI': (b'sl-si-g1.utb', None, b'sl-si-comp8.ctb', b'sl-si-g1.utb'),
        'hr_HR': (b'hr-g1.ctb', None, b'hr-comp8.utb', b'hr-g1.ctb'),
        'pt_PT': (b'pt-pt-g1.utb', b'pt-pt-g2.ctb', b'pt-pt-comp8.ctb', b'pt-pt-g1.utb'),
        'pl_PL': (b'Pl-Pl-g1.utb', None, b'pl-pl-comp8.ctb', b'Pl-Pl-g1.utb'),
        'af_ZA': (b'afr-za-g1.ctb', b'afr-za-g2.ctb', b'en-us-comp8.ctb', b'afr-za-g1.ctb'),
        'xh_ZA': (b'xh-za-g1.utb', b'xh-za-g2.ctb', b'en-gb-comp8.ctb', b'xh-za-g1.utb'),
        'zu_ZA': (b'zu-za-g1.utb', b'zu-za-g2.ctb', b'en-gb-comp8.ctb', b'zu-za-g1.utb'),
        'sw_KE': (b'en-gb-g1.utb', b'en-GB-g2.ctb', b'en-gb-comp8.ctb', b'en-gb-g1.utb'),
        'bg_BG': (b'bg.utb', None, b'bg.ctb', b'bg.utb'),
        'ru_RU': (b'ru-ru-g1.ctb', None, b'ru.ctb', b'ru-ru-g1.ctb'),
        'bu_US': (b'en-ueb-g1.ctb', b'en-ueb-g2.ctb', b'en-us-comp8.ctb', b'en-ueb-g1.ctb'),
        'eo_ES': (b'eo.tbl', None, b'Es-Es-G0.utb', b'eo.tbl'),
    }

    language_default = (b'en-us-g1.ctb', b'en-us-g2.ctb', b'en-us-comp8-ext.utb', b'en-us-comp6.ctb')

    # grade1 is used through text_to_grade1 and grade1_to_text but these functions are not called.
    # grade2 is used through text_to_grade2 and grade2_to_text. text_to_grade2 is used by editor to grade2 forward.
    # dots is the table used by to_dots_6 and to_text_8. It is the main 8 dots to character conversion.
    # dots6 is used by to_dots_6 and to_text_6. to_dots_6 is used by .brf file reading
    Tables = namedtuple('tables', ['fr_FR', 'grade1', 'grade2', 'dots', 'dots6'])

    def __init__(self, langue):
        # Mutex for multiple threads access.
        self.lou_mutex = threading.Lock()  # equal to threading.Semaphore(1)
        # absolute path on Pi : /usr/local/share/liblouis/tables
        self.path = b"../tables/"

        table_grade1, table_grade2, table_dots8, table_dots6 = Lou.language_dict.get(langue, Lou.language_default)
        self.tables = Lou.Tables(langue,
                                 grade1=table_grade1, grade2=table_grade2, dots=table_dots8, dots6=table_dots6)

    def is_grade2(self):
        """
        Check if grade2 exists in current language.
        -> None if not grade2.
        """
        return self.tables.grade2

    def text_to_grade1(self, txt, cursor=0):
        with self.lou_mutex:
            return self.__text_to_grade1(txt, cursor)

    def __text_to_grade1(self, txt, cursor=0):
        """
        Convert a text to grade1 txt with 2 index list and an int.
        :param txt: The string to convert
        :param cursor: The cursor position
        :return:
            The converted string
            First index list is the position in converted string for each char in origianl string.
            Second index is the position in original string of each char in converted string.
            The int is the position of input caret in converted string
            Example : '¨bonjour chez vous !' cursor=5 return
            ('¨bj àz v „!',
            [0, 0, 0, 7, 8, 8, 12, 13, 17, 18, 18],
            [0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 6, 7, 7, 7, 7, 8, 9],
            6)
        """
        if self.tables.grade1:
            return liblouis.translate([self.path + self.tables.grade1], txt, None, cursor)
        else:
            return None, None, None, None

    def grade1_to_text(self, txt, cursor=0):
        with self.lou_mutex:
            return self.__grade1_to_text(txt, cursor)

    def __grade1_to_text(self, txt, cursor=0):
        if self.tables.grade1:
            return liblouis.backTranslate([self.path + self.tables.grade1], txt, None, cursor)
        else:
            return None, None, None, None

    def text_to_grade2(self, txt, cursor=0):
        """
        Convert a text to grade1 txt with 2 index list and an int.
        :param txt: The string to convert
        :param cursor: The cursor position
        :return :
            The converted string
            First index list is the position in converted string for each char in origianl string.
            Second index is the position in original string of each char in converted string.
            The int is the position of input caret in converted string
        """
        with self.lou_mutex:
            if self.tables.grade2:
                return liblouis.translate([self.path + self.tables.grade2], txt, None, cursor)
            else:
                # if no grade2, conversion in grade1
                return self.__text_to_grade1(txt, cursor)

    def grade2_to_text(self, txt, cursor=0):
        with self.lou_mutex:
            if self.tables.grade2:
                return liblouis.backTranslate([self.path + self.tables.grade2], txt, None, cursor)
            else:
                # if no grade2, conversion in grade1
                return self.__grade1_to_text(txt, cursor)

    def _to_dots(self, txt, table):
        dots = liblouis.charToDots([self.path + table], txt)
        output_txt = str()
        for c in dots:
            output_txt += chr((ord(c) & 0xFF) + 0x2800)
        log.info('braille:{}'.format(output_txt))
        return output_txt

    def to_dots_6(self, txt):
        """
        Convert a string into an unicode braille string (6 dots) (x28nn chars).
        """
        if not txt:
            # Empty string.
            return txt
        with self.lou_mutex:
            return self._to_dots(txt, self.tables.dots6)

    def to_dots_8(self, txt):
        """
        Convert a string into an unicode braille string (8 dots) (x28nn chars).
        :param txt: (str) alphanumeric string of text
        :return: (str) unicode braille string (\\u28xx...)
        """
        if not txt:
            # Empty string.
            return txt
        with self.lou_mutex:
            return self._to_dots(txt, self.tables.dots)

    def to_text_6(self, braille):
        """
        Convert an unicode braille string (6 dots) (x28nn chars) into a string.
        """
        if not braille:
            # Empty string.
            return braille
        with self.lou_mutex:
            txt = liblouis.dotsToChar([self.path + self.tables.dots6], braille)
            log.info('text:{}'.format(txt))
            return txt

    def to_text_8(self, braille):
        """
        Convert an unicode braille string (x28nn chars) into a string.
        """
        if not braille:
            # Empty string.
            return braille
        with self.lou_mutex:
            txt = liblouis.dotsToChar([self.path + self.tables.dots], braille)
            log.info('text:{}'.format(txt))
            return txt

    def _to_dots_in_bytes(self, text, to_dots):
        static_dots = None
        if text:
            dots = to_dots(text)
            # Convert /u28xx comb. to 8 bits.
            static_dots = bytearray()
            for character in dots:
                byt = ord(character[0]).to_bytes(2, byteorder='big')
                static_dots.append(byt[1])
        return static_dots

    def to_dots_8_in_bytes(self, text):
        # self.to_dots_8 is mutex protected
        return self._to_dots_in_bytes(text, self.to_dots_8)

    def to_dots_6_in_bytes(self, text):
        # self.to_dots_6 is mutex protected
        return self._to_dots_in_bytes(text, self.to_dots_6)

    def to_stm32_display_statics_dots(self, static_text, fixed_dots, braille_display_len) -> bytearray:
        # Complete display with space
        if len(static_text) < braille_display_len:
            static_text += " " * (braille_display_len - len(static_text))
        # Convert to braille dots (\u28xx form)
        dots = self.to_dots_8(static_text).replace(' ', '\u2800')

        added_dots = ''
        if fixed_dots:
            for index, ch in enumerate(dots):
                log.debug('[Index, ch]=[{}, {}]'.format(index, ch))
                if len(fixed_dots) > index:
                    added_dots += chr(ord(ch) | fixed_dots[index])
                else:
                    added_dots += ch
        else:
            added_dots = dots

        # Convert /u28xx comb. to 8 bits.
        static_dots = bytearray()
        for character in added_dots:
            byt = ord(character[0]).to_bytes(2, byteorder='big')
            static_dots.append(byt[1])

        return static_dots

    @staticmethod
    def unicode_braille_to_byte(unicode):
        """
        Convert an unicode braille string into a bytearray of dots.
        """
        braille = bytearray()
        for c in unicode:
            bytes_value = (ord(c) & 0xFF).to_bytes(1, byteorder='big')
            braille += bytes_value
        log.info('braille:{}'.format(braille))
        return braille

    @staticmethod
    def byte_to_unicode_braille(dots):
        output_txt = str()
        for c in dots:
            output_txt += chr(c + 0x2800)
        log.info('braille text:{}'.format(output_txt))
        return output_txt

    def convert_to_braille(self, braille_type, text, pos=-1, no_grade=False) -> (str, str, int):
        # Convert a text (alphanum character) to a braille string ("\u28nn" characters)
        if no_grade:
            text_grade = text
            if braille_type == 'grade1' or braille_type == 'grade2':
                braille = self.to_dots_6(text)
            else:
                braille = self.to_dots_8(text)
        else:
            if braille_type == 'grade1':
                if pos >= 0:
                    (text_grade, index1_origin, index_text, pos) = self.text_to_grade1(text, pos)
                else:
                    (text_grade, index1_origin, index_text, pos) = self.text_to_grade1(text)
                    pos = -1
                log.debug("grade1:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
                braille = self.to_dots_6(text_grade)
            elif braille_type == 'grade2':
                if pos >= 0:
                    (text_grade, index1_origin, index_text, pos) = self.text_to_grade2(text, pos)
                else:
                    (text_grade, index1_origin, index_text, pos) = self.text_to_grade2(text)
                    pos = -1
                log.debug("grade2:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
                braille = self.to_dots_6(text_grade)
            else:
                text_grade = text
                braille = self.to_dots_8(text)

        return text_grade, braille, pos

    def convert_to_text(self, braille_type, braille, pos=-1, no_grade=False) -> (str, int):
        # Convert a braille string ("\u28nn" characters) to a text (alphanum character)
        if no_grade:
            if braille_type == 'grade1' or braille_type == 'grade2':
                text = self.to_text_6(braille)
            else:
                text = self.to_text_8(braille)
        else:
            if braille_type == 'grade1':
                if pos >= 0:
                    (text_grade1, index1_origin, index_text, pos) = self.grade1_to_text(braille, pos)
                else:
                    (text_grade1, index1_origin, index_text, pos) = self.grade1_to_text(braille)
                    pos = -1
                log.debug("grade1:<{}>, {}, {}, {}".format(text_grade1, index1_origin, index_text, pos))
                text = text_grade1
            elif braille_type == 'grade2':
                if pos >= 0:
                    (text_grade2, index1_origin, index_text, pos) = self.grade2_to_text(braille, pos)
                else:
                    (text_grade2, index1_origin, index_text, pos) = self.grade2_to_text(braille)
                    pos = -1
                log.debug("grade2:<{}>, {}, {}, {}".format(text_grade2, index1_origin, index_text, pos))
                text = text_grade2
            else:
                text = self.to_text_8(braille)
        return text, pos


def main():
    print("--------------")
    print("Louis class test:")
    print("--------------")

    print(liblouis.version())
    converter = Lou('ar_LB')
    text_grade1 = "⢁"
    print("backconvertion:<{}> -> <{}>".format(text_grade1, converter.to_text_8(text_grade1)))
    return

    print("----- Test grade2 :")
    # (text_grade2, index1_origin, index_text, pos) = converter.text_to_grade2("The Beatles were an English rock band formed in Liverpool in 1960.")
    (text_grade2, index1_origin, index_text, pos) = converter.text_to_grade2("nouveau fichier.txt")
    print("grade2:<{}>, {}, {}, {}".format(text_grade2, index1_origin, index_text, pos))
    (text_grade2, index1_origin, index_text, pos) = converter.text_to_grade2(".txt")
    print("grade2:<{}>, {}, {}, {}".format(text_grade2, index1_origin, index_text, pos))
    print("backconvertion:<{}>".format(converter.grade2_to_text(text_grade2)))
    (text_grade2, index1_origin, index_text, pos) = converter.text_to_grade2("txt")
    print("grade2:<{}>, {}, {}, {}".format(text_grade2, index1_origin, index_text, pos))
    print("backconvertion:<{}>".format(converter.grade2_to_text(text_grade2)))
    braille = converter.to_dots_6(text_grade2)
    print(f"braille_6 <{braille}>")
    print("grade2_pos:{} {}".format(pos, type(pos)))
    print("backconvertion:<{}>".format(converter.grade2_to_text(text_grade2)))

    print("----- Test grade1 :")
    (text_grade1, index1_origin, index_text, pos) = converter.text_to_grade1("angle: radian")
    print("grade1:{}, {}, {}, {}".format(text_grade1, index1_origin, index_text, pos))
    print("grade1_pos:{} {}".format(pos, type(pos)))
    braille = converter.to_dots_8(text_grade1)
    print("braille_8 :" + braille)
    braille = converter.to_dots_6(text_grade1)
    print("braille_6 :" + braille)

    print("backconvertion:{}".format(converter.grade1_to_text(text_grade1)))

    print("----- Test dots conversion and reverse :")
    braille = converter.to_dots_8("Bonjour chez vous 1234 + 5 !")
    print("braille :" + braille)
    print("text :{}".format(converter.to_text_8(braille)))


if __name__ == "__main__":
    main()
