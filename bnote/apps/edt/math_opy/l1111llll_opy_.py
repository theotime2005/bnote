"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import math
from enum import Enum, auto
from .l1llll_opy_ import l1lll1_opy_
from .math_exception import MathException
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG
from .l1ll1l_opy_ import l111l_opy_
log = ColoredLogger(__name__, level=MATH_LOG)
class l11l111l_opy_(Enum):
    l11l1111l_opy_ = auto()
    l11ll11l_opy_ = auto()
    l1l11l11_opy_ = auto()
    l1l1lll_opy_ = auto()
    l1ll11l1_opy_ = auto()
    l11l11l11_opy_ = auto()
class l1lll11l1_opy_(l1lll1_opy_):
    def __init__(self, pos, l1ll1l1111_opy_=l11l111l_opy_.l11ll11l_opy_, l1llllll1l_opy_=None):
        l1lll1_opy_.__init__(self, pos)
        self.arg = l1llllll1l_opy_
        self.l1ll1l1111_opy_ = l1ll1l1111_opy_
    def display_tree(self, level):
        return ''.join(['    ' * level, self.l1ll1l1111_opy_.name,
                       l1lll1_opy_.display_tree(self, level), "\n", self.arg.display_tree(level + 1)])
    def compute(self):
        if not self.arg:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid argument"))
        if self.l1ll1l1111_opy_ == l11l111l_opy_.l11l11l11_opy_:
            if isinstance(self.arg, l111l_opy_):
                return self.l1ll1l111l_opy_(self.arg.l1111_opy_[0], self.arg.l1111_opy_[1])
            else:
                return math.sqrt(self.arg.compute())
        else:
            return self.arg.compute()
    def l1ll1l111l_opy_(self, l1ll1l11l1_opy_, l11ll1_opy_):
        try:
            l11ll1_opy_ = l11ll1_opy_.compute()
            l1ll1l11l1_opy_ = l1ll1l11l1_opy_.compute()
            if (l11ll1_opy_ < 0) and ((l11ll1_opy_ % 2) == 0):
                res = -1 * ((-1 * l11ll1_opy_) ** (1 / l1ll1l11l1_opy_))
            else:
                res = l11ll1_opy_ ** (1 / l1ll1l11l1_opy_)
            return res
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))