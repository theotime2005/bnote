"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


# import slate3k as slate
# import PyPDF2
import os
from shlex import quote

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_ODT_FILE_LOG
log = ColoredLogger(__name__, level=READ_ODT_FILE_LOG)


class ReadPdfFile:
    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    # Essai 1 slate3k
    # def read_file(self, write_lines):
    #     with open(self._full_file_name, 'rb') as f:
    #         doc = slate.PDF(f)
    #
    #     print(doc)
    #     print("-------------------------------------")
    #     print(doc[0])
    #
    #     for page in doc:
    #         print("Page ----------")
    #         print(type(page))
    #         print(page.replace('\n', ''))
    #         print("End of page ---")

    # Essai 2 PyPDF2
    #    def read_file(self, write_lines):
    #        pdfFileObj = open(self._full_file_name, 'rb')
    #        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #        print(pdfReader.numPages)
    #
    #        pageObj = pdfReader.getPage(9)
    #        text = pageObj.extractText()
    #        print(text)

    # Essai 3 pdftotext
    # Before runs, execute : $sudo apt-get install poppler-utils
    def read_file(self, write_lines):
        fp = None
        output_file = str(self._full_file_name) + ".tmp.txt"
        if not os.path.exists(output_file):
            log.info("pdftotext '" + str(self._full_file_name) + "' '" + str(output_file) + "'")
            # https://stackoverflow.com/questions/35817/how-to-escape-os-system-calls
            os.system("pdftotext " + quote(str(self._full_file_name)) + " " + quote(str(output_file)))

            try:
                fp = open(output_file, 'r')

                line = fp.readline()
                cnt = 1
                while line:
                    # Sleep 1 sec. just for test edition during file reading.
                    # time.sleep(0.5)
                    line = line.replace("\r", "")
                    line = line.replace("\n", "")
                    write_lines(line)
                    # print("Line {}: {}".format(cnt, line.strip()))
                    line = fp.readline()
                    cnt += 1

            finally:
                if fp:
                    fp.close()
                    os.remove(output_file)


# -----------------------------------------------
# Unitary test
def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read PDF file class test:")
    print("--------------")

    read_txt = ReadPdfFile("test2.pdf")
    read_txt.read_file(write_line)


if __name__ == "__main__":
    main()
