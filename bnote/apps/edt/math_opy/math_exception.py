"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from enum import Enum, auto


class MathException(Exception):
    """ Exception raised for math parsing error

     Attributes:
         pos: Error position in original text to parse
         error_code: error code of parsing (see class ErrorCode)
         message: Explanation of the error
     """

    class ErrorCode(Enum):
        EMPTY_ARG = auto()
        BLOC_ERROR = auto()
        INVALID_ARG = auto()
        INVALID_FUNCTION = auto()
        DIVISION_BY_ZERO = auto()
        INFINITE_VALUE = auto()
        NOT_EVALUABLE = auto()
        NEGATIVE_SQRT = auto()
        UNDEFINED_PARAM = auto()
        INVALID_ASSIGNMENT = auto()

    def __init__(self, pos, error_code, message="Unknown error"):
        self.error_code = error_code
        self.pos = pos
        self.message = message
        super().__init__(self.message)


class MathInjectionException(Exception):
    """ Exception raised for invisible mul injection.

     Attributes:
         pos: Injection position in original text to parse
         message: Explanation of the error
     """

    def __init__(self, pos, message="Inject invisible mul"):
        self.inject_pos = pos
        self.message = message
        super().__init__(self.message)


class MathUnaryException(Exception):
    """ Exception raised for invisible mul injection.

     Attributes:
         pos: Injection position in original text to parse
         message: Explanation of the error
     """

    def __init__(self, pos, message="Unary operand"):
        self.unary_pos = pos
        self.message = message
        super().__init__(self.message)
