"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

# pip3.8 xlrd3
# csv already in the pi's python package
# Sources : https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python

import csv
import os

import xlrd3

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_XLSX_FILE_LOG
from .exception import BadSheet, SelectSheet

log = ColoredLogger(__name__, level=READ_XLSX_FILE_LOG)

'''
# Setup the logger for this file
from bnote.debug import logging, READ_XLSX_FILE_LOG
log = ColoredLogger(__name__)
log.setLevel(READ_XLSX_FILE_LOG)
'''


class ReadXlsxFile:
    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    def read_file(self, write_lines, encoding=None, sheet_name=None):
        wb = xlrd3.open_workbook(self._full_file_name)
        sheet_list = wb.sheet_names()
        log.info(f"sheet names : {sheet_list}")

        if len(sheet_list) == 1:
            sheet_name = sheet_list[0]
        elif not sheet_name:
            raise SelectSheet(_("select sheet."), sheet_list)

        if sheet_name in sheet_list:
            sh = wb.sheet_by_name(sheet_name)
            # Write csv file.
            csv_file_name = 'csv_file.csv'
            csv_file = open(csv_file_name, 'w')
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for row_num in range(sh.nrows):
                wr.writerow(sh.row_values(row_num))
            csv_file.close()
        else:
            raise BadSheet(_("sheet {} type not found.").format(sheet_name))

        fp = None
        try:
            fp = open(csv_file_name, mode='r', encoding=encoding)

            line = fp.readline()
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
            os.remove(csv_file_name)


# -----------------------------------------------
# Unitary test

def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read XLSX file class test:")
    print("--------------")

    read_txt = ReadXlsxFile("test.xlsx")
    read_txt.read_file(write_line)


if __name__ == "__main__":
    main()
