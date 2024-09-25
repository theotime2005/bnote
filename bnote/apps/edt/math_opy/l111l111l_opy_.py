"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import sys

# l11l_opy_ the logger for this file
from .colored_log import ColoredLogger, MATH_LOG

log = ColoredLogger(__name__, level=MATH_LOG)


class l1lll11ll_opy_:
    def __init__(self, text="", l1l1111l1_opy_=None, index=None):
        self.text = text
        if index and l1l1111l1_opy_:
            raise
        if index:
            self.l1l1111l1_opy_ = [index for i in range(0, len(text))]
        elif l1l1111l1_opy_:
            self.l1l1111l1_opy_ = l1l1111l1_opy_
        else:
            self.l1l1111l1_opy_ = [i for i in range(0, len(text))]

    def __str__(self):
        return "text:<{}>,indexed:{}".format(self.text, self.l1l1111l1_opy_)

    def __getitem__(self, i):
        if isinstance(i, int):
            return l1lll11ll_opy_(self.text[i], [self.l1l1111l1_opy_[i]])
        if isinstance(i, slice):
            return l1lll11ll_opy_(self.text[i.start: i.stop], self.l1l1111l1_opy_[i.start: i.stop])
        elif len(i) == 2:
            return l1lll11ll_opy_(self.text[i[0]: i[1]], self.l1l1111l1_opy_[i[0]: i[1]])
        else:
            raise ValueError("__getitem__ !merdum!")

    def __add__(self, other):
        l1llll111ll_opy_ = self.text + other.text
        l1llll1l1l1_opy_ = self.l1l1111l1_opy_ + other.l1l1111l1_opy_
        return l1lll11ll_opy_(l1llll111ll_opy_, l1llll1l1l1_opy_)

    def __len__(self):
        return len(self.text)

    def l1ll1ll11_opy_(self):
        return self.text

    def l1l1111_opy_(self):
        return self.l1l1111l1_opy_

    def find(self, l1llll11l1l_opy_, start=0, end=sys.maxsize):
        return self.text.find(l1llll11l1l_opy_, start, end)

    def rfind(self, l1llll11l1l_opy_, start=0, end=sys.maxsize):
        return self.text.rfind(l1llll11l1l_opy_, start, end)

    def replace(self, l1llll11lll_opy_, l1llll11111_opy_):
        l1111ll1_opy_ = self.text
        l1llll1l111_opy_ = self.l1l1111l1_opy_
        pos = l1111ll1_opy_.find(l1llll11lll_opy_)
        while pos != -1:
            l1llll11l11_opy_ = [l1llll1l111_opy_[pos] for i in range(0, len(l1llll11111_opy_))]
            l1llll1l111_opy_ = l1llll1l111_opy_[0: pos] + l1llll11l11_opy_ \
                               + l1llll1l111_opy_[pos + len(l1llll11lll_opy_): len(l1111ll1_opy_)]
            l1111ll1_opy_ = l1111ll1_opy_[0: pos] + l1llll11111_opy_ + l1111ll1_opy_[
                                                                       pos + len(l1llll11lll_opy_): len(l1111ll1_opy_)]
            pos = l1111ll1_opy_.find(l1llll11lll_opy_)
        return l1lll11ll_opy_(l1111ll1_opy_, l1l1111l1_opy_=l1llll1l111_opy_)

    def split(self, seq) -> []:
        l1llll1111l_opy_ = list()
        start = 0
        while True:
            end = self.find(seq, start)
            if end == -1:
                break
            else:
                l1llll1111l_opy_.append(self[start: end])
                start = end + len(seq)
        l1llll1111l_opy_.append(self[start: len(self)])
        return l1llll1111l_opy_

    def join(self, l1llll11ll1_opy_):
        """
        The join() method takes all IndexedText in an iterable and joins them into one IndexedText.
        An IndexedText must be specified as the separator.
        (likes "join" for strings)
        """
        l1111ll1_opy_ = l1lll11ll_opy_()
        for index, text in enumerate(l1llll11ll1_opy_):
            if index != 0:
                l1111ll1_opy_ += self
            l1111ll1_opy_ += text
        return l1111ll1_opy_

    def l11l11l1l_opy_(self, l1llll1l11l_opy_):
        """
        Return the position of less or equal index present in the IndexedString
        """
        l1llll111l1_opy_ = -1
        for pos, index in enumerate(self.l1l1111l1_opy_):
            if index == l1llll1l11l_opy_:
                return pos
            elif index > l1llll1l11l_opy_:
                return l1llll111l1_opy_
            else:
                l1llll111l1_opy_ = pos
        return l1llll111l1_opy_
