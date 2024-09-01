"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import xml.sax

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_MBE_FILE_LOG

log = ColoredLogger(__name__)
log.setLevel(READ_MBE_FILE_LOG)


class ReadMbeFile:
    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    class MbeHandler(xml.sax.handler.ContentHandler):

        def __init__(self, lou, write_lines):
            xml.sax.handler.ContentHandler.__init__(self)
            self.is_body = False
            self.is_p = False
            self.is_span = False
            self.current_data = ""
            self.span_title = None
            self.span_data = ""
            self._write_lines = write_lines
            self.lou = lou

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            # print(name)
            if name == "body":
                self.is_body = True
            elif name == "p":
                self.is_p = True
            elif name == "span":
                # Parse span attribute 'title'
                self.span_title = ""
                keys = attrs.keys()
                if 'title' in keys:
                    self.span_title = attrs.getValue('title')
                    log.info("SPAN TITLE <{}>".format(self.span_title))
                self.is_span = True

        def endElement(self, name):
            if name == "body":
                self.is_body = False
            elif name == "p":
                # Each end of paragraph indicates a end of line
                log.info("paragraph <{}>".format(self.current_data))
                self._write_lines(self.current_data)
                self.current_data = ""
                self.is_p = False
            elif name == "span":
                if self.span_data:
                    if self.span_title == 'Grade1' or self.span_title == 'Grade2' or self.span_title == 'Math':
                        # Transcode braille code to char.
                        text = self.lou.to_text_8(self.span_data)
                        log.info("{} braille <{}> character <{}>".format(self.span_title, self.span_data, text))
                        self.current_data += text
                    else:
                        log.info("text <{}>".format(self.span_data))
                        self.current_data += self.span_data

                self.span_data = ""
                self.span_title = ""
                self.is_span = False

        def characters(self, content):
            if self.is_body and self.is_p:
                if self.is_span:
                    self.span_data += content
                # else:
                # store all text external to the span
                # !!! this branch generate multiple space before and after span content
                #    self.current_data += content

    def read_file(self, lou, write_lines):
        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namespaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        # override the default ContextHandler
        handler = self.MbeHandler(lou, write_lines)
        parser.setContentHandler(handler)

        parser.parse(self._full_file_name)


# -----------------------------------------------
# Unitary test

def write_line(line):
    print(line)


def main():
    print("--------------")
    print("Read MBE file class test:")
    print("--------------")

    # For test define language to "FR"
    lou = Lou("FR")
    try:
        read_mbe = ReadMbeFile("esytime.mbe")
        read_mbe.read_file(lou, write_line)

    except ValueError:
        print("Parsing ERROR !")
        print(ValueError)

    finally:
        print("End of parsing")


if __name__ == "__main__":
    main()
