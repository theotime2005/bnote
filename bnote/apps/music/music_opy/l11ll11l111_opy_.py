"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

from .l11l1l1l111_opy_ import *


class l11l1lll1l1_opy_:
    def __init__(self, lou, l1l1l111_opy_, l1l1ll11lll_opy_, l1ll1111l1_opy_, settings):
        self.lou = lou
        self._1llll111_opy_ = l1l1l111_opy_
        self._1l1l1lll1l_opy_ = l1l1ll11lll_opy_
        self._1l1l1l1l_opy_ = l1ll1111l1_opy_
        (self._11l1lll_opy_, self._111l1ll_opy_) = settings
        self._111ll11l11_opy_ = 1
        self.l11ll1lll1l_opy_ = True
        self.l111lll1111_opy_ = 0
        self.l111ll1l1l1_opy_ = True
        self.l11l11l1ll1_opy_ = 0
        self.l11l1l11l1l_opy_ = False
        self.l111ll1ll1l_opy_ = list()
        self.l11l1l1ll11_opy_ = list()

    def l1ll111111_opy_(self, text):
        if self._11l1lll_opy_[self._111l1ll_opy_]["braille_type"] == "dot-8":
            return self.lou.to_dots_8(text).replace(b0, b7)
        else:
            return self.lou.l11lll1llll_opy_(
                self.lou.l11l1lllll1_opy_(text)[0]
            ).replace(b0, b7)

    def l1ll1l_opy_(self, element):
        (l1l11lll_opy_, braille) = l11l1l1l1l1_opy_.get(
            (element.l1l1l_opy_, element.l1111ll1l_opy_), (None, None)
        )
        if l1l11lll_opy_:
            return braille
        elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
            return element.l1l1l_opy_
        elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
            return element.l1111ll1l_opy_

    def l11ll1lllll_opy_(self, element):
        (l1l11lll_opy_, braille) = l11l1l1l1l1_opy_.get(
            (element.l1l1l_opy_, element.l1111ll1l_opy_), (None, None)
        )
        if l1l11lll_opy_:
            return braille
        elif (
            self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name"
            and element.l1l1l_opy_ != "no"
        ):
            return "".join(
                [b56, b23, b23, b1234, self.l1ll111111_opy_(element.l1l1l_opy_)]
            )
        elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
            if element.l1111ll1l_opy_ == "no":
                element.l1111ll1l_opy_ = element.l1l1l_opy_
            return "".join(
                [b56, b23, b23, b1234, self.l1ll111111_opy_(element.l1111ll1l_opy_)]
            )

    def l11l111l111_opy_(self, l1l111l1l1l_opy_):
        _111lll1l11_opy_ = "no"
        _name = "no"
        _11l11l1l1l_opy_ = "no"
        for i in self._1l1l1l1l_opy_.l1l1l1l_opy_:
            if i.t == "part-list":
                _111lll1l11_opy_ = i.l1l1l1111l_opy_[l1l111l1l1l_opy_].l1llll1llll_opy_
                _name = i.l1l1l1111l_opy_[l1l111l1l1l_opy_].l1l1l_opy_
                _11l11l1l1l_opy_ = i.l1l1l1111l_opy_[l1l111l1l1l_opy_].l1111ll1l_opy_
        if self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
            if _name == "Br Piano right hand":
                return b46 + b345
            elif _name == "Br Piano left hand":
                return b456 + b345
            elif _name == "Br Piano solo":
                return b5 + b345
            elif _name == "Bru Piano right hand":
                return "".join([b46, b345, b345])
            elif _name == "Brd Piano left hand":
                return "".join([b456, b345, b345])
            elif _name == "Br Organ pedal":
                return b45 + b345
            elif _name != "no":
                return "".join([b56, b23, b23, b1234, self.l1ll111111_opy_(_name)])
            else:
                return "".join(
                    [b56, b23, b23, b1234, self.l1ll111111_opy_(_111lll1l11_opy_)]
                )
        elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
            if _11l11l1l1l_opy_ != "no":
                return "".join(
                    [b56, b23, b23, b1234, self.l1ll111111_opy_(_11l11l1l1l_opy_)]
                )
            else:
                return "".join(
                    [b56, b23, b23, b1234, self.l1ll111111_opy_(_111lll1l11_opy_)]
                )

    def l111l11l11l_opy_(self, l1ll1lll1l_opy_):
        return l111l1l1lll_opy_[l1ll1lll1l_opy_]

    def l11lll1l11l_opy_(self, l1l1ll1l1l_opy_):
        return l111l1ll111_opy_[l1l1ll1l1l_opy_]

    def l11ll1l1l1l_opy_(self, step, type, l1l11l11111_opy_):
        if self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"] in ["edit", "listen"]:
            return l111l1l1111_opy_[step, type][0]
        else:
            if self._11l1lll_opy_[self._111l1ll_opy_]["notes_dots"] == "8_dots":
                return l111l1l1111_opy_[step, type][0]
            elif self._11l1lll_opy_[self._111l1ll_opy_]["notes_dots"] == "6_dots":
                return l111l1l1111_opy_[step, type][1]
            elif (
                self._11l1lll_opy_[self._111l1ll_opy_]["notes_dots"]
                == "6_dots_with_group"
            ):
                if l1l11l11111_opy_ in [0, 1, 2, 3]:
                    return l111l1l1111_opy_[step, type][1]
                else:
                    return l111l1l1111_opy_[step, type][2]

    def l11l1l1l11l_opy_(self, dot):
        if dot:
            return b3
        else:
            return ""

    def l111l11l1ll_opy_(self, l1ll1l11_opy_):
        if l1ll1l11_opy_ not in l11ll11ll11_opy_.keys():
            return ""
        if self._11l1lll_opy_[self._111l1ll_opy_]["fingering"]:
            return l11ll11ll11_opy_[l1ll1l11_opy_]
        else:
            return ""

    def l111ll11lll_opy_(self, text):
        if (
            self._11l1lll_opy_[self._111l1ll_opy_]["lyrics"] == "after_each_note"
            or self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"] == "edit"
        ):
            if text != "":
                return "".join([b0, b56, b23, self.l1ll111111_opy_(text), b0])
            else:
                return ""
        elif (
            self._11l1lll_opy_[self._111l1ll_opy_]["lyrics"]
            in ["before_each_section", "after_each_section"]
            and self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"] != "edit"
        ):
            self.l11l1l1ll11_opy_.append(self.l1ll111111_opy_(text))
            return ""
        else:
            return ""

    def l11ll111111_opy_(self, l1ll11111l1_opy_):
        if l1ll11111l1_opy_ in ["start", "stop-start"]:
            return b4 + b14
        else:
            return ""

    def l11lll11lll_opy_(self):
        return b236

    def l11lll11ll1_opy_(self):
        return b6 + b236

    def l11llll111l_opy_(self):
        return b46 + b236

    def l111l1llll1_opy_(self):
        return b6 + b34

    def l11l11l1l11_opy_(self):
        return b126 + b123

    def l11l1lll11l_opy_(self):
        return b235

    def l11ll1111ll_opy_(self, l111l1l1l1l_opy_, l11l1l1l1_opy_):
        if l111l1l1l1l_opy_ and l11l1l1l1_opy_ == "no":
            return b5 + b235
        elif l111l1l1l1l_opy_ and l11l1l1l1_opy_ == "yes":
            return b56 + b235
        if not l111l1l1l1l_opy_ and l11l1l1l1_opy_ == "no":
            return "".join([b5, b235, b123])
        elif not l111l1l1l1l_opy_ and l11l1l1l1_opy_ == "yes":
            return "".join([b56, b235, b123])

    def l11llll1l1l_opy_(self, l11ll1ll11l_opy_, l1ll1l1l11_opy_):
        l11llll1l1l_opy_ = ""
        if l11ll1ll11l_opy_:
            l11llll1l1l_opy_ += b5
        l11llll1l1l_opy_ += b345 + b13
        if l1ll1l1l11_opy_ == "down":
            l11llll1l1l_opy_ += b13
        return l11llll1l1l_opy_

    def l111l1l111l_opy_(self, l11lll_opy_):
        return l11ll1l1lll_opy_[l11lll_opy_]

    def l11l1l1l1ll_opy_(self, l1ll1l11l1l_opy_):
        if l1ll1l11l1l_opy_ == "start":
            return b126 + b14
        elif l1ll1l11l1l_opy_ == "stop":
            return b16 + b14

    def l11ll1l1l11_opy_(self, l1l1l1ll1l1_opy_):
        if l1l1l1ll1l1_opy_ == "crescendo":
            return b345 + b14
        elif l1l1l1ll1l1_opy_ == "diminuendo":
            self.l11l1l11l1l_opy_ = False
            return b345 + b145
        elif l1l1l1ll1l1_opy_ == "stop":
            if self.l11l1l11l1l_opy_:
                return b345 + b25
            else:
                self.l11l1l11l1l_opy_ = True
                return b345 + b256

    def l11lllll1ll_opy_(self, l1l1111l_opy_):
        return "".join([b0, l111l11l111_opy_[l1l1111l_opy_], b0])

    def l11l1llll11_opy_(self, l1ll1lll_opy_, l1ll11l11_opy_, symbol):
        l11l11lll11_opy_ = ""
        for char in l1ll1lll_opy_:
            l11l11lll11_opy_ += numeral_to_braille_high(char)
        l11l1l11l11_opy_ = ""
        for char in l1ll11l11_opy_:
            l11l1l11l11_opy_ += numeral_to_braille_low(char)
        braille = "".join([NumeralPrefix, l11l11lll11_opy_, l11l1l11l11_opy_, b0])
        if symbol == "common":
            braille = "".join([b46, b14, b0])
        if symbol == "cut":
            braille = "".join([b456, b14, b0])
        return braille

    def l11llll11l1_opy_(self, l11l111l1_opy_, l1ll111l11l_opy_, l1l111l1l_opy_):
        if l11l111l1_opy_ == "eighth":
            l11lll1l1ll_opy_ = b145
        elif l11l111l1_opy_ == "quarter":
            l11lll1l1ll_opy_ = b1456
        elif l11l111l1_opy_ == "half":
            l11lll1l1ll_opy_ = b1345
        elif l11l111l1_opy_ == "whole":
            l11lll1l1ll_opy_ = b13456
        else:
            l11lll1l1ll_opy_ = b1345 + b135
        if l1ll111l11l_opy_:
            l111lll11l1_opy_ = b3
        else:
            l111lll11l1_opy_ = ""
        l11l1l111l1_opy_ = ""
        for char in l1l111l1l_opy_:
            l11l1l111l1_opy_ += numeral_to_braille_high(char)
        braille = "".join(
            [
                b0,
                l11lll1l1ll_opy_,
                l111lll11l1_opy_,
                b2356,
                NumeralPrefix,
                l11l1l111l1_opy_,
                b0,
            ]
        )
        return braille

    def l11l1l1ll1l_opy_(self, l1l111l1l_opy_):
        l11l1l1111l_opy_ = round(float(l1l111l1l_opy_))
        l111ll11ll1_opy_ = str(l11l1l1111l_opy_)
        l11l1l111l1_opy_ = ""
        for char in l111ll11ll1_opy_:
            l11l1l111l1_opy_ += numeral_to_braille_high(char)
        braille = "".join([b0, b1456, b2356, b6, NumeralPrefix, l11l1l111l1_opy_, b0])
        return braille

    def l11l1l1llll_opy_(self, l1l1ll1111_opy_, l11l11ll1ll_opy_):
        l11ll1l1111_opy_ = b0
        l11lll1ll1l_opy_ = b2356
        for char in str(l1l1ll1111_opy_):
            l11lll1ll1l_opy_ += numeral_to_braille_high(char)
        l11lll1ll1l_opy_ += b2356 + b0
        if (
            (
                self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"]
                in ["edit", "listen"]
                and l11l11ll1ll_opy_
            )
            or (
                self._11l1lll_opy_[self._111l1ll_opy_]["measure_b123"]
                and l11l11ll1ll_opy_
            )
        ) and not self.l11ll1lll1l_opy_:
            l11ll1l1111_opy_ += b123 + b0
        if (
            self._11l1lll_opy_[self._111l1ll_opy_]["measure_number"]
            and l1l1ll1111_opy_
            % int(self._11l1lll_opy_[self._111l1ll_opy_]["measure_every"])
            == 0
        ):
            l11ll1l1111_opy_ += l11lll1ll1l_opy_
        if self.l11ll1lll1l_opy_:
            self.l111lll1111_opy_ += 1
            if self.l111lll1111_opy_ == self._111ll11l11_opy_:
                self.l11ll1lll1l_opy_ = False
        self.l111ll1l1l1_opy_ = True
        return l11ll1l1111_opy_

    def l11lll11l11_opy_(self, interval):
        return l11lllll111_opy_[interval]

    def l11l1llllll_opy_(self, l11lll1111l_opy_):
        if (
            l11lll1111l_opy_.location == "left"
            and l11lll1111l_opy_.l111l11ll_opy_ == "1"
            and l11lll1111l_opy_.l1l1l111l1l_opy_ == "start"
        ):
            return b3456 + b2
        if (
            l11lll1111l_opy_.location == "left"
            and l11lll1111l_opy_.l111l11ll_opy_ == "2"
            and l11lll1111l_opy_.l1l1l111l1l_opy_ == "start"
        ):
            return b3456 + b23
        if (
            l11lll1111l_opy_.location == "left"
            and l11lll1111l_opy_.l111l11ll_opy_ == "3"
            and l11lll1111l_opy_.l1l1l111l1l_opy_ == "start"
        ):
            return b3456 + b25
        if (
            l11lll1111l_opy_.location == "left"
            and l11lll1111l_opy_.l111l11ll_opy_ == "4"
            and l11lll1111l_opy_.l1l1l111l1l_opy_ == "start"
        ):
            return b3456 + b256
        if (
            l11lll1111l_opy_.location == "left"
            and l11lll1111l_opy_.l1l1ll111ll_opy_ == "heavy-light"
            and l11lll1111l_opy_.repeat == "forward"
        ):
            return b126 + b2356
        if (
            l11lll1111l_opy_.location == "right"
            and l11lll1111l_opy_.l1l1ll111ll_opy_ == "light-heavy"
            and l11lll1111l_opy_.l1l1l1ll11l_opy_
            and l11lll1111l_opy_.repeat == "backward"
        ):
            return b126 + b23
        if l11lll1111l_opy_.l1l1ll111ll_opy_ == "light-light":
            return b126 + b13 + b3
        if l11lll1111l_opy_.l1l1ll111ll_opy_ == "regular":
            return b0 + b123
        return b126 + b13

    def l1ll11lll1l_opy_(
        self, sign, line, l1llll1ll_opy_, l1ll1lll1l1_opy_, l11l1lll111_opy_
    ):
        l111l1ll11l_opy_ = l111ll11111_opy_[sign]
        l11l1111l11_opy_ = l11ll1l1ll1_opy_[line]
        if (
            (sign == "G" and line == "2")
            or (sign == "F" and line == "4")
            or (sign == "C" and line == "4")
        ) and l11l1lll111_opy_ not in ["double", "double-hand"]:
            l11l1111l11_opy_ = ""
        l11ll1ll1l1_opy_ = l11ll111lll_opy_[l1llll1ll_opy_]
        if l11l1lll111_opy_ in ["no", "double"]:
            l111ll1ll11_opy_ = b123
        else:
            l111ll1ll11_opy_ = b13
        l11l11111l1_opy_ = "".join(
            [b345, l111l1ll11l_opy_, l11l1111l11_opy_, l111ll1ll11_opy_]
        )
        l1ll11lll1l_opy_ = "".join([b0, l11l11111l1_opy_, l11ll1ll1l1_opy_, b0])
        if self._11l1lll_opy_[self._111l1ll_opy_]["clef"]:
            return l1ll11lll1l_opy_
        else:
            return ""

    def l11l1llll1l_opy_(self, words):
        if self._11l1lll_opy_[self._111l1ll_opy_]["words"]:
            l11ll111ll1_opy_ = words.strip()
            return "".join(
                [b0, b345, b345, self.l1ll111111_opy_(l11ll111ll1_opy_), b3, b0]
            )
        else:
            return ""

    def l111ll1l11l_opy_(self, l1ll1l1ll1l_opy_, l1lll1l11l1_opy_):
        l11ll1lll11_opy_ = {
            "title": "".join([b56, b23, b23, b14, b2345]),
            "subtitle": "".join([b56, b23, b23, b14, b234]),
            "composer": "".join([b56, b23, b23, b14, b14]),
            "lyricist": "".join([b56, b23, b23, b14, b123]),
            "arranger": "".join([b56, b23, b23, b14, b1]),
            "rights": "".join([b56, b23, b23, b14, b1235]),
            "no": "".join([b56, b23, b23, b14, b2456]),
        }
        l111l1lll11_opy_ = l11ll1lll11_opy_.get(l1lll1l11l1_opy_, "")
        if self._11l1lll_opy_[self._111l1ll_opy_]["credit_words"]:
            l11l1l111ll_opy_ = l1ll1l1ll1l_opy_.strip()
            return l111l1lll11_opy_ + b25 + self.l1ll111111_opy_(l11l1l111ll_opy_)
        else:
            return ""

    def l111l11ll11_opy_(self, title):
        if self._11l1lll_opy_[self._111l1ll_opy_]["credit_words"]:
            l11ll1llll1_opy_ = title.strip()
            return "".join(
                [
                    b56,
                    b23,
                    b23,
                    b2456,
                    b2345,
                    b25,
                    self.l1ll111111_opy_(l11ll1llll1_opy_),
                ]
            )
        else:
            return ""

    def l11l111ll1l_opy_(self, l1l1ll1111_opy_):
        if self._11l1lll_opy_[self._111l1ll_opy_]["credit_words"]:
            l11l1ll1ll1_opy_ = l1l1ll1111_opy_.strip()
            return "".join(
                [
                    b56,
                    b23,
                    b23,
                    b2456,
                    b1345,
                    b25,
                    self.l1ll111111_opy_(l11l1ll1ll1_opy_),
                ]
            )
        else:
            return ""

    def l11lll11111_opy_(self, l111ll_opy_):
        if self._11l1lll_opy_[self._111l1ll_opy_]["karaoke"] and l111ll_opy_ != "":
            return "".join(
                [b0, b56, b23, b23, b13, self.l1ll111111_opy_(l111ll_opy_), b0]
            )
        else:
            return ""

    def l111llll111_opy_(self, l111lll111l_opy_, l1l1llll1l_opy_):
        return "".join(
            [
                b56,
                b23,
                b3,
                b134,
                b1234,
                b36,
                self.l1ll111111_opy_(l111lll111l_opy_),
                b25,
                self.l1ll111111_opy_(l1l1llll1l_opy_),
            ]
        )

    def l11ll11llll_opy_(self, l111lll111l_opy_, l1lll11l1_opy_):
        return "".join(
            [
                b56,
                b23,
                b3,
                b134,
                b14,
                b36,
                self.l1ll111111_opy_(l111lll111l_opy_),
                b25,
                self.l1ll111111_opy_(l1lll11l1_opy_),
            ]
        )

    def l11l1ll111l_opy_(self, l111lll111l_opy_, l1lll11ll1_opy_):
        return "".join(
            [
                b56,
                b23,
                b3,
                b134,
                b1236,
                b36,
                self.l1ll111111_opy_(l111lll111l_opy_),
                b25,
                self.l1ll111111_opy_(l1lll11ll1_opy_),
            ]
        )

    def l11l11ll1l1_opy_(self, element, l1l1l11ll11_opy_):
        l11l11ll1_opy_ = ""
        if l1l1l11ll11_opy_ != 0:
            if self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b145,
                        b24,
                        b36,
                        self.l1ll111111_opy_(element.l1l1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1l1l11ll11_opy_),
                    ]
                )
            elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b145,
                        b24,
                        b36,
                        self.l1ll111111_opy_(element.l1111ll1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1l1l11ll11_opy_),
                    ]
                )
            return l11l11ll1_opy_
        else:
            return ""

    def l11ll1l11l1_opy_(self, element, l1ll1l111ll_opy_):
        l11l11ll1_opy_ = ""
        if l1ll1l111ll_opy_ != 0:
            if self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b14,
                        b125,
                        b36,
                        self.l1ll111111_opy_(element.l1l1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1ll1l111ll_opy_),
                    ]
                )
            elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b14,
                        b125,
                        b36,
                        self.l1ll111111_opy_(element.l1111ll1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1ll1l111ll_opy_),
                    ]
                )
            return l11l11ll1_opy_
        else:
            return ""

    def l111ll1l1ll_opy_(self, element, l1ll1l11111_opy_):
        l11l11ll1_opy_ = ""
        if l1ll1l11111_opy_ != 0:
            if self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b135,
                        b14,
                        b36,
                        self.l1ll111111_opy_(element.l1l1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1ll1l11111_opy_),
                    ]
                )
            elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b135,
                        b14,
                        b36,
                        self.l1ll111111_opy_(element.l1111ll1l_opy_),
                        b25,
                        self.l1ll111111_opy_(l1ll1l11111_opy_),
                    ]
                )
            return l11l11ll1_opy_
        else:
            return ""

    def l11llll11ll_opy_(self, element, l1ll11lll11_opy_, l1llll1l1ll_opy_):
        l11l11ll1_opy_ = ""
        if l1ll11lll11_opy_:
            if self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "name":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b145,
                        b135,
                        b36,
                        self.l1ll111111_opy_(element.l1l1l_opy_),
                        b25,
                    ]
                )
            elif self._11l1lll_opy_[self._111l1ll_opy_]["parts"] == "abbreviation":
                l11l11ll1_opy_ = "".join(
                    [
                        b56,
                        b23,
                        b3,
                        b2345,
                        b1235,
                        b145,
                        b135,
                        b36,
                        self.l1ll111111_opy_(element.l1111ll1l_opy_),
                        b25,
                    ]
                )
            if l1llll1l1ll_opy_ != "":
                l11l11ll1_opy_ += self.l1ll111111_opy_(l1llll1l1ll_opy_)
            return l11l11ll1_opy_
        else:
            return ""

    def l111l1ll1l1_opy_(self, l1l1ll1111_opy_):
        l111llll1ll_opy_ = ""
        for char in l1l1ll1111_opy_:
            braille_char = numeral_to_braille_high((char))
            l111llll1ll_opy_ += braille_char
        return "".join([b3456, l111llll1ll_opy_])

    def l11ll11ll1l_opy_(self, l1l1ll1111_opy_):
        if l1l1ll1111_opy_ == "1":
            return b2356
        else:
            l111llll1ll_opy_ = ""
            for char in l1l1ll1111_opy_:
                braille_char = numeral_to_braille_high((char))
                l111llll1ll_opy_ += braille_char
            return "".join([b3456, l111llll1ll_opy_])

    def section(self, list, l11l111111l_opy_):
        l = len(list)
        r = int(l / l11l111111l_opy_) + (l % l11l111111l_opy_ > 0)
        return [
            list[k * l11l111111l_opy_ : (k + 1) * l11l111111l_opy_] for k in range(r)
        ]

    def l111lll11ll_opy_(self, l11llll1_opy_, values):
        l11ll11111l_opy_ = list()
        first = 0
        values.append(len(l11llll1_opy_) + 1)
        for k in values:
            l11ll11111l_opy_.append(l11llll1_opy_[first : k - 1])
            first = k - 1
        return l11ll11111l_opy_

    def l11l1lll1ll_opy_(self, sec):
        empty = True
        l11l1111l11_opy_ = "".join([b56, b23, b23, b13456])
        for l1lll11_opy_ in sec:
            index = 0
            empty = True
            for item in l1lll11_opy_[3]:
                if l1lll11_opy_[3][index] != "":
                    if empty:
                        l11l1111l11_opy_ += l1lll11_opy_[3][index]
                    else:
                        l11l1111l11_opy_ += b36 + l1lll11_opy_[3][index]
                    empty = False
                index += 1
            l11l1111l11_opy_ += b0
        self._1l1l1lll1l_opy_(l11l1111l11_opy_)
        if not empty:
            self._1llll111_opy_(l11l1111l11_opy_)

    def l11l1111111_opy_(self, element, l11llll1111_opy_):
        for sec in l11llll1111_opy_:
            if (
                self._11l1lll_opy_[self._111l1ll_opy_]["lyrics"]
                == "before_each_section"
            ):
                self.l11l1lll1ll_opy_(sec)
            if self._111ll11l11_opy_ == 1:
                l11l1111l11_opy_ = self.l11ll1lllll_opy_(element)
            else:
                l11l1111l11_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b16]
                )
            for l1lll11_opy_ in sec:
                index = 0
                for item in l1lll11_opy_[0]:
                    l11l1111l11_opy_ += l1lll11_opy_[0][index]
                    index += 1
            self._1l1l1lll1l_opy_(l11l1111l11_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l11l1111l11_opy_)
            if self._111ll11l11_opy_ >= 2:
                l11l1111l11_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b126]
                )
                for l1lll11_opy_ in sec:
                    index = 0
                    for item in l1lll11_opy_[1]:
                        l11l1111l11_opy_ += l1lll11_opy_[1][index]
                        index += 1
                self._1l1l1lll1l_opy_(l11l1111l11_opy_)
                if self._1llll111_opy_:
                    self._1llll111_opy_(l11l1111l11_opy_)
            if self._111ll11l11_opy_ >= 3:
                l11l1111l11_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b146]
                )
                for l1lll11_opy_ in sec:
                    index = 0
                    for item in l1lll11_opy_[2]:
                        l11l1111l11_opy_ += l1lll11_opy_[1][index]
                        index += 1
                self._1l1l1lll1l_opy_(l11l1111l11_opy_)
                if self._1llll111_opy_:
                    self._1llll111_opy_(l11l1111l11_opy_)
            if self._11l1lll_opy_[self._111l1ll_opy_]["lyrics"] == "after_each_section":
                self.l11l1lll1ll_opy_(sec)

    def l11lllll1l1_opy_(self):
        self._1l1l1lll1l_opy_("\nmodel to braille")

        def l11l11llll1_opy_(braille="", l1ll1lll1l1_opy_=1):
            if self.l111l111lll_opy_:
                if l1ll1lll1l1_opy_ == 1:
                    l111lllllll_opy_.append(braille)
                elif l1ll1lll1l1_opy_ == 2:
                    l11l11ll11l_opy_.append(braille)
                elif l1ll1lll1l1_opy_ == 3:
                    l11l11l1111_opy_.append(braille)
                elif l1ll1lll1l1_opy_ == 0:
                    self.l111ll1ll1l_opy_.append(braille)

        def l11l11111ll_opy_(l111ll11l1l_opy_):
            if self._111ll11l11_opy_ == 1:
                l11l1ll11l1_opy_ = self.l11ll1lllll_opy_(element)
            else:
                l11l1ll11l1_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b16]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[0]:
                    l11l1ll11l1_opy_ += l1lll11_opy_[0][index]
                    index += 1
            self._1l1l1lll1l_opy_(l11l1ll11l1_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l11l1ll11l1_opy_)
            l111l1lllll_opy_ = ""
            if self._111ll11l11_opy_ >= 2:
                l111l1lllll_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b126]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[1]:
                    l111l1lllll_opy_ += l1lll11_opy_[1][index]
                    index += 1
            self._1l1l1lll1l_opy_(l111l1lllll_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l111l1lllll_opy_)
            l11l11l11l1_opy_ = ""
            if self._111ll11l11_opy_ >= 3:
                l11l11l11l1_opy_ = "".join(
                    [self.l11ll1lllll_opy_(element), b36, b12, b1235, b146]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[2]:
                    l11l11l11l1_opy_ += l1lll11_opy_[1][index]
                    index += 1
            self._1l1l1lll1l_opy_(l11l11l11l1_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l11l11l11l1_opy_)

        def l11ll11l11l_opy_(l111ll11l1l_opy_, l1l111l1l1l_opy_):
            if self._111ll11l11_opy_ == 1:
                l11l1ll11l1_opy_ = self.l11l111l111_opy_(l1l111l1l1l_opy_)
            else:
                l11l1ll11l1_opy_ = "".join(
                    [self.l11l111l111_opy_(l1l111l1l1l_opy_), b36, b12, b1235, b16]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[0]:
                    l11l1ll11l1_opy_ += l1lll11_opy_[0][index]
                    index += 1
            self._1l1l1lll1l_opy_(l11l1ll11l1_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l11l1ll11l1_opy_)
            l111l1lllll_opy_ = ""
            if self._111ll11l11_opy_ >= 2:
                l111l1lllll_opy_ = "".join(
                    [self.l11l111l111_opy_(l1l111l1l1l_opy_), b36, b12, b1235, b126]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[1]:
                    l111l1lllll_opy_ += l1lll11_opy_[1][index]
                    index += 1
            self._1l1l1lll1l_opy_(l111l1lllll_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l111l1lllll_opy_)
            l11l11l11l1_opy_ = ""
            if self._111ll11l11_opy_ >= 3:
                l11l11l11l1_opy_ = "".join(
                    [self.l11l111l111_opy_(l1l111l1l1l_opy_), b36, b12, b1235, b146]
                )
            for l1lll11_opy_ in l111ll11l1l_opy_:
                index = 0
                for item in l1lll11_opy_[2]:
                    l11l11l11l1_opy_ += l1lll11_opy_[1][index]
                    index += 1
            self._1l1l1lll1l_opy_(l11l11l11l1_opy_)
            if self._1llll111_opy_:
                self._1llll111_opy_(l11l11l11l1_opy_)

        def l11ll1l11ll_opy_():
            index = 0
            for item in self.l111ll1ll1l_opy_:
                self._1l1l1lll1l_opy_(item)
                if self._1llll111_opy_:
                    self._1llll111_opy_(item)
                index += 1
            self.l111ll1ll1l_opy_.clear()
            if self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"] in [
                "edit",
                "listen",
            ]:
                l11l11111ll_opy_(l111ll11l1l_opy_)
            else:
                if self._11l1lll_opy_[self._111l1ll_opy_]["section"] == "system":
                    l111ll1llll_opy_ = self.l111lll11ll_opy_(
                        l111ll11l1l_opy_, l1l1lllll11_opy_
                    )
                    self.l11l1111111_opy_(element, l111ll1llll_opy_)
                elif self._11l1lll_opy_[self._111l1ll_opy_]["section"] == "total_part":
                    l11l11111ll_opy_(l111ll11l1l_opy_)
                else:
                    l11llll1111_opy_ = self.section(
                        l111ll11l1l_opy_,
                        int(
                            self._11l1lll_opy_[self._111l1ll_opy_][
                                "measures_per_section"
                            ]
                        ),
                    )
                    self.l11l1111111_opy_(element, l11llll1111_opy_)

        def l11l1ll1lll_opy_():
            index = 0
            for item in self.l111ll1ll1l_opy_:
                self._1l1l1lll1l_opy_(item)
                if self._1llll111_opy_:
                    self._1llll111_opy_(item)
                index += 1
            self.l111ll1ll1l_opy_.clear()
            try:
                l11l1ll1l11_opy_ = len(self.l11ll1ll1ll_opy_[0][0])
            except:
                l11l1ll1l11_opy_ = -1
            if self._11l1lll_opy_[self._111l1ll_opy_]["section"] == "number":
                l1llll_opy_ = 0
                l11llll1l11_opy_ = list()
                while l1llll_opy_ < l11l1ll1l11_opy_:
                    l1l111l1l1l_opy_ = 0
                    for part in self.l11ll1ll1ll_opy_:
                        self._111ll11l11_opy_ = part[2]
                        for l1lll11_opy_ in part[0][
                            l1llll_opy_ : min(
                                l1llll_opy_
                                + int(
                                    self._11l1lll_opy_[self._111l1ll_opy_][
                                        "measures_per_section"
                                    ]
                                ),
                                len(part[0]),
                            )
                        ]:
                            l11llll1l11_opy_.append(l1lll11_opy_)
                        l11ll11l11l_opy_(l11llll1l11_opy_, l1l111l1l1l_opy_)
                        l11llll1l11_opy_.clear()
                        l1l111l1l1l_opy_ += 1
                    l1llll_opy_ += int(
                        self._11l1lll_opy_[self._111l1ll_opy_]["measures_per_section"]
                    )
            elif self._11l1lll_opy_[self._111l1ll_opy_]["section"] == "system":
                l111ll111ll_opy_ = list()
                for part in self.l11ll1ll1ll_opy_:
                    for system in part[1]:
                        l111ll111ll_opy_.append(system - 1)
                l11ll1111l1_opy_ = sorted(l111ll111ll_opy_)
                l11l111l11l_opy_ = list()
                for i in l11ll1111l1_opy_:
                    if i not in l11l111l11l_opy_:
                        l11l111l11l_opy_.append(i)
                l11l111l11l_opy_.append(l11l1ll1l11_opy_)
                l1llll_opy_ = 0
                l11llll1l11_opy_ = list()
                l11l11l11ll_opy_ = 0
                for system in l11l111l11l_opy_:
                    l1l111l1l1l_opy_ = 0
                    for part in self.l11ll1ll1ll_opy_:
                        self._111ll11l11_opy_ = part[2]
                        for l1lll11_opy_ in part[0][
                            l1llll_opy_ : min(
                                l1llll_opy_ + system - l11l11l11ll_opy_, len(part[0])
                            )
                        ]:
                            l11llll1l11_opy_.append(l1lll11_opy_)
                        l11ll11l11l_opy_(l11llll1l11_opy_, l1l111l1l1l_opy_)
                        l11llll1l11_opy_.clear()
                        l1l111l1l1l_opy_ += 1
                    l1llll_opy_ += system - l11l11l11ll_opy_
                    l11l11l11ll_opy_ = system

        def l11l111ll11_opy_(l11ll1ll1_opy_, l1lll11111_opy_, l1ll1lll1l1_opy_):
            l11lll111ll_opy_ = (l11ll1ll1_opy_ / l1lll11111_opy_) // 1
            while l11lll111ll_opy_ > 0:
                if l11lll111ll_opy_ >= 4:
                    l11l11llll1_opy_(
                        self.l11ll1l1l1l_opy_(
                            "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111l11_opy_, 0
                        ),
                        l1ll1lll1l1_opy_,
                    )
                    l11lll111ll_opy_ -= 4
                if l11lll111ll_opy_ >= 2:
                    l11l11llll1_opy_(
                        self.l11ll1l1l1l_opy_(
                            "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111l1l_opy_, 0
                        ),
                        l1ll1lll1l1_opy_,
                    )
                    l11lll111ll_opy_ -= 2
                if l11lll111ll_opy_ >= 1:
                    l11l11llll1_opy_(
                        self.l11ll1l1l1l_opy_(
                            "no", l11lll1ll_opy_.l1l111ll11l_opy_.l11llllllll_opy_, 0
                        ),
                        l1ll1lll1l1_opy_,
                    )
                    l11lll111ll_opy_ -= 1
            l111ll1l111_opy_ = (l11ll1ll1_opy_ / l1lll11111_opy_) % 1
            if l111ll1l111_opy_ >= 1 / 2:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l11ll_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 2
            if l111ll1l111_opy_ >= 1 / 4:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111lll_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 4
            if l111ll1l111_opy_ >= 1 / 8:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l111l_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 8
            if l111ll1l111_opy_ >= 1 / 16:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l11l1l111_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 16
            if l111ll1l111_opy_ >= 1 / 32:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l11lllllll1_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 32
            if l111ll1l111_opy_ >= 1 / 64:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l111111l1_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 64
            if l111ll1l111_opy_ >= 1 / 128:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l11llllll1l_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 128
            if l111ll1l111_opy_ >= 1 / 256:
                l11l11llll1_opy_(
                    self.l11ll1l1l1l_opy_(
                        "no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l1111111l_opy_, 0
                    ),
                    l1ll1lll1l1_opy_,
                )
                l111ll1l111_opy_ -= 1 / 256

        l11l111lll1_opy_ = True
        l111l1l1l11_opy_ = 0  # for groups of l11l1ll11_opy_
        self.l111lll1lll_opy_ = False  # l1l11l1_opy_ for l1l1l1111_opy_-l1lll1l11_opy_ in a part, insert a sign for l11l11l111l_opy_ l11l1ll1l1l_opy_
        self._111ll11l11_opy_ = 1
        l1l1111l_opy_ = 0
        l111l11ll1l_opy_ = 0
        l111lllll1l_opy_ = ""
        l111l1l11ll_opy_ = ""
        l11ll1l111l_opy_ = ""
        l111l111l_opy_ = False
        l111l111l11_opy_ = False  # l1l11l1_opy_ for braille l1l1ll1l1l_opy_ which l11l1l1lll1_opy_ on the first note of the l111l11l1_opy_ for l11llll1ll1_opy_
        l111lll1l1l_opy_ = False  # l1l11l1_opy_ for braille l1l1ll1l1l_opy_ which l11l1l1lll1_opy_ of the first note of the l111l11l1_opy_ for l111l111l1l_opy_
        l11ll11lll1_opy_ = False  # l1l11l1_opy_ for braille l1l1ll1l1l_opy_ which l11l1l1lll1_opy_ of the first note of the l111l11l1_opy_ for l11l111llll_opy_
        self.l11l1l11l1l_opy_ = True  # l1l11l1_opy_ to l111l1l11l1_opy_ the l111ll1lll1_opy_ end of l1ll111ll1_opy_ b345 + b25 for end l11l1111lll_opy_, b345 + b256 for end l111llll1l1_opy_
        l11l11lllll_opy_ = True
        self.l11ll1lll1l_opy_ = True
        self.l111ll1ll1l_opy_ = list()
        self.l11l1l11lll_opy_ = list()
        self.l11l1l11ll1_opy_ = list()
        self.l11ll1ll1ll_opy_ = list()
        self._1lll1l111_opy_ = self._11l1lll_opy_[self._111l1ll_opy_][
            "ascending_chords"
        ]
        self._111ll1111l_opy_ = list()
        self.l111l111lll_opy_ = True
        l111l11lll1_opy_ = list()
        for element in self._1l1l1l1l_opy_.l1l1l1l_opy_:
            if element.t == "part":
                self._111ll11l11_opy_ = 1
                for l1lll11_opy_ in element.l1ll11llll_opy_:
                    for event in l1lll11_opy_.l1l111ll11_opy_:
                        if event.t == "attributes":
                            for l1llllll1l1_opy_ in event.l1l1l1lllll_opy_:
                                if l1llllll1l1_opy_.t == "staves":
                                    self._111ll11l11_opy_ = int(
                                        l1llllll1l1_opy_.l1lll1l11_opy_
                                    )
                        if event.t == "note":
                            if event.l1ll1lll1l1_opy_ > self._111ll11l11_opy_:
                                self._111ll11l11_opy_ = event.l1ll1lll1l1_opy_
                l111l11lll1_opy_.append(
                    [
                        element.l1llll1llll_opy_,
                        element.l1l1l_opy_,
                        element.l1111ll1l_opy_,
                        self._111ll11l11_opy_,
                    ]
                )
        self._1l1l1lll1l_opy_("braille_sub_parts " + str(l111l11lll1_opy_))
        l11l1ll11ll_opy_ = list()
        for part in l111l11lll1_opy_:
            if part[3] == 1:
                l11l1ll11ll_opy_.append(
                    [
                        part[0],
                        part[0],
                        part[1],
                        part[1],
                        part[2],
                        part[2],
                        1,
                        "no",
                        "no",
                        "no",
                        "no",
                    ]
                )
            else:
                l11l1ll11ll_opy_.append(
                    [
                        part[0],
                        part[0] + "-br1",
                        part[1],
                        part[1] + "-br1",
                        part[2],
                        part[2] + "-br1",
                        part[3],
                        "no",
                        "no",
                        "no",
                        "no",
                    ]
                )
            if part[3] >= 2:
                l11l1ll11ll_opy_.append(
                    [
                        part[0],
                        part[0] + "-br2",
                        part[1],
                        part[1] + "-br2",
                        part[2],
                        part[2] + "-br2",
                        2,
                        "no",
                        "no",
                        "no",
                        "no",
                    ]
                )
            if part[3] >= 3:
                l11l1ll11ll_opy_.append(
                    [
                        part[0],
                        part[0] + "-br3",
                        part[1],
                        part[1] + "-br3",
                        part[2],
                        part[2] + "-br3",
                        3,
                        "no",
                        "no",
                        "no",
                        "no",
                    ]
                )
        l11l11l1lll_opy_ = 0
        l11l1l11111_opy_ = (
            1  # l1l11l1_opy_ for l11lll111l1_opy_ l11111lll_opy_ or for forward
        )
        l11ll11l1_opy_ = 0
        l1lll11111_opy_ = 1
        for element in self._1l1l1l1l_opy_.l1l1l1l_opy_:
            if element.t == "braille-global":
                l1lll1111_opy_ = ""
                for event in element.l1llll11111_opy_:
                    if event.t == "global-key":
                        l1l1111l_opy_ = event.l1l1111l_opy_
                        l111l11ll1l_opy_ = event.l1l1111l_opy_
                        l1lll1111_opy_ += self.l11lllll1ll_opy_(event.l1l1111l_opy_)
                    elif event.t == "global-time":
                        l1ll1lll_opy_ = event.l1ll1lll_opy_
                        l111lllll1l_opy_ = event.l1ll1lll_opy_
                        l1ll11l11_opy_ = event.l1ll11l11_opy_
                        l111l1l11ll_opy_ = event.l1ll11l11_opy_
                        l11ll1l111l_opy_ = event.symbol
                        l1lll1111_opy_ += self.l11l1llll11_opy_(
                            event.l1ll1lll_opy_, event.l1ll11l11_opy_, event.symbol
                        )
                if l1lll1111_opy_ != "":
                    l11l11llll1_opy_(l1lll1111_opy_, 0)
            if element.t == "credit":
                l11l11llll1_opy_(
                    self.l111ll1l11l_opy_(
                        element.l1ll1l1ll1l_opy_, element.l1lll1l11l1_opy_
                    ),
                    0,
                )
            if element.t == "work":
                if element.l1ll1ll1l11_opy_ != "no":
                    l11l11llll1_opy_(self.l11l111ll1l_opy_(element.l1ll1ll1l11_opy_), 0)
                if element.l1ll1l11lll_opy_ != "no":
                    l11l11llll1_opy_(self.l111l11ll11_opy_(element.l1ll1l11lll_opy_), 0)
            if element.t == "part-list":
                l111lll1ll1_opy_ = 0
                for item in element.l1l1l1111l_opy_:
                    l111lll1ll1_opy_ += 1
                    self._111ll1111l_opy_.append(item.l1ll11l1111_opy_)
                    for info in l11l1ll11ll_opy_:
                        if info[0] == item.l1llll1llll_opy_:
                            info[7] = item.l1ll11l1111_opy_
                    if item.l1l1llll1l_opy_ != "no":
                        for info in l11l1ll11ll_opy_:
                            if info[0] == item.l1llll1llll_opy_:
                                info[8] = item.l1l1llll1l_opy_
                        for part in l111l11lll1_opy_:
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 1:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l111llll111_opy_(
                                            self.l1ll1l_opy_(item), item.l1l1llll1l_opy_
                                        ),
                                    ]
                                )
                            elif part[0] == item.l1llll1llll_opy_ and part[3] >= 2:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l111llll111_opy_(
                                            self.l1ll1l_opy_(item) + "-br1",
                                            item.l1l1llll1l_opy_,
                                        ),
                                    ]
                                )
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l111llll111_opy_(
                                            self.l1ll1l_opy_(item) + "-br2",
                                            item.l1l1llll1l_opy_,
                                        ),
                                    ]
                                )
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 3:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l111llll111_opy_(
                                            self.l1ll1l_opy_(item) + "-br3",
                                            item.l1l1llll1l_opy_,
                                        ),
                                    ]
                                )
                    if item.l1lll11l1_opy_ != "no":
                        for info in l11l1ll11ll_opy_:
                            if info[0] == item.l1llll1llll_opy_:
                                info[9] = item.l1lll11l1_opy_
                        for part in l111l11lll1_opy_:
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 1:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11ll11llll_opy_(
                                            self.l1ll1l_opy_(item), item.l1lll11l1_opy_
                                        ),
                                    ]
                                )
                            elif part[0] == item.l1llll1llll_opy_ and part[3] >= 2:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11ll11llll_opy_(
                                            self.l1ll1l_opy_(item) + "-br1",
                                            item.l1lll11l1_opy_,
                                        ),
                                    ]
                                )
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11ll11llll_opy_(
                                            self.l1ll1l_opy_(item) + "-br2",
                                            item.l1lll11l1_opy_,
                                        ),
                                    ]
                                )
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 3:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11ll11llll_opy_(
                                            self.l1ll1l_opy_(item) + "-br3",
                                            item.l1lll11l1_opy_,
                                        ),
                                    ]
                                )
                    if item.l1lll11ll1_opy_ != "no":
                        for info in l11l1ll11ll_opy_:
                            if info[0] == item.l1llll1llll_opy_:
                                info[10] = item.l1lll11ll1_opy_
                        for part in l111l11lll1_opy_:
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 1:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11l1ll111l_opy_(
                                            self.l1ll1l_opy_(item), item.l1lll11ll1_opy_
                                        ),
                                    ]
                                )
                            elif part[0] == item.l1llll1llll_opy_ and part[3] >= 2:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11l1ll111l_opy_(
                                            self.l1ll1l_opy_(item) + "-br1",
                                            item.l1lll11ll1_opy_,
                                        ),
                                    ]
                                )
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11l1ll111l_opy_(
                                            self.l1ll1l_opy_(item) + "-br2",
                                            item.l1lll11ll1_opy_,
                                        ),
                                    ]
                                )
                            if part[0] == item.l1llll1llll_opy_ and part[3] == 3:
                                self.l11l1l11lll_opy_.append(
                                    [
                                        l111lll1ll1_opy_,
                                        self.l11l1ll111l_opy_(
                                            self.l1ll1l_opy_(item) + "-br3",
                                            item.l1lll11ll1_opy_,
                                        ),
                                    ]
                                )
                self.l11lll1lll1_opy_ = False
                for part in self._111ll1111l_opy_:
                    if (
                        part
                        != self._11l1lll_opy_[self._111l1ll_opy_]["ascending_chords"]
                    ):
                        self.l11lll1lll1_opy_ = True
            if element.t == "part":
                l11ll11l1_opy_ += 1
                self._111ll11l11_opy_ = l111l11lll1_opy_[l11l11l1lll_opy_][3]
                if self._111ll11l11_opy_ >= 2:
                    self.l111lll1lll_opy_ = True
                l11ll111l1l_opy_ = -1
                l11lll1l1l1_opy_ = -7
                l111l1ll1ll_opy_ = -1
                l111l11llll_opy_ = -7
                l11l1111l1l_opy_ = -1
                l11l111l1l1_opy_ = -7
                l11l11lllll_opy_ = True
                self.l11ll1lll1l_opy_ = True
                self.l111lll1111_opy_ = 0
                l111l1l1ll1_opy_ = False
                l111ll11l1l_opy_ = list()
                l1l1lllll11_opy_ = list()
                if self._111ll1111l_opy_[l11l11l1lll_opy_] == "1":
                    self._1lll1l111_opy_ = True
                elif self._111ll1111l_opy_[l11l11l1lll_opy_] == "-1":
                    self._1lll1l111_opy_ = False
                for l1lll11_opy_ in element.l1ll11llll_opy_:
                    if self.l11l11l1ll1_opy_ > 0:
                        self.l11l11l1ll1_opy_ -= 1
                        l111ll11l1l_opy_.append([[], [], [], []])
                        continue
                    l111lllllll_opy_ = list()
                    l11l11ll11l_opy_ = list()
                    l11l11l1111_opy_ = list()
                    self.l11l1l1ll11_opy_ = list()
                    l1l11111l_opy_ = list()
                    if self.l111lll1lll_opy_ and self.l11ll1lll1l_opy_:
                        l11l11llll1_opy_("".join([b0, b46, b46, b345, b0]), 1)
                        l11l11llll1_opy_("".join([b0, b456, b456, b345, b0]), 2)
                        if self._111ll11l11_opy_ >= 3:
                            l11l11llll1_opy_("".join([b0, b456, b456, b345, b0]), 3)
                    if (
                        self.l11lll1lll1_opy_
                        and self.l11ll1lll1l_opy_
                        and element.l1l1l_opy_
                        not in [
                            "Br Piano right hand",
                            "Br Piano left hand",
                            "Br Piano solo",
                            "Bru Piano right hand",
                            "Brd Piano left hand",
                            "Br Organ pedal",
                        ]
                    ):
                        if self._111ll1111l_opy_[l11l11l1lll_opy_] == "1":
                            l11l11llll1_opy_("".join([b0, b456, b456, b345, b0]), 1)
                        elif self._111ll1111l_opy_[l11l11l1lll_opy_] == "-1":
                            l11l11llll1_opy_("".join([b0, b46, b46, b345, b0]), 1)
                    l11l11llll1_opy_(
                        self.l11l1l1llll_opy_(
                            l1lll11_opy_.l1llllllll1_opy_, l11l11lllll_opy_
                        ),
                        1,
                    )
                    if self._111ll11l11_opy_ >= 2:
                        l11l11llll1_opy_(
                            self.l11l1l1llll_opy_(
                                l1lll11_opy_.l1llllllll1_opy_, l11l11lllll_opy_
                            ),
                            2,
                        )
                    if self._111ll11l11_opy_ >= 3:
                        l11l11llll1_opy_(
                            self.l11l1l1llll_opy_(
                                l1lll11_opy_.l1llllllll1_opy_, l11l11lllll_opy_
                            ),
                            3,
                        )
                    l11l11lllll_opy_ = True
                    if l111l1l1ll1_opy_:
                        try:
                            l11ll111l1l_opy_ = -1
                            l11lll1l1l1_opy_ = -7
                            l111l1ll1ll_opy_ = -1
                            l111l11llll_opy_ = -7
                            l11l1111l1l_opy_ = -1
                            l11l111l1l1_opy_ = -7
                            l111l1l1ll1_opy_ = False
                        except:
                            pass
                    for event in l1lll11_opy_.l1l111ll11_opy_:
                        if event.t == "direction":
                            for l1llllll1l1_opy_ in event.l1lll11l111_opy_:
                                if l1llllll1l1_opy_.t == "words":
                                    l11l11llll1_opy_(
                                        self.l11l1llll1l_opy_(l1llllll1l1_opy_.words),
                                        l1llllll1l1_opy_.l1ll1lll1l1_opy_,
                                    )
                                elif l1llllll1l1_opy_.t == "dynamics":
                                    l11l11llll1_opy_(
                                        self.l111l1l111l_opy_(
                                            l1llllll1l1_opy_.l11lll_opy_
                                        ),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                    if event.l1ll1lll1l1_opy_ == 1:
                                        l11ll111l1l_opy_ = -1
                                        l11lll1l1l1_opy_ = -7
                                    elif event.l1ll1lll1l1_opy_ == 2:
                                        l111l1ll1ll_opy_ = -1
                                        l111l11llll_opy_ = -7
                                    elif event.l1ll1lll1l1_opy_ == 3:
                                        l11l1111l1l_opy_ = -1
                                        l11l111l1l1_opy_ = -7
                                elif l1llllll1l1_opy_.t == "pedal":
                                    l11l11llll1_opy_(
                                        self.l11l1l1l1ll_opy_(
                                            l1llllll1l1_opy_.l1ll1l11l1l_opy_
                                        ),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                elif l1llllll1l1_opy_.t == "wedge":
                                    l11l11llll1_opy_(
                                        self.l11ll1l1l11_opy_(
                                            l1llllll1l1_opy_.l1l1l1ll1l1_opy_
                                        ),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                elif l1llllll1l1_opy_.t == "metronome":
                                    l11l11llll1_opy_(
                                        self.l11llll11l1_opy_(
                                            l1llllll1l1_opy_.l11l111l1_opy_,
                                            l1llllll1l1_opy_.l1ll111l11l_opy_,
                                            l1llllll1l1_opy_.l1l111l1l_opy_,
                                        ),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                elif l1llllll1l1_opy_.t == "sound":
                                    if l1llllll1l1_opy_.l1lll1l1lll_opy_ != "no":
                                        l11l11llll1_opy_(
                                            self.l11l1l1ll1l_opy_(
                                                l1llllll1l1_opy_.l1lll1l1lll_opy_
                                            ),
                                            event.l1ll1lll1l1_opy_,
                                        )
                        if event.t == "backup" and event.l11l111l1ll_opy_:
                            l11l11llll1_opy_(b126 + b345, event.l1ll1lll1l1_opy_)
                            if event.l1ll1lll1l1_opy_ == 1:
                                l11ll111l1l_opy_ = -1
                                l11lll1l1l1_opy_ = -7
                            elif event.l1ll1lll1l1_opy_ == 2:
                                l111l1ll1ll_opy_ = -1
                                l111l11llll_opy_ = -7
                            elif event.l1ll1lll1l1_opy_ == 3:
                                l11l1111l1l_opy_ = -1
                                l11l111l1l1_opy_ = -7
                            l111l1l1ll1_opy_ = True
                        if event.t == "backup" and not event.l11l111l1ll_opy_:
                            l1l11111l_opy_ = list()
                        if (
                            event.t == "backup"
                            and event.l11ll1ll1_opy_ < l11lll11l1l_opy_
                        ):
                            l11l111ll11_opy_(
                                l11lll11l1l_opy_ - event.l11ll1ll1_opy_,
                                l1lll11111_opy_,
                                l11l1l11111_opy_,
                            )
                        if event.t == "forward":
                            l11l111ll11_opy_(
                                event.l11ll1ll1_opy_, l1lll11111_opy_, l11l1l11111_opy_
                            )
                            # if l1lll11111_opy_ / event.l11ll1ll1_opy_ == 4:
                            # l11l11llll1_opy_(self.l11ll1l1l1l_opy_("no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l11111lll_opy_, 0), l11l1l11111_opy_)
                            # if l1lll11111_opy_ / event.l11ll1ll1_opy_ == 2:
                            # l11l11llll1_opy_(self.l11ll1l1l1l_opy_("no", l11lll1ll_opy_.l1l111ll11l_opy_.l1l111l11ll_opy_, 0), l11l1l11111_opy_)
                        if event.t == "attributes":
                            for l1llllll1l1_opy_ in event.l1l1l1lllll_opy_:
                                if l1llllll1l1_opy_.t == "key":
                                    l1l1111l_opy_ = l1llllll1l1_opy_.l1l1111l_opy_
                                    if l1l1111l_opy_ != l111l11ll1l_opy_:
                                        l11l11llll1_opy_(
                                            self.l11lllll1ll_opy_(l1l1111l_opy_), 1
                                        )
                                        if self._111ll11l11_opy_ >= 2:
                                            l11l11llll1_opy_(
                                                self.l11lllll1ll_opy_(l1l1111l_opy_), 2
                                            )
                                        if self._111ll11l11_opy_ >= 3:
                                            l11l11llll1_opy_(
                                                self.l11lllll1ll_opy_(l1l1111l_opy_), 3
                                            )
                                elif l1llllll1l1_opy_.t == "time" and (
                                    l1llllll1l1_opy_.l1ll1lll_opy_ != l111lllll1l_opy_
                                    or l1llllll1l1_opy_.l1ll11l11_opy_
                                    != l111l1l11ll_opy_
                                    or l1llllll1l1_opy_.symbol != l11ll1l111l_opy_
                                ):
                                    l1ll1lll_opy_ = l1llllll1l1_opy_.l1ll1lll_opy_
                                    l1ll11l11_opy_ = l1llllll1l1_opy_.l1ll11l11_opy_
                                    l11lll11l1l_opy_ = int(
                                        int(l1ll1lll_opy_)
                                        * 4
                                        / int(l1ll11l11_opy_)
                                        * l1lll11111_opy_
                                    )
                                    l11l11llll1_opy_(
                                        self.l11l1llll11_opy_(
                                            l1llllll1l1_opy_.l1ll1lll_opy_,
                                            l1llllll1l1_opy_.l1ll11l11_opy_,
                                            l1llllll1l1_opy_.symbol,
                                        ),
                                        1,
                                    )
                                    if self._111ll11l11_opy_ >= 2:
                                        l11l11llll1_opy_(
                                            self.l11l1llll11_opy_(
                                                l1llllll1l1_opy_.l1ll1lll_opy_,
                                                l1llllll1l1_opy_.l1ll11l11_opy_,
                                                l1llllll1l1_opy_.symbol,
                                            ),
                                            2,
                                        )
                                    if self._111ll11l11_opy_ >= 3:
                                        l11l11llll1_opy_(
                                            self.l11l1llll11_opy_(
                                                l1llllll1l1_opy_.l1ll1lll_opy_,
                                                l1llllll1l1_opy_.l1ll11l11_opy_,
                                                l1llllll1l1_opy_.symbol,
                                            ),
                                            3,
                                        )
                                elif l1llllll1l1_opy_.t == "clef":
                                    l11l11llll1_opy_(
                                        self.l1ll11lll1l_opy_(
                                            l1llllll1l1_opy_.sign,
                                            l1llllll1l1_opy_.line,
                                            l1llllll1l1_opy_.l1llll1ll_opy_,
                                            l1llllll1l1_opy_.l11l1111ll1_opy_,
                                            l1llllll1l1_opy_.l1ll11lll1l_opy_,
                                        ),
                                        l1llllll1l1_opy_.l11l1111ll1_opy_,
                                    )
                                elif l1llllll1l1_opy_.t == "transpose":
                                    self.l11l1l11lll_opy_.append(
                                        [
                                            l11ll11l1_opy_,
                                            self.l11l11ll1l1_opy_(
                                                element,
                                                l1llllll1l1_opy_.l1l1l11ll11_opy_,
                                            ),
                                        ]
                                    )
                                    self.l11l1l11lll_opy_.append(
                                        [
                                            l11ll11l1_opy_,
                                            self.l11ll1l11l1_opy_(
                                                element,
                                                l1llllll1l1_opy_.l1ll1l111ll_opy_,
                                            ),
                                        ]
                                    )
                                    self.l11l1l11lll_opy_.append(
                                        [
                                            l11ll11l1_opy_,
                                            self.l111ll1l1ll_opy_(
                                                element,
                                                l1llllll1l1_opy_.l1ll1l11111_opy_,
                                            ),
                                        ]
                                    )
                                    self.l11l1l11lll_opy_.append(
                                        [
                                            l11ll11l1_opy_,
                                            self.l11llll11ll_opy_(
                                                element,
                                                l1llllll1l1_opy_.l1ll11lll11_opy_,
                                                l1llllll1l1_opy_.l1llll1l1ll_opy_,
                                            ),
                                        ]
                                    )
                                elif l1llllll1l1_opy_.t == "measure-style":
                                    if l1llllll1l1_opy_.l1l11lllll_opy_ != "no":
                                        self.l11l11l1ll1_opy_ = (
                                            int(l1llllll1l1_opy_.l1l11lllll_opy_) - 1
                                        )
                                        l11l11llll1_opy_(
                                            self.l111l1ll1l1_opy_(
                                                l1llllll1l1_opy_.l1l11lllll_opy_
                                            ),
                                            1,
                                        )
                                        if self._111ll11l11_opy_ >= 2:
                                            l11l11llll1_opy_(
                                                self.l111l1ll1l1_opy_(
                                                    l1llllll1l1_opy_.l1l11lllll_opy_
                                                ),
                                                2,
                                            )
                                        if self._111ll11l11_opy_ >= 3:
                                            l11l11llll1_opy_(
                                                self.l111l1ll1l1_opy_(
                                                    l1llllll1l1_opy_.l1l11lllll_opy_
                                                ),
                                                3,
                                            )
                                    if (
                                        l1llllll1l1_opy_.l11ll11l1l1_opy_ != "no"
                                        and l1llllll1l1_opy_.l11lll1ll11_opy_ != "stop"
                                    ):
                                        l11l11llll1_opy_(
                                            self.l11ll11ll1l_opy_(
                                                l1llllll1l1_opy_.l11ll11l1l1_opy_
                                            ),
                                            1,
                                        )
                                        if self._111ll11l11_opy_ >= 2:
                                            l11l11llll1_opy_(
                                                self.l11ll11ll1l_opy_(
                                                    l1llllll1l1_opy_.l11ll11l1l1_opy_
                                                ),
                                                2,
                                            )
                                        if self._111ll11l11_opy_ >= 3:
                                            l11l11llll1_opy_(
                                                self.l11ll11ll1l_opy_(
                                                    l1llllll1l1_opy_.l11ll11l1l1_opy_
                                                ),
                                                3,
                                            )
                                        self.l111l111lll_opy_ = False
                                    if (
                                        l1llllll1l1_opy_.l11ll11l1l1_opy_ != "no"
                                        and l1llllll1l1_opy_.l11lll1ll11_opy_ == "stop"
                                    ):
                                        self.l111l111lll_opy_ = True
                                        l11l11llll1_opy_(
                                            self.l11l1l1llll_opy_(
                                                l1lll11_opy_.l1llllllll1_opy_,
                                                l11l11lllll_opy_,
                                            ),
                                            1,
                                        )
                                elif l1llllll1l1_opy_.t == "divisions":
                                    l1lll11111_opy_ = l1llllll1l1_opy_.l1lll11111_opy_
                                    if (
                                        l111lllll1l_opy_ != ""
                                        and l111l1l11ll_opy_ != ""
                                    ):
                                        l11lll11l1l_opy_ = int(
                                            int(l111lllll1l_opy_)
                                            * 4
                                            / int(l111l1l11ll_opy_)
                                            * l1lll11111_opy_
                                        )
                        if event.t == "barline":
                            l11l11llll1_opy_(self.l11l1llllll_opy_(event), 1)
                            if self._111ll11l11_opy_ >= 2:
                                l11l11llll1_opy_(self.l11l1llllll_opy_(event), 2)
                            if self._111ll11l11_opy_ >= 3:
                                l11l11llll1_opy_(self.l11l1llllll_opy_(event), 3)
                            if event.l1l1ll111ll_opy_ == "light-light":
                                l11l11lllll_opy_ = False
                            l11ll111l1l_opy_ = -1
                            l11lll1l1l1_opy_ = -7
                            l111l1ll1ll_opy_ = -1
                            l111l11llll_opy_ = -7
                            l11l1111l1l_opy_ = -1
                            l11l111l1l1_opy_ = -7
                        if (
                            event.t == "note"
                            and event.l1l1ll11111_opy_ == 3
                            and event.l1ll1111l11_opy_ == 2
                            and not event.l111l11l1_opy_
                        ):
                            if not event.l1llllllll_opy_:
                                l111l1l1l11_opy_ += 1
                            if l111l1l1l11_opy_ == 1 and not event.l1llllllll_opy_:
                                l11l11llll1_opy_(b23, event.l1ll1lll1l1_opy_)
                            if l111l1l1l11_opy_ == 3:
                                l111l1l1l11_opy_ -= 3
                        if event.t == "note" and event.l1llllllll_opy_:
                            if (
                                event.l1l1l1l111_opy_ == "yes"
                                or event.l1l1l1l111_opy_ == "missing"
                            ):
                                l11l11llll1_opy_(b26, event.l1ll1lll1l1_opy_)
                            if event.l1l1l1l111_opy_ == "no":
                                l11l11llll1_opy_(b5 + b26, event.l1ll1lll1l1_opy_)
                        if event.t == "note" and event.l111l1111_opy_:
                            l11l11llll1_opy_(
                                self.l11lll11lll_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "note" and event.l1l11ll111_opy_:
                            l11l11llll1_opy_(
                                self.l11lll11ll1_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "note" and event.l1lll1ll1_opy_:
                            l11l11llll1_opy_(
                                self.l11llll111l_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "note" and event.l111l1_opy_:
                            l11l11llll1_opy_(
                                self.l11l1lll11l_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "note" and event.l1ll1ll1ll_opy_:
                            l11l11llll1_opy_(
                                self.l11ll1111ll_opy_(True, event.l11l_opy_),
                                event.l1ll1lll1l1_opy_,
                            )
                        if event.t == "note" and event.l111111ll_opy_:
                            l11l11llll1_opy_(
                                self.l11ll1111ll_opy_(False, event.l11l1l1l1_opy_),
                                event.l1ll1lll1l1_opy_,
                            )
                        if (
                            event.t == "note"
                            and event.l111l111_opy_
                            and event.l1l1111ll11_opy_ == 1
                        ):
                            l11l11llll1_opy_(
                                self.l11llll1l1l_opy_(False, event.l1lll1111l1_opy_),
                                event.l1ll1lll1l1_opy_,
                            )
                        if (
                            event.t == "note"
                            and event.l1ll11_opy_
                            and event.l1l1111ll11_opy_ == 1
                        ):
                            l11l11llll1_opy_(
                                self.l11llll1l1l_opy_(True, event.l1ll1llll11_opy_),
                                event.l1ll1lll1l1_opy_,
                            )
                        if event.t == "note" and event.l1l1111ll11_opy_ == 0:
                            l11l1l11111_opy_ = event.l1ll1lll1l1_opy_
                            if event.l1ll1l1l_opy_ == "natural":
                                l11l11llll1_opy_(
                                    self.l111l11l11l_opy_(
                                        l11lll1ll_opy_.l1l11llll1l_opy_.l1l11ll11l1_opy_
                                    ),
                                    event.l1ll1lll1l1_opy_,
                                )
                            if (
                                event.step,
                                event.l1ll1lll1l_opy_,
                            ) not in l111l1111ll_opy_[l1l1111l_opy_] and (
                                event.step,
                                event.l1ll1lll1l_opy_,
                            ) not in l1l11111l_opy_:
                                l11l11llll1_opy_(
                                    self.l111l11l11l_opy_(event.l1ll1lll1l_opy_),
                                    event.l1ll1lll1l1_opy_,
                                )
                            for l1ll1lll1l_opy_ in l111l1111ll_opy_[l1l1111l_opy_]:
                                if (
                                    l1ll1lll1l_opy_[0] == event.step
                                    and l1ll1lll1l_opy_[1] != event.l1ll1lll1l_opy_
                                ):
                                    l1l11111l_opy_.append(
                                        (event.step, event.l1ll1lll1l_opy_)
                                    )
                            if (
                                event.l1ll1lll1l_opy_ != "no"
                                and (event.step, event.l1ll1lll1l_opy_)
                                not in l111l1111ll_opy_[l1l1111l_opy_]
                                and (event.step, event.l1ll1lll1l_opy_)
                                not in l1l11111l_opy_
                            ):
                                l1l11111l_opy_.append(
                                    (event.step, event.l1ll1lll1l_opy_)
                                )
                            i = 0
                            for l111l11l1l1_opy_ in l1l11111l_opy_:
                                if (
                                    l111l11l1l1_opy_[0] == event.step
                                    and l111l11l1l1_opy_[1] != event.l1ll1lll1l_opy_
                                ):
                                    l11l11llll1_opy_(
                                        self.l111l11l11l_opy_(event.l1ll1lll1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                    del l1l11111l_opy_[i]
                                    l1l11111l_opy_.append(
                                        (event.step, event.l1ll1lll1l_opy_)
                                    )
                                i += 1
                            if (
                                self._11l1lll_opy_[self._111l1ll_opy_]["section"]
                                == "system"
                                and self.l111ll1l1l1_opy_
                                and l1lll11_opy_.l1llllllll1_opy_ in l1l1lllll11_opy_
                                and self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"]
                                in ["read", "expert"]
                            ):
                                l11l11llll1_opy_(
                                    self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                    event.l1ll1lll1l1_opy_,
                                )
                            elif (
                                self._11l1lll_opy_[self._111l1ll_opy_]["section"]
                                == "number"
                                and self.l111ll1l1l1_opy_
                                and (l1lll11_opy_.l1llllllll1_opy_ - 1)
                                % int(
                                    self._11l1lll_opy_[self._111l1ll_opy_][
                                        "measures_per_section"
                                    ]
                                )
                                == 0
                                and self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"]
                                in ["read", "expert"]
                            ):
                                l11l11llll1_opy_(
                                    self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                    event.l1ll1lll1l1_opy_,
                                )
                            elif event.l1ll1lll1l1_opy_ == 1:
                                if l111l111l11_opy_ == False and (
                                    abs(event.l11ll11l1ll_opy_ - l11lll1l1l1_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l11lll1l1l1_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l11ll111l1l_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                if l111l111l11_opy_ and (
                                    abs(event.l11ll11l1ll_opy_ - l11lllll11l_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l11lllll11l_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l111llllll1_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                            elif event.l1ll1lll1l1_opy_ == 2:
                                if l111lll1l1l_opy_ == False and (
                                    abs(event.l11ll11l1ll_opy_ - l111l11llll_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l111l11llll_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l111l1ll1ll_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                if l111lll1l1l_opy_ and (
                                    abs(event.l11ll11l1ll_opy_ - l11lll1l111_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l11lll1l111_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l11l11lll1l_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                            elif event.l1ll1lll1l1_opy_ == 3:
                                if l11ll11lll1_opy_ == False and (
                                    abs(event.l11ll11l1ll_opy_ - l11l111l1l1_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l11l111l1l1_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l11l1111l1l_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                                if l11ll11lll1_opy_ and (
                                    abs(event.l11ll11l1ll_opy_ - l11l11ll111_opy_) > 4
                                    or (
                                        abs(event.l11ll11l1ll_opy_ - l11l11ll111_opy_)
                                        > 2
                                        and event.l1l1ll1l1l_opy_ != l111ll111l1_opy_
                                    )
                                ):
                                    l11l11llll1_opy_(
                                        self.l11lll1l11l_opy_(event.l1l1ll1l1l_opy_),
                                        event.l1ll1lll1l1_opy_,
                                    )
                            l11l11llll1_opy_(
                                self.l11ll1l1l1l_opy_(
                                    event.step, event.type, event.l1l11l11111_opy_
                                )
                                + self.l11l1l1l11l_opy_(event.dot)
                                + self.l111l11l1ll_opy_(event.l1ll1l11_opy_)
                                + self.l11ll111111_opy_(event.l1ll11111l1_opy_)
                                + self.l111ll11lll_opy_(event.text),
                                event.l1ll1lll1l1_opy_,
                            )
                            if event.l1l1ll1l1l_opy_ != 100:
                                if event.l1ll1lll1l1_opy_ == 1:
                                    l11ll111l1l_opy_ = event.l1l1ll1l1l_opy_
                                    l11lll1l1l1_opy_ = event.l11ll11l1ll_opy_
                                elif event.l1ll1lll1l1_opy_ == 2:
                                    l111l1ll1ll_opy_ = event.l1l1ll1l1l_opy_
                                    l111l11llll_opy_ = event.l11ll11l1ll_opy_
                                elif event.l1ll1lll1l1_opy_ == 3:
                                    l11l1111l1l_opy_ = event.l1l1ll1l1l_opy_
                                    l11l111l1l1_opy_ = event.l11ll11l1ll_opy_
                            if event.l11111l11_opy_ == "stop":
                                l111l111l_opy_ = False
                            if (
                                event.l11111l11_opy_ in ["start", "continue"]
                                or l111l111l_opy_ == True
                            ):
                                l11l11llll1_opy_(b14, event.l1ll1lll1l1_opy_)
                                l111l111l_opy_ = True
                            if event.l1ll1lll1l1_opy_ == 1:
                                l111l111l11_opy_ = False
                            elif event.l1ll1lll1l1_opy_ == 2:
                                l111lll1l1l_opy_ = False
                            elif event.l1ll1lll1l1_opy_ == 3:
                                l11ll11lll1_opy_ = False
                            self.l111ll1l1l1_opy_ = False
                        if event.t == "note" and event.l1l1111ll11_opy_ in [1, 2, 3]:
                            self.l11l1l11ll1_opy_.append(event)
                        if event.t == "note" and event.l1l1111ll11_opy_ == 3:
                            if event.l1ll1lll1l1_opy_ == 1:
                                l111l111l11_opy_ = True
                            elif event.l1ll1lll1l1_opy_ == 2:
                                l111lll1l1l_opy_ = True
                            elif event.l1ll1lll1l1_opy_ == 3:
                                l11ll11lll1_opy_ = True
                            if self.l111lll1lll_opy_:
                                if event.l1ll1lll1l1_opy_ == 1:
                                    self.l11ll1ll111_opy_ = sorted(
                                        self.l11l1l11ll1_opy_,
                                        key=lambda note: note.l11ll11l1ll_opy_,
                                        reverse=True,
                                    )
                                else:
                                    self.l11ll1ll111_opy_ = sorted(
                                        self.l11l1l11ll1_opy_,
                                        key=lambda note: note.l11ll11l1ll_opy_,
                                    )
                            else:
                                if self._1lll1l111_opy_:
                                    self.l11ll1ll111_opy_ = sorted(
                                        self.l11l1l11ll1_opy_,
                                        key=lambda note: note.l11ll11l1ll_opy_,
                                    )
                                else:
                                    self.l11ll1ll111_opy_ = sorted(
                                        self.l11l1l11ll1_opy_,
                                        key=lambda note: note.l11ll11l1ll_opy_,
                                        reverse=True,
                                    )
                            l11ll111l11_opy_ = self.l11ll1ll111_opy_[0].l11ll11l1ll_opy_
                            l111l1lll1l_opy_ = self.l11ll1ll111_opy_[0].l1l1ll1l1l_opy_
                            if event.l1ll1lll1l1_opy_ == 1:
                                l11lllll11l_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l11ll11l1ll_opy_
                                l111llllll1_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l1l1ll1l1l_opy_
                            elif event.l1ll1lll1l1_opy_ == 2:
                                l11lll1l111_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l11ll11l1ll_opy_
                                l11l11lll1l_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l1l1ll1l1l_opy_
                            elif event.l1ll1lll1l1_opy_ == 3:
                                l11l11ll111_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l11ll11l1ll_opy_
                                l111ll111l1_opy_ = self.l11ll1ll111_opy_[
                                    0
                                ].l1l1ll1l1l_opy_
                            for i, l111llll11l_opy_ in enumerate(self.l11ll1ll111_opy_):
                                if i == 0:
                                    if (
                                        l111llll11l_opy_.step,
                                        l111llll11l_opy_.l1ll1lll1l_opy_,
                                    ) not in l111l1111ll_opy_[l1l1111l_opy_] and (
                                        l111llll11l_opy_.step,
                                        l111llll11l_opy_.l1ll1lll1l_opy_,
                                    ) not in l1l11111l_opy_:
                                        l11l11llll1_opy_(
                                            self.l111l11l11l_opy_(
                                                l111llll11l_opy_.l1ll1lll1l_opy_
                                            ),
                                            l111llll11l_opy_.l1ll1lll1l1_opy_,
                                        )
                                    if (
                                        self._11l1lll_opy_[self._111l1ll_opy_][
                                            "section"
                                        ]
                                        == "system"
                                        and self.l111ll1l1l1_opy_
                                        and l1lll11_opy_.l1llllllll1_opy_
                                        in l1l1lllll11_opy_
                                        and self._11l1lll_opy_[self._111l1ll_opy_][
                                            "edit_mode"
                                        ]
                                        in ["read", "expert"]
                                    ):
                                        l11l11llll1_opy_(
                                            self.l11lll1l11l_opy_(
                                                event.l1l1ll1l1l_opy_
                                            ),
                                            event.l1ll1lll1l1_opy_,
                                        )
                                    elif (
                                        self._11l1lll_opy_[self._111l1ll_opy_][
                                            "section"
                                        ]
                                        == "number"
                                        and self.l111ll1l1l1_opy_
                                        and (l1lll11_opy_.l1llllllll1_opy_ - 1)
                                        % int(
                                            self._11l1lll_opy_[self._111l1ll_opy_][
                                                "measures_per_section"
                                            ]
                                        )
                                        == 0
                                        and self._11l1lll_opy_[self._111l1ll_opy_][
                                            "edit_mode"
                                        ]
                                        in ["read", "expert"]
                                    ):
                                        l11l11llll1_opy_(
                                            self.l11lll1l11l_opy_(
                                                event.l1l1ll1l1l_opy_
                                            ),
                                            event.l1ll1lll1l1_opy_,
                                        )
                                    elif event.l1ll1lll1l1_opy_ == 1:
                                        if abs(
                                            l11lllll11l_opy_ - l11lll1l1l1_opy_
                                        ) > 4 or (
                                            abs(l11lllll11l_opy_ - l11lll1l1l1_opy_) > 2
                                            and l111llllll1_opy_ != l11ll111l1l_opy_
                                        ):
                                            l11l11llll1_opy_(
                                                self.l11lll1l11l_opy_(
                                                    l111llll11l_opy_.l1l1ll1l1l_opy_
                                                ),
                                                l111llll11l_opy_.l1ll1lll1l1_opy_,
                                            )
                                    elif event.l1ll1lll1l1_opy_ == 2:
                                        if abs(
                                            l11lll1l111_opy_ - l111l11llll_opy_
                                        ) > 4 or (
                                            abs(l11lll1l111_opy_ - l111l11llll_opy_) > 2
                                            and l11l11lll1l_opy_ != l111l1ll1ll_opy_
                                        ):
                                            l11l11llll1_opy_(
                                                self.l11lll1l11l_opy_(
                                                    l111llll11l_opy_.l1l1ll1l1l_opy_
                                                ),
                                                l111llll11l_opy_.l1ll1lll1l1_opy_,
                                            )
                                    elif event.l1ll1lll1l1_opy_ == 3:
                                        if abs(
                                            l11l11ll111_opy_ - l11l111l1l1_opy_
                                        ) > 4 or (
                                            abs(l11l11ll111_opy_ - l11l111l1l1_opy_) > 2
                                            and l111ll111l1_opy_ != l11l1111l1l_opy_
                                        ):
                                            l11l11llll1_opy_(
                                                self.l11lll1l11l_opy_(
                                                    l111llll11l_opy_.l1l1ll1l1l_opy_
                                                ),
                                                l111llll11l_opy_.l1ll1lll1l1_opy_,
                                            )
                                    l11l11llll1_opy_(
                                        self.l11ll1l1l1l_opy_(
                                            l111llll11l_opy_.step,
                                            l111llll11l_opy_.type,
                                            l111llll11l_opy_.l1l11l11111_opy_,
                                        )
                                        + self.l11l1l1l11l_opy_(l111llll11l_opy_.dot)
                                        + self.l111l11l1ll_opy_(
                                            l111llll11l_opy_.l1ll1l11_opy_
                                        )
                                        + self.l11ll111111_opy_(
                                            l111llll11l_opy_.l1ll11111l1_opy_
                                        ),
                                        l111llll11l_opy_.l1ll1lll1l1_opy_,
                                    )
                                    l11l1ll1111_opy_ = l111llll11l_opy_.text
                                    if event.l1l1ll1l1l_opy_ != 100:
                                        if event.l1ll1lll1l1_opy_ == 1:
                                            l11ll111l1l_opy_ = event.l1l1ll1l1l_opy_
                                            l11lll1l1l1_opy_ = event.l11ll11l1ll_opy_
                                        elif event.l1ll1lll1l1_opy_ == 2:
                                            l111l1ll1ll_opy_ = event.l1l1ll1l1l_opy_
                                            l111l11llll_opy_ = event.l11ll11l1ll_opy_
                                        elif event.l1ll1lll1l1_opy_ == 3:
                                            l11l1111l1l_opy_ = event.l1l1ll1l1l_opy_
                                            l11l111l1l1_opy_ = event.l11ll11l1ll_opy_
                                else:
                                    interval = abs(
                                        l111llll11l_opy_.l11ll11l1ll_opy_
                                        - l11ll111l11_opy_
                                    )
                                    if interval == 0:
                                        l1ll11111l_opy_ = self.l11lll1l11l_opy_(
                                            l111llll11l_opy_.l1l1ll1l1l_opy_
                                        )
                                    else:
                                        l1ll11111l_opy_ = ""
                                    l111lllll11_opy_ = interval
                                    # l1ll11111l_opy_ = ""
                                    while l111lllll11_opy_ > 7:
                                        l111lllll11_opy_ -= 7
                                        l1ll11111l_opy_ = self.l11lll1l11l_opy_(
                                            l111llll11l_opy_.l1l1ll1l1l_opy_
                                        )
                                    if (
                                        l111llll11l_opy_.step,
                                        l111llll11l_opy_.l1ll1lll1l_opy_,
                                    ) not in l111l1111ll_opy_[l1l1111l_opy_] and (
                                        l111llll11l_opy_.step,
                                        l111llll11l_opy_.l1ll1lll1l_opy_,
                                    ) not in l1l11111l_opy_:
                                        l11l11llll1_opy_(
                                            self.l111l11l11l_opy_(
                                                l111llll11l_opy_.l1ll1lll1l_opy_
                                            ),
                                            l111llll11l_opy_.l1ll1lll1l1_opy_,
                                        )
                                    l11l11llll1_opy_(
                                        l1ll11111l_opy_
                                        + self.l11lll11l11_opy_(l111lllll11_opy_)
                                        + self.l111l11l1ll_opy_(
                                            l111llll11l_opy_.l1ll1l11_opy_
                                        )
                                        + self.l11ll111111_opy_(
                                            l111llll11l_opy_.l1ll11111l1_opy_
                                        ),
                                        l111llll11l_opy_.l1ll1lll1l1_opy_,
                                    )
                                    l11l11llll1_opy_(
                                        self.l111ll11lll_opy_(l11l1ll1111_opy_),
                                        l111llll11l_opy_.l1ll1lll1l1_opy_,
                                    )
                            self.l11l1l11ll1_opy_.clear()
                            self.l11ll1ll111_opy_.clear()
                            self.l111ll1l1l1_opy_ = False
                        if event.t == "note" and event.l1l1l1111l1_opy_:
                            l11l11llll1_opy_(
                                self.l111l1llll1_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "note" and event.l1lll1l11ll_opy_:
                            l11l11llll1_opy_(
                                self.l11l11l1l11_opy_(), event.l1ll1lll1l1_opy_
                            )
                        if event.t == "print" and event.l1l1lllll11_opy_ == "yes":
                            l1l1lllll11_opy_.append(l1lll11_opy_.l1llllllll1_opy_)
                        if event.t == "karaoke":
                            l11l11llll1_opy_(
                                self.l11lll11111_opy_(event.l111ll_opy_), 1
                            )
                        if event.t == "sound":
                            if event.l1lll1l1lll_opy_ != "no":
                                l11l11llll1_opy_(
                                    self.l11l1l1ll1l_opy_(event.l1lll1l1lll_opy_), 1
                                )
                    l111ll11l1l_opy_.append(
                        [
                            l111lllllll_opy_,
                            l11l11ll11l_opy_,
                            l11l11l1111_opy_,
                            self.l11l1l1ll11_opy_,
                        ]
                    )
                self.l11ll1ll1ll_opy_.append(
                    (l111ll11l1l_opy_, l1l1lllll11_opy_, self._111ll11l11_opy_)
                )
                if (
                    self._11l1lll_opy_[self._111l1ll_opy_]["view"] == "by_part"
                    or self._11l1lll_opy_[self._111l1ll_opy_]["section"] == "total_part"
                    or self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"]
                    in ["edit", "listen"]
                ):
                    l11ll1l11ll_opy_()
                l11l11l1lll_opy_ += 1
                self.l111lll1lll_opy_ = False
        if (
            self._11l1lll_opy_[self._111l1ll_opy_]["view"] == "by_section"
            and self._11l1lll_opy_[self._111l1ll_opy_]["section"] != "total_part"
        ) and self._11l1lll_opy_[self._111l1ll_opy_]["edit_mode"] not in [
            "edit",
            "listen",
        ]:
            l11l1ll1lll_opy_()
        l111l111ll1_opy_ = sorted(
            self.l11l1l11lll_opy_, key=lambda l11llll1lll_opy_: l11llll1lll_opy_[0]
        )
        for item in l111l111ll1_opy_:
            self._1llll111_opy_(item[1])
        return self._1l1l1l1l_opy_
