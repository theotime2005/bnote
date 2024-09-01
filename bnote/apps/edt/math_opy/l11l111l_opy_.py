"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import math
from enum import Enum, auto

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG
from .l111l_opy_ import l1llll_opy_
from .l1lll1_opy_ import l1ll1l_opy_
from .math_exception import MathException

log = ColoredLogger(__name__, level=MATH_LOG)


class l11lll111_opy_(Enum):
    l1l111l11_opy_ = auto()
    l11l1111_opy_ = auto()
    l1l1lll1l_opy_ = auto()
    l11ll111l_opy_ = auto()
    l1l1111_opy_ = auto()
    l1lll1ll1_opy_ = auto()


class l111l1l1l_opy_(l1llll_opy_):
    def __init__(self, pos, l111lllll1_opy_=l11lll111_opy_.l11l1111_opy_, l11l1ll1l1_opy_=None):
        l1llll_opy_.__init__(self, pos)
        self.arg = l11l1ll1l1_opy_
        self.l111lllll1_opy_ = l111lllll1_opy_

    def display_tree(self, level):
        return ''.join(['    ' * level, self.l111lllll1_opy_.name,
                        l1llll_opy_.display_tree(self, level), "\n", self.arg.display_tree(level + 1)])

    def compute(self):
        if not self.arg:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid argument"))
        if self.l111lllll1_opy_ == l11lll111_opy_.l1lll1ll1_opy_:
            if isinstance(self.arg, l1ll1l_opy_):
                return self.l111llll1l_opy_(self.arg.l11l1_opy_[0], self.arg.l11l1_opy_[1])
            else:
                return math.sqrt(self.arg.compute())
        else:
            return self.arg.compute()

    def l111llll1l_opy_(self, l111llllll_opy_, l111ll11_opy_):
        try:
            l111ll11_opy_ = l111ll11_opy_.compute()
            l111llllll_opy_ = l111llllll_opy_.compute()
            if (l111ll11_opy_ < 0) and ((l111ll11_opy_ % 2) == 0):
                res = -1 * ((-1 * l111ll11_opy_) ** (1 / l111llllll_opy_))
            else:
                res = l111ll11_opy_ ** (1 / l111llllll_opy_)
            return res
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
