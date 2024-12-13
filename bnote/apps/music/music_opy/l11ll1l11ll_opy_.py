"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from .l111lllll1_opy_ import *
from .l1l111ll1_opy_ import *
from .l11ll1l11l1_opy_ import l11ll1l1111_opy_


class l11ll1l1l1l_opy_:
    def __init__(self, lou, l1l1lll1l_opy_, l1l111lll_opy_):
        self.lou = lou
        self._1ll1llll_opy_ = l1l1lll1l_opy_
        self.l1l111lll_opy_ = l1l111lll_opy_
        self._1l111l1l_opy_ = None
        self._1l1l1lll_opy_ = None

    def l1l1111ll_opy_(self, line):
        self._1l111l1l_opy_.write(line + "\n")

    def l1l11lll1_opy_(self, line):
        text = line.replace("\n", "")
        text = text.replace(" ", "\u2800")
        if len(text) > 0:
            text = self.lou.to_text_8(text)
            self._1l1l1lll_opy_(text)

    def l1ll1l11l1l_opy_(self, l1l1llll1ll_opy_, encoding=None):
        self._1l1l1lll_opy_ = l1l1llll1ll_opy_
        self._1l111l1l_opy_ = open("trace_bxml.txt", "w", encoding="utf-8")
        l1ll1l1ll_opy_ = l11ll1l111l_opy_()
        l11ll1l1l11_opy_ = l1111111ll_opy_(
            self.lou, self._1ll1llll_opy_, self.l1l111lll_opy_
        )
        l11ll1l1l11_opy_.l1ll1l11l1l_opy_(self.l1l1111ll_opy_, l1ll1l1ll_opy_)
        l1l111ll1_opy_ = l1l11llll_opy_(self.l1l1111ll_opy_, l1ll1l1ll_opy_)
        l1l111ll1_opy_.l1l1l1l11_opy_()
        l1l111ll1_opy_.l1l1ll111_opy_()
        l11ll1l11l1_opy_ = l11ll1l1111_opy_(
            self.lou,
            self.l1l11lll1_opy_,
            self.l1l1111ll_opy_,
            l1ll1l1ll_opy_,
            (self.l1l111lll_opy_, "music_bxml"),
        )
        l11ll1l11l1_opy_.l11ll11llll_opy_()
        self._1l111l1l_opy_.close()
        return l1ll1l1ll_opy_
