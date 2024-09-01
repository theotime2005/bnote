"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import logging

from .caret import Caret
from .color import Formatting
from .context import Context
from .editor import Editor
from .exception import SelectSheet
from .find_parameters import FindParameters
from .markers import Markers
from .paragraphs import Paragraphs
from .pos import Pos
from .read_file import ReadFile
from .read_mbe_file import ReadMbeFile
from .read_odt_file import ReadOdtFile
from .read_txt_file import ReadTxtFile
from .read_write_specific_file import ReadWriteSpecificFile, checksum
from .undo_redo import UndoRedo
from .write_brf_file import WriteBrfFile
from .writefile import WriteFile


class NullHandler(logging.Handler):
    """A Handler that does nothing."""

    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
