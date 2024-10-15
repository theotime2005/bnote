"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from enum import Enum, auto
from .l1llll_opy_ import l1lll1_opy_
from .l11111l_opy_ import l111111ll_opy_
from .l1l1_opy_ import l1l1l_opy_, l1_opy_
from .math_exception import MathException
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
class l111l11_opy_(Enum):
    l1lllll11_opy_ = auto()
    l1l1l1ll_opy_ = auto()
    l11ll11l1_opy_ = auto()
    l1llll1ll1_opy_ = auto()
    l1l1111l1_opy_ = auto()
    l1llll11l1_opy_ = auto()
    l111111_opy_ = auto()
    l1llllll_opy_ = auto()
    l1ll11ll_opy_ = auto()
    l111ll1l1_opy_ = auto()
class l111l1l_opy_(l1lll1_opy_):
    def __init__(self, pos, l1lllll1l1_opy_=l111l11_opy_.l1l1l1ll_opy_, l1llllll1l_opy_=None, l1lllll1ll_opy_=None):
        l1lll1_opy_.__init__(self, pos)
        self.l1lll1llll_opy_ = l1llllll1l_opy_
        self.l1llll111l_opy_ = l1lllll1ll_opy_
        self.l1lllll1l1_opy_ = l1lllll1l1_opy_
    def display_tree(self, level):
        return ''.join(['    ' * level, self.l1lllll1l1_opy_.name, l1lll1_opy_.display_tree(self, level), "\n",
                        self.l1lll1llll_opy_.display_tree(level + 1),
                        self.l1llll111l_opy_.display_tree(level + 1)])
    def compute(self):
        l1lll1lll1_opy_ = {
            l111l11_opy_.l1lllll11_opy_: l111l1l_opy_.l1lllll111_opy_,
            l111l11_opy_.l1l1l1ll_opy_: l111l1l_opy_.l1llll1l1l_opy_,
            l111l11_opy_.l11ll11l1_opy_: l111l1l_opy_.l1llllll11_opy_,
            l111l11_opy_.l1llll1ll1_opy_: l111l1l_opy_.l1llllll11_opy_,
            l111l11_opy_.l1l1111l1_opy_: l111l1l_opy_.l1llll11ll_opy_,
            l111l11_opy_.l1llll11l1_opy_: l111l1l_opy_.l1llll11ll_opy_,
            l111l11_opy_.l111111_opy_: l111l1l_opy_.l1lllllll1_opy_,
            l111l11_opy_.l1llllll_opy_: l111l1l_opy_.l1llll1l11_opy_,
            l111l11_opy_.l1ll11ll_opy_: l111l1l_opy_.l1lll1ll1l_opy_,
            l111l11_opy_.l111ll1l1_opy_: l111l1l_opy_.l1lllll11l_opy_,
        }
        function = l1lll1lll1_opy_.get(self.l1lllll1l1_opy_, None)
        if function:
            return function(self)
        else:
            msg = _("function not evaluable")
            log.warning(msg)
            raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("function not evaluable"))
    def l1lllll111_opy_(self):
        return self.l1lll1llll_opy_.compute() + self.l1llll111l_opy_.compute()
    def l1llll1l1l_opy_(self):
        return self.l1lll1llll_opy_.compute() - self.l1llll111l_opy_.compute()
    def l1llllll11_opy_(self):
        return self.l1lll1llll_opy_.compute() * self.l1llll111l_opy_.compute()
    def l1llll11ll_opy_(self):
        try:
            return self.l1lll1llll_opy_.compute() / self.l1llll111l_opy_.compute()
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1lllllll1_opy_(self):
        value = self.l1llll111l_opy_.compute()
        if not isinstance(self.l1lll1llll_opy_, l111111ll_opy_):
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ASSIGNMENT, _("assignment must be only into parameter"))
        else:
            l1_opy_.l1lll_opy_(self.l1lll1llll_opy_.l1llllllll_opy_, value)
        return value
    def l1llll1l11_opy_(self):
        value = self.l1llll111l_opy_.compute()
        l1llll1111_opy_ = self.l1lll1llll_opy_.compute()
        l1llll1lll_opy_ = int(l1llll1111_opy_ // 1)
        if l1llll1lll_opy_ == l1llll1111_opy_:
            return [value] * l1llll1lll_opy_
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("weighted arithmetic mean invalid"))
    def l1lll1ll1l_opy_(self):
        return self.l1lll1llll_opy_.compute() % self.l1llll111l_opy_.compute()
    def l1lllll11l_opy_(self):
        return self.l1lll1llll_opy_.compute() ** int(self.l1llll111l_opy_.compute())