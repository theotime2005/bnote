"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import re
from .l11l1ll1l_opy_ import l111l1l1l_opy_
from .l11lll_opy_ import l1l1l1_opy_
from .l11111l_opy_ import l111111ll_opy_
from .l1l1ll1ll_opy_ import l111l1l_opy_, l111l11_opy_
from .l1111llll_opy_ import l1lll11l1_opy_, l11l111l_opy_
from .l11l1l111_opy_ import l111ll1l_opy_, l1lll11_opy_, l11l1l11l_opy_
from .l11111_opy_ import l11lll1ll_opy_, l1l11l11l_opy_
from .l1l1_opy_ import l1_opy_
from .braille import b16, b126, b146, b1456, b156, b1246, b12456, b1256, b246, b3456, b15, b36, b46, b157
from .l1ll111l11_opy_ import l1ll111lll_opy_
from .math_exception import MathException
from .math_exception import MathInjectionException, MathUnaryException
from .l1ll1l_opy_ import l111l_opy_
from .l111l1ll_opy_ import l1l1l111_opy_, l1ll1l1ll_opy_
# ll_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG
log = ColoredLogger(__name__, level=MATH_LOG)
'''
-----------------------------------------------------------
Math Braille definitions.
-----------------------------------------------------------
'''
class MathBrailleTable:
    l1l1llll11_opy_ = "braille"
    l1ll1l11_opy_ = l1ll111lll_opy_.l11l1l1l1_opy_
    l111111l1_opy_ = {
        l1ll111lll_opy_.l1111ll_opy_: (l1ll111lll_opy_.l1lll1111_opy_, l11l111l_opy_.l11ll11l_opy_),
        l1ll111lll_opy_.l1l111l_opy_: (l1ll111lll_opy_.l1l111l11_opy_, l11l111l_opy_.l1l11l11_opy_),
        l1ll111lll_opy_.l1ll11l11_opy_: (l1ll111lll_opy_.l1llll11_opy_, l11l111l_opy_.l1l1lll_opy_),
        l1ll111lll_opy_.l1l1llllll_opy_: (l1ll111lll_opy_.l1l1lll1ll_opy_, l11l111l_opy_.l11l1111l_opy_),
        l1ll111lll_opy_.l1ll1ll11l_opy_: (l1ll111lll_opy_.l1lll1l11l_opy_, l11l111l_opy_.l1ll11l1_opy_),
    }
    l11l1ll_opy_ = {
        l1ll111lll_opy_.l1ll111_opy_: (l111l1l_opy_, l111l11_opy_.l111111_opy_),
        l1ll111lll_opy_.l1llllll_opy_: (l111l1l_opy_, l111l11_opy_.l1llllll_opy_),
        l1ll111lll_opy_.l11lll1l_opy_: (l111l1l_opy_, l111l11_opy_.l1lllll11_opy_),
        l1ll111lll_opy_.l11l11_opy_: (l111l1l_opy_, l111l11_opy_.l1l1l1ll_opy_),
        '\u2212': (l1l1l111_opy_, l1ll1l1ll_opy_.l1l11l111_opy_),
        l1ll111lll_opy_.l11lllll1_opy_: (l111l1l_opy_, l111l11_opy_.l1l1111l1_opy_),
        l1ll111lll_opy_.l1l1l11l1_opy_: (l111l1l_opy_, l111l11_opy_.l1l1111l1_opy_),
        l1ll111lll_opy_.l1ll111l_opy_: (l111l1l_opy_, l111l11_opy_.l1ll11ll_opy_),
        l1ll111lll_opy_.l1ll111ll_opy_: (l111l1l_opy_, l111l11_opy_.l11ll11l1_opy_),
        l1ll111lll_opy_.l11l11l_opy_: (l111l1l_opy_, l111l11_opy_.l11ll11l1_opy_),
        l1ll111lll_opy_.l1l1lll1l1_opy_: (l111l1l_opy_, l111l11_opy_.l111ll1l1_opy_),
        l1ll111lll_opy_.l1ll1llll_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1l1ll1_opy_),
        l1ll111lll_opy_.l1111l1l1_opy_: (l111ll1l_opy_, l1lll11_opy_.l11l1llll_opy_),
        l1ll111lll_opy_.l1ll11ll1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l111l1l_opy_),
        l1ll111lll_opy_.l11llll1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1lll1ll_opy_),
        l1ll111lll_opy_.l1l1llll1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1111l111_opy_),
        l1ll111lll_opy_.l1lll11ll_opy_: (l111ll1l_opy_, l1lll11_opy_.l1llll11l_opy_),
        l1ll111lll_opy_.l1ll11llll_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l111l1l_opy_),
        l1ll111lll_opy_.l1ll111ll1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1lll1ll_opy_),
        l1ll111lll_opy_.l1ll11l111_opy_: (l111ll1l_opy_, l1lll11_opy_.l1111l111_opy_),
        l1ll111lll_opy_.l1l1llll1l_opy_: (l111ll1l_opy_, l1lll11_opy_.l1llll11l_opy_),
        l1ll111lll_opy_.l1l1l1l_opy_: (l111ll1l_opy_, l1lll11_opy_.l111ll11_opy_),
        l1ll111lll_opy_.l11lll11l_opy_: (l111ll1l_opy_, l1lll11_opy_.l1ll1l111_opy_),
        l1ll111lll_opy_.l11lll111_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1ll1l_opy_),
        l1ll111lll_opy_.l1l11l1ll_opy_: (l111ll1l_opy_, l1lll11_opy_.l111ll111_opy_),
        l1ll111lll_opy_.l1ll11l1ll_opy_: (l111ll1l_opy_, l1lll11_opy_.l111ll11_opy_),
        l1ll111lll_opy_.l1ll11111l_opy_: (l111ll1l_opy_, l1lll11_opy_.l1ll1l111_opy_),
        l1ll111lll_opy_.l1ll1111l1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1ll1l_opy_),
        l1ll111lll_opy_.l1ll11ll11_opy_: (l111ll1l_opy_, l1lll11_opy_.l111ll111_opy_),
        l1ll111lll_opy_.l11ll1l1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1ll1lll_opy_),
        l1ll111lll_opy_.l111ll11l_opy_: (l111ll1l_opy_, l1lll11_opy_.l1111lll_opy_),
        l1ll111lll_opy_.l1ll1l1l_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1lll11_opy_),
        l1ll111lll_opy_.l1ll1111l_opy_: (l111ll1l_opy_, l1lll11_opy_.l111l111l_opy_),
        l1ll111lll_opy_.l1l1l1l11_opy_: (l111ll1l_opy_, l1lll11_opy_.l1llll111_opy_),
        l1ll111lll_opy_.l1111l1ll_opy_: (l111ll1l_opy_, l1lll11_opy_.l1lll111_opy_),
        l1ll111lll_opy_.l1l11l1l1_opy_: (l111ll1l_opy_, l1lll11_opy_.l111lll1l_opy_),
        l1ll111lll_opy_.l1l1lllll_opy_: (l111ll1l_opy_, l1lll11_opy_.l111ll_opy_),
        l1ll111lll_opy_.l1l1lll11l_opy_: (l111ll1l_opy_, l1lll11_opy_.l11l11l11_opy_),
        l1ll111lll_opy_.l1ll1l1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1lll1_opy_),
        l1ll111lll_opy_.l111l1ll1_opy_: (l111ll1l_opy_, l1lll11_opy_.l1l1ll11l_opy_),
        l1ll111lll_opy_.l11llll1l_opy_: (l111ll1l_opy_, l1lll11_opy_.l11l1ll1_opy_),
        l1ll111lll_opy_.l11l1l1l1_opy_: (l111l_opy_, None),
        l1ll111lll_opy_.l1ll11lll1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l1l1lll111_opy_),
        l1ll111lll_opy_.l1lll1ll1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l11111lll_opy_),
        l1ll111lll_opy_.l1lll1l1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l11llll_opy_),
        l1ll111lll_opy_.l1llllll1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.MAX),
        l1ll111lll_opy_.l11l11111_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l1l111111_opy_),
        l1ll111lll_opy_.l1llll1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l1l1111ll_opy_),
        l1ll111lll_opy_.l1ll1111_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l111llll_opy_),
        l1ll111lll_opy_.l1lllll1l_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l1l1l1l1_opy_),
        l1ll111lll_opy_.l1l1llll_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l1lllllll_opy_),
        l1ll111lll_opy_.l1l1ll1l1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l11111l11_opy_),
        l1ll111lll_opy_.l1l1l1l1l_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l111l1l11_opy_),
        l1ll111lll_opy_.l11l1lll1_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l111lll11_opy_),
        l1ll111lll_opy_.l1l1ll11_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l11ll1l1l_opy_),
        l1ll111lll_opy_.l11llll11_opy_: (l11lll1ll_opy_, l1l11l11l_opy_.l111l111_opy_),
        ''.join([b157, b36]): (None, None),
        ''.join([b46, b15, b36]): (None, None),
    }
    l11l1l1l_opy_ = {
        l1ll111lll_opy_.l1ll1l1l1_opy_: 'pi',
    }
'''
-----------------------------------------------------------
Math Text definitions.
-----------------------------------------------------------
'''
class MathTextTable:
    l1l1llll11_opy_ = "text"
    l1ll1l11_opy_ = ";"
    l111111l1_opy_ = {
        '{': ('}', l11l111l_opy_.l1ll11l1_opy_),
        '(': (')', l11l111l_opy_.l11ll11l_opy_),
        '[': (']', l11l111l_opy_.l1l11l11_opy_),
        #'{': ('}', l11l111l_opy_.l1l1lll_opy_)
    }
    l11l1ll_opy_ = {
        '=': (l111l1l_opy_, l111l11_opy_.l111111_opy_),
        '+': (l111l1l_opy_, l111l11_opy_.l1lllll11_opy_),
        '-': (l111l1l_opy_, l111l11_opy_.l1l1l1ll_opy_),
        '\u2212': (l1l1l111_opy_, l1ll1l1ll_opy_.l1l11l111_opy_),
        '*': (l111l1l_opy_, l111l11_opy_.l11ll11l1_opy_),
        '/': (l111l1l_opy_, l111l11_opy_.l1l1111l1_opy_),
        '%': (l111l1l_opy_, l111l11_opy_.l1ll11ll_opy_),
        '\u00D7': (l111l1l_opy_, l111l11_opy_.l11ll11l1_opy_),
        '^': (l111l1l_opy_, l111l11_opy_.l111ll1l1_opy_),
        'ln': (l111ll1l_opy_, l1lll11_opy_.l1l1l1ll1_opy_),
        'log': (l111ll1l_opy_, l1lll11_opy_.l11l1llll_opy_),
        'sin': (l111ll1l_opy_, l1lll11_opy_.l1l111l1l_opy_),
        'cos': (l111ll1l_opy_, l1lll11_opy_.l1lll1ll_opy_),
        'tan': (l111ll1l_opy_, l1lll11_opy_.l1111l111_opy_),
        'cot': (l111ll1l_opy_, l1lll11_opy_.l1llll11l_opy_),
        'asin': (l111ll1l_opy_, l1lll11_opy_.l111ll11_opy_),
        'acos': (l111ll1l_opy_, l1lll11_opy_.l1ll1l111_opy_),
        'atan': (l111ll1l_opy_, l1lll11_opy_.l1l1ll1l_opy_),
        'acot': (l111ll1l_opy_, l1lll11_opy_.l111ll111_opy_),
        'sh': (l111ll1l_opy_, l1lll11_opy_.l1ll1lll_opy_),
        'ch': (l111ll1l_opy_, l1lll11_opy_.l1111lll_opy_),
        'th': (l111ll1l_opy_, l1lll11_opy_.l1l1lll11_opy_),
        'sinh': (l111ll1l_opy_, l1lll11_opy_.l1ll1lll_opy_),
        'cosh': (l111ll1l_opy_, l1lll11_opy_.l1111lll_opy_),
        'tanh': (l111ll1l_opy_, l1lll11_opy_.l1l1lll11_opy_),
        'coth': (l111ll1l_opy_, l1lll11_opy_.l111l111l_opy_),
        'ash': (l111ll1l_opy_, l1lll11_opy_.l1llll111_opy_),
        'ach': (l111ll1l_opy_, l1lll11_opy_.l1lll111_opy_),
        'ath': (l111ll1l_opy_, l1lll11_opy_.l111lll1l_opy_),
        'asinh': (l111ll1l_opy_, l1lll11_opy_.l1llll111_opy_),
        'acosh': (l111ll1l_opy_, l1lll11_opy_.l1lll111_opy_),
        'atanh': (l111ll1l_opy_, l1lll11_opy_.l111lll1l_opy_),
        'acoth': (l111ll1l_opy_, l1lll11_opy_.l111ll_opy_),
        'sqrt': (l111ll1l_opy_, l1lll11_opy_.l11l11l11_opy_),
        'deg': (l111ll1l_opy_, l1lll11_opy_.l1l1lll1_opy_),
        'rad': (l111ll1l_opy_, l1lll11_opy_.l1l1ll11l_opy_),
        '!':  (l111ll1l_opy_, l1lll11_opy_.l11l1ll1_opy_),
        'nroot': (l11lll1ll_opy_, l1l11l11l_opy_.l1l1lll111_opy_),
        'E-': (None, None),
        ";": (l111l_opy_, None),
        "->": (l111l1l_opy_, l111l11_opy_.l1llllll_opy_),
        "sum": (l11lll1ll_opy_, l1l11l11l_opy_.l11111lll_opy_),
        "nbr": (l11lll1ll_opy_, l1l11l11l_opy_.l11llll_opy_),
        "max": (l11lll1ll_opy_, l1l11l11l_opy_.MAX),
        "min": (l11lll1ll_opy_, l1l11l11l_opy_.l1l111111_opy_),
        "ave": (l11lll1ll_opy_, l1l11l11l_opy_.l1l1111ll_opy_),
        "med": (l11lll1ll_opy_, l1l11l11l_opy_.l111llll_opy_),
        "qua1": (l11lll1ll_opy_, l1l11l11l_opy_.l1l1l1l1_opy_),
        "qua2": (l11lll1ll_opy_, l1l11l11l_opy_.l1lllllll_opy_),
        "qua3": (l11lll1ll_opy_, l1l11l11l_opy_.l11111l11_opy_),
        "var":  (l11lll1ll_opy_, l1l11l11l_opy_.l111l1l11_opy_),
        "dev": (l11lll1ll_opy_, l1l11l11l_opy_.l111lll11_opy_),
        "comb": (l11lll1ll_opy_, l1l11l11l_opy_.l11ll1l1l_opy_),
        "arr": (l11lll1ll_opy_, l1l11l11l_opy_.l111l111_opy_),
    }
l1lll1l11_opy_ = {
    (l1l1l111_opy_, l1ll1l1ll_opy_.l1l11l111_opy_),
}
l1111111_opy_ = {
    (l111l1l_opy_, l111l11_opy_.l111111_opy_),
    (l111l1l_opy_, l111l11_opy_.l1llllll_opy_),
}
l11l11lll_opy_ = {
    (l111l1l_opy_, l111l11_opy_.l1lllll11_opy_),
    (l111l1l_opy_, l111l11_opy_.l1l1l1ll_opy_),
}
l11lll1_opy_ = {
    (l111l1l_opy_, l111l11_opy_.l11ll11l1_opy_),
    (l111l1l_opy_, l111l11_opy_.l1l1111l1_opy_),
    (l111l1l_opy_, l111l11_opy_.l1ll11ll_opy_),
}
l11ll1ll_opy_ = {
    (l111l1l_opy_, l111l11_opy_.l111ll1l1_opy_),
}
l1l111lll_opy_ = {
    (l11lll1ll_opy_, l1l11l11l_opy_.l1l1lll111_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l11llll_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l11111lll_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.MAX),
    (l11lll1ll_opy_, l1l11l11l_opy_.l1l111111_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l1l1111ll_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l111llll_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l1l1l1l1_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l1lllllll_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l11111l11_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l111l1l11_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l111lll11_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l11ll1l1l_opy_),
    (l11lll1ll_opy_, l1l11l11l_opy_.l111l111_opy_),
}
l1111l1l_opy_ = {
    (l111ll1l_opy_, l1lll11_opy_.l1l1l1ll1_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l11l1llll_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1l111l1l_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1lll1ll_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1111l111_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1llll11l_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l111ll11_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1ll1l111_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1l1ll1l_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l111ll111_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1ll1lll_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1111lll_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1l1lll11_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l111l111l_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1llll111_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1lll111_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l111lll1l_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l111ll_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l11l11l11_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1l1lll1_opy_),
    (l111ll1l_opy_, l1lll11_opy_.l1l1ll11l_opy_),
}
l1ll1ll1_opy_ = {
    (l111ll1l_opy_, l1lll11_opy_.l11l1ll1_opy_),
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
    def __init__(self, l1l1111_opy_, l11l1l1_opy_, l111lllll_opy_):
        self.l1l1111_opy_ = l1l1111_opy_
        if l11l1l1_opy_ == 'radian':
            l111ll1l_opy_.l1l111l1_opy_ = l111ll1l_opy_.l1l111l1_opy_.l111l11l_opy_
        else:
            l111ll1l_opy_.l1l111l1_opy_ = l111ll1l_opy_.l1l111l1_opy_.l1ll1ll1l_opy_
        self.converter = l111lllll_opy_
        self.l11llllll_opy_ = dict()
        self.l1llll1ll_opy_ = 1
        self.l11l111ll_opy_ = str
    def l1l11ll11_opy_(self):
        self.l11llllll_opy_ = dict()
        self.l1llll1ll_opy_ = 1
        self.l11l111ll_opy_ = str
    def execute(self, text):
        self.l1l11ll11_opy_()
        text = text.replace(' ', '')
        #text = text.lower()
        self.l11l111ll_opy_ = l111l1l1l_opy_(text)
        return self._111l1l1_opy_(self.l11l111ll_opy_)
    def _111l1l1_opy_(self, l11l111ll_opy_):
        while True:
            l11ll1lll_opy_ = self._11l1111_opy_(l11l111ll_opy_)
            if l11ll1lll_opy_:
                l11l111ll_opy_ = l11ll1lll_opy_
            else:
                break
        while True:
            log.info("Try to parse <{}>".format(l11l111ll_opy_))
            try:
                l1ll1l11l_opy_ = l1l1l1_opy_(l11l111ll_opy_.text, self.parse(l11l111ll_opy_))
            except MathInjectionException as l1lllll1_opy_:
                index = l11l111ll_opy_.l111l11l1_opy_.index(l1lllll1_opy_.inject_pos)
                log.info("Invisible mul at {}".format(index))
                l1l1l111l_opy_ = l11l111ll_opy_[0: index + 1]
                if self.l1l1111_opy_.l1l1llll11_opy_ == "braille":
                    l1111lll1_opy_ = l111l1l1l_opy_(l1ll111lll_opy_.l11l11l_opy_, index=-1)
                else:
                    l1111lll1_opy_ = l111l1l1l_opy_("\u00D7", index=-1)
                l111111l_opy_ = l11l111ll_opy_[index + 1: len(l11l111ll_opy_)]
                l11l111ll_opy_ = l1l1l111l_opy_ + l1111lll1_opy_ + l111111l_opy_
                continue
            except MathUnaryException as l1lllll1_opy_:
                index = l11l111ll_opy_.l111l11l1_opy_.index(l1lllll1_opy_.unary_pos)
                log.info("Unary operator at {}".format(index))
                l11l111ll_opy_ = l11l111ll_opy_[:index] + l111l1l1l_opy_('\u2212', index=l1lllll1_opy_.unary_pos) + l11l111ll_opy_[index + 1:]
                continue
            return l1ll1l11l_opy_
    def parse(self, text):
        log.info("segment to parse <{}>".format(text))
        if len(text) == 0:
            raise MathException(-1, MathException.ErrorCode.EMPTY_ARG, _("empty argument"))
        items = self._1111111l_opy_(text)
        for key in items:
            (l1ll111l1_opy_, l111ll1ll_opy_, l11_opy_) = items.get(key)
            log.info("item:key={},class={},item={}, length={}".format(key, l1ll111l1_opy_, l111ll1ll_opy_, l11_opy_))
        '''
            En braille mathématique le séparateur d'arguments est le même code que la fin de bloc invisible.
            Lorsque l'on détecte une fonction multi opérande on segmente donc en une liste d'arguments
            la partie droite sans se soucier des clefs qu'elle contient.
        '''
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, {(l111l_opy_, None)})
        if l1ll111l1_opy_:
            l1111_opy_ = text.split(self.l1l1111_opy_.l1ll1l11_opy_)
            log.info("operands :")
            for l1ll11_opy_ in l1111_opy_:
                log.info("operands :<{}>".format(l1ll11_opy_))
            l11111l1_opy_ = list()
            for l1ll11_opy_ in l1111_opy_:
                l11111l1_opy_.append(self.parse(l1ll11_opy_))
            return l111l_opy_(text.l111l11l1_opy_[0], l11111l1_opy_)
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l1111111_opy_)
        if not l1ll111l1_opy_:
            l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l11l11lll_opy_)
            if not l1ll111l1_opy_:
                l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l11lll1_opy_)
        if l1ll111l1_opy_:
            try:
                l1l11lll1_opy_ = self.parse(text[0: l1l1lll1l_opy_])
            except MathException as l1lllll1_opy_:
                if (l1lllll1_opy_.error_code == MathException.ErrorCode.EMPTY_ARG) and (l1lll11l_opy_ == l111l11_opy_.l1l1l1ll_opy_):
                    raise MathUnaryException(text.l111l11l1_opy_[l1l1lll1l_opy_])
                else:
                    raise MathException(text.l111l11l1_opy_[l1l1lll1l_opy_], l1lllll1_opy_.error_code, l1lllll1_opy_.__str__())
            l11111l1l_opy_ = text[l1l1lll1l_opy_ + l11_opy_: len(text)]
            l1ll1ll_opy_ = self.parse(text[l1l1lll1l_opy_ + l11_opy_: len(text)])
            return l1ll111l1_opy_(text.l111l11l1_opy_[l1l1lll1l_opy_], l1lll11l_opy_, l1l11lll1_opy_, l1ll1ll_opy_)
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l1111l1l_opy_)
        if l1l1lll1l_opy_ == 0:
            l111l1lll_opy_, l1l111ll1_opy_, l11ll111_opy_, l111l11ll_opy_ = self._1ll11l_opy_(items, l11ll1ll_opy_)
            if l111l1lll_opy_ == l11_opy_ and l1l111ll1_opy_ == l111l1l_opy_ and l11ll111_opy_ == l111l11_opy_.l111ll1l1_opy_:
                try:
                    l1l11lll_opy_ = text[l11_opy_ + l111l11ll_opy_: len(text)]
                    arg = self.parse(l1l11lll_opy_)
                except MathInjectionException as l1lllll1_opy_:
                    index = l1l11lll_opy_.l111l11l1_opy_.index(l1lllll1_opy_.inject_pos)
                    l11ll1_opy_ = l1l11lll_opy_[0: index + 1]
                    l11111l1l_opy_ = l1l11lll_opy_[index + 1, len(l1l11lll_opy_)]
                    return l1l111ll1_opy_(text.l111l11l1_opy_[0], l11ll111_opy_, l1ll111l1_opy_(text.l111l11l1_opy_[0], l1lll11l_opy_, self.parse(l11111l1l_opy_)), self.parse(l11ll1_opy_))
                raise MathException(text.l111l11l1_opy_[l11_opy_ + l111l11ll_opy_], MathException.ErrorCode.EMPTY_ARG, _("empty argument"))
            arg = self.parse(text[l11_opy_: len(text)])
            if arg:
                return l1ll111l1_opy_(text.l111l11l1_opy_[0], l1lll11l_opy_, arg)
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l1ll1ll1_opy_)
        if l1l1lll1l_opy_ + l11_opy_ == len(text):
            arg = self.parse(text[0: l1l1lll1l_opy_])
            if arg:
                return l1ll111l1_opy_(text.l111l11l1_opy_[0], l1lll11l_opy_, arg)
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l1lll1l11_opy_)
        if l1ll111l1_opy_:
            l1ll1111ll_opy_ = self.parse(text[l1l1lll1l_opy_ + l11_opy_: len(text)])
            return l1l1l111_opy_(text.l111l11l1_opy_[l1l1lll1l_opy_], l1ll1l1ll_opy_.l1l11l111_opy_, l1ll1111ll_opy_)
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l11ll1ll_opy_, l111lll1_opy_=True)
        if l1ll111l1_opy_:
            return l1ll111l1_opy_(text.l111l11l1_opy_[l1l1lll1l_opy_], l1lll11l_opy_,
                              self.parse(text[0: l1l1lll1l_opy_]),
                              self.parse(text[l1l1lll1l_opy_ + l11_opy_: len(text)]))
        l1l1lll1l_opy_, l1ll111l1_opy_, l1lll11l_opy_, l11_opy_ = self._1ll11l_opy_(items, l1l111lll_opy_)
        if l1ll111l1_opy_:
            if (self.l1l1111_opy_ == MathBrailleTable) \
                    and (l1ll111l1_opy_ == l11lll1ll_opy_)\
                    and (l1lll11l_opy_ == l1l11l11l_opy_.l1l1lll111_opy_):
                log.info("Nroot found")
                l1ll111111_opy_, l1ll11l11l_opy_, l1ll111l1l_opy_, l1ll11l1l1_opy_ = \
                    self._1ll11l_opy_(items, {(l111ll1l_opy_, l1lll11_opy_.l11l11l11_opy_)})
                if l1ll11l11l_opy_:
                    l11ll1_opy_ = self.parse(text[l1l1lll1l_opy_ + l11_opy_: l1ll111111_opy_])
                    l11111l1l_opy_ = self.parse(text[l1ll111111_opy_ + l1ll11l1l1_opy_: len(text)])
                    return l11lll1ll_opy_(text.l111l11l1_opy_[l1l1lll1l_opy_], l1l11l11l_opy_.l1l1lll111_opy_, [l11ll1_opy_, l11111l1l_opy_])
                raise MathException(text.l111l11l1_opy_[l11_opy_], MathException.ErrorCode.INVALID_FUNCTION, _("invalid function"))
            l1l11lll_opy_ = text[l1l1lll1l_opy_ + l11_opy_: len(text)]
            args = []
            while len(l1l11lll_opy_) > 0:
                try:
                    arg = self.parse(l1l11lll_opy_)
                    args.append(arg)
                    l1l11lll_opy_ = ""
                except MathInjectionException as l1lllll1_opy_:
                    index = l1l11lll_opy_.l111l11l1_opy_.index(l1lllll1_opy_.inject_pos)
                    args.append(self.parse(l1l11lll_opy_[0: index + 1]))
                    l1l11lll_opy_ = l1l11lll_opy_[index + 1: len(l1l11lll_opy_)]
            return l1ll111l1_opy_(text.l111l11l1_opy_[l1l1lll1l_opy_], l1lll11l_opy_, args)
        pos = text.find("__blk")
        if pos == 0:
            kwargs = self.l11llllll_opy_.get(text.l11lll1l1_opy_())
            if not kwargs:
                l1l11ll1l_opy_ = self._1l11ll_opy_(text.l11lll1l1_opy_())
                if l1l11ll1l_opy_:
                    raise MathInjectionException(text.l111l11l1_opy_[len(l1l11ll1l_opy_)] - 1)
                else:
                    raise MathException(text.l111l11l1_opy_[len(l1l11ll1l_opy_)] - 1, MathException.ErrorCode.BLOC_ERROR, _("bloc error"))
            (l1111l11_opy_, l1l1ll111_opy_) = kwargs
            log.info("parse bloc:<{}>".format(l1l1ll111_opy_))
            key = l1l1ll111_opy_[0: l1111l11_opy_].l11lll1l1_opy_()
            (l111llll1_opy_, l111lll_opy_) = self.l1l1111_opy_.l111111l1_opy_[key]
            l1l1ll111_opy_ = l1l1ll111_opy_[l1111l11_opy_: len(l1l1ll111_opy_) - l1111l11_opy_]
            if l111lll_opy_ == l11l111l_opy_.l1ll11l1_opy_:
                return l111111ll_opy_(text.l111l11l1_opy_[0], l1l1ll111_opy_.l11lll1l1_opy_())
            else:
                l1ll1l11l_opy_ = self._111l1l1_opy_(l1l1ll111_opy_)
                return l1lll11l1_opy_(l1l1ll111_opy_.l111l11l1_opy_[0] - l1111l11_opy_, l111lll_opy_, l1ll1l11l_opy_)
        l1llll1l_opy_ = text.l11lll1l1_opy_()
        l11l11ll1_opy_ = False
        if self.l1l1111_opy_ == MathBrailleTable:
            key = MathBrailleTable.l11l1l1l_opy_.get(l1llll1l_opy_)
            if key:
                l1llll1l_opy_ = key
                l11l11ll1_opy_ = True
            else:
                l1llll1l_opy_ = self.converter.to_text_8(l1llll1l_opy_)
        key, value = l1_opy_.l111_opy_(l1llll1l_opy_)
        if value:
            if len(key) < len(text):
                raise MathInjectionException(text.l111l11l1_opy_[len(key) - 1])
            else:
                if l11l11ll1_opy_:
                    return l111111ll_opy_(l1llll1l_opy_, value)
                else:
                    return l111111ll_opy_(text.l111l11l1_opy_[0], value)
        value = self._1llll1l1_opy_(text)
        try:
            value = value.replace('\u2212', '-')
            val = float(value)
            return l111111ll_opy_(text.l111l11l1_opy_[0], val)
        except ValueError:
            if len(value) == 1:
                return l111111ll_opy_(text.l111l11l1_opy_[0], value)
            elif len(value) > 1:
                raise MathInjectionException(text.l111l11l1_opy_[0])
            else:
                raise MathException(text.l111l11l1_opy_[0], MathException.ErrorCode.EMPTY_ARG, _("empty argument"))
    def _1llll1l1_opy_(self, text):
        l1llll1l_opy_ = text.l11lll1l1_opy_()
        if self.l1l1111_opy_.l1l1llll11_opy_ == "braille":
            log.info("value:<{}>".format(l1llll1l_opy_))
            l1llll1l_opy_ = l1llll1l_opy_.replace(b46 + b15, b157)
            l1llll1l_opy_ = l1llll1l_opy_.replace('\u2212', l1ll111lll_opy_.l11l11_opy_)
            l1l1ll1lll_opy_ = len(l1llll1l_opy_)
            length = 0
            while (length < l1l1ll1lll_opy_) and ('\u2800' <= l1llll1l_opy_[length] <= '\u28FF'):
                length += 1
            l1ll11ll1l_opy_ = l1llll1l_opy_[0: length]
            l1l1lllll1_opy_ = l1llll1l_opy_[length: l1l1ll1lll_opy_]
            text = self.converter.to_text_8(l1ll11ll1l_opy_)
            text = text.replace(",", ".")
            text += l1l1lllll1_opy_
            log.info("converted value:<{}>".format(text))
            return text
        else:
            l1llll1l_opy_ = l1llll1l_opy_.replace(",", ".")
            return l1llll1l_opy_
    def _11l1111_opy_(self, text):
        l1111l11_opy_ = 0
        for key in self.l1l1111_opy_.l111111l1_opy_:
            if len(key) > l1111l11_opy_:
                l1111l11_opy_ = len(key)
        while l1111l11_opy_ > 0:
            for key in self.l1l1111_opy_.l111111l1_opy_:
                if len(key) == l1111l11_opy_:
                    l1lll111l_opy_ = text.find(key)
                    if l1lll111l_opy_ != -1:
                        l1l11111l_opy_ = l1lll111l_opy_
                        (l111llll1_opy_, l111lll_opy_) = self.l1l1111_opy_.l111111l1_opy_[key]
                        l1ll11111_opy_ = l1l11111l_opy_ + len(key)
                        l11l1lll_opy_ = text.find(l111llll1_opy_, l1ll11111_opy_)
                        l1lll111l_opy_ = text.find(key, l1ll11111_opy_)
                        l11lllll_opy_ = 1
                        while l11lllll_opy_ != 0:
                            if l11l1lll_opy_ == -1:
                                raise MathException(text.l111l11l1_opy_[l1l11111l_opy_], "bloc not closed.")
                            elif l1lll111l_opy_ == l11l1lll_opy_:
                                l11lllll_opy_ -= 1
                            elif (l1lll111l_opy_ != -1) and (l1lll111l_opy_ < l11l1lll_opy_):
                                l11lllll_opy_ += 1
                                l1ll11111_opy_ = l1lll111l_opy_ + len(key)
                                l1lll111l_opy_ = text.find(key, l1ll11111_opy_)
                            elif l11lllll_opy_ != 0:
                                l11lllll_opy_ -= 1
                                if l11lllll_opy_ != 0:
                                    l1ll11111_opy_ = l11l1lll_opy_ + len(l111llll1_opy_)
                                    l11l1lll_opy_ = text.find(l111llll1_opy_, l1ll11111_opy_)
                        if l11l1lll_opy_ != -1:
                            log.debug("bloc found, start:{} end:{}".format(l1l11111l_opy_, l11l1lll_opy_ + l1111l11_opy_ - 1))
                            name = "__blk{}__".format(self.l1llll1ll_opy_)
                            l1l11l1l_opy_ = l111l1l1l_opy_(name, l111l11l1_opy_=[text.l111l11l1_opy_[l1l11111l_opy_]] * len(name))
                            l1l11l1l_opy_.l111l11l1_opy_[len(name) - 1] = text.l111l11l1_opy_[l11l1lll_opy_ + l1111l11_opy_ - 1]
                            self.l1llll1ll_opy_ += 1
                            self.l11llllll_opy_.update({l1l11l1l_opy_.l11lll1l1_opy_(): (l1111l11_opy_, text[l1l11111l_opy_: l11l1lll_opy_ + l1111l11_opy_])})
                            log.info("bloc found:<{}>".format(text[l1l11111l_opy_: l11l1lll_opy_ + l1111l11_opy_]))
                            return text[0: l1l11111l_opy_] + l1l11l1l_opy_ + text[l11l1lll_opy_ + l1111l11_opy_: len(text)]
                        else:
                            raise MathException(text.l111l11l1_opy_[l1l11111l_opy_], "bloc not closed.")
            l1111l11_opy_ -= 1
    def _1111111l_opy_(self, text):
        l111ll1ll_opy_ = None
        l11_opy_ = 0
        items = dict()
        l1111ll1l_opy_ = 0
        l1ll111l1_opy_ = l111l1l_opy_
        while l1ll111l1_opy_:
            l1l1lll1l_opy_ = len(text)
            l1ll111l1_opy_ = None
            for key in self.l1l1111_opy_.l11l1ll_opy_:
                l1lll111l_opy_ = text.find(key, l1111ll1l_opy_)
                if l1lll111l_opy_ != -1:
                    if (l1lll111l_opy_ < l1l1lll1l_opy_) or ((l1lll111l_opy_ == l1l1lll1l_opy_) and (len(key) >= l11_opy_)):
                        l1l1lll1l_opy_ = l1lll111l_opy_
                        (l1ll111l1_opy_, l111ll1ll_opy_) = self.l1l1111_opy_.l11l1ll_opy_[key]
                        l11_opy_ = len(key)
            if l1ll111l1_opy_:
                items.update({l1l1lll1l_opy_: (l1ll111l1_opy_, l111ll1ll_opy_, l11_opy_)})
                l1111ll1l_opy_ = l1l1lll1l_opy_ + l11_opy_
        return items
    @staticmethod
    def _1ll11l_opy_(items, l11ll1l_opy_, l111lll1_opy_=False):
        l1l1lll1l_opy_ = -1
        l1ll111l1_opy_ = None
        l11111ll_opy_ = None
        l11_opy_ = 0
        for key in items:
            (l11ll11_opy_, l111l1_opy_, l11lll11_opy_) = items.get(key)
            for (l1l11ll1_opy_, l1l111ll_opy_) in l11ll1l_opy_:
                if (l1l11ll1_opy_ == l11ll11_opy_) and (l1l111ll_opy_ == l111l1_opy_):
                    if key > l1l1lll1l_opy_:
                        l1l1lll1l_opy_ = key
                        l1ll111l1_opy_ = l1l11ll1_opy_
                        l11111ll_opy_ = l1l111ll_opy_
                        l11_opy_ = l11lll11_opy_
            if (l1l1lll1l_opy_ != -1) and l111lll1_opy_:
                return l1l1lll1l_opy_, l1ll111l1_opy_, l11111ll_opy_, l11_opy_
        return l1l1lll1l_opy_, l1ll111l1_opy_, l11111ll_opy_, l11_opy_
    """ Return the parameter label """
    """ Return the bloc label (__blkxx__) """
    @staticmethod
    def _1l11ll_opy_(text):
        m = re.search("^(__blk[\d+]*__)", text)
        if m:
            return m.group(1)