"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l1l1ll11l_opy_ import *
class l1l1l1lll_opy_:
    def __init__(self, l11ll1ll11_opy_, l1ll1l1ll_opy_):
        self._1lll111l_opy_ = l1ll1l1ll_opy_
        self._1l11l11l_opy_ = l11ll1ll11_opy_
    def l1l1l1111_opy_ (self):
        """
         this function treats chords and assigns the chord_state parameter for braille statement
         0 automatically for notes without chord
         1 for the first note of a chord
         2 for intermediate notes of a chord
         3 for the last note of a chord
        """
        for element in self._1lll111l_opy_.l1l111llll_opy_:
            if element.t == "part":
                for l1lllll11ll_opy_ in element.l1lllllll11_opy_:
                    for index,event in enumerate (l1lllll11ll_opy_.l111111lll_opy_):
                        if event.t == "note" and event.l1lllllllll_opy_:
                            if not l1lllll11ll_opy_.l111111lll_opy_[index-1].l1lllllllll_opy_:
                                l1lllll11ll_opy_.l111111lll_opy_[index-1].l1lll11l11l_opy_ = 1
                            else:
                                l1lllll11ll_opy_.l111111lll_opy_[index-1].l1lll11l11l_opy_ = 2
                            event.l1lll11l11l_opy_ = 3
                            event.l1lll1ll1ll_opy_ = l1lllll11ll_opy_.l111111lll_opy_[index-1].l1lll1ll1ll_opy_
                            if l1lllll11ll_opy_.l111111lll_opy_[index-1].l1l1111l1l_opy_:
                                l1lllll11ll_opy_.l111111lll_opy_[index].l1l1lll1lll_opy_ (True)
                            if l1lllll11ll_opy_.l111111lll_opy_[index-1].l111lllll1_opy_ == "down":
                                l1lllll11ll_opy_.l111111lll_opy_[index].l1l1l1l11l1_opy_ ("down")
                            if l1lllll11ll_opy_.l111111lll_opy_[index-1].l1l1111l11_opy_:
                                l1lllll11ll_opy_.l111111lll_opy_[index].l1111ll11l1_opy_ (True)
                            if l1lllll11ll_opy_.l111111lll_opy_[index-1].l1llllll1l1_opy_ == "down":
                                l1lllll11ll_opy_.l111111lll_opy_[index].l1l111l111l_opy_ ("down")
        self._1l11l11l_opy_ ("\nOptimize model score2, chord assign\n")
        self._1l11l11l_opy_ (str(self._1lll111l_opy_))
    def l1l11llll_opy_ (self):
        def l1lll1l1l1ll_opy_ (l1lll1l1l111_opy_):
            l1lll1l1ll1l_opy_ = 0
            for item in self._1lll111l_opy_.l1l111llll_opy_:
                if item.t == "part-list":
                    for l1lll1l11l1l_opy_ in item.l111l1l1l1_opy_:
                        if l1lll1l1ll1l_opy_ == l1lll1l1l111_opy_:
                            element.l1111l1llll_opy_ (l1lll1l11l1l_opy_.l1lll1l11l1_opy_)
                            element.l1ll1ll11l1_opy_ (l1lll1l11l1l_opy_.l111l111l1_opy_)
                            element.l1l11l11ll1_opy_ (l1lll1l11l1l_opy_.l11l111111_opy_)
                        l1lll1l1ll1l_opy_ += 1
        l111lll1l1_opy_ = 0
        l1l1l1l1l1_opy_ = "0"
        l1lllll11l11_opy_ = 0
        l1lll1l111ll_opy_ = 1
        l1lll1ll1ll1_opy_ = 0
        l1lll1l1l111_opy_ = 0
        for l1lll1l1l11l_opy_,element in enumerate(self._1lll111l_opy_.l1l111llll_opy_):
            if element.t == "part":
                l1lll1l1l1ll_opy_(l1lll1l1l111_opy_)
                for l1lll1ll1l11_opy_,l1lllll11ll_opy_ in enumerate(element.l1lllllll11_opy_):
                    l1llll11l11l_opy_ = 0
                    l1lll1lll111_opy_ = 0
                    l1lllll11111_opy_ = False
                    l1lll1ll1l1l_opy_ = False
                    l1lll1ll1111_opy_ = False
                    l1lll1ll111l_opy_ = False
                    for l1lll1l11lll_opy_,event in enumerate (l1lllll11ll_opy_.l111111lll_opy_):
                        if event.t == "backup":
                            if l1lllll11111_opy_ and (l1lll1ll1l1l_opy_ == l1lll1l1l1l1_opy_ and l1lll1ll1111_opy_ == l1lll1l1lll1_opy_ and l1lll1ll111l_opy_ == l1lll1ll11l1_opy_):
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l1ll11_opy_].l1lllll111l1_opy_ (True)
                                if l1lll1ll1l1l_opy_:
                                    l1lll1l111ll_opy_ = 1
                                elif l1lll1ll1111_opy_:
                                    l1lll1l111ll_opy_ = 2
                                elif l1lll1ll111l_opy_:
                                    l1lll1l111ll_opy_ = 3
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l1ll11_opy_].l1l111l1111_opy_ (l1lll1l111ll_opy_)
                            l1lll1l1ll11_opy_ = l1lll1l11lll_opy_
                            l1lll1l1l1l1_opy_ = l1lll1ll1l1l_opy_
                            l1lll1l1lll1_opy_ = l1lll1ll1111_opy_
                            l1lll1ll11l1_opy_ = l1lll1ll111l_opy_
                            l1lll1ll1l1l_opy_ = False
                            l1lll1ll1111_opy_ = False
                            l1lll1ll111l_opy_ = False
                            l1lll1lll111_opy_ -= event.l1lll1ll1ll_opy_
                            l1llll11l11l_opy_ = l1lll1lll111_opy_
                            if event.l1lll1ll1ll_opy_ == l1lllll11l11_opy_:
                                event.l1llll11lll1_opy_ = True
                            l1lllll11111_opy_ = True
                            self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l1lllll1l111_opy_ (True)
                            if event.l1lll1ll1ll_opy_ == 0 and event.l1llll11lll1_opy_:
                                event.l1lll1ll1ll_opy_ = l1lllll11l11_opy_
                        if event.t == "attributes":
                            for l11111l1l1_opy_ in event.l1l11l1111_opy_:
                                if l11111l1l1_opy_.t == "divisions":
                                    l111lll1l1_opy_ = l11111l1l1_opy_.l111lll1l1_opy_
                                if l11111l1l1_opy_.t == "time":
                                    l1l1l1l1l1_opy_ = l11111l1l1_opy_.l1l1l1l1l1_opy_
                                    l1llll1l1l1_opy_ = l11111l1l1_opy_.l1llll1l1l1_opy_
                                    l1lllll11l11_opy_ = int(l111lll1l1_opy_ * int(l1l1l1l1l1_opy_) / (int(l1llll1l1l1_opy_) / 4))
                        l1lllll11ll_opy_.l1llll1l1111_opy_ (l1lllll11l11_opy_)
                        if event.t == "note":
                            if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l1llllllll11_opy_ and l1lll1ll1ll1_opy_ == 100:
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1ll11ll_opy_-3].l1lll1ll1lll_opy_ = 0
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1ll11ll_opy_-2].l1lll1ll1lll_opy_ = 0
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1ll11ll_opy_-1].l1lll1ll1lll_opy_ = 0
                                self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1ll11ll_opy_].l1lll1ll1lll_opy_ = 0
                                l1lll1ll1ll1_opy_ = 0
                            if event.l11l11ll1l_opy_ == 1:
                                l1lll1ll1l1l_opy_ = True
                            elif event.l11l11ll1l_opy_ == 2:
                                l1lll1ll1111_opy_ = True
                            elif event.l11l11ll1l_opy_ == 3:
                                l1lll1ll111l_opy_ = True
                            event.l1llll11l11l_opy_ = l1llll11l11l_opy_
                            l1lll1lll111_opy_ = l1llll11l11l_opy_ + event.l1lll1ll1ll_opy_
                            event.l1lll1lll111_opy_ = l1lll1lll111_opy_
                            try:
                                if l1llll1l1l1_opy_ == "4":
                                    event.l1llll1ll11l_opy_ = l1llll11l11l_opy_ // l111lll1l1_opy_ +1
                                    event.l1lllll1ll11_opy_ = (l1llll11l11l_opy_ % l111lll1l1_opy_) / l111lll1l1_opy_
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l1llllllll1l_opy_ and event.l1lllll1ll11_opy_ == 0.0:
                                        event.l1lll1ll1lll_opy_ = 1
                                        l1lll1ll1ll1_opy_ = 1
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l1llllllll1l_opy_ and event.l1lllll1ll11_opy_ in [0.25,0.5,0.75]:
                                        event.l1lll1ll1lll_opy_ = 2
                                        l1lll1ll1ll1_opy_ += 1
                                    if l1lll1ll1ll1_opy_ == 4:
                                        l1lll1ll11ll_opy_ = l1lll1l11lll_opy_ # for groups l1lll1l11ll1_opy_ by l1llll1l11_opy_ l1llllllll11_opy_
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-3].l1lll1ll1lll_opy_ = 3
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-2].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-1].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_].l1lll1ll1lll_opy_ = 4
                                        l1lll1ll1ll1_opy_ = 100
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l11111111l1_opy_ and event.l1lllll1ll11_opy_ in [0/8,4/8]:
                                        event.l1lll1ll1lll_opy_ = 1
                                        l1lll1ll1ll1_opy_ = 1
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l11111111l1_opy_ and event.l1lllll1ll11_opy_ in [1/8,2/8,3/8,5/8,6/8,7/8]:
                                        event.l1lll1ll1lll_opy_ = 2
                                        l1lll1ll1ll1_opy_ += 1
                                    if l1lll1ll1ll1_opy_ == 4:
                                        l1lll1ll11ll_opy_ = l1lll1l11lll_opy_ # for groups l1lll1l11ll1_opy_ by l1llll1l11_opy_ l1llllllll11_opy_
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-3].l1lll1ll1lll_opy_ = 3
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-2].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_-1].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l11lll_opy_].l1lll1ll1lll_opy_ = 4
                                        l1lll1ll1ll1_opy_ = 100
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l1lllllll11l_opy_ and event.l1lllll1ll11_opy_ in [0/16,4/16,8/16,12/16]:
                                        event.l1lll1ll1lll_opy_ = 1
                                        l1lll1ll1ll1_opy_ = 1
                                    if event.type == l1ll1ll111l_opy_.l1111111ll1_opy_.l1lllllll11l_opy_ and event.l1lllll1ll11_opy_ in [1/16,2/16,3/16,5/16,6/16,7/16,9/16,10/16,11/16,13/16,14/16,15/16]:
                                        event.l1lll1ll1lll_opy_ = 2
                                        l1lll1ll1ll1_opy_ += 1
                                    if l1lll1ll1ll1_opy_ == 4:
                                        l1lll1ll11ll_opy_ = l1lll1l11lll_opy_
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[
                                            l1lll1l11lll_opy_ - 3].l1lll1ll1lll_opy_ = 3
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[
                                            l1lll1l11lll_opy_ - 2].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[
                                            l1lll1l11lll_opy_ - 1].l1lll1ll1lll_opy_ = 4
                                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[
                                            l1lll1l11lll_opy_].l1lll1ll1lll_opy_ = 4
                                        l1lll1ll1ll1_opy_ = 100
                            except:
                                pass
                            if event.l1lll11l11l_opy_ in [0,3]:
                                l1llll11l11l_opy_ += event.l1lll1ll1ll_opy_
                        else: # in l1lll1l11l11_opy_ of other item than a note
                            l1lll1ll1ll1_opy_ = 0
                    if l1lllll11111_opy_ and (l1lll1ll1l1l_opy_ == l1lll1l1l1l1_opy_ and l1lll1ll1111_opy_ == l1lll1l1lll1_opy_ and l1lll1ll111l_opy_ == l1lll1ll11l1_opy_):
                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l1ll11_opy_].l1lllll111l1_opy_ (True)
                        if l1lll1ll1l1l_opy_:
                            l1lll1l111ll_opy_ = 1
                        elif l1lll1ll1111_opy_:
                            l1lll1l111ll_opy_ = 2
                        elif l1lll1ll111l_opy_:
                            l1lll1l111ll_opy_ = 3
                        self._1lll111l_opy_.l1l111llll_opy_[l1lll1l1l11l_opy_].l1lllllll11_opy_[l1lll1ll1l11_opy_].l111111lll_opy_[l1lll1l1ll11_opy_].l1l111l1111_opy_ (l1lll1l111ll_opy_)
                    l1lll1ll1ll1_opy_ = 0 # for l1lll1l1llll_opy_ end of l1lllll11ll_opy_
                l1lll1l1l111_opy_ += 1
        self._1l11l11l_opy_ ("\nOptimize model score2, with measure position\n")
        self._1l11l11l_opy_ (str(self._1lll111l_opy_))