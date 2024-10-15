"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l111ll1lll_opy_ import *
from .l1l1l1ll1_opy_ import *
from .l1l1l1ll1ll_opy_ import l1l1l1l1lll_opy_
class l1l11lll111_opy_:
    def __init__(self, lou, l1l1ll1l1_opy_, l1l1ll111_opy_):
        self.lou = lou
        self._1l1lllll_opy_ = l1l1ll1l1_opy_
        self.l1l1ll111_opy_ = l1l1ll111_opy_
        self._1l11l1ll_opy_ = None
        self._1l111lll_opy_ = None
    def l1l111l1l_opy_(self, line):
        self._1l11l1ll_opy_.write(line + "\n")
    def l1l1l11l1_opy_(self, line):
        text = line.replace('\n', '')
        text = text.replace(' ', '\u2800')
        if len(text) > 0:
            text = self.lou.to_text_8(text)
            self._1l111lll_opy_(text)
    def l1lllll1l11_opy_(self, l1l11lll1l_opy_, encoding=None):
        self._1l111lll_opy_ = l1l11lll1l_opy_
        self._1l11l1ll_opy_ = open("trace_musicxml.txt", "w", encoding='utf-8')
        l1l1ll1ll_opy_ = l1l1l1ll111_opy_()
        l111ll1lll_opy_ = l1ll1111111_opy_(self.lou, self._1l1lllll_opy_, self.l1l1ll111_opy_)
        l111ll1lll_opy_.l1lllll1l11_opy_(self.l1l111l1l_opy_, l1l1ll1ll_opy_)
        l1l11ll1lll_opy_ = l1l1ll11l_opy_(self.l1l111l1l_opy_, l1l1ll1ll_opy_)
        l1l11ll1lll_opy_.l1l1l11ll_opy_()
        l1l11ll1lll_opy_.l1l11l1l1_opy_()
        l1l1l1ll1ll_opy_ = l1l1l1l1lll_opy_(self.lou, self.l1l1l11l1_opy_, self.l1l111l1l_opy_, l1l1ll1ll_opy_, (self.l1l1ll111_opy_, 'music_xml'))
        l1l1l1ll1ll_opy_.l1l1l1ll11l_opy_()
        #for element in l1l11lll11l_opy_.l1lll1ll1l_opy_:
            #print("oui")
        self._1l11l1ll_opy_.close()
        return l1l1ll1ll_opy_