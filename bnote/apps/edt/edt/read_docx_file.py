"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import shutil  # For del folder
import xml.sax
from zipfile import ZipFile

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_DOCX_FILE_LOG, logging

log = ColoredLogger(__name__, level=READ_DOCX_FILE_LOG)


class ReadDocxFile:
    TEMP_FOLDER_NAME = '.bnote-temp'

    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    class ContentHandler(xml.sax.handler.ContentHandler):

        def __init__(self):
            xml.sax.handler.ContentHandler.__init__(self)
            self.is_types = False
            self.is_t = False
            self.current_data = ""
            self.document_name = None

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            if READ_DOCX_FILE_LOG <= logging.INFO:
                log.info(name)
            if name == "Types":
                self.is_types = True
            elif self.is_types and name == "Override":
                value = attrs.getValue("ContentType")
                if value == "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml":
                    self.document_name = attrs.getValue("PartName")
            # keys = attrs.keys()
            # value = attrs.getValue('myAttributeName')

        def endElement(self, name):
            if name == "Types":
                self.is_types = False

        def characters(self, content):
            pass

    class DocumentHandler(xml.sax.ContentHandler):

        DOCUMENT_TAG = "w:document"
        BODY_TAG = "w:body"
        PARAGRAPH_TAG = "w:p"
        T_TAG = "w:t"
        TAB_TAG = "w:tab"
        TBL_TAG = "w:tbl"
        TC_TAG = "w:tc"
        TR_TAG = "w:tr"

        def __init__(self, write_lines):
            self.is_document = False
            self.is_body = False
            self.is_paragraph = False
            self.is_t = False
            self.is_tab = False
            self.is_table = False
            self.is_table_row = False
            self.is_table_cell = False
            self.current_data = ""
            self._write_lines = write_lines

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            if READ_DOCX_FILE_LOG <= logging.INFO:
                log.info(name)
            if name == self.DOCUMENT_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag document")
                self.is_document = True
            elif name == self.BODY_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag body")
                self.is_body = True
            elif name == self.PARAGRAPH_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag paragraph")
                self.is_paragraph = True
            elif name == self.T_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag text")
                self.is_t = True
            elif name == self.TAB_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tab")
                self.is_tab = True
            elif name == self.TBL_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tbl")
                self.is_table = True
            elif name == self.TR_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tr")
                self.is_table_row = True
            elif name == self.TC_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tc")
                self.is_table_cell = True
                # Add column separator.
                if self.current_data != "":
                    self.current_data += '\t'

            # keys = attrs.keys()
            # value = attrs.getValue('myAttributeName')

        def endElement(self, name):
            if name == self.DOCUMENT_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag end document")
                self.is_document = False
            elif name == self.BODY_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag end body")
                self.is_body = False
            elif name == self.PARAGRAPH_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag end paragraph")
                self.is_paragraph = False
                # Each end of paragraph indicates a end of line
                if not self.is_table:
                    if READ_DOCX_FILE_LOG <= logging.INFO:
                        log.info(self.current_data)
                    self._write_lines(self.current_data)
                    self.current_data = ""
            elif name == self.T_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag end text")
                self.is_t = False
            elif name == self.TAB_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag end tab")
                self.is_tab = False
                # Add a tab separator
                self.current_data += '\t'
            elif name == self.TBL_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tbl")
                self.is_table = False
            elif name == self.TR_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tr")
                self.is_table_row = False
                self._write_lines(self.current_data)
                self.current_data = ""
            elif name == self.TC_TAG:
                if READ_DOCX_FILE_LOG <= logging.INFO:
                    log.info("Tag tc")
                self.is_table_cell = False

        def characters(self, content):
            if self.is_body and self.is_document and self.is_paragraph and self.is_t:
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
        with ZipFile(self._full_file_name, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(self.TEMP_FOLDER_NAME)

        # create an XMLReader
        parser = xml.sax.make_parser()
        # override the default ContextHandler
        content_handler = self.ContentHandler()
        parser.setContentHandler(content_handler)
        parser.parse(self.TEMP_FOLDER_NAME + "/" + "[Content_Types].xml")

        if content_handler.document_name:
            # create an XMLReader
            parser = xml.sax.make_parser()
            # turn off namepsaces
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            # override the default ContextHandler
            handler = self.DocumentHandler(write_lines)
            parser.setContentHandler(handler)

            parser.parse(self.TEMP_FOLDER_NAME + content_handler.document_name)

        # Delete temp folder.
        self.remove_folder(self.TEMP_FOLDER_NAME)


# -----------------------------------------------
# Unitary test

def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read DOCX file class test:")
    print("--------------")

    read_docx = ReadDocxFile("test.docx")
    read_docx.read_file(write_line)


if __name__ == "__main__":
    main()
