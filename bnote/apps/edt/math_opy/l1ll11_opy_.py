"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from .l111l_opy_ import l1llll_opy_
from .l11ll_opy_ import parameters

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_RESULT_LOG

log = ColoredLogger(__name__, level=MATH_RESULT_LOG)


class l1l1ll_opy_(l1llll_opy_):
    def __init__(self, l1l11l_opy_, arg):
        l1llll_opy_.__init__(self, -1)
        self.l1l11l_opy_ = l1l11l_opy_
        self.arg = arg

    def display_tree(self, level=0):
        if level == 0:
            l1l1l1_opy_ = "\nMATH EXPRESSION -----------\n"
            l1l111_opy_ = "---------------------------\n"
        else:
            l1l1l1_opy_ = ""
            l1l111_opy_ = ""
        return "".join(
            [
                l1l1l1_opy_,
                "    " * level,
                "expression:",
                self.l1l11l_opy_,
                "\n",
                self.arg.display_tree(level + 1),
                l1l111_opy_,
            ]
        )

    def compute(self):
        value = self.arg.compute()
        parameters.l1l1_opy_("r", value)
        return value
