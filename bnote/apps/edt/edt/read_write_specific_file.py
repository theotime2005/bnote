"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


import os
import hashlib
import string
import xml.sax

from .marker import Marker
from .pos import Pos
from .coordinates import Coordinates
from .paragraph import Paragraph
from .caret import Caret
from .markers import Markers

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_WRITE_SPECIFIC_FILE_LOG
log = ColoredLogger(__name__, level=READ_WRITE_SPECIFIC_FILE_LOG)


def checksum(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()


class ReadWriteSpecificFile:

    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    def compute_specific_file(self):
        head, tail = os.path.split(self._full_file_name)
        log.info("Head:{}".format(head))
        log.info("Tail:{}".format(tail))
        if head == "":
            filename = "." + tail
        else:
            filename = head + "/." + tail
        log.info("specific file:{}".format(filename))
        return filename

    class ReadHandler(xml.sax.handler.ContentHandler):

        def __init__(self):
            xml.sax.handler.ContentHandler.__init__(self)
            self._is_root = False
            self._is_doc = False
            self._is_body = False
            self._caret = None
            self._markers = None
            self._md5 = None

        # Accessors
        def md5(self):
            return self._md5

        def caret(self):
            return self._caret

        def markers(self):
            return self._markers

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            # print(name)
            if name == "root":
                self._is_root = True

            elif name == "doc":
                if self._is_root:
                    self._is_doc = True
                    keys = attrs.keys()
                    self._md5 = attrs.getValue('md5')
                    log.info("file: md5={}".format(self._md5))

            elif name == "body":
                if self._is_root:
                    self._is_body = True

            elif name == "caret":
                if self._is_root and self._is_body and self._is_doc:
                    keys = attrs.keys()
                    self._caret = Caret()
                    self._caret.start = Pos(int(attrs.getValue('start_x')), int(attrs.getValue('start_y')))
                    self._caret.end = Pos(int(attrs.getValue('end_x')), int(attrs.getValue('end_y')))
                    log.info("caret: {}".format(self._caret))

            elif name == "marker":
                if self._is_root and self._is_body and self._is_doc:
                    keys = attrs.keys()
                    marker = Marker(int(attrs.getValue('index')), int(attrs.getValue('paragraph')))
                    if self._markers is None:
                        self._markers = Markers()
                    self._markers.set_marker(marker)
                    log.info("marker: {}".format(marker))

        def endElement(self, name):
            if name == "body":
                self._is_body = False
            elif name == "doc":
                # Each end of paragraph indicates a end of line
                self._is_doc = False
            elif name == "root":
                self._is_root = False

        def characters(self, content):
            pass

    # https://stackoverflow.com/questions/16347883/generating-xml-in-python/47027013#47027013
    def write_specific_file(self, markers, caret):
        # Compute the name
        specific_filename = self.compute_specific_file()
        outer_template = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
    <root>
     <doc md5="${md5}">
      <body>
       ${caret_list}
       ${marker_list}
      </body>
     </doc>
    </root>
    """)
        md5 = checksum(self._full_file_name)
        # marker_template = string.Template('    <marker id="${id}" paragraph="${par}" index="${index}" />')

        caret_contents = caret.xml_render()
        marker_contents = markers.xml_render()
        result = outer_template.substitute(md5=md5, caret_list='\n'.join(caret_contents),
                                           marker_list='\n       '.join(marker_contents))
        log.info("xml file : \n{}".format(result))

        fp = open(specific_filename, 'w')
        fp.write(result)
        fp.close()

    def read_specific_file(self):
        # Compute the name
        specific_filename = self.compute_specific_file()

        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namespaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        # override the default ContextHandler
        handler = self.ReadHandler()
        parser.setContentHandler(handler)

        try:
            parser.parse(specific_filename)
            return handler.md5(), handler.caret(), handler.markers()

        except Exception as e:
            # Catch all exceptions.
            log.warning("Exception during reading:{}".format(e))
            return None, None, None

    def delete_specific_file(self):
        # Compute the name
        specific_filename = self.compute_specific_file()
        if os.path.exists(specific_filename):
            # removing the file using the os.remove() method
            os.remove(specific_filename)

# -----------------------------------------------
# Unitary test
def get_line(number):
    if number == 0:
        return "Line 1"
    elif number == 1:
        return "Line 2"
    elif number == 2:
        return "Line 3"
    else:
        return None


EDITOR_LINE_LENGTH = 12


def main():
    print("--------------")
    print("Write file class:")
    print("WARNING : To run this test you must have a file test_unitary.txt file create by unitary test of WriteFile "
          "class.")
    print("--------------")

    caret = Caret()
    markers = Markers()
    # paragraph = Paragraph(get_line(0), EDITOR_LINE_LENGTH)
    markers.add_marker(Coordinates(1, 0, 0), Paragraph(get_line(0), EDITOR_LINE_LENGTH))
    markers.add_marker(Coordinates(2, 0, 1), Paragraph(get_line(0), EDITOR_LINE_LENGTH))
    write_file = ReadWriteSpecificFile("test_unitary.txt")
    write_file.write_specific_file(markers, caret)


if __name__ == "__main__":
    main()


