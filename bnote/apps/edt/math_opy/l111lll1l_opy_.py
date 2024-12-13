"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import math
from enum import Enum, auto
from .l1lll1_opy_ import l1111_opy_
from .math_exception import MathException

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG
from .l1llll_opy_ import l11l1_opy_

log = ColoredLogger(__name__, level=MATH_LOG)


class l1111l1ll_opy_(Enum):
    l111l1l11_opy_ = auto()
    l1l11ll1_opy_ = auto()
    l1111lll1_opy_ = auto()
    l111ll11_opy_ = auto()
    l111lllll_opy_ = auto()
    l1llll1l_opy_ = auto()


class l1lll111l_opy_(l1111_opy_):
    def __init__(
        self, pos, l111lllll1_opy_=l1111l1ll_opy_.l1l11ll1_opy_, l11l1lll1l_opy_=None
    ):
        l1111_opy_.__init__(self, pos)
        self.arg = l11l1lll1l_opy_
        self.l111lllll1_opy_ = l111lllll1_opy_

    def display_tree(self, level):
        return "".join(
            [
                "    " * level,
                self.l111lllll1_opy_.name,
                l1111_opy_.display_tree(self, level),
                "\n",
                self.arg.display_tree(level + 1),
            ]
        )

    def compute(self):
        if not self.arg:
            raise MathException(
                self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid argument")
            )
        if self.l111lllll1_opy_ == l1111l1ll_opy_.l1llll1l_opy_:
            if isinstance(self.arg, l11l1_opy_):
                return self.l111llll1l_opy_(
                    self.arg.l1ll1l_opy_[0], self.arg.l1ll1l_opy_[1]
                )
            else:
                return math.sqrt(self.arg.compute())
        else:
            return self.arg.compute()

    def l111llll1l_opy_(self, l111llllll_opy_, l1lll1l11_opy_):
        try:
            l1lll1l11_opy_ = l1lll1l11_opy_.compute()
            l111llllll_opy_ = l111llllll_opy_.compute()
            if (l1lll1l11_opy_ < 0) and ((l1lll1l11_opy_ % 2) == 0):
                res = -1 * ((-1 * l1lll1l11_opy_) ** (1 / l111llllll_opy_))
            else:
                res = l1lll1l11_opy_ ** (1 / l111llllll_opy_)
            return res
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )
