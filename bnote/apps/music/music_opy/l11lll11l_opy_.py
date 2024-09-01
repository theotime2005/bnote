"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l11111l_opy_ import *
from .l111l1l_opy_ import l111111_opy_ as l11l1ll_opy_
import re
from .l1l111ll1_opy_ import *
import time


class l1l11l1l1_opy_:
    def __init__(self, lou, l11llll11l_opy_, l1l11ll11_opy_, text, settings):
        self.lou = lou
        self._1l1111ll_opy_ = l11llll11l_opy_
        self._1111111ll1_opy_ = l1l11ll11_opy_
        self.l1ll11111111_opy_ = list()
        self.l1ll1l1ll1ll_opy_ = list()
        self._1l11111l_opy_ = text
        (self._1ll111l11l1_opy_, self._1ll111ll111_opy_) = settings
        self._1ll11lll111_opy_ = 1  # l1ll1llll111_opy_ of parts in the l1l11ll11_opy_
        self._1lll111l111_opy_ = 1
        self._1ll1l1l11l1_opy_ = 0
        self._1ll111l1111_opy_ = False  # l1ll11l11lll_opy_ to l1ll1ll1l11l_opy_ l1ll11ll1l11_opy_ to insert self._1ll11l1l1l1_opy_, key, time, l1111111ll_opy_ and l1l1ll1l111_opy_
        self._1ll11111l11_opy_ = False  # l1ll11l11lll_opy_ to l1ll1ll1l11l_opy_ l1ll11ll1l11_opy_ to insert l1ll1llll111_opy_, title
        self._1ll11111ll1_opy_ = []  # list of l1ll111l1lll_opy_ in l1lll11ll1l1_opy_ part
        self._1ll11llllll_opy_ = 4
        self._1ll111ll1l1_opy_ = list()  # list of l1ll1ll11111_opy_ in l1lll11ll1l1_opy_ part
        self._1ll1lll11l1_opy_ = self._1ll11llllll_opy_
        self._1ll11l1ll11_opy_ = []  # list of l1l1llllllll_opy_ in l1lll11ll1l1_opy_ part l1ll11l11lll_opy_ for l1ll1l11l11l_opy_
        self._1ll1l1l1l11_opy_ = ""  # l1ll11l11lll_opy_ for l1ll1l11l11l_opy_
        self._1ll1l11llll_opy_ = []  # list of l1ll1ll1llll_opy_ in l1lll11ll1l1_opy_ part l1ll11l11lll_opy_ for l1ll1l11l11l_opy_
        self._1ll11l1llll_opy_ = ""  # l1ll11l11lll_opy_ for l1ll1l11l11l_opy_
        self._1ll11ll11ll_opy_ = []  # list of braille l1ll11lllll1_opy_ parts, l1lll11ll1l1_opy_ l11lllll1l_opy_ of braille part l1ll1l1l111l_opy_ l1ll1l111ll1_opy_ l1l1llllll11_opy_ times in the braille parts l1ll11l11l11_opy_ l1ll1ll1l1ll_opy_ be used l1ll1l1l1l1l_opy_ l1lll111ll1l_opy_ in the l1l11ll11_opy_ l1llll1ll1ll_opy_
        self._1ll111111ll_opy_ = self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['ascending_chords']
        self._1ll1l111l11_opy_ = 0  # key signature of l1lllllllll1_opy_ or l111111111l_opy_
        self._1ll1l111lll_opy_ = False  # b14 l1ll1l11ll11_opy_ note l1ll11l11111_opy_ that l1ll1l1l111l_opy_ l1ll1l111ll1_opy_ l1ll11ll1111_opy_ l1ll1l111111_opy_, l1ll1l1ll11l_opy_ l1ll11ll1111_opy_ l1ll1l1ll1l1_opy_
        self._1ll1l1l1111_opy_ = "no"  # l1ll1l1l111l_opy_ be no, continue or stop. b14 + b14 4 or l1ll1lll1111_opy_ note l1ll11l11111_opy_ that l1ll1l1l111l_opy_ l1ll1l111ll1_opy_ l1ll11ll1111_opy_ l1ll1l111111_opy_ l1ll1l1ll11l_opy_ l1ll11ll1111_opy_ l1ll1l1ll1l1_opy_
        self._1ll1lll1l1l_opy_ = "no"  # l1ll1l1l111l_opy_ be no, start or continue. b56 + b12,b45 + b23 4 or l1ll1lll1111_opy_ note l1ll11l11111_opy_ that l1ll1l1l111l_opy_ l1ll1l111ll1_opy_ l1ll11ll1111_opy_ l1ll1l1ll1l1_opy_
        self._1ll1ll1ll1l_opy_ = ["0", "0",
                                  "0"]  # l1ll1llll111_opy_ l1ll1l11l111_opy_ to l1lll11ll1l1_opy_ l1llllll1ll_opy_ type, index 0 for l1ll1l11ll11_opy_, 1 for l1ll1llll11l_opy_, 2 for l1lll111ll11_opy_
        self._1ll11l11l1l_opy_ = False  # l1lll111l11l_opy_ that l1ll1l1l111l_opy_ l1lll111l1l1_opy_ l1lll11111l1_opy_ or l1ll11ll1111_opy_ l1ll1l1ll1l1_opy_
        self.l1lll111l11l_opy_ = list()
        self._1ll1111l111_opy_ = 4
        self._1ll1ll1l111_opy_ = 4
        self._1ll11l111l1_opy_ = False
        self._1ll1ll1111l_opy_ = False
        self.l11ll111l1_opy_ = False
        self.l1ll111l111l_opy_ = {}
        self.l1llll1111l1_opy_ = "no"
        self._1l1l11ll_opy_ = None

    def l1ll111lll1l_opy_(self, braille):
        """ Converts a braille string from dots to text
        the braille string can be in grade0 or in grade1, depending on the corresponding parametter"""
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["braille_type"] == 'dot-8':
            return self.lou.to_text_8(braille)
        else:
            return self.lou.l1ll1lll11ll_opy_(self.lou.to_text_8(braille))[0]

    def l1ll111ll1ll_opy_(self, text):
        """ Converts a string from text to braille"""
        return self.lou.to_dots_8(text)

    def l11ll1ll1_opy_(self):
        """ Converts all the braille text to the model"""
        t1 = time.time()
        self.l1l11ll11l_opy_ = True
        self.l1ll1111111l_opy_()
        self._1l1l11ll_opy_ = l111111lll1_opy_()
        self.l1ll11ll1l1l_opy_()
        self.l1ll1llllll1_opy_()
        self.l1ll1lll1lll_opy_()
        self.l1ll111llll1_opy_()
        for block in self.l1ll1ll1lll1_opy_:
            if block in l1l1_opy_ or block[0:2] == b56 + b23 or (block[0] == NumeralPrefix and block[
                1] not in braille_low_numeral_dict) or b2356 + b3456 in block or b2356 + b6 + b3456 in block or (
                    block[0] == b2356 and block[-1] == b2356) or (block[0:2] == b345 + b345 and block[-1] == b3):
                self.l1ll1lll1ll1_opy_(block, self._1l1l11ll_opy_)
            else:
                self.l1lll111l1ll_opy_(block, self._1l1l11ll_opy_)
        if self.l1l11ll11l_opy_:
            self._1l1111ll_opy_(
                "Texts to find :\nbraille to model\nOptimize model score2, chord assign\nOptimize model score2, with measure position\nmodel to xml\n\nbraille to model\n")
            self._1l1111ll_opy_(str(self._1l1l11ll_opy_))
        self.l1ll1l1111l1_opy_()
        l1l1111lll_opy_ = time.time()
        return self._1l1l11ll_opy_

    def l1ll1111111l_opy_(self):
        self.l1ll1ll1lll1_opy_ = list()
        p = re.compile("  *")
        for line in self._1l11111l_opy_:
            _1ll1l1lll1l_opy_ = p.sub(" ", line)
            l1ll1llll1ll_opy_ = _1ll1l1lll1l_opy_.strip()
            if l1ll1llll1ll_opy_ != "":
                l1ll11ll1ll1_opy_ = self.l1ll111ll1ll_opy_(l1ll1llll1ll_opy_)
                l1ll1l1l11ll_opy_ = l1ll11ll1ll1_opy_.split("\u2800")
                for l1lll11111ll_opy_ in l1ll1l1l11ll_opy_:
                    l1ll11llll11_opy_ = l1lll11111ll_opy_
                    if l1ll11llll11_opy_[-1:] == "\n":
                        l1ll1ll11lll_opy_ = l1ll11llll11_opy_[0:-1]
                    else:
                        l1ll1ll11lll_opy_ = l1ll11llll11_opy_
                    self.l1ll1ll1lll1_opy_.append(l1ll1ll11lll_opy_)

    def l1ll11ll1l1l_opy_(self):
        for l1ll1ll11lll_opy_ in self.l1ll1ll1lll1_opy_:
            if (l1ll1ll11lll_opy_ in l1l1lll_opy_ or l1ll1ll11lll_opy_[
                                                     0:4] == b56 + b23 + b23 + b1234) and l1ll1ll11lll_opy_ not in self._1ll11ll11ll_opy_:
                self._1ll11ll11ll_opy_.append(l1ll1ll11lll_opy_)
        if self.l1l11ll11l_opy_:
            self._1l1111ll_opy_("nombre de parties " + str(self._1ll11lll111_opy_))

    def l1ll1llllll1_opy_(self):
        l1ll1l11l1l1_opy_ = {
            b46 + b345: (True, l11l1ll_opy_.l111l11_opy_, l11l1ll_opy_.l1ll_opy_, l11l1ll_opy_.l11l1l1l_opy_,
                         l11l1ll_opy_.l111ll11_opy_, l11l1ll_opy_.l1111ll1_opy_, l11l1ll_opy_.l1l1111l_opy_,
                         l11l1ll_opy_.l1ll1l11l_opy_),
            b46 + b345 + b345: (True, l11l1ll_opy_.l1l1l_opy_, l11l1ll_opy_.l11l1l1_opy_, l11l1ll_opy_.l1ll111l_opy_,
                                l11l1ll_opy_.l1ll11ll_opy_, l11l1ll_opy_.l1l1l111_opy_, l11l1ll_opy_.l1lllll1l_opy_,
                                l11l1ll_opy_.l1lllll11_opy_),
            b456 + b345: (True, l11l1ll_opy_.l1l111l_opy_, l11l1ll_opy_.l1l1ll_opy_, l11l1ll_opy_.l11l1ll1_opy_,
                          l11l1ll_opy_.l1ll1ll1l_opy_, l11l1ll_opy_.l1ll1111_opy_, l11l1ll_opy_.l11l1111_opy_,
                          l11l1ll_opy_.l1ll1ll11_opy_),
            b456 + b345 + b345: (True, l11l1ll_opy_.l11ll1_opy_, l11l1ll_opy_.l1l1111_opy_, l11l1ll_opy_.l1ll1l111_opy_,
                                 l11l1ll_opy_.l11llll1_opy_, l11l1ll_opy_.l1ll11ll1_opy_, l11l1ll_opy_.l1l1ll1l_opy_,
                                 l11l1ll_opy_.l111l111_opy_),
            b5 + b345: (True, l11l1ll_opy_.l11lll_opy_, l11l1ll_opy_.l111_opy_, l11l1ll_opy_.l1l11l11_opy_,
                        l11l1ll_opy_.l1ll1llll_opy_, l11l1ll_opy_.l1lll11ll_opy_, l11l1ll_opy_.l11ll1l1_opy_,
                        l11l1ll_opy_.l11l111l_opy_),
            b45 + b345: (True, l11l1ll_opy_.l11ll11_opy_, l11l1ll_opy_.l1lll1_opy_, l11l1ll_opy_.l1lll1lll_opy_,
                         l11l1ll_opy_.l11l11l1_opy_, l11l1ll_opy_.l1llll1l_opy_, l11l1ll_opy_.l1lll11l1_opy_,
                         l11l1ll_opy_.l1l1llll_opy_),
            b345 + b234 + b3: (True, l11l1ll_opy_.l11lll1_opy_, l11l1ll_opy_.l1llll_opy_, l11l1ll_opy_.l1l1l1ll_opy_,
                               l11l1ll_opy_.l1lll1111_opy_, l11l1ll_opy_.l1ll1l1l1_opy_, l11l1ll_opy_.l11lllll_opy_,
                               '0'),
            b345 + b1 + b3: (True, l11l1ll_opy_.l111ll_opy_, l11l1ll_opy_.l1llll1_opy_, l11l1ll_opy_.l1ll1l1l_opy_,
                             l11l1ll_opy_.l1lll1ll1_opy_, l11l1ll_opy_.l11ll111_opy_, l11l1ll_opy_.l111ll1l_opy_, '0'),
            b345 + b2345 + b3: (True, l11l1ll_opy_.l1ll1l1_opy_, l11l1ll_opy_.l111lll_opy_, l11l1ll_opy_.l1ll1l1ll_opy_,
                                l11l1ll_opy_.l1ll11l11_opy_, l11l1ll_opy_.l111l1l1_opy_, l11l1ll_opy_.l1llllll1_opy_,
                                '0'),
            b345 + b12 + b3: (True, l11l1ll_opy_.l1l1ll1_opy_, l11l1ll_opy_.l111ll1_opy_, l11l1ll_opy_.l1lll1l1_opy_,
                              l11l1ll_opy_.l1l1lll1_opy_, l11l1ll_opy_.l11l11ll_opy_, l11l1ll_opy_.l1ll1lll1_opy_, '0'),
            b345 + b234 + b2 + b3: (True, l11l1ll_opy_.l11ll1l_opy_, l11l1ll_opy_.l11_opy_, l11l1ll_opy_.l111llll_opy_,
                                    l11l1ll_opy_.l1llll11_opy_, l11l1ll_opy_.l111111l_opy_, l11l1ll_opy_.l1lllllll_opy_,
                                    '0'),
            b345 + b1 + b2 + b3: (True, l11l1ll_opy_.l11llll_opy_, l11l1ll_opy_.l1111_opy_, l11l1ll_opy_.l1lll111_opy_,
                                  l11l1ll_opy_.l1l11111_opy_, l11l1ll_opy_.l1l111ll_opy_, l11l1ll_opy_.l1ll1ll1_opy_,
                                  '0'),
            b345 + b2345 + b2 + b3: (
                True, l11l1ll_opy_.l1l1l1_opy_, l11l1ll_opy_.l11l11_opy_, l11l1ll_opy_.l11l1l11_opy_,
                l11l1ll_opy_.l1ll1lll_opy_, l11l1ll_opy_.l1llll11l_opy_, l11l1ll_opy_.l111l11l_opy_, '0'),
            b345 + b12 + b2 + b3: (True, l11l1ll_opy_.l1l11l_opy_, l11l1ll_opy_.l1l111_opy_, l11l1ll_opy_.l1l111l1_opy_,
                                   l11l1ll_opy_.l1lll11l_opy_, l11l1ll_opy_.l11111l1_opy_, l11l1ll_opy_.l1111lll_opy_,
                                   '0'),
            b345 + b234 + b23 + b3: (
                True, l11l1ll_opy_.l1lllll_opy_, l11l1ll_opy_.l1l11l1_opy_, l11l1ll_opy_.l1lll1l1l_opy_,
                l11l1ll_opy_.l1111l11_opy_, l11l1ll_opy_.l1l1l1l1_opy_, l11l1ll_opy_.l1ll11lll_opy_, '0'),
            b345 + b1 + b23 + b3: (True, l11l1ll_opy_.l11l1_opy_, l11l1ll_opy_.l11l11l_opy_, l11l1ll_opy_.l11ll11l_opy_,
                                   l11l1ll_opy_.l1l11lll_opy_, l11l1ll_opy_.l1l11ll1_opy_, l11l1ll_opy_.l111l1ll_opy_,
                                   '0'),
            b345 + b2345 + b23 + b3: (
                True, l11l1ll_opy_.l1_opy_, l11l1ll_opy_.ll_opy_, l11l1ll_opy_.l11lll11_opy_,
                l11l1ll_opy_.l1lllll1_opy_,
                l11l1ll_opy_.l1llll1l1_opy_, l11l1ll_opy_.l1111111_opy_, '0'),
            b345 + b12 + b23 + b3: (
                True, l11l1ll_opy_.l1l1l1l_opy_, l11l1ll_opy_.l1l1l11_opy_, l11l1ll_opy_.l1111l1l_opy_,
                l11l1ll_opy_.l1lll111l_opy_, l11l1ll_opy_.l11l1lll_opy_, l11l1ll_opy_.l1llll1ll_opy_, '0')
        }
        l1ll11111l1l_opy_ = l1l1ll1111l_opy_()
        self._1l1l11ll_opy_.l1l11l1llll_opy_(l1ll11111l1l_opy_)
        l1ll1l11lll1_opy_ = 0
        for part in self._1ll11ll11ll_opy_:
            l1ll1l11lll1_opy_ += 1
            found = False
            (l1ll11llll1l_opy_, l111lll1ll_opy_, l11111ll1l_opy_, l1lllll111l_opy_, l11ll11l11_opy_, l1lllll1lll_opy_,
             l1111ll1ll_opy_, l1ll11l1l11l_opy_) = l1ll1l11l1l1_opy_.get(part, (
                None, None, None, None, None, None, None, None))
            for element in self._1111111ll1_opy_.l1lll1l111l_opy_:
                if element.t == "part-list":
                    for l1l11111l1_opy_ in element.l111l1l1l1_opy_:
                        if (self._1ll111l11l1_opy_[self._1ll111ll111_opy_][
                                "parts"] == 'name' and self.l1ll111lll1l_opy_(
                            part[4:]) == l1l11111l1_opy_.l111lll1ll_opy_) or (
                                self._1ll111l11l1_opy_[self._1ll111ll111_opy_][
                                    "parts"] == 'abbreviation' and self.l1ll111lll1l_opy_(
                            part[4:]) == l1l11111l1_opy_.l11111ll1l_opy_) or (
                                l1ll11llll1l_opy_ and l111lll1ll_opy_ == l1l11111l1_opy_.l111lll1ll_opy_):
                            found = True
                            l1ll11111l1l_opy_.l1111lll111_opy_(l1l11111l1_opy_)
                            l1l11111l1_opy_.l1l11l11l11_opy_("P" + str(l1ll1l11lll1_opy_))
                            l1ll1lll111l_opy_ = l1l11ll1l11_opy_()
                            self._1l1l11ll_opy_.l1l11l1llll_opy_(l1ll1lll111l_opy_)
                            l1ll1lll111l_opy_.l1l11l11l11_opy_("P" + str(l1ll1l11lll1_opy_))
                            l1ll1lll111l_opy_.l11lll1lll1_opy_(l1l11111l1_opy_.l111lll1ll_opy_)
                            l1ll1lll111l_opy_.l11lll1ll1l_opy_(l1l11111l1_opy_.l11111ll1l_opy_)
                            l111111l1l_opy_ = l1l1l1l1l1l_opy_()
                            l1ll1lll111l_opy_.l11l1l11111_opy_(l111111l1l_opy_)
                            l111111l1l_opy_.l1ll111l111_opy_(1)
                            self._1ll11111ll1_opy_.append([l1ll1l11lll1_opy_ - 1, 0])
                            self._1ll111ll1l1_opy_.append(self._1ll11llllll_opy_)
                            self._1ll11l1ll11_opy_.append("")
            if not found:
                if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name' and part[:4] == "".join(
                        [b56, b23, b23, b1234]):
                    l1ll11111l1l_opy_.l1111lll111_opy_(
                        self.l1ll1l1llll1_opy_(l1ll1l11lll1_opy_, "no", l11l1ll_opy_.l1lll1l_opy_,
                                               l11l1ll_opy_.l1l1ll11_opy_, l11l1ll_opy_.l11ll1ll_opy_,
                                               l11l1ll_opy_.l1lll1l11_opy_, l11l1ll_opy_.l1ll11l1l_opy_,
                                               l11l1ll_opy_.l11lll1l_opy_, self.l1ll111lll1l_opy_(part[4:])))
                elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation' and part[:4] == "".join(
                        [b56, b23, b23, b1234]):
                    l1ll11111l1l_opy_.l1111lll111_opy_(
                        self.l1ll1l1llll1_opy_(l1ll1l11lll1_opy_, l11l1ll_opy_.l11l_opy_, "no",
                                               l11l1ll_opy_.l1l1ll11_opy_, l11l1ll_opy_.l11ll1ll_opy_,
                                               l11l1ll_opy_.l1lll1l11_opy_, l11l1ll_opy_.l1ll11l1l_opy_,
                                               l11l1ll_opy_.l11lll1l_opy_, self.l1ll111lll1l_opy_(part[4:])))
                elif l1ll11llll1l_opy_:
                    l1ll11111l1l_opy_.l1111lll111_opy_(
                        self.l1ll1l1llll1_opy_(l1ll1l11lll1_opy_, l111lll1ll_opy_, l11111ll1l_opy_, l1lllll111l_opy_,
                                               l11ll11l11_opy_, l1lllll1lll_opy_, l1111ll1ll_opy_, l1ll11l1l11l_opy_))
        if l1ll1l11lll1_opy_ == 0:
            l1ll11111l1l_opy_.l1111lll111_opy_(
                self.l1ll1l1llll1_opy_(l1ll1l11lll1_opy_ + 1, l11l1ll_opy_.l11l_opy_, l11l1ll_opy_.l1lll1l_opy_,
                                       l11l1ll_opy_.l1l1ll11_opy_, l11l1ll_opy_.l11ll1ll_opy_,
                                       l11l1ll_opy_.l1lll1l11_opy_, l11l1ll_opy_.l1ll11l1l_opy_,
                                       l11l1ll_opy_.l11lll1l_opy_))
            self._1ll11111ll1_opy_.append([0, 0])
        else:
            self._1ll11lll111_opy_ = l1ll1l11lll1_opy_

    def l1ll1l1llll1_opy_(self, l1ll1l11lll1_opy_, l111lll1ll_opy_, l11111ll1l_opy_, l1lllll111l_opy_, l11ll11l11_opy_,
                          l1lllll1lll_opy_, l1111ll1ll_opy_, l1ll11l1l11l_opy_, l1ll1111l1l1_opy_="no"):
        l1l11lllll1_opy_ = l1l11lll11l_opy_()
        l1l11lllll1_opy_.l1l11l11l11_opy_("P" + str(l1ll1l11lll1_opy_))
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name' and l1ll1111l1l1_opy_ != "no":
            l1l11lllll1_opy_.l11lll1lll1_opy_(l1ll1111l1l1_opy_)
            l1l11lllll1_opy_.l11lll1ll1l_opy_(l11l1ll_opy_.l1lll1l_opy_)
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation' and l1ll1111l1l1_opy_ != "no":
            l1l11lllll1_opy_.l11lll1ll1l_opy_(l1ll1111l1l1_opy_)
            l1l11lllll1_opy_.l11lll1lll1_opy_(l11l1ll_opy_.l11l_opy_)
        if l111lll1ll_opy_ != "no":
            l1l11lllll1_opy_.l11lll1lll1_opy_(l111lll1ll_opy_)
        if l11111ll1l_opy_ != "no":
            l1l11lllll1_opy_.l11lll1ll1l_opy_(l11111ll1l_opy_)
        l1l11lllll1_opy_.l11ll111ll1_opy_("P" + str(l1ll1l11lll1_opy_) + "-I" + str(l1ll1l11lll1_opy_))
        l1l11lllll1_opy_.l111lll1ll1_opy_(l1lllll111l_opy_)
        l1l11lllll1_opy_.l11lll1l1ll_opy_("P" + str(l1ll1l11lll1_opy_) + "-I" + str(l1ll1l11lll1_opy_))
        l1l11lllll1_opy_.l111l1ll1ll_opy_("1")
        l1l11lllll1_opy_.l11lllllll1_opy_("P" + str(l1ll1l11lll1_opy_) + "-I" + str(l1ll1l11lll1_opy_))
        l1l11lllll1_opy_.l111l1llll1_opy_(str(l1ll111_opy_[l1ll1l11lll1_opy_ % 15]))
        l1l11lllll1_opy_.l11lll111ll_opy_(l11ll11l11_opy_)
        l1l11lllll1_opy_.l11lll1ll11_opy_(l1lllll1lll_opy_)
        l1l11lllll1_opy_.l11l1l1l11l_opy_(l1111ll1ll_opy_)
        l1l11lllll1_opy_.l11l111l1ll_opy_(l1ll11l1l11l_opy_)
        part = l1l11ll1l11_opy_()
        self._1l1l11ll_opy_.l1l11l1llll_opy_(part)
        part.l1l11l11l11_opy_("P" + str(l1ll1l11lll1_opy_))
        part.l11lll1lll1_opy_(l1l11lllll1_opy_.l111lll1ll_opy_)
        part.l11lll1ll1l_opy_(l1l11lllll1_opy_.l11111ll1l_opy_)
        l111111l1l_opy_ = l1l1l1l1l1l_opy_()
        part.l11l1l11111_opy_(l111111l1l_opy_)
        l111111l1l_opy_.l1ll111l111_opy_(1)
        self._1ll11111ll1_opy_.append([l1ll1l11lll1_opy_ - 1, 0])
        self._1ll111ll1l1_opy_.append(self._1ll11llllll_opy_)
        self._1ll11l1ll11_opy_.append("")
        return l1l11lllll1_opy_

    def l1ll1lll1lll_opy_(self):
        def l1ll1l1lllll_opy_(l1lll1l1l11_opy_, a, b, c):
            l11111l11l1_opy_ = l111lll1l1l_opy_()
            l11111l11l1_opy_.l11ll1ll111_opy_(l1lll1l1l11_opy_)
            l11l1111l1l_opy_.l1l11l1llll_opy_(l11111l11l1_opy_)

        def l1l1lllll1l1_opy_(l1l1l11111_opy_, l1111lll11_opy_, l11lllll1l_opy_, l1ll11lll1ll_opy_):
            l1l111ll111_opy_ = l1111l111l1_opy_()
            l1l111ll111_opy_.l1111ll1l11_opy_(l1l1l11111_opy_)
            l1l111ll111_opy_.l1l1ll111l1_opy_(l1111lll11_opy_)
            l1l111ll111_opy_.l11ll11111l_opy_(l11lllll1l_opy_)
            l11l1111l1l_opy_.l1l11l1llll_opy_(l1l111ll111_opy_)
            self._1ll1111l111_opy_ = l1l1l11111_opy_
            self._1ll1ll1l111_opy_ = l1111lll11_opy_

        l1ll1l11111l_opy_ = {
            b16: (l1ll1l1lllll_opy_, "0", None, None, None),
            b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b3456 + b124 + b146: (l1ll1l1lllll_opy_, "6", None, None, None),
            b3456 + b1245 + b146: (l1ll1l1lllll_opy_, "7", None, None, None),
            b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b3456 + b124 + b126: (l1ll1l1lllll_opy_, "-6", None, None, None),
            b3456 + b1245 + b126: (l1ll1l1lllll_opy_, "-7", None, None, None),
            b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b16 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b145 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b15 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b124 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b16 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b145 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b15 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b124 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b16 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b3456 + b145 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b3456 + b15 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b16 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b3456 + b145 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b3456 + b15 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b16 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b3456 + b145 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b16 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b3456 + b145 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b16 + b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b16 + b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b16 + b16 + b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b16 + b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b16 + b16 + b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b16 + b3456 + b124 + b146: (l1ll1l1lllll_opy_, "6", None, None, None),
            b16 + b3456 + b124 + b126: (l1ll1l1lllll_opy_, "-6", None, None, None),
            b46 + b14: (l1l1lllll1l1_opy_, "4", "4", "common", None),
            b456 + b14: (l1l1lllll1l1_opy_, "2", "2", "cut", None)
        }
        l1ll1lll1l11_opy_ = False
        l1lll1111l1l_opy_ = False
        l1ll111lll11_opy_ = False
        l1ll1ll1l1l1_opy_ = list()
        for l1ll1ll11lll_opy_ in self.l1ll1ll1lll1_opy_:
            if l1ll1ll11lll_opy_ in self._1ll11ll11ll_opy_:
                l1lll1111l1l_opy_ = True
            if l1ll1ll11lll_opy_ in l11l1l_opy_:
                l1ll111lll11_opy_ = True
            if l1ll111lll11_opy_ and not l1lll1111l1l_opy_ and self._1ll11ll11ll_opy_ != []:
                l1ll1lll1l11_opy_ = True
                l1ll1ll1l1l1_opy_.append(l1ll1ll11lll_opy_)
            if l1ll1lll1l11_opy_:
                break
        if l1ll1lll1l11_opy_:
            l11l1111l1l_opy_ = l1l11ll11l1_opy_()
        for l1ll1ll11lll_opy_ in l1ll1ll1l1l1_opy_:
            (l1ll1l1ll111_opy_, sign, line, l1lllll1111_opy_, braille) = l1ll1l11111l_opy_.get(l1ll1ll11lll_opy_, (
                None, None, None, None, None))
            if l1ll1l1ll111_opy_:
                l1ll1l1ll111_opy_(sign, line, l1lllll1111_opy_, braille)
            if l1ll1ll11lll_opy_[0] == NumeralPrefix:
                l1ll11ll1lll_opy_ = l1ll1ll11ll1_opy_ = ""
                for char in l1ll1ll11lll_opy_[1:]:
                    if char in braille_high_numeral_dict:
                        l1ll11ll1lll_opy_ += braille_high_to_numeral(char)
                    if char in braille_low_numeral_dict:
                        l1ll1ll11ll1_opy_ += braille_low_to_numeral(char)
                if l1ll1ll11ll1_opy_ != "":
                    l1l1lllll1l1_opy_(l1ll11ll1lll_opy_, l1ll1ll11ll1_opy_, "no", "no")
        if l1ll1lll1l11_opy_:
            self._1l1l11ll_opy_.l1lll1l111l_opy_.insert(0, l11l1111l1l_opy_)

    def l1ll111llll1_opy_(self):
        l1ll1l11ll1l_opy_ = 8192
        l1l1lllllll1_opy_ = []
        for l1ll1ll11lll_opy_ in self.l1ll1ll1lll1_opy_:
            if l1ll1ll11lll_opy_ not in l1l1_opy_:
                if l1ll1ll11lll_opy_[0:2] != b56 + b23 and l1ll1ll11lll_opy_[
                    0] != NumeralPrefix and b2356 + b3456 not in l1ll1ll11lll_opy_ and b2356 + b6 + b3456 not in l1ll1ll11lll_opy_ and (
                        l1ll1ll11lll_opy_[0] != b2356 and l1ll1ll11lll_opy_[-1] != b2356) and (
                        l1ll1ll11lll_opy_[0:2] != b345 + b345 and l1ll1ll11lll_opy_[-1] != b3):
                    l1ll111ll11l_opy_ = l1ll1ll11lll_opy_
                    for element in l1111l_opy_:
                        if element in l1ll111ll11l_opy_:
                            l1ll111l1l1l_opy_ = l1ll111ll11l_opy_.replace(element, l1111l_opy_[element])
                            l1ll111ll11l_opy_ = l1ll111l1l1l_opy_
                    l1ll1llll1l1_opy_ = l1ll111ll11l_opy_.split("·")
                    for content in l1ll1llll1l1_opy_:
                        if content in l1111ll_opy_:
                            value = l1ll1ll_opy_[l1111ll_opy_[content]]
                            if value < l1ll1l11ll1l_opy_:
                                l1ll1l11ll1l_opy_ = value
                        if content in ["triplet", "group3"] and (3, 2) not in l1l1lllllll1_opy_:
                            l1l1lllllll1_opy_.append((3, 2))
                        if content == "group2":
                            l1l1lllllll1_opy_.append(2, 3)
                        if content == "group4":
                            l1l1lllllll1_opy_.append(4, 3)
                        if content == "group5":
                            l1l1lllllll1_opy_.append(5, 4)
                        if content == "group6":
                            l1l1lllllll1_opy_.append(6, 4)
                        if content == "group7":
                            l1l1lllllll1_opy_.append(7, 6)
                        if content == "group8":
                            l1l1lllllll1_opy_.append(8, 6)
                        if content == "group9":
                            l1l1lllllll1_opy_.append(9, 8)
        l1ll11l11ll1_opy_ = 1
        for l1ll111l1ll1_opy_ in l1l1lllllll1_opy_:
            l1ll11l11ll1_opy_ *= l1ll111l1ll1_opy_[0]
        self._1ll11l1l1l1_opy_ = int(256 / l1ll1l11ll1l_opy_) * l1ll11l11ll1_opy_
        if self._1ll11l1l1l1_opy_ < 1:
            self._1ll11l1l1l1_opy_ = 1
        if self.l1l11ll11l_opy_:
            self._1l1111ll_opy_(
                "smallest " + str(l1ll1l11ll1l_opy_) + " self._divisions " + str(self._1ll11l1l1l1_opy_) + "\n")
        l111l1111l_opy_ = l1l1lll1111_opy_()
        l111l1111l_opy_.l11lllll1ll_opy_(str(self._1ll11l1l1l1_opy_))
        l1ll1l1l1ll1_opy_ = l111l1ll11l_opy_()
        l1ll1l1l1ll1_opy_.l1l11l1llll_opy_(l111l1111l_opy_)
        self._1l1l11ll_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
            0].l1l11l1llll_opy_(l1ll1l1l1ll1_opy_)

    def l1ll1ll11l11_opy_(self, l1ll1ll11lll_opy_):
        self._1ll1l111l11_opy_ = 0
        self._1ll11l111l1_opy_ = False
        self._1ll1ll1111l_opy_ = False
        self._1ll11l1111l_opy_ = False
        self._1lll111l111_opy_ = self._1ll11ll11ll_opy_.index(l1ll1ll11lll_opy_) + 1
        self._1ll1l1l11l1_opy_ = self._1ll11111ll1_opy_[self._1lll111l111_opy_ - 1][1]
        self._1ll1lll11l1_opy_ = self._1ll11llllll_opy_
        self._1ll111ll1l1_opy_[self._1lll111l111_opy_ - 1] = self._1ll11llllll_opy_
        self._1ll1l1l1l11_opy_ = ""
        self._1ll11l1ll11_opy_[self._1lll111l111_opy_ - 1] = ""
        self._1ll111111ll_opy_ = self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['ascending_chords']
        if l1ll1ll11lll_opy_ in l1llllll_opy_:
            self._1ll111111ll_opy_ = False
            l1lll1l1111l_opy_ = 0
            for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if element.t == "part-list":
                    self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                        self._1lll111l111_opy_ - 1].l11l111l1ll_opy_("-1")
                l1lll1l1111l_opy_ += 1
        elif l1ll1ll11lll_opy_ in l1ll11_opy_:
            self._1ll111111ll_opy_ = True
            l1lll1l1111l_opy_ = 0
            for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if element.t == "part-list":
                    self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                        self._1lll111l111_opy_ - 1].l11l111l1ll_opy_("1")
                l1lll1l1111l_opy_ += 1

    def _1ll1ll1ll11_opy_(self, l1l11111l1_opy_, l1ll1ll11lll_opy_) -> bool:
        l1lll1111l11_opy_ = l1ll1ll11lll_opy_[6:l1ll1ll11lll_opy_.index(b25)]
        print(l1lll1111l11_opy_, l1lll1111l11_opy_ in l1l1lll_opy_)
        return (
                (self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name'
                 and (l1l11111l1_opy_.l111lll1ll_opy_ == self.l1ll111lll1l_opy_(l1lll1111l11_opy_)
                      or (l1lll1111l11_opy_ in l1l1lll_opy_ and l1l1lll_opy_[l1lll1111l11_opy_][
                                    0] == l1l11111l1_opy_.l111lll1ll_opy_)
                      )
                 )
                or (self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation'
                    and (l1l11111l1_opy_.l11111ll1l_opy_ == self.l1ll111lll1l_opy_(l1lll1111l11_opy_)
                         or (l1lll1111l11_opy_ in l1l1lll_opy_ and l1l1lll_opy_[l1lll1111l11_opy_][
                            1] == l1l11111l1_opy_.l11111ll1l_opy_)
                         )
                    )
        )

    def l11ll11l11_opy_(self, l1ll1ll11lll_opy_):
        l1lll1l1111l_opy_ = 0
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part-list":
                l1l1lllll1ll_opy_ = 0
                for l1l11111l1_opy_ in element.l111l1l1l1_opy_:
                    if self._1ll1ll1ll11_opy_(l1l11111l1_opy_, l1ll1ll11lll_opy_):
                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                            l1l1lllll1ll_opy_].l11lll111ll_opy_(
                            self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:]))
                    l1l1lllll1ll_opy_ += 1
            l1lll1l1111l_opy_ += 1

    def l111ll11ll_opy_(self, l1ll1ll11lll_opy_):
        l1lll1l1111l_opy_ = 0
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part-list":
                l1l1lllll1ll_opy_ = 0
                for l1l11111l1_opy_ in element.l111l1l1l1_opy_:
                    if self._1ll1ll1ll11_opy_(l1l11111l1_opy_, l1ll1ll11lll_opy_):
                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                            l1l1lllll1ll_opy_].l111l1llll1_opy_(
                            self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:]))
                    l1l1lllll1ll_opy_ += 1
            l1lll1l1111l_opy_ += 1

    def l1lllll1lll_opy_(self, l1ll1ll11lll_opy_):
        l1lll1l1111l_opy_ = 0
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part-list":
                l1l1lllll1ll_opy_ = 0
                for l1l11111l1_opy_ in element.l111l1l1l1_opy_:
                    if self._1ll1ll1ll11_opy_(l1l11111l1_opy_, l1ll1ll11lll_opy_):
                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                            l1l1lllll1ll_opy_].l11lll1ll11_opy_(
                            self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:]))
                    l1l1lllll1ll_opy_ += 1
            l1lll1l1111l_opy_ += 1

    def l1ll1l1111l1_opy_(self):
        l1ll1111l1ll_opy_ = 0
        for key in self.l1ll111l111l_opy_.items():
            l1l1l11l1ll_opy_ = l111l1ll11l_opy_()
            l1ll1ll11ll_opy_ = l11l1l1l1l1_opy_()
            l1lll1l1111l_opy_ = 0
            for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if element.t == "part" and ((self._1ll111l11l1_opy_[self._1ll111ll111_opy_][
                                                 "parts"] == 'name' and element.l111lll1ll_opy_ == key[0]) or (
                                                    self._1ll111l11l1_opy_[self._1ll111ll111_opy_][
                                                        "parts"] == 'abbreviation' and element.l11111ll1l_opy_ == key[
                                                        0])):
                    if key[1][0] != "":
                        l1ll1ll11ll_opy_.l11lll1llll_opy_(key[1][0])
                    if key[1][1] != "":
                        l1ll1ll11ll_opy_.l111ll1l11l_opy_(key[1][1])
                    if key[1][2] != "":
                        l1ll1ll11ll_opy_.l111l1ll1l1_opy_(key[1][2])
                    if key[1][3]:
                        l1ll1ll11ll_opy_.l1l1l1111l1_opy_(key[1][3])
                        if key[1][4] != "":
                            l1ll1ll11ll_opy_.l1111l11111_opy_(key[1][4])
                    l1l1l11l1ll_opy_.l1l11l1llll_opy_(l1ll1ll11ll_opy_)
                    element.l11l1l1ll1_opy_[0].l111l11lll_opy_.insert(0, l1l1l11l1ll_opy_)
                l1lll1l1111l_opy_ += 1
            l1ll1111l1ll_opy_ += 1

    def l1ll1lll1ll1_opy_(self, line, l1l11ll11_opy_):
        def l1lll1111lll_opy_(a, b, c, d):
            if self._1ll1ll1111l_opy_ and not self._1ll11l111l1_opy_:
                for i in \
                        l1l11ll11_opy_.l1lll1l111l_opy_[
                            -(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                            self._1ll1l1l11l1_opy_].l111l11lll_opy_:
                    if i.t == "note":
                        i.l11lll1111l_opy_(
                            l11lll1l11_opy_=int(self._1ll1111l111_opy_) * self._1ll11l1l1l1_opy_ * 4 / int(
                                self._1ll1ll1l111_opy_))
            self._1ll1l1l11l1_opy_ += 1
            self._1ll11111ll1_opy_[self._1lll111l111_opy_ - 1] = [self._1lll111l111_opy_, self._1ll1l1l11l1_opy_]
            l111111l1l_opy_ = l1l1l1l1l1l_opy_()
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l11111_opy_(
                l111111l1l_opy_)
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1ll111l111_opy_(self._1ll1l1l11l1_opy_ + 1)
            self._1ll11l111l1_opy_ = False
            self._1ll1ll1111l_opy_ = False

        def l1ll11l111ll_opy_(sign, line, l1lllll1111_opy_, braille):
            l1l1ll1l111_opy_ = l1l111l11l1_opy_()
            l1l1ll1l111_opy_.l1111l1ll1l_opy_(sign)
            l1l1ll1l111_opy_.l11l1l11l11_opy_(line)
            if l1lllll1111_opy_ != "no":
                l1l1ll1l111_opy_.l111lll11ll_opy_(l1lllll1111_opy_)
            if braille != "no":
                l1l1ll1l111_opy_.l111lll111l_opy_(braille)
            if self._1ll111l1111_opy_:
                for event in \
                        l1l11ll11_opy_.l1lll1l111l_opy_[
                            -(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                            self._1ll1l1l11l1_opy_].l111l11lll_opy_:
                    if event.t == "attributes":
                        event.l1l11l1llll_opy_(l1l1ll1l111_opy_)
            else:
                l1l1l11l1ll_opy_ = l111l1ll11l_opy_()
                l1l1l11l1ll_opy_.l1l11l1llll_opy_(l1l1ll1l111_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1l1l11l1ll_opy_)
                self._1ll11l1111l_opy_ = True

        def l1ll1l1lllll_opy_(l1lll1l1l11_opy_, a, b, c):
            key = l1l1l11l111_opy_()
            key.l11ll1ll111_opy_(l1lll1l1l11_opy_)
            if self._1ll111l1111_opy_:
                for event in \
                        l1l11ll11_opy_.l1lll1l111l_opy_[
                            -(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                            self._1ll1l1l11l1_opy_].l111l11lll_opy_:
                    if event.t == "attributes":
                        event.l1l11l1llll_opy_(key)
            else:
                l1l1l11l1ll_opy_ = l111l1ll11l_opy_()
                l1l1l11l1ll_opy_.l1l11l1llll_opy_(key)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1l1l11l1ll_opy_)
                self._1ll11l1111l_opy_ = True
            self._1ll1l111l11_opy_ = int(l1lll1l1l11_opy_)

        def l1l1lllll1l1_opy_(l1l1l11111_opy_, l1111lll11_opy_, l11lllll1l_opy_, l1ll11lll1ll_opy_):
            self._1ll1111l111_opy_ = l1l1l11111_opy_
            self._1ll1ll1l111_opy_ = l1111lll11_opy_
            time = l1l1ll11111_opy_()
            time.l1111ll1l11_opy_(l1l1l11111_opy_)
            time.l1l1ll111l1_opy_(l1111lll11_opy_)
            time.l11ll11111l_opy_(l11lllll1l_opy_)
            if self._1ll111l1111_opy_:
                for event in \
                        l1l11ll11_opy_.l1lll1l111l_opy_[
                            -(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                            self._1ll1l1l11l1_opy_].l111l11lll_opy_:
                    if event.t == "attributes":
                        event.l1l11l1llll_opy_(time)
            else:
                l1l1l11l1ll_opy_ = l111l1ll11l_opy_()
                l1l1l11l1ll_opy_.l1l11l1llll_opy_(time)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1l1l11l1ll_opy_)
                self._1ll11l1111l_opy_ = True

        def l1lll1111ll1_opy_(type, value):
            l1l11l1l111_opy_ = l1l1l1ll111_opy_()
            if type != "no":
                l1l11l1l111_opy_.l111ll1llll_opy_(type)
            l1l11l1l111_opy_.l1l1l11l11l_opy_(self.l1ll111lll1l_opy_(value))
            index = 0
            for element in l1l11ll11_opy_.l1lll1l111l_opy_:
                if element.t == "braille-global":
                    l1l11ll11_opy_.l1lll1l111l_opy_.insert(index, l1l11l1l111_opy_)
                    break
                if element.t == "part-list":
                    l1l11ll11_opy_.l1lll1l111l_opy_.insert(index, l1l11l1l111_opy_)
                    break
                index += 1

        def l1ll11lll11l_opy_(type, value):
            """work = Work()
            if type == "title":
                work.set_work_title(self.braille_to_text(value))
            elif type == "number":
                work.set_work_number(self.braille_to_text(value))"""
            if self._1ll11111l11_opy_:
                for event in l1l11ll11_opy_.l1lll1l111l_opy_:
                    if event.t == "work":
                        if type == "title":
                            event.l11ll1lllll_opy_(self.l1ll111lll1l_opy_(value))
                        elif type == "number":
                            event.l1l1l11lll1_opy_(self.l1ll111lll1l_opy_(value))
            else:
                l1ll111l1l1_opy_ = l1l11ll1111_opy_()
                if type == "title":
                    l1ll111l1l1_opy_.l11ll1lllll_opy_(self.l1ll111lll1l_opy_(value))
                elif type == "number":
                    l1ll111l1l1_opy_.l1l1l11lll1_opy_(self.l1ll111lll1l_opy_(value))
                index = 0
                for element in l1l11ll11_opy_.l1lll1l111l_opy_:
                    if element.t == "credit":
                        l1l11ll11_opy_.l1lll1l111l_opy_.insert(index, l1ll111l1l1_opy_)
                        break
                    if element.t == "braille-global":
                        l1l11ll11_opy_.l1lll1l111l_opy_.insert(index, l1ll111l1l1_opy_)
                        break
                    if element.t == "part-list":
                        l1l11ll11_opy_.l1lll1l111l_opy_.insert(index, l1ll111l1l1_opy_)
                        break
                    index += 1
                self._1ll11l1111l_opy_ = True
            # index = 0
            # for element in l1l11ll11_opy_.l1lll1l111l_opy_:
            # if element.t == "braille-global":
            # if element.t == "part-list":
            # index +=1

        if line[-1:] == "\n":
            l1ll1ll11lll_opy_ = line[0:-1]
        else:
            l1ll1ll11lll_opy_ = line
        l1ll1ll111l1_opy_ = {
            b123: (l1lll1111lll_opy_, None, None, None, None),
            b126 + b13 + b3: (l1lll1111lll_opy_, None, None, None, None),
            b345 + b34 + b123: (l1ll11l111ll_opy_, "G", "2", "no", "no"),
            b345 + b34 + b13: (l1ll11l111ll_opy_, "G", "2", "no", "hand"),
            b345 + b3456 + b123: (l1ll11l111ll_opy_, "F", "4", "no", "no"),
            b345 + b3456 + b13: (l1ll11l111ll_opy_, "F", "4", "no", "hand"),
            b345 + b346 + b123: (l1ll11l111ll_opy_, "C", "4", "no", "no"),
            b345 + b34 + b4 + b123: (l1ll11l111ll_opy_, "G", "1", "no", "no"),
            b345 + b34 + b4 + b13: (l1ll11l111ll_opy_, "G", "1", "no", "hand"),
            b345 + b34 + b45 + b123: (l1ll11l111ll_opy_, "G", "2", "no", "double"),
            b345 + b34 + b45 + b13: (l1ll11l111ll_opy_, "G", "2", "no", "double-hand"),
            b345 + b34 + b456 + b123: (l1ll11l111ll_opy_, "G", "3", "no", "no"),
            b345 + b34 + b456 + b13: (l1ll11l111ll_opy_, "G", "3", "no", "hand"),
            b345 + b34 + b5 + b123: (l1ll11l111ll_opy_, "G", "4", "no", "no"),
            b345 + b34 + b5 + b13: (l1ll11l111ll_opy_, "G", "4", "no", "hand"),
            b345 + b34 + b46 + b123: (l1ll11l111ll_opy_, "G", "5", "no", "no"),
            b345 + b34 + b46 + b13: (l1ll11l111ll_opy_, "G", "5", "no", "hand"),
            b345 + b3456 + b4 + b123: (l1ll11l111ll_opy_, "F", "1", "no", "no"),
            b345 + b3456 + b4 + b13: (l1ll11l111ll_opy_, "F", "1", "no", "hand"),
            b345 + b3456 + b45 + b123: (l1ll11l111ll_opy_, "F", "2", "no", "no"),
            b345 + b3456 + b45 + b13: (l1ll11l111ll_opy_, "F", "2", "no", "hand"),
            b345 + b3456 + b456 + b123: (l1ll11l111ll_opy_, "F", "3", "no", "no"),
            b345 + b3456 + b456 + b13: (l1ll11l111ll_opy_, "F", "3", "no", "hand"),
            b345 + b3456 + b5 + b123: (l1ll11l111ll_opy_, "F", "4", "no", "double"),
            b345 + b3456 + b5 + b13: (l1ll11l111ll_opy_, "F", "4", "no", "double-hand"),
            b345 + b3456 + b46 + b123: (l1ll11l111ll_opy_, "F", "5", "no", "no"),
            b345 + b3456 + b46 + b13: (l1ll11l111ll_opy_, "F", "5", "no", "hand"),
            b345 + b346 + b4 + b123: (l1ll11l111ll_opy_, "C", "1", "no", "no"),
            b345 + b346 + b45 + b123: (l1ll11l111ll_opy_, "C", "2", "no", "no"),
            b345 + b346 + b456 + b123: (l1ll11l111ll_opy_, "C", "3", "no", "no"),
            b345 + b346 + b5 + b123: (l1ll11l111ll_opy_, "C", "4", "no", "double"),
            b345 + b346 + b46 + b123: (l1ll11l111ll_opy_, "C", "5", "no", "no"),
            b345 + b34 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "2", "1", "no"),
            b345 + b34 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "2", "1", "hand"),
            b345 + b3456 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "4", "1", "no"),
            b345 + b3456 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "4", "1", "hand"),
            b345 + b346 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "4", "1", "no"),
            b345 + b34 + b4 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "1", "1", "no"),
            b345 + b34 + b4 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "1", "1", "hand"),
            b345 + b34 + b45 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "2", "1", "no"),
            b345 + b34 + b45 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "2", "1", "hand"),
            b345 + b34 + b456 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "3", "1", "no"),
            b345 + b34 + b456 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "3", "1", "hand"),
            b345 + b34 + b5 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "4", "1", "no"),
            b345 + b34 + b5 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "4", "1", "hand"),
            b345 + b34 + b46 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "G", "5", "1", "no"),
            b345 + b34 + b46 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "G", "5", "1", "hand"),
            b345 + b3456 + b4 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "1", "1", "no"),
            b345 + b3456 + b4 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "1", "1", "hand"),
            b345 + b3456 + b45 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "2", "1", "no"),
            b345 + b3456 + b45 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "2", "1", "hand"),
            b345 + b3456 + b456 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "3", "1", "no"),
            b345 + b3456 + b456 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "3", "1", "hand"),
            b345 + b3456 + b5 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "4", "1", "no"),
            b345 + b3456 + b5 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "4", "1", "hand"),
            b345 + b3456 + b46 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "F", "5", "1", "no"),
            b345 + b3456 + b46 + b13 + b3456 + b125: (l1ll11l111ll_opy_, "F", "5", "1", "hand"),
            b345 + b346 + b4 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "1", "1", "no"),
            b345 + b346 + b45 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "2", "1", "no"),
            b345 + b346 + b456 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "3", "1", "no"),
            b345 + b346 + b5 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "4", "1", "no"),
            b345 + b346 + b46 + b123 + b3456 + b125: (l1ll11l111ll_opy_, "C", "5", "1", "no"),
            b345 + b34 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "2", "-1", "no"),
            b345 + b34 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "2", "-1", "hand"),
            b345 + b3456 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "4", "-1", "no"),
            b345 + b3456 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "4", "-1", "hand"),
            b345 + b346 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "4", "-1", "no"),
            b345 + b34 + b4 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "1", "-1", "no"),
            b345 + b34 + b4 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "1", "-1", "hand"),
            b345 + b34 + b45 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "2", "-1", "no"),
            b345 + b34 + b45 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "2", "-1", "hand"),
            b345 + b34 + b456 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "3", "-1", "no"),
            b345 + b34 + b456 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "3", "-1", "hand"),
            b345 + b34 + b5 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "4", "-1", "no"),
            b345 + b34 + b5 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "4", "-1", "hand"),
            b345 + b34 + b46 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "G", "5", "-1", "no"),
            b345 + b34 + b46 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "G", "5", "-1", "hand"),
            b345 + b3456 + b4 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "1", "-1", "no"),
            b345 + b3456 + b4 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "1", "-1", "hand"),
            b345 + b3456 + b45 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "2", "-1", "no"),
            b345 + b3456 + b45 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "2", "-1", "hand"),
            b345 + b3456 + b456 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "3", "-1", "no"),
            b345 + b3456 + b456 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "3", "-1", "hand"),
            b345 + b3456 + b5 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "4", "-1", "no"),
            b345 + b3456 + b5 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "4", "-1", "hand"),
            b345 + b3456 + b46 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "F", "5", "-1", "no"),
            b345 + b3456 + b46 + b13 + b3456 + b236: (l1ll11l111ll_opy_, "F", "5", "-1", "hand"),
            b345 + b346 + b4 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "1", "-1", "no"),
            b345 + b346 + b45 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "2", "-1", "no"),
            b345 + b346 + b456 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "3", "-1", "no"),
            b345 + b346 + b5 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "4", "-1", "no"),
            b345 + b346 + b46 + b123 + b3456 + b236: (l1ll11l111ll_opy_, "C", "5", "-1", "no"),
            b16: (l1ll1l1lllll_opy_, "0", None, None, None),
            b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b3456 + b124 + b146: (l1ll1l1lllll_opy_, "6", None, None, None),
            b3456 + b1245 + b146: (l1ll1l1lllll_opy_, "7", None, None, None),
            b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b3456 + b124 + b126: (l1ll1l1lllll_opy_, "-6", None, None, None),
            b3456 + b1245 + b126: (l1ll1l1lllll_opy_, "-7", None, None, None),
            b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b16 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b145 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b15 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b3456 + b124 + b16 + b146: (l1ll1l1lllll_opy_, "1", None, None, None),
            b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b16 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b145 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b15 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b3456 + b124 + b16 + b126: (l1ll1l1lllll_opy_, "-1", None, None, None),
            b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b16 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b3456 + b145 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b3456 + b15 + b16 + b146 + b146: (l1ll1l1lllll_opy_, "2", None, None, None),
            b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b16 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b3456 + b145 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b3456 + b15 + b16 + b126 + b126: (l1ll1l1lllll_opy_, "-2", None, None, None),
            b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b16 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b3456 + b145 + b16 + b146 + b146 + b146: (l1ll1l1lllll_opy_, "3", None, None, None),
            b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b16 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b3456 + b145 + b16 + b126 + b126 + b126: (l1ll1l1lllll_opy_, "-3", None, None, None),
            b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b16 + b16 + b3456 + b145 + b146: (l1ll1l1lllll_opy_, "4", None, None, None),
            b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b16 + b16 + b3456 + b145 + b126: (l1ll1l1lllll_opy_, "-4", None, None, None),
            b16 + b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b16 + b16 + b3456 + b15 + b146: (l1ll1l1lllll_opy_, "5", None, None, None),
            b16 + b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b16 + b16 + b3456 + b15 + b126: (l1ll1l1lllll_opy_, "-5", None, None, None),
            b16 + b3456 + b124 + b146: (l1ll1l1lllll_opy_, "6", None, None, None),
            b16 + b3456 + b124 + b126: (l1ll1l1lllll_opy_, "-6", None, None, None),
            b46 + b14: (l1l1lllll1l1_opy_, "4", "4", "common", None),
            b456 + b14: (l1l1lllll1l1_opy_, "2", "2", "cut", None)
        }
        (l1ll1l1ll111_opy_, sign, line, l1lllll1111_opy_, braille) = l1ll1ll111l1_opy_.get(l1ll1ll11lll_opy_, (
            None, None, None, None, None))
        if l1ll1l1ll111_opy_:
            l1ll1l1ll111_opy_(sign, line, l1lllll1111_opy_, braille)
        if l1ll1ll11lll_opy_[0] == NumeralPrefix:
            l1ll11ll1lll_opy_ = l1ll1ll11ll1_opy_ = ""
            for char in l1ll1ll11lll_opy_[1:]:
                if char in braille_high_numeral_dict:
                    l1ll11ll1lll_opy_ += braille_high_to_numeral(char)
                if char in braille_low_numeral_dict:
                    l1ll1ll11ll1_opy_ += braille_low_to_numeral(char)
            if l1ll1ll11ll1_opy_ != "":
                l1l1lllll1l1_opy_(l1ll11ll1lll_opy_, l1ll1ll11ll1_opy_, "no", "no")
        if b2356 + b3456 in l1ll1ll11lll_opy_:
            if l1ll1ll11lll_opy_[0] == b13456 or l1ll1ll11lll_opy_[0:2] == b13456 + b3:
                l11111l111_opy_ = "whole"
            elif l1ll1ll11lll_opy_[0] == b1345 or l1ll1ll11lll_opy_[0:2] == b1345 + b3:
                l11111l111_opy_ = "half"
            elif l1ll1ll11lll_opy_[0] == b1456 or l1ll1ll11lll_opy_[0:2] == b1456 + b3:
                l11111l111_opy_ = "quarter"
            elif l1ll1ll11lll_opy_[0] == b145 or l1ll1ll11lll_opy_[0:2] == b145 + b3:
                l11111l111_opy_ = "eighth"
            l1ll1lllll11_opy_ = l1ll1ll11lll_opy_.index(b3456)
            l1ll111ll11l_opy_ = l1ll1ll11lll_opy_[l1ll1lllll11_opy_ + 1:]
            l111111ll1_opy_ = ""
            for char in l1ll111ll11l_opy_:
                l111111ll1_opy_ += braille_high_to_numeral(char)
            direction = l11ll11l1l1_opy_()
            l111l1lll1l_opy_ = l11llll11ll_opy_()
            l111l1lll1l_opy_.l11l11ll111_opy_(l11111l111_opy_)
            if l1ll1ll11lll_opy_[1] == b3:
                l111l1lll1l_opy_.l1ll11l111l_opy_(True)
            l111l1lll1l_opy_.l1ll1111l1l_opy_(l111111ll1_opy_)
            direction.l1l11l1llll_opy_(l111l1lll1l_opy_)
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
        if b2356 + b6 + b3456 in l1ll1ll11lll_opy_:
            # print("passé tempo")
            l1ll1111lll1_opy_ = l1ll1ll11lll_opy_.index(b3456)
            l1ll111ll11l_opy_ = l1ll1ll11lll_opy_[l1ll1111lll1_opy_ + 1:]
            l111111ll1_opy_ = ""
            for char in l1ll111ll11l_opy_:
                l111111ll1_opy_ += braille_high_to_numeral(char)
            # direction = l11ll11l1l1_opy_()
            l1l11l1ll1l_opy_ = l1l1l111l11_opy_()
            l1l11l1ll1l_opy_.l1111ll1111_opy_(True)
            l1l11l1ll1l_opy_.l111llll111_opy_(l111111ll1_opy_)
            # direction.l1l11l1llll_opy_(l1l11l1ll1l_opy_)
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1l11l1ll1l_opy_)
        if l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b2345, b25]):
            l1lll1111ll1_opy_("title", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b234, b25]):
            l1lll1111ll1_opy_("subtitle", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b14, b25]):
            l1lll1111ll1_opy_("composer", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b123, b25]):
            l1lll1111ll1_opy_("lyricist", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b1, b25]):
            l1lll1111ll1_opy_("arranger", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b1235, b25]):
            l1lll1111ll1_opy_("rights", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b14, b2456, b25]):
            l1lll1111ll1_opy_("no", l1ll1ll11lll_opy_[6:])
        if l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b2456, b2345, b25]):
            l1ll11lll11l_opy_("title", l1ll1ll11lll_opy_[6:])
        elif l1ll1ll11lll_opy_[0:6] == "".join([b56, b23, b23, b2456, b1345, b25]):
            l1ll11lll11l_opy_("number", l1ll1ll11lll_opy_[6:])
        if l1ll1ll11lll_opy_[0:2] == b345 + b345 and l1ll1ll11lll_opy_[-1] == b3:
            direction = l11ll11l1l1_opy_()
            words = l11ll1l1111_opy_()
            words.l1ll1111111_opy_(self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[2:-1]).strip())
            words.l1l1l1ll11l_opy_(self._1lll111l111_opy_)
            direction.l1l11l1llll_opy_(words)
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
        if l1ll1ll11lll_opy_[0] == b56 and l1ll1ll11lll_opy_[1] == b23 and l1ll1ll11lll_opy_[2] not in [b23, b3]:
            self.note.l1l111l11ll_opy_("single")
            self.note.l1111l11lll_opy_(self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[2:]))
        if l1ll1ll11lll_opy_[0:4] == b56 + b23 + b23 + b13:
            l111l1l11l_opy_ = l111l11llll_opy_()
            l111l1l11l_opy_.l111ll11ll1_opy_(self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[4:]).strip())
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l111l1l11l_opy_)
        if l1ll1ll11lll_opy_ in self._1ll11ll11ll_opy_:
            self.l1ll1ll11l11_opy_(l1ll1ll11lll_opy_)
        if l1ll1ll11lll_opy_[:5] == "".join([b56, b23, b3, b134, b1234]):
            self.l11ll11l11_opy_(l1ll1ll11lll_opy_)
        if l1ll1ll11lll_opy_[:5] == "".join([b56, b23, b3, b134, b14]):
            self.l111ll11ll_opy_(l1ll1ll11lll_opy_)
        if l1ll1ll11lll_opy_[:5] == "".join([b56, b23, b3, b134, b1236]):
            self.l1lllll1lll_opy_(l1ll1ll11lll_opy_)
        if l1ll1ll11lll_opy_[:7] == "".join([b56, b23, b3, b2345, b1235, b145, b24]):
            if self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)]) in self.l1ll111l111l_opy_:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])][
                    0] = l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:])
            else:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])] = [
                    self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:]), "", "", False, ""]
        if l1ll1ll11lll_opy_[:7] == "".join([b56, b23, b3, b2345, b1235, b14, b125]):
            if self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)]) in self.l1ll111l111l_opy_:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])][
                    1] = self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:])
            else:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])] = ["",
                                                                                                                     self.l1ll111lll1l_opy_(
                                                                                                                         l1ll1ll11lll_opy_[
                                                                                                                         l1ll1ll11lll_opy_.index(
                                                                                                                             b25) + 1:]),
                                                                                                                     "",
                                                                                                                     False,
                                                                                                                     ""]
        if l1ll1ll11lll_opy_[:7] == "".join([b56, b23, b3, b2345, b1235, b135, b14]):
            if self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)]) in self.l1ll111l111l_opy_:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])][
                    2] = self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:])
            else:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])] = ["",
                                                                                                                     "",
                                                                                                                     self.l1ll111lll1l_opy_(
                                                                                                                         l1ll1ll11lll_opy_[
                                                                                                                         l1ll1ll11lll_opy_.index(
                                                                                                                             b25) + 1:]),
                                                                                                                     False,
                                                                                                                     ""]
        if l1ll1ll11lll_opy_[:7] == "".join([b56, b23, b3, b2345, b1235, b145, b135]):
            if self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)]) in self.l1ll111l111l_opy_:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])][
                    3] = True
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])][
                    4] = self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[l1ll1ll11lll_opy_.index(b25) + 1:])
            else:
                self.l1ll111l111l_opy_[self.l1ll111lll1l_opy_(l1ll1ll11lll_opy_[8:l1ll1ll11lll_opy_.index(b25)])] = ["",
                                                                                                                     "",
                                                                                                                     "",
                                                                                                                     True,
                                                                                                                     self.l1ll111lll1l_opy_(
                                                                                                                         l1ll1ll11lll_opy_[
                                                                                                                         l1ll1ll11lll_opy_.index(
                                                                                                                             b25) + 1:])]
        if l1ll1ll11lll_opy_ == "".join([b46, b46, b345]):
            self._1ll111111ll_opy_ = False
            l1lll1l1111l_opy_ = 0
            for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if element.t == "part-list":
                    self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                        self._1lll111l111_opy_ - 1].l11l111l1ll_opy_("-1")
                l1lll1l1111l_opy_ += 1
        if l1ll1ll11lll_opy_ == "".join([b456, b456, b345]):
            self._1ll111111ll_opy_ = True
            l1lll1l1111l_opy_ = 0
            for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if element.t == "part-list":
                    self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l111l1l1l1_opy_[
                        self._1lll111l111_opy_ - 1].l11l111l1ll_opy_("1")
                l1lll1l1111l_opy_ += 1

    def l1lll111l1ll_opy_(self, line, l1l11ll11_opy_):
        def l1ll1l1l1lll_opy_():
            if self._1ll1ll1111l_opy_ and not self._1ll11l111l1_opy_:
                for i in \
                        l1l11ll11_opy_.l1lll1l111l_opy_[
                            -(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                            self._1ll1l1l11l1_opy_].l111l11lll_opy_:
                    if i.t == "note":
                        i.l11lll1111l_opy_(
                            l11lll1l11_opy_=int(self._1ll1111l111_opy_) * self._1ll11l1l1l1_opy_ * 4 / int(
                                self._1ll1ll1l111_opy_))
            l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
            l1ll111l1l11_opy_.l11l1lll1ll_opy_("right")
            l1ll111l1l11_opy_.l1111lll11l_opy_("light-light")
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            self._1ll1l1l11l1_opy_ += 1
            self._1ll11111ll1_opy_[self._1lll111l111_opy_ - 1] = [self._1lll111l111_opy_, self._1ll1l1l11l1_opy_]
            l111111l1l_opy_ = l1l1l1l1l1l_opy_()
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l11111_opy_(
                l111111l1l_opy_)
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1ll111l111_opy_(self._1ll1l1l11l1_opy_ + 1)
            l1ll1lllllll_opy_ = l111l111l11_opy_()
            l1ll1lllllll_opy_.l1l1ll1llll_opy_("yes")
            l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll1lllllll_opy_)
            self._1ll11l111l1_opy_ = False
            self._1ll1ll1111l_opy_ = False

        if b126 + b345 in line:
            l1ll1ll11lll_opy_ = line.replace(b126 + b345, l1111l_opy_[b126 + b345])
            line = l1ll1ll11lll_opy_
        while b345 + b345 in line:
            l1ll1lllll1l_opy_ = line.index(b345 + b345)
            try:
                l1ll1111llll_opy_ = line.index(b3)
            except:
                l1ll1111llll_opy_ = len(line)
            words = line[l1ll1lllll1l_opy_ + 2:l1ll1111llll_opy_]
            l1ll1ll11lll_opy_ = line.replace(line[l1ll1lllll1l_opy_:l1ll1111llll_opy_ + 1],
                                             "_words_" + self.l1ll111lll1l_opy_(
                                                 line[l1ll1lllll1l_opy_ + 2:l1ll1111llll_opy_]) + "·")
            line = l1ll1ll11lll_opy_
        for element in l1111l_opy_:
            if element in line:
                l1ll1ll11lll_opy_ = line.replace(element, l1111l_opy_[element])
                line = l1ll1ll11lll_opy_
        l1ll1llll1l1_opy_ = line.split("·")
        self._1ll11l1111l_opy_ = False
        l1lll111111l_opy_ = False  # note of the l1llll1ll1ll_opy_
        l1ll1l11l1ll_opy_ = False  # l1l1llllll1l_opy_ l11lll11ll_opy_ l1lllllllll1_opy_ or l111111111l_opy_
        l1ll1ll11l1l_opy_ = False  # braille l1l11111ll_opy_ sign
        l1ll11l1lll1_opy_ = False  # note or interval braille sign
        l1lll1111111_opy_ = False  # braille l11llll111_opy_ sign
        l1ll11l1l111_opy_ = False  # braille l1ll11l1l111_opy_ sign
        l1ll1111l11l_opy_ = False  # b26 l1ll1l111111_opy_ l1ll11ll111l_opy_ l11lll1l11_opy_
        l1ll1ll111ll_opy_ = False  # b5 + b26 l1ll1l111111_opy_ l1ll11ll111l_opy_ l11lll1l11_opy_
        l1llll1l1l1_opy_ = False
        l1l111l11l_opy_ = False
        l1lll1l1lll_opy_ = False
        l11llllll1_opy_ = False
        l1l111l111_opy_ = False
        l1lll1ll11l_opy_ = False
        l111l11l11_opy_ = False
        l1l11ll1l1_opy_ = False
        l11l1ll111_opy_ = False
        l1lllllll11_opy_ = False
        l1ll1l1111ll_opy_ = False
        l1ll1l1lll11_opy_ = False
        l1ll111lllll_opy_ = []  # list of l11lll11ll_opy_ found in the current l111111l1l_opy_ to be used l1ll11111lll_opy_ the end of the l111111l1l_opy_
        l1l1l1ll1l1_opy_ = 1  # used for braille l1ll111111l1_opy_ or part l111111l1l_opy_ in-l1ll11ll11l1_opy_, l1ll1l111l1l_opy_ to l1l1l1ll1l1_opy_ in l1ll11l1l1ll_opy_ and in the l1llll1ll1ll_opy_
        l1l11l1ll1_opy_ = False
        l1ll111l1l11_opy_ = False
        for content in l1ll1llll1l1_opy_:
            if content == "crescendo":
                direction = l11ll11l1l1_opy_()
                l1111l1l111_opy_ = l11ll1111l1_opy_()
                l1111l1l111_opy_.l1l1llll11l_opy_(True)
                l1111l1l111_opy_.l1l1lll11l1_opy_("crescendo")
                direction.l1l11l1llll_opy_(l1111l1l111_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content == "diminuendo":
                direction = l11ll11l1l1_opy_()
                l1111l1l111_opy_ = l11ll1111l1_opy_()
                l1111l1l111_opy_.l1l1llll11l_opy_(True)
                l1111l1l111_opy_.l1l1lll11l1_opy_("diminuendo")
                direction.l1l11l1llll_opy_(l1111l1l111_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content in ["end_crescendo", "end_diminuendo"]:
                direction = l11ll11l1l1_opy_()
                l1111l1l111_opy_ = l11ll1111l1_opy_()
                l1111l1l111_opy_.l1l1llll11l_opy_(False)
                l1111l1l111_opy_.l1l1lll11l1_opy_("stop")
                direction.l1l11l1llll_opy_(l1111l1l111_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content[:7] == "_words_":
                direction = l11ll11l1l1_opy_()
                words = l11ll1l1111_opy_()
                words.l1ll1111111_opy_(content[7:])
                words.l1l1l1ll11l_opy_(self._1lll111l111_opy_)
                direction.l1l11l1llll_opy_(words)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content == "pedal_start":
                direction = l11ll11l1l1_opy_()
                l111l1lllll_opy_ = l1ll11l1lll_opy_()
                l111l1lllll_opy_.l1l11llll1l_opy_(True)
                l111l1lllll_opy_.l1111l111ll_opy_("start")
                direction.l1l11l1llll_opy_(l111l1lllll_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content == "pedal_stop":
                direction = l11ll11l1l1_opy_()
                l111l1lllll_opy_ = l1ll11l1lll_opy_()
                l111l1lllll_opy_.l1l11llll1l_opy_(True)
                l111l1lllll_opy_.l1111l111ll_opy_("stop")
                direction.l1l11l1llll_opy_(l111l1lllll_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content == "dot":
                self.note.dot = True
                self.note.l11lll1111l_opy_(l11lll1l11_opy_ * 3 / 2)
            if content == "short_appoggiatura":
                l1ll1111l11l_opy_ = True
            if content == "appoggiatura":
                l1ll1ll111ll_opy_ = True
            if content == "staccato":
                l1llll1l1l1_opy_ = True
            if content == "staccatissimo":
                l1l111l11l_opy_ = True
            if content == "accent":
                l1lll1l1lll_opy_ = True
            if content == "trill":
                l11llllll1_opy_ = True
            if content == "inverted_mordent":
                l1l111l111_opy_ = True
            if content == "inverted_mordent_long":
                l1lll1ll11l_opy_ = True
            if content == "mordent":
                l111l11l11_opy_ = True
            if content == "mordent_long":
                l1l11ll1l1_opy_ = True
            if content == "arpeggiate":
                l11l1ll111_opy_ = True
            if content == "two_hands_arpeggiate":
                l1lllllll11_opy_ = True
            if content == "down_arpeggiate":
                l1ll1l1111ll_opy_ = True
            if content == "down_two_hands_arpeggiate":
                l1ll1l1lll11_opy_ = True
            if content in ["triplet", "group3"]:
                l1ll11l1l111_opy_ = True
            if content == "start_phrasing_slur":
                self._1ll1lll1l1l_opy_ = "start"
            if l1lll111111l_opy_ == False and content in l1ll1l_opy_:
                l1lll111111l_opy_ = True
                self.note = l1l111l111l_opy_()
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(self.note)
            if l1ll11l1lll1_opy_ and content in l1ll1l_opy_:
                self.note = l1l111l111l_opy_()
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(self.note)
                self.note.l111lll11l1_opy_(str(self._1ll1lll11l1_opy_))
                l1ll1l11l1ll_opy_ = False
                l1ll1ll11l1l_opy_ = False
                l1ll11l1lll1_opy_ = False
                l1lll1111111_opy_ = False
            if content in l111l_opy_:
                l1ll1l11l1ll_opy_ = True
                l1ll1111ll1l_opy_ = l111l_opy_[content]
                self.note.l1l1111lll1_opy_(l111l_opy_[content])
                self.note.l1llll1l1l11_opy_(content)
            if content in l1ll11l_opy_:
                l1ll1ll11l1l_opy_ = True
                l1ll111l11ll_opy_ = int(l1ll11l_opy_[content])
            if content in l1111ll_opy_:
                if content not in l1l_opy_:
                    self._1ll11l111l1_opy_ = True
                l1ll11l1lll1_opy_ = True
                self.note.l1l11l1ll11_opy_(l1lll_opy_[content])
                self.note.l11ll1l1l1l_opy_(l1111ll_opy_[content])
                l11lll1l11_opy_ = int(l1ll1ll_opy_[l1111ll_opy_[content]] / 256 * self._1ll11l1l1l1_opy_)
                if l11lll1l11_opy_ > int(
                        self._1ll1111l111_opy_) * self._1ll11l1l1l1_opy_ and not self._1ll11l111l1_opy_:
                    l11lll1l11_opy_ = int(self._1ll1111l111_opy_) * self._1ll11l1l1l1_opy_
                if l1ll1111l11l_opy_ or l1ll1ll111ll_opy_:
                    self.note.l1111lll1l_opy_ = True
                    if l1ll1111l11l_opy_:
                        self.note.l11lll1111_opy_ = "yes"
                        l1ll1111l11l_opy_ = False
                    if l1ll1ll111ll_opy_:
                        self.note.l11lll1111_opy_ = "no"
                        l1ll1ll111ll_opy_ = False
                else:
                    if l1ll11l1l111_opy_:
                        self.note.l11lll1111l_opy_(l11lll1l11_opy_ * 2 / 3)
                    else:
                        self.note.l11lll1111l_opy_(l11lll1l11_opy_)
                self.note.l11ll11lll1_opy_(str(l1l1l1ll1l1_opy_))
                if l1ll1l11l1ll_opy_:
                    l1ll111lllll_opy_.append([l1lll_opy_[content], l1ll1111ll1l_opy_])
                else:
                    self.note.l1l1111lll1_opy_(l1lll11_opy_[(l1lll_opy_[content], self._1ll1l111l11_opy_)])
                if len(l1ll111lllll_opy_) > 0:
                    for l1llll11ll1_opy_ in l1ll111lllll_opy_:
                        if l1llll11ll1_opy_[0] == l1lll_opy_[content]:
                            self.note.l1l1111lll1_opy_(l1llll11ll1_opy_[1])
                if self._1ll1l1l1l11_opy_ == "":
                    self._1ll1l1l1l11_opy_ = l1lll_opy_[content]
                if l1ll1ll11l1l_opy_ == False:
                    self._1ll1lll11l1_opy_ += l11111_opy_[(self._1ll1l1l1l11_opy_, l1lll_opy_[content])]
                    self.note.l111lll11l1_opy_(str(self._1ll1lll11l1_opy_))
                else:
                    self._1ll1lll11l1_opy_ = l1ll111l11ll_opy_
                    self.note.l111lll11l1_opy_(str(self._1ll1lll11l1_opy_))
                if l1ll11l1l111_opy_ != 0:
                    self.note.l1l1lllll11_opy_("3")
                    self.note.l11ll1lll11_opy_("2")
                    l1ll11l1l111_opy_ += 1
                    if l1ll11l1l111_opy_ > 3:
                        l1ll11l1l111_opy_ = 0
                if l1llll1l1l1_opy_:
                    self.note.l11lll1l1l1_opy_(True)
                    l1llll1l1l1_opy_ = False
                if l1l111l11l_opy_:
                    self.note.l11l1ll1l11_opy_(True)
                    l1l111l11l_opy_ = False
                if l1lll1l1lll_opy_:
                    self.note.l1l111l1l11_opy_(True)
                    l1lll1l1lll_opy_ = False
                if l11llllll1_opy_:
                    self.note.l11ll11l111_opy_(True)
                    l11llllll1_opy_ = False
                if l1l111l111_opy_:
                    self.note.l111l11ll1l_opy_(True)
                    self.note.l1l11111ll1_opy_("above")
                    self.note.l111ll111ll_opy_("no")
                    l1l111l111_opy_ = False
                if l1lll1ll11l_opy_:
                    self.note.l111l11ll1l_opy_(True)
                    self.note.l1l11111ll1_opy_("above")
                    self.note.l111ll111ll_opy_("yes")
                    l1lll1ll11l_opy_ = False
                if l111l11l11_opy_:
                    self.note.l111l11111l_opy_(True)
                    self.note.l111l1lll11_opy_("above")
                    self.note.l1l1lll1ll1_opy_("no")
                    l111l11l11_opy_ = False
                if l1l11ll1l1_opy_:
                    self.note.l111l11111l_opy_(True)
                    self.note.l111l1lll11_opy_("above")
                    self.note.l1l1lll1ll1_opy_("yes")
                    l1l11ll1l1_opy_ = False
                if l11l1ll111_opy_:
                    self.note.l11l1l11ll1_opy_(True)
                    l11l1ll111_opy_ = False
                if l1lllllll11_opy_:
                    self.note.l1l11ll111l_opy_(True)
                    l1lllllll11_opy_ = False
                if l1ll1l1111ll_opy_:
                    self.note.l11l1l11ll1_opy_(True)
                    self.note.l1l1l111111_opy_("down")
                    l1ll1l1111ll_opy_ = False
                if l1ll1l1lll11_opy_:
                    self.note.l1l11ll111l_opy_(True)
                    self.note.l1l1l1l11ll_opy_("down")
                    l1ll1l1lll11_opy_ = False
                if self._1ll1lll1l1l_opy_ == "continue":
                    if self._1ll1ll1ll1l_opy_[2] == "1":
                        self.note.l1llllll1ll_opy_ = True
                        self.note.l11l1111ll_opy_ = "above"
                        self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[2])
                        self.note.l1111l1l11_opy_ = "continue"
                    elif self._1ll1ll1ll1l_opy_[2] == "2":
                        self.note.l111ll11l1_opy_ = True
                        self.note.l1llll1lll1_opy_ = "above"
                        self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[2]
                        self.note.l11l111l11_opy_ = "continue"
                if self._1ll1lll1l1l_opy_ == "start":
                    self._1ll1lll1l1l_opy_ = "continue"
                    if "1" not in self._1ll1ll1ll1l_opy_:
                        self._1ll1ll1ll1l_opy_[2] = "1"
                        self.note.l1llllll1ll_opy_ = True
                        self.note.l11l1111ll_opy_ = "above"
                        self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[2])
                        self.note.l1111l1l11_opy_ = "start"
                    elif "2" not in self._1ll1ll1ll1l_opy_:
                        self._1ll1ll1ll1l_opy_[2] = "2"
                        self.note.l111ll11l1_opy_ = True
                        self.note.l1llll1lll1_opy_ = "above"
                        self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[2]
                        self.note.l11l111l11_opy_ = "start"
                if content not in l1l_opy_:
                    self._1ll1l1l1l11_opy_ = l1lll_opy_[content]
                self._1ll11l1llll_opy_ = l1111ll_opy_[content]
            if content in l1l_opy_:
                if content == "rest123":
                    self._1ll1ll1111l_opy_ = True
                l1ll11l1lll1_opy_ = True
                self.note.rest = True
                self.note.l11ll1l1l1l_opy_(l1111ll_opy_[content])
                l11lll1l11_opy_ = l1ll1ll_opy_[l1111ll_opy_[content]] / 256 * self._1ll11l1l1l1_opy_
                if l11lll1l11_opy_ > int(self._1ll1111l111_opy_) * 4 * self._1ll11l1l1l1_opy_ / int(
                        self._1ll1ll1l111_opy_):
                    l11lll1l11_opy_ = int(self._1ll1111l111_opy_) * self._1ll11l1l1l1_opy_ * 4 / int(
                        self._1ll1ll1l111_opy_)
                self.note.l11lll1111l_opy_(l11lll1l11_opy_)
                self.note.l11ll11lll1_opy_(str(l1l1l1ll1l1_opy_))
                self.note.l111lll11l1_opy_("100")
                if l1ll11l1l111_opy_ != 0:
                    self.note.l1l1lllll11_opy_("3")
                    self.note.l11ll1lll11_opy_("2")
                    l1ll11l1l111_opy_ += 1
                    if l1ll11l1l111_opy_ > 3:
                        l1ll11l1l111_opy_ = 0
                if self._1ll1lll1l1l_opy_ == "continue":
                    if self._1ll1ll1ll1l_opy_[2] == "1":
                        self.note.l1llllll1ll_opy_ = True
                        self.note.l11l1111ll_opy_ = "above"
                        self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[2])
                        self.note.l1111l1l11_opy_ = "continue"
                    elif self._1ll1ll1ll1l_opy_[2] == "2":
                        self.note.l111ll11l1_opy_ = True
                        self.note.l1llll1lll1_opy_ = "above"
                        self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[2]
                        self.note.l11l111l11_opy_ = "continue"
                if self._1ll1lll1l1l_opy_ == "start":
                    self._1ll1lll1l1l_opy_ = "continue"
                    if "1" not in self._1ll1ll1ll1l_opy_:
                        self._1ll1ll1ll1l_opy_[2] = "1"
                        self.note.l1llllll1ll_opy_ = True
                        self.note.l11l1111ll_opy_ = "above"
                        self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[2])
                        self.note.l1111l1l11_opy_ = "start"
                    elif "2" not in self._1ll1ll1ll1l_opy_:
                        self._1ll1ll1ll1l_opy_[2] = "2"
                        self.note.l111ll11l1_opy_ = True
                        self.note.l1llll1lll1_opy_ = "above"
                        self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[2]
                        self.note.l11l111l11_opy_ = "start"
                self._1ll11l1llll_opy_ = l1111ll_opy_[content]
            if content in l111l1_opy_:
                l1ll11l1lll1_opy_ = True
                self.note.l1l11l1ll11_opy_(l11ll_opy_[(self._1ll1l1l1l11_opy_, content, self._1ll111111ll_opy_)][0])
                self.note.l11ll1l1l1l_opy_(self._1ll11l1llll_opy_)
                self.note.l11lll1111l_opy_(l1ll1ll_opy_[self._1ll11l1llll_opy_] / 256 * self._1ll11l1l1l1_opy_)
                self.note.l1lll1l11l1_opy_ = True
                self.note.l11ll11lll1_opy_(str(l1l1l1ll1l1_opy_))
                if l1ll1ll11l1l_opy_ == False:
                    l1ll11lll1l1_opy_ = self._1ll1lll11l1_opy_ + \
                                        l11ll_opy_[(self._1ll1l1l1l11_opy_, content, self._1ll111111ll_opy_)][1]
                    self.note.l111lll11l1_opy_(str(l1ll11lll1l1_opy_))
                else:
                    self.note.l111lll11l1_opy_(l1ll111l11ll_opy_)
                if l1ll1l11l1ll_opy_:
                    l1ll111lllll_opy_.append(
                        [l11ll_opy_[(self._1ll1l1l1l11_opy_, content, self._1ll111111ll_opy_)][0], l1ll1111ll1l_opy_])
                else:
                    self.note.l1l1111lll1_opy_(l1lll11_opy_[(
                        l11ll_opy_[(self._1ll1l1l1l11_opy_, content, self._1ll111111ll_opy_)][0],
                        self._1ll1l111l11_opy_)])
                if l1ll11l1l111_opy_ != 0:
                    self.note.l1l1lllll11_opy_("3")
                    self.note.l11ll1lll11_opy_("2")
            if content in l1l11ll_opy_:
                l1lll1111111_opy_ = True
                if self.note:
                    self.note.l11llll111_opy_ = l1l11ll_opy_[content]
                else:
                    return
            if l1lll111111l_opy_ and self._1ll1l111lll_opy_:
                self._1ll1l111lll_opy_ = False
                if self._1ll1ll1ll1l_opy_[0] == "1":
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[0])
                    self.note.l1111l1l11_opy_ = "stop"
                elif self._1ll1ll1ll1l_opy_[0] == "2":
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[0]
                    self.note.l11l111l11_opy_ = "stop"
                self._1ll1ll1ll1l_opy_[0] = "0"
            if content == "slur12" and self._1ll1l1l1111_opy_ != "continue":
                self._1ll1l111lll_opy_ = True
                if "1" not in self._1ll1ll1ll1l_opy_:
                    self._1ll1ll1ll1l_opy_[0] = "1"
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[0])
                    self.note.l1111l1l11_opy_ = "start"
                elif "2" not in self._1ll1ll1ll1l_opy_:
                    self._1ll1ll1ll1l_opy_[0] = "2"
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[0]
                    self.note.l11l111l11_opy_ = "start"
            if l1lll111111l_opy_ and self._1ll1l1l1111_opy_ == "stop":
                self._1ll1l1l1111_opy_ = "no"
                if self._1ll1ll1ll1l_opy_[1] == "1":
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[1])
                    self.note.l1111l1l11_opy_ = "stop"
                elif self._1ll1ll1ll1l_opy_[1] == "2":
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[1]
                    self.note.l11l111l11_opy_ = "stop"
                self._1ll1ll1ll1l_opy_[1] = "0"
            if content == "slur12" and self._1ll1l1l1111_opy_ == "continue":
                self._1ll1l1l1111_opy_ = "stop"
                if self._1ll1ll1ll1l_opy_[1] == "1":
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[1])
                    self.note.l1111l1l11_opy_ = "continue"
                elif self._1ll1ll1ll1l_opy_[1] == "2":
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[1]
                    self.note.l11l111l11_opy_ = "continue"
            if l1lll111111l_opy_ and self._1ll1l1l1111_opy_ == "continue":
                if self._1ll1ll1ll1l_opy_[1] == "1":
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[1])
                    self.note.l1111l1l11_opy_ = "continue"
                elif self._1ll1ll1ll1l_opy_[1] == "2":
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[1]
                    self.note.l11l111l11_opy_ = "continue"
            if content == "phrasing_slur":
                self._1ll1l1l1111_opy_ = "continue"
                if "1" not in self._1ll1ll1ll1l_opy_:
                    self._1ll1ll1ll1l_opy_[1] = "1"
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[1])
                    self.note.l1111l1l11_opy_ = "start"
                elif "2" not in self._1ll1ll1ll1l_opy_:
                    self._1ll1ll1ll1l_opy_[1] = "2"
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[1]
                    self.note.l11l111l11_opy_ = "start"
            if content == "end_phrasing_slur":
                self._1ll1lll1l1l_opy_ = "no"
                if self._1ll1ll1ll1l_opy_[2] == "1":
                    self.note.l1llllll1ll_opy_ = True
                    self.note.l11l1111ll_opy_ = "above"
                    self.note.l11l1l111l1_opy_(self._1ll1ll1ll1l_opy_[2])
                    self.note.l1111l1l11_opy_ = "stop"
                if self._1ll1ll1ll1l_opy_[2] == "2":
                    self.note.l111ll11l1_opy_ = True
                    self.note.l1llll1lll1_opy_ = "above"
                    self.note.l11l11l1ll_opy_ = self._1ll1ll1ll1l_opy_[2]
                    self.note.l11l111l11_opy_ = "stop"
                self._1ll1ll1ll1l_opy_[2] = "0"
            if l1lll111111l_opy_ and [self.note.step, self.note.l11lll11ll_opy_,
                                      self.note.l1l11111ll_opy_] in self.l1lll111l11l_opy_:
                self._1ll11l11l1l_opy_ = False
                self.note.l1l11lll1l1_opy_(True)
                self.note.l11llllll1l_opy_("stop")
                # if [self.note.step, self.note.l11lll11ll_opy_, self.note.l1l11111ll_opy_] in self.l1lll111l11l_opy_:
                self.l1lll111l11l_opy_.remove([self.note.step, self.note.l11lll11ll_opy_, self.note.l1l11111ll_opy_])
            if content == "single_note_tie":
                self._1ll11l11l1l_opy_ = True
                self.note.l1l11lll1l1_opy_(True)
                self.note.l11llllll1l_opy_("start")
                if [self.note.step, self.note.l11lll11ll_opy_, self.note.l1l11111ll_opy_] not in self.l1lll111l11l_opy_:
                    self.l1lll111l11l_opy_.append(
                        [self.note.step, self.note.l11lll11ll_opy_, self.note.l1l11111ll_opy_])
                else:
                    self.note.l11llllll1l_opy_("stop-start")
            if content == "breath_mark":
                self.note.l1ll11l1ll1l_opy_(True)
            if content == "fermata":
                self.note.l11l1l1111l_opy_(True)
            if content == "full_measure_in_accord":
                l1l1l1ll1l1_opy_ += 1
                l1ll1111ll11_opy_ = l111ll1ll1l_opy_()
                l1ll1111ll11_opy_.l1lll1lllll1_opy_(True)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll1111ll11_opy_)
            if content == "part_measure_in_accord":
                l1l1l1ll1l1_opy_ += 1
                l1ll1111ll11_opy_ = l111ll1ll1l_opy_()
                l1ll1111ll11_opy_.l1lll1lllll1_opy_(False)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll1111ll11_opy_)
            if content == "measure_division":
                l1l1l1ll1l1_opy_ = 1
            if content in l11l111_opy_:
                direction = l11ll11l1l1_opy_()
                l1l11l1ll1_opy_ = l11l1llll1l_opy_()
                l1l11l1ll1_opy_.l11ll1111ll_opy_(content)
                direction.l1l11l1llll_opy_(l1l11l1ll1_opy_)
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(direction)
            if content == "end_composition_double_bar":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("right")
                l1ll111l1l11_opy_.l1111lll11l_opy_("light-heavy")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "end_measure_double_bar":
                l1ll1l1l1lll_opy_()
            if content == "begin_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("left")
                l1ll111l1l11_opy_.l1111lll11l_opy_("heavy-light")
                l1ll111l1l11_opy_.l1l1l1llll1_opy_("forward")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "end_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("right")
                l1ll111l1l11_opy_.l1111lll11l_opy_("light-heavy")
                l1ll111l1l11_opy_.l1l1l1llll1_opy_("backward")
                if self.l1llll1111l1_opy_ != "no":
                    l1ll111l1l11_opy_.l1l11l1l1l1_opy_(True)
                    l1ll111l1l11_opy_.l11111lllll_opy_(self.l1llll1111l1_opy_)
                    l1ll111l1l11_opy_.l11ll1llll1_opy_("stop")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "first_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("left")
                l1ll111l1l11_opy_.l1l11l1l1l1_opy_(True)
                l1ll111l1l11_opy_.l11111lllll_opy_("1")
                self.l1llll1111l1_opy_ = "1"
                l1ll111l1l11_opy_.l11ll1llll1_opy_("start")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "second_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("left")
                l1ll111l1l11_opy_.l1l11l1l1l1_opy_(True)
                l1ll111l1l11_opy_.l11111lllll_opy_("2")
                self.l1llll1111l1_opy_ = "2"
                l1ll111l1l11_opy_.l11ll1llll1_opy_("start")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "third_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("left")
                l1ll111l1l11_opy_.l1l11l1l1l1_opy_(True)
                l1ll111l1l11_opy_.l11111lllll_opy_("3")
                self.l1llll1111l1_opy_ = "3"
                l1ll111l1l11_opy_.l11ll1llll1_opy_("start")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content == "fourth_repeat":
                l1ll111l1l11_opy_ = l1l1l1l111l_opy_()
                l1ll111l1l11_opy_.l11l1lll1ll_opy_("left")
                l1ll111l1l11_opy_.l1l11l1l1l1_opy_(True)
                l1ll111l1l11_opy_.l11111lllll_opy_("4")
                self.l1llll1111l1_opy_ = "4"
                l1ll111l1l11_opy_.l11ll1llll1_opy_("start")
                l1l11ll11_opy_.l1lll1l111l_opy_[-(1 + self._1ll11lll111_opy_ - self._1lll111l111_opy_)].l11l1l1ll1_opy_[
                    self._1ll1l1l11l1_opy_].l1l11l1llll_opy_(l1ll111l1l11_opy_)
            if content not in l1ll11l_opy_ and content not in l1111ll_opy_ and content not in l111l_opy_ and content not in l111l1_opy_ and content not in l1l11ll_opy_ and content != "dot":
                l1lll111111l_opy_ = False
                l1ll1l11l1ll_opy_ = False
                l1ll1ll11l1l_opy_ = False
                l1ll11l1lll1_opy_ = False
                l1lll1111111_opy_ = False
