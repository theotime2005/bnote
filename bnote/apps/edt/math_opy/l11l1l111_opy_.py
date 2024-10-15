"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from enum import Enum, auto
import math
from .l1llll_opy_ import l1lll1_opy_
from .math_exception import MathException
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
class l1lll11_opy_(Enum):
    l1l1l1ll1_opy_ = auto()
    l11l1llll_opy_ = auto()
    l1l111l1l_opy_ = auto()
    l1lll1ll_opy_ = auto()
    l1111l111_opy_ = auto()
    l1llll11l_opy_ = auto()
    l11l11l11_opy_ = auto()
    l111ll11_opy_ = auto()
    l1ll1l111_opy_ = auto()
    l1l1ll1l_opy_ = auto()
    l111ll111_opy_ = auto()
    l1l1lll1_opy_ = auto()
    l1l1ll11l_opy_ = auto()
    l1ll1lll_opy_ = auto()
    l1111lll_opy_ = auto()
    l1l1lll11_opy_ = auto()
    l111l111l_opy_ = auto()
    l1llll111_opy_ = auto()
    l1lll111_opy_ = auto()
    l111lll1l_opy_ = auto()
    l111ll_opy_ = auto()
    l1lllll11_opy_ = auto()
    l1l1l1ll_opy_ = auto()
    l11l1ll1_opy_ = auto()
class l11l1l11l_opy_(Enum):
    l111l11l_opy_ = auto()
    l1ll1ll1l_opy_ = auto()
class l111ll1l_opy_(l1lll1_opy_):
    l1l111l1_opy_ = l11l1l11l_opy_.l111l11l_opy_
    def __init__(self, pos, function=None, arg=None):
        l1lll1_opy_.__init__(self, pos)
        if not function or not arg:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_FUNCTION, _("invalid function"))
        self.arg = arg
        self.function = function
    def display_tree(self, level):
        return ''.join(['    ' * level, self.function.name, l1lll1_opy_.display_tree(self, level), "\n", self.arg.display_tree(level + 1)])
    def compute(self):
        l1lll1lll1_opy_ = {
            l1lll11_opy_.l1l1l1ll1_opy_: l111ll1l_opy_.l1l111l11l_opy_,
            l1lll11_opy_.l11l1llll_opy_: l111ll1l_opy_.l1l11l11l1_opy_,
            l1lll11_opy_.l1l111l1l_opy_: l111ll1l_opy_.l1l11l1ll1_opy_,
            l1lll11_opy_.l1lll1ll_opy_: l111ll1l_opy_.l1l11l11ll_opy_,
            l1lll11_opy_.l1111l111_opy_: l111ll1l_opy_.l1l111l111_opy_,
            l1lll11_opy_.l1llll11l_opy_: l111ll1l_opy_.l1l111lll1_opy_,
            l1lll11_opy_.l11l11l11_opy_: l111ll1l_opy_.l1l1111lll_opy_,
            l1lll11_opy_.l111ll11_opy_: l111ll1l_opy_.l1l111l1l1_opy_,
            l1lll11_opy_.l1ll1l111_opy_: l111ll1l_opy_.l1l11l1111_opy_,
            l1lll11_opy_.l1l1ll1l_opy_: l111ll1l_opy_.l1l11l1l11_opy_,
            l1lll11_opy_.l111ll111_opy_: l111ll1l_opy_.l1l11l111l_opy_,
            l1lll11_opy_.l1ll1lll_opy_: l111ll1l_opy_.l1l11111l1_opy_,
            l1lll11_opy_.l1111lll_opy_: l111ll1l_opy_.l1l111ll1l_opy_,
            l1lll11_opy_.l1l1lll11_opy_: l111ll1l_opy_.l1l11l1lll_opy_,
            l1lll11_opy_.l111l111l_opy_: l111ll1l_opy_.l1l1111111_opy_,
            l1lll11_opy_.l1llll111_opy_: l111ll1l_opy_.l11lllllll_opy_,
            l1lll11_opy_.l1lll111_opy_: l111ll1l_opy_.l1l111ll11_opy_,
            l1lll11_opy_.l111lll1l_opy_: l111ll1l_opy_.l1l11l1l1l_opy_,
            l1lll11_opy_.l111ll_opy_: l111ll1l_opy_.l1l111llll_opy_,
            l1lll11_opy_.l1l1lll1_opy_: l111ll1l_opy_.l1l1111ll1_opy_,
            l1lll11_opy_.l1l1ll11l_opy_: l111ll1l_opy_.l1l11111ll_opy_,
            l1lll11_opy_.l1lllll11_opy_: l111ll1l_opy_.l1l1111l11_opy_,
            l1lll11_opy_.l1l1l1ll_opy_: l111ll1l_opy_.l1l1111l1l_opy_,
            l1lll11_opy_.l11l1ll1_opy_: l111ll1l_opy_.l1l111l1ll_opy_,
        }
        function = l1lll1lll1_opy_.get(self.function, None)
        if function:
            return function(self)
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_FUNCTION, _("invalid function"))
    def _11llllll1_opy_(self, arg):
        if l111ll1l_opy_.l1l111l1_opy_ == l11l1l11l_opy_.l111l11l_opy_:
            return arg
        else:
            return math.radians(arg)
    def _1l111111l_opy_(self, arg):
        if l111ll1l_opy_.l1l111l1_opy_ == l11l1l11l_opy_.l1ll1ll1l_opy_:
            return math.degrees(arg)
        else:
            return arg
    def l1l11ll111_opy_(self, l11l1l111_opy_):
        return l11l1l111_opy_(self.arg.compute())
    def l1l11l1ll1_opy_(self):
        return math.sin(self._11llllll1_opy_(self.arg.compute()))
    def l1l11l11ll_opy_(self):
        return math.cos(self._11llllll1_opy_(self.arg.compute()))
    def l1l111l111_opy_(self):
        return math.tan(self._11llllll1_opy_(self.arg.compute()))
    def l1l111lll1_opy_(self):
        try:
            return 1 / math.tan(self._11llllll1_opy_(self.arg.compute()))
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO,  _("division by zero"))
    def l1l111l1l1_opy_(self):
        return self._1l111111l_opy_(self.l1l11ll111_opy_(math.asin))
    def l1l11l1111_opy_(self):
        return self._1l111111l_opy_(self.l1l11ll111_opy_(math.acos))
    def l1l11l1l11_opy_(self):
        return self._1l111111l_opy_(self.l1l11ll111_opy_(math.atan))
    def l1l11l111l_opy_(self):
        try:
            return self._1l111111l_opy_(math.atan(1 / self.arg.compute()))
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1l11111l1_opy_(self):
        return self.l1l11ll111_opy_(math.sinh)
    def l1l111ll1l_opy_(self):
        return self.l1l11ll111_opy_(math.cosh)
    def l1l11l1lll_opy_(self):
        return self.l1l11ll111_opy_(math.tanh)
    def l1l1111111_opy_(self):
        try:
            return 1 / self.l1l11ll111_opy_(math.tanh)
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l11lllllll_opy_(self):
        return self.l1l11ll111_opy_(math.asinh)
    def l1l111ll11_opy_(self):
        return self.l1l11ll111_opy_(math.acosh)
    def l1l11l1l1l_opy_(self):
        return self.l1l11ll111_opy_(math.atanh)
    def l1l111llll_opy_(self):
        try:
            return 1 / self.l1l11ll111_opy_(math.atanh)
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1l11111ll_opy_(self):
        return self.l1l11ll111_opy_(math.radians)
    def l1l1111ll1_opy_(self):
        return self.l1l11ll111_opy_(math.degrees)
    def l1l111l11l_opy_(self):
        return self.l1l11ll111_opy_(math.log)
    def l1l11l11l1_opy_(self):
        return self.l1l11ll111_opy_(math.log10)
    def l1l1111lll_opy_(self):
        return self.l1l11ll111_opy_(math.sqrt)
    def l1l1111l11_opy_(self):
        return self.arg.compute()
    def l1l1111l1l_opy_(self):
        return 0 - self.arg.compute()
    def l1l111l1ll_opy_(self):
        value = self.arg.compute()
        l1l1l1llll_opy_ = int(value)
        res = 1.0
        if (value > 0) and (value - l1l1l1llll_opy_ == 0):
            while l1l1l1llll_opy_ > 0:
                res = l1l1l1llll_opy_ * res
                l1l1l1llll_opy_ -= 1
            return res
        else:
            raise MathException(self.pos,  MathException.ErrorCode.INVALID_ARG, _("invalid argument"))