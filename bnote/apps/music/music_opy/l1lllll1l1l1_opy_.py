"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l111ll11111_opy_ import *
from .l1l11l111_opy_ import *
from .l111111ll11_opy_ import l11111l1111_opy_
class l1lllll1l111_opy_:
    def __init__(self, lou, l1l1lllll_opy_, l11llll11_opy_):
        self.lou = lou
        self._1l1ll111_opy_ = l1l1lllll_opy_
        self.l11llll11_opy_ = l11llll11_opy_
        self._11llllll_opy_ = None
        self._1l1111ll_opy_ = None
    def l11lll1ll_opy_(self, line):
        self._11llllll_opy_.write(line + "\n")
    def l1l111lll_opy_(self, line):
        text = line.replace('\n', '')
        text = text.replace(' ', '\u2800')
        if len(text) > 0:
            text = self.lou.to_text_8(text)
            self._1l1111ll_opy_(text)
    def l11lll11l11_opy_(self, l11llll11l_opy_, encoding=None):
        self._1l1111ll_opy_ = l11llll11l_opy_
        self._11llllll_opy_ = open("trace_musicxml.txt", "w", encoding='utf-8')
        l1l11ll11_opy_ = l111111lll1_opy_()
        l111ll11111_opy_ = l1l111ll1ll_opy_(self.lou, self._1l1ll111_opy_, self.l11llll11_opy_)
        l111ll11111_opy_.l11lll11l11_opy_(self.l11lll1ll_opy_, l1l11ll11_opy_)
        l1lllll1l11l_opy_ = l11lll1l1_opy_(self.l11lll1ll_opy_, l1l11ll11_opy_)
        l1lllll1l11l_opy_.l1l1111l1_opy_()
        l1lllll1l11l_opy_.l11lll111_opy_()
        l111111ll11_opy_ = l11111l1111_opy_(self.lou, self.l1l111lll_opy_, self.l11lll1ll_opy_, l1l11ll11_opy_, (self.l11llll11_opy_, 'music_xml'))
        l111111ll11_opy_.l111111llll_opy_()
        self._11llllll_opy_.close()
        return l1l11ll11_opy_