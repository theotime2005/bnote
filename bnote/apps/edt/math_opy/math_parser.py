"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import re

from .braille import b15, b36, b46, b157
# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG
from .l1111ll11_opy_ import l11l1111l_opy_, l11l1llll_opy_
from .l111l111l_opy_ import l1lll11ll_opy_
from .l111lll1l1_opy_ import l111lll11l_opy_
from .l111lll1l_opy_ import l1lll111l_opy_, l1111l1ll_opy_
from .l11_opy_ import parameters
from .l11ll1ll1_opy_ import l111l1l1_opy_
from .l1l1l1_opy_ import l1l111_opy_
from .l1l1l1ll1_opy_ import l1l11l1_opy_, l1111l1l_opy_
from .l1ll1lll_opy_ import l1ll11111_opy_, l1l11111l_opy_
from .l1llll_opy_ import l11l1_opy_
from .l1lllll1l_opy_ import l1l1lll11_opy_, l11lll1l_opy_
from .math_exception import MathException
from .math_exception import MathInjectionException, MathUnaryException

log = ColoredLogger(__name__, level=MATH_LOG)
'''
-----------------------------------------------------------
Math Braille definitions.
-----------------------------------------------------------
'''


class MathBrailleTable:
    l111ll1l1l_opy_ = "braille"
    l1111ll_opy_ = l111lll11l_opy_.l111l1l1l_opy_
    l1llllll_opy_ = {
        l111lll11l_opy_.l1l1l1l11_opy_: (l111lll11l_opy_.l111ll11l_opy_, l1111l1ll_opy_.l1l11ll1_opy_),
        l111lll11l_opy_.l1l1ll1l1_opy_: (l111lll11l_opy_.l1ll1ll_opy_, l1111l1ll_opy_.l1111lll1_opy_),
        l111lll11l_opy_.l1lllll11_opy_: (l111lll11l_opy_.l1l1l11ll_opy_, l1111l1ll_opy_.l111ll11_opy_),
        l111lll11l_opy_.l111l1l1ll_opy_: (l111lll11l_opy_.l111l1ll1l_opy_, l1111l1ll_opy_.l111l1l11_opy_),
        l111lll11l_opy_.l11l1ll11l_opy_: (l111lll11l_opy_.l11l11ll11_opy_, l1111l1ll_opy_.l111lllll_opy_),
    }
    l11l111l_opy_ = {
        l111lll11l_opy_.l1ll111l1_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1llll1_opy_),
        l111lll11l_opy_.l11l11l1_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l11l11l1_opy_),
        l111lll11l_opy_.l111lll11_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1ll1l11l_opy_),
        l111lll11l_opy_.l1l11l1l_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1ll111ll_opy_),
        '\u2212': (l11l1111l_opy_, l11l1llll_opy_.l1lllllll_opy_),
        l111lll11l_opy_.l11l1ll1_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1l1l1l1_opy_),
        l111lll11l_opy_.l111ll111_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1l1l1l1_opy_),
        l111lll11l_opy_.l111l1ll_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l11l1111_opy_),
        l111lll11l_opy_.l11ll1l1l_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1111l_opy_),
        l111lll11l_opy_.l1ll1111_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l1111l_opy_),
        l111lll11l_opy_.l111ll1l11_opy_: (l1l1lll11_opy_, l11lll1l_opy_.l111111ll_opy_),
        l111lll11l_opy_.l11l11ll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1l1ll11_opy_),
        l111lll11l_opy_.l11111l11_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1l11lll_opy_),
        l111lll11l_opy_.l1l111l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11lll1ll_opy_),
        l111lll11l_opy_.l1llll11_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1lll1l1_opy_),
        l111lll11l_opy_.l11111111_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1ll11ll1_opy_),
        l111lll11l_opy_.l11l11l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l111ll_opy_),
        l111lll11l_opy_.l111ll1111_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11lll1ll_opy_),
        l111lll11l_opy_.l111l1l1l1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1lll1l1_opy_),
        l111lll11l_opy_.l111l1l111_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1ll11ll1_opy_),
        l111lll11l_opy_.l111llll11_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l111ll_opy_),
        l111lll11l_opy_.l111l1lll_opy_: (l1ll11111_opy_, l1l11111l_opy_.l111l11l1_opy_),
        l111lll11l_opy_.l1111l11l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l11111_opy_),
        l111lll11l_opy_.l11ll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11lll1l1_opy_),
        l111lll11l_opy_.l1l1l1l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11111_opy_),
        l111lll11l_opy_.l111l11ll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l111l11l1_opy_),
        l111lll11l_opy_.l111l1llll_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l11111_opy_),
        l111lll11l_opy_.l111ll1lll_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11lll1l1_opy_),
        l111lll11l_opy_.l111ll111l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11111_opy_),
        l111lll11l_opy_.l111111_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1111l1_opy_),
        l111lll11l_opy_.l11l1lll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1lll1ll1_opy_),
        l111lll11l_opy_.l1l111ll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1l11ll_opy_),
        l111lll11l_opy_.l1llll1l1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l111l1ll1_opy_),
        l111lll11l_opy_.l11l11l11_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11ll11l1_opy_),
        l111lll11l_opy_.l11ll1l1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11ll1l11_opy_),
        l111lll11l_opy_.l11111ll1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l1l111_opy_),
        l111lll11l_opy_.l11l1l11l_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1l11111_opy_),
        l111lll11l_opy_.l111l11l11_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1llll1l_opy_),
        l111lll11l_opy_.l111l111_opy_: (l1ll11111_opy_, l1l11111l_opy_.l1ll1l1ll_opy_),
        l111lll11l_opy_.l1l1111ll_opy_: (l1ll11111_opy_, l1l11111l_opy_.l11l1l1_opy_),
        l111lll11l_opy_.l1l111l1_opy_: (l1ll11111_opy_, l1l11111l_opy_.l111l11_opy_),
        l111lll11l_opy_.l111l1l1l_opy_: (l11l1_opy_, None),
        l111lll11l_opy_.l111ll11ll_opy_: (l1l11l1_opy_, l1111l1l_opy_.l111l11lll_opy_),
        l111lll11l_opy_.l1lllll1_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1ll1ll1l_opy_),
        l111lll11l_opy_.l1111111l_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1l11ll11_opy_),
        l111lll11l_opy_.l1l1l11l_opy_: (l1l11l1_opy_, l1111l1l_opy_.MAX),
        l111lll11l_opy_.l1ll1l111_opy_: (l1l11l1_opy_, l1111l1l_opy_.l11llllll_opy_),
        l111lll11l_opy_.l11l1l11_opy_: (l1l11l1_opy_, l1111l1l_opy_.l11111lll_opy_),
        l111lll11l_opy_.l1l1ll11l_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1ll11l_opy_),
        l111lll11l_opy_.l1llll1ll_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1l1lllll_opy_),
        l111lll11l_opy_.l1ll111l_opy_: (l1l11l1_opy_, l1111l1l_opy_.l11ll1l_opy_),
        l111lll11l_opy_.l111111l1_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1ll1l1_opy_),
        l111lll11l_opy_.l1llll111_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1ll11ll_opy_),
        l111lll11l_opy_.l1l11l111_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1l111l11_opy_),
        l111lll11l_opy_.l1lll111_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1ll11l11_opy_),
        l111lll11l_opy_.l11ll11l_opy_: (l1l11l1_opy_, l1111l1l_opy_.l1111l11_opy_),
        ''.join([b157, b36]): (None, None),
        ''.join([b46, b15, b36]): (None, None),
    }
    l111lll1_opy_ = {
        l111lll11l_opy_.l1l1l111l_opy_: 'pi',
    }


'''
-----------------------------------------------------------
Math Text definitions.
-----------------------------------------------------------
'''


class MathTextTable:
    l111ll1l1l_opy_ = "text"
    l1111ll_opy_ = ";"
    l1llllll_opy_ = {
        '{': ('}', l1111l1ll_opy_.l111lllll_opy_),
        '(': (')', l1111l1ll_opy_.l1l11ll1_opy_),
        '[': (']', l1111l1ll_opy_.l1111lll1_opy_),
        # '{': ('}', l1111l1ll_opy_.l111ll11_opy_)
    }
    l11l111l_opy_ = {
        '=': (l1l1lll11_opy_, l11lll1l_opy_.l1llll1_opy_),
        '+': (l1l1lll11_opy_, l11lll1l_opy_.l1ll1l11l_opy_),
        '-': (l1l1lll11_opy_, l11lll1l_opy_.l1ll111ll_opy_),
        '\u2212': (l11l1111l_opy_, l11l1llll_opy_.l1lllllll_opy_),
        '*': (l1l1lll11_opy_, l11lll1l_opy_.l1111l_opy_),
        '/': (l1l1lll11_opy_, l11lll1l_opy_.l1l1l1l1_opy_),
        '%': (l1l1lll11_opy_, l11lll1l_opy_.l11l1111_opy_),
        '\u00D7': (l1l1lll11_opy_, l11lll1l_opy_.l1111l_opy_),
        '^': (l1l1lll11_opy_, l11lll1l_opy_.l111111ll_opy_),
        'ln': (l1ll11111_opy_, l1l11111l_opy_.l1l1ll11_opy_),
        'log': (l1ll11111_opy_, l1l11111l_opy_.l1l11lll_opy_),
        'sin': (l1ll11111_opy_, l1l11111l_opy_.l11lll1ll_opy_),
        'cos': (l1ll11111_opy_, l1l11111l_opy_.l1lll1l1_opy_),
        'tan': (l1ll11111_opy_, l1l11111l_opy_.l1ll11ll1_opy_),
        'cot': (l1ll11111_opy_, l1l11111l_opy_.l11l111ll_opy_),
        'asin': (l1ll11111_opy_, l1l11111l_opy_.l111l11l1_opy_),
        'acos': (l1ll11111_opy_, l1l11111l_opy_.l11l11111_opy_),
        'atan': (l1ll11111_opy_, l1l11111l_opy_.l11lll1l1_opy_),
        'acot': (l1ll11111_opy_, l1l11111l_opy_.l11111_opy_),
        'sh': (l1ll11111_opy_, l1l11111l_opy_.l1111l1_opy_),
        'ch': (l1ll11111_opy_, l1l11111l_opy_.l1lll1ll1_opy_),
        'th': (l1ll11111_opy_, l1l11111l_opy_.l1l11ll_opy_),
        'sinh': (l1ll11111_opy_, l1l11111l_opy_.l1111l1_opy_),
        'cosh': (l1ll11111_opy_, l1l11111l_opy_.l1lll1ll1_opy_),
        'tanh': (l1ll11111_opy_, l1l11111l_opy_.l1l11ll_opy_),
        'coth': (l1ll11111_opy_, l1l11111l_opy_.l111l1ll1_opy_),
        'ash': (l1ll11111_opy_, l1l11111l_opy_.l11ll11l1_opy_),
        'ach': (l1ll11111_opy_, l1l11111l_opy_.l11ll1l11_opy_),
        'ath': (l1ll11111_opy_, l1l11111l_opy_.l11l1l111_opy_),
        'asinh': (l1ll11111_opy_, l1l11111l_opy_.l11ll11l1_opy_),
        'acosh': (l1ll11111_opy_, l1l11111l_opy_.l11ll1l11_opy_),
        'atanh': (l1ll11111_opy_, l1l11111l_opy_.l11l1l111_opy_),
        'acoth': (l1ll11111_opy_, l1l11111l_opy_.l1l11111_opy_),
        'sqrt': (l1ll11111_opy_, l1l11111l_opy_.l1llll1l_opy_),
        'deg': (l1ll11111_opy_, l1l11111l_opy_.l1ll1l1ll_opy_),
        'rad': (l1ll11111_opy_, l1l11111l_opy_.l11l1l1_opy_),
        '!': (l1ll11111_opy_, l1l11111l_opy_.l111l11_opy_),
        'nroot': (l1l11l1_opy_, l1111l1l_opy_.l111l11lll_opy_),
        'E-': (None, None),
        ";": (l11l1_opy_, None),
        "->": (l1l1lll11_opy_, l11lll1l_opy_.l11l11l1_opy_),
        "sum": (l1l11l1_opy_, l1111l1l_opy_.l1ll1ll1l_opy_),
        "nbr": (l1l11l1_opy_, l1111l1l_opy_.l1l11ll11_opy_),
        "max": (l1l11l1_opy_, l1111l1l_opy_.MAX),
        "min": (l1l11l1_opy_, l1111l1l_opy_.l11llllll_opy_),
        "ave": (l1l11l1_opy_, l1111l1l_opy_.l11111lll_opy_),
        "med": (l1l11l1_opy_, l1111l1l_opy_.l1ll11l_opy_),
        "qua1": (l1l11l1_opy_, l1111l1l_opy_.l1l1lllll_opy_),
        "qua2": (l1l11l1_opy_, l1111l1l_opy_.l11ll1l_opy_),
        "qua3": (l1l11l1_opy_, l1111l1l_opy_.l1ll1l1_opy_),
        "var": (l1l11l1_opy_, l1111l1l_opy_.l1ll11ll_opy_),
        "dev": (l1l11l1_opy_, l1111l1l_opy_.l1l111l11_opy_),
        "comb": (l1l11l1_opy_, l1111l1l_opy_.l1ll11l11_opy_),
        "arr": (l1l11l1_opy_, l1111l1l_opy_.l1111l11_opy_),
    }


l1111l1l1_opy_ = {
    (l11l1111l_opy_, l11l1llll_opy_.l1lllllll_opy_),
}
l1l1lll1l_opy_ = {
    (l1l1lll11_opy_, l11lll1l_opy_.l1llll1_opy_),
    (l1l1lll11_opy_, l11lll1l_opy_.l11l11l1_opy_),
}
l1l1lll1_opy_ = {
    (l1l1lll11_opy_, l11lll1l_opy_.l1ll1l11l_opy_),
    (l1l1lll11_opy_, l11lll1l_opy_.l1ll111ll_opy_),
}
l11l11lll_opy_ = {
    (l1l1lll11_opy_, l11lll1l_opy_.l1111l_opy_),
    (l1l1lll11_opy_, l11lll1l_opy_.l1l1l1l1_opy_),
    (l1l1lll11_opy_, l11lll1l_opy_.l11l1111_opy_),
}
l1l11l11_opy_ = {
    (l1l1lll11_opy_, l11lll1l_opy_.l111111ll_opy_),
}
l11lll11l_opy_ = {
    (l1l11l1_opy_, l1111l1l_opy_.l111l11lll_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1l11ll11_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1ll1ll1l_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.MAX),
    (l1l11l1_opy_, l1111l1l_opy_.l11llllll_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l11111lll_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1ll11l_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1l1lllll_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l11ll1l_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1ll1l1_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1ll11ll_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1l111l11_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1ll11l11_opy_),
    (l1l11l1_opy_, l1111l1l_opy_.l1111l11_opy_),
}
l1l11llll_opy_ = {
    (l1ll11111_opy_, l1l11111l_opy_.l1l1ll11_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1l11lll_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11lll1ll_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1lll1l1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1ll11ll1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11l111ll_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l111l11l1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11l11111_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11lll1l1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11111_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1111l1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1lll1ll1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1l11ll_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l111l1ll1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11ll11l1_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11ll1l11_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11l1l111_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1l11111_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1llll1l_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l1ll1l1ll_opy_),
    (l1ll11111_opy_, l1l11111l_opy_.l11l1l1_opy_),
}
l111l11l_opy_ = {
    (l1ll11111_opy_, l1l11111l_opy_.l111l11_opy_),
}
'''
-----------------------------------------------------------
Math parser.
Non géré :
    Opérateur unaire '+' '-'.
    Fonctions statistique multi arguments.
-----------------------------------------------------------
'''


class MathParser:
    #
    def __init__(self, l11l1lll_opy_, l11111ll_opy_, l1lll11l1_opy_):
        self.l11l1lll_opy_ = l11l1lll_opy_
        if l11111ll_opy_ == 'radian':
            l1ll11111_opy_.l11ll1ll_opy_ = l1ll11111_opy_.l11ll1ll_opy_.l11lll111_opy_
        else:
            l1ll11111_opy_.l11ll1ll_opy_ = l1ll11111_opy_.l11ll1ll_opy_.l1lll11_opy_
        self.l111llll1_opy_ = l1lll11l1_opy_
        self.l111ll1ll_opy_ = dict()
        self.l11l1l1ll_opy_ = 1
        self.l1l11l11l_opy_ = str

    def l1l111111_opy_(self):
        self.l111ll1ll_opy_ = dict()
        self.l11l1l1ll_opy_ = 1
        self.l1l11l11l_opy_ = str

    def execute(self, text):
        self.l1l111111_opy_()
        text = text.replace(' ', '')
        # text = text.lower()
        self.l1l11l11l_opy_ = l1lll11ll_opy_(text)
        return self._11lll1_opy_(self.l1l11l11l_opy_)

    def _11lll1_opy_(self, l1l11l11l_opy_):
        while True:
            l1l111lll_opy_ = self._11lll11_opy_(l1l11l11l_opy_)
            if l1l111lll_opy_:
                l1l11l11l_opy_ = l1l111lll_opy_
            else:
                break
        while True:
            log.info("Try to parse <{}>".format(l1l11l11l_opy_))
            try:
                l11l1l1l_opy_ = l1l111_opy_(l1l11l11l_opy_.text, self.parse(l1l11l11l_opy_))
            except MathInjectionException as l1lll1111_opy_:
                index = l1l11l11l_opy_.l1l1111l1_opy_.index(l1lll1111_opy_.inject_pos)
                log.info("Invisible mul at {}".format(index))
                l1l111l1l_opy_ = l1l11l11l_opy_[0: index + 1]
                if self.l11l1lll_opy_.l111ll1l1l_opy_ == "braille":
                    l111ll1_opy_ = l1lll11ll_opy_(l111lll11l_opy_.l1ll1111_opy_, index=-1)
                else:
                    l111ll1_opy_ = l1lll11ll_opy_("\u00D7", index=-1)
                l1lll11l_opy_ = l1l11l11l_opy_[index + 1: len(l1l11l11l_opy_)]
                l1l11l11l_opy_ = l1l111l1l_opy_ + l111ll1_opy_ + l1lll11l_opy_
                continue
            except MathUnaryException as l1lll1111_opy_:
                index = l1l11l11l_opy_.l1l1111l1_opy_.index(l1lll1111_opy_.unary_pos)
                log.info("Unary operator at {}".format(index))
                l1l11l11l_opy_ = l1l11l11l_opy_[:index] + l1lll11ll_opy_('\u2212',
                                                                         index=l1lll1111_opy_.unary_pos) + l1l11l11l_opy_[
                                                                                                           index + 1:]
                continue
            return l11l1l1l_opy_

    def parse(self, text):
        log.info("segment to parse <{}>".format(text))
        if len(text) == 0:
            raise MathException(-1, MathException.ErrorCode.EMPTY_ARG, _("empty argument"))
        items = self._1l111ll_opy_(text)
        for key in items:
            (l1l1111l_opy_, l11l1ll1l_opy_, l1_opy_) = items.get(key)
            log.info("item:key={},class={},item={}, length={}".format(key, l1l1111l_opy_, l11l1ll1l_opy_, l1_opy_))
        '''
            En braille mathématique le séparateur d'arguments est le même code que la fin de bloc invisible.
            Lorsque l'on détecte une fonction multi opérande on segmente donc en une liste d'arguments
            la partie droite sans se soucier des clefs qu'elle contient.
        '''
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, {(l11l1_opy_, None)})
        if l1l1111l_opy_:
            l1ll1l_opy_ = text.split(self.l11l1lll_opy_.l1111ll_opy_)
            log.info("operands :")
            for l111l_opy_ in l1ll1l_opy_:
                log.info("operands :<{}>".format(l111l_opy_))
            l1l1l11_opy_ = list()
            for l111l_opy_ in l1ll1l_opy_:
                l1l1l11_opy_.append(self.parse(l111l_opy_))
            return l11l1_opy_(text.l1l1111l1_opy_[0], l1l1l11_opy_)
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l1l1lll1l_opy_)
        if not l1l1111l_opy_:
            l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l1l1lll1_opy_)
            if not l1l1111l_opy_:
                l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l11l11lll_opy_)
        if l1l1111l_opy_:
            try:
                l1l11ll1l_opy_ = self.parse(text[0: l11l1ll_opy_])
            except MathException as l1lll1111_opy_:
                if (l1lll1111_opy_.error_code == MathException.ErrorCode.EMPTY_ARG) and (
                        l1ll1lll1_opy_ == l11lll1l_opy_.l1ll111ll_opy_):
                    raise MathUnaryException(text.l1l1111l1_opy_[l11l1ll_opy_])
                else:
                    raise MathException(text.l1l1111l1_opy_[l11l1ll_opy_], l1lll1111_opy_.error_code,
                                        l1lll1111_opy_.__str__())
            l11llll_opy_ = text[l11l1ll_opy_ + l1_opy_: len(text)]
            l1111lll_opy_ = self.parse(text[l11l1ll_opy_ + l1_opy_: len(text)])
            return l1l1111l_opy_(text.l1l1111l1_opy_[l11l1ll_opy_], l1ll1lll1_opy_, l1l11ll1l_opy_, l1111lll_opy_)
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l1l11llll_opy_)
        if l11l1ll_opy_ == 0:
            l1llllll1_opy_, l11l1l_opy_, l11l11_opy_, l1ll1l1l1_opy_ = self._1ll1111l_opy_(items, l1l11l11_opy_)
            if l1llllll1_opy_ == l1_opy_ and l11l1l_opy_ == l1l1lll11_opy_ and l11l11_opy_ == l11lll1l_opy_.l111111ll_opy_:
                try:
                    l111111l_opy_ = text[l1_opy_ + l1ll1l1l1_opy_: len(text)]
                    arg = self.parse(l111111l_opy_)
                except MathInjectionException as l1lll1111_opy_:
                    index = l111111l_opy_.l1l1111l1_opy_.index(l1lll1111_opy_.inject_pos)
                    l1lll1l11_opy_ = l111111l_opy_[0: index + 1]
                    l11llll_opy_ = l111111l_opy_[index + 1, len(l111111l_opy_)]
                    return l11l1l_opy_(text.l1l1111l1_opy_[0], l11l11_opy_,
                                       l1l1111l_opy_(text.l1l1111l1_opy_[0], l1ll1lll1_opy_, self.parse(l11llll_opy_)),
                                       self.parse(l1lll1l11_opy_))
                raise MathException(text.l1l1111l1_opy_[l1_opy_ + l1ll1l1l1_opy_], MathException.ErrorCode.EMPTY_ARG,
                                    _("empty argument"))
            arg = self.parse(text[l1_opy_: len(text)])
            if arg:
                return l1l1111l_opy_(text.l1l1111l1_opy_[0], l1ll1lll1_opy_, arg)
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l111l11l_opy_)
        if l11l1ll_opy_ + l1_opy_ == len(text):
            arg = self.parse(text[0: l11l1ll_opy_])
            if arg:
                return l1l1111l_opy_(text.l1l1111l1_opy_[0], l1ll1lll1_opy_, arg)
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l1111l1l1_opy_)
        if l1l1111l_opy_:
            l111l1ll11_opy_ = self.parse(text[l11l1ll_opy_ + l1_opy_: len(text)])
            return l11l1111l_opy_(text.l1l1111l1_opy_[l11l1ll_opy_], l11l1llll_opy_.l1lllllll_opy_, l111l1ll11_opy_)
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l1l11l11_opy_,
                                                                                   l111ll1l_opy_=True)
        if l1l1111l_opy_:
            return l1l1111l_opy_(text.l1l1111l1_opy_[l11l1ll_opy_], l1ll1lll1_opy_,
                                 self.parse(text[0: l11l1ll_opy_]),
                                 self.parse(text[l11l1ll_opy_ + l1_opy_: len(text)]))
        l11l1ll_opy_, l1l1111l_opy_, l1ll1lll1_opy_, l1_opy_ = self._1ll1111l_opy_(items, l11lll11l_opy_)
        if l1l1111l_opy_:
            if (self.l11l1lll_opy_ == MathBrailleTable) \
                    and (l1l1111l_opy_ == l1l11l1_opy_) \
                    and (l1ll1lll1_opy_ == l1111l1l_opy_.l111l11lll_opy_):
                log.info("Nroot found")
                l111l11l1l_opy_, l111ll1ll1_opy_, l111ll11l1_opy_, l111lll111_opy_ = \
                    self._1ll1111l_opy_(items, {(l1ll11111_opy_, l1l11111l_opy_.l1llll1l_opy_)})
                if l111ll1ll1_opy_:
                    l1lll1l11_opy_ = self.parse(text[l11l1ll_opy_ + l1_opy_: l111l11l1l_opy_])
                    l11llll_opy_ = self.parse(text[l111l11l1l_opy_ + l111lll111_opy_: len(text)])
                    return l1l11l1_opy_(text.l1l1111l1_opy_[l11l1ll_opy_], l1111l1l_opy_.l111l11lll_opy_,
                                        [l1lll1l11_opy_, l11llll_opy_])
                raise MathException(text.l1l1111l1_opy_[l1_opy_], MathException.ErrorCode.INVALID_FUNCTION,
                                    _("invalid function"))
            l111111l_opy_ = text[l11l1ll_opy_ + l1_opy_: len(text)]
            args = []
            while len(l111111l_opy_) > 0:
                try:
                    arg = self.parse(l111111l_opy_)
                    args.append(arg)
                    l111111l_opy_ = ""
                except MathInjectionException as l1lll1111_opy_:
                    index = l111111l_opy_.l1l1111l1_opy_.index(l1lll1111_opy_.inject_pos)
                    args.append(self.parse(l111111l_opy_[0: index + 1]))
                    l111111l_opy_ = l111111l_opy_[index + 1: len(l111111l_opy_)]
            return l1l1111l_opy_(text.l1l1111l1_opy_[l11l1ll_opy_], l1ll1lll1_opy_, args)
        pos = text.find("__blk")
        if pos == 0:
            kwargs = self.l111ll1ll_opy_.get(text.l1ll1ll11_opy_())
            if not kwargs:
                l11ll111_opy_ = self._11lllll_opy_(text.l1ll1ll11_opy_())
                if l11ll111_opy_:
                    raise MathInjectionException(text.l1l1111l1_opy_[len(l11ll111_opy_)] - 1)
                else:
                    raise MathException(text.l1l1111l1_opy_[len(l11ll111_opy_)] - 1, MathException.ErrorCode.BLOC_ERROR,
                                        _("bloc error"))
            (l1ll1l1l_opy_, l11ll1111_opy_) = kwargs
            log.info("parse bloc:<{}>".format(l11ll1111_opy_))
            key = l11ll1111_opy_[0: l1ll1l1l_opy_].l1ll1ll11_opy_()
            (l11ll111l_opy_, l1111l111_opy_) = self.l11l1lll_opy_.l1llllll_opy_[key]
            l11ll1111_opy_ = l11ll1111_opy_[l1ll1l1l_opy_: len(l11ll1111_opy_) - l1ll1l1l_opy_]
            if l1111l111_opy_ == l1111l1ll_opy_.l111lllll_opy_:
                return l111l1l1_opy_(text.l1l1111l1_opy_[0], l11ll1111_opy_.l1ll1ll11_opy_())
            else:
                l11l1l1l_opy_ = self._11lll1_opy_(l11ll1111_opy_)
                return l1lll111l_opy_(l11ll1111_opy_.l1l1111l1_opy_[0] - l1ll1l1l_opy_, l1111l111_opy_, l11l1l1l_opy_)
        l1l11l1l1_opy_ = text.l1ll1ll11_opy_()
        l1lll1l1l_opy_ = False
        if self.l11l1lll_opy_ == MathBrailleTable:
            key = MathBrailleTable.l111lll1_opy_.get(l1l11l1l1_opy_)
            if key:
                l1l11l1l1_opy_ = key
                l1lll1l1l_opy_ = True
            else:
                l1l11l1l1_opy_ = self.l111llll1_opy_.to_text_8(l1l11l1l1_opy_)
        key, value = parameters.l1l1_opy_(l1l11l1l1_opy_)
        if value:
            if len(key) < len(text):
                raise MathInjectionException(text.l1l1111l1_opy_[len(key) - 1])
            else:
                if l1lll1l1l_opy_:
                    return l111l1l1_opy_(l1l11l1l1_opy_, value)
                else:
                    return l111l1l1_opy_(text.l1l1111l1_opy_[0], value)
        value = self._11llll1_opy_(text)
        try:
            value = value.replace('\u2212', '-')
            val = float(value)
            return l111l1l1_opy_(text.l1l1111l1_opy_[0], val)
        except ValueError:
            if len(value) == 1:
                return l111l1l1_opy_(text.l1l1111l1_opy_[0], value)
            elif len(value) > 1:
                raise MathInjectionException(text.l1l1111l1_opy_[0])
            else:
                raise MathException(text.l1l1111l1_opy_[0], MathException.ErrorCode.EMPTY_ARG, _("empty argument"))

    def _11llll1_opy_(self, text):
        l1l11l1l1_opy_ = text.l1ll1ll11_opy_()
        if self.l11l1lll_opy_.l111ll1l1l_opy_ == "braille":
            log.info("value:<{}>".format(l1l11l1l1_opy_))
            l1l11l1l1_opy_ = l1l11l1l1_opy_.replace(b46 + b15, b157)
            l1l11l1l1_opy_ = l1l11l1l1_opy_.replace('\u2212', l111lll11l_opy_.l1l11l1l_opy_)
            l111l1lll1_opy_ = len(l1l11l1l1_opy_)
            length = 0
            while (length < l111l1lll1_opy_) and ('\u2800' <= l1l11l1l1_opy_[length] <= '\u28FF'):
                length += 1
            l111l1l11l_opy_ = l1l11l1l1_opy_[0: length]
            l111lll1ll_opy_ = l1l11l1l1_opy_[length: l111l1lll1_opy_]
            text = self.l111llll1_opy_.to_text_8(l111l1l11l_opy_)
            text = text.replace(",", ".")
            text += l111lll1ll_opy_
            log.info("converted value:<{}>".format(text))
            return text
        else:
            l1l11l1l1_opy_ = l1l11l1l1_opy_.replace(",", ".")
            return l1l11l1l1_opy_

    def _11lll11_opy_(self, text):
        l1ll1l1l_opy_ = 0
        for key in self.l11l1lll_opy_.l1llllll_opy_:
            if len(key) > l1ll1l1l_opy_:
                l1ll1l1l_opy_ = len(key)
        while l1ll1l1l_opy_ > 0:
            for key in self.l11l1lll_opy_.l1llllll_opy_:
                if len(key) == l1ll1l1l_opy_:
                    l1ll1llll_opy_ = text.find(key)
                    if l1ll1llll_opy_ != -1:
                        l1l1l1lll_opy_ = l1ll1llll_opy_
                        (l11ll111l_opy_, l1111l111_opy_) = self.l11l1lll_opy_.l1llllll_opy_[key]
                        l1l1llll1_opy_ = l1l1l1lll_opy_ + len(key)
                        l11ll11ll_opy_ = text.find(l11ll111l_opy_, l1l1llll1_opy_)
                        l1ll1llll_opy_ = text.find(key, l1l1llll1_opy_)
                        l11l1l1l1_opy_ = 1
                        while l11l1l1l1_opy_ != 0:
                            if l11ll11ll_opy_ == -1:
                                raise MathException(text.l1l1111l1_opy_[l1l1l1lll_opy_], "bloc not closed.")
                            elif l1ll1llll_opy_ == l11ll11ll_opy_:
                                l11l1l1l1_opy_ -= 1
                            elif (l1ll1llll_opy_ != -1) and (l1ll1llll_opy_ < l11ll11ll_opy_):
                                l11l1l1l1_opy_ += 1
                                l1l1llll1_opy_ = l1ll1llll_opy_ + len(key)
                                l1ll1llll_opy_ = text.find(key, l1l1llll1_opy_)
                            elif l11l1l1l1_opy_ != 0:
                                l11l1l1l1_opy_ -= 1
                                if l11l1l1l1_opy_ != 0:
                                    l1l1llll1_opy_ = l11ll11ll_opy_ + len(l11ll111l_opy_)
                                    l11ll11ll_opy_ = text.find(l11ll111l_opy_, l1l1llll1_opy_)
                        if l11ll11ll_opy_ != -1:
                            log.debug("bloc found, start:{} end:{}".format(l1l1l1lll_opy_,
                                                                           l11ll11ll_opy_ + l1ll1l1l_opy_ - 1))
                            name = "__blk{}__".format(self.l11l1l1ll_opy_)
                            l1l1llll_opy_ = l1lll11ll_opy_(name,
                                                           l1l1111l1_opy_=[text.l1l1111l1_opy_[l1l1l1lll_opy_]] * len(
                                                               name))
                            l1l1llll_opy_.l1l1111l1_opy_[len(name) - 1] = text.l1l1111l1_opy_[
                                l11ll11ll_opy_ + l1ll1l1l_opy_ - 1]
                            self.l11l1l1ll_opy_ += 1
                            self.l111ll1ll_opy_.update({l1l1llll_opy_.l1ll1ll11_opy_(): (
                                l1ll1l1l_opy_, text[l1l1l1lll_opy_: l11ll11ll_opy_ + l1ll1l1l_opy_])})
                            log.info("bloc found:<{}>".format(text[l1l1l1lll_opy_: l11ll11ll_opy_ + l1ll1l1l_opy_]))
                            return text[0: l1l1l1lll_opy_] + l1l1llll_opy_ + text[
                                                                             l11ll11ll_opy_ + l1ll1l1l_opy_: len(text)]
                        else:
                            raise MathException(text.l1l1111l1_opy_[l1l1l1lll_opy_], "bloc not closed.")
            l1ll1l1l_opy_ -= 1

    def _1l111ll_opy_(self, text):
        l11l1ll1l_opy_ = None
        l1_opy_ = 0
        items = dict()
        l1l1lll_opy_ = 0
        l1l1111l_opy_ = l1l1lll11_opy_
        while l1l1111l_opy_:
            l11l1ll_opy_ = len(text)
            l1l1111l_opy_ = None
            for key in self.l11l1lll_opy_.l11l111l_opy_:
                l1ll1llll_opy_ = text.find(key, l1l1lll_opy_)
                if l1ll1llll_opy_ != -1:
                    if (l1ll1llll_opy_ < l11l1ll_opy_) or ((l1ll1llll_opy_ == l11l1ll_opy_) and (len(key) >= l1_opy_)):
                        l11l1ll_opy_ = l1ll1llll_opy_
                        (l1l1111l_opy_, l11l1ll1l_opy_) = self.l11l1lll_opy_.l11l111l_opy_[key]
                        l1_opy_ = len(key)
            if l1l1111l_opy_:
                items.update({l11l1ll_opy_: (l1l1111l_opy_, l11l1ll1l_opy_, l1_opy_)})
                l1l1lll_opy_ = l11l1ll_opy_ + l1_opy_
        return items

    @staticmethod
    def _1ll1111l_opy_(items, l1111ll1l_opy_, l111ll1l_opy_=False):
        l11l1ll_opy_ = -1
        l1l1111l_opy_ = None
        l111lll_opy_ = None
        l1_opy_ = 0
        for key in items:
            (l11llll11_opy_, l11111l1_opy_, l11llll1l_opy_) = items.get(key)
            for (l11l111l1_opy_, l111l1111_opy_) in l1111ll1l_opy_:
                if (l11l111l1_opy_ == l11llll11_opy_) and (l111l1111_opy_ == l11111l1_opy_):
                    if key > l11l1ll_opy_:
                        l11l1ll_opy_ = key
                        l1l1111l_opy_ = l11l111l1_opy_
                        l111lll_opy_ = l111l1111_opy_
                        l1_opy_ = l11llll1l_opy_
            if (l11l1ll_opy_ != -1) and l111ll1l_opy_:
                return l11l1ll_opy_, l1l1111l_opy_, l111lll_opy_, l1_opy_
        return l11l1ll_opy_, l1l1111l_opy_, l111lll_opy_, l1_opy_

    """ Return the parameter label """
    """ Return the bloc label (__blkxx__) """

    @staticmethod
    def _11lllll_opy_(text):
        m = re.search("^(__blk[\d+]*__)", text)
        if m:
            return m.group(1)
