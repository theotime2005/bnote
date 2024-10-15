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
class l1ll1l1ll_opy_(Enum):
    l1ll1lllll1_opy_ = auto()
    l1l11l111_opy_ = auto()
class l1l1l111_opy_(l1lll1_opy_):
    def __init__(self, pos, l1lllll1l1_opy_=l1ll1l1ll_opy_.l1l11l111_opy_, l1llllll1l_opy_=None):
        l1lll1_opy_.__init__(self, pos)
        self.arg = l1llllll1l_opy_
        self.l1lllll1l1_opy_ = l1lllll1l1_opy_
    def display_tree(self, level):
        return ''.join(['    ' * level, self.l1lllll1l1_opy_.name, l1lll1_opy_.display_tree(self, level), "\n",
                        self.arg.display_tree(level + 1)])
    def compute(self):
        l1lll1lll1_opy_ = {
            l1ll1l1ll_opy_.l1ll1lllll1_opy_: l1l1l111_opy_.l1lllll111_opy_,
            l1ll1l1ll_opy_.l1l11l111_opy_: l1l1l111_opy_.l1llll1l1l_opy_,
        }
        function = l1lll1lll1_opy_.get(self.l1lllll1l1_opy_, None)
        if function:
            return function(self)
        else:
            msg = _("function not evaluable")
            log.warning(msg)
            raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("function not evaluable"))
    def l1lllll111_opy_(self):
        return self.arg.compute()
    def l1llll1l1l_opy_(self):
        return -1 * self.arg.compute()