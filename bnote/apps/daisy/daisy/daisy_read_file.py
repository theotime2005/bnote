"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import codecs
import os
import threading
import xml.sax

from zipfile import BadZipFile


class BadExtensionFile(Exception):
    pass


class DaisyReadFile(threading.Thread):
    STATE_INSTANTIATE = 0
    STATE_RUNNING = 1
    STATE_ENDED = 2

    def __init__(
        self,
        lou,
        full_file_name,
        read_daisy_file,
        language,
        settings_data,
        append_paragraph,
        ended,
    ):
        threading.Thread.__init__(self)
        self.language = language
        self.lou = lou
        self.settings_data = settings_data
        # The name of the file to read.
        self.full_file_name = full_file_name
        self.read_daisy_file = read_daisy_file
        # The lines list to construct.
        self.append_paragraph = append_paragraph
        # Call at the end of reading to define the file_name for write operation.
        self.ended = ended
        # The current thread state.
        self.state = self.STATE_INSTANTIATE
        # The full_file_name used to save the file after modification.
        self.full_file_name_to_write = None
        self.error = None

    def write_lines(self, line):
        self.append_paragraph(line)

    def run(self):
        self.state = self.STATE_RUNNING
        self.read_daisy_file.setup()
        self.read_daisy_file.read_file(self.append_paragraph)
        self.ended(self.error, self.full_file_name, None)
        self.state = self.STATE_ENDED
