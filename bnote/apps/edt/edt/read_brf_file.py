"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from pathlib import Path
from bnote.braille.lou import Lou
import time

# Setup the logger for this file
# from .colored_log import ColoredLogger, READ_BRF_FILE_LOG
# log = ColoredLogger(__name__, level=READ_BRF_FILE_LOG)


class ReadBrfFile:
    def __init__(self, full_file_name):
        self._full_file_name = Path(full_file_name)

    def read_file(self, lou, language, append_paragraph, encoding=None):
        if not self._full_file_name.is_file():
            append_paragraph("Invalid file !")
            return
        fp = None
        try:
            lou_us = None
            if language == "US":
                # log.info("transcode brf file with US table")
                lou_us = Lou("en_US")

            fp = open(self._full_file_name, mode="r", encoding=encoding)

            line = fp.readline()
            cnt = 1

            if not line:
                # File of 0 bytes, write a line anyway.
                append_paragraph(line)
            else:
                while line:
                    # Sleep 1 sec. just for test edition during file reading.
                    # time.sleep(0.5)
                    # Just to let others threads running.
                    time.sleep(0.001)

                    line = line.replace("\r", "")
                    line = line.replace("\n", "")
                    line = line.replace("\x0c", "")
                    cnv_line = ""
                    if len(line) > 0:
                        # print(f"{line=}")
                        for c in line:
                            # Each car. is replaced by the last car. of the conversion of car. to dot then to string
                            if lou_us:
                                dot6 = chr(ord(lou_us.to_dots_8(c)) & 0x283F)
                            else:
                                dot6 = chr(ord(lou.to_dots_8(c)) & 0x283F)
                            if dot6 and dot6 != 0:
                                cnv_c = lou.to_text_8(dot6)
                                # print(f"{c=} {dot6=} {cnv_c=}")
                                cnv_line = "".join((cnv_line, cnv_c))
                    append_paragraph(cnv_line)
                    # print("Line {}: {}".format(cnt, line.strip()))
                    line = fp.readline()
                    cnt += 1

        finally:
            if fp:
                fp.close()


# -----------------------------------------------
# Unitary test


def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read BRF file class test:")
    print("--------------")

    # For test define language to "FR"
    lou = Lou("fr_FR")

    lou_us = Lou("en_US")
    line = "A"
    dot6 = lou_us.to_dots_6(line)
    cnv_line = lou.to_text_6(dot6)
    print(f"{line=} {dot6=} {cnv_line=}")

    line = "1"
    dot6 = lou.to_dots_6(line)
    cnv_line = lou.to_text_6(dot6)
    print(f"{line=} {dot6=} {cnv_line=}")

    line = "â"
    dot6 = lou.to_dots_6(line)
    cnv_line = lou.to_text_6(dot6)
    print(f"{line=} {dot6=} {cnv_line=}")

    line = "%"
    dot6 = lou.to_dots_6(line)
    cnv_line = lou.to_text_6(dot6)
    print(f"{line=} {dot6=} {cnv_line=}")

    line = "A"
    (text_grade, index1_origin, index_text, pos) = lou_us.text_to_grade1(line, cursor=0)
    c = text_grade[len(text_grade) - 1]
    dot6 = lou_us.to_dots_6(c)
    cnv_line = lou.to_text_6(dot6)
    print(f"{line=} {text_grade=} {c=} {dot6=} {cnv_line=}")

    # read_txt = ReadBrfFile("68108.BRF")
    # read_txt.read_file(lou, "FR", write_line, 'cp1252')
    # read_txt = ReadBrfFile("Chimie.brf")
    # read_txt.read_file(lou, "FR", write_line, 'cp1252')


if __name__ == "__main__":
    main()
