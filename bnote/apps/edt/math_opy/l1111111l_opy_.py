"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from enum import Enum, auto

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
from .l111l_opy_ import l1llll_opy_
from .math_exception import MathException

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class l111l11l_opy_(Enum):
    l1ll1lll1ll_opy_ = auto()
    l1lll1l1_opy_ = auto()


class l11l11l1l_opy_(l1llll_opy_):
    def __init__(self, pos, l11ll1111l_opy_=l111l11l_opy_.l1lll1l1_opy_, l11l1ll1l1_opy_=None):
        l1llll_opy_.__init__(self, pos)
        self.arg = l11l1ll1l1_opy_
        self.l11ll1111l_opy_ = l11ll1111l_opy_

    def display_tree(self, level):
        return ''.join(['    ' * level, self.l11ll1111l_opy_.name, l1llll_opy_.display_tree(self, level), "\n",
                        self.arg.display_tree(level + 1)])

    def compute(self):
        l11ll111l1_opy_ = {
            l111l11l_opy_.l1ll1lll1ll_opy_: l11l11l1l_opy_.l11l1ll1ll_opy_,
            l111l11l_opy_.l1lll1l1_opy_: l11l11l1l_opy_.l11ll11lll_opy_,
        }
        function = l11ll111l1_opy_.get(self.l11ll1111l_opy_, None)
        if function:
            return function(self)
        else:
            msg = _("function not evaluable")
            log.warning(msg)
            raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("function not evaluable"))

    def l11l1ll1ll_opy_(self):
        return self.arg.compute()

    def l11ll11lll_opy_(self):
        return -1 * self.arg.compute()
