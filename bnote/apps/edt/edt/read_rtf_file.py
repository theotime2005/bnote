"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
from striprtf.striprtf import rtf_to_text


class ReadRtfFile:
    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    # Before runs, execute : $sudo apt-get install poppler-utils
    def read_file(self, write_lines):
        fp = None

        try:
            fp = open(self._full_file_name, mode="r")

            rtf = fp.read()
            text = rtf_to_text(rtf)
            text = text.replace("\r", "")
            lines = text.split("\n")
            cnt = 1
            for line in lines:
                # Sleep 1 sec. just for test edition during file reading.
                # time.sleep(0.5)
                write_lines(line)
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
    print("Read RTF file class test:")
    print("--------------")

    read_txt = ReadRtfFile("test.rtf")
    read_txt.read_file(write_line)


if __name__ == "__main__":
    main()
