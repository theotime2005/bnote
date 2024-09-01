"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import copy
import decimal
import math
from enum import Enum, auto

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class MathResult:
    class l1lll11l1l1_opy_(Enum):
        l1lll111l1l_opy_ = auto()
        l1lll1ll111_opy_ = auto()
        l1lll1111ll_opy_ = auto()

    def __init__(self, l1lll11llll_opy_=None, l1lll1lllll_opy_=2, l1lll11l111_opy_=True, l1lll1ll1l1_opy_="en_US"):
        self.l1lll11llll_opy_ = MathResult.l1lll11l1l1_opy_.l1lll111l1l_opy_
        if l1lll11llll_opy_ == 'scientific':
            self.l1lll11llll_opy_ = MathResult.l1lll11l1l1_opy_.l1lll1ll111_opy_
        self.l1lll1lllll_opy_ = l1lll1lllll_opy_
        self.__1lll1l1111_opy_ = l1lll11l111_opy_
        self.l1lll1ll1l1_opy_ = l1lll1ll1l1_opy_

    l1lll1l11l1_opy_ = [
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97],
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47],
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47],
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37],
        [2, 3, 5, 7, 11, 13, 17, 19],
        [2, 3, 5, 7, 11, 13, 17, 19]
    ]
    l1lll1lll1l_opy_ = {
        math.pi: "{pi}",
        math.sqrt(2): "sqrt(2)",
        math.sqrt(3): "sqrt(3)",
    }
    l1lll1l11ll_opy_ = {
        math.pi: "{pi}",
        2.0 * math.pi: "2{pi}",
        3.0 * math.pi: "3{pi}",
        5.0 * math.pi: "5{pi}",
        math.sqrt(2): "sqrt(2)",
        2.0 * math.sqrt(2): "2sqrt(2)",
        3.0 * math.sqrt(2): "3sqrt(2)",
        5.0 * math.sqrt(2): "5sqrt(2)",
        7.0 * math.sqrt(2): "7sqrt(2)",
        math.sqrt(3): "sqrt(3)",
        2.0 * math.sqrt(3): "2sqrt(3)",
        3.0 * math.sqrt(3): "3sqrt(3)",
        5.0 * math.sqrt(3): "5sqrt(3)",
        7.0 * math.sqrt(3): "7sqrt(3)",
    }

    class l1lll1l1lll_opy_:
        def __init__(self, value, l1lll1l111l_opy_=None):
            self.numerator = value
            if l1lll1l111l_opy_:
                self.denominator = l1lll1l111l_opy_
            else:
                self.denominator = list()

        @staticmethod
        def new(l1lll1l1ll1_opy_):
            return MathResult.l1lll1l1lll_opy_(l1lll1l1ll1_opy_.numerator, copy.deepcopy(l1lll1l1ll1_opy_.denominator))

        def __str__(self):
            return "Fract item : numerator {} denominator {}".format(self.numerator, self.denominator)

        def level(self):
            return len(self.denominator)

        def l1lll1l1l11_opy_(self):
            result = 1
            for l1lll1l111l_opy_ in self.denominator:
                result = result * l1lll1l111l_opy_
            return result

    @staticmethod
    def l1lll11l11l_opy_(value, l1lll1l111l_opy_):
        numerator = value * l1lll1l111l_opy_
        if numerator in MathResult.l1lll1l11ll_opy_.keys():
            return True, numerator
        elif (numerator // 1) == numerator:
            return True, numerator
        else:
            return False, numerator

    @staticmethod
    def l1lll111ll1_opy_(l1lll11l1ll_opy_, level):
        l1lll111lll_opy_ = copy.deepcopy(l1lll11l1ll_opy_)
        for index, l1lll1l1ll1_opy_ in enumerate(l1lll11l1ll_opy_):
            l1lll1ll11l_opy_ = len(l1lll1l1ll1_opy_.denominator)
            if level >= l1lll1ll11l_opy_:
                for l1lll1l111l_opy_ in MathResult.l1lll1l11l1_opy_[level]:
                    if l1lll1ll11l_opy_ == 0 or l1lll1l111l_opy_ >= l1lll1l1ll1_opy_.denominator[l1lll1ll11l_opy_ - 1]:
                        l1lll11l11l_opy_, numerator = MathResult.l1lll11l11l_opy_(l1lll1l1ll1_opy_.numerator,
                                                                                  l1lll1l111l_opy_)
                        if l1lll11l11l_opy_:
                            log.info("Found frac:{}".format(l1lll1l1ll1_opy_))
                            l1lll1111l1_opy_ = MathResult.l1lll1l11ll_opy_.get(numerator, None)
                            if l1lll1111l1_opy_:
                                return True, "{}/{}".format(l1lll1111l1_opy_,
                                                            l1lll1l1ll1_opy_.l1lll1l1l11_opy_() * l1lll1l111l_opy_)
                            else:
                                return True, "{}/{}".format(int(numerator),
                                                            l1lll1l1ll1_opy_.l1lll1l1l11_opy_() * l1lll1l111l_opy_)
                        else:
                            l1lll1ll1ll_opy_ = MathResult.l1lll1l1lll_opy_.new(
                                MathResult.l1lll1l1lll_opy_(numerator, l1lll1l1ll1_opy_.denominator))
                            l1lll1ll1ll_opy_.denominator.append(l1lll1l111l_opy_)
                            l1lll111lll_opy_.append(l1lll1ll1ll_opy_)
        return False, l1lll111lll_opy_

    def display_fraction(self, value) -> (bool, str):
        if math.isnan(value):
            return False, value
        if self.__1lll1l1111_opy_ and ((value // 1) != value):
            values = MathResult.l1lll1l1lll_opy_(value)
            l1lll11lll1_opy_ = [values]
            l1lll11l11l_opy_, numerator = MathResult.l1lll11l11l_opy_(value, 1)
            if l1lll11l11l_opy_:
                l1lll1111l1_opy_ = MathResult.l1lll1l11ll_opy_.get(numerator, None)
                if l1lll1111l1_opy_:
                    return True, "{}".format(l1lll1111l1_opy_)
                else:
                    return True, "{}".format(numerator)
            level = 0
            while level < 6:
                l1lll11l11l_opy_, result = self.l1lll111ll1_opy_(l1lll11lll1_opy_, level)
                if l1lll11l11l_opy_:
                    return True, result
                else:
                    l1lll11lll1_opy_ = result
                level += 1
        if self.l1lll11llll_opy_ == MathResult.l1lll11l1l1_opy_.l1lll111l1l_opy_:
            return False, self.l1lll1lll11_opy_(value, self.l1lll1lllll_opy_)
        elif self.l1lll11llll_opy_ == MathResult.l1lll11l1l1_opy_.l1lll1ll111_opy_:
            return False, self.l1lll1llll1_opy_(value, self.l1lll1lllll_opy_)
        else:
            return False, self.l1lll1llll1_opy_(value, self.l1lll1lllll_opy_)

    def l1lll1lll11_opy_(self, value, prec):
        val = float('%.{}f'.format(prec) % value)
        if val % 1 == 0:
            return '{}'.format(int(val))
        else:
            value = '{}'.format(val)
            if self.l1lll1ll1l1_opy_ == "fr_FR":
                value = value.replace(".", ",")
            return value

    def l1lll1llll1_opy_(self, value, prec):
        """ Examples:
        formatE_decimal('0.1613965',10)
        '1.6139650000E-01'
        formatE_decimal('0.1613965',5)
        '1.61397E-01'
        formatE_decimal('0.9995',2)
        '1.00E+00'
        """
        x = "{}".format(value)
        l1lll11ll1l_opy_ = decimal.Decimal(x) if type(x) == type("") else x
        tup = l1lll11ll1l_opy_.as_tuple()
        l1lll11ll1l_opy_ = l1lll11ll1l_opy_.quantize(decimal.Decimal("1E{0}".format(len(tup[1]) + tup[2] - prec - 1)),
                                                     decimal.ROUND_HALF_UP)
        tup = l1lll11ll1l_opy_.as_tuple()
        exp = l1lll11ll1l_opy_.adjusted()
        sign = '-' if tup.sign else ''
        l1lll111l11_opy_ = ''.join(str(i) for i in tup[1][1:prec + 1]).rstrip('0')
        l1lll11ll11_opy_ = "."
        if self.l1lll1ll1l1_opy_ == "fr_FR":
            l1lll11ll11_opy_ = ","
        if (prec > 0) and (l1lll111l11_opy_ != ''):
            l1lll1l1l1l_opy_ = ''.join(
                [sign, "{}".format(tup[1][0]), l1lll11ll11_opy_, l1lll111l11_opy_, 'E', "{:+03d}".format(exp)])
        else:
            l1lll1l1l1l_opy_ = ''.join([sign, "{}".format(tup[1][0]), 'E', "{:+03d}".format(exp)])
        return l1lll1l1l1l_opy_
