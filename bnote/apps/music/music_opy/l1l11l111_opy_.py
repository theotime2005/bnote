"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l1l111ll1_opy_ import *
class l11lll1l1_opy_:
    def __init__(self, l11llll11l_opy_, l1l11ll11_opy_):
        self._1l1l11ll_opy_ = l1l11ll11_opy_
        self._1l1111ll_opy_ = l11llll11l_opy_
    def l1l1111l1_opy_ (self):
        """
         this function treats chords and assigns the chord_state parameter for braille statement
         0 automatically for notes without chord
         1 for the first note of a chord
         2 for intermediate notes of a chord
         3 for the last note of a chord
        """
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part":
                for l111111l1l_opy_ in element.l11l1l1ll1_opy_:
                    for index,event in enumerate (l111111l1l_opy_.l111l11lll_opy_):
                        if event.t == "note" and event.l1lll1l11l1_opy_:
                            if not l111111l1l_opy_.l111l11lll_opy_[index-1].l1lll1l11l1_opy_:
                                l111111l1l_opy_.l111l11lll_opy_[index-1].l1ll1llll11_opy_ = 1
                            else:
                                l111111l1l_opy_.l111l11lll_opy_[index-1].l1ll1llll11_opy_ = 2
                            event.l1ll1llll11_opy_ = 3
                            event.l11lll1l11_opy_ = l111111l1l_opy_.l111l11lll_opy_[index-1].l11lll1l11_opy_
                            if l111111l1l_opy_.l111l11lll_opy_[index-1].l11l1ll111_opy_:
                                l111111l1l_opy_.l111l11lll_opy_[index].l11l1l11ll1_opy_ (True)
                            if l111111l1l_opy_.l111l11lll_opy_[index-1].l1lllll11l1_opy_ == "down":
                                l111111l1l_opy_.l111l11lll_opy_[index].l1l1l111111_opy_ ("down")
                            if l111111l1l_opy_.l111l11lll_opy_[index-1].l1lllllll11_opy_:
                                l111111l1l_opy_.l111l11lll_opy_[index].l1l11ll111l_opy_ (True)
                            if l111111l1l_opy_.l111l11lll_opy_[index-1].l111l1lll1_opy_ == "down":
                                l111111l1l_opy_.l111l11lll_opy_[index].l1l1l1l11ll_opy_ ("down")
        self._1l1111ll_opy_ ("\nOptimize model score2, chord assign\n")
        self._1l1111ll_opy_ (str(self._1l1l11ll_opy_))
    def l11lll111_opy_ (self):
        def l1lll11llll1_opy_ (l1lll11lll11_opy_):
            l1lll11l1l11_opy_ = 0
            for item in self._1l1l11ll_opy_.l1lll1l111l_opy_:
                if item.t == "part-list":
                    for l1lll11l11l1_opy_ in item.l111l1l1l1_opy_:
                        if l1lll11l1l11_opy_ == l1lll11lll11_opy_:
                            element.l1l11l11l11_opy_ (l1lll11l11l1_opy_.l111l1l1ll_opy_)
                            element.l11lll1lll1_opy_ (l1lll11l11l1_opy_.l111lll1ll_opy_)
                            element.l11lll1ll1l_opy_ (l1lll11l11l1_opy_.l11111ll1l_opy_)
                        l1lll11l1l11_opy_ += 1
        l111l1111l_opy_ = 0
        l1l1l11111_opy_ = "0"
        l1lll1l1l1ll_opy_ = 0
        l1lll11ll111_opy_ = 1
        l1lll11l1ll1_opy_ = 0
        l1lll11lll11_opy_ = 0
        for l1lll1l1111l_opy_,element in enumerate(self._1l1l11ll_opy_.l1lll1l111l_opy_):
            if element.t == "part":
                l1lll11llll1_opy_(l1lll11lll11_opy_)
                for l1lll11lll1l_opy_,l111111l1l_opy_ in enumerate(element.l11l1l1ll1_opy_):
                    l1llll111ll1_opy_ = 0
                    l1llll11ll1l_opy_ = 0
                    l1llll11lll1_opy_ = False
                    l1lll11l11ll_opy_ = False
                    l1lll11lllll_opy_ = False
                    l1lll111lll1_opy_ = False
                    for l1lll11l1111_opy_,event in enumerate (l111111l1l_opy_.l111l11lll_opy_):
                        if event.t == "backup":
                            if l1llll11lll1_opy_ and (l1lll11l11ll_opy_ == l1lll111llll_opy_ and l1lll11lllll_opy_ == l1lll11ll11l_opy_ and l1lll111lll1_opy_ == l1lll11l111l_opy_):
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll1l11111_opy_].l1llll11l111_opy_ (True)
                                if l1lll11l11ll_opy_:
                                    l1lll11ll111_opy_ = 1
                                elif l1lll11lllll_opy_:
                                    l1lll11ll111_opy_ = 2
                                elif l1lll111lll1_opy_:
                                    l1lll11ll111_opy_ = 3
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll1l11111_opy_].l1l1l1ll11l_opy_ (l1lll11ll111_opy_)
                            l1lll1l11111_opy_ = l1lll11l1111_opy_
                            l1lll111llll_opy_ = l1lll11l11ll_opy_
                            l1lll11ll11l_opy_ = l1lll11lllll_opy_
                            l1lll11l111l_opy_ = l1lll111lll1_opy_
                            l1lll11l11ll_opy_ = False
                            l1lll11lllll_opy_ = False
                            l1lll111lll1_opy_ = False
                            l1llll11ll1l_opy_ -= event.l11lll1l11_opy_
                            l1llll111ll1_opy_ = l1llll11ll1l_opy_
                            if event.l11lll1l11_opy_ == l1lll1l1l1ll_opy_:
                                event.l1llll1l1ll1_opy_ = True
                            l1llll11lll1_opy_ = True
                            self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l1lll1l1ll11_opy_ (True)
                            if event.l11lll1l11_opy_ == 0 and event.l1llll1l1ll1_opy_:
                                event.l11lll1l11_opy_ = l1lll1l1l1ll_opy_
                        if event.t == "attributes":
                            for l11lllll11_opy_ in event.l11l111ll1_opy_:
                                if l11lllll11_opy_.t == "divisions":
                                    l111l1111l_opy_ = l11lllll11_opy_.l111l1111l_opy_
                                if l11lllll11_opy_.t == "time":
                                    l1l1l11111_opy_ = l11lllll11_opy_.l1l1l11111_opy_
                                    l1111lll11_opy_ = l11lllll11_opy_.l1111lll11_opy_
                                    l1lll1l1l1ll_opy_ = int(l111l1111l_opy_ * int(l1l1l11111_opy_) / (int(l1111lll11_opy_) / 4))
                        l111111l1l_opy_.l1llll11l1l1_opy_ (l1lll1l1l1ll_opy_)
                        if event.t == "note":
                            if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1llllll11ll_opy_ and l1lll11l1ll1_opy_ == 100:
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1l1l_opy_-3].l1lll1l11ll1_opy_ = 0
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1l1l_opy_-2].l1lll1l11ll1_opy_ = 0
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1l1l_opy_-1].l1lll1l11ll1_opy_ = 0
                                self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1l1l_opy_].l1lll1l11ll1_opy_ = 0
                                l1lll11l1ll1_opy_ = 0
                            if event.l11111ll11_opy_ == 1:
                                l1lll11l11ll_opy_ = True
                            elif event.l11111ll11_opy_ == 2:
                                l1lll11lllll_opy_ = True
                            elif event.l11111ll11_opy_ == 3:
                                l1lll111lll1_opy_ = True
                            event.l1llll111ll1_opy_ = l1llll111ll1_opy_
                            l1llll11ll1l_opy_ = l1llll111ll1_opy_ + event.l11lll1l11_opy_
                            event.l1llll11ll1l_opy_ = l1llll11ll1l_opy_
                            try:
                                if l1111lll11_opy_ == "4":
                                    event.l1llll11l1ll_opy_ = l1llll111ll1_opy_ // l111l1111l_opy_ +1
                                    event.l1lll1lll111_opy_ = (l1llll111ll1_opy_ % l111l1111l_opy_) / l111l1111l_opy_
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1llllll111l_opy_ and event.l1lll1lll111_opy_ == 0.0:
                                        event.l1lll1l11ll1_opy_ = 1
                                        l1lll11l1ll1_opy_ = 1
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1llllll111l_opy_ and event.l1lll1lll111_opy_ in [0.25,0.5,0.75]:
                                        event.l1lll1l11ll1_opy_ = 2
                                        l1lll11l1ll1_opy_ += 1
                                    if l1lll11l1ll1_opy_ == 4:
                                        l1lll11l1l1l_opy_ = l1lll11l1111_opy_ # for groups l1lll11l1lll_opy_ by l11l11111_opy_ l1llllll11ll_opy_
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-3].l1lll1l11ll1_opy_ = 3
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-2].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-1].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_].l1lll1l11ll1_opy_ = 4
                                        l1lll11l1ll1_opy_ = 100
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1lllll1llll_opy_ and event.l1lll1lll111_opy_ in [0/8,4/8]:
                                        event.l1lll1l11ll1_opy_ = 1
                                        l1lll11l1ll1_opy_ = 1
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1lllll1llll_opy_ and event.l1lll1lll111_opy_ in [1/8,2/8,3/8,5/8,6/8,7/8]:
                                        event.l1lll1l11ll1_opy_ = 2
                                        l1lll11l1ll1_opy_ += 1
                                    if l1lll11l1ll1_opy_ == 4:
                                        l1lll11l1l1l_opy_ = l1lll11l1111_opy_ # for groups l1lll11l1lll_opy_ by l11l11111_opy_ l1llllll11ll_opy_
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-3].l1lll1l11ll1_opy_ = 3
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-2].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_-1].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll11l1111_opy_].l1lll1l11ll1_opy_ = 4
                                        l1lll11l1ll1_opy_ = 100
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1llllll1111_opy_ and event.l1lll1lll111_opy_ in [0/16,4/16,8/16,12/16]:
                                        event.l1lll1l11ll1_opy_ = 1
                                        l1lll11l1ll1_opy_ = 1
                                    if event.type == l1l111l111l_opy_.l1lllll1ll11_opy_.l1llllll1111_opy_ and event.l1lll1lll111_opy_ in [1/16,2/16,3/16,5/16,6/16,7/16,9/16,10/16,11/16,13/16,14/16,15/16]:
                                        event.l1lll1l11ll1_opy_ = 2
                                        l1lll11l1ll1_opy_ += 1
                                    if l1lll11l1ll1_opy_ == 4:
                                        l1lll11l1l1l_opy_ = l1lll11l1111_opy_
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[
                                            l1lll11l1111_opy_ - 3].l1lll1l11ll1_opy_ = 3
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[
                                            l1lll11l1111_opy_ - 2].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[
                                            l1lll11l1111_opy_ - 1].l1lll1l11ll1_opy_ = 4
                                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[
                                            l1lll11l1111_opy_].l1lll1l11ll1_opy_ = 4
                                        l1lll11l1ll1_opy_ = 100
                            except:
                                pass
                            if event.l1ll1llll11_opy_ in [0,3]:
                                l1llll111ll1_opy_ += event.l11lll1l11_opy_
                        else: # in l1lll11ll1ll_opy_ of other item than a note
                            l1lll11l1ll1_opy_ = 0
                    if l1llll11lll1_opy_ and (l1lll11l11ll_opy_ == l1lll111llll_opy_ and l1lll11lllll_opy_ == l1lll11ll11l_opy_ and l1lll111lll1_opy_ == l1lll11l111l_opy_):
                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll1l11111_opy_].l1llll11l111_opy_ (True)
                        if l1lll11l11ll_opy_:
                            l1lll11ll111_opy_ = 1
                        elif l1lll11lllll_opy_:
                            l1lll11ll111_opy_ = 2
                        elif l1lll111lll1_opy_:
                            l1lll11ll111_opy_ = 3
                        self._1l1l11ll_opy_.l1lll1l111l_opy_[l1lll1l1111l_opy_].l11l1l1ll1_opy_[l1lll11lll1l_opy_].l111l11lll_opy_[l1lll1l11111_opy_].l1l1l1ll11l_opy_ (l1lll11ll111_opy_)
                    l1lll11l1ll1_opy_ = 0 # for l1lll11ll1l1_opy_ end of l111111l1l_opy_
                l1lll11lll11_opy_ += 1
        self._1l1111ll_opy_ ("\nOptimize model score2, with measure position\n")
        self._1l1111ll_opy_ (str(self._1l1l11ll_opy_))