"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import xml.etree.ElementTree as l1ll11ll111_opy_
from xml.dom import minidom
from .l1ll111l111_opy_ import *
import time
import bnote.__init__ as version


class l1l1ll1lll1_opy_:
    def __init__(self, l1l1l111_opy_, l1l1ll11lll_opy_, l1ll1111l1_opy_):
        self._1llll111_opy_ = l1l1l111_opy_
        self._1l1l1lll1l_opy_ = l1l1ll11lll_opy_
        self._1l1l1l1l_opy_ = l1ll1111l1_opy_

    def create_file(self, l1lllll1111_opy_):
        t1 = time.time()
        l11111_opy_ = False
        if l11111_opy_:
            self._1l1l1lll1l_opy_("\nmodel to xml\n")
        root = l1ll11ll111_opy_.Element("score-partwise")
        root.attrib = {"version": "4.0"}
        l1lll1ll111_opy_ = l1ll11ll111_opy_.SubElement(root, "identification")
        l1ll1l1ll11_opy_ = l1ll11ll111_opy_.SubElement(l1lll1ll111_opy_, "encoding")
        l1ll11l11ll_opy_ = l1ll11ll111_opy_.SubElement(
            l1ll1l1ll11_opy_, "software"
        ).text = ("eurobraille b.note " + version.__version__)
        l1llll1111l_opy_ = l1ll11ll111_opy_.SubElement(root, "defaults")
        l1lll1l1l11_opy_ = l1ll11ll111_opy_.SubElement(l1llll1111l_opy_, "lyric-font")
        l1lll1l1l11_opy_.attrib = {"font-family": "Times New Roman"}
        l1ll1111ll1_opy_ = False
        l1ll111l1ll_opy_ = False
        for element in self._1l1l1l1l_opy_.l1l1l1l_opy_:
            if element.t == "part":
                l1ll11l111l_opy_ = l1ll11ll111_opy_.SubElement(root, "part")
                l1ll11l111l_opy_.attrib = {"id": element.l1llll1llll_opy_}
                for l1lll11_opy_ in element.l1ll11llll_opy_:
                    l1l1l11l111_opy_ = l1ll11ll111_opy_.SubElement(
                        l1ll11l111l_opy_, "measure"
                    )
                    l1l1l11l111_opy_.attrib = {
                        "number": str(l1lll11_opy_.l1llllllll1_opy_)
                    }
                    l1llll11ll1_opy_ = False
                    l1ll1lllll1_opy_ = False
                    l1lll111ll1_opy_ = False
                    l1l1l11llll_opy_ = False
                    l1lllllll1l_opy_ = False
                    l1111111_opy_ = False
                    l1lll111111_opy_ = False
                    l1lll11l1ll_opy_ = False
                    for event in l1lll11_opy_.l1l111ll11_opy_:
                        l1l1l11l11l_opy_ = False
                        if event.t == "attributes":
                            for l1llllll1l1_opy_ in event.l1l1l1lllll_opy_:
                                if l1llllll1l1_opy_.t == "divisions":
                                    l1llll11ll1_opy_ = True
                                    l1lll111lll_opy_ = str(
                                        l1llllll1l1_opy_.l1lll11111_opy_
                                    )
                                elif l1llllll1l1_opy_.t == "key":
                                    l1ll1lllll1_opy_ = True
                                    l1l1llll1ll_opy_ = str(
                                        l1llllll1l1_opy_.l1l1111l_opy_
                                    )
                                    l1lll1l1ll1_opy_ = l1llllll1l1_opy_.mode
                                elif l1llllll1l1_opy_.t == "time":
                                    l1lll111ll1_opy_ = True
                                    l1lll11lll1_opy_ = l1llllll1l1_opy_.l1ll1lll_opy_
                                    l1lllll1lll_opy_ = l1llllll1l1_opy_.l1ll11l11_opy_
                                    l1ll11l1l11_opy_ = l1llllll1l1_opy_.symbol
                                elif l1llllll1l1_opy_.t == "staves":
                                    l1l1l11llll_opy_ = True
                                    l1l1ll11ll1_opy_ = l1llllll1l1_opy_.l1lll1l11_opy_
                                elif l1llllll1l1_opy_.t == "clef":
                                    l1lllllll1l_opy_ = True
                                    l1lll11ll1l_opy_ = l1llllll1l1_opy_.sign
                                    l1l1l1l1l1l_opy_ = l1llllll1l1_opy_.line
                                    l1l1l111l11_opy_ = l1llllll1l1_opy_.l1llll1ll_opy_
                                    l1ll11ll11l_opy_ = l1llllll1l1_opy_.l1ll11lll1l_opy_
                                elif l1llllll1l1_opy_.t == "transpose":
                                    l1111111_opy_ = True
                                    l1ll1ll1l1l_opy_ = str(
                                        l1llllll1l1_opy_.l1l1l11ll11_opy_
                                    )
                                    l1l1l1llll1_opy_ = str(
                                        l1llllll1l1_opy_.l1ll1l111ll_opy_
                                    )
                                    l1llll1l111_opy_ = str(
                                        l1llllll1l1_opy_.l1ll1l11111_opy_
                                    )
                                    l1lllll111l_opy_ = l1llllll1l1_opy_.l1ll11lll11_opy_
                                    l1l1ll1l111_opy_ = l1llllll1l1_opy_.l1llll1l1ll_opy_
                                elif l1llllll1l1_opy_.t == "measure-style":
                                    l1lll111111_opy_ = True
                                    l1lll111l1l_opy_ = l1llllll1l1_opy_.l1l11lllll_opy_
                        else:
                            if (
                                l1llll11ll1_opy_
                                or l1ll1lllll1_opy_
                                or l1lll111ll1_opy_
                                or l1l1l11llll_opy_
                                or l1lllllll1l_opy_
                                or l1111111_opy_
                                or l1lll111111_opy_
                            ):
                                l1ll1l1lll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1l11l111_opy_, "attributes"
                                )
                                if l1llll11ll1_opy_:
                                    l1llll11l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "divisions"
                                    ).text = l1lll111lll_opy_
                                    l1llll11ll1_opy_ = False
                                if l1ll1lllll1_opy_:
                                    l1ll1ll1111_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "key"
                                    )
                                    l1l1lll1111_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1ll1111_opy_, "fifths"
                                    ).text = l1l1llll1ll_opy_
                                    if l1lll1l1ll1_opy_ != "no":
                                        l1ll1ll1ll1_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1ll1ll1111_opy_, "mode"
                                        ).text = l1lll1l1ll1_opy_
                                    l1ll1lllll1_opy_ = False
                                if l1lll111ll1_opy_:
                                    l1lll1l111l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "time"
                                    )
                                    l1lll1ll1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1l111l_opy_, "beats"
                                    ).text = l1lll11lll1_opy_
                                    l1l1l11ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1l111l_opy_, "beat-type"
                                    ).text = l1lllll1lll_opy_
                                    if l1ll11l1l11_opy_ != "no":
                                        l1lll1l111l_opy_.attrib = {
                                            "symbol": l1ll11l1l11_opy_
                                        }
                                    l1lll111ll1_opy_ = False
                                if l1l1l11llll_opy_:
                                    l1ll1l11ll1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "staves"
                                    ).text = l1l1ll11ll1_opy_
                                    l1l1l11llll_opy_ = False
                                if l1lllllll1l_opy_:
                                    l1lll11111l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "clef"
                                    )
                                    l1llll1lll1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll11111l_opy_, "sign"
                                    ).text = l1lll11ll1l_opy_
                                    l1llll1l1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll11111l_opy_, "line"
                                    ).text = l1l1l1l1l1l_opy_
                                    if l1l1l111l11_opy_ != "no":
                                        l1l1l1ll1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1lll11111l_opy_, "clef-octave-change"
                                        ).text = l1l1l111l11_opy_
                                    if l1ll11ll11l_opy_ != "no":
                                        l1ll111111l_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1lll11111l_opy_, "braille-clef"
                                        ).text = l1ll11ll11l_opy_
                                    l1lllllll1l_opy_ = False
                                if l1111111_opy_:
                                    l1l1ll1111l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "transpose"
                                    )
                                    l1ll1l1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1ll1111l_opy_, "diatonic"
                                    ).text = l1ll1ll1l1l_opy_
                                    l1lll11llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1ll1111l_opy_, "chromatic"
                                    ).text = l1l1l1llll1_opy_
                                    l1lll11l11l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1ll1111l_opy_, "octave-change"
                                    ).text = l1llll1l111_opy_
                                    if l1lllll111l_opy_:
                                        l1ll1l1111l_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1l1ll1111l_opy_, "double"
                                        )
                                        if l1l1ll1l111_opy_ != "":
                                            l1ll1l1111l_opy_.attrib = {
                                                "above": l1l1ll1l111_opy_
                                            }
                                    l1111111_opy_ = False
                                if l1lll111111_opy_:
                                    l1l1l1lll11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l1lll1_opy_, "measure-style"
                                    )
                                    l1ll1ll1lll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1l1lll11_opy_, "multiple-rest"
                                    ).text = l1lll111l1l_opy_
                        if event.t == "note":
                            l1l1l1l1lll_opy_ = False
                            l1lll1111ll_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "note"
                            )
                            if event.l1llllllll_opy_:
                                l1ll1lll1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "grace"
                                )
                                if event.l1l1l1l111_opy_ != "missing":
                                    l1ll1lll1ll_opy_.attrib = {
                                        "slash": event.l1l1l1l111_opy_
                                    }
                            if event.l111l11l1_opy_:
                                l1l1l1l1l11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "chord"
                                )
                            if event.step != "no":
                                l1l1ll11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "pitch"
                                )
                                l1l1lll1lll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll11l11_opy_, "step"
                                ).text = l1l1lllllll_opy_[event.step]
                            if event.l1ll1lll1l_opy_ != "no":
                                l1ll111lll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll11l11_opy_, "alter"
                                ).text = l1l1lll111l_opy_[event.l1ll1lll1l_opy_]
                            if event.l1l1ll1l1l_opy_ != 100:
                                l1l1l1l11l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll11l11_opy_, "octave"
                                ).text = str(event.l1l1ll1l1l_opy_)
                            if event.rest:
                                l1ll1l1l1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "rest"
                                )
                            if event.l11ll1ll1_opy_ != 0:
                                l1l1l1l111l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "duration"
                                ).text = str(event.l11ll1ll1_opy_)
                            if event.l1llll111ll_opy_:
                                l1l1ll1ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "tie"
                                )
                                if event.l1ll11111l1_opy_ in ["start", "stop"]:
                                    l1l1ll1ll1l_opy_.attrib = {
                                        "type": event.l1ll11111l1_opy_
                                    }
                                elif event.l1ll11111l1_opy_ == "stop-start":
                                    l1l1ll1ll1l_opy_.attrib = {"type": "stop"}
                                    l1l1ll1ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "tie"
                                    )
                                    l1l1ll1ll1l_opy_.attrib = {"type": "start"}
                            if event.l1ll1ll11ll_opy_ != 0:
                                l1l1l1ll111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "voice"
                                ).text = str(event.l1ll1ll11ll_opy_)
                            if event.type != "no":
                                l1ll1llllll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "type"
                                ).text = l1llll11lll_opy_[event.type]
                            if event.dot:
                                l1l1ll1l1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "dot"
                                )
                            if event.l1ll1l1l_opy_ != "no":
                                l1ll111ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "accidental"
                                ).text = event.l1ll1l1l_opy_
                            if (
                                event.l1l1ll11111_opy_ != 0
                                and event.l1ll1111l11_opy_ != 0
                            ):
                                l1ll1lll111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "time-modification"
                                )
                                l1l1lllll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1lll111_opy_, "actual-notes"
                                ).text = str(event.l1l1ll11111_opy_)
                                l1l1l1l11ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1lll111_opy_, "normal-notes"
                                ).text = str(event.l1ll1111l11_opy_)
                            if event.l1ll1lll1l1_opy_ != "no":
                                l1ll1l1l111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "staff"
                                ).text = str(event.l1ll1lll1l1_opy_)
                            if event.l1llll111ll_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1l11l1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "tied"
                                )
                                if event.l1ll11111l1_opy_ in ["start", "stop"]:
                                    l1l1l11l1ll_opy_.attrib = {
                                        "type": event.l1ll11111l1_opy_
                                    }
                                elif event.l1ll11111l1_opy_ == "stop-start":
                                    l1l1l11l1ll_opy_.attrib = {"type": "stop"}
                                    l1l1l11l1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1ll1llll_opy_, "tied"
                                    )
                                    l1l1l11l1ll_opy_.attrib = {"type": "start"}
                            if event.l111l111l_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1l11lll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "slur"
                                )
                                if event.l11111l11_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib = {
                                        "type": event.l11111l11_opy_
                                    }
                                if event.l1l1lll1l11_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib.update(
                                        {"number": event.l1l1lll1l11_opy_}
                                    )
                                if event.l1l1l11l1l_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib.update(
                                        {"placement": event.l1l1l11l1l_opy_}
                                    )
                            if event.l1l111ll1l_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1l11lll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "slur"
                                )
                                if event.l11lll11l_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib = {
                                        "type": event.l11lll11l_opy_
                                    }
                                if event.l11l11ll_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib.update(
                                        {"number": event.l11l11ll_opy_}
                                    )
                                if event.l1ll1ll1_opy_ != "no":
                                    l1l1l11lll1_opy_.attrib.update(
                                        {"placement": event.l1ll1ll1_opy_}
                                    )
                            if event.l1ll1l11_opy_ != "no":
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll1lll11l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "technical"
                                )
                                l1llll11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1lll11l_opy_, "fingering"
                                ).text = event.l1ll1l11_opy_
                            if event.l111l1111_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll1111111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "articulations"
                                )
                                l1lllll1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111111_opy_, "staccato"
                                )
                            if event.l1l11ll111_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll1111111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "articulations"
                                )
                                l1l1l111lll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111111_opy_, "staccatissimo"
                                )
                            if event.l1lll1ll1_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll1111111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "articulations"
                                )
                                l1l1l1l1111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111111_opy_, "accent"
                                )
                            if event.l1l1l1111l1_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll1111111_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "articulations"
                                )
                                l1l1lll11l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111111_opy_, "breath-mark"
                                )
                            if event.l1lll1l11ll_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1lll1llll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "fermata"
                                )
                            if event.l111l1_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1lll1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "ornaments"
                                )
                                l1lll1ll1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1lll1l1l_opy_, "trill-mark"
                                )
                            if event.l1ll1ll1ll_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1lll1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "ornaments"
                                )
                                l1llll1ll11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1lll1l1l_opy_, "inverted-mordent"
                                )
                                l1llll1ll11_opy_.attrib = {
                                    "placement": event.l1lll1lll1l_opy_
                                }
                                l1llll1ll11_opy_.attrib = {"long": event.l11l_opy_}
                            if event.l111111ll_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1l1lll1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "ornaments"
                                )
                                l1lllll1l11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1lll1l1l_opy_, "mordent"
                                )
                                l1lllll1l11_opy_.attrib = {
                                    "placement": event.l1lll1l1111_opy_
                                }
                                l1lllll1l11_opy_.attrib = {"long": event.l11l1l1l1_opy_}
                            if event.l111l111_opy_ or (
                                not l1lllll1111_opy_ and event.l1ll11_opy_
                            ):
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll111l1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "arpeggiate"
                                )
                                if event.l1lll1111l1_opy_ == "down" or (
                                    not l1lllll1111_opy_
                                    and event.l1ll1llll11_opy_ == "down"
                                ):
                                    l1ll111l1l1_opy_.attrib = {"direction": "down"}
                            if l1lllll1111_opy_ and event.l1ll11_opy_:
                                if not l1l1l1l1lll_opy_:
                                    l1l1ll1llll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1lll1111ll_opy_, "notations"
                                    )
                                    l1l1l1l1lll_opy_ = True
                                l1ll11l1ll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1l1ll1llll_opy_, "two-hands-arpeggiate"
                                )
                                if event.l1ll1llll11_opy_ == "down":
                                    l1ll11l1ll1_opy_.attrib = {"direction": "down"}
                            if event.text != "":
                                l1llllll1ll_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1lll1111ll_opy_, "lyric"
                                )
                                l1l1l11l1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1llllll1ll_opy_, "syllabic"
                                ).text = event.l1lll11ll11_opy_
                                l1lll1ll11l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1llllll1ll_opy_, "text"
                                ).text = event.text
                        elif event.t == "direction":
                            l1ll11l1lll_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "direction"
                            )
                            if event.l1ll111llll_opy_ != "no":
                                l1ll11l1lll_opy_.attrib = {
                                    "placement": event.l1ll111llll_opy_
                                }
                            for l1llllll1l1_opy_ in event.l1lll11l111_opy_:
                                if l1llllll1l1_opy_.t == "dynamics":
                                    l1ll1l11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "direction-type"
                                    )
                                    l1l1lll11ll_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l11l11_opy_, "dynamics"
                                    )
                                    l1lll1lll11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1l1lll11ll_opy_, l1llllll1l1_opy_.l11lll_opy_
                                    )
                                if l1llllll1l1_opy_.t == "pedal":
                                    l1ll1l11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "direction-type"
                                    )
                                    l1ll11llll1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l11l11_opy_, "pedal"
                                    )
                                    l1ll11llll1_opy_.attrib = {
                                        "type": l1llllll1l1_opy_.l1ll1l11l1l_opy_
                                    }
                                if l1llllll1l1_opy_.t == "wedge":
                                    l1ll1l11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "direction-type"
                                    )
                                    l1ll1l1l1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l11l11_opy_, "wedge"
                                    )
                                    l1ll1l1l1l1_opy_.attrib = {
                                        "type": l1llllll1l1_opy_.l1l1l1ll1l1_opy_
                                    }
                                if l1llllll1l1_opy_.t == "metronome":
                                    l1ll1l11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "direction-type"
                                    )
                                    l1lll111l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l11l11_opy_, "metronome"
                                    )
                                    if l1llllll1l1_opy_.l11l111l1_opy_ != "no":
                                        l1l1llll111_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1lll111l11_opy_, "beat-unit"
                                        ).text = l1llllll1l1_opy_.l11l111l1_opy_
                                    if l1llllll1l1_opy_.l1ll111l11l_opy_:
                                        l1l1llll111_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1lll111l11_opy_, "beat-unit-dot"
                                        )
                                    if l1llllll1l1_opy_.l1l111l1l_opy_ != "no":
                                        l1llllll111_opy_ = l1ll11ll111_opy_.SubElement(
                                            l1lll111l11_opy_, "per-minute"
                                        ).text = l1llllll1l1_opy_.l1l111l1l_opy_
                                if l1llllll1l1_opy_.t == "sound":
                                    l1ll1l1l11l_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "sound"
                                    )
                                    if l1llllll1l1_opy_.l1lll1l1lll_opy_ != "no":
                                        l1ll1l1l11l_opy_.attrib = {
                                            "tempo": l1llllll1l1_opy_.l1lll1l1lll_opy_
                                        }
                                    if l1llllll1l1_opy_.l1l1l1l1ll1_opy_ != "no":
                                        l1ll1l1l11l_opy_.attrib = {
                                            "tempo": l1llllll1l1_opy_.l1l1l1l1ll1_opy_
                                        }
                                if l1llllll1l1_opy_.t == "words":
                                    l1ll1l11l11_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll11l1lll_opy_, "direction-type"
                                    )
                                    l1ll1ll11l1_opy_ = l1ll11ll111_opy_.SubElement(
                                        l1ll1l11l11_opy_, "words"
                                    ).text = l1llllll1l1_opy_.words
                            if event.l1ll1lll1l1_opy_ != 1:
                                l1l1ll1ll11_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll11l1lll_opy_, "staff"
                                ).text = str(event.l1ll1lll1l1_opy_)
                        elif event.t == "backup":
                            l1ll11ll1l1_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "backup"
                            )
                            l1l1l1l111l_opy_ = l1ll11ll111_opy_.SubElement(
                                l1ll11ll1l1_opy_, "duration"
                            ).text = str(event.l11ll1ll1_opy_)
                        elif event.t == "barline":
                            l1ll1111l1l_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "barline"
                            )
                            if event.location != "no":
                                l1ll1111l1l_opy_.attrib = {"location": event.location}
                            if event.l1l1ll111ll_opy_ != "no":
                                l1l1lll1ll1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111l1l_opy_, "bar-style"
                                ).text = event.l1l1ll111ll_opy_
                            if event.l1l1l1ll11l_opy_:
                                l1ll1llll1l_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111l1l_opy_, "ending"
                                )
                                if event.l111l11ll_opy_ != "no":
                                    l1ll1llll1l_opy_.attrib = {
                                        "number": event.l111l11ll_opy_
                                    }
                                if event.l1l1l111l1l_opy_ != "no":
                                    l1ll1llll1l_opy_.attrib.update(
                                        {"type": event.l1l1l111l1l_opy_}
                                    )
                            if event.repeat != "no":
                                l1llll111l1_opy_ = l1ll11ll111_opy_.SubElement(
                                    l1ll1111l1l_opy_, "repeat"
                                )
                                l1llll111l1_opy_.attrib = {"direction": event.repeat}
                        elif event.t == "print":
                            l1l1llllll1_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "print"
                            )
                            if event.l1l1lllll11_opy_ != "no":
                                l1l1llllll1_opy_.attrib = {
                                    "new-system": event.l1l1lllll11_opy_
                                }
                        elif event.t == "sound":
                            l1ll1l1l11l_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "sound"
                            )
                            if event.l1lll1l1lll_opy_ != "no":
                                l1ll1l1l11l_opy_.attrib = {
                                    "tempo": event.l1lll1l1lll_opy_
                                }
                            if event.l1l1l1l1ll1_opy_ != "no":
                                l1ll1l1l11l_opy_.attrib = {
                                    "tempo": event.l1l1l1l1ll1_opy_
                                }
                        elif l1lllll1111_opy_ and event.t == "karaoke":
                            l1ll11l11l1_opy_ = l1ll11ll111_opy_.SubElement(
                                l1l1l11l111_opy_, "karaoke"
                            ).text = event.l111ll_opy_
            elif element.t == "part-list":
                l1ll1111lll_opy_ = l1ll11ll111_opy_.SubElement(root, "part-list")
                for l111l11_opy_ in element.l1l1l1111l_opy_:
                    l1lllll11ll_opy_ = l1ll11ll111_opy_.SubElement(
                        l1ll1111lll_opy_, "score-part"
                    )
                    if l111l11_opy_.l1llll1llll_opy_ != "no":
                        l1lllll11ll_opy_.attrib = {"id": l111l11_opy_.l1llll1llll_opy_}
                    if l111l11_opy_.l1l1l_opy_ != "no":
                        l1ll1ll111l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "part-name"
                        ).text = l111l11_opy_.l1l1l_opy_
                    if l111l11_opy_.l1111ll1l_opy_ != "no":
                        l1ll11111ll_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "part-abbreviation"
                        ).text = l111l11_opy_.l1111ll1l_opy_
                    if l111l11_opy_.l1l1llll11l_opy_ != "no":
                        l1l1l111ll1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "score-instrument"
                        )
                        l1l1l111ll1_opy_.attrib = {"id": l111l11_opy_.l1l1llll11l_opy_}
                    if l111l11_opy_.l1llll1l1_opy_ != "no":
                        l1l1ll1l1ll_opy_ = l1ll11ll111_opy_.SubElement(
                            l1l1l111ll1_opy_, "instrument-name"
                        ).text = l111l11_opy_.l1llll1l1_opy_
                    if (
                        l111l11_opy_.l1ll111ll11_opy_ != "no"
                        or l111l11_opy_.l1llllll11l_opy_ != "no"
                    ):
                        l1llll1ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "midi-device"
                        )
                        l1llll1ll1l_opy_.attrib = {
                            "id": l111l11_opy_.l1ll111ll11_opy_,
                            "port": l111l11_opy_.l1llllll11l_opy_,
                        }
                    if l111l11_opy_.l1ll11lllll_opy_ != "no":
                        l1lllll11l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "midi-instrument"
                        )
                        l1lllll11l1_opy_.attrib = {"id": l111l11_opy_.l1ll11lllll_opy_}
                    if l111l11_opy_.l1lll11l1_opy_ != "no":
                        l1l1ll11l1l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11l1_opy_, "midi-channel"
                        ).text = l111l11_opy_.l1lll11l1_opy_
                    if l111l11_opy_.l1l1llll1l_opy_ != "no":
                        l1lll1l1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11l1_opy_, "midi-program"
                        ).text = l111l11_opy_.l1l1llll1l_opy_
                    if l111l11_opy_.l1lll11ll1_opy_ != "no":
                        l1lllllll11_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11l1_opy_, "volume"
                        ).text = l111l11_opy_.l1lll11ll1_opy_
                    if l111l11_opy_.l11ll1111_opy_ != "no":
                        l1l1llll1l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11l1_opy_, "pan"
                        ).text = l111l11_opy_.l11ll1111_opy_
                    if l111l11_opy_.l1ll11l1111_opy_ == True:
                        l1ll1l111l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "braille-ascending-chords"
                        ).text = "1"
                    elif l111l11_opy_.l1ll11l1111_opy_ == False:
                        l1ll1l111l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "braille-ascending-chords"
                        ).text = "-1"
                    else:
                        l1ll1l111l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lllll11ll_opy_, "braille-ascending-chords"
                        ).text = l111l11_opy_.l1ll11l1111_opy_
            elif element.t == "credit":
                l1lllll1ll1_opy_ = l1ll11ll111_opy_.SubElement(root, "credit")
                l1lllll1ll1_opy_.attrib = {"page": "1"}
                if element.l1lll1l11l1_opy_ != "no":
                    l1lll1lllll_opy_ = l1ll11ll111_opy_.SubElement(
                        l1lllll1ll1_opy_, "credit-type"
                    ).text = element.l1lll1l11l1_opy_
                l1ll11l1l1l_opy_ = l1ll11ll111_opy_.SubElement(
                    l1lllll1ll1_opy_, "credit-words"
                ).text = element.l1ll1l1ll1l_opy_
            elif element.t == "work":
                if not l1ll1111ll1_opy_ and not l1ll111l1ll_opy_:
                    l1l1ll1l11l_opy_ = l1ll11ll111_opy_.SubElement(root, "work")
                if element.l1ll1ll1l11_opy_ != "no":
                    l1ll1111ll1_opy_ = True
                    l1ll1ll1l11_opy_ = element.l1ll1ll1l11_opy_
                if element.l1ll1l11lll_opy_ != "no":
                    l1ll111l1ll_opy_ = True
                    l1ll1l11lll_opy_ = element.l1ll1l11lll_opy_
            elif l1lllll1111_opy_ and element.t == "braille-global":
                l1llll1l11l_opy_ = l1ll11ll111_opy_.SubElement(root, "braille-global")
                for event in element.l1llll11111_opy_:
                    if event.t == "global-key":
                        l1ll1ll1111_opy_ = l1ll11ll111_opy_.SubElement(
                            l1llll1l11l_opy_, "global-key"
                        )
                        l1l1lll1111_opy_ = l1ll11ll111_opy_.SubElement(
                            l1ll1ll1111_opy_, "global-fifths"
                        ).text = str(event.l1l1111l_opy_)
                    if event.t == "global-time":
                        l1lll1l111l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1llll1l11l_opy_, "global-time"
                        )
                        l1lll1ll1l1_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lll1l111l_opy_, "global-beats"
                        ).text = event.l1ll1lll_opy_
                        l1l1l11ll1l_opy_ = l1ll11ll111_opy_.SubElement(
                            l1lll1l111l_opy_, "global-beat-type"
                        ).text = event.l1ll11l11_opy_
                        if event.symbol != "no":
                            l1lll1l111l_opy_.attrib = {"symbol": event.symbol}
        if l1ll1111ll1_opy_:
            l1ll11ll1ll_opy_ = l1ll11ll111_opy_.SubElement(
                l1l1ll1l11l_opy_, "work-number"
            ).text = l1ll1ll1l11_opy_
        if l1ll111l1ll_opy_:
            l1l1l1111ll_opy_ = l1ll11ll111_opy_.SubElement(
                l1l1ll1l11l_opy_, "work-title"
            ).text = l1ll1l11lll_opy_
        l1lll11l1l1_opy_ = minidom.parseString(
            l1ll11ll111_opy_.tostring(root)
        ).toprettyxml(indent="   ", encoding="UTF-8", standalone="")
        if l11111_opy_:
            self._1l1l1lll1l_opy_(str(l1lll11l1l1_opy_))
        self._1llll111_opy_(l1lll11l1l1_opy_)
        l1lllll11_opy_ = time.time()
        if l1lllll1111_opy_:
            print("temps model to bxml", l1lllll11_opy_ - t1)
        else:
            print("temps model to musicxml", l1lllll11_opy_ - t1)
