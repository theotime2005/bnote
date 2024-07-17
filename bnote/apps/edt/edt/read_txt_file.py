"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


import time
'''
# Setup the logger for this file
from bnote.debug import logging, READ_TXT_FILE_LOG
log = ColoredLogger(__name__)
log.setLevel(READ_TXT_FILE_LOG)
'''


class ReadTxtFile:
    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    def read_file(self, write_lines, encoding=None):
        fp = None
        try:
            fp = open(self._full_file_name, mode='r', encoding=encoding)
            line = fp.readline()
            # For the first line, remove the BOM indicator
            line = line.replace(u"\ufeff", "")
            cnt = 1
            if not line:
                # File of 0 bytes, write a line anyway.
                write_lines(line)
            else:
                while line:
                    # Just to let others threads running.
                    # time.sleep(1)

                    line = line.replace("\r", "")
                    line = line.replace("\n", "")
                    write_lines(line)
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
    print("Read TXT file class test:")
    print("--------------")

    read_txt = ReadTxtFile("test.txt")
    read_txt.read_file(write_line)


if __name__ == "__main__":
    main()
