"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
from zipfile import ZipFile
import xml.sax
import shutil  # For del folder

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_ODT_FILE_LOG

log = ColoredLogger(__name__, level=READ_ODT_FILE_LOG)


class ReadOdtFile:
    TEMP_FOLDER_NAME = ".bnote-temp"

    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    class DocumentHandler(xml.sax.handler.ContentHandler):

        DOCUMENT_TAG = "office:document-content"
        BODY_TAG = "office:body"
        PARAGRAPH_TAG = "text:p"
        A_TAG = "text:a"
        SPAN_TAG = "text:span"
        TAB_TAG = "text:tab"

        TABLE_TABLE = "table:table"
        TABLE_COLUMN = "table:table-column"
        TABLE_ROW = "table:table-row"
        TABLE_CELL = "table:table-cell"

        def __init__(self, write_lines):
            xml.sax.handler.ContentHandler.__init__(self)
            self.is_document = False
            self.is_body = False
            self.is_paragraph = False
            self.is_a = False
            self.is_span = False
            self.current_data = ""
            self._write_lines = write_lines

            self.is_table = 0
            self.is_table_column = 0
            self.is_table_row = 0
            self.is_table_cell = 0

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            log.info(name)
            if name == self.DOCUMENT_TAG:
                log.info("Tag document")
                self.is_document = True
            elif name == self.BODY_TAG:
                log.info("Tag body")
                self.is_body = True
            elif name == self.PARAGRAPH_TAG:
                log.info("Tag paragraph")
                self.is_paragraph = True
            elif name == self.A_TAG:
                log.info("Tag a")
                self.is_a = True
            elif name == self.TABLE_TABLE:
                log.info("Tag table")
                self.is_table += 1
            elif name == self.TABLE_COLUMN:
                log.info("Tag table column")
                self.is_table_column += 1
            elif name == self.TABLE_ROW:
                log.info("Tag table row")
                self.is_table_row += 1
            elif name == self.TABLE_CELL:
                log.info("Tag table cell")
                self.is_table_cell += 1
                # Add column separator.
                self.current_data += "\t"
            elif name == self.SPAN_TAG:
                log.info("Tag span")
                self.is_span = True
            # keys = attrs.keys()
            # value = attrs.getValue('myAttributeName')

        def endElement(self, name):
            if name == self.DOCUMENT_TAG:
                log.info("Tag end document")
                self.is_document = False
            elif name == self.BODY_TAG:
                log.info("Tag end body")
                self.is_body = False
            elif name == self.PARAGRAPH_TAG:
                log.info("Tag end paragraph")
                self.is_paragraph = False
                # Each end of paragraph indicates a end of line
                if self.is_table == 0:
                    log.info(self.current_data)
                    self._write_lines(self.current_data)
                    self.current_data = ""
            elif name == self.A_TAG:
                log.info("Tag end a")
                self.is_a = False
            elif name == self.SPAN_TAG:
                log.info("Tag end span")
                self.is_span = False
            elif name == self.TAB_TAG:
                # Replace a Tab tag by a tag character.
                self.current_data += "\t"
            elif name == self.TABLE_TABLE:
                log.info("Tag end table")
                self.is_table -= 1
            elif name == self.TABLE_COLUMN:
                log.info("Tag end table column")
                self.is_table_column -= 1
            elif name == self.TABLE_ROW:
                log.info("Tag end table row")
                self.is_table_row -= 1
                self._write_lines(self.current_data)
                self.current_data = ""
            elif name == self.TABLE_CELL:
                log.info("Tag end table cell")
                self.is_table_cell -= 1

        def characters(self, content):
            # if self.is_body and self.is_document and self.is_paragraph and (self.is_span or self.is_a):
            if self.is_body and self.is_document and self.is_paragraph:
                # store all span
                self.current_data += content

    @staticmethod
    def remove_folder(path):
        # check if folder exists
        if os.path.exists(path):
            # remove if exists
            shutil.rmtree(path)
        # else:
        # throw your exception to handle this special scenario
        # raise XXError("your exception")

    def read_file(self, write_lines):
        with ZipFile(self._full_file_name, "r") as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(self.TEMP_FOLDER_NAME)

        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namespaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        # override the default ContextHandler
        handler = self.DocumentHandler(write_lines)
        parser.setContentHandler(handler)

        parser.parse(self.TEMP_FOLDER_NAME + "/content.xml")

        # Delete temp folder.
        self.remove_folder(self.TEMP_FOLDER_NAME)


# -----------------------------------------------
# Unitary test


def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read ODT file class test:")
    print("--------------")

    read_odt = ReadOdtFile("test.odt")
    read_odt.read_file(write_line)


if __name__ == "__main__":
    main()
