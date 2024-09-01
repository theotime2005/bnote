"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import math

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG
from .math_exception import MathException

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)
l1l_opy_ = {
    'e': math.e,
    'pi': math.pi,
}


class l111_opy_:
    def __init__(self):
        self.parameters = dict()

    def __str__(self):
        text = str()
        for (key, value) in self.parameters.items():
            text += "key:{}, value:{}\n".format(key, value)
        return text

    @staticmethod
    def _1l11_opy_(l1lll_opy_, l1ll_opy_):
        l1_opy_ = 0
        ll_opy_ = None
        l1ll1_opy_ = None
        for (key, value) in l1ll_opy_.items():
            pos = l1lll_opy_.find(key)
            if (pos == 0) and (l1_opy_ < len(key)):
                l1_opy_ = len(key)
                ll_opy_ = key
                l1ll1_opy_ = value
        return ll_opy_, l1ll1_opy_

    def l1l1_opy_(self, l1lll_opy_):
        log.info("get_parameters({})".format(l1lll_opy_))
        ll_opy_, l1ll1_opy_ = self._1l11_opy_(l1lll_opy_, l1l_opy_)
        return ll_opy_, l1ll1_opy_

    def l11ll_opy_(self, l1lll_opy_):
        log.info("get_parameters_value({})".format(l1lll_opy_))
        l1ll1_opy_ = l1l_opy_.get(l1lll_opy_)
        if not l1ll1_opy_:
            l1ll1_opy_ = self.parameters.get(l1lll_opy_)
        return l1ll1_opy_

    def l1l1l_opy_(self, l1lll_opy_, value):
        if not isinstance(l1lll_opy_, str) or (not isinstance(value, float) and not isinstance(value, list)):
            raise MathException(-1, MathException.ErrorCode.INVALID_ASSIGNMENT, _("error during set_parameters"))
        self.parameters.update({l1lll_opy_: value})


parameters = l111_opy_()
