from .braille import b6, b3, b2, b15, b36, b56
from .math_parser import MathParser, MathBrailleTable, MathTextTable
from .math_nemeth_parser import MathNemethParser, MathNemethBrailleTable
from .math_exception import MathInjectionException, MathUnaryException, MathException
from .math_result import MathResult

import logging


class NullHandler(logging.Handler):
    """A Handler that does nothing."""

    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
