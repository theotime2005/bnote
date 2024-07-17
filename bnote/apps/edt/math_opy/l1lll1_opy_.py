"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .math_exception import MathException
# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
class l1111_opy_:
    def __init__(self, pos):
        self.pos = pos
    def display_tree(self, level):
        return " ({}) ".format(self.pos)
    def compute(self):
        raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("item not evaluable"))