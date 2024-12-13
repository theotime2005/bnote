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
"""
    Multi operand function for nroot and statistic functions
"""


class l1111l1l_opy_(Enum):
    l111l11lll_opy_ = auto()
    l1ll1ll1l_opy_ = auto()
    l1l11ll11_opy_ = auto()
    MAX = auto()
    l11llllll_opy_ = auto()
    l11111lll_opy_ = auto()
    l1ll11l_opy_ = auto()
    l1l1lllll_opy_ = auto()
    l11ll1l_opy_ = auto()
    l1ll1l1_opy_ = auto()
    l1ll11ll_opy_ = auto()
    l1l111l11_opy_ = auto()
    l1ll11l11_opy_ = auto()
    l1111l11_opy_ = auto()


class l1l11l1_opy_(l1111_opy_):
    def __init__(self, pos, function=None, args=None):
        l1111_opy_.__init__(self, pos)
        if not function or not args:
            raise MathException(
                self.pos,
                MathException.ErrorCode.INVALID_FUNCTION,
                _("invalid function"),
            )
        self.args = args
        self.function = function

    def display_tree(self, level):
        text = "".join(
            [
                ("    " * level),
                self.function.name,
                l1111_opy_.display_tree(self, level),
                "\n",
            ]
        )
        for arg in self.args:
            text = "".join([text, arg.display_tree(level + 1)])
        return text

    def compute(self):
        l11l1ll1l1_opy_ = {
            l1111l1l_opy_.l111l11lll_opy_: l1l11l1_opy_.l111llll1l_opy_,
            l1111l1l_opy_.l1ll1ll1l_opy_: l1l11l1_opy_.l1111l1l11_opy_,
            l1111l1l_opy_.l1l11ll11_opy_: l1l11l1_opy_.l11111l11l_opy_,
            l1111l1l_opy_.MAX: l1l11l1_opy_.l11111ll11_opy_,
            l1111l1l_opy_.l11llllll_opy_: l1l11l1_opy_.l11111ll1l_opy_,
            l1111l1l_opy_.l11111lll_opy_: l1l11l1_opy_.l111111lll_opy_,
            l1111l1l_opy_.l1ll11l_opy_: l1l11l1_opy_.l111l1111l_opy_,
            l1111l1l_opy_.l1l1lllll_opy_: l1l11l1_opy_.l1111lll11_opy_,
            l1111l1l_opy_.l11ll1l_opy_: l1l11l1_opy_.l1111l1111_opy_,
            l1111l1l_opy_.l1ll1l1_opy_: l1l11l1_opy_.l1111ll11l_opy_,
            l1111l1l_opy_.l1ll11ll_opy_: l1l11l1_opy_.l1111lllll_opy_,
            l1111l1l_opy_.l1l111l11_opy_: l1l11l1_opy_.l1111l1lll_opy_,
            l1111l1l_opy_.l1ll11l11_opy_: l1l11l1_opy_.l1111lll1l_opy_,
            l1111l1l_opy_.l1111l11_opy_: l1l11l1_opy_.l1111llll1_opy_,
        }
        function = l11l1ll1l1_opy_.get(self.function, None)
        if function:
            return function(self)
        else:
            raise MathException(
                self.pos,
                MathException.ErrorCode.NOT_EVALUABLE,
                _("function not evaluable"),
            )

    def l111llll1l_opy_(self):
        try:
            l1lll1l11_opy_ = self.args[1].compute()
            l111llllll_opy_ = self.args[0].compute()
            if (l1lll1l11_opy_ < 0) and ((l1lll1l11_opy_ % 2) == 0):
                res = -1 * ((-1 * l1lll1l11_opy_) ** (1 / l111llllll_opy_))
            else:
                res = l1lll1l11_opy_ ** (1 / l111llllll_opy_)
            return res
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def __111l11111_opy_(self):
        values = self.args[0].compute()
        log.info("{}".format(values))
        if isinstance(values, list):
            return values
        else:
            raise MathException(
                self.pos,
                MathException.ErrorCode.INVALID_ARG,
                _("invalid argument, list needed"),
            )

    def l11111l11l_opy_(self):
        return l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__1111l11ll_opy_, self.__111l11111_opy_()
        )

    def l1111l1l11_opy_(self):
        return l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__11111l1l1_opy_, self.__111l11111_opy_()
        )

    def l11111ll11_opy_(self):
        return l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__11111lll1_opy_, self.__111l11111_opy_()
        )

    def l11111ll1l_opy_(self):
        return l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__1111ll1ll_opy_, self.__111l11111_opy_()
        )

    @staticmethod
    def __1111ll1l1_opy_(function, values, result=None):
        for value in values:
            if isinstance(value, list):
                result = l1l11l1_opy_.__1111ll1l1_opy_(function, value, result)
            else:
                result = function(value, result)
        return result

    @staticmethod
    def __1111l11ll_opy_(value, result):
        if result:
            return 1.0 + result
        else:
            return 1.0

    @staticmethod
    def __11111l1l1_opy_(value, result):
        if result:
            return value + result
        else:
            return value

    @staticmethod
    def __11111lll1_opy_(value, result):
        if not result or result < value:
            result = value
        return result

    @staticmethod
    def __1111ll1ll_opy_(value, result):
        if not result or result > value:
            result = value
        return result

    @staticmethod
    def __111l111ll_opy_(value, result):
        if not result:
            result = [value]
        else:
            result.append(value)
        return result

    @staticmethod
    def l11111l111_opy_(values):
        l1111l1l1l_opy_ = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__11111l1l1_opy_, values
        )
        l111111ll1_opy_ = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__1111l11ll_opy_, values
        )
        try:
            return l1111l1l1l_opy_ / l111111ll1_opy_
        except ZeroDivisionError:
            raise MathException(
                0, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero")
            )

    def l111111lll_opy_(self):
        values = self.__111l11111_opy_()
        return l1l11l1_opy_.l11111l111_opy_(values)

    def l111l1111l_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
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

    def l1111lll11_opy_(self):
        """Q = N / 4:
        First quartile, 25th percentile xl(Q1)
        Second quartile(Mediane), 50th percentile xm(Q2 / Qm)
        Third quartile, 75th percentile xh(Q3)
        """
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        if len(values) > 1:
            values = sorted(values)
            index = int(len(values) / 4)
            if (index * 4) != len(values):
                index += 1
            if (index > 0) and (index <= len(values)):
                return values[index - 1]
        raise MathException(
            self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments")
        )

    def l1111l1111_opy_(self):
        return self.l111l1111l_opy_()

    def l1111ll11l_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        if len(values) > 1:
            values = sorted(values)
            index = int((len(values) * 3) / 4)
            if (index * 4) != int(len(values) * 3):
                index += 1
            if (index > 0) and (index <= int(len(values))):
                return values[index - 1]
        raise MathException(
            self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments")
        )

    def l1111lllll_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        return l1l11l1_opy_.l11111l1ll_opy_(values)

    @staticmethod
    def l11111l1ll_opy_(values):
        l1111l1ll1_opy_ = l1l11l1_opy_.l11111l111_opy_(values)
        result = 0.0
        for value in values:
            value -= l1111l1ll1_opy_
            result += value * value
        try:
            return result / len(values)
        except ZeroDivisionError:
            raise MathException(
                0, MathException.ErrorCode.DIVISION_BY_ZERO, _("division by zero")
            )

    def l1111l1lll_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        l1111l111l_opy_ = l1l11l1_opy_.l11111l1ll_opy_(values)
        if l1111l111l_opy_ >= 0:
            return math.sqrt(l1111l111l_opy_)
        else:
            raise MathException(
                self.pos,
                MathException.ErrorCode.NEGATIVE_SQRT,
                _("negative sqrt error"),
            )

    def l1111lll1l_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        l11111llll_opy_ = self.l1111l11l1_opy_(values)
        try:
            return (l11111llll_opy_ / self.l1111ll111_opy_(values[1])) // 1
        except ZeroDivisionError:
            raise MathException(
                self.pos,
                MathException.ErrorCode.DIVISION_BY_ZERO,
                _("division by zero"),
            )

    def l1111ll111_opy_(self, value):
        l111l111l1_opy_ = value // 1
        res = 1.0
        if (value > 0) and (value - l111l111l1_opy_ == 0):
            while l111l111l1_opy_ > 0:
                res = l111l111l1_opy_ * res
                if math.isinf(res):
                    raise MathException(
                        self.pos,
                        MathException.ErrorCode.INFINITE_VALUE,
                        _("infinite value"),
                    )
                l111l111l1_opy_ -= 1
            return res
        else:
            raise MathException(
                self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments")
            )

    def l1111llll1_opy_(self):
        values = l1l11l1_opy_.__1111ll1l1_opy_(
            l1l11l1_opy_.__111l111ll_opy_, self.__111l11111_opy_()
        )
        return self.l1111l11l1_opy_(values)

    def l1111l11l1_opy_(self, values):
        if len(values) == 2:
            if values[0] >= values[1]:
                try:
                    numerator = self.l1111ll111_opy_(values[0])
                    denominator = self.l1111ll111_opy_(values[0] - values[1])
                    return (numerator / denominator) // 1
                except ZeroDivisionError:
                    raise MathException(
                        self.pos,
                        MathException.ErrorCode.DIVISION_BY_ZERO,
                        _("division by zero"),
                    )
                except OverflowError:
                    raise MathException(
                        self.pos,
                        MathException.ErrorCode.INFINITE_VALUE,
                        _("infinite value"),
                    )
        else:
            raise MathException(
                self.pos, MathException.ErrorCode.INVALID_ARG, _("invalid arguments")
            )
