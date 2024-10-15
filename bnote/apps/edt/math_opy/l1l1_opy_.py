"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import math
from .math_exception import MathException
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
l1l_opy_ = {
    'e': math.e,
    'pi': math.pi,
}
class l1l1l_opy_:
    def __init__(self):
        self.l1_opy_ = dict()
    def __str__(self):
        text = str()
        for (key, value) in self.l1_opy_.items():
            text += "key:{}, value:{}\n".format(key, value)
        return text
    @staticmethod
    def _11l1_opy_(l1ll_opy_, l11l_opy_):
        l11_opy_ = 0
        l11ll_opy_ = None
        l1ll1_opy_ = None
        for (key, value) in l11l_opy_.items():
            pos = l1ll_opy_.find(key)
            if (pos == 0) and (l11_opy_ < len(key)):
                l11_opy_ = len(key)
                l11ll_opy_ = key
                l1ll1_opy_ = value
        return l11ll_opy_, l1ll1_opy_
    def l111_opy_(self, l1ll_opy_):
        log.info("get_parameters({})".format(l1ll_opy_))
        l11ll_opy_, l1ll1_opy_ = self._11l1_opy_(l1ll_opy_, l1l_opy_)
        return l11ll_opy_, l1ll1_opy_
    def l1l11_opy_(self, l1ll_opy_):
        log.info("get_parameters_value({})".format(l1ll_opy_))
        l1ll1_opy_ = l1l_opy_.get(l1ll_opy_)
        if not l1ll1_opy_:
            l1ll1_opy_ = self.l1_opy_.get(l1ll_opy_)
        return l1ll1_opy_
    def l1lll_opy_(self, l1ll_opy_, value):
        if not isinstance(l1ll_opy_, str) or (not isinstance(value, float) and not isinstance(value, list)):
            raise MathException(-1, MathException.ErrorCode.INVALID_ASSIGNMENT, _("error during set_parameters"))
        self.l1_opy_.update({l1ll_opy_: value})
l1_opy_ = l1l1l_opy_()