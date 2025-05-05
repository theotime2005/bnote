"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from .l1l1l1ll11_opy_ import *


class l1l11l111l1_opy_:
    def __init__(self, l1l1l111_opy_, l1ll1111l1_opy_):
        self._1l1l1l1l_opy_ = l1ll1111l1_opy_
        self._1llll111_opy_ = l1l1l111_opy_

    def l1l11l1111l_opy_(self):
        """
        this function treats chords and assigns the chord_state parameter for braille statement
        0 automatically for notes without chord
        1 for the first note of a chord
        2 for intermediate notes of a chord
        3 for the last note of a chord
        """
        for element in self._1l1l1l1l_opy_.l1l1l1l_opy_:
            if element.t == "part":
                for l1lll11_opy_ in element.l1ll11llll_opy_:
                    for index, event in enumerate(l1lll11_opy_.l1l111ll11_opy_):
                        if event.t == "note" and event.l111l11l1_opy_:
                            if not l1lll11_opy_.l1l111ll11_opy_[
                                index - 1
                            ].l111l11l1_opy_:
                                l1lll11_opy_.l1l111ll11_opy_[
                                    index - 1
                                ].l1l1111ll11_opy_ = 1
                            else:
                                l1lll11_opy_.l1l111ll11_opy_[
                                    index - 1
                                ].l1l1111ll11_opy_ = 2
                            event.l1l1111ll11_opy_ = 3
                            event.l11ll1ll1_opy_ = l1lll11_opy_.l1l111ll11_opy_[
                                index - 1
                            ].l11ll1ll1_opy_
                            if l1lll11_opy_.l1l111ll11_opy_[index - 1].l111l111_opy_:
                                l1lll11_opy_.l1l111ll11_opy_[index].l1l1ll11l_opy_(True)
                            if (
                                l1lll11_opy_.l1l111ll11_opy_[index - 1].l1lll1111l1_opy_
                                == "down"
                            ):
                                l1lll11_opy_.l1l111ll11_opy_[index].l11lll1l1_opy_(
                                    "down"
                                )
                            if l1lll11_opy_.l1l111ll11_opy_[index - 1].l1ll11_opy_:
                                l1lll11_opy_.l1l111ll11_opy_[index].l1l11l11ll_opy_(
                                    True
                                )
                            if (
                                l1lll11_opy_.l1l111ll11_opy_[index - 1].l1ll1llll11_opy_
                                == "down"
                            ):
                                l1lll11_opy_.l1l111ll11_opy_[index].l1l1lll1l_opy_(
                                    "down"
                                )
        self._1llll111_opy_("\nOptimize model score2, chord assign\n")
        self._1llll111_opy_(str(self._1l1l1l1l_opy_))

    def l1l11l1ll11_opy_(self):
        def l1l11l11ll1_opy_(l1l111l1l1l_opy_):
            l1l111l1ll1_opy_ = 0
            for item in self._1l1l1l1l_opy_.l1l1l1l_opy_:
                if item.t == "part-list":
                    for l1l1111l11l_opy_ in item.l1l1l1111l_opy_:
                        if l1l111l1ll1_opy_ == l1l111l1l1l_opy_:
                            element.l11ll1ll_opy_(l1l1111l11l_opy_.l1llll1llll_opy_)
                            element.l1l1lllll_opy_(l1l1111l11l_opy_.l1l1l_opy_)
                            element.l1l_opy_(l1l1111l11l_opy_.l1111ll1l_opy_)
                        l1l111l1ll1_opy_ += 1

        l1lll11111_opy_ = 0
        l1ll1lll_opy_ = "0"
        l1l111lllll_opy_ = 0
        l1l111lll1l_opy_ = 1
        l1l111ll1ll_opy_ = 0
        l1l111l1l1l_opy_ = 0
        for l1111111l_opy_, element in enumerate(self._1l1l1l1l_opy_.l1l1l1l_opy_):
            if element.t == "part":
                l1l11l11ll1_opy_(l1l111l1l1l_opy_)
                for l1l111lll11_opy_, l1lll11_opy_ in enumerate(
                    element.l1ll11llll_opy_
                ):
                    l1l111llll1_opy_ = 0
                    l1l111ll111_opy_ = 0
                    l1l11l1l11l_opy_ = False
                    l1l111ll1l1_opy_ = False
                    l1l11l1l1l1_opy_ = False
                    l1l111l1l11_opy_ = False
                    for l1l11l1l1ll_opy_, event in enumerate(
                        l1lll11_opy_.l1l111ll11_opy_
                    ):
                        if event.t == "backup":
                            if l1l11l1l11l_opy_ and (
                                l1l111ll1l1_opy_ == l1l1111l1ll_opy_
                                and l1l11l1l1l1_opy_ == l1l1111llll_opy_
                                and l1l111l1l11_opy_ == l1l1111l111_opy_
                            ):
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l11l1ll1l_opy_
                                ].l1l11l11lll_opy_(
                                    True
                                )
                                if l1l111ll1l1_opy_:
                                    l1l111lll1l_opy_ = 1
                                elif l1l11l1l1l1_opy_:
                                    l1l111lll1l_opy_ = 2
                                elif l1l111l1l11_opy_:
                                    l1l111lll1l_opy_ = 3
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l11l1ll1l_opy_
                                ].l1ll111lll_opy_(
                                    l1l111lll1l_opy_
                                )
                            l1l11l1ll1l_opy_ = l1l11l1l1ll_opy_
                            l1l1111l1ll_opy_ = l1l111ll1l1_opy_
                            l1l1111llll_opy_ = l1l11l1l1l1_opy_
                            l1l1111l111_opy_ = l1l111l1l11_opy_
                            l1l111ll1l1_opy_ = False
                            l1l11l1l1l1_opy_ = False
                            l1l111l1l11_opy_ = False
                            l1l111ll111_opy_ -= event.l11ll1ll1_opy_
                            l1l111llll1_opy_ = l1l111ll111_opy_
                            if event.l11ll1ll1_opy_ == l1l111lllll_opy_:
                                event.l1l11l111ll_opy_ = True
                            l1l11l1l11l_opy_ = True
                            self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                l1111111l_opy_
                            ].l1ll11llll_opy_[l1l111lll11_opy_].l1l1111lll1_opy_(True)
                            if event.l11ll1ll1_opy_ == 0 and event.l1l11l111ll_opy_:
                                event.l11ll1ll1_opy_ = l1l111lllll_opy_
                        if event.t == "attributes":
                            for l1llllll1l1_opy_ in event.l1l1l1lllll_opy_:
                                if l1llllll1l1_opy_.t == "divisions":
                                    l1lll11111_opy_ = l1llllll1l1_opy_.l1lll11111_opy_
                                if l1llllll1l1_opy_.t == "time":
                                    l1ll1lll_opy_ = l1llllll1l1_opy_.l1ll1lll_opy_
                                    l1ll11l11_opy_ = l1llllll1l1_opy_.l1ll11l11_opy_
                                    l1l111lllll_opy_ = int(
                                        l1lll11111_opy_
                                        * int(l1ll1lll_opy_)
                                        / (int(l1ll11l11_opy_) / 4)
                                    )
                        l1lll11_opy_.l1l111l1lll_opy_(l1l111lllll_opy_)
                        if event.t == "note":
                            if (
                                event.type
                                == l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l11ll_opy_
                                and l1l111ll1ll_opy_ == 100
                            ):
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l111l1111_opy_ - 3
                                ].l1l11l11111_opy_ = 0
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l111l1111_opy_ - 2
                                ].l1l11l11111_opy_ = 0
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l111l1111_opy_ - 1
                                ].l1l11l11111_opy_ = 0
                                self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                    l1111111l_opy_
                                ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                                    l1l111l1111_opy_
                                ].l1l11l11111_opy_ = 0
                                l1l111ll1ll_opy_ = 0
                            if event.l1ll1lll1l1_opy_ == 1:
                                l1l111ll1l1_opy_ = True
                            elif event.l1ll1lll1l1_opy_ == 2:
                                l1l11l1l1l1_opy_ = True
                            elif event.l1ll1lll1l1_opy_ == 3:
                                l1l111l1l11_opy_ = True
                            event.l1l111llll1_opy_ = l1l111llll1_opy_
                            l1l111ll111_opy_ = l1l111llll1_opy_ + event.l11ll1ll1_opy_
                            event.l1l111ll111_opy_ = l1l111ll111_opy_
                            try:
                                if l1ll11l11_opy_ == "4":
                                    event.l1l1111ll1l_opy_ = (
                                        l1l111llll1_opy_ // l1lll11111_opy_ + 1
                                    )
                                    event.l1l1111l1l1_opy_ = (
                                        l1l111llll1_opy_ % l1lll11111_opy_
                                    ) / l1lll11111_opy_
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111lll_opy_
                                        and event.l1l1111l1l1_opy_ == 0.0
                                    ):
                                        event.l1l11l11111_opy_ = 1
                                        l1l111ll1ll_opy_ = 1
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111lll_opy_
                                        and event.l1l1111l1l1_opy_ in [0.25, 0.5, 0.75]
                                    ):
                                        event.l1l11l11111_opy_ = 2
                                        l1l111ll1ll_opy_ += 1
                                    if l1l111ll1ll_opy_ == 4:
                                        l1l111l1111_opy_ = l1l11l1l1ll_opy_  # for groups l1l11111ll1_opy_ by l1l11l11l11_opy_ l1l111l11ll_opy_
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 3
                                        ].l1l11l11111_opy_ = 3
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 2
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 1
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_
                                        ].l1l11l11111_opy_ = 4
                                        l1l111ll1ll_opy_ = 100
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l111l_opy_
                                        and event.l1l1111l1l1_opy_ in [0 / 8, 4 / 8]
                                    ):
                                        event.l1l11l11111_opy_ = 1
                                        l1l111ll1ll_opy_ = 1
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l111l_opy_
                                        and event.l1l1111l1l1_opy_
                                        in [1 / 8, 2 / 8, 3 / 8, 5 / 8, 6 / 8, 7 / 8]
                                    ):
                                        event.l1l11l11111_opy_ = 2
                                        l1l111ll1ll_opy_ += 1
                                    if l1l111ll1ll_opy_ == 4:
                                        l1l111l1111_opy_ = l1l11l1l1ll_opy_  # for groups l1l11111ll1_opy_ by l1l11l11l11_opy_ l1l111l11ll_opy_
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 3
                                        ].l1l11l11111_opy_ = 3
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 2
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 1
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_
                                        ].l1l11l11111_opy_ = 4
                                        l1l111ll1ll_opy_ = 100
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l11l1l111_opy_
                                        and event.l1l1111l1l1_opy_
                                        in [0 / 16, 4 / 16, 8 / 16, 12 / 16]
                                    ):
                                        event.l1l11l11111_opy_ = 1
                                        l1l111ll1ll_opy_ = 1
                                    if (
                                        event.type
                                        == l11lll1ll_opy_.l1l111ll11l_opy_.l1l11l1l111_opy_
                                        and event.l1l1111l1l1_opy_
                                        in [
                                            1 / 16,
                                            2 / 16,
                                            3 / 16,
                                            5 / 16,
                                            6 / 16,
                                            7 / 16,
                                            9 / 16,
                                            10 / 16,
                                            11 / 16,
                                            13 / 16,
                                            14 / 16,
                                            15 / 16,
                                        ]
                                    ):
                                        event.l1l11l11111_opy_ = 2
                                        l1l111ll1ll_opy_ += 1
                                    if l1l111ll1ll_opy_ == 4:
                                        l1l111l1111_opy_ = l1l11l1l1ll_opy_
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 3
                                        ].l1l11l11111_opy_ = 3
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 2
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_ - 1
                                        ].l1l11l11111_opy_ = 4
                                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                                            l1111111l_opy_
                                        ].l1ll11llll_opy_[
                                            l1l111lll11_opy_
                                        ].l1l111ll11_opy_[
                                            l1l11l1l1ll_opy_
                                        ].l1l11l11111_opy_ = 4
                                        l1l111ll1ll_opy_ = 100
                            except:
                                pass
                            if event.l1l1111ll11_opy_ in [0, 3]:
                                l1l111llll1_opy_ += event.l11ll1ll1_opy_
                        else:  # in l1l111l11l1_opy_ of other item than a note
                            l1l111ll1ll_opy_ = 0
                    if l1l11l1l11l_opy_ and (
                        l1l111ll1l1_opy_ == l1l1111l1ll_opy_
                        and l1l11l1l1l1_opy_ == l1l1111llll_opy_
                        and l1l111l1l11_opy_ == l1l1111l111_opy_
                    ):
                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                            l1111111l_opy_
                        ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                            l1l11l1ll1l_opy_
                        ].l1l11l11lll_opy_(
                            True
                        )
                        if l1l111ll1l1_opy_:
                            l1l111lll1l_opy_ = 1
                        elif l1l11l1l1l1_opy_:
                            l1l111lll1l_opy_ = 2
                        elif l1l111l1l11_opy_:
                            l1l111lll1l_opy_ = 3
                        self._1l1l1l1l_opy_.l1l1l1l_opy_[
                            l1111111l_opy_
                        ].l1ll11llll_opy_[l1l111lll11_opy_].l1l111ll11_opy_[
                            l1l11l1ll1l_opy_
                        ].l1ll111lll_opy_(
                            l1l111lll1l_opy_
                        )
                    l1l111ll1ll_opy_ = 0  # for l1111llll_opy_ end of l1lll11_opy_
                l1l111l1l1l_opy_ += 1
        self._1llll111_opy_("\nOptimize model score2, with measure position\n")
        self._1llll111_opy_(str(self._1l1l1l1l_opy_))
