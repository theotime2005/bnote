"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import string
import xml.sax
# import hashlib
# import xxhash
from pathlib import Path

from bnote.apps.edt.edt.mp3 import Mp3
from .caret import Caret
# Setup the logger for this file
from .colored_log import ColoredLogger, READ_WRITE_SPECIFIC_FILE_LOG
from .marker import Marker
from .markers import Markers
from .pos import Pos

log = ColoredLogger(__name__, level=READ_WRITE_SPECIFIC_FILE_LOG)


def checksum(filename):
    # 13 sec. for A_Ceux_qui_revent.zip
    # return hashlib.md5(open(filename, 'rb').read()).hexdigest()
    # 7 sec. for A_Ceux_qui_revent.zip
    # return xxhash.xxh64(open(filename, "rb").read()).hexdigest()
    # 0.0001 sec.
    return os.path.getsize(filename)


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

    """
    File example:
    <?xml version="1.0" encoding="UTF-8"?>
            <root>
             <doc md5="34f417a85ca00b75f7e4351297359f45">
              <body>
                   <caret start_x="0" start_y="124" end_x="0" end_y="124" />
                   <marker id="0" paragraph="3" index="0" />
                   <marker id="1" paragraph="4" index="2" />
                   <read_only value="none" />
                   <mp3 mp3_file="/tmp/bsuite_daisy_jilzg7ot/S00197/05_CHAPITRE_1.mp3" mp3_offset="8435" />
              </body>
             </doc>
            </root>
    """

    class ReadHandler(xml.sax.handler.ContentHandler):
        def __init__(self):
            xml.sax.handler.ContentHandler.__init__(self)
            self._is_root = False
            self._is_doc = False
            self._is_body = False
            self._caret = None
            self._markers = None
            self._read_only = None
            self._md5 = None
            self._mp3 = None

        # Accessors
        def md5(self):
            return self._md5

        def caret(self):
            return self._caret

        def markers(self):
            return self._markers

        def read_only(self):
            return self._read_only

        def mp3(self):
            return self._mp3

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
            elif name == "read_only":
                self._read_only = None
                if attrs.getValue('value') == 'true':
                    self._read_only = True
                elif attrs.getValue('value') == 'false':
                    self._read_only = False
            elif name == "mp3":
                self._mp3 = Mp3(Path(attrs.getValue('mp3_file')), int(attrs.getValue('mp3_offset')))

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

    @staticmethod
    def xml_render_bool(label, value):
        caret_template = string.Template('    <${label_xml} value="${value_xml}" />')
        return [caret_template.substitute(label_xml=label, value_xml=str(value).lower())]

    # https://stackoverflow.com/questions/16347883/generating-xml-in-python/47027013#47027013
    def write_specific_file(self, **kwargs):
        # Compute the name
        specific_filename = self.compute_specific_file()
        editor_template = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
    <root>
     <doc md5="${md5}">
      <body>
       ${caret_list}
       ${marker_list}
       ${read_only_bool}
      </body>
     </doc>
    </root>
    """)
        daisy_template = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
        <root>
         <doc md5="${md5}">
          <body>
           ${caret_list}
           ${marker_list}
           ${read_only_bool}
           ${mp3_list}
          </body>
         </doc>
        </root>
        """)
        md5 = checksum(self._full_file_name)
        # marker_template = string.Template('    <marker id="${id}" paragraph="${par}" index="${index}" />')
        caret_contents = kwargs['caret'].xml_render()
        marker_contents = kwargs['markers'].xml_render()
        read_only_contents = self.xml_render_bool("read_only", kwargs['read_only'])
        mp3_contents = None
        if 'mp3' in kwargs:
            mp3_contents = kwargs['mp3'].xml_render()
        if mp3_contents:
            result = daisy_template.substitute(md5=md5, caret_list='\n'.join(caret_contents),
                                               marker_list='\n       '.join(marker_contents),
                                               read_only_bool='\n'.join(read_only_contents),
                                               mp3_list='\n'.join(mp3_contents)
                                               )
        else:
            result = editor_template.substitute(md5=md5, caret_list='\n'.join(caret_contents),
                                                marker_list='\n       '.join(marker_contents),
                                                read_only_bool='\n'.join(read_only_contents))
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
            return {
                'md5': handler.md5(), 'caret': handler.caret(),
                'markers': handler.markers(), 'read_only': handler.read_only(),
                'mp3': handler.mp3()
            }

        except Exception as e:
            # Catch all exceptions.
            log.warning("Exception during reading:{}".format(e))
            return {
                'md5': None, 'caret': None,
                'markers': None, 'read_only': None,
                'mp3': None
            }

    def delete_specific_file(self):
        # Compute the name
        specific_filename = self.compute_specific_file()
        if os.path.exists(specific_filename):
            # removing the file using the os.remove() method
            os.remove(specific_filename)
