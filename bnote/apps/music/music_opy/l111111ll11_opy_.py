"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l1l1lll1ll11_opy_ import *
from .l111l1l_opy_ import l111111_opy_ as l11l1ll_opy_
class l11111l1111_opy_:
    def __init__(self, lou, l11llll11l_opy_, l1lll111l1l_opy_, l1l11ll11_opy_, settings):
        self.lou = lou
        self._1l1111ll_opy_ = l11llll11l_opy_
        self._11lllll1_opy_ = l1lll111l1l_opy_
        self._1l1l11ll_opy_ = l1l11ll11_opy_
        (self._1ll111l11l1_opy_, self._1ll111ll111_opy_) = settings
    def l1ll111ll1ll_opy_(self, text):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['braille_type'] == 'dot-8':
            return self.lou.to_dots_8(text).replace(b0, b7)
        else:
            return self.lou.l1l1l1lll1l1_opy_(self.lou.l1l1ll11ll11_opy_(text)[0]).replace(b0,b7)
    def l1lll1111l11_opy_(self, element):
        l1l11l1ll111_opy_ = {
            (l11l1ll_opy_.l111l11_opy_, l11l1ll_opy_.l1ll_opy_): (True, b46 + b345),
            (l11l1ll_opy_.l1l1l_opy_, l11l1ll_opy_.l1ll_opy_): (True, b46 + b345 + b345),
            (l11l1ll_opy_.l1l111l_opy_, l11l1ll_opy_.l1l1ll_opy_): (True, b456 + b345),
            (l11l1ll_opy_.l11ll1_opy_, l11l1ll_opy_.l1l1ll_opy_): (True, b456 + b345 + b345),
            (l11l1ll_opy_.l11lll_opy_, l11l1ll_opy_.l111_opy_): (True, b5 + b345),
            (l11l1ll_opy_.l11ll11_opy_, l11l1ll_opy_.l1lll1_opy_): (True, b45 + b345),
            (l11l1ll_opy_.l11lll1_opy_, l11l1ll_opy_.l1llll_opy_): (True, b345 + b234 + b3),
            (l11l1ll_opy_.l111ll_opy_, l11l1ll_opy_.l1llll1_opy_): (True, b345 + b1 + b3),
            (l11l1ll_opy_.l1ll1l1_opy_, l11l1ll_opy_.l111lll_opy_): (True, b345 + b2345 + b3),
            (l11l1ll_opy_.l1l1ll1_opy_, l11l1ll_opy_.l111ll1_opy_): (True, b345 + b12 + b3),
            (l11l1ll_opy_.l11ll1l_opy_, l11l1ll_opy_.l11_opy_): (True, b345 + b234 + b2 + b3),
            (l11l1ll_opy_.l11llll_opy_, l11l1ll_opy_.l1111_opy_): (True, b345 + b1 + b2 + b3),
            (l11l1ll_opy_.l1l1l1_opy_, l11l1ll_opy_.l11l11_opy_): (True, b345 + b2345 + b2 + b3),
            (l11l1ll_opy_.l1l11l_opy_, l11l1ll_opy_.l1l111_opy_): (True, b345 + b12 + b2 + b3),
            (l11l1ll_opy_.l1lllll_opy_, l11l1ll_opy_.l1l11l1_opy_): (True, b345 + b234 + b23 + b3),
            (l11l1ll_opy_.l11l1_opy_, l11l1ll_opy_.l11l11l_opy_): (True, b345 + b1 + b23 + b3),
            (l11l1ll_opy_.l1_opy_, l11l1ll_opy_.ll_opy_): (True, b345 + b2345 + b23 + b3),
            (l11l1ll_opy_.l1l1l1l_opy_, l11l1ll_opy_.l1l1l11_opy_): (True, b345 + b12 + b23 + b3)
        }
        (l1ll11llll1l_opy_, braille) = l1l11l1ll111_opy_.get((element.l111lll1ll_opy_, element.l11111ll1l_opy_), (None, None))
        if l1ll11llll1l_opy_:
            return braille
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
            return element.l111lll1ll_opy_
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
            return element.l11111ll1l_opy_
    def l1l1lll11l1l_opy_(self, element):
        l1l11l1ll111_opy_ = {
            (l11l1ll_opy_.l111l11_opy_, l11l1ll_opy_.l1ll_opy_): (True, b46 + b345),
            (l11l1ll_opy_.l1l1l_opy_, l11l1ll_opy_.l1ll_opy_): (True, b46 + b345 + b345),
            (l11l1ll_opy_.l1l111l_opy_, l11l1ll_opy_.l1l1ll_opy_): (True, b456 + b345),
            (l11l1ll_opy_.l11ll1_opy_, l11l1ll_opy_.l1l1ll_opy_): (True, b456 + b345 + b345),
            (l11l1ll_opy_.l11lll_opy_, l11l1ll_opy_.l111_opy_): (True, b5 + b345),
            (l11l1ll_opy_.l11ll11_opy_, l11l1ll_opy_.l1lll1_opy_): (True, b45 + b345),
            (l11l1ll_opy_.l11lll1_opy_, l11l1ll_opy_.l1llll_opy_): (True, b345 + b234 + b3),
            (l11l1ll_opy_.l111ll_opy_, l11l1ll_opy_.l1llll1_opy_): (True, b345 + b1 + b3),
            (l11l1ll_opy_.l1ll1l1_opy_, l11l1ll_opy_.l111lll_opy_): (True, b345 + b2345 + b3),
            (l11l1ll_opy_.l1l1ll1_opy_, l11l1ll_opy_.l111ll1_opy_): (True, b345 + b12 + b3),
            (l11l1ll_opy_.l11ll1l_opy_, l11l1ll_opy_.l11_opy_): (True, b345 + b234 + b2 + b3),
            (l11l1ll_opy_.l11llll_opy_, l11l1ll_opy_.l1111_opy_): (True, b345 + b1 + b2 + b3),
            (l11l1ll_opy_.l1l1l1_opy_, l11l1ll_opy_.l11l11_opy_): (True, b345 + b2345 + b2 + b3),
            (l11l1ll_opy_.l1l11l_opy_, l11l1ll_opy_.l1l111_opy_): (True, b345 + b12 + b2 + b3),
            (l11l1ll_opy_.l1lllll_opy_, l11l1ll_opy_.l1l11l1_opy_): (True, b345 + b234 + b23 + b3),
            (l11l1ll_opy_.l11l1_opy_, l11l1ll_opy_.l11l11l_opy_): (True, b345 + b1 + b23 + b3),
            (l11l1ll_opy_.l1_opy_, l11l1ll_opy_.ll_opy_): (True, b345 + b2345 + b23 + b3),
            (l11l1ll_opy_.l1l1l1l_opy_, l11l1ll_opy_.l1l1l11_opy_): (True, b345 + b12 + b23 + b3)
        }
        (l1ll11llll1l_opy_, braille) = l1l11l1ll111_opy_.get((element.l111lll1ll_opy_, element.l11111ll1l_opy_), (None, None))
        if l1ll11llll1l_opy_:
            return braille
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name' and element.l111lll1ll_opy_ != "no":
            return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(element.l111lll1ll_opy_)])
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation' and element.l11111ll1l_opy_ != "no":
            return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(element.l11111ll1l_opy_)])
    def l1l1l111llll_opy_(self, l1lll11lll11_opy_):
        _1l1l1ll111l_opy_ = "no"
        _name = "no"
        _1l11lll1111_opy_ = "no"
        for i in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if i.t == "part-list":
                _1l1l1ll111l_opy_ = i.l111l1l1l1_opy_[l1lll11lll11_opy_].l111l1l1ll_opy_
                _name = i.l111l1l1l1_opy_[l1lll11lll11_opy_].l111lll1ll_opy_
                _1l11lll1111_opy_ = i.l111l1l1l1_opy_[l1lll11lll11_opy_].l11111ll1l_opy_
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
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
                return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(_name)])
            else:
                return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(_1l1l1ll111l_opy_)])
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
            if _1l11lll1111_opy_ != "no":
                return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(_1l11lll1111_opy_)])
            else:
                return "".join([b56, b23, b23, b1234, self.l1ll111ll1ll_opy_(_1l1l1ll111l_opy_)])
    def l1l11l11l11l_opy_(self, l11lll11ll_opy_):
        return [l1l1lll11lll_opy_[l11lll11ll_opy_], l1l1lll11lll_opy_[l11lll11ll_opy_]]
    def l1l11ll1111l_opy_(self, l1l11111ll_opy_):
        return l1l1lll1lll1_opy_[l1l11111ll_opy_]
    def l1l1ll11llll_opy_(self, step, type, l1lll1l11ll1_opy_):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] in ['edit', 'listen']:
            return l1l1lll1llll_opy_[step, type][0]
        else:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['notes_dots'] == '8_dots':
                return l1l1lll1llll_opy_[step, type][0]
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['notes_dots'] == '6_dots':
                return l1l1lll1llll_opy_[step, type][1]
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['notes_dots'] == '6_dots_with_group':
                if l1lll1l11ll1_opy_ in [0, 1, 2, 3]:
                    return l1l1lll1llll_opy_[step, type][1]
                else:
                    return l1l1lll1llll_opy_[step, type][2]
    def l1l11ll1l11l_opy_(self, dot):
        if dot:
            return b3
        else:
            return ""
    def l1l1ll111111_opy_(self, l11llll111_opy_):
        if l11llll111_opy_ not in l1l1llll11ll_opy_.keys():
            return ""
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['fingering']:
            return l1l1llll11ll_opy_[l11llll111_opy_]
        else:
            return ""
    def l1l1ll1ll111_opy_(self, text):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['lyrics'] == 'after_each_note' or self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] == 'edit':
            if text != "":
                return "".join([b0, b56, b23, self.l1ll111ll1ll_opy_(text), b0])
            else:
                return ""
        elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['lyrics'] in ['before_each_section', 'after_each_section'] and self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] != 'edit':
            self.l1l1l1l1lll1_opy_.append(self.l1ll111ll1ll_opy_(text))
            return ""
        else:
            return ""
    def l1l1l11lllll_opy_(self, l1l1111111_opy_):
        if l1l1111111_opy_ in ["start", "stop-start"]:
            return b4 + b14
        else:
            return ""
    def l1l11l11lll1_opy_(self):
        return b236
    def l1l1l1ll1111_opy_(self):
        return b6 + b236
    def l1l1l1ll1lll_opy_(self):
        return b46 + b236
    def l1l11l11l1ll_opy_(self):
        return b6 + b34
    def l1l11l1ll1l1_opy_(self):
        return b126 + b123
    def l1l1ll1l1l11_opy_(self):
        return b235
    def l1l11l11l111_opy_(self, l1l1l111l1l1_opy_, l1l11ll1l1_opy_):
        if l1l1l111l1l1_opy_ and l1l11ll1l1_opy_ == "no":
            return b5 + b235
        elif l1l1l111l1l1_opy_ and l1l11ll1l1_opy_ == "yes":
            return b56 + b235
        if not l1l1l111l1l1_opy_ and l1l11ll1l1_opy_ == "no":
            return "".join([b5, b235, b123])
        elif not l1l1l111l1l1_opy_ and l1l11ll1l1_opy_ == "yes":
            return "".join([b56, b235, b123])
    def l1l11l1lll11_opy_(self, l1l1ll111l11_opy_, direction):
        l1l11l1lll11_opy_ = ""
        if l1l1ll111l11_opy_:
            l1l11l1lll11_opy_ += b5
        l1l11l1lll11_opy_ += b345 + b13
        if direction == "down":
            l1l11l1lll11_opy_ += b13
        return l1l11l1lll11_opy_
    def l1l1l1l11lll_opy_(self, l1l11l1ll1_opy_):
        return l1l1llll11l1_opy_[l1l11l1ll1_opy_]
    def l1l1l11lll11_opy_(self, l1l11l1l11_opy_):
        if l1l11l1l11_opy_ == "start":
            return b126 + b14
        elif l1l11l1l11_opy_ == "stop":
            return b16 + b14
    def l1l1ll1l111l_opy_(self, l11ll11ll1_opy_):
        if l11ll11ll1_opy_ == "crescendo":
            return b345 + b14
        elif l11ll11ll1_opy_ == "diminuendo":
            self.l1l11ll11111_opy_ = False
            return b345 + b145
        elif l11ll11ll1_opy_ == "stop":
            if self.l1l11ll11111_opy_:
                return b345 + b25
            else:
                self.l1l11ll11111_opy_ = True
                return b345 + b256
    def l1l11l1111ll_opy_(self, l1lll1l1l11_opy_):
        return "".join([b0, l1l1lll1l11l_opy_[l1lll1l1l11_opy_], b0])
    def l1l1l11l1l1l_opy_(self, l1l1l11111_opy_, l1111lll11_opy_, l11lllll1l_opy_):
        l1l11ll1l1ll_opy_ = ""
        for char in l1l1l11111_opy_:
            l1l11ll1l1ll_opy_ += numeral_to_braille_high(char)
        l1l1l11ll111_opy_ = ""
        for char in l1111lll11_opy_:
            l1l1l11ll111_opy_ += numeral_to_braille_low(char)
        braille = "".join([NumeralPrefix, l1l11ll1l1ll_opy_, l1l1l11ll111_opy_, b0])
        if l11lllll1l_opy_ == "common":
            braille = "".join([b46, b14, b0])
        if l11lllll1l_opy_ == "cut":
            braille = "".join([b456, b14, b0])
        return braille
    def l1l1lll111l1_opy_(self, l11111l111_opy_, l1l11lllll_opy_, l111111ll1_opy_):
        self._1l11lllll11_opy_ = l11111l111_opy_
        self._1l1ll1111ll_opy_ = l1l11lllll_opy_
        self._1l11l1l1l1l_opy_ = l111111ll1_opy_
        if self._1l11lllll11_opy_ == "eighth":
            self._1l1ll111ll1_opy_ = b145
        elif self._1l11lllll11_opy_ == "quarter":
            self._1l1ll111ll1_opy_ = b1456
        elif self._1l11lllll11_opy_ == "half":
            self._1l1ll111ll1_opy_ = b1345
        elif self._1l11lllll11_opy_ == "whole":
            self._1l1ll111ll1_opy_ = b13456
        else:
            self._1l1ll111ll1_opy_ = b1345 + b135
        if self._1l1ll1111ll_opy_:
            self._1l1lll1111l_opy_ = b3
        else:
            self._1l1lll1111l_opy_ = ""
        self._1l11l1ll1ll_opy_ = ""
        for char in self._1l11l1l1l1l_opy_:
            self._1l11l1ll1ll_opy_ += numeral_to_braille_high(char)
        self._1l11ll111l1_opy_ = "".join([b0, self._1l1ll111ll1_opy_, self._1l1lll1111l_opy_, b2356, NumeralPrefix, self._1l11l1ll1ll_opy_, b0])
        return self._1l11ll111l1_opy_
    def l1l11lll11l1_opy_(self, l111111ll1_opy_):
        l1l1l1l1l1l1_opy_ = round(float(l111111ll1_opy_))
        l1l11ll11l1l_opy_ = str(l1l1l1l1l1l1_opy_)
        l1l1l1111lll_opy_ = ""
        for char in l1l11ll11l1l_opy_:
            l1l1l1111lll_opy_ += numeral_to_braille_high(char)
        braille = "".join([b0, b1456, b2356, b6, NumeralPrefix, l1l1l1111lll_opy_, b0])
        return braille
    def l1l1ll1lll11_opy_(self, l1ll1llll111_opy_, l1l11l1lllll_opy_):
        l1l1ll1ll1ll_opy_ = b0
        l1l1l1l1l111_opy_ = b2356
        for char in str(l1ll1llll111_opy_):
            l1l1l1l1l111_opy_ += numeral_to_braille_high(char)
        l1l1l1l1l111_opy_ += b2356 + b0
        if ((self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] in ['edit', 'listen'] and l1l11l1lllll_opy_) or (self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measure_b123'] and l1l11l1lllll_opy_)) and not self.l1l11llll1ll_opy_:
            l1l1ll1ll1ll_opy_ += b123 + b0
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measure_number'] and l1ll1llll111_opy_ % int(self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measure_every']) == 0:
            l1l1ll1ll1ll_opy_ += l1l1l1l1l111_opy_
        if self.l1l11llll1ll_opy_:
            self.l1l1l1lllll1_opy_ += 1
            if self.l1l1l1lllll1_opy_ == self._1l11lll11ll_opy_:
                self.l1l11llll1ll_opy_ = False
        return l1l1ll1ll1ll_opy_
    def l1l11l11ll1l_opy_(self, interval):
        return l1l1lll1l1ll_opy_[interval]
    def l1l1l1ll1l1l_opy_(self, l1l1l1l1ll11_opy_):
        if l1l1l1l1ll11_opy_.location == "left" and l1l1l1l1ll11_opy_.l1llll1111l1_opy_ == "1" and l1l1l1l1ll11_opy_.l1llll11ll11_opy_ == "start":
            return b3456 + b2
        if l1l1l1l1ll11_opy_.location == "left" and l1l1l1l1ll11_opy_.l1llll1111l1_opy_ == "2" and l1l1l1l1ll11_opy_.l1llll11ll11_opy_ == "start":
            return b3456 + b23
        if l1l1l1l1ll11_opy_.location == "left" and l1l1l1l1ll11_opy_.l1llll1111l1_opy_ == "3" and l1l1l1l1ll11_opy_.l1llll11ll11_opy_ == "start":
            return b3456 + b25
        if l1l1l1l1ll11_opy_.location == "left" and l1l1l1l1ll11_opy_.l1llll1111l1_opy_ == "4" and l1l1l1l1ll11_opy_.l1llll11ll11_opy_ == "start":
            return b3456 + b256
        if l1l1l1l1ll11_opy_.location == "left" and l1l1l1l1ll11_opy_.l11ll1lll1_opy_ == "heavy-light" and l1l1l1l1ll11_opy_.l1l111l1ll_opy_ == "forward":
            return b126 + b2356
        if l1l1l1l1ll11_opy_.location == "right" and l1l1l1l1ll11_opy_.l11ll1lll1_opy_ == "light-heavy" and l1l1l1l1ll11_opy_.l1lll1ll111l_opy_ and l1l1l1l1ll11_opy_.l1l111l1ll_opy_ == "backward":
            return b126 + b23
        if l1l1l1l1ll11_opy_.l11ll1lll1_opy_ == "light-light":
            return b126 + b13 + b3
        if l1l1l1l1ll11_opy_.l11ll1lll1_opy_ == "regular":
            return b0 + b123
        return b126 + b13
    def l1lllll1ll1_opy_(self, sign, line, l1lllll1111_opy_, l11111ll11_opy_, l1l1l11l111l_opy_):
        l1l1l11ll11l_opy_ = l1l1llll1111_opy_[sign]
        l1l11l1l111l_opy_ = l1l1llll111l_opy_[line]
        if ((sign == "G" and line == "2") or (sign == "F" and line == "4") or (sign == "C" and line == "4")) and l1l1l11l111l_opy_ not in ["double", "double-hand"]:
            l1l11l1l111l_opy_ = ""
        l1l1ll11l111_opy_ = l1l1lll1ll1l_opy_[l1lllll1111_opy_]
        if l1l1l11l111l_opy_ in ["no", "double"]:
            l1l11ll1ll11_opy_ = b123
        else:
            l1l11ll1ll11_opy_ = b13
        l1l11ll11ll1_opy_ = "".join([b345, l1l1l11ll11l_opy_, l1l11l1l111l_opy_, l1l11ll1ll11_opy_])
        l1lllll1ll1_opy_ = "".join([b0, l1l11ll11ll1_opy_, l1l1ll11l111_opy_, b0])
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['clef']:
            return l1lllll1ll1_opy_
        else:
            return ""
    def l1l11lll1lll_opy_(self, words):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['words']:
            l1l1l1llll1l_opy_ = words.strip()
            return "".join([b0, b345, b345, self.l1ll111ll1ll_opy_(l1l1l1llll1l_opy_), b3, b0])
        else:
            return ""
    def l1l1l1l1l11l_opy_(self, l1llll1ll11_opy_, l111lll111_opy_):
        l1l1ll1l1l1l_opy_ = {
            "title": "".join([b56, b23, b23, b14, b2345]),
            "subtitle": "".join([b56, b23, b23, b14, b234]),
            "composer": "".join([b56, b23, b23, b14, b14]),
            "lyricist": "".join([b56, b23, b23, b14, b123]),
            "arranger": "".join([b56, b23, b23, b14, b1]),
            "rights": "".join([b56, b23, b23, b14, b1235]),
            "no": "".join([b56, b23, b23, b14, b2456])
        }
        l1l1l1lll1ll_opy_ = l1l1ll1l1l1l_opy_.get(l111lll111_opy_, "")
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['credit_words']:
            l1l11l1ll11l_opy_ = l1llll1ll11_opy_.strip()
            return l1l1l1lll1ll_opy_ + b25 + self.l1ll111ll1ll_opy_(l1l11l1ll11l_opy_)
        else:
            return ""
    def l1l1l1lll11l_opy_(self, title):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['credit_words']:
            l1l1l1llll11_opy_ = title.strip()
            return "".join([b56, b23, b23, b2456, b2345, b25, self.l1ll111ll1ll_opy_(l1l1l1llll11_opy_)])
        else:
            return ""
    def l1l11l1l11l1_opy_(self, l1ll1llll111_opy_):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['credit_words']:
            l1l11ll1l111_opy_ = l1ll1llll111_opy_.strip()
            return "".join([b56, b23, b23, b2456, b1345, b25, self.l1ll111ll1ll_opy_(l1l11ll1l111_opy_)])
        else:
            return ""
    def l1l1l11l1lll_opy_(self, l111l1l11l_opy_):
        if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['karaoke'] and l111l1l11l_opy_ != "":
            return "".join([b0, b56, b23, b23, b13, self.l1ll111ll1ll_opy_(l111l1l11l_opy_), b0])
        else:
            return ""
    def l1l1l1ll11ll_opy_(self, l1l11ll111ll_opy_, l11ll11l11_opy_):
        return "".join([b56, b23, b3, b134, b1234, b36, self.l1ll111ll1ll_opy_(l1l11ll111ll_opy_), b25, self.l1ll111ll1ll_opy_(l11ll11l11_opy_)])
    def l1l11ll1l1l1_opy_(self, l1l11ll111ll_opy_, l111ll11ll_opy_):
        return "".join([b56, b23, b3, b134, b14, b36, self.l1ll111ll1ll_opy_(l1l11ll111ll_opy_), b25, self.l1ll111ll1ll_opy_(l111ll11ll_opy_)])
    def l1l1l1ll1ll1_opy_(self, l1l11ll111ll_opy_, l1lllll1lll_opy_):
        return "".join([b56, b23, b3, b134, b1236, b36, self.l1ll111ll1ll_opy_(l1l11ll111ll_opy_), b25, self.l1ll111ll1ll_opy_(l1lllll1lll_opy_)])
    def l1l1l111ll11_opy_(self, element, l11lll111l_opy_):
        l1ll1l1111l1_opy_ = ""
        if l11lll111l_opy_ != 0:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b145, b24, b36, self.l1ll111ll1ll_opy_(element.l111lll1ll_opy_), b25, self.l1ll111ll1ll_opy_(l11lll111l_opy_)])
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b145, b24, b36, self.l1ll111ll1ll_opy_(element.l11111ll1l_opy_), b25, self.l1ll111ll1ll_opy_(l11lll111l_opy_)])
            return l1ll1l1111l1_opy_
        else:
            return ""
    def l1l11llllll1_opy_(self, element, l111111111_opy_):
        l1ll1l1111l1_opy_ = ""
        if l111111111_opy_ !=0:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b14, b125, b36, self.l1ll111ll1ll_opy_(element.l111lll1ll_opy_), b25, self.l1ll111ll1ll_opy_(l111111111_opy_)])
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b14, b125, b36, self.l1ll111ll1ll_opy_(element.l11111ll1l_opy_), b25, self.l1ll111ll1ll_opy_(l111111111_opy_)])
            return l1ll1l1111l1_opy_
        else:
            return ""
    def l1l1l1ll1l11_opy_(self, element, l1lll1llll1_opy_):
        l1ll1l1111l1_opy_ = ""
        if l1lll1llll1_opy_ !=0:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b135, b14, b36, self.l1ll111ll1ll_opy_(element.l111lll1ll_opy_), b25, self.l1ll111ll1ll_opy_(l1lll1llll1_opy_)])
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b135, b14, b36, self.l1ll111ll1ll_opy_(element.l11111ll1l_opy_), b25, self.l1ll111ll1ll_opy_(l1lll1llll1_opy_)])
            return l1ll1l1111l1_opy_
        else:
            return ""
    def l1l11l1l11ll_opy_(self, element, l1111l11l1_opy_, l1lllllll1l_opy_):
        l1ll1l1111l1_opy_ = ""
        if l1111l11l1_opy_:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'name':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b145, b135, b36, self.l1ll111ll1ll_opy_(element.l111lll1ll_opy_), b25])
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]["parts"] == 'abbreviation':
                l1ll1l1111l1_opy_ = "".join([b56, b23, b3, b2345, b1235, b145, b135, b36, self.l1ll111ll1ll_opy_(element.l11111ll1l_opy_), b25])
            if l1lllllll1l_opy_ != "":
                l1ll1l1111l1_opy_ += self.l1ll111ll1ll_opy_(l1lllllll1l_opy_)
            return l1ll1l1111l1_opy_
        else:
            return ""
    def l1l1l1l111l1_opy_(self, l1ll1llll111_opy_):
        l1l1l11llll1_opy_ = ""
        for char in l1ll1llll111_opy_:
            l1l1ll11lll1_opy_ = numeral_to_braille_high((char))
            l1l1l11llll1_opy_ += l1l1ll11lll1_opy_
        return "".join([b3456, l1l1l11llll1_opy_, b134])
    def l1l1ll1ll11l_opy_(self, l1ll1llll111_opy_):
        if l1ll1llll111_opy_ == "1":
            return b2356
        else:
            l1l1l11llll1_opy_ = ""
            for char in l1ll1llll111_opy_:
                l1l1ll11lll1_opy_ = numeral_to_braille_high((char))
                l1l1l11llll1_opy_ += l1l1ll11lll1_opy_
            return "".join([b3456, l1l1l11llll1_opy_])
    def l1l1l1l11l1l_opy_(self, list, l1l1ll1lll1l_opy_):
        l = len(list)
        r = int(l / l1l1ll1lll1l_opy_) + (l % l1l1ll1lll1l_opy_ > 0)
        return [list[k * l1l1ll1lll1l_opy_: (k + 1) * l1l1ll1lll1l_opy_] for k in range(r)]
    def l1l11ll1lll1_opy_(self, l1ll1l1ll1l1_opy_, values):
        l1l1ll11l1l1_opy_ = list()
        first = 0
        values.append(len(l1ll1l1ll1l1_opy_) + 1)
        for k in values:
            l1l1ll11l1l1_opy_.append(l1ll1l1ll1l1_opy_[first:k - 1])
            first = k - 1
        return l1l1ll11l1l1_opy_
    def l1l11l11ll11_opy_(self, l1l1ll1l1111_opy_):
        empty = True
        l1l11l1l111l_opy_ = "".join([b56, b23, b23, b13456])
        for l111111l1l_opy_ in l1l1ll1l1111_opy_:
            index = 0
            empty = True
            for item in l111111l1l_opy_[3]:
                if l111111l1l_opy_[3][index] != "":
                    if empty:
                        l1l11l1l111l_opy_ += l111111l1l_opy_[3][index]
                    else:
                        l1l11l1l111l_opy_ += b36 + l111111l1l_opy_[3][index]
                    empty = False
                index += 1
            l1l11l1l111l_opy_ += b0
        self._11lllll1_opy_(l1l11l1l111l_opy_)
        if not empty:
            self._1l1111ll_opy_(l1l11l1l111l_opy_)
    def l1l1l11l1l11_opy_(self, element, l1l1ll1111l1_opy_):
        for l1l1ll1l1111_opy_ in l1l1ll1111l1_opy_:
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['lyrics'] == 'before_each_section':
                self.l1l11l11ll11_opy_(l1l1ll1l1111_opy_)
            if self._1l11lll11ll_opy_ == 1:
                l1l11l1l111l_opy_ = self.l1l1lll11l1l_opy_(element)
            else:
                l1l11l1l111l_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br1")])
            for l111111l1l_opy_ in l1l1ll1l1111_opy_:
                index = 0
                for item in l111111l1l_opy_[0]:
                    l1l11l1l111l_opy_ += l111111l1l_opy_[0][index]
                    index += 1
            self._11lllll1_opy_(l1l11l1l111l_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l11l1l111l_opy_)
            if self._1l11lll11ll_opy_ >= 2:
                l1l11l1l111l_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br2")])
                for l111111l1l_opy_ in l1l1ll1l1111_opy_:
                    index = 0
                    for item in l111111l1l_opy_[1]:
                        l1l11l1l111l_opy_ += l111111l1l_opy_[1][index]
                        index += 1
                self._11lllll1_opy_(l1l11l1l111l_opy_)
                if self._1l1111ll_opy_:
                    self._1l1111ll_opy_(l1l11l1l111l_opy_)
            if self._1l11lll11ll_opy_ >= 3:
                l1l11l1l111l_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br3")])
                for l111111l1l_opy_ in l1l1ll1l1111_opy_:
                    index = 0
                    for item in l111111l1l_opy_[2]:
                        l1l11l1l111l_opy_ += l111111l1l_opy_[1][index]
                        index += 1
                self._11lllll1_opy_(l1l11l1l111l_opy_)
                if self._1l1111ll_opy_:
                    self._1l1111ll_opy_(l1l11l1l111l_opy_)
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['lyrics'] == 'after_each_section':
                self.l1l11l11ll11_opy_(l1l1ll1l1111_opy_)
    def l111111llll_opy_(self):
        self._11lllll1_opy_("\nmodel to braille")
        def l1l11l1ll_opy_(braille="", l11111ll11_opy_=1):
            if self.l1l1l1llllll_opy_:
                if l11111ll11_opy_ == 1:
                    l1l1l111l111_opy_.append(braille)
                elif l11111ll11_opy_ == 2:
                    l1l1ll1l11ll_opy_.append(braille)
                elif l11111ll11_opy_ == 3:
                    l1l1ll11111l_opy_.append(braille)
                elif l11111ll11_opy_ == 0:
                    self.l1l1l11111ll_opy_.append(braille)
        def l1l1l1l111ll_opy_(l1l1ll1l11l1_opy_):
            if self._1l11lll11ll_opy_ == 1:
                l1l1ll1l1lll_opy_ = self.l1l1lll11l1l_opy_(element)
            else:
                l1l1ll1l1lll_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br1")])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[0]:
                    l1l1ll1l1lll_opy_ += l111111l1l_opy_[0][index]
                    index +=1
            self._11lllll1_opy_(l1l1ll1l1lll_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1ll1l1lll_opy_)
            l1l1l111lll1_opy_ = ""
            if self._1l11lll11ll_opy_ >= 2:
                l1l1l111lll1_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br2")])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[1]:
                    l1l1l111lll1_opy_ += l111111l1l_opy_[1][index]
                    index +=1
            self._11lllll1_opy_(l1l1l111lll1_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1l111lll1_opy_)
            l1l1l111111l_opy_ = ""
            if self._1l11lll11ll_opy_ >= 3:
                l1l1l111111l_opy_ = "".join([self.l1l1lll11l1l_opy_(element), self.l1ll111ll1ll_opy_("-br3")])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[2]:
                    l1l1l111111l_opy_ += l111111l1l_opy_[1][index]
                    index +=1
            self._11lllll1_opy_(l1l1l111111l_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1l111111l_opy_)
        def l1l11l1lll1l_opy_(l1l1ll1l11l1_opy_, l1lll11lll11_opy_):
            if self._1l11lll11ll_opy_ == 1:
                l1l1ll1l1lll_opy_ = self.l1l1l111llll_opy_(l1lll11lll11_opy_)
            else:
                l1l1ll1l1lll_opy_ = "".join([self.l1l1l111llll_opy_(l1lll11lll11_opy_), b36, b16])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[0]:
                    l1l1ll1l1lll_opy_ += l111111l1l_opy_[0][index]
                    index +=1
            self._11lllll1_opy_(l1l1ll1l1lll_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1ll1l1lll_opy_)
            l1l1l111lll1_opy_ = ""
            if self._1l11lll11ll_opy_ >= 2:
                l1l1l111lll1_opy_ = "".join([self.l1l1l111llll_opy_(l1lll11lll11_opy_), b36, b126])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[1]:
                    l1l1l111lll1_opy_ += l111111l1l_opy_[1][index]
                    index +=1
            self._11lllll1_opy_(l1l1l111lll1_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1l111lll1_opy_)
            l1l1l111111l_opy_ = ""
            if self._1l11lll11ll_opy_ >= 3:
                l1l1l111111l_opy_ = "".join([self.l1l1l111llll_opy_(l1lll11lll11_opy_), b36, b146])
            for l111111l1l_opy_ in l1l1ll1l11l1_opy_:
                index = 0
                for item in l111111l1l_opy_[2]:
                    l1l1l111111l_opy_ += l111111l1l_opy_[1][index]
                    index +=1
            self._11lllll1_opy_(l1l1l111111l_opy_)
            if self._1l1111ll_opy_:
                self._1l1111ll_opy_(l1l1l111111l_opy_)
        def l1l11lll1l1l_opy_():
            index = 0
            for item in self.l1l1l11111ll_opy_:
                self._11lllll1_opy_(item)
                if self._1l1111ll_opy_:
                    self._1l1111ll_opy_(item)
                index +=1
            self.l1l1l11111ll_opy_.clear()
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] in ['edit', 'listen']:
                l1l1l1l111ll_opy_(l1l1ll1l11l1_opy_)
            else:
                if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] == 'system':
                    l1l1ll1l1ll1_opy_ = self.l1l11ll1lll1_opy_(l1l1ll1l11l1_opy_, l1111l11ll_opy_)
                    self.l1l1l11l1l11_opy_(element, l1l1ll1l1ll1_opy_)
                elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] == 'total_part':
                    l1l1l1l111ll_opy_(l1l1ll1l11l1_opy_)
                else:
                    l1l1ll1111l1_opy_ = self.l1l1l1l11l1l_opy_(l1l1ll1l11l1_opy_, int(self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measures_per_section']))
                    self.l1l1l11l1l11_opy_(element, l1l1ll1111l1_opy_)
        def l1l11l111ll1_opy_():
            index = 0
            for item in self.l1l1l11111ll_opy_:
                self._11lllll1_opy_(item)
                if self._1l1111ll_opy_:
                    self._1l1111ll_opy_(item)
                index +=1
            self.l1l1l11111ll_opy_.clear()
            try:
                l1l1l11l1111_opy_ = len(self.l1l1ll1ll1l1_opy_[0][0])
            except:
                l1l1l11l1111_opy_ = -1
            if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] == 'number':
                l1ll111l1lll_opy_ = 0
                l1l1l1l11111_opy_ = list()
                while l1ll111l1lll_opy_ < l1l1l11l1111_opy_:
                    l1lll11lll11_opy_ = 0
                    for part in self.l1l1ll1ll1l1_opy_:
                        self._1l11lll11ll_opy_ = part[2]
                        for l111111l1l_opy_ in part[0][l1ll111l1lll_opy_:min(l1ll111l1lll_opy_+int(self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measures_per_section']),len(part[0]))]:
                            l1l1l1l11111_opy_.append(l111111l1l_opy_)
                        l1l11l1lll1l_opy_(l1l1l1l11111_opy_, l1lll11lll11_opy_)
                        l1l1l1l11111_opy_.clear()
                        l1lll11lll11_opy_ += 1
                    l1ll111l1lll_opy_ += int(self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['measures_per_section'])
            elif self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] == 'system':
                l1l1l1l1111l_opy_ = list()
                for part in self.l1l1ll1ll1l1_opy_:
                    for system in part[1]:
                        l1l1l1l1111l_opy_.append(system - 1)
                l1l1ll11l1ll_opy_ = sorted(l1l1l1l1111l_opy_)
                l1l1ll11l11l_opy_ = list()
                for i in l1l1ll11l1ll_opy_:
                    if i not in l1l1ll11l11l_opy_:
                        l1l1ll11l11l_opy_.append(i)
                l1l1ll11l11l_opy_.append(l1l1l11l1111_opy_)
                l1ll111l1lll_opy_ = 0
                l1l1l1l11111_opy_ = list()
                l1l11l1llll1_opy_ = 0
                for system in l1l1ll11l11l_opy_:
                    l1lll11lll11_opy_ = 0
                    for part in self.l1l1ll1ll1l1_opy_:
                        self._1l11lll11ll_opy_ = part[2]
                        for l111111l1l_opy_ in part[0][l1ll111l1lll_opy_:min(l1ll111l1lll_opy_+system - l1l11l1llll1_opy_, len(part[0]))]:
                            l1l1l1l11111_opy_.append(l111111l1l_opy_)
                        l1l11l1lll1l_opy_(l1l1l1l11111_opy_, l1lll11lll11_opy_)
                        l1l1l1l11111_opy_.clear()
                        l1lll11lll11_opy_ += 1
                    l1ll111l1lll_opy_ += system - l1l11l1llll1_opy_
                    l1l11l1llll1_opy_ = system
        l1l1l1l11ll1_opy_ = True
        l1l1ll111l1l_opy_ = 0 # for groups of l1ll1l111111_opy_
        self.l1l11lll111l_opy_ = False # l1ll11l11lll_opy_ for l1ll1llll11l_opy_-l1111111ll_opy_ in a part, insert a sign for l1l11ll1ll1l_opy_ l1l11lllll1l_opy_
        self._1l11lll11ll_opy_ = 1
        l1lll1l1l11_opy_ = 0
        l1l1l11lll1l_opy_ = 0
        l1l1l1111ll1_opy_ = ""
        l1l11lll1ll1_opy_ = ""
        l1l1l1l1llll_opy_ = ""
        l1llllll1ll_opy_ = False
        l1l1ll11ll1l_opy_ = False # l1ll11l11lll_opy_ for braille l1l11111ll_opy_ which l1l1l11111l1_opy_ of the first note of the l1lll1l11l1_opy_ for l1l11l111lll_opy_
        l1l1l1111l1l_opy_ = False # l1ll11l11lll_opy_ for braille l1l11111ll_opy_ which l1l1l11111l1_opy_ of the first note of the l1lll1l11l1_opy_ for l1l1l111ll1l_opy_
        l1l11llll1l1_opy_ = False # l1ll11l11lll_opy_ for braille l1l11111ll_opy_ which l1l1l11111l1_opy_ of the first note of the l1lll1l11l1_opy_ for l1l11l11l1l1_opy_
        self.l1l11ll11111_opy_ = True # l1ll11l11lll_opy_ to l1l1l1l1ll1l_opy_ the l1l1l111l1ll_opy_ end of l1111l1l111_opy_ b345 + b25 for end l1l1ll1llll1_opy_, b345 + b256 for end l1l1l11ll1ll_opy_
        l1l11l1l1111_opy_ = True
        self.l1l11llll1ll_opy_ = True
        self.l1l1l11111ll_opy_ = list()
        self.l1l1l111l11l_opy_ = list()
        self.l1l1ll111lll_opy_ = list()
        self.l1l1ll1ll1l1_opy_ = list()
        self._1ll111111ll_opy_ = self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['ascending_chords']
        self._1l11ll1llll_opy_ = list()
        self.l1l1l1llllll_opy_ = True
        l1l1lll11111_opy_ = list()
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part":
                self._1l11lll11ll_opy_ = 1
                for l111111l1l_opy_ in element.l11l1l1ll1_opy_:
                    for event in l111111l1l_opy_.l111l11lll_opy_:
                        if event.t == "attributes":
                            for l11lllll11_opy_ in event.l11l111ll1_opy_:
                                if l11lllll11_opy_.t == "staves":
                                    self._1l11lll11ll_opy_ = int(l11lllll11_opy_.l1111111ll_opy_)
                        if event.t == "note":
                            if event.l11111ll11_opy_ > self._1l11lll11ll_opy_:
                                self._1l11lll11ll_opy_ = event.l11111ll11_opy_
                l1l1lll11111_opy_.append([element.l111l1l1ll_opy_, element.l111lll1ll_opy_, element.l11111ll1l_opy_, self._1l11lll11ll_opy_])
        self._11lllll1_opy_("braille_sub_parts " + str(l1l1lll11111_opy_))
        l1l11ll11l11_opy_ = list()
        for part in l1l1lll11111_opy_:
            if part[3] == 1:
                l1l11ll11l11_opy_.append([part[0], part[0], part[1], part[1], part[2], part[2], 1, "no", "no", "no", "no"])
            else:
                l1l11ll11l11_opy_.append([part[0], part[0] + "-br1", part[1], part[1] + "-br1", part[2], part[2] + "-br1", part[3], "no", "no", "no", "no"])
            if part[3] >= 2:
                l1l11ll11l11_opy_.append([part[0], part[0] + "-br2", part[1], part[1] + "-br2", part[2], part[2] + "-br2", 2, "no", "no", "no", "no"])
            if part[3] >= 3:
                l1l11ll11l11_opy_.append([part[0], part[0] + "-br3", part[1], part[1] + "-br3", part[2], part[2] + "-br3", 3, "no", "no", "no", "no"])
        l1l11l11llll_opy_ = 0
        l1ll1l11lll1_opy_ = 0
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "braille-global":
                l11l1111l1l_opy_ = ""
                for event in element.l11l1l1lll_opy_:
                    if event.t == "global-key":
                        l1lll1l1l11_opy_ = event.l1lll1l1l11_opy_
                        l1l1l11lll1l_opy_ = event.l1lll1l1l11_opy_
                        l11l1111l1l_opy_ += self.l1l11l1111ll_opy_(event.l1lll1l1l11_opy_)
                    elif event.t == "global-time":
                        l1l1l11111_opy_ = event.l1l1l11111_opy_
                        l1l1l1111ll1_opy_ = event.l1l1l11111_opy_
                        l1l11lll1ll1_opy_ = event.l1111lll11_opy_
                        l1l1l1l1llll_opy_ =event.l11lllll1l_opy_
                        l11l1111l1l_opy_ += self.l1l1l11l1l1l_opy_(event.l1l1l11111_opy_, event.l1111lll11_opy_, event.l11lllll1l_opy_)
                if l11l1111l1l_opy_ != "":
                    l1l11l1ll_opy_(l11l1111l1l_opy_, 0)
            if element.t == "credit":
                l1l11l1ll_opy_(self.l1l1l1l1l11l_opy_(element.l1llll1ll11_opy_, element.l111lll111_opy_), 0)
            if element.t == "work":
                if element.l1lll1lll1ll_opy_ != "no":
                    l1l11l1ll_opy_(self.l1l11l1l11l1_opy_(element.l1lll1lll1ll_opy_), 0)
                if element.l1llll11l11l_opy_ != "no":
                    l1l11l1ll_opy_(self.l1l1l1lll11l_opy_(element.l1llll11l11l_opy_), 0)
            if element.t == "part-list":
                l1l11lllllll_opy_ = 0
                for item in element.l111l1l1l1_opy_:
                    l1l11lllllll_opy_ += 1
                    self._1l11ll1llll_opy_.append(item.l1lll111lll_opy_)
                    for info in l1l11ll11l11_opy_:
                        if info[0] == item.l111l1l1ll_opy_:
                            info[7] = item.l1lll111lll_opy_
                    if item.l11ll11l11_opy_ != "no":
                        for info in l1l11ll11l11_opy_:
                            if info[0] == item.l111l1l1ll_opy_:
                                info[8] = item.l11ll11l11_opy_
                        for part in l1l1lll11111_opy_:
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 1:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll11ll_opy_(self.l1lll1111l11_opy_(item), item.l11ll11l11_opy_)])
                            elif part[0] == item.l111l1l1ll_opy_ and part[3] >= 2:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll11ll_opy_(self.l1lll1111l11_opy_(item) + "-br1", item.l11ll11l11_opy_)])
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll11ll_opy_(self.l1lll1111l11_opy_(item) + "-br2", item.l11ll11l11_opy_)])
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 3:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll11ll_opy_(self.l1lll1111l11_opy_(item) + "-br3", item.l11ll11l11_opy_)])
                    if item.l111ll11ll_opy_ != "no":
                        for info in l1l11ll11l11_opy_:
                            if info[0] == item.l111l1l1ll_opy_:
                                info[9] = item.l111ll11ll_opy_
                        for part in l1l1lll11111_opy_:
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 1:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l11ll1l1l1_opy_(self.l1lll1111l11_opy_(item), item.l111ll11ll_opy_)])
                            elif part[0] == item.l111l1l1ll_opy_ and part[3] >= 2:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l11ll1l1l1_opy_(self.l1lll1111l11_opy_(item) + "-br1", item.l111ll11ll_opy_)])
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l11ll1l1l1_opy_(self.l1lll1111l11_opy_(item) + "-br2", item.l111ll11ll_opy_)])
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 3:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l11ll1l1l1_opy_(self.l1lll1111l11_opy_(item) + "-br3", item.l111ll11ll_opy_)])
                    if item.l1lllll1lll_opy_ != "no":
                        for info in l1l11ll11l11_opy_:
                            if info[0] == item.l111l1l1ll_opy_:
                                info[10] = item.l1lllll1lll_opy_
                        for part in l1l1lll11111_opy_:
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 1:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll1ll1_opy_(self.l1lll1111l11_opy_(item), item.l1lllll1lll_opy_)])
                            elif part[0] == item.l111l1l1ll_opy_ and part[3] >= 2:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll1ll1_opy_(self.l1lll1111l11_opy_(item) + "-br1", item.l1lllll1lll_opy_)])
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll1ll1_opy_(self.l1lll1111l11_opy_(item) + "-br2", item.l1lllll1lll_opy_)])
                            if part[0] == item.l111l1l1ll_opy_ and part[3] == 3:
                                self.l1l1l111l11l_opy_.append([l1l11lllllll_opy_, self.l1l1l1ll1ll1_opy_(self.l1lll1111l11_opy_(item) + "-br3", item.l1lllll1lll_opy_)])
                self.l1l1l11l1ll1_opy_ = False
                for part in self._1l11ll1llll_opy_:
                    if part != self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['ascending_chords']:
                        self.l1l1l11l1ll1_opy_ = True
            if element.t == "part":
                l1ll1l11lll1_opy_ += 1
                self._1l11lll11ll_opy_ = l1l1lll11111_opy_ [l1l11l11llll_opy_][3]
                if self._1l11lll11ll_opy_ >= 2:
                    self.l1l11lll111l_opy_ = True
                l1l1ll1lllll_opy_ = - 1
                l1l11ll11lll_opy_ = - 7
                l1l1l11l11l1_opy_ = - 1
                l1l11l1l1l11_opy_ = - 7
                l1l11lll1l11_opy_ = - 1
                l1l1l11l11ll_opy_ = - 7
                l1l11l1l1111_opy_ = True
                self.l1l11llll1ll_opy_ = True
                self.l1l1l1lllll1_opy_ = 0
                l1l1l1l11l11_opy_ = False
                l1l1ll1l11l1_opy_ = list()
                l1111l11ll_opy_ = list()
                if self._1l11ll1llll_opy_[l1l11l11llll_opy_] == "1":
                    self._1ll111111ll_opy_ = True
                elif self._1l11ll1llll_opy_[l1l11l11llll_opy_] == "-1":
                    self._1ll111111ll_opy_ = False
                for l111111l1l_opy_ in element.l11l1l1ll1_opy_:
                    l1l1l111l111_opy_ = list()
                    l1l1ll1l11ll_opy_ = list()
                    l1l1ll11111l_opy_ = list()
                    self.l1l1l1l1lll1_opy_ = list()
                    l1ll111lllll_opy_ = list()
                    if self.l1l11lll111l_opy_:
                        l1l11l1ll_opy_("".join([b0, b46, b46, b345, b0]), 1)
                        l1l11l1ll_opy_("".join([b0, b456, b456, b345, b0]), 2)
                        if self._1l11lll11ll_opy_ >= 3:
                            l1l11l1ll_opy_("".join([b0, b456, b456, b345, b0]), 3)
                    if self.l1l1l11l1ll1_opy_ and self.l1l11llll1ll_opy_ and element.l111lll1ll_opy_ not in ["Br Piano right hand", "Br Piano left hand", "Br Piano solo", "Bru Piano right hand", "Brd Piano left hand", "Br Organ pedal"]:
                        if self._1l11ll1llll_opy_[l1l11l11llll_opy_] == "1":
                            l1l11l1ll_opy_("".join([b0, b456, b456, b345, b0]), 1)
                        elif self._1l11ll1llll_opy_[l1l11l11llll_opy_] == "-1":
                            l1l11l1ll_opy_("".join([b0, b46, b46, b345, b0]), 1)
                    l1l11l1ll_opy_(self.l1l1ll1lll11_opy_(l111111l1l_opy_.l1lll111l11_opy_, l1l11l1l1111_opy_), 1)
                    if self._1l11lll11ll_opy_ >= 2:
                        l1l11l1ll_opy_(self.l1l1ll1lll11_opy_(l111111l1l_opy_.l1lll111l11_opy_, l1l11l1l1111_opy_), 2)
                    if self._1l11lll11ll_opy_ >= 3:
                        l1l11l1ll_opy_(self.l1l1ll1lll11_opy_(l111111l1l_opy_.l1lll111l11_opy_, l1l11l1l1111_opy_), 3)
                    l1l11l1l1111_opy_ = True
                    if l1l1l1l11l11_opy_:
                        try:
                            l1l1ll1lllll_opy_ = - 1
                            l1l11ll11lll_opy_ = - 7
                            l1l1l11l11l1_opy_ = - 1
                            l1l11l1l1l11_opy_ = - 7
                            l1l11lll1l11_opy_ = - 1
                            l1l1l11l11ll_opy_ = - 7
                            l1l1l1l11l11_opy_ = False
                        except:
                            pass
                    for event in l111111l1l_opy_.l111l11lll_opy_:
                        if event.t == "direction":
                            for l11lllll11_opy_ in event.l1lll1111l1_opy_:
                                if l11lllll11_opy_.t == "words":
                                    l1l11l1ll_opy_(self.l1l11lll1lll_opy_(l11lllll11_opy_.words), l11lllll11_opy_.l11111ll11_opy_)
                                elif l11lllll11_opy_.t == "dynamics":
                                    l1l11l1ll_opy_(self.l1l1l1l11lll_opy_(l11lllll11_opy_.l1l11l1ll1_opy_), event.l11111ll11_opy_)
                                    if event.l11111ll11_opy_ == 1:
                                        l1l1ll1lllll_opy_ = - 1
                                        l1l11ll11lll_opy_ = - 7
                                    elif event.l11111ll11_opy_ == 2:
                                        l1l1l11l11l1_opy_ = - 1
                                        l1l11l1l1l11_opy_ = - 7
                                    elif event.l11111ll11_opy_ == 3:
                                        l1l11lll1l11_opy_ = - 1
                                        l1l1l11l11ll_opy_ = - 7
                                elif l11lllll11_opy_.t == "pedal":
                                    l1l11l1ll_opy_(self.l1l1l11lll11_opy_(l11lllll11_opy_.l1l11l1l11_opy_), event.l11111ll11_opy_)
                                elif l11lllll11_opy_.t == "wedge":
                                    l1l11l1ll_opy_(self.l1l1ll1l111l_opy_(l11lllll11_opy_.l11ll11ll1_opy_), event.l11111ll11_opy_)
                                elif l11lllll11_opy_.t == "metronome":
                                    l1l11l1ll_opy_(self.l1l1lll111l1_opy_(l11lllll11_opy_.l11111l111_opy_, l11lllll11_opy_.l1l11lllll_opy_, l11lllll11_opy_.l111111ll1_opy_), event.l11111ll11_opy_)
                                elif l11lllll11_opy_.t == "sound":
                                    if l11lllll11_opy_.l11111l1ll_opy_ != "no":
                                        l1l11l1ll_opy_(self.l1l11lll11l1_opy_(l11lllll11_opy_.l11111l1ll_opy_), event.l11111ll11_opy_)
                        if event.t == "backup" and event.l1llll1l11l1_opy_:
                            l1l11l1ll_opy_(b126 + b345, event.l11111ll11_opy_)
                            if event.l11111ll11_opy_ == 1:
                                l1l1ll1lllll_opy_ = - 1
                                l1l11ll11lll_opy_ = - 7
                            elif event.l11111ll11_opy_ == 2:
                                l1l1l11l11l1_opy_ = - 1
                                l1l11l1l1l11_opy_ = - 7
                            elif event.l11111ll11_opy_ == 3:
                                l1l11lll1l11_opy_ = - 1
                                l1l1l11l11ll_opy_ = - 7
                            l1l1l1l11l11_opy_ = True
                        if event.t == "backup" and not event.l1llll1l11l1_opy_:
                            l1ll111lllll_opy_ = list()
                        if event.t == "attributes":
                            for l11lllll11_opy_ in event.l11l111ll1_opy_:
                                if l11lllll11_opy_.t == "key":
                                    l1lll1l1l11_opy_ = l11lllll11_opy_.l1lll1l1l11_opy_
                                    if l1lll1l1l11_opy_ != l1l1l11lll1l_opy_:
                                        l1l11l1ll_opy_(self.l1l11l1111ll_opy_(l1lll1l1l11_opy_), 1)
                                        if self._1l11lll11ll_opy_ >=2:
                                            l1l11l1ll_opy_(self.l1l11l1111ll_opy_(l1lll1l1l11_opy_), 2)
                                        if self._1l11lll11ll_opy_ >=3:
                                            l1l11l1ll_opy_(self.l1l11l1111ll_opy_(l1lll1l1l11_opy_), 3)
                                elif l11lllll11_opy_.t == "time" and (l11lllll11_opy_.l1l1l11111_opy_ != l1l1l1111ll1_opy_ or l11lllll11_opy_.l1111lll11_opy_ != l1l11lll1ll1_opy_ or l11lllll11_opy_.l11lllll1l_opy_ != l1l1l1l1llll_opy_):
                                    l1l11l1ll_opy_(self.l1l1l11l1l1l_opy_(l11lllll11_opy_.l1l1l11111_opy_, l11lllll11_opy_.l1111lll11_opy_, l11lllll11_opy_.l11lllll1l_opy_), 1)
                                    if self._1l11lll11ll_opy_ >=2:
                                        l1l11l1ll_opy_(self.l1l1l11l1l1l_opy_(l11lllll11_opy_.l1l1l11111_opy_, l11lllll11_opy_.l1111lll11_opy_, l11lllll11_opy_.l11lllll1l_opy_), 2)
                                    if self._1l11lll11ll_opy_ >=3:
                                        l1l11l1ll_opy_(self.l1l1l11l1l1l_opy_(l11lllll11_opy_.l1l1l11111_opy_, l11lllll11_opy_.l1111lll11_opy_, l11lllll11_opy_.l11lllll1l_opy_), 3)
                                elif l11lllll11_opy_.t == "clef":
                                    l1l11l1ll_opy_(self.l1lllll1ll1_opy_(l11lllll11_opy_.sign, l11lllll11_opy_.line, l11lllll11_opy_.l1lllll1111_opy_, l11lllll11_opy_.l1lll1l11l11_opy_, l11lllll11_opy_.l1lllll1ll1_opy_), l11lllll11_opy_.l1lll1l11l11_opy_)
                                elif l11lllll11_opy_.t == "transpose":
                                    self.l1l1l111l11l_opy_.append([l1ll1l11lll1_opy_, self.l1l1l111ll11_opy_(element, l11lllll11_opy_.l11lll111l_opy_)])
                                    self.l1l1l111l11l_opy_.append([l1ll1l11lll1_opy_, self.l1l11llllll1_opy_(element, l11lllll11_opy_.l111111111_opy_)])
                                    self.l1l1l111l11l_opy_.append([l1ll1l11lll1_opy_, self.l1l1l1ll1l11_opy_(element, l11lllll11_opy_.l1lll1llll1_opy_)])
                                    self.l1l1l111l11l_opy_.append([l1ll1l11lll1_opy_, self.l1l11l1l11ll_opy_(element, l11lllll11_opy_.l1111l11l1_opy_, l11lllll11_opy_.l1lllllll1l_opy_)])
                                elif l11lllll11_opy_.t == "measure-style":
                                    if l11lllll11_opy_.l1lll1l111ll_opy_ != "no":
                                        l1l11l1ll_opy_(self.l1l1l1l111l1_opy_(l11lllll11_opy_.l1lll1l111ll_opy_), 1)
                                        if self._1l11lll11ll_opy_ >= 2:
                                            l1l11l1ll_opy_(self.l1l1l1l111l1_opy_(l11lllll11_opy_.l1lll1l111ll_opy_), 2)
                                        if self._1l11lll11ll_opy_ >= 3:
                                            l1l11l1ll_opy_(self.l1l1l1l111l1_opy_(l11lllll11_opy_.l1lll1l111ll_opy_), 3)
                                    if l11lllll11_opy_.l1llll1111ll_opy_ != "no" and l11lllll11_opy_.l1l1ll1lll1_opy_ != "stop":
                                        l1l11l1ll_opy_(self.l1l1ll1ll11l_opy_(l11lllll11_opy_.l1llll1111ll_opy_), 1)
                                        if self._1l11lll11ll_opy_ >= 2:
                                            l1l11l1ll_opy_(self.l1l1ll1ll11l_opy_(l11lllll11_opy_.l1llll1111ll_opy_), 2)
                                        if self._1l11lll11ll_opy_ >= 3:
                                            l1l11l1ll_opy_(self.l1l1ll1ll11l_opy_(l11lllll11_opy_.l1llll1111ll_opy_), 3)
                                        self.l1l1l1llllll_opy_ = False
                                    if l11lllll11_opy_.l1llll1111ll_opy_ != "no" and l11lllll11_opy_.l1l1ll1lll1_opy_ == "stop":
                                        self.l1l1l1llllll_opy_ = True
                                        l1l11l1ll_opy_(self.l1l1ll1lll11_opy_(l111111l1l_opy_.l1lll111l11_opy_, l1l11l1l1111_opy_), 1)
                        if event.t == "barline":
                            l1l11l1ll_opy_(self.l1l1l1ll1l1l_opy_(event), 1)
                            if self._1l11lll11ll_opy_ >=2:
                                l1l11l1ll_opy_(self.l1l1l1ll1l1l_opy_(event), 2)
                            if self._1l11lll11ll_opy_ >=3:
                                l1l11l1ll_opy_(self.l1l1l1ll1l1l_opy_(event), 3)
                            if event.l11ll1lll1_opy_ == "light-light":
                                l1l11l1l1111_opy_ = False
                            l1l1ll1lllll_opy_ = - 1
                            l1l11ll11lll_opy_ = - 7
                            l1l1l11l11l1_opy_ = - 1
                            l1l11l1l1l11_opy_ = - 7
                            l1l11lll1l11_opy_ = - 1
                            l1l1l11l11ll_opy_ = - 7
                        if event.t == "note" and event.l1llllll11l_opy_ == 3 and event.l1lll1lll11_opy_ == 2 and not event.l1lll1l11l1_opy_:
                            l1l1ll111l1l_opy_ +=1
                            if l1l1ll111l1l_opy_ == 1:
                                l1l11l1ll_opy_(b23, event.l11111ll11_opy_)
                            if l1l1ll111l1l_opy_ ==3:
                                l1l1ll111l1l_opy_ -=3
                        if event.t == "note" and event.l1111lll1l_opy_:
                            if event.l11lll1111_opy_ == "yes" or event.l11lll1111_opy_ == False:
                                l1l11l1ll_opy_(b26, event.l11111ll11_opy_)
                            if event.l11lll1111_opy_ == "no":
                                l1l11l1ll_opy_(b5 + b26, event.l11111ll11_opy_)
                        if event.t == "note" and event.l1llll1l1l1_opy_:
                            l1l11l1ll_opy_(self.l1l11l11lll1_opy_(), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1l111l11l_opy_:
                            l1l11l1ll_opy_(self.l1l1l1ll1111_opy_(), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1lll1l1lll_opy_:
                            l1l11l1ll_opy_(self.l1l1l1ll1lll_opy_(), event.l11111ll11_opy_)
                        if event.t == "note" and event.l11llllll1_opy_:
                            l1l11l1ll_opy_(self.l1l1ll1l1l11_opy_(), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1l111l111_opy_:
                            l1l11l1ll_opy_(self.l1l11l11l111_opy_(True, event.l1lll1ll11l_opy_), event.l11111ll11_opy_)
                        if event.t == "note" and event.l111l11l11_opy_:
                            l1l11l1ll_opy_(self.l1l11l11l111_opy_(False, event.l1l11ll1l1_opy_), event.l11111ll11_opy_)
                        if event.t == "note" and event.l11l1ll111_opy_ and event.l1ll1llll11_opy_ == 1:
                            l1l11l1ll_opy_(self.l1l11l1lll11_opy_(False, event.l1lllll11l1_opy_), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1lllllll11_opy_ and event.l1ll1llll11_opy_ == 1:
                            l1l11l1ll_opy_(self.l1l11l1lll11_opy_(True, event.l111l1lll1_opy_), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1ll1llll11_opy_ == 0:
                            if event.l1llll11ll1_opy_ == "natural":
                                l1l11l1ll_opy_(self.l1l11l11l11l_opy_(l1l111l111l_opy_.l1llllllll11_opy_.l1llllllllll_opy_)[1], event.l11111ll11_opy_)
                            if (event.step, event.l11lll11ll_opy_) not in l1l1lll11ll1_opy_[l1lll1l1l11_opy_] and (event.step, event.l11lll11ll_opy_) not in l1ll111lllll_opy_:
                                l1l11l1ll_opy_(self.l1l11l11l11l_opy_(event.l11lll11ll_opy_)[1], event.l11111ll11_opy_)
                                l1ll111lllll_opy_.append((event.step, event.l11lll11ll_opy_))
                            if event.l11111ll11_opy_ == 1:
                                if l1l1ll11ll1l_opy_ == False and (abs(event.l1llll1l111l_opy_ - l1l11ll11lll_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l11ll11lll_opy_) > 2 and event.l1l11111ll_opy_ != l1l1ll1lllll_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                                if l1l1ll11ll1l_opy_ and (abs(event.l1llll1l111l_opy_ - l1l11l111l11_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l11l111l11_opy_) > 2 and event.l1l11111ll_opy_ != l1l1l1lll111_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                            if event.l11111ll11_opy_ == 2:
                                if l1l1l1111l1l_opy_ == False and (abs(event.l1llll1l111l_opy_ - l1l11l1l1l11_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l11l1l1l11_opy_) > 2 and event.l1l11111ll_opy_ != l1l1l11l11l1_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                                if l1l1l1111l1l_opy_ and (abs(event.l1llll1l111l_opy_ - l1l1l1111111_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l1l1111111_opy_) > 2 and event.l1l11111ll_opy_ != l1l11llll11l_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                            if event.l11111ll11_opy_ == 3:
                                if l1l11llll1l1_opy_ == False and (abs(event.l1llll1l111l_opy_ - l1l1l11l11ll_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l1l11l11ll_opy_) > 2 and event.l1l11111ll_opy_ != l1l11lll1l11_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                                if l1l11llll1l1_opy_ and (abs(event.l1llll1l111l_opy_ - l1l1l1ll11l1_opy_) > 4 or (abs(event.l1llll1l111l_opy_ - l1l1l1ll11l1_opy_) > 2 and event.l1l11111ll_opy_ != l1l11l1l1ll1_opy_)):
                                    l1l11l1ll_opy_(self.l1l11ll1111l_opy_(event.l1l11111ll_opy_), event.l11111ll11_opy_)
                            l1l11l1ll_opy_(self.l1l1ll11llll_opy_(event.step, event.type, event.l1lll1l11ll1_opy_) + self.l1l11ll1l11l_opy_(event.dot) + self.l1l1ll111111_opy_(event.l11llll111_opy_) + self.l1l1l11lllll_opy_(event.l1l1111111_opy_) + self.l1l1ll1ll111_opy_(event.text), event.l11111ll11_opy_)
                            if event.l1l11111ll_opy_ !=100:
                                if event.l11111ll11_opy_ == 1:
                                    l1l1ll1lllll_opy_ = event.l1l11111ll_opy_
                                    l1l11ll11lll_opy_ = event.l1llll1l111l_opy_
                                elif event.l11111ll11_opy_ == 2:
                                    l1l1l11l11l1_opy_ = event.l1l11111ll_opy_
                                    l1l11l1l1l11_opy_ = event.l1llll1l111l_opy_
                                elif event.l11111ll11_opy_ == 3:
                                    l1l11lll1l11_opy_ = event.l1l11111ll_opy_
                                    l1l1l11l11ll_opy_ = event.l1llll1l111l_opy_
                            if event.l1111l1l11_opy_ == "stop":
                                l1llllll1ll_opy_ = False
                            if event.l1111l1l11_opy_ in ["start", "continue"] or l1llllll1ll_opy_ == True:
                                l1l11l1ll_opy_(b14, event.l11111ll11_opy_)
                                l1llllll1ll_opy_ = True
                            if event.l11111ll11_opy_ == 1:
                                l1l1ll11ll1l_opy_ = False
                            elif event.l11111ll11_opy_ == 2:
                                l1l1l1111l1l_opy_ = False
                            elif event.l11111ll11_opy_ == 3:
                                l1l11llll1l1_opy_ = False
                        if event.t == "note" and event.l1ll1llll11_opy_ in [1,2,3]:
                            self.l1l1ll111lll_opy_.append(event)
                        if event.t == "note" and event.l1ll1llll11_opy_ == 3:
                            if event.l11111ll11_opy_ == 1:
                                l1l1ll11ll1l_opy_ = True
                            elif event.l11111ll11_opy_ == 2:
                                l1l1l1111l1l_opy_ = True
                            elif event.l11111ll11_opy_ == 3:
                                l1l11llll1l1_opy_ = True
                            if self.l1l11lll111l_opy_:
                                if event.l11111ll11_opy_ ==1:
                                    self.l1l1l1111l11_opy_ = sorted(self.l1l1ll111lll_opy_, key=lambda note: note.l1llll1l111l_opy_, reverse=True)
                                else:
                                    self.l1l1l1111l11_opy_ = sorted(self.l1l1ll111lll_opy_, key=lambda note: note.l1llll1l111l_opy_)
                            else:
                                if self._1ll111111ll_opy_:
                                    self.l1l1l1111l11_opy_ = sorted(self.l1l1ll111lll_opy_, key = lambda note: note.l1llll1l111l_opy_)
                                else:
                                    self.l1l1l1111l11_opy_ = sorted(self.l1l1ll111lll_opy_, key = lambda note: note.l1llll1l111l_opy_, reverse = True)
                            l1l1lll11l11_opy_ = self.l1l1l1111l11_opy_[0].l1llll1l111l_opy_
                            l1l11llll111_opy_ = self.l1l1l1111l11_opy_[0].l1l11111ll_opy_
                            if event.l11111ll11_opy_ == 1:
                                l1l11l111l11_opy_ = self.l1l1l1111l11_opy_[0].l1llll1l111l_opy_
                                l1l1l1lll111_opy_ = self.l1l1l1111l11_opy_[0].l1l11111ll_opy_
                            elif event.l11111ll11_opy_ == 2:
                                l1l1l1111111_opy_ = self.l1l1l1111l11_opy_[0].l1llll1l111l_opy_
                                l1l11llll11l_opy_ = self.l1l1l1111l11_opy_[0].l1l11111ll_opy_
                            elif event.l11111ll11_opy_ == 3:
                                l1l1l1ll11l1_opy_ = self.l1l1l1111l11_opy_[0].l1llll1l111l_opy_
                                l1l11l1l1ll1_opy_ = self.l1l1l1111l11_opy_[0].l1l11111ll_opy_
                            for i, l1l1l11ll1l1_opy_ in enumerate(self.l1l1l1111l11_opy_):
                                if i == 0:
                                    l1l11l1ll_opy_(self.l1l11l11l11l_opy_(l1l1l11ll1l1_opy_.l11lll11ll_opy_)[1], l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    if event.l11111ll11_opy_ == 1:
                                        if abs(l1l11l111l11_opy_  - l1l11ll11lll_opy_) >4 or (abs(l1l11l111l11_opy_ - l1l11ll11lll_opy_) >2 and l1l1l1lll111_opy_ != l1l1ll1lllll_opy_):
                                            l1l11l1ll_opy_(self.l1l11ll1111l_opy_(l1l1l11ll1l1_opy_.l1l11111ll_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    elif event.l11111ll11_opy_ == 2:
                                        if abs(l1l1l1111111_opy_ - l1l11l1l1l11_opy_) >4 or (abs(l1l1l1111111_opy_ - l1l11l1l1l11_opy_) >2 and l1l11llll11l_opy_ != l1l1l11l11l1_opy_):
                                            l1l11l1ll_opy_(self.l1l11ll1111l_opy_(l1l1l11ll1l1_opy_.l1l11111ll_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    elif event.l11111ll11_opy_ == 3:
                                        if abs(l1l1l1ll11l1_opy_ - l1l1l11l11ll_opy_) >4 or (abs(l1l1l1ll11l1_opy_ - l1l1l11l11ll_opy_) >2 and l1l11l1l1ll1_opy_ != l1l11lll1l11_opy_):
                                            l1l11l1ll_opy_(self.l1l11ll1111l_opy_(l1l1l11ll1l1_opy_.l1l11111ll_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    l1l11l1ll_opy_(self.l1l1ll11llll_opy_(l1l1l11ll1l1_opy_.step, l1l1l11ll1l1_opy_.type, l1l1l11ll1l1_opy_.l1lll1l11ll1_opy_) + self.l1l11ll1l11l_opy_(l1l1l11ll1l1_opy_.dot) + self.l1l1ll111111_opy_(l1l1l11ll1l1_opy_.l11llll111_opy_) + self.l1l1l11lllll_opy_(l1l1l11ll1l1_opy_.l1l1111111_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    l1l11l1l1lll_opy_ = l1l1l11ll1l1_opy_.text
                                    if event.l1l11111ll_opy_ !=100:
                                        if event.l11111ll11_opy_ == 1:
                                            l1l1ll1lllll_opy_ = event.l1l11111ll_opy_
                                            l1l11ll11lll_opy_ = event.l1llll1l111l_opy_
                                        elif event.l11111ll11_opy_ == 2:
                                            l1l1l11l11l1_opy_ = event.l1l11111ll_opy_
                                            l1l11l1l1l11_opy_ = event.l1llll1l111l_opy_
                                        elif event.l11111ll11_opy_ == 3:
                                            l1l11lll1l11_opy_ = event.l1l11111ll_opy_
                                            l1l1l11l11ll_opy_ = event.l1llll1l111l_opy_
                                else:
                                    interval = abs(l1l1l11ll1l1_opy_.l1llll1l111l_opy_ - l1l1lll11l11_opy_)
                                    if interval == 0:
                                        l1ll11lll1l1_opy_ = self.l1l11ll1111l_opy_(l1l1l11ll1l1_opy_.l1l11111ll_opy_)
                                    else:
                                        l1ll11lll1l1_opy_ = ""
                                    l1l11l111l1l_opy_ = interval
                                    #l1ll11lll1l1_opy_ = ""
                                    while l1l11l111l1l_opy_ >7:
                                        l1l11l111l1l_opy_ -=7
                                        l1ll11lll1l1_opy_ = self.l1l11ll1111l_opy_(l1l1l11ll1l1_opy_.l1l11111ll_opy_)
                                    l1l11l1ll_opy_(self.l1l11l11l11l_opy_(l1l1l11ll1l1_opy_.l11lll11ll_opy_)[1] + l1ll11lll1l1_opy_ + self.l1l11l11ll1l_opy_(l1l11l111l1l_opy_) + self.l1l1ll111111_opy_(l1l1l11ll1l1_opy_.l11llll111_opy_) + self.l1l1l11lllll_opy_(l1l1l11ll1l1_opy_.l1l1111111_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                                    l1l11l1ll_opy_(self.l1l1ll1ll111_opy_(l1l11l1l1lll_opy_), l1l1l11ll1l1_opy_.l11111ll11_opy_)
                            self.l1l1ll111lll_opy_.clear()
                            self.l1l1l1111l11_opy_.clear()
                        if event.t == "note" and event.l1l11l1l1l_opy_:
                            l1l11l1ll_opy_(self.l1l11l11l1ll_opy_(), event.l11111ll11_opy_)
                        if event.t == "note" and event.l1llll111l1_opy_:
                            l1l11l1ll_opy_(self.l1l11l1ll1l1_opy_(), event.l11111ll11_opy_)
                        if event.t == "print" and event.l1111l11ll_opy_ == "yes":
                            l1111l11ll_opy_.append(l111111l1l_opy_.l1lll111l11_opy_)
                        if event.t == "karaoke":
                            l1l11l1ll_opy_(self.l1l1l11l1lll_opy_(event.l111l1l11l_opy_), 1)
                    l1l1ll1l11l1_opy_.append([l1l1l111l111_opy_, l1l1ll1l11ll_opy_, l1l1ll11111l_opy_, self.l1l1l1l1lll1_opy_])
                self.l1l1ll1ll1l1_opy_.append((l1l1ll1l11l1_opy_, l1111l11ll_opy_, self._1l11lll11ll_opy_))
                if self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['view'] == 'by_part' or self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] == 'total_part' or self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] in ['edit', 'listen']:
                    l1l11lll1l1l_opy_()
                l1l11l11llll_opy_ +=1
                self.l1l11lll111l_opy_ = False
        if (self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['view'] == 'by_section' and self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['section'] != 'total_part') and self._1ll111l11l1_opy_[self._1ll111ll111_opy_]['edit_mode'] not in ['edit', 'listen']:
            l1l11l111ll1_opy_()
        l1l1lll111ll_opy_ = sorted(self.l1l1l111l11l_opy_, key = lambda l1l1l1l1l1ll_opy_: l1l1l1l1l1ll_opy_[0])
        for item in l1l1lll111ll_opy_:
            self._1l1111ll_opy_(item[1])
        return self._1l1l11ll_opy_