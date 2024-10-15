"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l111_opy_ import *
from .l1llll11l_opy_ import l1lll1ll_opy_ as l1111l11l1l_opy_
import re
from .l1l1l111l_opy_ import *
class l1l1l1111_opy_:
    def __init__(self, lou, l1l11lll1l_opy_, l1l1ll1ll_opy_, text, settings):
        self.lou = lou
        self._1l111lll_opy_ = l1l11lll1l_opy_
        self._1l1l1l1111_opy_ = l1l1ll1ll_opy_
        self._1l111ll1_opy_ = text
        (self._11111111l1_opy_, self._1llll11ll11_opy_) = settings
        self._1llll1l1l11_opy_ = 1 # l111l1111ll_opy_ of parts in the l1l1ll1ll_opy_
        self._1llll1l111l_opy_ = 1
        self._1llll1l1lll_opy_ = 0
        self._11111l1111_opy_ = False # l1lllll11l11_opy_ to l11111l1l1l_opy_ l1llll1ll1l1_opy_ to insert self._111111l111_opy_, key, time, l1l1lll111_opy_ and l1lll1lll11_opy_
        self._1llll1llll1_opy_ = [] # list of l111l1l1111_opy_ in l11l1l1l1_opy_ part
        self._111l11l11l_opy_ = 4
        self._1111111l11_opy_ = [] # list of l1111ll111l_opy_ in l11l1l1l1_opy_ part
        self._1111lllll1_opy_ = self._111l11l11l_opy_
        self._111l11ll11_opy_ = [] # list of l111111l1l1_opy_ in l11l1l1l1_opy_ part l1lllll11l11_opy_ for l11111l1ll1_opy_
        self._1111llll1l_opy_ = "" # l1lllll11l11_opy_ for l11111l1ll1_opy_
        self._1llll111ll1_opy_ = [] # list of l1lllll1l111_opy_ in l11l1l1l1_opy_ part l1lllll11l11_opy_ for l11111l1ll1_opy_
        self._1111l1l111_opy_ = "" # l1lllll11l11_opy_ for l11111l1ll1_opy_
        self._1lllll1ll1l_opy_ = [] # list of braille l1111ll1ll1_opy_ parts, l11l1l1l1_opy_ l1ll1llll1_opy_ of braille part l1111llll11_opy_ l1111l1llll_opy_ l111l1l111l_opy_ times in the braille parts l1llll1111ll_opy_ l1llllll1ll1_opy_ be used l1lllllll1ll_opy_ l11111l1l11_opy_ in the l1l1ll1ll_opy_ l1l11l1l1ll_opy_
        self._1111l11lll_opy_ = self._11111111l1_opy_[self._1llll11ll11_opy_]["ascending_chords"]
        self._111111l1ll_opy_ = 0 # key signature of l1l1l11ll11_opy_ or l1l1l11l1l1_opy_
        self._1llll11l111_opy_ = False # b14 l1llll11l1l1_opy_ note l1llll1ll111_opy_ that l1111llll11_opy_ l1111l1llll_opy_ l1111lll1ll_opy_ l1111l111l1_opy_
        self._11111l111l_opy_ = 0 # 0 no, 1 continue, 2 stop, b14+b14 4 or l1lllllll1l1_opy_ note l1llll1ll111_opy_ that l1111llll11_opy_ l1111l1llll_opy_ l1111lll1ll_opy_ l1111l111l1_opy_
        self._1lllll111ll_opy_ = 0 # 0 no, 1 start, 2 continue, b56+b12,b45+b23 4 or l1lllllll1l1_opy_ note l1llll1ll111_opy_ that l1111llll11_opy_ l1111l1llll_opy_ l1111lll1ll_opy_ l1111l111l1_opy_
        self._11111ll1ll_opy_ = ["0","0","0"] # l111l1111ll_opy_ l1llll1lll11_opy_ to l11l1l1l1_opy_ l111llll1_opy_ type, index 0 for l1llll11l1l1_opy_, 1 for l1lllll11lll_opy_, 2 for l1llll11ll1l_opy_
        self._11111llll1_opy_ = False # l1llllllll11_opy_ that l1111llll11_opy_ l111111ll11_opy_ l1111lll1ll_opy_ l1111l111l1_opy_
        self._1lllll11l1l_opy_ = 4
        self._1111lll11l_opy_ = 4
        self._1111ll11ll_opy_ = False
        self._1111ll1lll_opy_ = False
        self._1l1lll11_opy_ = None
    def l1l111l11_opy_(self):
        self._1l1lll11_opy_ = l1l1l1ll111_opy_()
        self.l1111l1lll1_opy_()
        self.l1llllll1111_opy_()
# l111111l11l_opy_ all l1l11ll1l_opy_
        p = re.compile("  *")
        for line in self._1l111ll1_opy_:
            _1111ll1111_opy_ = p.sub(" ", line)
            l111l11l1l1_opy_ = _1111ll1111_opy_.strip()
            if l111l11l1l1_opy_ != "":
                l1llll1ll11l_opy_ = self.lou.to_dots_8(l111l11l1l1_opy_)
                l1lllll111l1_opy_=l1llll1ll11l_opy_.split("\u2800")
                for l1lllll11ll1_opy_ in l1lllll111l1_opy_:
                    l1llllll11l1_opy_ = l1lllll11ll1_opy_
                    if l1llllll11l1_opy_[-1:] == "\n":
                        l1lllllllll1_opy_ = l1llllll11l1_opy_[0:-1]
                    else:
                        l1lllllllll1_opy_ = l1llllll11l1_opy_
# l1111l1ll11_opy_ l1111l111l1_opy_ and l1llll1lll1l_opy_ l1llll111lll_opy_ l1111ll1l11_opy_
                    if l1lllllllll1_opy_ in l1_opy_ or l1lllllllll1_opy_[0:2] == b56+b23 or l1lllllllll1_opy_[0] == NumeralPrefix or b2356+b3456 in l1lllllllll1_opy_ or b2356+b6+b3456 in l1lllllllll1_opy_ or (l1lllllllll1_opy_[0] == b2356 and l1lllllllll1_opy_[-1] == b2356) or (l1lllllllll1_opy_[0:2] == b345+b345 and l1lllllllll1_opy_[-1] == b3):
                        self.l1llll11l1ll_opy_ (l1llllll11l1_opy_, self._1l1lll11_opy_)
                    else:
                        self.l1llllll1lll_opy_ (l1llllll11l1_opy_, self._1l1lll11_opy_)
        self._1l111lll_opy_ ("Texts to find :\nbraille to model\nOptimize model score2, chord assign\nOptimize model score2, with measure position\nmodel to xml\n\nbraille to model\n")
        self._1l111lll_opy_ (str(self._1l1lll11_opy_))
        self.l1lllll1llll_opy_()
        return self._1l1lll11_opy_
    def l1lllll1llll_opy_(self):
        l11111lll11_opy_ = []
        if self._1l1l1l1111_opy_ is not None:
            for element in self._1l1l1l1111_opy_.l1lll1ll1l_opy_:
                if element.t == "part-list":
                    for event in element.l1lll11ll1_opy_:
                        id = event.l1ll11lll1_opy_
                        name = event.l1lllll111_opy_
                        l111111lll1_opy_ = event.l111l1l11_opy_
                        l11111lll11_opy_.append([id, name, l111111lll1_opy_])
        return l11111lll11_opy_
    def l1111l1lll1_opy_ (self):
        for line in self._1l111ll1_opy_:
            l111l11l1l1_opy_ = self.lou.to_dots_8(line)
            l1llll1ll11l_opy_=l111l11l1l1_opy_.split("\u2800")
            for l1lllll11ll1_opy_ in l1llll1ll11l_opy_:
                l1llllll11l1_opy_ = l1lllll11ll1_opy_
                if l1llllll11l1_opy_[-1:] == "\n":
                    l1lllllllll1_opy_ = l1llllll11l1_opy_[0:-1]
                else:
                    l1lllllllll1_opy_ = l1llllll11l1_opy_
                if (l1lllllllll1_opy_ in l11l_opy_ or l1lllllllll1_opy_[0:4] == b56 + b23 + b23 + b1234) and l1lllllllll1_opy_ not in self._1lllll1ll1l_opy_:
                    self._1lllll1ll1l_opy_.append (l1lllllllll1_opy_)
        self._1llll1l1l11_opy_ = len (self._1lllll1ll1l_opy_)
        self._1l111lll_opy_ ("nombre de parties " + str(self._1llll1l1l11_opy_))
        if self._1lllll1ll1l_opy_:
            self.l11111ll111_opy_ (self._1l1lll11_opy_)
        else:
            self.l1111llllll_opy_ (self._1l1lll11_opy_)
            self._1llll1llll1_opy_.append ([0,0])
        index = 0
        for element in self._1lllll1ll1l_opy_:
            self._1llll1llll1_opy_.append ([self._1lllll1ll1l_opy_[index],0])
            self._1111111l11_opy_.append(self._111l11l11l_opy_)
            self._111l11ll11_opy_.append("")
            self._1llll111ll1_opy_.append("")
            index +=1
    def l1llllll1111_opy_(self):
        l1lllll1lll1_opy_ = 8192
        l1111lll111_opy_ = []
        p = re.compile("  *")
        for line in self._1l111ll1_opy_:
            _1111ll1111_opy_ = p.sub(" ", line)
            l111l11l1l1_opy_ = _1111ll1111_opy_.strip()
            if l111l11l1l1_opy_ != "":
                l1llll1ll11l_opy_ = self.lou.to_dots_8(l111l11l1l1_opy_)
                l1lllll111l1_opy_=l1llll1ll11l_opy_.split("\u2800")
                for l1llllll11l1_opy_ in l1lllll111l1_opy_:
                    if l1llllll11l1_opy_[-1:] == "\n":
                        l1lllllllll1_opy_ = l1llllll11l1_opy_[0:-1]
                    else:
                        l1lllllllll1_opy_ = l1llllll11l1_opy_
                    if l1lllllllll1_opy_ not in l1_opy_:
                         if l1lllllllll1_opy_[0:2] != b56+b23 and l1lllllllll1_opy_[0] != NumeralPrefix and b2356+b3456 not in l1lllllllll1_opy_ and b2356+b6+b3456 not in l1lllllllll1_opy_ and (l1lllllllll1_opy_[0] != b2356 and l1lllllllll1_opy_[-1] != b2356) and (l1lllllllll1_opy_[0:2] != b345+b345 and l1lllllllll1_opy_[-1] != b3):
                            l11111111ll_opy_ = l1lllllllll1_opy_
                            for element in l1lll_opy_:
                                if element in l11111111ll_opy_:
                                    l1llll111111_opy_ = l11111111ll_opy_.replace (element, l1lll_opy_[element])
                                    l11111111ll_opy_ = l1llll111111_opy_
                            l1llllll111l_opy_ = l11111111ll_opy_.split ("·")
                            for content in l1llllll111l_opy_:
                                if content in l1l_opy_:
                                    value = l1lll1_opy_[l1l_opy_[content]]
                                    if value < l1lllll1lll1_opy_:
                                        l1lllll1lll1_opy_ = value
                                if content in ["triplet", "group3"] and (3,2) not in l1111lll111_opy_:
                                    l1111lll111_opy_.append ((3,2))
                                if content == "group2":
                                    l1111lll111_opy_.append (2,3)
                                if content == "group4":
                                    l1111lll111_opy_.append (4,3)
                                if content == "group5":
                                    l1111lll111_opy_.append (5,4)
                                if content == "group6":
                                    l1111lll111_opy_.append (6,4)
                                if content == "group7":
                                    l1111lll111_opy_.append (7,6)
                                if content == "group8":
                                    l1111lll111_opy_.append (8,6)
                                if content == "group9":
                                    l1111lll111_opy_.append (9,8)
        l1llll1ll1ll_opy_ = 1
        for l11111l11l1_opy_ in l1111lll111_opy_:
            l1llll1ll1ll_opy_ *= l11111l11l1_opy_[0]
        self._111111l111_opy_ = int (256 / l1lllll1lll1_opy_) * l1llll1ll1ll_opy_
        if self._111111l111_opy_ < 1:
            self._111111l111_opy_ = 1
        self._1l111lll_opy_ ("smallest " + str(l1lllll1lll1_opy_) + " self._divisions " + str(self._111111l111_opy_) + "\n")
        l1llll11l1_opy_ = l1llll1lll1_opy_()
        l1llll11l1_opy_.l1lll1ll11l_opy_ (str(self._111111l111_opy_))
        l11111l1lll_opy_ = l111111111_opy_()
        l11111l1lll_opy_.l1ll111111l_opy_ (l1llll11l1_opy_)
        self._1l1lll11_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[0].l1ll111111l_opy_ (l11111l1lll_opy_)
    def l1111llllll_opy_ (self, l1l1ll1ll_opy_):
        self._1llll1l1l11_opy_ = 1
        l111l11l1ll_opy_ = l111lllll1_opy_()
        l1l1ll1ll_opy_.l1ll111111l_opy_ (l111l11l1ll_opy_)
        l1llll1lllll_opy_ = l11111l1l1_opy_()
        l111l11l1ll_opy_.l11l11111l_opy_ (l1llll1lllll_opy_)
        l1llll1lllll_opy_.l1ll11111l1_opy_ (l1111l11l1l_opy_.l1ll111_opy_)
        l1llll1lllll_opy_.l111ll1l1l_opy_ (l1111l11l1l_opy_.l1l1ll11_opy_)
        l1llll1lllll_opy_.l11l11l1ll_opy_ (l1111l11l1l_opy_.l1111ll1_opy_)
        l1llll1lllll_opy_.l1lllll111l_opy_ (l1111l11l1l_opy_.l1l1llll_opy_)
        l1llll1lllll_opy_.l1ll11l1111_opy_ (l1111l11l1l_opy_.l11111l_opy_)
        l1llll1lllll_opy_.l1lll1l1l11_opy_ (l1111l11l1l_opy_.l11111_opy_)
        l1llll1lllll_opy_.l11ll1l11l_opy_ (l1111l11l1l_opy_.l1l1l111_opy_)
        l1llll1lllll_opy_.l1lll11l1ll_opy_ (l1111l11l1l_opy_.l11l1l11_opy_)
        l1llll1lllll_opy_.l1ll1l1l1ll_opy_ (l1111l11l1l_opy_.l111ll1l_opy_)
        l1llll1lllll_opy_.l111l1lll1_opy_ (l1111l11l1l_opy_.l1ll111l_opy_)
        l1llll1lllll_opy_.l11l1ll111_opy_ (l1111l11l1l_opy_.l111ll11_opy_)
        l1llll1lllll_opy_.l111l1l111_opy_ (l1111l11l1l_opy_.l11l1ll_opy_)
        part = l1llll1l1l1_opy_()
        l1l1ll1ll_opy_.l1ll111111l_opy_ (part)
        part.l1ll11111l1_opy_ (l1111l11l1l_opy_.l1ll111_opy_)
        part.l111ll1l1l_opy_ (l1111l11l1l_opy_.l1l1ll11_opy_)
        part.l11l11l1ll_opy_ (l1111l11l1l_opy_.l1111ll1_opy_)
        l11l11l11_opy_ = l1ll1llll11_opy_()
        part.l1lll11llll_opy_ (l11l11l11_opy_)
        l11l11l11_opy_.l11ll11l11_opy_ (1)
    def l11111ll111_opy_ (self, l1l1ll1ll_opy_):
        def l1llll11llll_opy_ (l1lllll111_opy_, l111l1l11_opy_, l1l1l1l111_opy_, l11111l1l_opy_, l11ll1l1l_opy_, l1lll111l1_opy_, l111l111111_opy_):
            l1llll1lllll_opy_.l111ll1l1l_opy_ (l1lllll111_opy_)
            l1llll1lllll_opy_.l11l11l1ll_opy_ (l111l1l11_opy_)
            l1llll1lllll_opy_.l1ll11l1111_opy_ (l1l1l1l111_opy_)
            l1llll1lllll_opy_.l111l1lll1_opy_ (l11111l1l_opy_)
            l1llll1lllll_opy_.l11l1ll111_opy_ (l11ll1l1l_opy_)
            l1llll1lllll_opy_.l111l1l111_opy_ (l1lll111l1_opy_)
            l1llll1lllll_opy_.l1lll11lll1_opy_ (l111l111111_opy_)
            part.l111ll1l1l_opy_ (l1lllll111_opy_)
            part.l11l11l1ll_opy_ (l111l1l11_opy_)
        l1lllll1ll11_opy_ = {
            b46+b345: (True, l1111l11l1l_opy_.l1lllll1l_opy_, l1111l11l1l_opy_.l1l111ll_opy_, l1111l11l1l_opy_.l1llllll1_opy_, l1111l11l1l_opy_.l11l11l_opy_, l1111l11l1l_opy_.l111l1_opy_, l1111l11l1l_opy_.l111l1l_opy_, False),
            b46+b345+b345: (True, l1111l11l1l_opy_.l11ll1ll_opy_, l1111l11l1l_opy_.l1l111ll_opy_, l1111l11l1l_opy_.l1llllll1_opy_, l1111l11l1l_opy_.l11l11l_opy_, l1111l11l1l_opy_.l111l1_opy_, l1111l11l1l_opy_.l111l1l_opy_, True),
            b456+b345: (True, l1111l11l1l_opy_.l1ll11ll_opy_, l1111l11l1l_opy_.l11l11_opy_, l1111l11l1l_opy_.l1ll1ll_opy_, l1111l11l1l_opy_.l11111l1_opy_, l1111l11l1l_opy_.l1lllll1_opy_, l1111l11l1l_opy_.l111ll1_opy_, True),
            b456+b345+b345: (True, l1111l11l1l_opy_.l11l1ll1_opy_, l1111l11l1l_opy_.l11l11_opy_, l1111l11l1l_opy_.l1ll1ll_opy_, l1111l11l1l_opy_.l11111l1_opy_, l1111l11l1l_opy_.l1lllll1_opy_, l1111l11l1l_opy_.l111ll1_opy_, False),
            b5+b345: (True, l1111l11l1l_opy_.l1llllll_opy_, l1111l11l1l_opy_.l1l111l1_opy_, l1111l11l1l_opy_.l1lll1lll_opy_, l1111l11l1l_opy_.l11llll1_opy_, l1111l11l1l_opy_.l111lll_opy_, l1111l11l1l_opy_.l11l1111_opy_, False),
            b45+b345: (True, l1111l11l1l_opy_.l1llll11_opy_, l1111l11l1l_opy_.l1111ll_opy_, l1111l11l1l_opy_.l111l111_opy_, l1111l11l1l_opy_.l1l11ll_opy_, l1111l11l1l_opy_.l1lll11l_opy_, l1111l11l1l_opy_.l1l1111l_opy_, True),
            b345+b234+b3: (True, l1111l11l1l_opy_.l11lll1_opy_, l1111l11l1l_opy_.l1lll1ll1_opy_, l1111l11l1l_opy_.l111l1ll_opy_, l1111l11l1l_opy_.l1l1l1ll_opy_, l1111l11l1l_opy_.l1ll11l1_opy_, l1111l11l1l_opy_.l1111lll_opy_, None),
            b345+b1+b3: (True, l1111l11l1l_opy_.l1lll1l_opy_, l1111l11l1l_opy_.l1l1l1l1_opy_, l1111l11l1l_opy_.l111llll_opy_, l1111l11l1l_opy_.l1l11l_opy_, l1111l11l1l_opy_.l111l11_opy_, l1111l11l1l_opy_.l1111l1_opy_, None),
            b345+b2345+b3: (True, l1111l11l1l_opy_.l11l1l1l_opy_, l1111l11l1l_opy_.l11ll11l_opy_, l1111l11l1l_opy_.l11l1lll_opy_, l1111l11l1l_opy_.l1llll111_opy_, l1111l11l1l_opy_.l1l11111_opy_, l1111l11l1l_opy_.l1lll1l11_opy_, None),
            b345+b12+b3: (True, l1111l11l1l_opy_.l1lll111_opy_, l1111l11l1l_opy_.l1lllll_opy_, l1111l11l1l_opy_.l1l1l11_opy_, l1111l11l1l_opy_.l1l111_opy_, l1111l11l1l_opy_.l11l11ll_opy_, l1111l11l1l_opy_.l1111l1l_opy_, None),
            b345+b234+b2+b3: (True, l1111l11l1l_opy_.l1llll1_opy_, l1111l11l1l_opy_.l11ll1_opy_, l1111l11l1l_opy_.l11l1l1_opy_, l1111l11l1l_opy_.l1111l_opy_, l1111l11l1l_opy_.l11l111_opy_, l1111l11l1l_opy_.l1l1111_opy_, None),
            b345+b1+b2+b3: (True, l1111l11l1l_opy_.l1l11l11_opy_, l1111l11l1l_opy_.l11ll111_opy_, l1111l11l1l_opy_.l1ll1lll_opy_, l1111l11l1l_opy_.l1l11l1_opy_, l1111l11l1l_opy_.l111l1l1_opy_, l1111l11l1l_opy_.l1l11l1l_opy_, None),
            b345+b2345+b2+b3: (True, l1111l11l1l_opy_.l1l1l11l_opy_, l1111l11l1l_opy_.l1llll1ll_opy_, l1111l11l1l_opy_.l1ll1l1_opy_, l1111l11l1l_opy_.l1l1ll1l_opy_, l1111l11l1l_opy_.l1ll1111_opy_, l1111l11l1l_opy_.l1ll1l11_opy_, None),
            b345+b12+b2+b3: (True, l1111l11l1l_opy_.l11l111l_opy_, l1111l11l1l_opy_.l1llll1l_opy_, l1111l11l1l_opy_.l1l11lll_opy_, l1111l11l1l_opy_.l1lllll11_opy_, l1111l11l1l_opy_.l111111l_opy_, l1111l11l1l_opy_.l1lll11l1_opy_, None),
            b345+b234+b23+b3: (True, l1111l11l1l_opy_.l11ll1l1_opy_, l1111l11l1l_opy_.l111ll_opy_, l1111l11l1l_opy_.l11lll11_opy_, l1111l11l1l_opy_.l1111l11_opy_, l1111l11l1l_opy_.l1ll1l1l_opy_, l1111l11l1l_opy_.l1l111l_opy_, None),
            b345+b1+b23+b3: (True, l1111l11l1l_opy_.l1lllllll_opy_, l1111l11l1l_opy_.l1lll1l1_opy_, l1111l11l1l_opy_.l1l1lll1_opy_, l1111l11l1l_opy_.l1111111_opy_, l1111l11l1l_opy_.l11lll_opy_, l1111l11l1l_opy_.l1ll1ll1_opy_, None),
            b345+b2345+b23+b3: (True, l1111l11l1l_opy_.l11llll_opy_, l1111l11l1l_opy_.l1lll11_opy_, l1111l11l1l_opy_.l1llll1l1_opy_, l1111l11l1l_opy_.l111l11l_opy_, l1111l11l1l_opy_.l1lll11ll_opy_, l1111l11l1l_opy_.l1l1lll_opy_, None),
            b345+b12+b23+b3: (True, l1111l11l1l_opy_.l11ll1l_opy_, l1111l11l1l_opy_.l1lll1l1l_opy_, l1111l11l1l_opy_.l11l1l_opy_, l1111l11l1l_opy_.l11111ll_opy_, l1111l11l1l_opy_.l1ll11l_opy_, l1111l11l1l_opy_.l1l1ll1_opy_, None)
        }
        l111l11l1ll_opy_ = l111lllll1_opy_()
        l1l1ll1ll_opy_.l1ll111111l_opy_ (l111l11l1ll_opy_)
        l11111ll1l1_opy_ = 0
        self._1l111lll_opy_(str(self._1lllll1ll1l_opy_))
        for element in self._1lllll1ll1l_opy_:
            l11111ll1l1_opy_ += 1
            l1llll1lllll_opy_ = l11111l1l1_opy_()
            l111l11l1ll_opy_.l11l11111l_opy_ (l1llll1lllll_opy_)
            l1llll1lllll_opy_.l1ll11111l1_opy_ ("P" + str(l11111ll1l1_opy_))
            l1llll1lllll_opy_.l1lllll111l_opy_ ("P" + str(l11111ll1l1_opy_) + "-I" + str(l11111ll1l1_opy_))
            l1llll1lllll_opy_.l1lll1l1l11_opy_ ("P" + str(l11111ll1l1_opy_) + "-I" + str(l11111ll1l1_opy_))
            l1llll1lllll_opy_.l11ll1l11l_opy_ ("1")
            l1llll1lllll_opy_.l1lll11l1ll_opy_ ("P" + str(l11111ll1l1_opy_) + "-I" + str(l11111ll1l1_opy_))
            l1llll1lllll_opy_.l1ll1l1l1ll_opy_ (str(l11111ll1l1_opy_))
            part = l1llll1l1l1_opy_()
            l1l1ll1ll_opy_.l1ll111111l_opy_ (part)
            part.l1ll11111l1_opy_ ("P" + str(l11111ll1l1_opy_))
            (l111l111ll1_opy_, l1lllll111_opy_, l111l1l11_opy_, l1l1l1l111_opy_, l11111l1l_opy_, l11ll1l1l_opy_, l1lll111l1_opy_, l111l111111_opy_) = l1lllll1ll11_opy_.get (element, (None, None, None, None, None, None, None, None))
            if l111l111ll1_opy_:
                l1llll11llll_opy_ (l1lllll111_opy_, l111l1l11_opy_, l1l1l1l111_opy_, l11111l1l_opy_, l11ll1l1l_opy_, l1lll111l1_opy_, l111l111111_opy_)
            if b56 + b23 + b23 + b1234 in element:
                if len(element) == 4:
                    l1llll11llll_opy_ (l1111l11l1l_opy_.l11ll11_opy_, l1111l11l1l_opy_.l11lll1l_opy_, l1111l11l1l_opy_.l1l1l1l_opy_, l1111l11l1l_opy_.l1l11ll1_opy_, l1111l11l1l_opy_.l11lllll_opy_, l1111l11l1l_opy_.l11l11l1_opy_, self._1111l11lll_opy_)
                else:
                    l1llll11llll_opy_ (self.lou.to_text_8(element[4:]), l1111l11l1l_opy_.l11lll1l_opy_, l1111l11l1l_opy_.l1l1l1l_opy_, l1111l11l1l_opy_.l1l11ll1_opy_, l1111l11l1l_opy_.l11lllll_opy_, l1111l11l1l_opy_.l11l11l1_opy_, self._1111l11lll_opy_)
# l1llll11111l_opy_ l11lll11l1l_opy_ empty l11l11l11_opy_
            l11l11l11_opy_ = l1ll1llll11_opy_()
            part.l1lll11llll_opy_ (l11l11l11_opy_)
            l11l11l11_opy_.l11ll11l11_opy_ (1)
    def l1llll11l1ll_opy_ (self, line, l1l1ll1ll_opy_):
        def l1llll1l11ll_opy_ (a, b, c):
            if self._1111ll1lll_opy_ and not self._1111ll11ll_opy_:
                for i in l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11llll11_opy_:
                    if i.t == "note":
                        i.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_ = int(self._1lllll11l1l_opy_) * self._111111l111_opy_ * 4 / int(self._1111lll11l_opy_))
            self._1llll1l1lll_opy_ += 1
            self._1llll1llll1_opy_ [self._1llll1l111l_opy_-1] = [self._1llll1l111l_opy_, self._1llll1l1lll_opy_]
            l11l11l11_opy_ = l1ll1llll11_opy_()
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l1lll11llll_opy_ (l11l11l11_opy_)
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11ll11l11_opy_ (self._1llll1l1lll_opy_ + 1)
            self._1111ll11ll_opy_ = False
            self._1111ll1lll_opy_ = False
        def l1llll1l1l1l_opy_ (sign, line, l1l1ll1111_opy_):
            l1lll1lll11_opy_ = l1llll11ll1_opy_()
            l1lll1lll11_opy_.l1ll1l1ll11_opy_ (sign)
            l1lll1lll11_opy_.l11ll1111l_opy_ (line)
            if l1l1ll1111_opy_ !="no":
                l1lll1lll11_opy_.l1lllllllll_opy_  (l1l1ll1111_opy_)
            if self._11111l1111_opy_:
                for event in l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11llll11_opy_:
                    if event.t == "attributes":
                        event.l1ll111111l_opy_ (l1lll1lll11_opy_)
            else:
                l1l11llll1_opy_ = l111111111_opy_()
                l1l11llll1_opy_.l1ll111111l_opy_ (l1lll1lll11_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1l11llll1_opy_)
                self._1llll11l11l_opy_ = True
        def l111l11lll1_opy_ (l1l1l1l1l1_opy_, a, b):
            key = l1l1ll11ll1_opy_()
            key.l1llllll11l_opy_ (l1l1l1l1l1_opy_)
            if self._11111l1111_opy_:
                for event in l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11llll11_opy_:
                    if event.t == "attributes":
                        event.l1ll111111l_opy_ (key)
            else:
                l1l11llll1_opy_ = l111111111_opy_()
                l1l11llll1_opy_.l1ll111111l_opy_ (key)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1l11llll1_opy_)
                self._1llll11l11l_opy_ = True
            self._111111l1ll_opy_ = int(l1l1l1l1l1_opy_)
        def l111l11ll1l_opy_ (l1l11l1111_opy_, l1l11ll111_opy_, l1ll1llll1_opy_):
            self._1lllll11l1l_opy_ = l1l11l1111_opy_
            self._1111lll11l_opy_ = l1l11ll111_opy_
            time = l111lll1ll_opy_()
            time.l11ll1l111_opy_ (l1l11l1111_opy_)
            time.l11111lll1_opy_ (l1l11ll111_opy_)
            time.l1111ll11l_opy_ (l1ll1llll1_opy_)
            if self._11111l1111_opy_:
                for event in l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11llll11_opy_:
                    if event.t == "attributes":
                        event.l1ll111111l_opy_ (time)
            else:
                l1l11llll1_opy_ = l111111111_opy_()
                l1l11llll1_opy_.l1ll111111l_opy_ (time)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1l11llll1_opy_)
                self._1llll11l11l_opy_ = True
        def l1111l1ll1l_opy_ (type, value, a):
            l1lll1111l1_opy_ = l11l11l111_opy_()
            if type != "no":
                l1lll1111l1_opy_.l1ll11ll1l1_opy_ (type)
            l1lll1111l1_opy_.l11111ll11_opy_ (self.lou.to_text_8(value))
            index = 0
            for element in l1l1ll1ll_opy_.l1lll1ll1l_opy_:
                if element.t == "part-list":
                    l1111l1111l_opy_ = index
                index +=1
            l1l1ll1ll_opy_.l1lll1ll1l_opy_.insert (l1111l1111l_opy_, l1lll1111l1_opy_)
        if line[-1:] == "\n":
            l1lllllllll1_opy_ = line[0:-1]
        else:
            l1lllllllll1_opy_ = line
        l1lllllll111_opy_ = {
            b123: (l1llll1l11ll_opy_, None, None, None),
            b126+b13+b3: (l1llll1l11ll_opy_, None, None, None),
            b345+b34+b123: (l1llll1l1l1l_opy_, "G", "2", "no"),
            b345+b34+b13: (l1llll1l1l1l_opy_, "G", "2", "no"),
            b345+b34+b45+b123: (l1llll1l1l1l_opy_, "G", "2", "no"),
            b345+b34+b45+b13: (l1llll1l1l1l_opy_, "G", "2", "no"),
            b345+b3456+b123: (l1llll1l1l1l_opy_, "F", "4", "no"),
            b345+b3456+b13: (l1llll1l1l1l_opy_, "F", "4", "no"),
            b345+b3456+b5+b123: (l1llll1l1l1l_opy_, "F", "4", "no"),
            b345+b3456+b5+b13: (l1llll1l1l1l_opy_, "F", "4", "no"),
            b345+b346+b123: (l1llll1l1l1l_opy_, "C", "4", "no"),
            b345+b346+b5+b123: (l1llll1l1l1l_opy_, "C", "4", "no"),
            b345+b34+b123+b3456+b125: (l1llll1l1l1l_opy_, "G", "2", "1"),
            b345+b34+b123+b3456+b236: (l1llll1l1l1l_opy_, "G", "2", "-1"),
            b345+b34+b4+b123: (l1llll1l1l1l_opy_, "G", "1", "no"),
            b345+b34+b4+b13: (l1llll1l1l1l_opy_, "G", "1", "no"),
            b345+b34+b456+b123: (l1llll1l1l1l_opy_, "G", "3", "no"),
            b345+b34+b456+b13: (l1llll1l1l1l_opy_, "G", "3", "no"),
            b345+b34+b5+b123: (l1llll1l1l1l_opy_, "G", "4", "no"),
            b345+b34+b5+b13: (l1llll1l1l1l_opy_, "G", "4", "no"),
            b345+b34+b46+b123: (l1llll1l1l1l_opy_, "G", "5", "no"),
            b345+b34+b46+b13: (l1llll1l1l1l_opy_, "G", "5", "no"),
            b345+b3456+b4+b123: (l1llll1l1l1l_opy_, "F", "1", "no"),
            b345+b3456+b4+b13: (l1llll1l1l1l_opy_, "F", "1", "no"),
            b345+b3456+b45+b123: (l1llll1l1l1l_opy_, "F", "2", "no"),
            b345+b3456+b45+b13: (l1llll1l1l1l_opy_, "F", "2", "no"),
            b345+b3456+b456+b123: (l1llll1l1l1l_opy_, "F", "3", "no"),
            b345+b3456+b456+b13: (l1llll1l1l1l_opy_, "F", "3", "no"),
            b345+b3456+b46+b123: (l1llll1l1l1l_opy_, "F", "5", "no"),
            b345+b3456+b46+b13: (l1llll1l1l1l_opy_, "F", "5", "no"),
            b345+b346+b4+b123: (l1llll1l1l1l_opy_, "C", "1", "no"),
            b345+b346+b45+b123: (l1llll1l1l1l_opy_, "C", "2", "no"),
            b345+b346+b456+b123: (l1llll1l1l1l_opy_, "C", "3", "no"),
            b345+b346+b46+b123: (l1llll1l1l1l_opy_, "C", "5", "no"),
            b16: (l111l11lll1_opy_, "0", None, None),
            b146: (l111l11lll1_opy_, "1", None, None),
            b146+b146: (l111l11lll1_opy_, "2", None, None),
            b146+b146+b146: (l111l11lll1_opy_, "3", None, None),
            b3456+b145+b146: (l111l11lll1_opy_, "4", None, None),
            b3456+b15+b146: (l111l11lll1_opy_, "5", None, None),
            b3456+b124+b146: (l111l11lll1_opy_, "6", None, None),
            b3456+b1245+b146: (l111l11lll1_opy_, "7", None, None),
            b126: (l111l11lll1_opy_, "-1", None, None),
            b126+b126: (l111l11lll1_opy_, "-2", None, None),
            b126+b126+b126: (l111l11lll1_opy_, "-3", None, None),
            b3456+b145+b126: (l111l11lll1_opy_, "-4", None, None),
            b3456+b15+b126: (l111l11lll1_opy_, "-5", None, None),
            b3456+b124+b126: (l111l11lll1_opy_, "-6", None, None),
            b3456+b1245+b126: (l111l11lll1_opy_, "-7", None, None),
            b46+b14: (l111l11ll1l_opy_, "4", "4", "common"),
            b456+b14: (l111l11ll1l_opy_, "2", "2", "cut")
        }
        (l1ll1l111l_opy_, sign, line, l1l1ll1111_opy_) = l1lllllll111_opy_.get (l1lllllllll1_opy_, (None, None, None, None))
        if l1ll1l111l_opy_:
            l1ll1l111l_opy_ (sign, line, l1l1ll1111_opy_)
# for l11l11l11_opy_ l111111llll_opy_ with numeral values
        if l1lllllllll1_opy_[0] == NumeralPrefix:
            l111111ll1l_opy_ = l1111l1l1ll_opy_ = ""
            for char in l1lllllllll1_opy_[1:]:
                if char in braille_high_numeral_dict:
                    l111111ll1l_opy_ += braille_high_to_numeral (char)
                if char in braille_low_numeral_dict:
                    l1111l1l1ll_opy_ += braille_low_to_numeral (char)
            if l1111l1l1ll_opy_ != "":
                l111l11ll1l_opy_(l111111ll1l_opy_, l1111l1l1ll_opy_, "no")
# for l1ll1l1l11l_opy_
        if b2356+b3456 in l1lllllllll1_opy_:
            if l1lllllllll1_opy_[0] == b13456 or l1lllllllll1_opy_[0:2] == b13456+b3:
                l1llll111l_opy_ = "whole"
            elif l1lllllllll1_opy_[0] == b1345 or l1lllllllll1_opy_[0:2] == b1345+b3:
                l1llll111l_opy_ = "half"
            elif l1lllllllll1_opy_[0] == b1456 or l1lllllllll1_opy_[0:2] == b1456+b3:
                l1llll111l_opy_ = "quarter"
            elif l1lllllllll1_opy_[0] == b145 or l1lllllllll1_opy_[0:2] == b145+b3:
                l1llll111l_opy_ = "eighth"
            l11111lll1l_opy_ = l1lllllllll1_opy_.index (b3456)
            l11111111ll_opy_ = l1lllllllll1_opy_[l11111lll1l_opy_+1:]
            l111111l1_opy_ = ""
            for char in l11111111ll_opy_:
                l111111l1_opy_ += braille_high_to_numeral (char)
            direction = l1lllll11ll_opy_()
            l1ll1l1l11l_opy_ = l1l1llll1l1_opy_()
            l1ll1l1l11l_opy_.l1llll1ll11_opy_ (l1llll111l_opy_)
            if l1lllllllll1_opy_[1] == b3:
                l1ll1l1l11l_opy_.l1lll1l111l_opy_ (True)
            l1ll1l1l11l_opy_.l11ll111l1_opy_ (l111111l1_opy_)
            direction.l1ll111111l_opy_ (l1ll1l1l11l_opy_)
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
# for l11l1l1ll1_opy_ tempo
        if b2356+b6+b3456 in l1lllllllll1_opy_:
            l1111l11l11_opy_ = l1lllllllll1_opy_.index (b3456)
            l11111111ll_opy_ = l1lllllllll1_opy_[l1111l11l11_opy_+1:]
            l111111l1_opy_ = ""
            for char in l11111111ll_opy_:
                l111111l1_opy_ += braille_high_to_numeral (char)
            #direction = l1lllll11ll_opy_()
            l11l1l1ll1_opy_ = l111l11l11_opy_()
            l11l1l1ll1_opy_.l111l1ll1l_opy_ (True)
            l11l1l1ll1_opy_.l1lllll1111_opy_ (l111111l1_opy_)
            #direction.l1ll111111l_opy_ (l11l1l1ll1_opy_)
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l11l1l1ll1_opy_)
# for l1lll1111l1_opy_, words l1111lll1l1_opy_ l111l111lll_opy_
        if l1lllllllll1_opy_[0:4] == b56+b23+b23+b2345:
            l1111l1ll1l_opy_ ("title", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b234:
            l1111l1ll1l_opy_ ("subtitle", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b14:
            l1111l1ll1l_opy_ ("composer", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b123:
            l1111l1ll1l_opy_ ("lyricist", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b1:
            l1111l1ll1l_opy_ ("arranger", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b1235:
            l1111l1ll1l_opy_ ("rights", l1lllllllll1_opy_[4:], None)
        elif l1lllllllll1_opy_[0:4] == b56+b23+b23+b2456:
            l1111l1ll1l_opy_ ("no", l1lllllllll1_opy_[4:], None)
# for words in the l1l1ll1ll_opy_
        if l1lllllllll1_opy_[0:2] == b345+b345 and l1lllllllll1_opy_[-1] == b3:
            direction = l1lllll11ll_opy_()
            words = l1lll1lllll_opy_()
            words.l1llll111ll_opy_ (self.lou.to_text_8(l1lllllllll1_opy_[2:-1]).strip())
            words.l111ll111l_opy_ (self._1llll1l111l_opy_)
            direction.l1ll111111l_opy_ (words)
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
# for l1llllllllll_opy_ l11111lllll_opy_ to l11ll1ll11_opy_ l1llll11lll1_opy_ = 1, l111l11l111_opy_ l11l1l1l1_opy_ note
        if l1lllllllll1_opy_[0] == b56 and l1lllllllll1_opy_[1] == b23 and l1lllllllll1_opy_[2] != b23:
            self.note.l1ll111l1l1_opy_ ("single")
            self.note.l1ll1l1111l_opy_ (self.lou.to_text_8(l1lllllllll1_opy_[2:]))
# for l1l1lll1ll_opy_
        if l1lllllllll1_opy_[0:4] == b56+b23+b23+b13:
            l1l1lll1ll_opy_ = l1l1ll11111_opy_()
            l1l1lll1ll_opy_.l1l1l1lllll_opy_ (self.lou.to_text_8(l1lllllllll1_opy_[4:]).strip())
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1l1lll1ll_opy_)
# for l11l1l1l1_opy_ braille part l111111llll_opy_ in the braille l1l1ll1ll_opy_, l1llllll11ll_opy_ l1111llll11_opy_ l1111l1llll_opy_ l111l1l111l_opy_ times in the l1l1ll1ll_opy_, it is l1111ll11l1_opy_ to l1111ll1l1l_opy_ : the current part, the current l11l11l11_opy_ of the current part, and other l1lllll1l1ll_opy_
        if l1lllllllll1_opy_ in self._1lllll1ll1l_opy_:
            self._1111ll11ll_opy_ = False
            self._1111ll1lll_opy_ = False
            self._1llll11l11l_opy_ = False
            self._1llll1l111l_opy_ = self._1lllll1ll1l_opy_.index (l1lllllllll1_opy_) + 1
            self._1llll1l1lll_opy_ = self._1llll1llll1_opy_ [self._1llll1l111l_opy_-1][1]
            self._1111lllll1_opy_ = self._111l11l11l_opy_
            self._1111111l11_opy_[self._1llll1l111l_opy_-1] = self._111l11l11l_opy_
            self._1111llll1l_opy_ = ""
            self._111l11ll11_opy_[self._1llll1l111l_opy_-1] = ""
            if l1lllllllll1_opy_ in l1l1_opy_:
                self._1111l11lll_opy_ = False
                l11lll1111l_opy_ = 0
                for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
                    if element.t == "part-list":
                        self._1l1lll11_opy_.l1lll1ll1l_opy_[l11lll1111l_opy_].l1lll11ll1_opy_[self._1llll1l111l_opy_-1].l1lll11lll1_opy_(False)
                    l11lll1111l_opy_ += 1
            elif l1lllllllll1_opy_ in l1l1l1_opy_:
                self._1111l11lll_opy_ = True
                l11lll1111l_opy_ = 0
                for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
                    if element.t == "part-list":
                        self._1l1lll11_opy_.l1lll1ll1l_opy_[l11lll1111l_opy_].l1lll11ll1_opy_[self._1llll1l111l_opy_-1].l1lll11lll1_opy_(True)
                    l11lll1111l_opy_ += 1
    def l1llllll1lll_opy_ (self, line, l1l1ll1ll_opy_):
        def l1llllllll1l_opy_ ():
            if self._1111ll1lll_opy_ and not self._1111ll11ll_opy_:
                for i in l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11llll11_opy_:
                    if i.t == "note":
                        i.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_ = int(self._1lllll11l1l_opy_) * self._111111l111_opy_ * 4 / int(self._1111lll11l_opy_))
            l11ll1l1l1_opy_ = l1lll11l11l_opy_()
            l11ll1l1l1_opy_.l1ll1l111ll_opy_ ("right")
            l11ll1l1l1_opy_.l1ll1ll1lll_opy_ ("light-light")
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l11ll1l1l1_opy_)
            self._1llll1l1lll_opy_ += 1
            self._1llll1llll1_opy_ [self._1llll1l111l_opy_-1] = [self._1llll1l111l_opy_, self._1llll1l1lll_opy_]
            l11l11l11_opy_ = l1ll1llll11_opy_()
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l1lll11llll_opy_ (l11l11l11_opy_)
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l11ll11l11_opy_ (self._1llll1l1lll_opy_ + 1)
            l1111l1l1l1_opy_ = l1ll111ll1l_opy_()
            l1111l1l1l1_opy_.l1ll111ll11_opy_("yes")
            l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1111l1l1l1_opy_)
            self._1111ll11ll_opy_ = False
            self._1111ll1lll_opy_ = False
        if b126+b345 in line:
            l1lllllllll1_opy_ = line.replace (b126+b345, l1lll_opy_[b126+b345])
            line = l1lllllllll1_opy_
        while b345 + b345 in line:
            l1111111lll_opy_ = line.index (b345+b345)
            try:
                l1llll1l11l1_opy_ = line.index (b3)
            except:
                l1llll1l11l1_opy_ = len(line)
            words = line[l1111111lll_opy_+2:l1llll1l11l1_opy_]
            l1lllllllll1_opy_ = line.replace (line[l1111111lll_opy_:l1llll1l11l1_opy_+1], "_words_" + self.lou.to_text_8(line[l1111111lll_opy_+2:l1llll1l11l1_opy_]) + "·")
            line = l1lllllllll1_opy_
# l1lllll1l1l1_opy_ l11l1l1l1_opy_ braille l1ll1llll1_opy_ in the l11l11l11_opy_, the l1lllllll11l_opy_ elements l1111lll1l1_opy_ the l11111ll11l_opy_, l111111111l_opy_ l1llll1l1ll1_opy_ l1l111l1ll_opy_ l111l11llll_opy_ l1111l1l11l_opy_ elements
        for element in l1lll_opy_:
            if element in line:
                l1lllllllll1_opy_ = line.replace (element, l1lll_opy_[element])
                line = l1lllllllll1_opy_
        l1llllll111l_opy_ = line.split ("·")
# l1111ll1l1l_opy_ l111l111l1l_opy_ for l11l1l1l1_opy_ new l11l11l11_opy_
        self._1llll11l11l_opy_ = False
        l1lllll1111l_opy_ = False # note of the l1l11l1l1ll_opy_
        l1111111ll1_opy_ = False # l11111l11ll_opy_ l1111l111_opy_ l1l1l11ll11_opy_ or l1l1l11l1l1_opy_
        l1111111111_opy_ = False # braille l1l1llllll_opy_ sign
        l1111l11ll1_opy_ = False # note or interval braille sign
        l1llllll1l11_opy_ = False # braille l1l1l1l1ll_opy_ sign
        l1llll111l11_opy_ = False # braille l1llll111l11_opy_ sign
        l1111l111ll_opy_ = False # l1lllll11111_opy_ l111l11111l_opy_ l1llll1l1111_opy_ l1l1ll1ll1_opy_
        l11lll111_opy_ = False
        l11lllll1_opy_ = False
        l1l1111l1l_opy_ = False
        l1llll1111l1_opy_ = [] # list of l1111l111_opy_ found in the current l11l11l11_opy_ to be used l111l111l11_opy_ the end of the l11l11l11_opy_
        l11l111l1l_opy_ = 1 # used for braille l111l1111l1_opy_ or part l11l11l11_opy_ in-l1llllll1l1l_opy_, l11111lllll_opy_ to l11l111l1l_opy_ in l1l1l11l1l_opy_ and in the l1l11l1l1ll_opy_
        l1ll11l11l_opy_ = False
        l11ll1l1l1_opy_ = False
# l1llll1l1ll1_opy_ l11l1l1l1_opy_ element of the l11l11l11_opy_
        for content in l1llllll111l_opy_:
            if content == "crescendo":
                direction = l1lllll11ll_opy_()
                l111l1l1ll_opy_ = l1lll111l1l_opy_()
                l111l1l1ll_opy_.l1lll1l11ll_opy_ (True)
                l111l1l1ll_opy_.l1ll1l11111_opy_ ("crescendo")
                direction.l1ll111111l_opy_ (l111l1l1ll_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content == "diminuendo":
                direction = l1lllll11ll_opy_()
                l111l1l1ll_opy_ = l1lll111l1l_opy_()
                l111l1l1ll_opy_.l1lll1l11ll_opy_ (True)
                l111l1l1ll_opy_.l1ll1l11111_opy_ ("diminuendo")
                direction.l1ll111111l_opy_ (l111l1l1ll_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content in ["end_crescendo", "end_diminuendo"]:
                direction = l1lllll11ll_opy_()
                l111l1l1ll_opy_ = l1lll111l1l_opy_()
                l111l1l1ll_opy_.l1lll1l11ll_opy_ (False)
                l111l1l1ll_opy_.l1ll1l11111_opy_ ("stop")
                direction.l1ll111111l_opy_ (l111l1l1ll_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content[:7] == "_words_":
                direction = l1lllll11ll_opy_()
                words = l1lll1lllll_opy_()
                words.l1llll111ll_opy_ (content[7:])
                words.l111ll111l_opy_ (self._1llll1l111l_opy_)
                direction.l1ll111111l_opy_(words)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content == "pedal_start":
                direction = l1lllll11ll_opy_()
                l1lllll1lll_opy_ = l1ll1l1l1l1_opy_()
                l1lllll1lll_opy_.l111111l11_opy_ (True)
                l1lllll1lll_opy_.l1111l1ll1_opy_ ("start")
                direction.l1ll111111l_opy_ (l1lllll1lll_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content == "pedal_stop":
                direction = l1lllll11ll_opy_()
                l1lllll1lll_opy_ = l1ll1l1l1l1_opy_()
                l1lllll1lll_opy_.l111111l11_opy_ (True)
                l1lllll1lll_opy_.l1111l1ll1_opy_ ("stop")
                direction.l1ll111111l_opy_ (l1lllll1lll_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content == "dot":
                self.note.dot = True
                self.note.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_ * 3 / 2)
            if content == "short_appoggiatura":
                l1111l111ll_opy_ = True
            if content == "staccato":
                l11lll111_opy_ = True
            if content == "staccatissimo":
                l11lllll1_opy_ = True
            if content == "accent":
                l1l1111l1l_opy_ = True
            if content in ["triplet", "group3"]:
                l1llll111l11_opy_ = True
            if content == "start_phrasing_slur":
                self._1lllll111ll_opy_ = 1
            if l1lllll1111l_opy_ == False and content in l1l1ll_opy_:
                l1lllll1111l_opy_ = True
                self.note = l1l1ll1l11l_opy_()
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (self.note)
            if l1111l11ll1_opy_ and content in l1l1ll_opy_:
                self.note = l1l1ll1l11l_opy_()
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (self.note)
                self.note.l1l1lll11l1_opy_ (str(self._1111lllll1_opy_))
                l1111111ll1_opy_ = False
                l1111111111_opy_ = False
                l1111l11ll1_opy_ = False
                l1llllll1l11_opy_ = False
            if content in l1ll1l_opy_:
                l1111111ll1_opy_ = True
                l1111111l1l_opy_ = l1ll1l_opy_[content]
                self.note.l111l1ll11_opy_ (l1ll1l_opy_[content])
                self.note.l1l11ll1l1_opy_ = content
            if content in l1ll11_opy_:
                l1111111111_opy_ = True
                l1llll111l1l_opy_ = int(l1ll11_opy_[content])
            if content in l1l_opy_:
                if content not in l1111_opy_:
                    self._1111ll11ll_opy_ = True
                l1111l11ll1_opy_ = True
                self.note.l11l1lll1l_opy_ (l1l11_opy_[content])
                self.note.l111ll11l1_opy_ (l1l_opy_[content])
                l1l1ll1ll1_opy_ = int(l1lll1_opy_[l1l_opy_[content]] / 256 * self._111111l111_opy_)
                if l1l1ll1ll1_opy_ > int(self._1lllll11l1l_opy_) * self._111111l111_opy_ and not self._1111ll11ll_opy_:
                    l1l1ll1ll1_opy_ = int(self._1lllll11l1l_opy_) * self._111111l111_opy_
                if not l1111l111ll_opy_:
                    if not l1llll111l11_opy_:
                        self.note.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_)
                    else:
                        self.note.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_ * 2 / 3)
                else:
                    self.note.l1ll1ll11l_opy_ = True
                    self.note.l1lll1l1l1_opy_ =True
                    l1111l111ll_opy_ = False
                self.note.l111l1llll_opy_ (str(l11l111l1l_opy_))
                if l1111111ll1_opy_:
                    l1llll1111l1_opy_.append ([l1l11_opy_[content],l1111111l1l_opy_])
                else:
                    self.note.l111l1ll11_opy_ (l11l1_opy_[(l1l11_opy_[content],self._111111l1ll_opy_)])
                if len(l1llll1111l1_opy_)> 0:
                    for l1l11ll1l1_opy_ in l1llll1111l1_opy_:
                        if l1l11ll1l1_opy_[0] == l1l11_opy_[content]:
                            self.note.l111l1ll11_opy_ (l1l11ll1l1_opy_[1])
                if self._1111llll1l_opy_ == "":
                    self._1111llll1l_opy_ = l1l11_opy_[content]
                if l1111111111_opy_ == False:
                    self._1111lllll1_opy_ += l111l_opy_[(self._1111llll1l_opy_,l1l11_opy_[content])]
                    self.note.l1l1lll11l1_opy_ (str(self._1111lllll1_opy_))
                else:
                    self._1111lllll1_opy_ = l1llll111l1l_opy_
                    self.note.l1l1lll11l1_opy_ (str(self._1111lllll1_opy_))
                if l1llll111l11_opy_ != 0:
                    self.note.l1111ll1l1_opy_ ("3")
                    self.note.l1llll1l1ll_opy_ ("2")
                    l1llll111l11_opy_ +=1
                    if l1llll111l11_opy_ > 3:
                        l1llll111l11_opy_ = 0
                if l11lll111_opy_:
                    self.note.l1ll1l111l1_opy_ (True)
                    l11lll111_opy_ = False
                if l11lllll1_opy_:
                    self.note.l1lllllll11_opy_ (True)
                    l11lllll1_opy_ = False
                if l1l1111l1l_opy_:
                    self.note.l1lll111111_opy_ (True)
                    l1l1111l1l_opy_ = False
                if self._1lllll111ll_opy_ == 2:
                    if self._11111ll1ll_opy_[2] == "1":
                        self.note.l111llll1_opy_ = True
                        self.note.l1lll1111l_opy_ = "above"
                        self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[2])
                        self.note.l111ll11l_opy_ = "continue"
                    elif self._11111ll1ll_opy_[2] == "2":
                        self.note.l11l1111l_opy_ = True
                        self.note.l1111111l_opy_ = "above"
                        self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[2]
                        self.note.l1l111111_opy_ = "continue"
                if self._1lllll111ll_opy_ == 1:
                    self._1lllll111ll_opy_ = 2
                    if "1" not in self._11111ll1ll_opy_:
                        self._11111ll1ll_opy_ [2] = "1"
                        self.note.l111llll1_opy_ = True
                        self.note.l1lll1111l_opy_ = "above"
                        self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[2])
                        self.note.l111ll11l_opy_ = "start"
                    elif "2" not in self._11111ll1ll_opy_:
                        self._11111ll1ll_opy_ [2] = "2"
                        self.note.l11l1111l_opy_ = True
                        self.note.l1111111l_opy_ = "above"
                        self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[2]
                        self.note.l1l111111_opy_ = "start"
                self._1111llll1l_opy_ = l1l11_opy_[content]
                self._1111l1l111_opy_ = l1l_opy_[content]
            if content in l1111_opy_:
                if content == "rest123":
                    self._1111ll1lll_opy_ = True
                l1111l11ll1_opy_ = True
                self.note.rest = True
                self.note.l111ll11l1_opy_ (l1l_opy_[content])
                l1l1ll1ll1_opy_ = l1lll1_opy_[l1l_opy_[content]] / 256 * self._111111l111_opy_
                if l1l1ll1ll1_opy_ > int(self._1lllll11l1l_opy_) * 4 * self._111111l111_opy_ / int(self._1111lll11l_opy_):
                    l1l1ll1ll1_opy_ = int(self._1lllll11l1l_opy_) * self._111111l111_opy_ * 4 / int(self._1111lll11l_opy_)
                self.note.l1ll1lllll1_opy_ (l1l1ll1ll1_opy_)
                self.note.l111l1llll_opy_ (str(l11l111l1l_opy_))
                self.note.l1l1lll11l1_opy_ ("100")
                if l1llll111l11_opy_ != 0:
                    self.note.l1111ll1l1_opy_ ("3")
                    self.note.l1llll1l1ll_opy_ ("2")
                    l1llll111l11_opy_ +=1
                    if l1llll111l11_opy_ > 3:
                        l1llll111l11_opy_ = 0
                if self._1lllll111ll_opy_ == 2:
                    if self._11111ll1ll_opy_[2] == "1":
                        self.note.l111llll1_opy_ = True
                        self.note.l1lll1111l_opy_ = "above"
                        self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[2])
                        self.note.l111ll11l_opy_ = "continue"
                    elif self._11111ll1ll_opy_[2] == "2":
                        self.note.l11l1111l_opy_ = True
                        self.note.l1111111l_opy_ = "above"
                        self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[2]
                        self.note.l1l111111_opy_ = "continue"
                if self._1lllll111ll_opy_ == 1:
                    self._1lllll111ll_opy_ = 2
                    if "1" not in self._11111ll1ll_opy_:
                        self._11111ll1ll_opy_ [2] = "1"
                        self.note.l111llll1_opy_ = True
                        self.note.l1lll1111l_opy_ = "above"
                        self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[2])
                        self.note.l111ll11l_opy_ = "start"
                    elif "2" not in self._11111ll1ll_opy_:
                        self._11111ll1ll_opy_ [2] = "2"
                        self.note.l11l1111l_opy_ = True
                        self.note.l1111111l_opy_ = "above"
                        self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[2]
                        self.note.l1l111111_opy_ = "start"
                self._1111l1l111_opy_ = l1l_opy_[content]
            if content in ll_opy_:
                l1111l11ll1_opy_ = True
                self.note.l11l1lll1l_opy_ (l11ll_opy_ [(self._1111llll1l_opy_,content,self._1111l11lll_opy_)][0])
                self.note.l111ll11l1_opy_ (self._1111l1l111_opy_)
                self.note.l1ll1lllll1_opy_ (l1lll1_opy_[self._1111l1l111_opy_] / 256 * self._111111l111_opy_)
                self.note.l11ll1lll_opy_ = True
                self.note.l111l1llll_opy_ (str(l11l111l1l_opy_))
                if l1111111111_opy_ == False:
                    l1111l11111_opy_ = self._1111lllll1_opy_ + l11ll_opy_ [(self._1111llll1l_opy_,content,self._1111l11lll_opy_)][1]
                    self.note.l1l1lll11l1_opy_ (str(l1111l11111_opy_))
                else:
                    self.note.l1l1lll11l1_opy_ (l1llll111l1l_opy_)
                if l1111111ll1_opy_:
                    l1llll1111l1_opy_.append ([l11ll_opy_ [(self._1111llll1l_opy_,content,self._1111l11lll_opy_)][0],l1111111l1l_opy_])
                else:
                    self.note.l111l1ll11_opy_ (l11l1_opy_[(l11ll_opy_ [(self._1111llll1l_opy_,content,self._1111l11lll_opy_)][0],self._111111l1ll_opy_)])
                if l1llll111l11_opy_ != 0:
                    self.note.l1111ll1l1_opy_ ("3")
                    self.note.l1llll1l1ll_opy_ ("2")
            if content in l1l1l_opy_:
                l1llllll1l11_opy_ = True
                if self.note:
                    self.note.l1l1l1l1ll_opy_ = l1l1l_opy_[content]
                else:
                    return
            if l1lllll1111l_opy_ and self._1llll11l111_opy_:
                self._1llll11l111_opy_ = False
                if self._11111ll1ll_opy_[0] == "1":
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[0])
                    self.note.l111ll11l_opy_ = "stop"
                elif self._11111ll1ll_opy_[0] == "2":
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[0]
                    self.note.l1l111111_opy_ = "stop"
                self._11111ll1ll_opy_[0] = "0"
            if content == "slur12" and self._11111l111l_opy_ != 1:
                self._1llll11l111_opy_ = True
                if "1" not in self._11111ll1ll_opy_:
                    self._11111ll1ll_opy_ [0] = "1"
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[0])
                    self.note.l111ll11l_opy_ = "start"
                elif "2" not in self._11111ll1ll_opy_:
                    self._11111ll1ll_opy_ [0] = "2"
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[0]
                    self.note.l1l111111_opy_ = "start"
            if l1lllll1111l_opy_ and self._11111l111l_opy_ == 2:
                self._11111l111l_opy_ = 0
                if self._11111ll1ll_opy_[1] == "1":
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[1])
                    self.note.l111ll11l_opy_ = "stop"
                elif self._11111ll1ll_opy_[1] == "2":
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[1]
                    self.note.l1l111111_opy_ = "stop"
                self._11111ll1ll_opy_[1] = "0"
            if content == "slur12" and self._11111l111l_opy_ == 1:
                self._11111l111l_opy_ = 2
                if self._11111ll1ll_opy_[1] == "1":
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[1])
                    self.note.l111ll11l_opy_ = "continue"
                elif self._11111ll1ll_opy_[1] == "2":
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[1]
                    self.note.l1l111111_opy_ = "continue"
            if l1lllll1111l_opy_ and self._11111l111l_opy_ == 1:
                if self._11111ll1ll_opy_[1] == "1":
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[1])
                    self.note.l111ll11l_opy_ = "continue"
                elif self._11111ll1ll_opy_[1] == "2":
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[1]
                    self.note.l1l111111_opy_ = "continue"
            if content == "phrasing_slur":
                self._11111l111l_opy_ = 1
                if "1" not in self._11111ll1ll_opy_:
                    self._11111ll1ll_opy_ [1] = "1"
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[1])
                    self.note.l111ll11l_opy_ = "start"
                elif "2" not in self._11111ll1ll_opy_:
                    self._11111ll1ll_opy_ [1] = "2"
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[1]
                    self.note.l1l111111_opy_ = "start"
            if content == "end_phrasing_slur":
                self._1lllll111ll_opy_ = 0
                if self._11111ll1ll_opy_[2] == "1":
                    self.note.l111llll1_opy_ = True
                    self.note.l1lll1111l_opy_ = "above"
                    self.note.l1llll1ll1l_opy_ (self._11111ll1ll_opy_[2])
                    self.note.l111ll11l_opy_ = "stop"
                if self._11111ll1ll_opy_[2] == "2":
                    self.note.l11l1111l_opy_ = True
                    self.note.l1111111l_opy_ = "above"
                    self.note.l1lll11lll_opy_ = self._11111ll1ll_opy_[2]
                    self.note.l1l111111_opy_ = "stop"
                self._11111ll1ll_opy_[2] = "0"
            if l1lllll1111l_opy_ and self._11111llll1_opy_:
                self._11111llll1_opy_ = False
                self.note.l111llll11_opy_ (True)
                self.note.l11l11ll1l_opy_ ("stop")
            if content == "single_note_tie":
                self._11111llll1_opy_ = True
                self.note.l111llll11_opy_ (True)
                self.note.l11l11ll1l_opy_ ("start")
            if content == "breath_mark":
                self.note.l111l1l1l1_opy_ (True)
            if content == "fermata":
                self.note.l11111l111_opy_ (True)
            if content == "full_measure_in_accord":
                l11l111l1l_opy_ +=1
                l1lllll1l11l_opy_ = l1111l1lll_opy_()
                l1lllll1l11l_opy_.l1l111l1lll_opy_ (True)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1lllll1l11l_opy_)
            if content == "part_measure_in_accord":
                l11l111l1l_opy_ +=1
                l1lllll1l11l_opy_ = l1111l1lll_opy_()
                l1lllll1l11l_opy_.l1l111l1lll_opy_ (False)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l1lllll1l11l_opy_)
            if content == "measure_division":
                l11l111l1l_opy_ = 1
            if content in l1ll_opy_:
                direction = l1lllll11ll_opy_ ()
                l1ll11l11l_opy_ = l1lll1lll1l_opy_()
                l1ll11l11l_opy_.l1ll1ll111l_opy_ (content)
                direction.l1ll111111l_opy_ (l1ll11l11l_opy_)
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (direction)
            if content == "end_composition_double_bar":
                l11ll1l1l1_opy_ = l1lll11l11l_opy_()
                l11ll1l1l1_opy_.l1ll1l111ll_opy_ ("right")
                l11ll1l1l1_opy_.l1ll1ll1lll_opy_ ("light-heavy")
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l11ll1l1l1_opy_)
            if content == "end_measure_double_bar":
                l1llllllll1l_opy_()
            if content == "begin_repeat":
                l11ll1l1l1_opy_ = l1lll11l11l_opy_()
                l11ll1l1l1_opy_.l1ll1l111ll_opy_ ("left")
                l11ll1l1l1_opy_.l1ll1ll1lll_opy_ ("heavy-light")
                l11ll1l1l1_opy_.l1l1llll1ll_opy_ ("forward")
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l11ll1l1l1_opy_)
            if content == "end_repeat":
                l11ll1l1l1_opy_ = l1lll11l11l_opy_()
                l11ll1l1l1_opy_.l1ll1l111ll_opy_ ("right")
                l11ll1l1l1_opy_.l1ll1ll1lll_opy_ ("light-heavy")
                l11ll1l1l1_opy_.l1l1llll1ll_opy_ ("backward")
                l1l1ll1ll_opy_.l1lll1ll1l_opy_[-(1+self._1llll1l1l11_opy_-self._1llll1l111l_opy_)].l11l1llll_opy_[self._1llll1l1lll_opy_].l1ll111111l_opy_ (l11ll1l1l1_opy_)
            if content not in l1ll11_opy_ and content not in l1l_opy_ and content not in l1ll1l_opy_ and content not in ll_opy_ and content not in l1l1l_opy_ and content != "dot":
                l1lllll1111l_opy_ = False
                l1111111ll1_opy_ = False
                l1111111111_opy_ = False
                l1111l11ll1_opy_ = False
                l1llllll1l11_opy_ = False