"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from .l1111111111_opy_ import *
from .l1l11l11l1l_opy_ import *
from .l11ll11l111_opy_ import l11l1lll1l1_opy_


class l111111111_opy_:
    def __init__(self, lou, l11111l1ll_opy_, l111111l1l_opy_):
        self.lou = lou
        self._11111ll11_opy_ = l11111l1ll_opy_
        self.l111111l1l_opy_ = l111111l1l_opy_
        self._1111llll11_opy_ = None
        self._1llll111_opy_ = None

    def l1111ll1ll1_opy_(self, line):
        self._1111llll11_opy_.write(line + "\n")

    def l1111lll1ll_opy_(self, line):
        text = line.replace("\n", "")
        text = text.replace(" ", "\u2800")
        if len(text) > 0:
            text = self.lou.to_text_8(text)
            self._1llll111_opy_(text)

    def l1111111l1_opy_(self, l1l1l111_opy_, encoding=None):
        self._1llll111_opy_ = l1l1l111_opy_
        self._1111llll11_opy_ = open("trace_bxml.txt", "w", encoding="utf-8")
        l1ll1111l1_opy_ = l1l11ll11_opy_()
        l1l1lll11lll_opy_ = l1l1llll1lll_opy_(
            self.lou, self._11111ll11_opy_, self.l111111l1l_opy_
        )
        l1l1lll11lll_opy_.l1111111l1_opy_(self.l1111ll1ll1_opy_, l1ll1111l1_opy_)
        l1l11l11l1l_opy_ = l1l11l111l1_opy_(self.l1111ll1ll1_opy_, l1ll1111l1_opy_)
        l1l11l11l1l_opy_.l1l11l1111l_opy_()
        l1l11l11l1l_opy_.l1l11l1ll11_opy_()
        l11ll11l111_opy_ = l11l1lll1l1_opy_(
            self.lou,
            self.l1111lll1ll_opy_,
            self.l1111ll1ll1_opy_,
            l1ll1111l1_opy_,
            (self.l111111l1l_opy_, "music_bxml"),
        )
        l11ll11l111_opy_.l11lllll1l1_opy_()
        self._1111llll11_opy_.close()
        return l1ll1111l1_opy_
