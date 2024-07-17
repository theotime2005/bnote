"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import string
from xml.sax import saxutils

from .pos import Pos


# -----------------------------------------------
# Caret definition
class Mp3:
    def __init__(self, mp3_file=None, mp3_offset=None):
        self.mp3_file = mp3_file
        self.mp3_offset = mp3_offset

    # For print()
    def __repr__(self):
        return f"Mp3[{self.mp3_file=}] [{self.mp3_offset=}]"

    def xml_render(self):
        if self.mp3_file is not None and self.mp3_offset is not None:
            mp3_template = string.Template('    <mp3 mp3_file="${file}" mp3_offset="${offset}" />')
            return [mp3_template.substitute(
                file=saxutils.escape(str(self.mp3_file.as_posix())),
                offset=saxutils.escape(str(self.mp3_offset))
            )]

