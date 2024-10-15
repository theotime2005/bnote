"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
from .l1l11l11l11_opy_ import *
from .l1lll1lll11l_opy_ import *
class l1l1l1l1lll_opy_:
    def __init__(self, lou, l1l11lll1l_opy_, l1l111l1l1_opy_, l1l1ll1ll_opy_, settings):
        self.lou = lou
        self._1l111lll_opy_ = l1l11lll1l_opy_
        self._1l1l1l1l_opy_ = l1l111l1l1_opy_
        self._1l1lll11_opy_ = l1l1ll1ll_opy_
        (self._11111111l1_opy_, self._1llll11ll11_opy_) = settings
    def l1l1l1ll11l_opy_ (self):
        self._1l1l1l1l_opy_ ("\nmodel to braille")
        def l1ll11l111ll_opy_ ():
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "id":
                return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(element.l1ll11lll1_opy_)
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "name":
                if element.l1lllll111_opy_ == "Br Piano right hand":
                    return b46 + b345
                elif element.l1lllll111_opy_ == "Br Piano left hand":
                    return b456 + b345
                elif element.l1lllll111_opy_ == "Br Piano solo":
                    return b5 + b345
                elif element.l1lllll111_opy_ == "Bru Piano right hand":
                    return b46 + b345 + b345
                elif element.l1lllll111_opy_ == "Brd Piano left hand":
                    return b456 + b345 + b345
                elif element.l1lllll111_opy_ == "Br Organ pedal":
                    return b45 + b345
                elif element.l1lllll111_opy_ != "no":
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(element.l1lllll111_opy_.replace(" ", " "))
                else:
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(element.l1ll11lll1_opy_)
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "abbreviation":
                if element.l111l1l11_opy_ != "no":
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(element.l111l1l11_opy_)
                else:
                    return b56 + b23 + b23 + b1234 + self.to_dots_8(element.l1ll11lll1_opy_)
        def l1ll1l111ll1_opy_ (l1ll1l1l111l_opy_):
            for i in self._1l1lll11_opy_.l1lll1ll1l_opy_:
                if i.t == "part-list":
                    _1lll1l1l111_opy_ = i.l1lll11ll1_opy_[l1ll1l1l111l_opy_].l1ll11lll1_opy_
                    _name = i.l1lll11ll1_opy_[l1ll1l1l111l_opy_].l1lllll111_opy_
                    _1lll1l1l1l1_opy_ = i.l1lll11ll1_opy_[l1ll1l1l111l_opy_].l111l1l11_opy_
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "id":
                return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(_1lll1l1l111_opy_)
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "name":
                if _name == "Br Piano right hand":
                    return b46 + b345
                elif _name == "Br Piano left hand":
                    return b456 + b345
                elif _name != "no":
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(_name.replace(" ", " "))
                else:
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(_1lll1l1l111_opy_)
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["parts"] == "abbreviation":
                if _1lll1l1l1l1_opy_ != "no":
                    return b56 + b23 + b23 + b1234 + self.lou.to_dots_8(_1lll1l1l1l1_opy_)
                else:
                    return b56 + b23 + b23 + b1234 + self.to_dots_8(_1lll1l1l111_opy_)
        def l1lll1111ll1_opy_(l1111l111_opy_):
            if l11ll1ll11_opy_.l1l11l1ll11_opy_ == True:
                return [l1lll1ll1lll_opy_ [l1111l111_opy_], l1lll1ll1lll_opy_ [l1111l111_opy_]]
            else:
                return [l1lll1ll1lll_opy_ [l1111l111_opy_], ""]
        def l1lll1111l11_opy_ (l1l1llllll_opy_):
            if l11ll1ll11_opy_.l1l11l1l11l_opy_:
                return l1lll1llll1l_opy_ [l1l1llllll_opy_]
            else:
                return ""
        def l1ll11ll11ll_opy_ (step, type, l1l111ll1l1_opy_):
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["edit_mode"]:
                return l1lll1ll11ll_opy_ [step,type][0]
            else:
                if self._11111111l1_opy_[self._1llll11ll11_opy_]["notes_dots"] == "8_dots" :
                    return l1lll1ll11ll_opy_ [step,type][0]
                elif self._11111111l1_opy_[self._1llll11ll11_opy_]["notes_dots"] == "6_dots":
                    return l1lll1ll11ll_opy_ [step,type][1]
                elif self._11111111l1_opy_[self._1llll11ll11_opy_]["notes_dots"] == "6_dots_with_group":
                    if l1l111ll1l1_opy_ in [0,1,2,3]:
                        return l1lll1ll11ll_opy_ [step,type][1]
                    else:
                        return l1lll1ll11ll_opy_ [step,type][2]
        def l1ll1ll1111l_opy_ (dot):
            if dot:
                return b3
            else:
                return ""
        def l1ll1l11llll_opy_ (l1l1l1l1ll_opy_):
            if l1l1l1l1ll_opy_ not in l1lll1lllll1_opy_.keys():
                return ""
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["fingering"]:
                return l1lll1lllll1_opy_ [l1l1l1l1ll_opy_]
            else:
                return ""
        def l1lll11l1lll_opy_ (text):
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["lyrics"] == "after_each_note":
                if text != "":
                    return b0 + b56 + b23 + self.lou.to_dots_8(text) + b0
                else:
                    return ""
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["lyrics"] in ["before_each_section", "after_each_section"]:
                l1ll1l1lll11_opy_.append (self.lou.to_dots_6(text))
                return ""
            else:
                return ""
        def l1ll1l1l1lll_opy_ (l1l111l11l_opy_):
            if l1l111l11l_opy_ in ["start", "stop-start"]:
                return b4 + b14
            else:
                return ""
        def l1ll11l1l111_opy_ ():
            return b236
        def l1ll1l111l1l_opy_ ():
            return b6 + b236
        def l1ll1lllll11_opy_ ():
            return b46 + b236
        def l1ll1l11lll1_opy_ ():
            return b6 + b34
        def l1ll1ll11l1l_opy_ ():
            return b126 + b123
        def l1ll1l1111l1_opy_ ():
            return b235
        def l1lll11lll1l_opy_ (l1ll11l11l_opy_):
            return l1lll1ll1l11_opy_ [l1ll11l11l_opy_]
        def l1ll11llll11_opy_ (l1llllll11_opy_):
            if l1llllll11_opy_ == "start":
                return b126+b14
            elif l1llllll11_opy_ == "stop":
                return b16+b14
        def l1ll11lll1ll_opy_ (self, l1l1111l1_opy_):
            if l1l1111l1_opy_ == "crescendo":
                return b345+b14
            elif l1l1111l1_opy_ == "diminuendo":
                self.l1ll1l111lll_opy_ = False
                return b345+b145
            elif l1l1111l1_opy_ == "stop":
                if self.l1ll1l111lll_opy_:
                    return b345+b25
                else:
                    self.l1ll1l111lll_opy_ = True
                    return b345+b256
        def l1lll111111l_opy_ (l1l1l1l1l1_opy_):
            return l1lll1ll11l1_opy_ [l1l1l1l1l1_opy_] + b0
        def l1ll1lll1l1l_opy_ (l1l11l1111_opy_, l1l11ll111_opy_, l1ll1llll1_opy_):
            self._1lllll11l1l_opy_ = l1l11l1111_opy_
            self._1111lll11l_opy_ = l1l11ll111_opy_
            self._1ll1ll1l1l1_opy_ = l1ll1llll1_opy_
            self._1lll11l1l1l_opy_ = ""
            for char in self._1lllll11l1l_opy_:
                self._1lll11l1l1l_opy_  += numeral_to_braille_high (char)
            self._1ll1ll1l1ll_opy_ = ""
            for char in self._1111lll11l_opy_:
                self._1ll1ll1l1ll_opy_  += numeral_to_braille_low (char)
            self._1ll1llll1ll_opy_ = NumeralPrefix + self._1lll11l1l1l_opy_ + self._1ll1ll1l1ll_opy_ + b0
            if self._1ll1ll1l1l1_opy_ == "common":
                self._1ll1llll1ll_opy_ = b46 + b14 + b0
            if self._1ll1ll1l1l1_opy_ == "cut":
                self._1ll1llll1ll_opy_ = b456 + b14 + b0
            return self._1ll1llll1ll_opy_
        def l1lll11l11l1_opy_ (l1llll111l_opy_, l1ll1ll111_opy_, l111111l1_opy_):
            self._1lll111l111_opy_ = l1llll111l_opy_
            self._1ll11ll11l1_opy_ = l1ll1ll111_opy_
            self._1lll1l1l11l_opy_ = l111111l1_opy_
            if self._1lll111l111_opy_ == "eighth":
                self._1lll1l11l11_opy_ = b145
            elif self._1lll111l111_opy_ == "quarter":
                self._1lll1l11l11_opy_ = b1456
            elif self._1lll111l111_opy_ == "half":
                self._1lll1l11l11_opy_ = b1345
            elif self._1lll111l111_opy_ == "whole":
                self._1lll1l11l11_opy_ = b13456
            else:
                self._1lll1l11l11_opy_ = b1345 + b135
            if self._1ll11ll11l1_opy_:
                self._1ll11l1lll1_opy_ = b3
            else:
                self._1ll11l1lll1_opy_ = ""
            self._1ll1ll1lll1_opy_ = ""
            for char in self._1lll1l1l11l_opy_:
                self._1ll1ll1lll1_opy_ += numeral_to_braille_high (char)
            self._1ll1llll1ll_opy_ = b0 + self._1lll1l11l11_opy_ + self._1ll11l1lll1_opy_ + b2356 + NumeralPrefix + self._1ll1ll1lll1_opy_ + b0
            return self._1ll1llll1ll_opy_
        def l1ll1lll111l_opy_ (l111111l1_opy_):
            l1ll1l1l1ll1_opy_ = round(float(l111111l1_opy_))
            self._1lll1l1l11l_opy_ = str (l1ll1l1l1ll1_opy_)
            self._1ll1ll1lll1_opy_ = ""
            for char in self._1lll1l1l11l_opy_:
                self._1ll1ll1lll1_opy_ += numeral_to_braille_high (char)
            self._1ll1llll1ll_opy_ = b0 + b1456 + b2356 + b6 + NumeralPrefix + self._1ll1ll1lll1_opy_ + b0
            return self._1ll1llll1ll_opy_
        def l1lll1ll1111_opy_ (l111l1111ll_opy_, l1lll11111l1_opy_):
            l1lll1l1ll11_opy_ = b0
            l1ll1l11ll1l_opy_ = b2356
            for char in str(l111l1111ll_opy_):
                l1ll1l11ll1l_opy_ += numeral_to_braille_high (char)
            l1ll1l11ll1l_opy_ += b2356 + b0
            if (self._11111111l1_opy_[self._1llll11ll11_opy_]["edit_mode"] and l111l1111ll_opy_ != 1) or (self._11111111l1_opy_[self._1llll11ll11_opy_]["measure_b123"] and l111l1111ll_opy_ != 1 and l1lll11111l1_opy_):
                l1lll1l1ll11_opy_ += b123 + b0
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["measure_number"] and l111l1111ll_opy_ != 1 and l111l1111ll_opy_ % int(self._11111111l1_opy_[self._1llll11ll11_opy_]["measure_every"]) == 0:
                l1lll1l1ll11_opy_ += l1ll1l11ll1l_opy_
            return l1lll1l1ll11_opy_
        def l1lll111lll1_opy_ (interval):
            return l1lll1lll111_opy_ [interval]
        def l1lll1l11ll1_opy_ (l1ll1111ll_opy_, direction):
            return l1lll1lll1l1_opy_ [(l1ll1111ll_opy_,direction)]
        def l1ll11l11ll1_opy_ (sign, line, l1l1ll1111_opy_, l1l1ll111l_opy_):
            l1lll111ll1l_opy_ = l1lll1lll1ll_opy_ [sign]
            l1ll11l11lll_opy_ = l1lll1llllll_opy_ [line]
            l1lll11lllll_opy_ =l1lll1llll11_opy_ [l1l1ll1111_opy_]
            l1lll1l1lll1_opy_ = b345 + l1lll111ll1l_opy_ + l1ll11l11lll_opy_ + b123
            if sign == "G" and line == "2":
                if l1l1ll111l_opy_ in [1,3]:
                    l1lll1l1lll1_opy_ = b345 + b34 + b123
                else:
                    l1lll1l1lll1_opy_ = b345 + b34 + b13
            if sign == "F" and line == "4":
                if l1l1ll111l_opy_ in [2,3]:
                    l1lll1l1lll1_opy_ = b345 + b3456 + b123
                else:
                    l1lll1l1lll1_opy_ = b345 + b3456 + b13
            l1ll11l11ll1_opy_ = l1lll1l1lll1_opy_ + l1lll11lllll_opy_ + b0
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["clef"]:
                return l1ll11l11ll1_opy_
            else:
                return ""
        def l1ll1l11111l_opy_ (words):
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["words"]:
                l1ll1l1lllll_opy_ = words.strip()
                return b0 + b345 + b345 + self.lou.to_dots_8(l1ll1l1lllll_opy_) + b3 + b0
            else:
                return ""
        def l1lll1l11l1l_opy_ (l11l111l1_opy_, l1111l11l_opy_):
            l1ll11l1l1ll_opy_ = {
                "title": b56 + b23 + b23 + b2345,
                "subtitle": b56 + b23 + b23 + b234,
                "composer": b56 + b23 + b23 + b14,
                "lyricist": b56 + b23 + b23 + b123,
                "arranger": b56 + b23 + b23 + b1,
                "rights": b56 + b23 + b23 + b1235,
                "no": b56 + b23 + b23 + b2456
            }
            l1ll1lll1111_opy_ = l1ll11l1l1ll_opy_.get (l1111l11l_opy_, "")
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["credit_words"]:
                l1ll1llll11l_opy_ = l11l111l1_opy_.strip()
                return l1ll1lll1111_opy_ + self.lou.to_dots_8(l1ll1llll11l_opy_)
            else:
                return ""
        def l1ll11ll1l11_opy_ (l11lllllll_opy_):
            if 0 <= l11lllllll_opy_ < 128:
                l1ll1l1ll11l_opy_ = ""
                for char in l11lllllll_opy_:
                    l1ll1l1ll11l_opy_ += numeral_to_braille_high (char)
                return b56 + b23 + b3 + b1234 + b3456 + l1ll1l1ll11l_opy_
        def l1ll1llllll1_opy_ (l1l1lll1ll_opy_):
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["karaoke"] and l1l1lll1ll_opy_ != "":
                return b0 + b56 + b23 + b23 + b13 + self.lou.to_dots_8(l1l1lll1ll_opy_) + b0
            else:
                return ""
        def l1l11ll1l_opy_ (braille="", l1l1ll111l_opy_=1):
            if l1l1ll111l_opy_ == 1:
                    l1lll11lll11_opy_.append (braille)
            elif l1l1ll111l_opy_ == 2:
                l1ll11ll111l_opy_.append (braille)
            elif l1l1ll111l_opy_ == 3:
                l1ll1ll1l11l_opy_.append (braille)
            elif l1l1ll111l_opy_ == 0:
                self.l1lll1l1111l_opy_.append (braille)
        def l1ll1l11ll11_opy_ (list, l1ll11l1l11l_opy_):
            l = len(list)
# l111l1111ll_opy_ of sub elements of the list
            r = int(l / l1ll11l1l11l_opy_) + (l % l1ll11l1l11l_opy_ > 0)
            return ([list[k * l1ll11l1l11l_opy_: (k + 1) * l1ll11l1l11l_opy_] for k in range(r)])
        def l1ll1lll1lll_opy_ (l1111l111l1_opy_, values):
            l1ll11lllll1_opy_ = list()
            first = 0
            values.append (len(l1111l111l1_opy_) + 1)
            for k in values:
                l1ll11lllll1_opy_.append (l1111l111l1_opy_[first:k - 1])
                first = k - 1
            return (l1ll11lllll1_opy_)
        def l1ll1ll11lll_opy_ (l1lll1l11111_opy_):
            def l1lll1l1llll_opy_ ():
                l1ll11l11lll_opy_ = b56+b23+b23+b13456
                for l11l11l11_opy_ in l1ll11l1ll11_opy_:
                    index = 0
                    empty = True
                    for item in l11l11l11_opy_[3]:
                        if l11l11l11_opy_[3][index] != "":
                            if empty:
                                l1ll11l11lll_opy_ += l11l11l11_opy_[3][index]
                            else:
                                l1ll11l11lll_opy_ += b36 + l11l11l11_opy_[3][index]
                            empty = False
                        index +=1
                    l1ll11l11lll_opy_ += b0
                self._1l1l1l1l_opy_ (l1ll11l11lll_opy_)
                if not empty:
                    self._1l111lll_opy_ (l1ll11l11lll_opy_)
            for l1ll11l1ll11_opy_ in l1lll1l11111_opy_:
                if self._11111111l1_opy_[self._1llll11ll11_opy_]["lyrics"] == "before_each_section":
                    l1lll1l1llll_opy_()
                if self._1lll1111l1l_opy_ == 1:
                    l1ll11l11lll_opy_ = l1ll11l111ll_opy_()
                else:
                    l1ll11l11lll_opy_ = l1ll11l111ll_opy_() + b36 + b16
                for l11l11l11_opy_ in l1ll11l1ll11_opy_:
                    index = 0
                    for item in l11l11l11_opy_[0]:
                        l1ll11l11lll_opy_ += l11l11l11_opy_[0][index]
                        index +=1
                self._1l1l1l1l_opy_ (l1ll11l11lll_opy_)
                if self._1l111lll_opy_:
                    self._1l111lll_opy_ (l1ll11l11lll_opy_)
                if self._1lll1111l1l_opy_ >= 2:
                    l1ll11l11lll_opy_ = l1ll11l111ll_opy_() + b36 + b126
                    for l11l11l11_opy_ in l1ll11l1ll11_opy_:
                        index = 0
                        for item in l11l11l11_opy_[1]:
                            l1ll11l11lll_opy_ += l11l11l11_opy_[1][index]
                            index +=1
                    self._1l1l1l1l_opy_ (l1ll11l11lll_opy_)
                    if self._1l111lll_opy_:
                        self._1l111lll_opy_ (l1ll11l11lll_opy_)
                if self._1lll1111l1l_opy_ >= 3:
                    l1ll11l11lll_opy_ = l1ll11l111ll_opy_() + b36 + b146
                    for l11l11l11_opy_ in l1ll11l1ll11_opy_:
                        index = 0
                        for item in l11l11l11_opy_[2]:
                            l1ll11l11lll_opy_ += l11l11l11_opy_[1][index]
                            index +=1
                    self._1l1l1l1l_opy_ (l1ll11l11lll_opy_)
                    if self._1l111lll_opy_:
                        self._1l111lll_opy_ (l1ll11l11lll_opy_)
                if self._11111111l1_opy_[self._1llll11ll11_opy_]["lyrics"] == "after_each_section":
                    l1lll1l1llll_opy_()
        def l1ll11ll1111_opy_ (l1ll11l11l11_opy_):
            if self._1lll1111l1l_opy_ == 1:
                l1ll1lll11l1_opy_ = l1ll11l111ll_opy_()
            else:
                l1ll1lll11l1_opy_ = l1ll11l111ll_opy_() + b36 + b16
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[0]:
                    l1ll1lll11l1_opy_ += l11l11l11_opy_[0][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1ll1lll11l1_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1ll1lll11l1_opy_)
            l1lll1l111ll_opy_ = ""
            if self._1lll1111l1l_opy_ >= 2:
                l1lll1l111ll_opy_ = l1ll11l111ll_opy_() + b36 + b126
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[1]:
                    l1lll1l111ll_opy_ += l11l11l11_opy_[1][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1lll1l111ll_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1lll1l111ll_opy_)
            l1lll111llll_opy_ = ""
            if self._1lll1111l1l_opy_ >= 3:
                l1lll111llll_opy_ = l1ll11l111ll_opy_() + b36 + b146
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[2]:
                    l1lll111llll_opy_ += l11l11l11_opy_[1][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1lll111llll_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1lll111llll_opy_)
        def l1ll1llll1l1_opy_ (l1ll11l11l11_opy_, l1ll1l1l111l_opy_):
            if self._1lll1111l1l_opy_ == 1:
                l1ll1lll11l1_opy_ = l1ll1l111ll1_opy_(l1ll1l1l111l_opy_)
            else:
                l1ll1lll11l1_opy_ = l1ll1l111ll1_opy_(l1ll1l1l111l_opy_) + b36 + b16
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[0]:
                    l1ll1lll11l1_opy_ += l11l11l11_opy_[0][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1ll1lll11l1_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1ll1lll11l1_opy_)
            l1lll1l111ll_opy_ = ""
            if self._1lll1111l1l_opy_ >= 2:
                l1lll1l111ll_opy_ = l1ll1l111ll1_opy_(l1ll1l1l111l_opy_) + b36 + b126
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[1]:
                    l1lll1l111ll_opy_ += l11l11l11_opy_[1][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1lll1l111ll_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1lll1l111ll_opy_)
            l1lll111llll_opy_ = ""
            if self._1lll1111l1l_opy_ >= 3:
                l1lll111llll_opy_ = l1ll1l111ll1_opy_(l1ll1l1l111l_opy_) + b36 + b146
            for l11l11l11_opy_ in l1ll11l11l11_opy_:
                index = 0
                for item in l11l11l11_opy_[2]:
                    l1lll111llll_opy_ += l11l11l11_opy_[1][index]
                    index +=1
            self._1l1l1l1l_opy_ (l1lll111llll_opy_)
            if self._1l111lll_opy_:
                self._1l111lll_opy_ (l1lll111llll_opy_)
        def l1ll11ll1l1l_opy_ ():
# l1ll1ll1l111_opy_ l1ll1ll1llll_opy_
            index = 0
            for item in self.l1lll1l1111l_opy_:
                self._1l1l1l1l_opy_ (item)
                if self._1l111lll_opy_:
                    self._1l111lll_opy_ (item)
                index +=1
            self.l1lll1l1111l_opy_.clear()
# for l1lll11l111l_opy_ mode
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["edit_mode"]:
                l1ll11ll1111_opy_ (l1ll11l11l11_opy_)
            else:
# l1ll1ll1l111_opy_ with l111l1111ll_opy_ of l1111l111l1_opy_ l11111lllll_opy_ with the l1lll1l111l1_opy_
                if self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] == "system":
                    l1ll1lll1l11_opy_ = l1ll1lll1lll_opy_ (l1ll11l11l11_opy_, l1llllllll_opy_)
                    l1ll1ll11lll_opy_ (l1ll1lll1l11_opy_)
# l1ll1ll1l111_opy_ l11l1l1l1_opy_ part l1lll111l1l1_opy_
                elif self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] == "total_part":
                    l1ll11ll1111_opy_ (l1ll11l11l11_opy_)
# l1lll11ll1l1_opy_ the l1l1ll1ll_opy_ in l1ll11lllll1_opy_ of x l1111l111l1_opy_, l11111lllll_opy_ to l1lll111l11l_opy_ l1ll11llll1l_opy_
                else:
                    l1lll1l11111_opy_ = l1ll1l11ll11_opy_ (l1ll11l11l11_opy_, int(self._11111111l1_opy_[self._1llll11ll11_opy_]["measures_per_section"]))
                    l1ll1ll11lll_opy_ (l1lll1l11111_opy_)
        def l1lll11l1l11_opy_ ():
# l1ll1ll1l111_opy_ l1ll1ll1llll_opy_
            index = 0
            for item in self.l1lll1l1111l_opy_:
                self._1l1l1l1l_opy_ (item)
                if self._1l111lll_opy_:
                    self._1l111lll_opy_ (item)
                index +=1
            self.l1lll1l1111l_opy_.clear()
# l1lll11ll1l1_opy_ the l1l1ll1ll_opy_ in l1ll11lllll1_opy_ of x l1111l111l1_opy_, l11111lllll_opy_ to l1lll111l11l_opy_ l1ll11llll1l_opy_
            l1lll111l1ll_opy_ = len(self.l1ll11ll1lll_opy_[0][0])
            if self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] == "number":
                l111l1l1111_opy_ = 0
                l1ll1l1111ll_opy_ = list()
                while l111l1l1111_opy_ < l1lll111l1ll_opy_:
                    l1ll1l1l111l_opy_ = 0
                    for part in self.l1ll11ll1lll_opy_:
                        self._1lll1111l1l_opy_ = part[2]
                        for l11l11l11_opy_ in part[0][l111l1l1111_opy_:min(l111l1l1111_opy_+int(self._11111111l1_opy_[self._1llll11ll11_opy_]["measures_per_section"]),len(part[0]))]:
                            l1ll1l1111ll_opy_.append(l11l11l11_opy_)
                        l1ll1llll1l1_opy_(l1ll1l1111ll_opy_, l1ll1l1l111l_opy_)
                        l1ll1l1111ll_opy_.clear()
                        l1ll1l1l111l_opy_ += 1
                    l111l1l1111_opy_ += int(self._11111111l1_opy_[self._1llll11ll11_opy_]["measures_per_section"])
# l1ll1ll1l111_opy_ with l111l1111ll_opy_ of l1111l111l1_opy_ l11111lllll_opy_ with the l1lll1l111l1_opy_
            elif self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] == "system":
                l1lll1l111l1_opy_ = list()
                for part in self.l1ll11ll1lll_opy_:
                    for system in part[1]:
                        l1lll1l111l1_opy_.append(system - 1)
                l1ll11l1llll_opy_ = sorted(l1lll1l111l1_opy_)
                l1ll1l111l11_opy_ = list()
                for i in l1ll11l1llll_opy_:
                    if i not in l1ll1l111l11_opy_:
                        l1ll1l111l11_opy_.append(i)
                l1ll1l111l11_opy_.append(l1lll111l1ll_opy_)
                l111l1l1111_opy_ = 0
                l1ll1l1111ll_opy_ = list()
                l1ll11l1l1l1_opy_ = 0
                for system in l1ll1l111l11_opy_:
                    l1ll1l1l111l_opy_ = 0
                    for part in self.l1ll11ll1lll_opy_:
                        self._1lll1111l1l_opy_ = part[2]
                        for l11l11l11_opy_ in part[0][l111l1l1111_opy_:min(l111l1l1111_opy_+system - l1ll11l1l1l1_opy_, len(part[0]))]:
                            l1ll1l1111ll_opy_.append(l11l11l11_opy_)
                        l1ll1llll1l1_opy_(l1ll1l1111ll_opy_, l1ll1l1l111l_opy_)
                        l1ll1l1111ll_opy_.clear()
                        l1ll1l1l111l_opy_ += 1
                    l111l1l1111_opy_ += system - l1ll11l1l1l1_opy_
                    l1ll11l1l1l1_opy_ = system
        l1ll11llllll_opy_ = 0 # for groups of l111l11111l_opy_
        self._1lll1111l1l_opy_ = 1
        l1l1l1l1l1_opy_ = 0
        l111llll1_opy_ = False
        l1ll1lll1ll1_opy_ = False # l1lllll11l11_opy_ for braille l1l1llllll_opy_ which l1ll1ll11l11_opy_ of the first note of the l11ll1lll_opy_ for l1lll11l1ll1_opy_
        l1ll1ll111ll_opy_ = False # l1lllll11l11_opy_ for braille l1l1llllll_opy_ which l1ll1ll11l11_opy_ of the first note of the l11ll1lll_opy_ for l1ll1ll111l1_opy_
        l1ll1l1ll1l1_opy_ = False # l1lllll11l11_opy_ for braille l1l1llllll_opy_ which l1ll1ll11l11_opy_ of the first note of the l11ll1lll_opy_ for l1ll1l1llll1_opy_
        self.l1ll1l111lll_opy_ = True # l1lllll11l11_opy_ to l1ll1llll111_opy_ the l11111lll_opy_ end of l111l1l1ll_opy_ b345+b25 for end l1ll1ll1ll1l_opy_, b345+b256 for end l1lll111ll11_opy_
        l1ll11lll111_opy_ = True
        self.l1lll1l1111l_opy_ = list()
        self.l1ll1l111111_opy_ = list()
        self.l1ll11ll1lll_opy_ = list()
        self._1111l11lll_opy_ = self._11111111l1_opy_[self._1llll11ll11_opy_]["ascending_chords"]
        self._1lll11ll1ll_opy_ = list()
# l1ll1l1l11ll_opy_ for the l111l1111ll_opy_ of l1111ll11l1_opy_ braille parts
        l1lll11111ll_opy_ = list()
        for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
            if element.t == "part":
                for l11l11l11_opy_ in element.l11l1llll_opy_:
                    for event in l11l11l11_opy_.l11llll11_opy_:
                        if event.t == "attributes":
                            for l1l1ll1l11_opy_ in event.l1l1lll11l_opy_:
                                if l1l1ll1l11_opy_.t == "staves":
                                    self._1lll1111l1l_opy_ = int(l1l1ll1l11_opy_.l1l1lll111_opy_)
                        if event.t == "note":
                            if event.l1l1ll111l_opy_ > self._1lll1111l1l_opy_:
                                self._1lll1111l1l_opy_ = event.l1l1ll111l_opy_
                l1lll11111ll_opy_.append ([element.l1ll11lll1_opy_, self._1lll1111l1l_opy_])
        self._1l1l1l1l_opy_ ("braille_sub_parts " + str(l1lll11111ll_opy_))
# l1ll1lll11ll_opy_ part-list l1ll1l1l1l11_opy_ for l1lllll11lll_opy_ l1l1ll111l_opy_ braille
        #l1ll1lllllll_opy_ = 1
        #for part in l1lll11111ll_opy_:
            #if part[1] > 1:
                #print(part[0])
                #for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
                    #if element.t == "part-list":
# l111111l11l_opy_ the l1ll11lll11l_opy_ l1l1ll1ll_opy_
        l1ll11lll1l1_opy_ = 0
        for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
            if element.t == "credit":
                l1l11ll1l_opy_ (l1lll1l11l1l_opy_ (element.l11l111l1_opy_, element.l1111l11l_opy_), 0)
            if element.t == "part-list":
                for item in element.l1lll11ll1_opy_:
                    self._1lll11ll1ll_opy_.append(item.l1l1111ll11_opy_)
            if element.t == "part":
                self._1lll1111l1l_opy_ = l1lll11111ll_opy_ [l1ll11lll1l1_opy_][1]
                l1ll1l1lll1l_opy_ = -1
                l1lll11l1111_opy_ = -7
                l1ll1l1l11l1_opy_ = -1
                l1ll1ll11ll1_opy_ = -7
                l1lll1l1ll1l_opy_ = -1
                l1lll11ll11l_opy_ = -7
                l1ll11lll111_opy_ = True
                l1ll11l11l11_opy_ = list()
                l1llllllll_opy_ = list()
                self._1111l11lll_opy_ = self._1lll11ll1ll_opy_[l1ll11lll1l1_opy_]
                for l11l11l11_opy_ in element.l11l1llll_opy_:
                    l1lll11lll11_opy_ = list()
                    l1ll11ll111l_opy_ = list()
                    l1ll1ll1l11l_opy_ = list()
                    l1ll1l1lll11_opy_ = list()
                    l1llll1111l1_opy_ = list()
                    l1l11ll1l_opy_ (l1lll1ll1111_opy_(l11l11l11_opy_.l1l111l111_opy_, l1ll11lll111_opy_), 1)
                    if self._1lll1111l1l_opy_ >= 2:
                        l1l11ll1l_opy_ (l1lll1ll1111_opy_(l11l11l11_opy_.l1l111l111_opy_, l1ll11lll111_opy_), 2)
                    if self._1lll1111l1l_opy_ >= 3:
                        l1l11ll1l_opy_ (l1lll1ll1111_opy_(l11l11l11_opy_.l1l111l111_opy_, l1ll11lll111_opy_), 3)
                    l1ll11lll111_opy_ = True
                    for event in l11l11l11_opy_.l11llll11_opy_:
                        if event.t == "direction":
                            for l1l1ll1l11_opy_ in event.l11l1l111_opy_:
                                if l1l1ll1l11_opy_.t == "words":
                                    l1l11ll1l_opy_ (l1ll1l11111l_opy_ (l1l1ll1l11_opy_.words), l1l1ll1l11_opy_.l1l1ll111l_opy_)
                                elif l1l1ll1l11_opy_.t == "dynamics":
                                    l1l11ll1l_opy_ (l1lll11lll1l_opy_ (l1l1ll1l11_opy_.l1ll11l11l_opy_), event.l1l1ll111l_opy_)
                                    if event.l1l1ll111l_opy_ == 1:
                                        l1ll1l1lll1l_opy_ = -1
                                        l1lll11l1111_opy_ = -7
                                    elif event.l1l1ll111l_opy_ == 2:
                                        l1ll1l1l11l1_opy_ = -1
                                        l1ll1ll11ll1_opy_ = -7
                                    elif event.l1l1ll111l_opy_ == 3:
                                        l1lll1l1ll1l_opy_ = -1
                                        l1lll11ll11l_opy_ = -7
                                elif l1l1ll1l11_opy_.t == "pedal":
                                    l1l11ll1l_opy_ (l1ll11llll11_opy_ (l1l1ll1l11_opy_.l1llllll11_opy_), event.l1l1ll111l_opy_)
                                elif l1l1ll1l11_opy_.t == "wedge":
                                    l1l11ll1l_opy_ (l1ll11lll1ll_opy_ (self, l1l1ll1l11_opy_.l1l1111l1_opy_), event.l1l1ll111l_opy_)
                                elif l1l1ll1l11_opy_.t == "metronome":
                                    l1l11ll1l_opy_ (l1lll11l11l1_opy_(l1l1ll1l11_opy_.l1llll111l_opy_, l1l1ll1l11_opy_.l1ll1ll111_opy_, l1l1ll1l11_opy_.l111111l1_opy_), event.l1l1ll111l_opy_)
                                elif l1l1ll1l11_opy_.t == "sound":
                                    if l1l1ll1l11_opy_.l1l11111ll_opy_ != "no":
                                        l1l11ll1l_opy_ (l1ll1lll111l_opy_ (l1l1ll1l11_opy_.l1l11111ll_opy_), event.l1l1ll111l_opy_)
                        if event.t == "backup" and event.l1l1111ll1l_opy_:
                            l1l11ll1l_opy_ (b126+b345, event.l1l1ll111l_opy_)
                        if event.t == "attributes":
                            for l1l1ll1l11_opy_ in event.l1l1lll11l_opy_:
                                if l1l1ll1l11_opy_.t == "key":
                                    l1l1l1l1l1_opy_ = l1l1ll1l11_opy_.l1l1l1l1l1_opy_
                                    l1l11ll1l_opy_ (l1lll111111l_opy_(l1l1l1l1l1_opy_), 1)
                                    if self._1lll1111l1l_opy_ >=2:
                                        l1l11ll1l_opy_ (l1lll111111l_opy_(l1l1l1l1l1_opy_), 2)
                                    if self._1lll1111l1l_opy_ >=3:
                                        l1l11ll1l_opy_ (l1lll111111l_opy_(l1l1l1l1l1_opy_), 3)
                                elif l1l1ll1l11_opy_.t == "time":
                                    l1l11ll1l_opy_ (l1ll1lll1l1l_opy_(l1l1ll1l11_opy_.l1l11l1111_opy_, l1l1ll1l11_opy_.l1l11ll111_opy_, l1l1ll1l11_opy_.l1ll1llll1_opy_), 1)
                                elif l1l1ll1l11_opy_.t == "clef":
                                    l1l11ll1l_opy_ (l1ll11l11ll1_opy_(l1l1ll1l11_opy_.sign, l1l1ll1l11_opy_.line, l1l1ll1l11_opy_.l1l1ll1111_opy_, l1l1ll1l11_opy_.l1l1111l111_opy_), l1l1ll1l11_opy_.l1l1111l111_opy_)
                        if event.t == "barline":
                            l1l11ll1l_opy_ (l1lll1l11ll1_opy_(event.l1ll1111ll_opy_, event.l1llll1ll1_opy_), 1)
                            if self._1lll1111l1l_opy_ >=2:
                                l1l11ll1l_opy_ (l1lll1l11ll1_opy_(event.l1ll1111ll_opy_, event.l1llll1ll1_opy_), 2)
                            if self._1lll1111l1l_opy_ >=3:
                                l1l11ll1l_opy_ (l1lll1l11ll1_opy_(event.l1ll1111ll_opy_, event.l1llll1ll1_opy_), 3)
                            if event.l1ll1111ll_opy_ == "light-light":
                                l1ll11lll111_opy_ = False
# for l1ll1l1ll111_opy_ l1ll1ll1ll11_opy_
                        if event.t == "note" and event.l1ll1lll11_opy_ == 3 and event.l1l1ll1lll_opy_ == 2:
                            l1ll11llllll_opy_ +=1
                            if l1ll11llllll_opy_ == 1:
                                l1l11ll1l_opy_ (b23, event.l1l1ll111l_opy_)
                            if l1ll11llllll_opy_ ==3:
                                l1ll11llllll_opy_ -=3
# for l1ll1ll11l_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l1ll1ll11l_opy_:
                            if event.l1lll1l1l1_opy_ == "yes" or event.l1lll1l1l1_opy_ == False:
                                l1l11ll1l_opy_ (b26, event.l1l1ll111l_opy_)
                            if event.l1lll1l1l1_opy_ == "no":
                                l1l11ll1l_opy_ (b5+b26, event.l1l1ll111l_opy_)
# for l11lll111_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l11lll111_opy_:
                            l1l11ll1l_opy_ (l1ll11l1l111_opy_(), event.l1l1ll111l_opy_)
# for l11lllll1_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l11lllll1_opy_:
                            l1l11ll1l_opy_ (l1ll1l111l1l_opy_(), event.l1l1ll111l_opy_)
# for l1l1111l1l_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l1l1111l1l_opy_:
                            l1l11ll1l_opy_ (l1ll1lllll11_opy_(), event.l1l1ll111l_opy_)
# for l1l11ll11l_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l1l11ll11l_opy_:
                            l1l11ll1l_opy_ (l1ll1l1111l1_opy_(), event.l1l1ll111l_opy_)
# for l1lll11l11ll_opy_ l111l11111l_opy_ (l1llll1l1111_opy_ l11ll1lll_opy_)
                        if event.t == "note" and event.l1l111ll11l_opy_ == 0:
                            if event.l1l11ll1l1_opy_ == "natural":
                                l1l11ll1l_opy_ (l1lll1111ll1_opy_(l1l1ll1l11l_opy_.l1l1l11l1ll_opy_.l1l1l11ll1l_opy_)[1] , event.l1l1ll111l_opy_)
                            if (event.step, event.l1111l111_opy_) not in l1lll1ll1l1l_opy_[l1l1l1l1l1_opy_] and (event.step, event.l1111l111_opy_) not in l1llll1111l1_opy_:
                                l1l11ll1l_opy_ (l1lll1111ll1_opy_(event.l1111l111_opy_)[1], event.l1l1ll111l_opy_)
                                l1llll1111l1_opy_.append ((event.step, event.l1111l111_opy_))
                            if event.l1l1ll111l_opy_ == 1:
                                if l1ll1lll1ll1_opy_ == False and (abs(event.l1l111l1l1l_opy_ - l1lll11l1111_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1lll11l1111_opy_) > 2 and event.l1l1llllll_opy_ != l1ll1l1lll1l_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                                if l1ll1lll1ll1_opy_ and (abs(event.l1l111l1l1l_opy_ - l1ll11ll1ll1_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1ll11ll1ll1_opy_) > 2 and event.l1l1llllll_opy_ != l1lll1111lll_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                            if event.l1l1ll111l_opy_ == 2:
                                if l1ll1ll111ll_opy_ == False and (abs(event.l1l111l1l1l_opy_ - l1ll1ll11ll1_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1ll1ll11ll1_opy_) > 2 and event.l1l1llllll_opy_ != l1ll1l1l11l1_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                                if l1ll1ll111ll_opy_ and (abs(event.l1l111l1l1l_opy_ - l1ll1l1l1l1l_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1ll1l1l1l1l_opy_) > 2 and event.l1l1llllll_opy_ != l1ll1l1ll1ll_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                            if event.l1l1ll111l_opy_ == 3:
                                if l1ll1l1ll1l1_opy_ == False and (abs(event.l1l111l1l1l_opy_ - l1lll11ll11l_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1lll11ll11l_opy_) > 2 and event.l1l1llllll_opy_ != l1lll1l1ll1l_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                                if l1ll1l1ll1l1_opy_ and (abs(event.l1l111l1l1l_opy_ - l1ll1ll11111_opy_) > 4 or (abs(event.l1l111l1l1l_opy_ - l1ll1ll11111_opy_) > 2 and event.l1l1llllll_opy_ != l1ll1l11l111_opy_)):
                                    l1l11ll1l_opy_ (l1lll1111l11_opy_(event.l1l1llllll_opy_), event.l1l1ll111l_opy_)
                            l1l11ll1l_opy_ (l1ll11ll11ll_opy_(event.step, event.type, event.l1l111ll1l1_opy_) + l1ll1ll1111l_opy_ (event.dot) + l1ll1l11llll_opy_(event.l1l1l1l1ll_opy_) + l1ll1l1l1lll_opy_ (event.l1l111l11l_opy_) + l1lll11l1lll_opy_ (event.text), event.l1l1ll111l_opy_)
                            if event.l1l1llllll_opy_ !=100:
                                if event.l1l1ll111l_opy_ == 1:
                                    l1ll1l1lll1l_opy_ = event.l1l1llllll_opy_
                                    l1lll11l1111_opy_ = event.l1l111l1l1l_opy_
                                elif event.l1l1ll111l_opy_ == 2:
                                    l1ll1l1l11l1_opy_ = event.l1l1llllll_opy_
                                    l1ll1ll11ll1_opy_ = event.l1l111l1l1l_opy_
                                elif event.l1l1ll111l_opy_ == 3:
                                    l1lll1l1ll1l_opy_ = event.l1l1llllll_opy_
                                    l1lll11ll11l_opy_ = event.l1l111l1l1l_opy_
                            if event.l111ll11l_opy_ == "stop":
                                l111llll1_opy_ = False
                            if event.l111ll11l_opy_ in ["start", "continue"] or l111llll1_opy_ == True:
                                l1l11ll1l_opy_ (b14, event.l1l1ll111l_opy_)
                                l111llll1_opy_ = True
                            if event.l1l1ll111l_opy_ == 1:
                                l1ll1lll1ll1_opy_ = False
                            elif event.l1l1ll111l_opy_ == 2:
                                l1ll1ll111ll_opy_ = False
                            elif event.l1l1ll111l_opy_ == 3:
                                l1ll1l1ll1l1_opy_ = False
# for l1ll11l11l1l_opy_, 1 l1llll11111l_opy_ a sub-list of l11ll1lll_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l1l111ll11l_opy_ in [1,2,3]:
                            self.l1ll1l111111_opy_.append (event)
# 2 when the l11ll1lll_opy_ is l1ll1lllll1l_opy_, sort the l111l11111l_opy_ l1lll11llll1_opy_ to the l1ll1l11l11l_opy_ of braille l11111l1ll1_opy_
                        if event.t == "note" and event.l1l111ll11l_opy_ == 3:
                            if event.l1l1ll111l_opy_ == 1:
                                l1ll1lll1ll1_opy_ = True
                            elif event.l1l1ll111l_opy_ == 2:
                                l1ll1ll111ll_opy_ = True
                            elif event.l1l1ll111l_opy_ == 3:
                                l1ll1l1ll1l1_opy_ = True
                            if self._1111l11lll_opy_:
                                self.l1ll1l1l1111_opy_ = sorted (self.l1ll1l111111_opy_, key = lambda note: note.l1l111l1l1l_opy_)
                            else:
                                self.l1ll1l1l1111_opy_ = sorted (self.l1ll1l111111_opy_, key = lambda note: note.l1l111l1l1l_opy_, reverse = True)
                            l1lll11ll111_opy_ = self.l1ll1l1l1111_opy_[0].l1l111l1l1l_opy_
                            l1ll1l11l1l1_opy_ = self.l1ll1l1l1111_opy_[0].l1l1llllll_opy_
                            if event.l1l1ll111l_opy_ == 1:
                                l1ll11ll1ll1_opy_ = self.l1ll1l1l1111_opy_[0].l1l111l1l1l_opy_
                                l1lll1111lll_opy_ = self.l1ll1l1l1111_opy_[0].l1l1llllll_opy_
                            elif event.l1l1ll111l_opy_ == 2:
                                l1ll1l1l1l1l_opy_ = self.l1ll1l1l1111_opy_[0].l1l111l1l1l_opy_
                                l1ll1l1ll1ll_opy_ = self.l1ll1l1l1111_opy_[0].l1l1llllll_opy_
                            elif event.l1l1ll111l_opy_ == 3:
                                l1ll1ll11111_opy_ = self.l1ll1l1l1111_opy_[0].l1l111l1l1l_opy_
                                l1ll1l11l111_opy_ = self.l1ll1l1l1111_opy_[0].l1l1llllll_opy_
                            for i, l1ll11l1ll1l_opy_ in enumerate(self.l1ll1l1l1111_opy_):
# first note of the l11ll1lll_opy_
                                if i == 0:
                                    l1l11ll1l_opy_ (l1lll1111ll1_opy_(l1ll11l1ll1l_opy_.l1111l111_opy_)[1], l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                                    if event.l1l1ll111l_opy_ == 1:
                                        if abs(l1ll11ll1ll1_opy_  - l1lll11l1111_opy_) >4 or (abs(l1ll11ll1ll1_opy_ - l1lll11l1111_opy_) >2 and l1lll1111lll_opy_ != l1ll1l1lll1l_opy_):
                                            l1l11ll1l_opy_ (l1lll1111l11_opy_(l1ll11l1ll1l_opy_.l1l1llllll_opy_), l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                                    elif event.l1l1ll111l_opy_ == 2:
                                        if abs(l1ll1l1l1l1l_opy_ - l1ll1ll11ll1_opy_) >4 or (abs(l1ll1l1l1l1l_opy_ - l1ll1ll11ll1_opy_) >2 and l1ll1l1ll1ll_opy_ != l1ll1l1l11l1_opy_):
                                            l1l11ll1l_opy_ (l1lll1111l11_opy_(l1ll11l1ll1l_opy_.l1l1llllll_opy_), l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                                    elif event.l1l1ll111l_opy_ == 3:
                                        if abs(l1ll1ll11111_opy_ - l1lll11ll11l_opy_) >4 or (abs(l1ll1ll11111_opy_ - l1lll11ll11l_opy_) >2 and l1ll1l11l111_opy_ != l1lll1l1ll1l_opy_):
                                            l1l11ll1l_opy_ (l1lll1111l11_opy_(l1ll11l1ll1l_opy_.l1l1llllll_opy_), l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                                    l1l11ll1l_opy_ (l1ll11ll11ll_opy_(l1ll11l1ll1l_opy_.step, l1ll11l1ll1l_opy_.type, l1ll11l1ll1l_opy_.l1l111ll1l1_opy_) + l1ll1ll1111l_opy_ (l1ll11l1ll1l_opy_.dot) + l1ll1l11llll_opy_(l1ll11l1ll1l_opy_.l1l1l1l1ll_opy_), l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                                    if event.l1l1llllll_opy_ !=100:
                                        if event.l1l1ll111l_opy_ == 1:
                                            l1ll1l1lll1l_opy_ = event.l1l1llllll_opy_
                                            l1lll11l1111_opy_ = event.l1l111l1l1l_opy_
                                        elif event.l1l1ll111l_opy_ == 2:
                                            l1ll1l1l11l1_opy_ = event.l1l1llllll_opy_
                                            l1ll1ll11ll1_opy_ = event.l1l111l1l1l_opy_
                                        elif event.l1l1ll111l_opy_ == 3:
                                            l1lll1l1ll1l_opy_ = event.l1l1llllll_opy_
                                            l1lll11ll11l_opy_ = event.l1l111l1l1l_opy_
# other l111l11111l_opy_ of the l11ll1lll_opy_, l1llll11111l_opy_ the l11111l1ll1_opy_
                                else:
                                    interval = abs(l1ll11l1ll1l_opy_.l1l111l1l1l_opy_ - l1lll11ll111_opy_)
                                    l1lll1l11lll_opy_ = interval
                                    l1111l11111_opy_ = ""
                                    while l1lll1l11lll_opy_ >7:
                                        l1lll1l11lll_opy_ -=7
                                        l1111l11111_opy_ = l1lll1111l11_opy_ (l1ll11l1ll1l_opy_.l1l1llllll_opy_)
                                    l1l11ll1l_opy_ (l1lll1111ll1_opy_(l1ll11l1ll1l_opy_.l1111l111_opy_)[1] + l1111l11111_opy_ + l1lll111lll1_opy_ (l1lll1l11lll_opy_) + l1ll1l11llll_opy_(l1ll11l1ll1l_opy_.l1l1l1l1ll_opy_), l1ll11l1ll1l_opy_.l1l1ll111l_opy_)
                            self.l1ll1l111111_opy_.clear()
                            self.l1ll1l1l1111_opy_.clear()
# for l1lll1ll111l_opy_-l1ll1l11l1ll_opy_ l111l11111l_opy_
                        if event.t == "note" and event.l1ll11111l_opy_:
                            l1l11ll1l_opy_ (l1ll1l11lll1_opy_(), event.l1l1ll111l_opy_)
# for l1ll1l1ll1_opy_ l111l11111l_opy_, l1lll1l1l1ll_opy_ d'l1lll1111111_opy_
                        if event.t == "note" and event.l1ll1l1ll1_opy_:
                            l1l11ll1l_opy_ (l1ll1ll11l1l_opy_(), event.l1l1ll111l_opy_)
                        if event.t == "print" and event.l1llllllll_opy_ == "yes":
                            l1llllllll_opy_.append (l11l11l11_opy_.l1l111l111_opy_)
                        if event.t == "karaoke":
                            l1l11ll1l_opy_ (l1ll1llllll1_opy_ (event.l1l1lll1ll_opy_), 1)
                    l1ll11l11l11_opy_.append ([l1lll11lll11_opy_, l1ll11ll111l_opy_, l1ll1ll1l11l_opy_, l1ll1l1lll11_opy_])
                self.l1ll11ll1lll_opy_.append ((l1ll11l11l11_opy_, l1llllllll_opy_, self._1lll1111l1l_opy_))
                if self._11111111l1_opy_[self._1llll11ll11_opy_]["view"] == "by_part" or self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] == "total_part" or self._11111111l1_opy_[self._1llll11ll11_opy_]["edit_mode"]:
                    l1ll11ll1l1l_opy_ ()
                l1ll11lll1l1_opy_ +=1
        if (self._11111111l1_opy_[self._1llll11ll11_opy_]["view"] == "by_section" and self._11111111l1_opy_[self._1llll11ll11_opy_]["section"] != "total_part") and not self._11111111l1_opy_[self._1llll11ll11_opy_]["edit_mode"]:
            l1lll11l1l11_opy_()
        return self._1l1lll11_opy_