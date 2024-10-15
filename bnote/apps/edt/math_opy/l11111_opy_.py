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
"""
    Multi operand function for nroot and statistic functions
"""
class l1l11l11l_opy_(Enum):
    l1l1lll111_opy_ = auto()
    l11111lll_opy_ = auto()
    l11llll_opy_ = auto()
    MAX = auto()
    l1l111111_opy_ = auto()
    l1l1111ll_opy_ = auto()
    l111llll_opy_ = auto()
    l1l1l1l1_opy_ = auto()
    l1lllllll_opy_ = auto()
    l11111l11_opy_ = auto()
    l111l1l11_opy_ = auto()
    l111lll11_opy_ = auto()
    l11ll1l1l_opy_ = auto()
    l111l111_opy_ = auto()
class l11lll1ll_opy_(l1lll1_opy_):
    def __init__(self, pos, function=None, args=None):
        l1lll1_opy_.__init__(self, pos)
        if not function or not args:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_FUNCTION, _("invalid function"))
        self.args = args
        self.function = function
    def display_tree(self, level):
        text = ''.join([('    ' * level), self.function.name, l1lll1_opy_.display_tree(self, level), "\n"])
        for arg in self.args:
            text = ''.join([text, arg.display_tree(level + 1)])
        return text
    def compute(self):
        l1lll1lll1_opy_ = {
            l1l11l11l_opy_.l1l1lll111_opy_: l11lll1ll_opy_.l1ll1l111l_opy_,
            l1l11l11l_opy_.l11111lll_opy_: l11lll1ll_opy_.l1l1ll1l11_opy_,
            l1l11l11l_opy_.l11llll_opy_: l11lll1ll_opy_.l1l1l11lll_opy_,
            l1l11l11l_opy_.MAX: l11lll1ll_opy_.l1l11ll11l_opy_,
            l1l11l11l_opy_.l1l111111_opy_: l11lll1ll_opy_.l1l1l1l11l_opy_,
            l1l11l11l_opy_.l1l1111ll_opy_: l11lll1ll_opy_.l1l1ll111l_opy_,
            l1l11l11l_opy_.l111llll_opy_: l11lll1ll_opy_.l1l1ll1ll1_opy_,
            l1l11l11l_opy_.l1l1l1l1_opy_: l11lll1ll_opy_.l1l1l1l1ll_opy_,
            l1l11l11l_opy_.l1lllllll_opy_: l11lll1ll_opy_.l1l1l1ll1l_opy_,
            l1l11l11l_opy_.l11111l11_opy_: l11lll1ll_opy_.l1l11llll1_opy_,
            l1l11l11l_opy_.l111l1l11_opy_: l11lll1ll_opy_.l1l1l111ll_opy_,
            l1l11l11l_opy_.l111lll11_opy_: l11lll1ll_opy_.l1l1ll1111_opy_,
            l1l11l11l_opy_.l11ll1l1l_opy_: l11lll1ll_opy_.l1l1l11111_opy_,
            l1l11l11l_opy_.l111l111_opy_: l11lll1ll_opy_.l1l1ll1l1l_opy_,
        }
        function = l1lll1lll1_opy_.get(self.function, None)
        if function:
            return function(self)
        else:
            raise MathException(self.pos, MathException.ErrorCode.NOT_EVALUABLE, _("function not evaluable"))
    def l1ll1l111l_opy_(self):
        try:
            l11ll1_opy_ = self.args[1].compute()
            l1ll1l11l1_opy_ = self.args[0].compute()
            if (l11ll1_opy_ < 0) and ((l11ll1_opy_ % 2) == 0):
                res = -1 * ((-1 * l11ll1_opy_) ** (1 / l1ll1l11l1_opy_))
            else:
                res = l11ll1_opy_ ** (1 / l1ll1l11l1_opy_)
            return res
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def __1l1l11ll1_opy_(self):
        values = self.args[0].compute()
        log.info("{}".format(values))
        if isinstance(values, list):
            return values
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid argument, list needed"))
    def l1l1l11lll_opy_(self):
        return l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1ll11ll_opy_, self.__1l1l11ll1_opy_())
    def l1l1ll1l11_opy_(self):
        return l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l1ll11_opy_, self.__1l1l11ll1_opy_())
    def l1l11ll11l_opy_(self):
        return l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1ll11l1_opy_, self.__1l1l11ll1_opy_())
    def l1l1l1l11l_opy_(self):
        return l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l1l111_opy_, self.__1l1l11ll1_opy_())
    @staticmethod
    def __1l1l1lll1_opy_(function, values, result=None):
        for value in values:
            if isinstance(value, list):
                result = l11lll1ll_opy_.__1l1l1lll1_opy_(function, value, result)
            else:
                result = function(value, result)
        return result
    @staticmethod
    def __1l1ll11ll_opy_(value, result):
        if result:
            return 1.0 + result
        else:
            return 1.0
    @staticmethod
    def __1l1l1ll11_opy_(value, result):
        if result:
            return value + result
        else:
            return value
    @staticmethod
    def __1l1ll11l1_opy_(value, result):
        if not result or result < value:
            result = value
        return result
    @staticmethod
    def __1l1l1l111_opy_(value, result):
        if not result or result > value:
            result = value
        return result
    @staticmethod
    def __1l1l11l11_opy_(value, result):
        if not result:
            result = [value]
        else:
            result.append(value)
        return result
    @staticmethod
    def l1l11lll1l_opy_(values):
        l1l11lll11_opy_ = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l1ll11_opy_, values)
        l1l11ll1ll_opy_ = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1ll11ll_opy_, values)
        try:
            return l1l11lll11_opy_ / l1l11ll1ll_opy_
        except ZeroDivisionError:
            raise MathException(0, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1l1ll111l_opy_(self):
        values = self.__1l1l11ll1_opy_()
        return l11lll1ll_opy_.l1l11lll1l_opy_(values)
    def l1l1ll1ll1_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        values = sorted(values)
        if len(values) == 0:
            return 0.0
        result = 0.0
        if len(values) % 2.0 == 0.0:
            index = int((len(values) / 2) - 1)
            if (index >= 0) and ((index + 1) < len(values)):
                result = (values[index] + values[index + 1]) / 2.0
        else:
            index = int(((len(values) + 1.0) / 2.0) - 1.0)
            if (index >= 0) and (index < len(values)):
                result = values[index]
        return result
    def l1l1l1l1ll_opy_(self):
        ''' Q = N / 4:
            First quartile, 25th percentile xl(Q1)
            Second quartile(Mediane), 50th percentile xm(Q2 / Qm)
            Third quartile, 75th percentile xh(Q3)
        '''
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        if len(values) > 1:
            values = sorted(values)
            index = int(len(values) / 4)
            if (index * 4) != len(values):
                index += 1
            if (index > 0) and (index <= len(values)):
                return values[index - 1]
        raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments"))
    def l1l1l1ll1l_opy_(self):
        return self.l1l1ll1ll1_opy_()
    def l1l11llll1_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        if len(values) > 1:
            values = sorted(values)
            index = int((len(values) * 3) / 4)
            if (index * 4) != int(len(values) * 3):
                index += 1
            if (index > 0) and (index <= int(len(values))):
                return values[index - 1]
        raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments"))
    def l1l1l111ll_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        return l11lll1ll_opy_.l1l11lllll_opy_(values)
    @staticmethod
    def l1l11lllll_opy_(values):
        l1l1l111l1_opy_ = l11lll1ll_opy_.l1l11lll1l_opy_(values)
        result = 0.0
        for value in values:
            value -= l1l1l111l1_opy_
            result += value * value
        try:
            return result / len(values)
        except ZeroDivisionError:
            raise MathException(0, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1l1ll1111_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        l1l11ll1l1_opy_ = l11lll1ll_opy_.l1l11lllll_opy_(values)
        if l1l11ll1l1_opy_ >= 0:
            return math.sqrt(l1l11ll1l1_opy_)
        else:
            raise MathException(self.pos, MathException.ErrorCode.NEGATIVE_SQRT, _("negative sqrt error"))
    def l1l1l11111_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        l1l1l11l1l_opy_ = self.l1l1l1111l_opy_(values)
        try:
            return (l1l1l11l1l_opy_ / self.l1l1l1l1l1_opy_(values[1])) // 1
        except ZeroDivisionError:
            raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
    def l1l1l1l1l1_opy_(self, value):
        l1l1l1llll_opy_ = value // 1
        res = 1.0
        if (value > 0) and (value - l1l1l1llll_opy_ == 0):
            while l1l1l1llll_opy_ > 0:
                res = l1l1l1llll_opy_ * res
                if math.isinf(res):
                    raise MathException(self.pos, MathException.ErrorCode.INFINITE_VALUE, _("infinite value"))
                l1l1l1llll_opy_ -= 1
            return res
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments"))
    def l1l1ll1l1l_opy_(self):
        values = l11lll1ll_opy_.__1l1l1lll1_opy_(l11lll1ll_opy_.__1l1l11l11_opy_, self.__1l1l11ll1_opy_())
        return self.l1l1l1111l_opy_(values)
    def l1l1l1111l_opy_(self, values):
        if len(values) == 2:
            if values[0] >= values[1]:
                try:
                    numerator = self.l1l1l1l1l1_opy_(values[0])
                    denominator = self.l1l1l1l1l1_opy_(values[0] - values[1])
                    return (numerator / denominator) // 1
                except ZeroDivisionError:
                    raise MathException(self.pos, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero"))
                except OverflowError:
                    raise MathException(self.pos, MathException.ErrorCode.INFINITE_VALUE, _("infinite value"))
        else:
            raise MathException(self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments"))