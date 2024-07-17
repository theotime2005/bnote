"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


import codecs
import os
import threading
import zlib
from os import path
from zipfile import BadZipFile
from ebooklib import epub
from lxml import etree

from .exception import *
from .read_rtf_file import ReadRtfFile
from .read_mbe_file import ReadMbeFile
from .read_txt_file import ReadTxtFile
from .read_docx_file import ReadDocxFile
from .read_odt_file import ReadOdtFile
from .read_pdf_file import ReadPdfFile
from .read_brf_file import ReadBrfFile
from .read_epub_file import ReadEpubFile
from .read_xlsx_file import ReadXlsxFile

# Set up the logger for this file
from .colored_log import ColoredLogger, READ_FILE_LOG, logging
log = ColoredLogger(__name__)
log.setLevel(READ_FILE_LOG)


class ReadFile(threading.Thread):
    STATE_INSTANTIATE = 0
    STATE_RUNNING = 1
    STATE_ENDED = 2

    def __init__(self, lou, full_file_name, language, add_line, ended, sheet_name=None):
        threading.Thread.__init__(self)
        self.language = language
        self.lou = lou
        # The name of the file to read.
        self._full_file_name = full_file_name
        # The lines list to construct.
        self.add_line = add_line
        # Call at the end of reading to define the file_name for write operation.
        self.ended = ended
        # for xlsx import, the sheet_name
        self.sheet_name = sheet_name
        # The current thread state.
        self.state = self.STATE_INSTANTIATE
        # The full_file_name used to save the file after modification.
        self.full_file_name_to_write = None
        self.error = None
        self.sheet_list = None

    def write_lines(self, line, marker=False):
        if READ_FILE_LOG <= logging.WARNING:
            log.warning(line)
        self.add_line(line, marker)

    @staticmethod
    def create_save_file_name(full_file_name):
        if READ_FILE_LOG <= logging.DEBUG:
            log.debug("Compute filename from imported file {}".format(full_file_name))
        new_name = str(full_file_name) + os.extsep + "txt"
        if path.exists(new_name):
            # File already exists.
            raise BadNewFileName(
                _('the original file has already been converted. Please open the converted file or rename/delete it if you want to try again this conversion.')
            )
        else:
            return new_name

    def run(self):
        self.state = self.STATE_RUNNING
        file_name, file_extension = os.path.splitext(self._full_file_name)
        if file_extension:
            file_extension = file_extension.lower()

        try:
            if file_extension == ".txt":
                encodings = ['utf-8', 'cp1252']
                e = None
                for e in encodings:
                    try:
                        fh = codecs.open(self._full_file_name, 'r', encoding=e)
                        fh.readlines()
                        fh.seek(0)
                    except UnicodeDecodeError:
                        log.warning('got unicode error with %s , trying different encoding' % e)
                    else:
                        log.warning('opening the file with encoding:  %s ' % e)
                        break
                self.full_file_name_to_write = self._full_file_name
                read_txt_file = ReadTxtFile(self._full_file_name)
                read_txt_file.read_file(self.write_lines, encoding=e)
            elif file_extension == ".mbe":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_mbe_file = ReadMbeFile(self._full_file_name)
                read_mbe_file.read_file(self.lou, self.write_lines)
            elif file_extension == ".docx":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_mbe_file = ReadDocxFile(self._full_file_name)
                read_mbe_file.read_file(self.write_lines)
            elif file_extension == ".odt":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_mbe_file = ReadOdtFile(self._full_file_name)
                read_mbe_file.read_file(self.write_lines)
            elif file_extension == ".pdf":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_pdf_file = ReadPdfFile(self._full_file_name)
                read_pdf_file.read_file(self.write_lines)
            elif file_extension == ".rtf":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_pdf_file = ReadRtfFile(self._full_file_name)
                read_pdf_file.read_file(self.write_lines)
            elif file_extension == ".brf":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_brf_file = ReadBrfFile(self._full_file_name)
                read_brf_file.read_file(self.lou, self.language, self.write_lines, 'cp1252')
            elif file_extension == ".epub":
                self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_epub_file = ReadEpubFile(self._full_file_name)
                read_epub_file.read_file(self.write_lines)
            elif file_extension == ".xlsx":
                if self.sheet_name:
                    file_name = f"{self._full_file_name}{'#'}{self.sheet_name}"
                    self.full_file_name_to_write = self.create_save_file_name(file_name)
                else:
                    self.full_file_name_to_write = self.create_save_file_name(self._full_file_name)
                read_xlsx_file = ReadXlsxFile(self._full_file_name)
                read_xlsx_file.read_file(self.write_lines, encoding='cp1252', sheet_name=self.sheet_name)

            else:
                raise BadExtensionFile(_("file {} type not supported.").format(self._full_file_name))

        except ValueError as error:
            self.error = error

        except IOError as error:
            self.error = error

        except BadZipFile as error:
            self.error = error

        except BadExtensionFile as error:
            self.error = error

        except BadNewFileName as error:
            self.error = error

        except BadSheet as error:
            self.error = error

        except SelectSheet as error:
            self.error = error
            self.sheet_list = error.sheet_list

        # Dans certain epub.
        # KeyError: "There is no item named 'OEBPS/content/resources/page-template.xpgt' in the archive"
        except KeyError as error:
            self.error = error

        # Dans certain epub (BadZipFile).
        # zipfile.BadZipFile: File is not a zip file
        # ebooklib.epub.EpubException: 'Bad Zip file'
        except epub.EpubException as error:
            self.error = error

        # Dans certain epub.
        # zlib.error: Error -3 while decompressing data: invalid distance too far back
        except zlib.error as error:
            self.error = error

        # Dans certain epub.
        # lxml.etree.XMLSyntaxError: Entity 'nbsp' not defined, line 1, column 604
        except etree.XMLSyntaxError as error:
            self.error = error

        finally:
            self.ended(self.error, self.full_file_name_to_write, self.sheet_list)
            self.state = self.STATE_ENDED
            if READ_FILE_LOG <= logging.INFO:
                log.info("End reading file")


# -----------------------------------------------
# Unitary test
def main():
    print("--------------")
    print("Read file class:")
    print("--------------")

    print("TO DO")


if __name__ == "__main__":
    main()
