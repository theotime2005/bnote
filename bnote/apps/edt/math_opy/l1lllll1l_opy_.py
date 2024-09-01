"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from enum import Enum, auto

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
from .l11_opy_ import parameters
from .l11ll1ll1_opy_ import l111l1l1_opy_
from .l1lll1_opy_ import l1111_opy_
from .math_exception import MathException

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class l11lll1l_opy_(Enum):
    l1ll1l11l_opy_ = auto()
    l1ll111ll_opy_ = auto()
    l1111l_opy_ = auto()
    l11ll1l111_opy_ = auto()
    l1l1l1l1_opy_ = auto()
    l11ll1l1ll_opy_ = auto()
    l1llll1_opy_ = auto()
    l11l11l1_opy_ = auto()
    l11l1111_opy_ = auto()
    l111111ll_opy_ = auto()


class l1l1lll11_opy_(l1111_opy_):
    def __init__(self, pos, l11ll1l11l_opy_=l11lll1l_opy_.l1ll111ll_opy_, l11l1lll1l_opy_=None, l11l1llll1_opy_=None):
        l1111_opy_.__init__(self, pos)
        self.l11l1lll11_opy_ = l11l1lll1l_opy_
        self.l11ll11l1l_opy_ = l11l1llll1_opy_
        self.l11ll1l11l_opy_ = l11ll1l11l_opy_

    def display_tree(self, level):
        return ''.join(['    ' * level, self.l11ll1l11l_opy_.name, l1111_opy_.display_tree(self, level), "\n",
                        self.l11l1lll11_opy_.display_tree(level + 1),
                        self.l11ll11l1l_opy_.display_tree(level + 1)])

    def compute(self):
        l11l1ll1l1_opy_ = {
            l11lll1l_opy_.l1ll1l11l_opy_: l1l1lll11_opy_.l11l1lllll_opy_,
            l11lll1l_opy_.l1ll111ll_opy_: l1l1lll11_opy_.l11l1ll1ll_opy_,
            l11lll1l_opy_.l1111l_opy_: l1l1lll11_opy_.l11ll111ll_opy_,
            l11lll1l_opy_.l11ll1l111_opy_: l1l1lll11_opy_.l11ll111ll_opy_,
            l11lll1l_opy_.l1l1l1l1_opy_: l1l1lll11_opy_.l11ll1l1l1_opy_,
            l11lll1l_opy_.l11ll1l1ll_opy_: l1l1lll11_opy_.l11ll1l1l1_opy_,
            l11lll1l_opy_.l1llll1_opy_: l1l1lll11_opy_.l11ll11111_opy_,
            l11lll1l_opy_.l11l11l1_opy_: l1l1lll11_opy_.l11ll111l1_opy_,
            l11lll1l_opy_.l11l1111_opy_: l1l1lll11_opy_.l11ll1111l_opy_,
            l11lll1l_opy_.l111111ll_opy_: l1l1lll11_opy_.l11ll11l11_opy_,
        }
        function = l11l1ll1l1_opy_.get(self.l11ll1l11l_opy_, None)
        if function:
            return function(self)
        else:
            msg = _("function not evaluable")
            log.warning(msg)
            raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("function not evaluable"))

    def l11l1lllll_opy_(self):
        return self.l11l1lll11_opy_.compute() + self.l11ll11l1l_opy_.compute()

    def l11l1ll1ll_opy_(self):
        return self.l11l1lll11_opy_.compute() - self.l11ll11l1l_opy_.compute()

    def l11ll111ll_opy_(self):
        return self.l11l1lll11_opy_.compute() * self.l11ll11l1l_opy_.compute()

    def l11ll1l1l1_opy_(self):
        try:
            return self.l11l1lll11_opy_.compute() / self.l11ll11l1l_opy_.compute()
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))

    def l11ll11111_opy_(self):
        value = self.l11ll11l1l_opy_.compute()
        if not isinstance(self.l11l1lll11_opy_, l111l1l1_opy_):
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ASSIGNMENT,
                                _("assignment must be only into parameter"))
        else:
            parameters.l1l1l_opy_(self.l11l1lll11_opy_.l11ll1ll11_opy_, value)
        return value

    def l11ll111l1_opy_(self):
        value = self.l11ll11l1l_opy_.compute()
        l11ll11ll1_opy_ = self.l11l1lll11_opy_.compute()
        l11ll11lll_opy_ = int(l11ll11ll1_opy_ // 1)
        if l11ll11lll_opy_ == l11ll11ll1_opy_:
            return [value] * l11ll11lll_opy_
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("weighted arithmetic mean invalid"))

    def l11ll1111l_opy_(self):
        return self.l11l1lll11_opy_.compute() % self.l11ll11l1l_opy_.compute()

    def l11ll11l11_opy_(self):
        return self.l11l1lll11_opy_.compute() ** int(self.l11ll11l1l_opy_.compute())
