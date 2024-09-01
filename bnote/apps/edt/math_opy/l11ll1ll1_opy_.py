"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
from .l11_opy_ import parameters
from .l1lll1_opy_ import l1111_opy_
from .math_exception import MathException

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class l111l1l1_opy_(l1111_opy_):
    def __init__(self, pos, value=0):
        l1111_opy_.__init__(self, pos)
        if isinstance(value, str):
            self.l11ll1ll11_opy_ = value
            self.value = None
        else:
            self.l11ll1ll11_opy_ = None
            self.value = value

    def display_tree(self, level):
        if self.l11ll1ll11_opy_:
            return ''.join(['    ' * level, self.l11ll1ll11_opy_, l1111_opy_.display_tree(self, level), "\n"])
        else:
            return ''.join(['    ' * level, str(self.value), l1111_opy_.display_tree(self, level), "\n"])

    def compute(self):
        if self.l11ll1ll11_opy_:
            value = parameters.l11ll_opy_(self.l11ll1ll11_opy_)
            if not value:
                raise MathException(self.pos, MathException.ErrorCode.UNDEFINED_PARAM, _("undefined parameters"))
            return value
        else:
            return self.value
