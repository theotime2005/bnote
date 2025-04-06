"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from .editor import Editor
from .undo_redo import UndoRedo
from .caret import Caret
from .markers import Markers
from .paragraphs import Paragraphs
from .pos import Pos
from .color import Formatting
from .read_txt_file import ReadTxtFile
from .find_parameters import FindParameters
from .read_odt_file import ReadOdtFile
from .read_mbe_file import ReadMbeFile
from .read_write_specific_file import ReadWriteSpecificFile, checksum
from .context import Context
from .read_file import ReadFile
from .writefile import WriteFile
from .exception import SelectSheet
from .write_brf_file import WriteBrfFile

import logging


class NullHandler(logging.Handler):
    """A Handler that does nothing."""

    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
