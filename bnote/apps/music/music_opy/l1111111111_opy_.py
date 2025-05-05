"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import os
import xml.sax
from .l1l1l1ll11_opy_ import *
import time


class l1lll1111111_opy_:
    def __init__(self, lou, l11111l1ll_opy_, l111111l1l_opy_, l1ll1ll1l11l_opy_):
        self.lou = lou
        self._11111ll11_opy_ = l11111l1ll_opy_
        self.l111111l1l_opy_ = l111111l1l_opy_
        self.l1ll1ll1l11l_opy_ = l1ll1ll1l11l_opy_

    class l1l1lll1ll11_opy_(xml.sax.ContentHandler):
        l1lll1llllll_opy_ = "measure"
        l1l1llll11l1_opy_ = "note"
        l1l1llllll1l_opy_ = "chord"
        l1llll1l11ll_opy_ = "grace"
        l1ll1111l111_opy_ = "rest"
        l1lllll11l1l_opy_ = "step"
        l1ll1l111111_opy_ = "alter"
        l1ll1111llll_opy_ = "accidental"
        l1ll1ll11lll_opy_ = "octave"
        l1lll11l1ll1_opy_ = "duration"
        l1lllll111ll_opy_ = "voice"
        l1lll11ll1l1_opy_ = "type"
        l1ll1l11ll1l_opy_ = "dot"
        l1ll1l1llll1_opy_ = "staff"
        l1lll1l1l11l_opy_ = "slur"
        l1lll1l11l1l_opy_ = "credit"
        l1llll1ll11l_opy_ = "credit-type"
        l1ll1ll11111_opy_ = "credit-words"
        l1lll11111ll_opy_ = "score-part"
        l1ll11111lll_opy_ = "part-name"
        l1ll1l1l1111_opy_ = "part-abbreviation"
        l1ll111llll1_opy_ = "score-instrument"
        l1lll111111l_opy_ = "instrument-name"
        l1lll11l1lll_opy_ = "midi-device"
        l1llll1l1lll_opy_ = "midi-instrument"
        l1llll11llll_opy_ = "midi-channel"
        l1l1llll1l11_opy_ = "midi-program"
        l1lll1ll1111_opy_ = "volume"
        l1l1lll1l1ll_opy_ = "pan"
        l1ll1l1ll1l1_opy_ = "part-list"
        l1ll11111l11_opy_ = "part"
        l1ll11ll11l1_opy_ = "attributes"
        l1ll11ll1ll1_opy_ = "divisions"
        l1ll1llll111_opy_ = "key"
        l1lll1111ll1_opy_ = "fifths"
        l1ll1ll11l11_opy_ = "mode"
        l1lll1ll1ll1_opy_ = "time"
        l1ll1llll11l_opy_ = "beats"
        l1l1llll1l1l_opy_ = "beat-type"
        l1ll11111111_opy_ = "staves"
        l1lll1l1111l_opy_ = "clef"
        l1ll11lllll1_opy_ = "sign"
        l1ll1llll1l1_opy_ = "line"
        l1ll11lll11l_opy_ = "clef-octave-change"
        l1ll1ll1llll_opy_ = "braille-clef"
        l1ll1ll1l111_opy_ = "transpose"
        l1l1lll1l1l1_opy_ = "diatonic"
        l1llllll1111_opy_ = "chromatic"
        l1ll11l11ll1_opy_ = "octave-change"
        l1lllll1ll1l_opy_ = "double"
        l1ll1l1l1ll1_opy_ = "metronome"
        l1ll1ll1111l_opy_ = "beat-unit"
        l1llll11ll11_opy_ = "beat-unit-dot"
        l1llll1ll1l1_opy_ = "per-minute"
        l1lll11llll1_opy_ = "fingering"
        l1ll1l1l111l_opy_ = "backup"
        l1ll11l111l1_opy_ = "forward"
        l1ll1l1l11ll_opy_ = "direction"
        l1ll1ll1ll11_opy_ = "p"
        l1llll111l1l_opy_ = "pp"
        l1ll11l1l1ll_opy_ = "ppp"
        l1ll111l1lll_opy_ = "pppp"
        l1ll11l1111l_opy_ = "ppppp"
        l1lll1l1ll1l_opy_ = "pppppp"
        l1l1lllll1l1_opy_ = "f"
        l1lll1l111ll_opy_ = "ff"
        l1ll1ll11l1l_opy_ = "fff"
        l1ll1l1lllll_opy_ = "ffff"
        l1ll1l1lll11_opy_ = "fffff"
        l1ll1lllllll_opy_ = "ffffff"
        l1ll1111ll1l_opy_ = "mp"
        l1llll11l11l_opy_ = "mf"
        l1l1llll111l_opy_ = "sf"
        l1lll1llll11_opy_ = "sfp"
        l1lllll111l1_opy_ = "sfpp"
        l1ll1l1ll11l_opy_ = "fp"
        l1lll1lll11l_opy_ = "rf"
        l1ll1ll1ll1l_opy_ = "rfz"
        l1llll111111_opy_ = "sfz"
        l1ll1lll1l1l_opy_ = "sffz"
        l1lll1111l11_opy_ = "fz"
        N = "n"
        l1ll11ll111l_opy_ = "pf"
        l1ll1l1ll1ll_opy_ = "sfzp"
        l1ll111l1l1l_opy_ = "other-dynamics"
        l1ll1ll111l1_opy_ = "words"
        l1ll1lll11l1_opy_ = "actual-notes"
        l1lll1ll111l_opy_ = "normal-notes"
        l1lll11l1l1l_opy_ = "print"
        l1lll111l1l1_opy_ = "staff-layout"
        l1lll1ll1l1l_opy_ = "lyric"
        l1ll11l1ll11_opy_ = "syllabic"
        l1ll11llll11_opy_ = "text"
        l1ll111lll11_opy_ = "tie"
        l1lllll11l11_opy_ = "barline"
        l1ll1111ll11_opy_ = "bar-style"
        REPEAT = "repeat"
        l1lll1l1l1ll_opy_ = "ending"
        l1lll1111l1l_opy_ = "staccato"
        l1ll11ll11ll_opy_ = "staccatissimo"
        l1ll1ll11ll1_opy_ = "accent"
        l1llll1l1l11_opy_ = "breath-mark"
        l1llll1l11l1_opy_ = "fermata"
        l1ll11llllll_opy_ = "trill-mark"
        l1l1lllll11l_opy_ = "inverted-mordent"
        l1ll1lll1lll_opy_ = "mordent"
        l1ll1111l1l1_opy_ = "arpeggiate"
        l1lll1l11ll1_opy_ = "two-hands-arpeggiate"
        l1ll1lll111l_opy_ = "pedal"
        l1ll1l1ll111_opy_ = "wedge"
        l1ll1ll111ll_opy_ = "sound"
        l1lll11l111l_opy_ = "karaoke"
        l1ll111lll1l_opy_ = "braille-global"
        l1lll111l1ll_opy_ = "global-key"
        l1lll1l11lll_opy_ = "global-fifths"
        l1ll11llll1l_opy_ = "global-time"
        l1ll1lll1111_opy_ = "global-beats"
        l1ll1lll1l11_opy_ = "global-beat-type"
        l1lll1l1l111_opy_ = "global-symbol"
        l1ll11l11lll_opy_ = "measure-style"
        l1lll111ll1l_opy_ = "multiple-rest"
        l1ll1111111l_opy_ = "measure-repeat"
        l1ll1l11l1l1_opy_ = "braille-ascending-chords"
        l1ll1l1lll1l_opy_ = "work"
        l1lll11l1l11_opy_ = "work-number"
        l1l1llll1111_opy_ = "work-title"
        l1llll11lll1_opy_ = (
            l1lllll11l1l_opy_,
            l1ll1l111111_opy_,
            l1ll1111llll_opy_,
            l1ll1ll11lll_opy_,
            l1lll11l1ll1_opy_,
            l1lllll111ll_opy_,
            l1lll11ll1l1_opy_,
            l1ll1l1llll1_opy_,
            l1llll1ll11l_opy_,
            l1ll1ll11111_opy_,
            l1ll11ll1ll1_opy_,
            l1lll1111ll1_opy_,
            l1ll1ll11l11_opy_,
            l1ll1llll11l_opy_,
            l1l1llll1l1l_opy_,
            l1ll11111111_opy_,
            l1ll11lllll1_opy_,
            l1ll1llll1l1_opy_,
            l1ll11lll11l_opy_,
            l1ll1ll1llll_opy_,
            l1l1lll1l1l1_opy_,
            l1llllll1111_opy_,
            l1ll11l11ll1_opy_,
            l1ll1ll1111l_opy_,
            l1llll1ll1l1_opy_,
            l1lll11llll1_opy_,
            l1ll11111lll_opy_,
            l1ll1l1l1111_opy_,
            l1lll111111l_opy_,
            l1llll11llll_opy_,
            l1l1llll1l11_opy_,
            l1lll1ll1111_opy_,
            l1l1lll1l1ll_opy_,
            l1ll1ll111l1_opy_,
            l1ll1lll11l1_opy_,
            l1lll1ll111l_opy_,
            l1ll11l1ll11_opy_,
            l1ll11llll11_opy_,
            l1ll1111ll11_opy_,
            l1lll11l111l_opy_,
            l1lll1l11lll_opy_,
            l1ll1lll1111_opy_,
            l1ll1lll1l11_opy_,
            l1lll111ll1l_opy_,
            l1ll1111111l_opy_,
            l1ll1l11l1l1_opy_,
            l1lll11l1l11_opy_,
            l1l1llll1111_opy_,
        )

        def __init__(
            self, l1l1l111_opy_, l1ll1111l1_opy_, l1lll11l1111_opy_, l1ll1ll1l11l_opy_
        ):
            self._1llll111_opy_ = l1l1l111_opy_
            self.l1ll1111l1_opy_ = l1ll1111l1_opy_
            self._1ll11l1llll_opy_ = l1lll11l1111_opy_
            self.l1ll1ll1l11l_opy_ = l1ll1ll1l11l_opy_
            self.l1lll11_opy_ = None
            self.note = None
            self.l1lll1111lll_opy_ = None
            self.l11lll111_opy_ = None
            self.l1llll1l1l1l_opy_ = None
            self.l111l1l_opy_ = None
            self.part = None
            self.l11l11_opy_ = None
            self.l1lll11111_opy_ = None
            self.time = None
            self.l1lll1l11_opy_ = None
            self.l11l111ll_opy_ = None
            self.l1l1l1ll1l_opy_ = None
            self.l1l11ll11l_opy_ = None
            self.l11111lll_opy_ = None
            self.forward = None
            self.key = None
            self.l1ll1l1l11_opy_ = None
            self.words = None
            self._1lllll11111_opy_ = 1
            self.l1lll111l111_opy_ = False
            self.l111ll_opy_ = None
            self.l1lll1111_opy_ = None
            self.l1111l1ll_opy_ = None
            self.l1lllll1ll_opy_ = None
            self.l1ll11l1111_opy_ = None
            self.l111l1l11_opy_ = None
            self.l1l1lllll111_opy_ = ""
            self.l1llll111l11_opy_ = list()
            self.l1lllll1llll_opy_ = {
                self.l1lll1llllll_opy_: {
                    "start_element_fn": self.l1ll111l11l1_opy_,
                    "end_element_fn": self.l1ll1l1l1l1l_opy_,
                    "is_inside": False,
                },
                self.l1l1llll11l1_opy_: {
                    "start_element_fn": self.l1lll1l111l1_opy_,
                    "end_element_fn": self.l1ll1l1l11l1_opy_,
                    "is_inside": False,
                },
                self.l1lllll11l1l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lllll1l111_opy_,
                    "is_inside": False,
                },
                self.l1ll1111l111_opy_: {
                    "start_element_fn": self.l1l1lllllll1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1l1llllll1l_opy_: {
                    "start_element_fn": self.l1ll11lll1l1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll1l11ll_opy_: {
                    "start_element_fn": self.l1lllll1l1l1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l11ll1l_opy_: {
                    "start_element_fn": self.l1lllll1l1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l111111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11ll1111_opy_,
                    "is_inside": False,
                },
                self.l1ll1111llll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1llllll1_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll11lll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll1ll1ll_opy_,
                    "is_inside": False,
                },
                self.l1lll11l1ll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11111l1l_opy_,
                    "is_inside": False,
                },
                self.l1lllll111ll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll111l11l_opy_,
                    "is_inside": False,
                },
                self.l1lll11ll1l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1l111l11_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1llll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll1llll1l_opy_,
                    "is_inside": False,
                },
                self.l1lll1l1l11l_opy_: {
                    "start_element_fn": self.l1lll1lll1l1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1l11l1l_opy_: {
                    "start_element_fn": self.l1ll1ll1l1l1_opy_,
                    "end_element_fn": self.l1lll11ll11l_opy_,
                    "is_inside": False,
                },
                self.l1llll1ll11l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lllll1lll1_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll11111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll111ll111_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1ll1l1_opy_: {
                    "start_element_fn": self.l1llllll11ll_opy_,
                    "end_element_fn": self.l1ll11l11111_opy_,
                    "is_inside": False,
                },
                self.l1lll11111ll_opy_: {
                    "start_element_fn": self.l1ll111l111l_opy_,
                    "end_element_fn": self.l1ll11111ll1_opy_,
                    "is_inside": False,
                },
                self.l1ll11111lll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1l1llll11ll_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1l1111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1111lll1_opy_,
                    "is_inside": False,
                },
                self.l1ll111llll1_opy_: {
                    "start_element_fn": self.l1lll11lll11_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll111111l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1l1lll1lll1_opy_,
                    "is_inside": False,
                },
                self.l1lll11l1lll_opy_: {
                    "start_element_fn": self.l1lll1ll1l11_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll1l1lll_opy_: {
                    "start_element_fn": self.l1lllll1ll11_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll11llll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1l11l11l_opy_,
                    "is_inside": False,
                },
                self.l1l1llll1l11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll1l111l_opy_,
                    "is_inside": False,
                },
                self.l1lll1ll1111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11l1l11l_opy_,
                    "is_inside": False,
                },
                self.l1l1lll1l1ll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1lll11ll_opy_,
                    "is_inside": False,
                },
                self.l1ll11111l11_opy_: {
                    "start_element_fn": self.l1lll11ll111_opy_,
                    "end_element_fn": self.l1lll1ll11l1_opy_,
                    "is_inside": False,
                },
                self.l1ll11ll11l1_opy_: {
                    "start_element_fn": self.l1ll1l1l1lll_opy_,
                    "end_element_fn": self.l1ll111l11ll_opy_,
                    "is_inside": False,
                },
                self.l1ll11ll1ll1_opy_: {
                    "start_element_fn": self.l1ll1ll1l1ll_opy_,
                    "end_element_fn": self.l1llll111ll1_opy_,
                    "is_inside": False,
                },
                self.l1lll1111ll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll111ll11_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll11l11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1l1111l1_opy_,
                    "is_inside": False,
                },
                self.l1lll1ll1ll1_opy_: {
                    "start_element_fn": self.l1llll1llll1_opy_,
                    "end_element_fn": self.l1l1lll1l11l_opy_,
                    "is_inside": False,
                },
                self.l1ll1llll11l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11l1ll1l_opy_,
                    "is_inside": False,
                },
                self.l1l1llll1l1l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1ll1lll1_opy_,
                    "is_inside": False,
                },
                self.l1ll11111111_opy_: {
                    "start_element_fn": self.l1ll1l11ll11_opy_,
                    "end_element_fn": self.l1ll111111l1_opy_,
                    "is_inside": False,
                },
                self.l1lll1l1111l_opy_: {
                    "start_element_fn": self.l1lllll11lll_opy_,
                    "end_element_fn": self.l1l1lll1ll1l_opy_,
                    "is_inside": False,
                },
                self.l1ll11lllll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11ll1lll_opy_,
                    "is_inside": False,
                },
                self.l1ll1llll1l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11ll1l1l_opy_,
                    "is_inside": False,
                },
                self.l1ll11lll11l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll11lllll_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll1l111_opy_: {
                    "start_element_fn": self.l1llllll111l_opy_,
                    "end_element_fn": self.l1ll1l111l1l_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll1llll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll1ll11ll_opy_,
                    "is_inside": False,
                },
                self.l1l1lll1l1l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll1l11l11_opy_,
                    "is_inside": False,
                },
                self.l1llllll1111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll11ll1l_opy_,
                    "is_inside": False,
                },
                self.l1ll11l11ll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll1l1111_opy_,
                    "is_inside": False,
                },
                self.l1lllll1ll1l_opy_: {
                    "start_element_fn": self.l1l1llllll11_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1l1ll1_opy_: {
                    "start_element_fn": self.l1llll1111l1_opy_,
                    "end_element_fn": self.l1ll111ll11l_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll1111l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1l11l111_opy_,
                    "is_inside": False,
                },
                self.l1llll11ll11_opy_: {
                    "start_element_fn": self.l1ll1lllll1l_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll1ll1l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll1ll111_opy_,
                    "is_inside": False,
                },
                self.l1lll11llll1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll11l1l111_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1l111l_opy_: {
                    "start_element_fn": self.l1lll1lll1ll_opy_,
                    "end_element_fn": self.l1lll11111l1_opy_,
                    "is_inside": False,
                },
                self.l1ll11l111l1_opy_: {
                    "start_element_fn": self.l1ll11l111ll_opy_,
                    "end_element_fn": self.l1ll1l11llll_opy_,
                    "is_inside": False,
                },
                self.l1ll1llll111_opy_: {
                    "start_element_fn": self.l1ll1l11111l_opy_,
                    "end_element_fn": self.l1ll111ll1l1_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1l11ll_opy_: {
                    "start_element_fn": self.l1lll11l11l1_opy_,
                    "end_element_fn": self.l1ll111l1l11_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll111l1_opy_: {
                    "start_element_fn": self.l1ll1l1l1l11_opy_,
                    "end_element_fn": self.l1lllll11ll1_opy_,
                    "is_inside": False,
                },
                self.l1ll1ll1ll11_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll111l1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11l1l1ll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll111l1lll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11l1111l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1l1ll1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1l1lllll1l1_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1l111ll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1ll11l1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1lllll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1lll11_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1lllllll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1111ll1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll11l11l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1l1llll111l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1llll11_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lllll111l1_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1ll11l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1lll11l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1ll1ll1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll111111_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1lll1l1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1111l11_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.N: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11ll111l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1ll1ll_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll111l1l1l_opy_: {
                    "start_element_fn": self.l1lll11ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1lll11l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1l1llllllll_opy_,
                    "is_inside": False,
                },
                self.l1lll1ll111l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll1l1llll_opy_,
                    "is_inside": False,
                },
                self.l1lll11l1l1l_opy_: {
                    "start_element_fn": self.l1lll1lll111_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll111l1l1_opy_: {
                    "start_element_fn": self.l1llll1111ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1ll1l1l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11l1ll11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll11l11ll_opy_,
                    "is_inside": False,
                },
                self.l1ll11llll11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll1l1ll11_opy_,
                    "is_inside": False,
                },
                self.l1ll111lll11_opy_: {
                    "start_element_fn": self.l1lllll1l11l_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lllll11l11_opy_: {
                    "start_element_fn": self.l1llll11l1l1_opy_,
                    "end_element_fn": self.l1ll11l11l11_opy_,
                    "is_inside": False,
                },
                self.l1ll1111ll11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1lll111lll1_opy_,
                    "is_inside": False,
                },
                self.REPEAT: {
                    "start_element_fn": self.l1ll1l111lll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1l1l1ll_opy_: {
                    "start_element_fn": self.l1l1lll1l111_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1111l1l_opy_: {
                    "start_element_fn": self.l1ll1l1111ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11ll11ll_opy_: {
                    "start_element_fn": self.l1ll11lll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1ll11ll1_opy_: {
                    "start_element_fn": self.l1llll111lll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll1l1l11_opy_: {
                    "start_element_fn": self.l1ll1l111ll1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1llll1l11l1_opy_: {
                    "start_element_fn": self.l1lll11lll1l_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll11llllll_opy_: {
                    "start_element_fn": self.l1ll11l11l1l_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1l1lllll11l_opy_: {
                    "start_element_fn": self.l1ll111ll1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1lll1lll_opy_: {
                    "start_element_fn": self.l1ll1l11lll1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1111l1l1_opy_: {
                    "start_element_fn": self.l1lll1lllll1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll1l11ll1_opy_: {
                    "start_element_fn": self.l1lll1l11111_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1lll111l_opy_: {
                    "start_element_fn": self.l1ll11l1l1l1_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1l1ll111_opy_: {
                    "start_element_fn": self.l1ll1l11l1ll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1ll1ll111ll_opy_: {
                    "start_element_fn": self.l1l1lll1llll_opy_,
                    "end_element_fn": None,
                    "is_inside": False,
                },
                self.l1lll11l111l_opy_: {
                    "start_element_fn": self.l1lllll1111l_opy_,
                    "end_element_fn": self.l1ll1lll1ll1_opy_,
                    "is_inside": False,
                },
                self.l1ll111lll1l_opy_: {
                    "start_element_fn": self.l1ll111l1111_opy_,
                    "end_element_fn": self.l1ll1llll1ll_opy_,
                    "is_inside": False,
                },
                self.l1lll111l1ll_opy_: {
                    "start_element_fn": self.l1ll111111ll_opy_,
                    "end_element_fn": self.l1llll1lll1l_opy_,
                    "is_inside": False,
                },
                self.l1lll1l11lll_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll11l1ll_opy_,
                    "is_inside": False,
                },
                self.l1ll11llll1l_opy_: {
                    "start_element_fn": self.l1lll1l1lll1_opy_,
                    "end_element_fn": self.l1l1llll1ll1_opy_,
                    "is_inside": False,
                },
                self.l1ll1lll1111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll1lllll11_opy_,
                    "is_inside": False,
                },
                self.l1ll1lll1l11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll111lllll_opy_,
                    "is_inside": False,
                },
                self.l1ll11l11lll_opy_: {
                    "start_element_fn": self.l1llll1lll11_opy_,
                    "end_element_fn": self.l1lll1ll1lll_opy_,
                    "is_inside": False,
                },
                self.l1lll111ll1l_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll11111l_opy_,
                    "is_inside": False,
                },
                self.l1ll1111111l_opy_: {
                    "start_element_fn": self.l1ll11ll1l11_opy_,
                    "end_element_fn": self.l1llllll11l1_opy_,
                    "is_inside": False,
                },
                self.l1ll1l11l1l1_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1l1lllll1ll_opy_,
                    "is_inside": False,
                },
                self.l1ll1l1lll1l_opy_: {
                    "start_element_fn": self.l1llll1lllll_opy_,
                    "end_element_fn": self.l1ll11l1lll1_opy_,
                    "is_inside": False,
                },
                self.l1lll11l1l11_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1llll11l111_opy_,
                    "is_inside": False,
                },
                self.l1l1llll1111_opy_: {
                    "start_element_fn": None,
                    "end_element_fn": self.l1ll111l1ll1_opy_,
                    "is_inside": False,
                },
            }

        def startDocument(self):
            self.l11111_opy_ = False
            if self.l11111_opy_:
                self._1llll111_opy_(
                    "Texts to find\nxml to model score\nOptimize model score2, chord assign\nOptimize model score2, with measure position\nmodel to braille\n\nStart reading xml file"
                )

        def endDocument(self):
            if self.l11111_opy_:
                self._1llll111_opy_("End reading xml file\n")
                self._1llll111_opy_("xml to model score, first extraction")
                self._1llll111_opy_(str(self.l1ll1111l1_opy_))

        def startElement(self, name, attrs):
            if name in self.l1lllll1llll_opy_.keys():
                # print(f"key found {name=}!")
                l1ll1111l1ll_opy_ = self.l1lllll1llll_opy_[name]
                l1ll1111l1ll_opy_["is_inside"] = True
                if l1ll1111l1ll_opy_["start_element_fn"] is not None:
                    l1ll1111l1ll_opy_["start_element_fn"](name, attrs)

        def endElement(self, name):
            if name in self.l1lllll1llll_opy_.keys():
                l1ll1111l1ll_opy_ = self.l1lllll1llll_opy_[name]
                l1ll1111l1ll_opy_["is_inside"] = False
                if l1ll1111l1ll_opy_["end_element_fn"] is not None:
                    l1ll1111l1ll_opy_["end_element_fn"]()

        def l1ll1111l11l_opy_(self, elements):
            for element in elements:
                if self.l1lllll1llll_opy_[element]["is_inside"]:
                    return True
            return False

        def characters(self, content):
            if self.l1ll1111l11l_opy_(self.l1llll11lll1_opy_):
                self.l1l1lllll111_opy_ += content

        def l1ll111l11l1_opy_(self, name, attrs):
            self.l1lll11_opy_ = l1l11l_opy_()
            self._1lllll11111_opy_ = 1
            keys = attrs.keys()
            if "number" in keys:
                self.l1lll11_opy_.l1ll11ll_opy_(attrs.getValue("number"))
                if self.l11111_opy_:
                    print("mesure", attrs.getValue("number"))

        def l1ll1l1l1l1l_opy_(self):
            self.part.l1l1l11ll_opy_(self.l1lll11_opy_)
            self.l1lll11_opy_ = None

        def l1lll1l111l1_opy_(self, name, attrs):
            self.note = l11lll1ll_opy_()
            if self._1lllll11111_opy_ != 1:
                self.note.l111111llll_opy_(self._1lllll11111_opy_)

        def l1ll1l1l11l1_opy_(self):
            self.note.l1111l1l1ll_opy_()
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.note)
            self.note = None

        def l1lllll1l111_opy_(self):
            self.note.l1111lll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1l1lllllll1_opy_(self, name, attrs):
            self.note.rest = True

        def l1ll11lll1l1_opy_(self, name, attrs):
            self.note.l111l11l1_opy_ = True

        def l1lllll1l1l1_opy_(self, name, attrs):
            self.note.l1llllllll_opy_ = True
            keys = attrs.keys()
            if "slash" in keys:
                self.note.l1l1l1l111_opy_ = attrs.getValue("slash")

        def l1lllll1l1ll_opy_(self, name, attrs):
            self.note.dot = True

        def l1ll11ll1111_opy_(self):
            self.note.l1l1l11l1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1llllll1_opy_(self):
            self.note.l1ll1l1l_opy_ = self.l1l1lllll111_opy_
            self.__1lll1l1l1l1_opy_()

        def l1llll1ll1ll_opy_(self):
            self.note.l11lllll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll11111l1l_opy_(self):
            if self.l1lllll1llll_opy_[self.l1ll1l1l111l_opy_]["is_inside"]:
                self.l11111lll_opy_.l111lll1_opy_(self.l1l1lllll111_opy_)
            if self.l1lllll1llll_opy_[self.l1ll11l111l1_opy_]["is_inside"]:
                self.forward.l111lll1_opy_(self.l1l1lllll111_opy_)
            elif self.l1lllll1llll_opy_[self.l1l1llll11l1_opy_]["is_inside"]:
                self.note.l111lll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll111l11l_opy_(self):
            if self.l1lllll1llll_opy_[self.l1l1llll11l1_opy_]["is_inside"]:
                self.note.l1l111l1ll_opy_(self.l1l1lllll111_opy_)
                self._1lllll11111_opy_ = self.l1l1lllll111_opy_
            self.__1lll1l1l1l1_opy_()

        def l1ll1l111l11_opy_(self):
            self.note.set_type(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1llll1l_opy_(self):
            if self.l1lllll1llll_opy_[self.l1l1llll11l1_opy_]["is_inside"]:
                self.note.l1ll111lll_opy_(self.l1l1lllll111_opy_)
            if self.l1lllll1llll_opy_[self.l1ll1l1l11ll_opy_]["is_inside"]:
                self.l1ll1l1l11_opy_.l1ll111lll_opy_(self.l1l1lllll111_opy_)
            if self.l1lllll1llll_opy_[self.l1ll1ll111l1_opy_]["is_inside"]:
                self.words.l1ll111lll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1lll1l1_opy_(self, name, attrs):
            self.note.l111l111l_opy_ = True
            keys = attrs.keys()
            if "placement" in keys:
                self.note.l1l1l11l1l_opy_ = attrs.getValue("placement")
            if "number" in keys:
                self.note.l11ll1_opy_(attrs.getValue("number"))
            if "type" in keys:
                self.note.l11111l11_opy_ = attrs.getValue("type")

        def l1ll1ll1l1l1_opy_(self, name, attrs):
            self.l11lll111_opy_ = l11l1l_opy_()

        def l1lll11ll11l_opy_(self):
            self.l1ll1111l1_opy_.l1ll1ll1l1_opy_(self.l11lll111_opy_)

        def l1lllll1lll1_opy_(self):
            self.l11lll111_opy_.l11ll11l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll111ll111_opy_(self):
            self.l11lll111_opy_.l11111ll_opy_(self.l1l1lllll111_opy_.replace(" ", " "))
            self.__1lll1l1l1l1_opy_()

        def l1llllll11ll_opy_(self, name, attrs):
            self.l1llll1l1l1l_opy_ = l11l1ll_opy_()

        def l1ll11l11111_opy_(self):
            self.l1ll1111l1_opy_.l1ll1ll1l1_opy_(self.l1llll1l1l1l_opy_)
            self.l1llll1l1l1l_opy_ = None

        def l1ll111l111l_opy_(self, name, attrs):
            self.l111l1l_opy_ = l1l1lllll1_opy_()
            self.l111l1l_opy_.l1ll1l1ll_opy_(
                self._1ll11l1llll_opy_[self.l1ll1ll1l11l_opy_]["ascending_chords"]
            )
            keys = attrs.keys()
            if "id" in keys:
                self.l111l1l_opy_.l11ll1ll_opy_(attrs.getValue("id"))

        def l1ll11111ll1_opy_(self):
            self.l1llll1l1l1l_opy_.l11l1l1_opy_(self.l111l1l_opy_)

        def l1l1llll11ll_opy_(self):
            l1lll111llll_opy_ = False
            if self.l1l1lllll111_opy_ == "":
                self.l1l1lllll111_opy_ = "default"
            for i in self.l1llll111l11_opy_:
                if self.l1l1lllll111_opy_ in i[0]:
                    i[1] += 1
                    self.l111l1l_opy_.l1l1lllll_opy_(
                        self.l1l1lllll111_opy_.replace("♭", "flat") + str(i[1])
                    )
                    l1lll111llll_opy_ = True
            if not l1lll111llll_opy_:
                self.l111l1l_opy_.l1l1lllll_opy_(
                    self.l1l1lllll111_opy_.replace("♭", "flat")
                )
                self.l1llll111l11_opy_.append([self.l1l1lllll111_opy_, 1])
            if self.l1l1lllll111_opy_ in [
                "Br Piano right hand",
                "Br Piano solo",
                "Brd Piano left hand",
            ]:
                self.l111l1l_opy_.l1ll1l1ll_opy_(False)
            elif self.l1l1lllll111_opy_ in [
                "Br Piano left hand",
                "Br Organ pedal",
                "Bru Piano right hand",
            ]:
                self.l111l1l_opy_.l1ll1l1ll_opy_(True)
            self.__1lll1l1l1l1_opy_()

        def l1ll1111lll1_opy_(self):
            self.l111l1l_opy_.l1l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll11lll11_opy_(self, name, attrs):
            keys = attrs.keys()
            if "id" in keys:
                self.l111l1l_opy_.l1l111lll_opy_(attrs.getValue("id"))

        def l1l1lll1lll1_opy_(self):
            self.l111l1l_opy_.l1l1ll11ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1ll1l11_opy_(self, name, attrs):
            keys = attrs.keys()
            if "id" in keys:
                self.l111l1l_opy_.l1l111ll1_opy_(attrs.getValue("id"))
            if "port" in keys:
                self.l111l1l_opy_.l1lll1l1l1_opy_(attrs.getValue("port"))

        def l1lllll1ll11_opy_(self, name, attrs):
            keys = attrs.keys()
            if "id" in keys:
                self.l111l1l_opy_.l1111l11l_opy_(attrs.getValue("id"))

        def l1ll1l11l11l_opy_(self):
            self.l111l1l_opy_.l1l1lll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll1l111l_opy_(self):
            self.l111l1l_opy_.l1l1ll111l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll11l1l11l_opy_(self):
            self.l111l1l_opy_.l1llll11l1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1lll11ll_opy_(self):
            self.l111l1l_opy_.l1lll1ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll11ll111_opy_(self, name, attrs):
            self.part = l11ll1l1l_opy_()
            keys = attrs.keys()
            if "id" in keys:
                self.part.l11ll1ll_opy_(attrs.getValue("id"))
                if self.l11111_opy_:
                    print("partie", attrs.getValue("id"))

        def l1lll1ll11l1_opy_(self):
            self.l1ll1111l1_opy_.l1ll1ll1l1_opy_(self.part)
            self.part = None

        def l1ll1l1l1lll_opy_(self, name, attrs):
            self.l11l11_opy_ = l11l1lll1_opy_()
            if self._1lllll11111_opy_ != 1:
                self.l11l11_opy_.l111111llll_opy_(self._1lllll11111_opy_)

        def l1ll111l11ll_opy_(self):
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.l11l11_opy_)
            self.l11l11_opy_ = None

        def l1ll1ll1l1ll_opy_(self, name, attrs):
            self.l1lll11111_opy_ = l11ll11ll_opy_()

        def l1llll111ll1_opy_(self):
            self.l1lll11111_opy_.l1llll111l_opy_(self.l1l1lllll111_opy_)
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.l1lll11111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll111ll11_opy_(self):
            self.key.l1l11lll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1l1111l1_opy_(self):
            self.key.l1111111l1l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll1llll1_opy_(self, name, attrs):
            self.time = l111ll11_opy_()
            keys = attrs.keys()
            if "symbol" in keys:
                self.time.l1lllll111_opy_(attrs.getValue("symbol"))

        def l1l1lll1l11l_opy_(self):
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.time)
            self.time = None

        def l1ll11l1ll1l_opy_(self):
            self.time.l1llllll11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1ll1lll1_opy_(self):
            self.time.l11ll1l11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1l11ll11_opy_(self, name, attrs):
            self.l1lll1l11_opy_ = l1111l1l111_opy_()

        def l1ll111111l1_opy_(self):
            self.l1lll1l11_opy_.l1111l1llll_opy_(self.l1l1lllll111_opy_)
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.l1lll1l11_opy_)
            self.__1lll1l1l1l1_opy_()
            self.l1lll1l11_opy_ = None

        def l1lllll11lll_opy_(self, name, attrs):
            self.l11l111ll_opy_ = l1lllllll1_opy_()
            keys = attrs.keys()
            if "number" in keys:
                self.l11l111ll_opy_.l1111l1l1l1_opy_(attrs.getValue("number"))

        def l1l1lll1ll1l_opy_(self):
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.l11l111ll_opy_)
            self.l11l111ll_opy_ = None

        def l1ll11ll1lll_opy_(self):
            self.l11l111ll_opy_.l1l1ll1l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll11ll1l1l_opy_(self):
            self.l11l111ll_opy_.l1lll1l1ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll11lllll_opy_(self):
            self.l11l111ll_opy_.l11ll111_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llllll111l_opy_(self, name, attrs):
            self.l1l1l1ll1l_opy_ = l111lll11_opy_()

        def l1ll1l111l1l_opy_(self):
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.l1l1l1ll1l_opy_)
            self.l1l1l1ll1l_opy_ = None

        def l1lll1ll11ll_opy_(self):
            self.l11l111ll_opy_.l1llll1l11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1l11l11_opy_(self):
            self.l1l1l1ll1l_opy_.l1l1111_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll11ll1l_opy_(self):
            self.l1l1l1ll1l_opy_.l11l111l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll1l1111_opy_(self):
            self.l1l1l1ll1l_opy_.l1ll11lll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1l1llllll11_opy_(self, name, attrs):
            self.l1l1l1ll1l_opy_.l1l1l11l_opy_(True)
            keys = attrs.keys()
            if "above" in keys:
                self.l1l1l1ll1l_opy_.l1l1lll_opy_(attrs.getValue("above"))

        def l1llll1111l1_opy_(self, name, attrs):
            self.l1l11ll11l_opy_ = l1l11ll_opy_()
            keys = attrs.keys()
            if "parentheses" in keys:
                self.l1l11ll11l_opy_.l1111l11l1l_opy_(attrs.getValue("parentheses"))

        def l1ll111ll11l_opy_(self):
            self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(self.l1l11ll11l_opy_)

        def l1ll1l11l111_opy_(self):
            self.l1l11ll11l_opy_.l1l1llll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1lllll1l_opy_(self, name, attrs):
            self.l1l11ll11l_opy_.l1llllll1_opy_(True)

        def l1llll1ll111_opy_(self):
            self.l1l11ll11l_opy_.l1llll1111_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll11l1l111_opy_(self):
            self.note.l1ll1l11_opy_ = self.l1l1lllll111_opy_
            self.__1lll1l1l1l1_opy_()

        def l1lll1lll1ll_opy_(self, name, attrs):
            self.l11111lll_opy_ = l1l1ll1ll1_opy_()
            self._1lllll11111_opy_ = 2
            self.l11111lll_opy_.l111111llll_opy_(2)
            if self._1lllll11111_opy_ != 1:
                self.l11111lll_opy_.l111111llll_opy_(self._1lllll11111_opy_)

        def l1lll11111l1_opy_(self):
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.l11111lll_opy_)
            self.l11111lll_opy_ = None

        def l1ll11l111ll_opy_(self, name, attrs):
            self.forward = l1111l111ll_opy_()

        def l1ll1l11llll_opy_(self):
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.forward)
            self.forward = None

        def l1ll1l11111l_opy_(self, name, attrs):
            self.key = l1l11l111_opy_()

        def l1ll111ll1l1_opy_(self):
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.key)
            self.key = None

        def l1lll11l11l1_opy_(self, name, attrs):
            self.l1ll1l1l11_opy_ = l1lllll1_opy_()
            if self._1lllll11111_opy_ != 1:
                self.l1ll1l1l11_opy_.l111111llll_opy_(self._1lllll11111_opy_)
            keys = attrs.keys()
            if "placement" in keys:
                self.l1ll1l1l11_opy_.l1111l1l11l_opy_(attrs.getValue("placement"))

        def l1ll111l1l11_opy_(self):
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.l1ll1l1l11_opy_)

        def l1ll1l1l1l11_opy_(self, name, attrs):
            self.words = l1l11ll1l_opy_()
            self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(self.words)

        def l1lllll11ll1_opy_(self):
            self.words.l1l11_opy_(self.l1l1lllll111_opy_.replace(" ", " "))
            self.__1lll1l1l1l1_opy_()

        def l1lll11ll1ll_opy_(self, name, attrs):
            l11lll_opy_ = l111l11l_opy_()
            l11lll_opy_.l1lll1llll_opy_(name)
            self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(l11lll_opy_)

        def l1l1llllllll_opy_(self):
            self.note.l1l11ll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1l1llll_opy_(self):
            self.note.l1l1llll11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1lll111_opy_(self, name, attrs):
            l1llll1l1ll1_opy_ = l11l1_opy_()
            keys = attrs.keys()
            if "new-system" in keys:
                l1llll1l1ll1_opy_.l1l1l1l1l1_opy_(attrs.getValue("new-system"))
            self.l1lll11_opy_.l1ll1ll1l1_opy_(l1llll1l1ll1_opy_)

        def l1llll1111ll_opy_(self, name, attrs):
            l1llll1l1ll1_opy_ = l11l1_opy_()
            keys = attrs.keys()
            if "number" in keys:
                l1llll1l1ll1_opy_.l11111lll1l_opy_(attrs.getValue("number"))
            if self.l1lll11_opy_ is not None:
                self.l1lll11_opy_.l1ll1ll1l1_opy_(l1llll1l1ll1_opy_)

        def l1lll11l11ll_opy_(self):
            self.note.l1l1l111ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1l1ll11_opy_(self):
            self.note.l1ll1llll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lllll1l11l_opy_(self, name, attrs):
            keys = attrs.keys()
            if "type" in keys:
                self.note.l1l1lll111_opy_(attrs.getValue("type"))
            self.note.l1l1ll11l1_opy_(True)

        def l1llll11l1l1_opy_(self, name, attrs):
            self.l1lll1111lll_opy_ = l1ll11l_opy_()
            if self._1lllll11111_opy_ != 1:
                self.l1lll1111lll_opy_.l111111llll_opy_(self._1lllll11111_opy_)
            keys = attrs.keys()
            if "location" in keys:
                self.l1lll1111lll_opy_.l1ll1l11l1_opy_(attrs.getValue("location"))

        def l1ll11l11l11_opy_(self):
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.l1lll1111lll_opy_)

        def l1lll111lll1_opy_(self):
            self.l1lll1111lll_opy_.l1l1l1l1ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll1l111lll_opy_(self, name, attrs):
            keys = attrs.keys()
            if "direction" in keys:
                self.l1lll1111lll_opy_.l11111l1l_opy_(attrs.getValue("direction"))

        def l1l1lll1l111_opy_(self, name, attrs):
            self.l1lll1111lll_opy_.l11llll_opy_(True)
            keys = attrs.keys()
            if "number" in keys:
                self.l1lll1111lll_opy_.l1ll1111_opy_(attrs.getValue("number"))
            if "type" in keys:
                self.l1lll1111lll_opy_.l1lll11ll_opy_(attrs.getValue("type"))

        def l1ll1l1111ll_opy_(self, name, attrs):
            self.note.l111_opy_(True)

        def l1ll11lll1ll_opy_(self, name, attrs):
            self.note.l1ll1l111_opy_(True)

        def l1llll111lll_opy_(self, name, attrs):
            self.note.l11ll1l1_opy_(True)

        def l1ll1l111ll1_opy_(self, name, attrs):
            self.note.l11111l11ll_opy_(True)

        def l1lll11lll1l_opy_(self, name, attrs):
            self.note.l1ll1l11ll_opy_(True)

        def l1ll11l11l1l_opy_(self, name, attrs):
            self.note.l1ll11l11l_opy_(True)

        def l1ll111ll1ll_opy_(self, name, attrs):
            self.note.l1l1lll11_opy_(True)
            keys = attrs.keys()
            if "placement" in keys:
                self.note.l111l1ll1_opy_(attrs.getValue("placement"))
            if "long" in keys:
                self.note.l1ll1l1l1_opy_(attrs.getValue("long"))

        def l1ll1l11lll1_opy_(self, name, attrs):
            self.note.l1lllllll_opy_(True)
            keys = attrs.keys()
            if "placement" in keys:
                self.note.l1l1l11l11_opy_(attrs.getValue("placement"))
            if "long" in keys:
                self.note.l1lll1l1_opy_(attrs.getValue("long"))

        def l1lll1lllll1_opy_(self, name, attrs):
            self.note.l1l1ll11l_opy_(True)
            keys = attrs.keys()
            if "direction" in keys:
                self.note.l11lll1l1_opy_(attrs.getValue("direction"))

        def l1lll1l11111_opy_(self, name, attrs):
            self.note.l1l11l11ll_opy_(True)
            keys = attrs.keys()
            if "direction" in keys:
                self.l1ll11lll111_opy_ = attrs.getValue("direction")
                self.note.l1l1lll1l_opy_(self.l1ll11lll111_opy_)

        def l1ll11l1l1l1_opy_(self, name, attrs):
            self.l1lll1l_opy_ = l1111ll_opy_()
            self.l1lll1l_opy_.l11ll1lll_opy_(True)
            keys = attrs.keys()
            if "type" in keys:
                self.l1lll1l_opy_.l1l1llll_opy_(attrs.getValue("type"))
            self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(self.l1lll1l_opy_)

        def l1ll1l11l1ll_opy_(self, name, attrs):
            l1ll111ll1_opy_ = l111ll1_opy_()
            l1ll111ll1_opy_.l11ll_opy_(True)
            keys = attrs.keys()
            if "type" in keys:
                l1ll111ll1_opy_.l1ll1l11l_opy_(attrs.getValue("type"))
            self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(l1ll111ll1_opy_)

        def l1l1lll1llll_opy_(self, name, attrs):
            l111ll1ll_opy_ = l1l11l1111_opy_()
            l111ll1ll_opy_.l1l1lll1ll_opy_(True)
            keys = attrs.keys()
            if "tempo" in keys:
                l111ll1ll_opy_.l1llll1_opy_(attrs.getValue("tempo"))
            if "dynamics" in keys:
                l111ll1ll_opy_.l11111l1111_opy_(attrs.getValue("dynamics"))
            if self.l1lllll1llll_opy_[self.l1ll1l1l11ll_opy_]["is_inside"]:
                self.l1ll1l1l11_opy_.l1ll1ll1l1_opy_(l111ll1ll_opy_)
            else:
                self.l1lll11_opy_.l1ll1ll1l1_opy_(l111ll1ll_opy_)

        def l1lllll1111l_opy_(self, name, attrs):
            self.l111ll_opy_ = l111111_opy_()

        def l1ll1lll1ll1_opy_(self):
            self.l111ll_opy_.l1lll1l11l_opy_(self.l1l1lllll111_opy_)
            self.l1lll11_opy_.l1ll1ll1l1_opy_(self.l111ll_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll111l1111_opy_(self, name, attrs):
            self.l1lll1111_opy_ = l1lll1ll1l_opy_()

        def l1ll1llll1ll_opy_(self):
            self.l1ll1111l1_opy_.l1ll1ll1l1_opy_(self.l1lll1111_opy_)

        def l1ll111111ll_opy_(self, name, attrs):
            self.l1111l1ll_opy_ = l1l1l1ll1_opy_()

        def l1llll1lll1l_opy_(self):
            self.l1lll1111_opy_.l1ll1ll1l1_opy_(self.l1111l1ll_opy_)

        def l1llll11l1ll_opy_(self):
            self.l1111l1ll_opy_.l1l11lll1_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1lll1l1lll1_opy_(self, name, attrs):
            self.l1lllll1ll_opy_ = l1l111l1_opy_()
            keys = attrs.keys()
            if "symbol" in keys:
                self.l1ll11lll111_opy_ = attrs.getValue("symbol")
                self.l1lllll1ll_opy_.l1lllll111_opy_(self.l1ll11lll111_opy_)

        def l1l1llll1ll1_opy_(self):
            self.l1lll1111_opy_.l1ll1ll1l1_opy_(self.l1lllll1ll_opy_)

        def l1ll1lllll11_opy_(self):
            self.l1lllll1ll_opy_.l1llllll11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll111lllll_opy_(self):
            self.l1lllll1ll_opy_.l11ll1l11_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll1lll11_opy_(self, name, attrs):
            self.l1lll111_opy_ = l1l11l1l1l_opy_()

        def l1lll1ll1lll_opy_(self):
            self.l11l11_opy_.l1ll1ll1l1_opy_(self.l1lll111_opy_)
            self.l1lll111_opy_ = None

        def l1llll11111l_opy_(self):
            self.l1lll111_opy_.l1111l111_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1ll11ll1l11_opy_(self, name, attrs):
            keys = attrs.keys()
            if "type" in keys:
                self.l1lll111_opy_.l11lll1ll11_opy_ = attrs.getValue("type")

        def l1llllll11l1_opy_(self):
            self.l1lll111_opy_.l1111l1ll1l_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1l1lllll1ll_opy_(self):
            self.l111l1l_opy_.l1ll1l1ll_opy_(self.l1l1lllll111_opy_)
            self.__1lll1l1l1l1_opy_()

        def l1llll1lllll_opy_(self, name, attrs):
            self.l111l1l11_opy_ = l1lllll11l_opy_()

        def l1ll11l1lll1_opy_(self):
            self.l1ll1111l1_opy_.l1ll1ll1l1_opy_(self.l111l1l11_opy_)

        def l1llll11l111_opy_(self):
            self.l111l1l11_opy_.l1ll111_opy_(self.l1l1lllll111_opy_.replace(" ", " "))
            self.__1lll1l1l1l1_opy_()

        def l1ll111l1ll1_opy_(self):
            self.l111l1l11_opy_.l11111111_opy_(self.l1l1lllll111_opy_.replace(" ", " "))
            self.__1lll1l1l1l1_opy_()

        def __1lll1l1l1l1_opy_(self):
            self.l1l1lllll111_opy_ = ""

    def l1111111l1_opy_(self, l1l1l111_opy_, l1ll1111l1_opy_):
        t1 = time.time()
        parser = xml.sax.make_parser()
        xml.sax.InputSource.setEncoding(parser, encoding="utf-8")
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = self.l1l1lll1ll11_opy_(
            l1l1l111_opy_, l1ll1111l1_opy_, self.l111111l1l_opy_, self.l1ll1ll1l11l_opy_
        )
        parser.setContentHandler(handler)
        if os.stat(self._11111ll11_opy_).st_size > 2:
            parser.parse(self._11111ll11_opy_)
        l1lllll11_opy_ = time.time()
        print("temps xml to model", l1lllll11_opy_ - t1)


class l111111111l_opy_(l1lll1111111_opy_):
    def __init__(self, lou, l11111l1ll_opy_, l111111l1l_opy_):
        super().__init__(lou, l11111l1ll_opy_, l111111l1l_opy_, "music_xml")


class l1l1llll1lll_opy_(l1lll1111111_opy_):
    def __init__(self, lou, l11111l1ll_opy_, l111111l1l_opy_):
        super().__init__(lou, l11111l1ll_opy_, l111111l1l_opy_, "music_bxml")
