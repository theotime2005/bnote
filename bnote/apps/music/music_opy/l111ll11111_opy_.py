"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import os
import xml.sax
from .l1l111ll1_opy_ import *
import time


class l11l11l1ll1_opy_:
    def __init__(self, lou, l1l1lllll_opy_, l11llll11_opy_, l111llllll1_opy_):
        self.lou = lou
        self._1l1ll111_opy_ = l1l1lllll_opy_
        self.l11llll11_opy_ = l11llll11_opy_
        self.l111llllll1_opy_ = l111llllll1_opy_

    class l11l1ll11ll_opy_(xml.sax.ContentHandler):
        l111ll1lll1_opy_ = "measure"
        l1l1llll111_opy_ = "note"
        l11llll1l11_opy_ = "chord"
        l1l1l1lllll_opy_ = "grace"
        l111l111l1l_opy_ = "rest"
        l11111ll111_opy_ = "step"
        l11ll1l11l1_opy_ = "alter"
        l11l111l1l1_opy_ = "accidental"
        l11lll1l111_opy_ = "octave"
        l1ll11l1l1l_opy_ = "duration"
        l1l1111ll1l_opy_ = "voice"
        l111l1l11ll_opy_ = "type"
        l1l11111lll_opy_ = "dot"
        l111ll1111l_opy_ = "staff"
        l11ll1l1ll1_opy_ = "slur"
        l1l111llll1_opy_ = "credit"
        l1l1l111lll_opy_ = "credit-type"
        l1l11l1l11l_opy_ = "credit-words"
        l1ll1l11lll_opy_ = "score-part"
        l11111l1l11_opy_ = "part-name"
        l11l1lll11l_opy_ = "part-abbreviation"
        l1ll11lll1l_opy_ = "score-instrument"
        l1ll1111lll_opy_ = "instrument-name"
        l1111l11ll1_opy_ = "midi-device"
        l11l11111l1_opy_ = "midi-instrument"
        l11ll1l1lll_opy_ = "midi-channel"
        l11llll1l1l_opy_ = "midi-program"
        l1111ll11ll_opy_ = "volume"
        l111l11l1l1_opy_ = "pan"
        l1l1111l1l1_opy_ = "part-list"
        l1l1l1l1lll_opy_ = "part"
        l11111ll1l1_opy_ = "attributes"
        l11111llll1_opy_ = "divisions"
        l11l11llll1_opy_ = "key"
        l1ll11l1l11_opy_ = "fifths"
        l111l1l1ll1_opy_ = "mode"
        l111l111ll1_opy_ = "time"
        l11l1llllll_opy_ = "beats"
        l11l1l1ll11_opy_ = "beat-type"
        l111lll1111_opy_ = "staves"
        l111l1l1lll_opy_ = "clef"
        l11l1l11l1l_opy_ = "sign"
        l11l111l111_opy_ = "line"
        l111l11l1ll_opy_ = "clef-octave-change"
        l111ll11l1l_opy_ = "braille-clef"
        l111l11l11l_opy_ = "transpose"
        l1l1l11111l_opy_ = "diatonic"
        l11l111llll_opy_ = "chromatic"
        l11l11l111l_opy_ = "octave-change"
        l111l1l1l11_opy_ = "double"
        l11llll1lll_opy_ = "metronome"
        l11111lll11_opy_ = "beat-unit"
        l1l1ll11l11_opy_ = "beat-unit-dot"
        l1l1l11l1l1_opy_ = "per-minute"
        l11l111111l_opy_ = "fingering"
        l1ll11ll1l1_opy_ = "backup"
        l1ll1111ll1_opy_ = "direction"
        l111l11lll1_opy_ = "p"
        l1ll1l111l1_opy_ = "pp"
        l1l1lll1l11_opy_ = "ppp"
        l1l111ll11l_opy_ = "pppp"
        l1l1111l11l_opy_ = "ppppp"
        l11ll1l111l_opy_ = "pppppp"
        l1l11l11lll_opy_ = "f"
        l1111l1lll1_opy_ = "ff"
        l11l1lllll1_opy_ = "fff"
        l111ll11l11_opy_ = "ffff"
        l1ll11lll11_opy_ = "fffff"
        l1l1ll11l1l_opy_ = "ffffff"
        l11l11ll11l_opy_ = "mp"
        l1ll111111l_opy_ = "mf"
        l1l111lllll_opy_ = "sf"
        l1l1l1l11l1_opy_ = "sfp"
        l111lll1l11_opy_ = "sfpp"
        l111l1l1111_opy_ = "fp"
        l1ll11111l1_opy_ = "rf"
        l1ll1111l11_opy_ = "rfz"
        l11ll111111_opy_ = "sfz"
        l1l1111ll11_opy_ = "sffz"
        l11111l111l_opy_ = "fz"
        N = "n"
        l111ll111l1_opy_ = "pf"
        l1l1l1l1111_opy_ = "sfzp"
        l1l1ll1ll11_opy_ = "other-dynamics"
        l11l11l1111_opy_ = "words"
        l11ll1l1l11_opy_ = "actual-notes"
        l1l1lll111l_opy_ = "normal-notes"
        l1111l1111l_opy_ = "print"
        l1l11111l1l_opy_ = "staff-layout"
        l1111l1l1l1_opy_ = "lyric"
        l1111ll11l1_opy_ = "syllabic"
        l1l1l1ll1ll_opy_ = "text"
        l1l11111l11_opy_ = "tie"
        l1l11l11111_opy_ = "barline"
        l1ll11l1ll1_opy_ = "bar-style"
        REPEAT = "repeat"
        l1111ll1lll_opy_ = "ending"
        l1l1ll1l1ll_opy_ = "staccato"
        l1l11lll1ll_opy_ = "staccatissimo"
        l11111l11ll_opy_ = "accent"
        l1ll111lll1_opy_ = "breath-mark"
        l1l1ll1l1l1_opy_ = "fermata"
        l1l1l1l1ll1_opy_ = "trill-mark"
        l1ll111ll1l_opy_ = "inverted-mordent"
        l1l1111111l_opy_ = "mordent"
        l1l1lll1lll_opy_ = "arpeggiate"
        l11lllll1l1_opy_ = "two-hands-arpeggiate"
        l1l1111llll_opy_ = "pedal"
        l111l1111ll_opy_ = "wedge"
        l1l11llll11_opy_ = "sound"
        l11llll1111_opy_ = "karaoke"
        l11l11lll1l_opy_ = "braille-global"
        l11l11l1lll_opy_ = "global-key"
        l11111l1l1l_opy_ = "global-fifths"
        l11l1l1llll_opy_ = "global-time"
        l11l11lllll_opy_ = "global-beats"
        l1l1l11ll1l_opy_ = "global-beat-type"
        l111l1ll111_opy_ = "global-symbol"
        l1111l11l1l_opy_ = "measure-style"
        l1ll1l111ll_opy_ = "multiple-rest"
        l1l1lll1l1l_opy_ = "measure-repeat"
        l11l11ll1l1_opy_ = "braille-ascending-chords"
        l1l1l1lll11_opy_ = "work"
        l11111l1ll1_opy_ = "work-number"
        l1111llll1l_opy_ = "work-title"
        l1l1ll11ll1_opy_ = (
            l11111ll111_opy_, l11ll1l11l1_opy_, l11l111l1l1_opy_, l11lll1l111_opy_, l1ll11l1l1l_opy_, l1l1111ll1l_opy_,
            l111l1l11ll_opy_, l111ll1111l_opy_, l1l1l111lll_opy_, l1l11l1l11l_opy_, l11111llll1_opy_, l1ll11l1l11_opy_,
            l111l1l1ll1_opy_, l11l1llllll_opy_, l11l1l1ll11_opy_,
            l111lll1111_opy_, l11l1l11l1l_opy_, l11l111l111_opy_, l111l11l1ll_opy_, l111ll11l1l_opy_, l1l1l11111l_opy_,
            l11l111llll_opy_, l11l11l111l_opy_, l11111lll11_opy_, l1l1l11l1l1_opy_, l11l111111l_opy_, l11111l1l11_opy_,
            l11l1lll11l_opy_,
            l1ll1111lll_opy_, l11ll1l1lll_opy_, l11llll1l1l_opy_, l1111ll11ll_opy_, l111l11l1l1_opy_, l11l11l1111_opy_,
            l11ll1l1l11_opy_, l1l1lll111l_opy_, l1111ll11l1_opy_, l1l1l1ll1ll_opy_, l1ll11l1ll1_opy_,
            l11llll1111_opy_, l11111l1l1l_opy_, l11l11lllll_opy_, l1l1l11ll1l_opy_, l1ll1l111ll_opy_, l1l1lll1l1l_opy_,
            l11l11ll1l1_opy_,
            l11111l1ll1_opy_, l1111llll1l_opy_
        )

        def __init__(self, l11llll11l_opy_, l1l11ll11_opy_, l11111l1lll_opy_, l111llllll1_opy_):
            self._1l1111ll_opy_ = l11llll11l_opy_
            self.l1l11ll11_opy_ = l1l11ll11_opy_
            self._11l1111ll1_opy_ = l11111l1lll_opy_
            self.l111llllll1_opy_ = l111llllll1_opy_
            self.l111111l1l_opy_ = None
            self.note = None
            self.l11lll11lll_opy_ = None
            self.l1l11l1l111_opy_ = None
            self.l111l111lll_opy_ = None
            self.l1l11lllll1_opy_ = None
            self.part = None
            self.l1l1l11l1ll_opy_ = None
            self.l111l1111l_opy_ = None
            self.time = None
            self.l1111111ll_opy_ = None
            self.l1l1ll1l111_opy_ = None
            self.l1ll1ll11ll_opy_ = None
            self.l111l1lll1l_opy_ = None
            self.l1l1l1ll1l1_opy_ = None
            self.key = None
            self.direction = None
            self.words = None
            self._1l1lllllll_opy_ = 1
            self.l1l1l1lll1l_opy_ = False
            self.l111l1l11l_opy_ = None
            self.l11l1111l1l_opy_ = None
            self.l11111l11l1_opy_ = None
            self.l1l111ll111_opy_ = None
            self.l1lll111lll_opy_ = None
            self.l1ll111l1l1_opy_ = None
            self.l11lllll11l_opy_ = ""
            self.l1ll1l1111l_opy_ = list()
            self.l1l111111ll_opy_ = {
                self.l111ll1lll1_opy_: {'start_element_fn': self.l1l1111l1ll_opy_,
                                        'end_element_fn': self.l11lllll111_opy_, 'is_inside': False},
                self.l1l1llll111_opy_: {'start_element_fn': self.l1ll111ll11_opy_,
                                        'end_element_fn': self.l11ll1l11ll_opy_, 'is_inside': False},
                self.l11111ll111_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll11ll111_opy_,
                                        'is_inside': False},
                self.l111l111l1l_opy_: {'start_element_fn': self.l1111l1l11l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11llll1l11_opy_: {'start_element_fn': self.l1l11ll1l1l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1l1lllll_opy_: {'start_element_fn': self.l1l1llll1ll_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11111lll_opy_: {'start_element_fn': self.l11l11l11ll_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11ll1l11l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l11llll11l1_opy_,
                                        'is_inside': False},
                self.l11l111l1l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll1l11l11_opy_,
                                        'is_inside': False},
                self.l11lll1l111_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1ll1ll1_opy_,
                                        'is_inside': False},
                self.l1ll11l1l1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1111llll11_opy_,
                                        'is_inside': False},
                self.l1l1111ll1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l11llllllll_opy_,
                                        'is_inside': False},
                self.l111l1l11ll_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll1l11111_opy_,
                                        'is_inside': False},
                self.l111ll1111l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l11l1l1ll_opy_,
                                        'is_inside': False},
                self.l11ll1l1ll1_opy_: {'start_element_fn': self.l111ll11lll_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l111llll1_opy_: {'start_element_fn': self.l11l11lll11_opy_,
                                        'end_element_fn': self.l11111ll1ll_opy_, 'is_inside': False},
                self.l1l1l111lll_opy_: {'start_element_fn': None, 'end_element_fn': self.l111l111111_opy_,
                                        'is_inside': False},
                self.l1l11l1l11l_opy_: {'start_element_fn': None, 'end_element_fn': self.l11111ll11l_opy_,
                                        'is_inside': False},
                self.l1l1111l1l1_opy_: {'start_element_fn': self.l1111l1l1ll_opy_,
                                        'end_element_fn': self.l11l1l1lll1_opy_, 'is_inside': False},
                self.l1ll1l11lll_opy_: {'start_element_fn': self.l1l1ll1ll1l_opy_,
                                        'end_element_fn': self.l1l11ll11ll_opy_, 'is_inside': False},
                self.l11111l1l11_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l111lll1l_opy_,
                                        'is_inside': False},
                self.l11l1lll11l_opy_: {'start_element_fn': None, 'end_element_fn': self.l11lll111l1_opy_,
                                        'is_inside': False},
                self.l1ll11lll1l_opy_: {'start_element_fn': self.l1l1ll1l11l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll1111lll_opy_: {'start_element_fn': None, 'end_element_fn': self.l11lll11ll1_opy_,
                                        'is_inside': False},
                self.l1111l11ll1_opy_: {'start_element_fn': self.l111llll11l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11l11111l1_opy_: {'start_element_fn': self.l11l111ll11_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11ll1l1lll_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1111111_opy_,
                                        'is_inside': False},
                self.l11llll1l1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll11111ll_opy_,
                                        'is_inside': False},
                self.l1111ll11ll_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll11ll11l_opy_,
                                        'is_inside': False},
                self.l111l11l1l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l1ll11l11l1_opy_,
                                        'is_inside': False},
                self.l1l1l1l1lll_opy_: {'start_element_fn': self.l1ll11lllll_opy_,
                                        'end_element_fn': self.l11l1llll11_opy_, 'is_inside': False},
                self.l11111ll1l1_opy_: {'start_element_fn': self.l1l11l1111l_opy_,
                                        'end_element_fn': self.l1111lll1ll_opy_, 'is_inside': False},
                self.l11111llll1_opy_: {'start_element_fn': self.l1ll11l1111_opy_,
                                        'end_element_fn': self.l1111ll111l_opy_, 'is_inside': False},
                self.l1ll11l1l11_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1l1l1ll_opy_,
                                        'is_inside': False},
                self.l111l1l1ll1_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l111ll1l1_opy_,
                                        'is_inside': False},
                self.l111l111ll1_opy_: {'start_element_fn': self.l111l1l11l1_opy_,
                                        'end_element_fn': self.l1ll11ll1ll_opy_, 'is_inside': False},
                self.l11l1llllll_opy_: {'start_element_fn': None, 'end_element_fn': self.l111llll1ll_opy_,
                                        'is_inside': False},
                self.l11l1l1ll11_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l1l111l1l_opy_,
                                        'is_inside': False},
                self.l111lll1111_opy_: {'start_element_fn': self.l11l1111lll_opy_,
                                        'end_element_fn': self.l11llllll11_opy_, 'is_inside': False},
                self.l111l1l1lll_opy_: {'start_element_fn': self.l11l1ll1111_opy_,
                                        'end_element_fn': self.l1111ll1l1l_opy_, 'is_inside': False},
                self.l11l1l11l1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1111l1llll_opy_,
                                        'is_inside': False},
                self.l11l111l111_opy_: {'start_element_fn': None, 'end_element_fn': self.l111llll1l1_opy_,
                                        'is_inside': False},
                self.l111l11l1ll_opy_: {'start_element_fn': None, 'end_element_fn': self.l11ll111l1l_opy_,
                                        'is_inside': False},
                self.l111l11l11l_opy_: {'start_element_fn': self.l11l1ll111l_opy_,
                                        'end_element_fn': self.l11111lll1l_opy_, 'is_inside': False},
                self.l111ll11l1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l1lllll1l_opy_,
                                        'is_inside': False},
                self.l1l1l11111l_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l11l1l1l_opy_,
                                        'is_inside': False},
                self.l11l111llll_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l11ll1lll_opy_,
                                        'is_inside': False},
                self.l11l11l111l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l11ll1ll1_opy_,
                                        'is_inside': False},
                self.l111l1l1l11_opy_: {'start_element_fn': self.l1l11llllll_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11llll1lll_opy_: {'start_element_fn': self.l11ll11l1ll_opy_,
                                        'end_element_fn': self.l11lll11l1l_opy_, 'is_inside': False},
                self.l11111lll11_opy_: {'start_element_fn': None, 'end_element_fn': self.l11ll111lll_opy_,
                                        'is_inside': False},
                self.l1l1ll11l11_opy_: {'start_element_fn': self.l1l11lll111_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1l11l1l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l111lllll1l_opy_,
                                        'is_inside': False},
                self.l11l111111l_opy_: {'start_element_fn': None, 'end_element_fn': self.l111ll1l1l1_opy_,
                                        'is_inside': False},
                self.l1ll11ll1l1_opy_: {'start_element_fn': self.l111ll1ll11_opy_,
                                        'end_element_fn': self.l11l111l11l_opy_, 'is_inside': False},
                self.l11l11llll1_opy_: {'start_element_fn': self.l1ll1l11ll1_opy_,
                                        'end_element_fn': self.l1l1l1l1l11_opy_, 'is_inside': False},
                self.l1ll1111ll1_opy_: {'start_element_fn': self.l11l11l11l1_opy_,
                                        'end_element_fn': self.l11ll1lll1l_opy_, 'is_inside': False},
                self.l11l11l1111_opy_: {'start_element_fn': self.l111ll1l1ll_opy_,
                                        'end_element_fn': self.l1l1lll11ll_opy_, 'is_inside': False},
                self.l111l11lll1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll1l111l1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1lll1l11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l111ll11l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1111l11l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11ll1l111l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11l11lll_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1111l1lll1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11l1lllll1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l111ll11l11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll11lll11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1ll11l1l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11l11ll11l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll111111l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l111lllll_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1l1l11l1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l111lll1l11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l111l1l1111_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll11111l1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll1111l11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11ll111111_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1111ll11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11111l111l_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.N: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None, 'is_inside': False},
                self.l111ll111l1_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1l1l1111_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1ll1ll11_opy_: {'start_element_fn': self.l11llll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11ll1l1l11_opy_: {'start_element_fn': None, 'end_element_fn': self.l1111llllll_opy_,
                                        'is_inside': False},
                self.l1l1lll111l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l11l111ll_opy_,
                                        'is_inside': False},
                self.l1111l1111l_opy_: {'start_element_fn': self.l1l111111l1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11111l1l_opy_: {'start_element_fn': self.l11ll11l11l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1111l1l1l1_opy_: {'start_element_fn': None, 'end_element_fn': None, 'is_inside': False},
                self.l1111ll11l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l111l1ll1_opy_,
                                        'is_inside': False},
                self.l1l1l1ll1ll_opy_: {'start_element_fn': None, 'end_element_fn': self.l111lll1lll_opy_,
                                        'is_inside': False},
                self.l1l11111l11_opy_: {'start_element_fn': self.l111l1111l1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11l11111_opy_: {'start_element_fn': self.l11l1lll1l1_opy_,
                                        'end_element_fn': self.l1ll1l11l1l_opy_, 'is_inside': False},
                self.l1ll11l1ll1_opy_: {'start_element_fn': None, 'end_element_fn': self.l111l1l111l_opy_,
                                        'is_inside': False},
                self.REPEAT: {'start_element_fn': self.l1111lll1l1_opy_, 'end_element_fn': None, 'is_inside': False},
                self.l1111ll1lll_opy_: {'start_element_fn': self.l11ll111l11_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1ll1l1ll_opy_: {'start_element_fn': self.l1l11l11l1l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11lll1ll_opy_: {'start_element_fn': self.l1111ll1ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11111l11ll_opy_: {'start_element_fn': self.l1111lllll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll111lll1_opy_: {'start_element_fn': self.l1l1llllll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1ll1l1l1_opy_: {'start_element_fn': self.l11l111lll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1l1l1ll1_opy_: {'start_element_fn': self.l11ll1ll1l1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1ll111ll1l_opy_: {'start_element_fn': self.l111lllll11_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1111111l_opy_: {'start_element_fn': self.l11l111ll1l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1lll1lll_opy_: {'start_element_fn': self.l1l111l1l1l_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11lllll1l1_opy_: {'start_element_fn': self.l1ll11llll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l1111llll_opy_: {'start_element_fn': self.l1111l11l11_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l111l1111ll_opy_: {'start_element_fn': self.l1l11l11ll1_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l1l11llll11_opy_: {'start_element_fn': self.l1l111lll11_opy_, 'end_element_fn': None,
                                        'is_inside': False},
                self.l11llll1111_opy_: {'start_element_fn': self.l11llll111l_opy_,
                                        'end_element_fn': self.l1ll111l11l_opy_, 'is_inside': False},
                self.l11l11lll1l_opy_: {'start_element_fn': self.l11l11l1l11_opy_,
                                        'end_element_fn': self.l1l1ll11lll_opy_, 'is_inside': False},
                self.l11l11l1lll_opy_: {'start_element_fn': self.l1l111l1111_opy_,
                                        'end_element_fn': self.l111ll1l111_opy_, 'is_inside': False},
                self.l11111l1l1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l1l11llll_opy_,
                                        'is_inside': False},
                self.l11l1l1llll_opy_: {'start_element_fn': self.l11ll11llll_opy_,
                                        'end_element_fn': self.l11ll11ll1l_opy_, 'is_inside': False},
                self.l11l11lllll_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l111l1lll_opy_,
                                        'is_inside': False},
                self.l1l1l11ll1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1l111ll_opy_,
                                        'is_inside': False},
                self.l1111l11l1l_opy_: {'start_element_fn': self.l11lll1l11l_opy_,
                                        'end_element_fn': self.l1ll11l11ll_opy_, 'is_inside': False},
                self.l1ll1l111ll_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l1l1111ll_opy_,
                                        'is_inside': False},
                self.l1l1lll1l1l_opy_: {'start_element_fn': self.l1l11111111_opy_,
                                        'end_element_fn': self.l11ll1ll1ll_opy_, 'is_inside': False},
                self.l11l11ll1l1_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1111l11_opy_,
                                        'is_inside': False},
                self.l1l1l1lll11_opy_: {'start_element_fn': self.l11l1ll1lll_opy_,
                                        'end_element_fn': self.l1l11l111l1_opy_, 'is_inside': False},
                self.l11111l1ll1_opy_: {'start_element_fn': None, 'end_element_fn': self.l11l1l1ll1l_opy_,
                                        'is_inside': False},
                self.l1111llll1l_opy_: {'start_element_fn': None, 'end_element_fn': self.l1l1l111ll1_opy_,
                                        'is_inside': False},
            }

        def startDocument(self):
            self.l1l11ll11l_opy_ = False
            if self.l1l11ll11l_opy_:
                self._1l1111ll_opy_(
                    "Texts to find\nxml to model score\nOptimize model score2, chord assign\nOptimize model score2, with measure position\nmodel to braille\n\nStart reading xml file")

        def endDocument(self):
            if self.l1l11ll11l_opy_:
                self._1l1111ll_opy_("End reading xml file\n")
                self._1l1111ll_opy_("xml to model score, first extraction")
                self._1l1111ll_opy_(str(self.l1l11ll11_opy_))

        def startElement(self, name, attrs):
            if name in self.l1l111111ll_opy_.keys():
                # print(f"key found {name=}!")
                l111l11ll11_opy_ = self.l1l111111ll_opy_[name]
                l111l11ll11_opy_['is_inside'] = True
                if l111l11ll11_opy_['start_element_fn'] is not None:
                    l111l11ll11_opy_['start_element_fn'](name, attrs)

        def endElement(self, name):
            if name in self.l1l111111ll_opy_.keys():
                l111l11ll11_opy_ = self.l1l111111ll_opy_[name]
                l111l11ll11_opy_['is_inside'] = False
                if l111l11ll11_opy_['end_element_fn'] is not None:
                    l111l11ll11_opy_['end_element_fn']()

        def l11l11ll1ll_opy_(self, elements):
            for element in elements:
                if self.l1l111111ll_opy_[element]['is_inside']:
                    return True
            return False

        def characters(self, content):
            if self.l11l11ll1ll_opy_(self.l1l1ll11ll1_opy_):
                self.l11lllll11l_opy_ += content

        def l1l1111l1ll_opy_(self, name, attrs):
            self.l111111l1l_opy_ = l1l1l1l1l1l_opy_()
            self._1l1lllllll_opy_ = 1
            keys = attrs.keys()
            if 'number' in keys:
                self.l111111l1l_opy_.l1ll111l111_opy_(attrs.getValue('number'))
                if self.l1l11ll11l_opy_:
                    print("mesure", attrs.getValue('number'))

        def l11lllll111_opy_(self):
            self.part.l11l1l11111_opy_(self.l111111l1l_opy_)
            self.l111111l1l_opy_ = None

        def l1ll111ll11_opy_(self, name, attrs):
            self.note = l1l111l111l_opy_()
            if self._1l1lllllll_opy_ != 1:
                self.note.l1ll111l1ll_opy_(self._1l1lllllll_opy_)

        def l11ll1l11ll_opy_(self):
            self.note.l1ll111llll_opy_()
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.note)
            self.note = None

        def l1ll11ll111_opy_(self):
            self.note.l1l11l1ll11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1111l1l11l_opy_(self, name, attrs):
            self.note.rest = True

        def l1l11ll1l1l_opy_(self, name, attrs):
            self.note.l1lll1l11l1_opy_ = True

        def l1l1llll1ll_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'slash' in keys:
                self.note.l11lll1111_opy_ = attrs.getValue('slash')

        def l11l11l11ll_opy_(self, name, attrs):
            self.note.dot = True

        def l11llll11l1_opy_(self):
            self.note.l1l1111lll1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1ll1l11l11_opy_(self):
            self.note.l1llll11ll1_opy_ = self.l11lllll11l_opy_
            self.__11lll11111_opy_()

        def l11l1ll1ll1_opy_(self):
            self.note.l111lll11l1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1111llll11_opy_(self):
            if self.l1l111111ll_opy_[self.l1ll11ll1l1_opy_]['is_inside']:
                self.l1l1l1ll1l1_opy_.l11lll1111l_opy_(self.l11lllll11l_opy_)
            elif self.l1l111111ll_opy_[self.l1l1llll111_opy_]['is_inside']:
                self.note.l11lll1111l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11llllllll_opy_(self):
            if self.l1l111111ll_opy_[self.l1l1llll111_opy_]['is_inside']:
                self.note.l11ll11lll1_opy_(self.l11lllll11l_opy_)
                self._1l1lllllll_opy_ = self.l11lllll11l_opy_
            self.__11lll11111_opy_()

        def l1ll1l11111_opy_(self):
            self.note.l11ll1l1l1l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11l1l1ll_opy_(self):
            if self.l1l111111ll_opy_[self.l1l1llll111_opy_]['is_inside']:
                self.note.l1l1l1ll11l_opy_(self.l11lllll11l_opy_)
            if self.l1l111111ll_opy_[self.l1ll1111ll1_opy_]['is_inside']:
                self.direction.l1l1l1ll11l_opy_(self.l11lllll11l_opy_)
            if self.l1l111111ll_opy_[self.l11l11l1111_opy_]['is_inside']:
                self.words.l1l1l1ll11l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111ll11lll_opy_(self, name, attrs):
            self.note.l1llllll1ll_opy_ = True
            keys = attrs.keys()
            if 'placement' in keys:
                self.note.l11l1111ll_opy_ = attrs.getValue('placement')
            if 'number' in keys:
                self.note.l11l1l111l1_opy_(attrs.getValue('number'))
            if 'type' in keys:
                self.note.l1111l1l11_opy_ = attrs.getValue('type')

        def l11l11lll11_opy_(self, name, attrs):
            self.l1l11l1l111_opy_ = l1l1l1ll111_opy_()

        def l11111ll1ll_opy_(self):
            self.l1l11ll11_opy_.l1l11l1llll_opy_(self.l1l11l1l111_opy_)

        def l111l111111_opy_(self):
            self.l1l11l1l111_opy_.l111ll1llll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11111ll11l_opy_(self):
            self.l1l11l1l111_opy_.l1l1l11l11l_opy_(self.l11lllll11l_opy_.replace(" ", " "))
            self.__11lll11111_opy_()

        def l1111l1l1ll_opy_(self, name, attrs):
            self.l111l111lll_opy_ = l1l1ll1111l_opy_()

        def l11l1l1lll1_opy_(self):
            self.l1l11ll11_opy_.l1l11l1llll_opy_(self.l111l111lll_opy_)
            self.l111l111lll_opy_ = None

        def l1l1ll1ll1l_opy_(self, name, attrs):
            self.l1l11lllll1_opy_ = l1l11lll11l_opy_()
            self.l1l11lllll1_opy_.l11l111l1ll_opy_(self._11l1111ll1_opy_[self.l111llllll1_opy_]['ascending_chords'])
            keys = attrs.keys()
            if 'id' in keys:
                self.l1l11lllll1_opy_.l1l11l11l11_opy_(attrs.getValue('id'))

        def l1l11ll11ll_opy_(self):
            self.l111l111lll_opy_.l1111lll111_opy_(self.l1l11lllll1_opy_)

        def l1l111lll1l_opy_(self):
            l11ll1ll11l_opy_ = False
            if self.l11lllll11l_opy_ == "":
                self.l11lllll11l_opy_ = "default"
            for i in self.l1ll1l1111l_opy_:
                if self.l11lllll11l_opy_ in i[0]:
                    i[1] += 1
                    self.l1l11lllll1_opy_.l11lll1lll1_opy_(self.l11lllll11l_opy_.replace("♭", "flat") + str(i[1]))
                    l11ll1ll11l_opy_ = True
            if not l11ll1ll11l_opy_:
                self.l1l11lllll1_opy_.l11lll1lll1_opy_(self.l11lllll11l_opy_.replace("♭", "flat"))
                self.l1ll1l1111l_opy_.append([self.l11lllll11l_opy_, 1])
            if self.l11lllll11l_opy_ in ["Br Piano right hand", "Br Piano solo", "Brd Piano left hand"]:
                self.l1l11lllll1_opy_.l11l111l1ll_opy_(False)
            elif self.l11lllll11l_opy_ in ["Br Piano left hand", "Br Organ pedal", "Bru Piano right hand"]:
                self.l1l11lllll1_opy_.l11l111l1ll_opy_(True)
            self.__11lll11111_opy_()

        def l11lll111l1_opy_(self):
            self.l1l11lllll1_opy_.l11lll1ll1l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l1ll1l11l_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'id' in keys:
                self.l1l11lllll1_opy_.l11ll111ll1_opy_(attrs.getValue('id'))

        def l11lll11ll1_opy_(self):
            self.l1l11lllll1_opy_.l111lll1ll1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111llll11l_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'id' in keys:
                self.l1l11lllll1_opy_.l11lll1l1ll_opy_(attrs.getValue('id'))
            if 'port' in keys:
                self.l1l11lllll1_opy_.l111l1ll1ll_opy_(attrs.getValue('port'))

        def l11l111ll11_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'id' in keys:
                self.l1l11lllll1_opy_.l11lllllll1_opy_(attrs.getValue('id'))

        def l11l1111111_opy_(self):
            self.l1l11lllll1_opy_.l111l1llll1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1ll11111ll_opy_(self):
            self.l1l11lllll1_opy_.l11lll111ll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1ll11ll11l_opy_(self):
            self.l1l11lllll1_opy_.l11lll1ll11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1ll11l11l1_opy_(self):
            self.l1l11lllll1_opy_.l11l1l1l11l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1ll11lllll_opy_(self, name, attrs):
            self.part = l1l11ll1l11_opy_()
            keys = attrs.keys()
            if 'id' in keys:
                self.part.l1l11l11l11_opy_(attrs.getValue('id'))
                if self.l1l11ll11l_opy_:
                    print("partie", attrs.getValue('id'))

        def l11l1llll11_opy_(self):
            self.l1l11ll11_opy_.l1l11l1llll_opy_(self.part)
            self.part = None

        def l1l11l1111l_opy_(self, name, attrs):
            self.l1l1l11l1ll_opy_ = l111l1ll11l_opy_()
            if self._1l1lllllll_opy_ != 1:
                self.l1l1l11l1ll_opy_.l1ll111l1ll_opy_(self._1l1lllllll_opy_)

        def l1111lll1ll_opy_(self):
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.l1l1l11l1ll_opy_)
            self.l1l1l11l1ll_opy_ = None

        def l1ll11l1111_opy_(self, name, attrs):
            self.l111l1111l_opy_ = l1l1lll1111_opy_()

        def l1111ll111l_opy_(self):
            self.l111l1111l_opy_.l11lllll1ll_opy_(self.l11lllll11l_opy_)
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.l111l1111l_opy_)
            self.__11lll11111_opy_()

        def l11l1l1l1ll_opy_(self):
            self.key.l11ll1ll111_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l111ll1l1_opy_(self):
            self.key.l111l11l111_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111l1l11l1_opy_(self, name, attrs):
            self.time = l1l1ll11111_opy_()
            keys = attrs.keys()
            if 'symbol' in keys:
                self.time.l11ll11111l_opy_(attrs.getValue('symbol'))

        def l1ll11ll1ll_opy_(self):
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.time)
            self.time = None

        def l111llll1ll_opy_(self):
            self.time.l1111ll1l11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l1l111l1l_opy_(self):
            self.time.l1l1ll111l1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l1111lll_opy_(self, name, attrs):
            self.l1111111ll_opy_ = l11l1ll11l1_opy_()

        def l11llllll11_opy_(self):
            self.l1111111ll_opy_.l11l1l11lll_opy_(self.l11lllll11l_opy_)
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.l1111111ll_opy_)
            self.__11lll11111_opy_()
            self.l1111111ll_opy_ = None

        def l11l1ll1111_opy_(self, name, attrs):
            self.l1l1ll1l111_opy_ = l1l111l11l1_opy_()
            keys = attrs.keys()
            if 'number' in keys:
                self.l1l1ll1l111_opy_.l1l1l11ll11_opy_(attrs.getValue('number'))

        def l1111ll1l1l_opy_(self):
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.l1l1ll1l111_opy_)
            self.l1l1ll1l111_opy_ = None

        def l1111l1llll_opy_(self):
            self.l1l1ll1l111_opy_.l1111l1ll1l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111llll1l1_opy_(self):
            self.l1l1ll1l111_opy_.l11l1l11l11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11ll111l1l_opy_(self):
            self.l1l1ll1l111_opy_.l111lll11ll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l1ll111l_opy_(self, name, attrs):
            self.l1ll1ll11ll_opy_ = l11l1l1l1l1_opy_()

        def l11111lll1l_opy_(self):
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.l1ll1ll11ll_opy_)
            self.l1ll1ll11ll_opy_ = None

        def l1l1lllll1l_opy_(self):
            self.l1l1ll1l111_opy_.l111lll111l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l11l1l1l_opy_(self):
            self.l1ll1ll11ll_opy_.l11lll1llll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11ll1lll_opy_(self):
            self.l1ll1ll11ll_opy_.l111ll1l11l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11ll1ll1_opy_(self):
            self.l1ll1ll11ll_opy_.l111l1ll1l1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11llllll_opy_(self, name, attrs):
            self.l1ll1ll11ll_opy_.l1l1l1111l1_opy_(True)
            keys = attrs.keys()
            if 'above' in keys:
                self.l1ll1ll11ll_opy_.l1111l11111_opy_(attrs.getValue('above'))

        def l11ll11l1ll_opy_(self, name, attrs):
            self.l111l1lll1l_opy_ = l11llll11ll_opy_()
            keys = attrs.keys()
            if 'parentheses' in keys:
                self.l111l1lll1l_opy_.l1l1ll111ll_opy_(attrs.getValue('parentheses'))

        def l11lll11l1l_opy_(self):
            self.direction.l1l11l1llll_opy_(self.l111l1lll1l_opy_)

        def l11ll111lll_opy_(self):
            self.l111l1lll1l_opy_.l11l11ll111_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11lll111_opy_(self, name, attrs):
            self.l111l1lll1l_opy_.l1ll11l111l_opy_(True)

        def l111lllll1l_opy_(self):
            self.l111l1lll1l_opy_.l1ll1111l1l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111ll1l1l1_opy_(self):
            self.note.l11llll111_opy_ = self.l11lllll11l_opy_
            self.__11lll11111_opy_()

        def l111ll1ll11_opy_(self, name, attrs):
            self.l1l1l1ll1l1_opy_ = l111ll1ll1l_opy_()
            self._1l1lllllll_opy_ = 2
            self.l1l1l1ll1l1_opy_.l1ll111l1ll_opy_(2)
            if self._1l1lllllll_opy_ != 1:
                self.l1l1l1ll1l1_opy_.l1ll111l1ll_opy_(self._1l1lllllll_opy_)

        def l11l111l11l_opy_(self):
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.l1l1l1ll1l1_opy_)
            self.l1l1l1ll1l1_opy_ = None

        def l1ll1l11ll1_opy_(self, name, attrs):
            self.key = l1l1l11l111_opy_()

        def l1l1l1l1l11_opy_(self):
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.key)
            self.key = None

        def l11l11l11l1_opy_(self, name, attrs):
            self.direction = l11ll11l1l1_opy_()
            if self._1l1lllllll_opy_ != 1:
                self.direction.l1ll111l1ll_opy_(self._1l1lllllll_opy_)
            keys = attrs.keys()
            if 'placement' in keys:
                self.direction.l1111l1ll11_opy_(attrs.getValue('placement'))

        def l11ll1lll1l_opy_(self):
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.direction)

        def l111ll1l1ll_opy_(self, name, attrs):
            self.words = l11ll1l1111_opy_()
            self.direction.l1l11l1llll_opy_(self.words)

        def l1l1lll11ll_opy_(self):
            self.words.l1ll1111111_opy_(self.l11lllll11l_opy_.replace(" ", " "))
            self.__11lll11111_opy_()

        def l11llll1ll1_opy_(self, name, attrs):
            l1l11l1ll1_opy_ = l11l1llll1l_opy_()
            l1l11l1ll1_opy_.l11ll1111ll_opy_(name)
            self.direction.l1l11l1llll_opy_(l1l11l1ll1_opy_)

        def l1111llllll_opy_(self):
            self.note.l1l1lllll11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11l111ll_opy_(self):
            self.note.l11ll1lll11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l111111l1_opy_(self, name, attrs):
            l111l1l1l1l_opy_ = l111l111l11_opy_()
            keys = attrs.keys()
            if 'new-system' in keys:
                l111l1l1l1l_opy_.l1l1ll1llll_opy_(attrs.getValue('new-system'))
            self.l111111l1l_opy_.l1l11l1llll_opy_(l111l1l1l1l_opy_)

        def l11ll11l11l_opy_(self, name, attrs):
            l111l1l1l1l_opy_ = l111l111l11_opy_()
            keys = attrs.keys()
            if 'number' in keys:
                l111l1l1l1l_opy_.l1l11l1lll1_opy_(attrs.getValue('number'))
            if self.l111111l1l_opy_ is not None:
                self.l111111l1l_opy_.l1l11l1llll_opy_(l111l1l1l1l_opy_)

        def l1l111l1ll1_opy_(self):
            self.note.l1l111l11ll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111lll1lll_opy_(self):
            self.note.l1111l11lll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l111l1111l1_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'type' in keys:
                self.note.l11llllll1l_opy_(attrs.getValue('type'))
            self.note.l1l11lll1l1_opy_(True)

        def l11l1lll1l1_opy_(self, name, attrs):
            self.l11lll11lll_opy_ = l1l1l1l111l_opy_()
            if self._1l1lllllll_opy_ != 1:
                self.l11lll11lll_opy_.l1ll111l1ll_opy_(self._1l1lllllll_opy_)
            keys = attrs.keys()
            if 'location' in keys:
                self.l11lll11lll_opy_.l11l1lll1ll_opy_(attrs.getValue('location'))

        def l1ll1l11l1l_opy_(self):
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.l11lll11lll_opy_)

        def l111l1l111l_opy_(self):
            self.l11lll11lll_opy_.l1111lll11l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1111lll1l1_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'direction' in keys:
                self.l11lll11lll_opy_.l1l1l1llll1_opy_(attrs.getValue('direction'))

        def l11ll111l11_opy_(self, name, attrs):
            self.l11lll11lll_opy_.l1l11l1l1l1_opy_(True)
            keys = attrs.keys()
            if 'number' in keys:
                self.l11lll11lll_opy_.l11111lllll_opy_(attrs.getValue('number'))
            if 'type' in keys:
                self.l11lll11lll_opy_.l11ll1llll1_opy_(attrs.getValue('type'))

        def l1l11l11l1l_opy_(self, name, attrs):
            self.note.l11lll1l1l1_opy_(True)

        def l1111ll1ll1_opy_(self, name, attrs):
            self.note.l11l1ll1l11_opy_(True)

        def l1111lllll1_opy_(self, name, attrs):
            self.note.l1l111l1l11_opy_(True)

        def l1l1llllll1_opy_(self, name, attrs):
            self.note.l11l11111ll_opy_(True)

        def l11l111lll1_opy_(self, name, attrs):
            self.note.l11l1l1111l_opy_(True)

        def l11ll1ll1l1_opy_(self, name, attrs):
            self.note.l11ll11l111_opy_(True)

        def l111lllll11_opy_(self, name, attrs):
            self.note.l111l11ll1l_opy_(True)
            keys = attrs.keys()
            if 'placement' in keys:
                self.note.l1l11111ll1_opy_(attrs.getValue('placement'))
            if 'long' in keys:
                self.note.l111ll111ll_opy_(attrs.getValue('long'))

        def l11l111ll1l_opy_(self, name, attrs):
            self.note.l111l11111l_opy_(True)
            keys = attrs.keys()
            if 'placement' in keys:
                self.note.l111l1lll11_opy_(attrs.getValue('placement'))
            if 'long' in keys:
                self.note.l1l1lll1ll1_opy_(attrs.getValue('long'))

        def l1l111l1l1l_opy_(self, name, attrs):
            self.note.l11l1l11ll1_opy_(True)
            keys = attrs.keys()
            if 'direction' in keys:
                self.note.l1l1l111111_opy_(attrs.getValue('direction'))

        def l1ll11llll1_opy_(self, name, attrs):
            self.note.l1l11ll111l_opy_(True)
            keys = attrs.keys()
            if 'direction' in keys:
                self.l111lllllll_opy_ = attrs.getValue('direction')
                self.note.l1l1l1l11ll_opy_(self.l111lllllll_opy_)

        def l1111l11l11_opy_(self, name, attrs):
            self.l111l1lllll_opy_ = l1ll11l1lll_opy_()
            self.l111l1lllll_opy_.l1l11llll1l_opy_(True)
            keys = attrs.keys()
            if 'type' in keys:
                self.l111l1lllll_opy_.l1111l111ll_opy_(attrs.getValue('type'))
            self.direction.l1l11l1llll_opy_(self.l111l1lllll_opy_)

        def l1l11l11ll1_opy_(self, name, attrs):
            l1111l1l111_opy_ = l11ll1111l1_opy_()
            l1111l1l111_opy_.l1l1llll11l_opy_(True)
            keys = attrs.keys()
            if 'type' in keys:
                l1111l1l111_opy_.l1l1lll11l1_opy_(attrs.getValue('type'))
            self.direction.l1l11l1llll_opy_(l1111l1l111_opy_)

        def l1l111lll11_opy_(self, name, attrs):
            l1l11l1ll1l_opy_ = l1l1l111l11_opy_()
            l1l11l1ll1l_opy_.l1111ll1111_opy_(True)
            keys = attrs.keys()
            if 'tempo' in keys:
                l1l11l1ll1l_opy_.l111llll111_opy_(attrs.getValue('tempo'))
            if 'dynamics' in keys:
                l1l11l1ll1l_opy_.l11l1l1l111_opy_(attrs.getValue('dynamics'))
            if self.l1l111111ll_opy_[self.l1ll1111ll1_opy_]['is_inside']:
                self.direction.l1l11l1llll_opy_(l1l11l1ll1l_opy_)

        def l11llll111l_opy_(self, name, attrs):
            self.l111l1l11l_opy_ = l111l11llll_opy_()

        def l1ll111l11l_opy_(self):
            self.l111l1l11l_opy_.l111ll11ll1_opy_(self.l11lllll11l_opy_)
            self.l111111l1l_opy_.l1l11l1llll_opy_(self.l111l1l11l_opy_)
            self.__11lll11111_opy_()

        def l11l11l1l11_opy_(self, name, attrs):
            self.l11l1111l1l_opy_ = l1l11ll11l1_opy_()

        def l1l1ll11lll_opy_(self):
            self.l1l11ll11_opy_.l1l11l1llll_opy_(self.l11l1111l1l_opy_)

        def l1l111l1111_opy_(self, name, attrs):
            self.l11111l11l1_opy_ = l111lll1l1l_opy_()

        def l111ll1l111_opy_(self):
            self.l11l1111l1l_opy_.l1l11l1llll_opy_(self.l11111l11l1_opy_)

        def l1l1l11llll_opy_(self):
            self.l11111l11l1_opy_.l11ll1ll111_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11ll11llll_opy_(self, name, attrs):
            self.l1l111ll111_opy_ = l1111l111l1_opy_()
            keys = attrs.keys()
            if 'symbol' in keys:
                self.l111lllllll_opy_ = attrs.getValue('symbol')
                self.l1l111ll111_opy_.l11ll11111l_opy_(self.l111lllllll_opy_)

        def l11ll11ll1l_opy_(self):
            self.l11l1111l1l_opy_.l1l11l1llll_opy_(self.l1l111ll111_opy_)

        def l1l111l1lll_opy_(self):
            self.l1l111ll111_opy_.l1111ll1l11_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l1l111ll_opy_(self):
            self.l1l111ll111_opy_.l1l1ll111l1_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11lll1l11l_opy_(self, name, attrs):
            self.l11l1lll111_opy_ = l11ll11ll11_opy_()

        def l1ll11l11ll_opy_(self):
            self.l1l1l11l1ll_opy_.l1l11l1llll_opy_(self.l11l1lll111_opy_)
            self.l11l1lll111_opy_ = None

        def l1l1l1111ll_opy_(self):
            self.l11l1lll111_opy_.l1l1111l111_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l1l11111111_opy_(self, name, attrs):
            keys = attrs.keys()
            if 'type' in keys:
                self.l11l1lll111_opy_.l1l1ll1lll1_opy_ = attrs.getValue('type')

        def l11ll1ll1ll_opy_(self):
            self.l11l1lll111_opy_.l11l1ll1l1l_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l1111l11_opy_(self):
            self.l1l11lllll1_opy_.l11l111l1ll_opy_(self.l11lllll11l_opy_)
            self.__11lll11111_opy_()

        def l11l1ll1lll_opy_(self, name, attrs):
            self.l1ll111l1l1_opy_ = l1l11ll1111_opy_()

        def l1l11l111l1_opy_(self):
            self.l1l11ll11_opy_.l1l11l1llll_opy_(self.l1ll111l1l1_opy_)

        def l11l1l1ll1l_opy_(self):
            self.l1ll111l1l1_opy_.l1l1l11lll1_opy_(self.l11lllll11l_opy_.replace(" ", " "))
            self.__11lll11111_opy_()

        def l1l1l111ll1_opy_(self):
            self.l1ll111l1l1_opy_.l11ll1lllll_opy_(self.l11lllll11l_opy_.replace(" ", " "))
            self.__11lll11111_opy_()

        def __11lll11111_opy_(self):
            self.l11lllll11l_opy_ = ""

    def l11lll11l11_opy_(self, l11llll11l_opy_, l1l11ll11_opy_):
        t1 = time.time()
        parser = xml.sax.make_parser()
        xml.sax.InputSource.setEncoding(parser, encoding="utf-8")
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = self.l11l1ll11ll_opy_(l11llll11l_opy_, l1l11ll11_opy_, self.l11llll11_opy_, self.l111llllll1_opy_)
        parser.setContentHandler(handler)
        if os.stat(self._1l1ll111_opy_).st_size > 2:
            parser.parse(self._1l1ll111_opy_)
        l1l1111lll_opy_ = time.time()
        print("temps xml to model", l1l1111lll_opy_ - t1)


class l1l111ll1ll_opy_(l11l11l1ll1_opy_):
    def __init__(self, lou, l1l1lllll_opy_, l11llll11_opy_):
        super().__init__(lou, l1l1lllll_opy_, l11llll11_opy_, 'music_xml')


class l1l1llll1l1_opy_(l11l11l1ll1_opy_):
    def __init__(self, lou, l1l1lllll_opy_, l11llll11_opy_):
        super().__init__(lou, l1l1lllll_opy_, l11llll11_opy_, 'music_bxml')
