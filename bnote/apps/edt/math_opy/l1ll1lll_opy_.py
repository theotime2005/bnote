"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from enum import Enum, auto
import math
from .l1lll1_opy_ import l1111_opy_
from .math_exception import MathException

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class l1l11111l_opy_(Enum):
    l1l1ll11_opy_ = auto()
    l1l11lll_opy_ = auto()
    l11lll1ll_opy_ = auto()
    l1lll1l1_opy_ = auto()
    l1ll11ll1_opy_ = auto()
    l11l111ll_opy_ = auto()
    l1llll1l_opy_ = auto()
    l111l11l1_opy_ = auto()
    l11l11111_opy_ = auto()
    l11lll1l1_opy_ = auto()
    l11111_opy_ = auto()
    l1ll1l1ll_opy_ = auto()
    l11l1l1_opy_ = auto()
    l1111l1_opy_ = auto()
    l1lll1ll1_opy_ = auto()
    l1l11ll_opy_ = auto()
    l111l1ll1_opy_ = auto()
    l11ll11l1_opy_ = auto()
    l11ll1l11_opy_ = auto()
    l11l1l111_opy_ = auto()
    l1l11111_opy_ = auto()
    l1ll1l11l_opy_ = auto()
    l1ll111ll_opy_ = auto()
    l111l11_opy_ = auto()


class l111ll_opy_(Enum):
    l11lll111_opy_ = auto()
    l1lll11_opy_ = auto()


class l1ll11111_opy_(l1111_opy_):
    l11ll1ll_opy_ = l111ll_opy_.l11lll111_opy_

    def __init__(self, pos, function=None, arg=None):
        l1111_opy_.__init__(self, pos)
        if not function or not arg:
            raise MathException(
                self.pos,
                MathException.ErrorCode.INVALID_FUNCTION,
                _("invalid function"),
            )
        self.arg = arg
        self.function = function

    def display_tree(self, level):
        return "".join(
            [
                "    " * level,
                self.function.name,
                l1111_opy_.display_tree(self, level),
                "\n",
                self.arg.display_tree(level + 1),
            ]
        )

    def compute(self):
        l11l1ll1l1_opy_ = {
            l1l11111l_opy_.l1l1ll11_opy_: l1ll11111_opy_.l1llll1ll1l_opy_,
            l1l11111l_opy_.l1l11lll_opy_: l1ll11111_opy_.l1111111ll_opy_,
            l1l11111l_opy_.l11lll1ll_opy_: l1ll11111_opy_.l1lllll1l1l_opy_,
            l1l11111l_opy_.l1lll1l1_opy_: l1ll11111_opy_.l1llll1ll11_opy_,
            l1l11111l_opy_.l1ll11ll1_opy_: l1ll11111_opy_.l1lllll1lll_opy_,
            l1l11111l_opy_.l11l111ll_opy_: l1ll11111_opy_.l1lllllll1l_opy_,
            l1l11111l_opy_.l1llll1l_opy_: l1ll11111_opy_.l1lllll11ll_opy_,
            l1l11111l_opy_.l111l11l1_opy_: l1ll11111_opy_.l1llllllll1_opy_,
            l1l11111l_opy_.l11l11111_opy_: l1ll11111_opy_.l1lllllll11_opy_,
            l1l11111l_opy_.l11lll1l1_opy_: l1ll11111_opy_.l111111l1l_opy_,
            l1l11111l_opy_.l11111_opy_: l1ll11111_opy_.l1llllll11l_opy_,
            l1l11111l_opy_.l1111l1_opy_: l1ll11111_opy_.l1lllll11l1_opy_,
            l1l11111l_opy_.l1lll1ll1_opy_: l1ll11111_opy_.l1111111l1_opy_,
            l1l11111l_opy_.l1l11ll_opy_: l1ll11111_opy_.l1llll1llll_opy_,
            l1l11111l_opy_.l111l1ll1_opy_: l1ll11111_opy_.l1llllll111_opy_,
            l1l11111l_opy_.l11ll11l1_opy_: l1ll11111_opy_.l11111111l_opy_,
            l1l11111l_opy_.l11ll1l11_opy_: l1ll11111_opy_.l1lllllllll_opy_,
            l1l11111l_opy_.l11l1l111_opy_: l1ll11111_opy_.l1llll1l1ll_opy_,
            l1l11111l_opy_.l1l11111_opy_: l1ll11111_opy_.l1lllll111l_opy_,
            l1l11111l_opy_.l1ll1l1ll_opy_: l1ll11111_opy_.l1lllll1111_opy_,
            l1l11111l_opy_.l11l1l1_opy_: l1ll11111_opy_.l1llllll1l1_opy_,
            l1l11111l_opy_.l1ll1l11l_opy_: l1ll11111_opy_.l1llllll1ll_opy_,
            l1l11111l_opy_.l1ll111ll_opy_: l1ll11111_opy_.l111111l11_opy_,
            l1l11111l_opy_.l111l11_opy_: l1ll11111_opy_.l1lllll1l11_opy_,
        }
        function = l11l1ll1l1_opy_.get(self.function, None)
        if function:
            return function(self)
        else:
            raise MathException(
                self.pos,
                MathException.ErrorCode.INVALID_FUNCTION,
                _("invalid function"),
            )

    def _1lllll1ll1_opy_(self, arg):
        if l1ll11111_opy_.l11ll1ll_opy_ == l111ll_opy_.l11lll111_opy_:
            return arg
        else:
            return math.radians(arg)

    def _111111111_opy_(self, arg):
        if l1ll11111_opy_.l11ll1ll_opy_ == l111ll_opy_.l1lll11_opy_:
            return math.degrees(arg)
        else:
            return arg

    def l1llll1lll1_opy_(self, l1ll1lll_opy_):
        return l1ll1lll_opy_(self.arg.compute())

    def l1lllll1l1l_opy_(self):
        return math.sin(self._1lllll1ll1_opy_(self.arg.compute()))

    def l1llll1ll11_opy_(self):
        return math.cos(self._1lllll1ll1_opy_(self.arg.compute()))

    def l1lllll1lll_opy_(self):
        return math.tan(self._1lllll1ll1_opy_(self.arg.compute()))

    def l1lllllll1l_opy_(self):
        try:
            return 1 / math.tan(self._1lllll1ll1_opy_(self.arg.compute()))
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def l1llllllll1_opy_(self):
        return self._111111111_opy_(self.l1llll1lll1_opy_(math.asin))

    def l1lllllll11_opy_(self):
        return self._111111111_opy_(self.l1llll1lll1_opy_(math.acos))

    def l111111l1l_opy_(self):
        return self._111111111_opy_(self.l1llll1lll1_opy_(math.atan))

    def l1llllll11l_opy_(self):
        try:
            return self._111111111_opy_(math.atan(1 / self.arg.compute()))
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def l1lllll11l1_opy_(self):
        return self.l1llll1lll1_opy_(math.sinh)

    def l1111111l1_opy_(self):
        return self.l1llll1lll1_opy_(math.cosh)

    def l1llll1llll_opy_(self):
        return self.l1llll1lll1_opy_(math.tanh)

    def l1llllll111_opy_(self):
        try:
            return 1 / self.l1llll1lll1_opy_(math.tanh)
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def l11111111l_opy_(self):
        return self.l1llll1lll1_opy_(math.asinh)

    def l1lllllllll_opy_(self):
        return self.l1llll1lll1_opy_(math.acosh)

    def l1llll1l1ll_opy_(self):
        return self.l1llll1lll1_opy_(math.atanh)

    def l1lllll111l_opy_(self):
        try:
            return 1 / self.l1llll1lll1_opy_(math.atanh)
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def l1llllll1l1_opy_(self):
        return self.l1llll1lll1_opy_(math.radians)

    def l1lllll1111_opy_(self):
        return self.l1llll1lll1_opy_(math.degrees)

    def l1llll1ll1l_opy_(self):
        return self.l1llll1lll1_opy_(math.log)

    def l1111111ll_opy_(self):
        return self.l1llll1lll1_opy_(math.log10)

    def l1lllll11ll_opy_(self):
        return self.l1llll1lll1_opy_(math.sqrt)

    def l1llllll1ll_opy_(self):
        return self.arg.compute()

    def l111111l11_opy_(self):
        return 0 - self.arg.compute()

    def l1lllll1l11_opy_(self):
        value = self.arg.compute()
        l111l111l1_opy_ = int(value)
        res = 1.0
        if (value > 0) and (value - l111l111l1_opy_ == 0):
            while l111l111l1_opy_ > 0:
                res = l111l111l1_opy_ * res
                l111l111l1_opy_ -= 1
            return res
        else:
            raise MathException(
                self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid argument")
            )
