"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l1llll_opy_ import l1lll1_opy_
from .math_exception import MathException
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
class l111l_opy_(l1lll1_opy_):
    def __init__(self, pos, l1111_opy_=[]):
        l1lll1_opy_.__init__(self, pos)
        self.l1111_opy_ = l1111_opy_
    def display_tree(self, level):
        text = ''.join(['    ' * level, "MULTI OPERAND", l1lll1_opy_.display_tree(self, level), "\n"])
        for l1ll11_opy_ in self.l1111_opy_:
            op = l1ll11_opy_.display_tree(level + 1)
            text = ''.join([text, op])
        return text
    def compute(self):
        values = list()
        for l1ll11_opy_ in self.l1111_opy_:
            values.append(l1ll11_opy_.compute())
        return values