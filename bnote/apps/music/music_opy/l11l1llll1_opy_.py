"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import xml.etree.ElementTree as l111lllll1_opy_
from xml.dom import minidom
from .l11llll1l1_opy_ import *
import time


class l1llllll1l1_opy_:
    def __init__(self, l11llll11l_opy_, l1lll111l1l_opy_, l1l11ll11_opy_):
        self._1l1111ll_opy_ = l11llll11l_opy_
        self._11lllll1_opy_ = l1lll111l1l_opy_
        self._1l1l11ll_opy_ = l1l11ll11_opy_

    def create_file(self):
        t1 = time.time()
        l1l11ll11l_opy_ = False
        if l1l11ll11l_opy_:
            self._11lllll1_opy_("\nmodel to xml\n")
        root = l111lllll1_opy_.Element("score-partwise")
        root.attrib = {"version": "2.0"}
        l1lll11llll_opy_ = l111lllll1_opy_.SubElement(root, "defaults")
        l11l1lllll_opy_ = l111lllll1_opy_.SubElement(l1lll11llll_opy_, "lyric-font")
        l11l1lllll_opy_.attrib = {"font-family": "Times New Roman"}
        for element in self._1l1l11ll_opy_.l1lll1l111l_opy_:
            if element.t == "part":
                l111llll11_opy_ = l111lllll1_opy_.SubElement(root, "part")
                l111llll11_opy_.attrib = {"id": element.l111l1l1ll_opy_}
                for l111111l1l_opy_ in element.l11l1l1ll1_opy_:
                    l111l11l1l_opy_ = l111lllll1_opy_.SubElement(l111llll11_opy_, "measure")
                    l111l11l1l_opy_.attrib = {"number": str(l111111l1l_opy_.l1lll111l11_opy_)}
                    l11l1l1l1l_opy_ = False
                    l1lllll11ll_opy_ = False
                    l11111l11l_opy_ = False
                    l1l1111l11_opy_ = False
                    l1111lllll_opy_ = False
                    l11ll111l1_opy_ = False
                    l1111ll111_opy_ = False
                    for event in l111111l1l_opy_.l111l11lll_opy_:
                        l11ll11111_opy_ = False
                        if event.t == "attributes":
                            for l11lllll11_opy_ in event.l11l111ll1_opy_:
                                if l11lllll11_opy_.t == "divisions":
                                    l11l1l1l1l_opy_ = True
                                    l1l111lll1_opy_ = str(l11lllll11_opy_.l111l1111l_opy_)
                                elif l11lllll11_opy_.t == "key":
                                    l1lllll11ll_opy_ = True
                                    l11llll1ll_opy_ = str(l11lllll11_opy_.l1lll1l1l11_opy_)
                                    l11l11llll_opy_ = l11lllll11_opy_.mode
                                elif l11lllll11_opy_.t == "time":
                                    l11111l11l_opy_ = True
                                    l11l1l1111_opy_ = l11lllll11_opy_.l1l1l11111_opy_
                                    l1lll11lll1_opy_ = l11lllll11_opy_.l1111lll11_opy_
                                    l1l11llll1_opy_ = l11lllll11_opy_.l11lllll1l_opy_
                                elif l11lllll11_opy_.t == "staves":
                                    l1l1111l11_opy_ = True
                                    l1lll1ll111_opy_ = l11lllll11_opy_.l1111111ll_opy_
                                elif l11lllll11_opy_.t == "clef":
                                    l1111lllll_opy_ = True
                                    l11111lll1_opy_ = l11lllll11_opy_.sign
                                    l11l11111l_opy_ = l11lllll11_opy_.line
                                    l111l1ll11_opy_ = l11lllll11_opy_.l1lllll1111_opy_
                                    l1111111l1_opy_ = l11lllll11_opy_.l1lllll1ll1_opy_
                                elif l11lllll11_opy_.t == "transpose":
                                    l11ll111l1_opy_ = True
                                    l1lll11l1l1_opy_ = str(l11lllll11_opy_.l11lll111l_opy_)
                                    l11ll1111l_opy_ = str(l11lllll11_opy_.l111111111_opy_)
                                    l11l111l1l_opy_ = str(l11lllll11_opy_.l1lll1llll1_opy_)
                                    l111ll1lll_opy_ = l11lllll11_opy_.l1111l11l1_opy_
                                    l1l11l1111_opy_ = l11lllll11_opy_.l1lllllll1l_opy_
                        else:
                            if l11l1l1l1l_opy_ or l1lllll11ll_opy_ or l11111l11l_opy_ or l1l1111l11_opy_ or l1111lllll_opy_ or l11ll111l1_opy_:
                                l1l11l111l_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "attributes")
                                if l11l1l1l1l_opy_:
                                    l1llllllll1_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_,
                                                                                  "divisions").text = l1l111lll1_opy_
                                    l11l1l1l1l_opy_ = False
                                if l1lllll11ll_opy_:
                                    l1l111l1l1_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_, "key")
                                    l1llll1l1ll_opy_ = l111lllll1_opy_.SubElement(l1l111l1l1_opy_,
                                                                                  "fifths").text = l11llll1ll_opy_
                                    if l11l11llll_opy_ != "no":
                                        l111ll111l_opy_ = l111lllll1_opy_.SubElement(l1l111l1l1_opy_,
                                                                                     "mode").text = l11l11llll_opy_
                                    l1lllll11ll_opy_ = False
                                if l11111l11l_opy_:
                                    l111111lll_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_, "time")
                                    l1lll1ll1l1_opy_ = l111lllll1_opy_.SubElement(l111111lll_opy_,
                                                                                  "beats").text = l11l1l1111_opy_
                                    l111111l11_opy_ = l111lllll1_opy_.SubElement(l111111lll_opy_,
                                                                                 "beat-type").text = l1lll11lll1_opy_
                                    if l1l11llll1_opy_ != "no":
                                        l111111lll_opy_.attrib = {"symbol": l1l11llll1_opy_}
                                    l11111l11l_opy_ = False
                                if l1l1111l11_opy_:
                                    l111l111l1_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_,
                                                                                 "staves").text = l1lll1ll111_opy_
                                    l1l1111l11_opy_ = False
                                if l1111lllll_opy_:
                                    l11111l1l1_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_, "clef")
                                    l11l11l11l_opy_ = l111lllll1_opy_.SubElement(l11111l1l1_opy_,
                                                                                 "sign").text = l11111lll1_opy_
                                    l111ll1l1l_opy_ = l111lllll1_opy_.SubElement(l11111l1l1_opy_,
                                                                                 "line").text = l11l11111l_opy_
                                    if l111l1ll11_opy_ != "no":
                                        l1lll1lll1l_opy_ = l111lllll1_opy_.SubElement(l11111l1l1_opy_,
                                                                                      "clef-octave-change").text = l111l1ll11_opy_
                                    if l1111111l1_opy_ != "no":
                                        l1lll11l11l_opy_ = l111lllll1_opy_.SubElement(l11111l1l1_opy_,
                                                                                      "braille-clef").text = l1111111l1_opy_
                                    l1111lllll_opy_ = False
                                if l11ll111l1_opy_:
                                    l11ll111ll_opy_ = l111lllll1_opy_.SubElement(l1l11l111l_opy_, "transpose")
                                    l1l11ll1ll_opy_ = l111lllll1_opy_.SubElement(l11ll111ll_opy_,
                                                                                 "diatonic").text = l1lll11l1l1_opy_
                                    l11l1l1l11_opy_ = l111lllll1_opy_.SubElement(l11ll111ll_opy_,
                                                                                 "chromatic").text = l11ll1111l_opy_
                                    l11111llll_opy_ = l111lllll1_opy_.SubElement(l11ll111ll_opy_,
                                                                                 "octave-change").text = l11l111l1l_opy_
                                    if l111ll1lll_opy_:
                                        l11l1111l1_opy_ = l111lllll1_opy_.SubElement(l11ll111ll_opy_, "double")
                                        if l1l11l1111_opy_ != "":
                                            l11l1111l1_opy_.attrib = {"above": l1l11l1111_opy_}
                                    l11ll111l1_opy_ = False
                        if event.t == "note":
                            l1111l1ll1_opy_ = False
                            l1lll1l1ll1_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "note")
                            if event.l1111lll1l_opy_:
                                l1lll1l1l1l_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "grace")
                                if event.l11lll1111_opy_ != "missing":
                                    l1lll1l1l1l_opy_.attrib = {"slash": event.l11lll1111_opy_}
                            if event.l1lll1l11l1_opy_:
                                l11l11l1l1_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "chord")
                            if event.step != "no":
                                l1lll111ll1_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "pitch")
                                l1l111llll_opy_ = l111lllll1_opy_.SubElement(l1lll111ll1_opy_, "step").text = \
                                    l11ll1l111_opy_[event.step]
                            if event.l11lll11ll_opy_ != "no":
                                l111l111ll_opy_ = l111lllll1_opy_.SubElement(l1lll111ll1_opy_, "alter").text = \
                                    l11l1lll11_opy_[event.l11lll11ll_opy_]
                            if event.l1l11111ll_opy_ != 100:
                                l11lllllll_opy_ = l111lllll1_opy_.SubElement(l1lll111ll1_opy_, "octave").text = str(
                                    event.l1l11111ll_opy_)
                            if event.rest:
                                l1111ll1l1_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "rest")
                            if event.l11lll1l11_opy_ != 0:
                                l11l1ll1ll_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "duration").text = str(
                                    event.l11lll1l11_opy_)
                            if event.l1l11l11l1_opy_:
                                l11l111111_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "tie")
                                if event.l1l1111111_opy_ in ["start", "stop"]:
                                    l11l111111_opy_.attrib = {"type": event.l1l1111111_opy_}
                                elif event.l1l1111111_opy_ == "stop-start":
                                    l11l111111_opy_.attrib = {"type": "stop"}
                                    l11l111111_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "tie")
                                    l11l111111_opy_.attrib = {"type": "start"}
                            if event.l1111l1lll_opy_ != 0:
                                l111l1llll_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "voice").text = str(
                                    event.l1111l1lll_opy_)
                            if event.type != "no":
                                l1lllll1l1l_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "type").text = \
                                    l111ll1l11_opy_[event.type]
                            if event.dot:
                                l1llll11l11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "dot")
                            if event.l1llll11ll1_opy_ != "no":
                                l1l11lll1l_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_,
                                                                             "accidental").text = event.l1llll11ll1_opy_
                            if event.l1llllll11l_opy_ != 0 and event.l1lll1lll11_opy_ != 0:
                                l1lll1lllll_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "time-modification")
                                l111l1l111_opy_ = l111lllll1_opy_.SubElement(l1lll1lllll_opy_,
                                                                             "actual-notes").text = str(
                                    event.l1llllll11l_opy_)
                                l11lll1lll_opy_ = l111lllll1_opy_.SubElement(l1lll1lllll_opy_,
                                                                             "normal-notes").text = str(
                                    event.l1lll1lll11_opy_)
                            if event.l11111ll11_opy_ != "no":
                                l111l11111_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "staff").text = str(
                                    event.l11111ll11_opy_)
                            if event.l1l11l11l1_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1111llll1_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "tied")
                                if event.l1l1111111_opy_ in ["start", "stop"]:
                                    l1111llll1_opy_.attrib = {"type": event.l1l1111111_opy_}
                                elif event.l1l1111111_opy_ == "stop-start":
                                    l1111llll1_opy_.attrib = {"type": "stop"}
                                    l1111llll1_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "tied")
                                    l1111llll1_opy_.attrib = {"type": "start"}
                            if event.l1llllll1ll_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1l11ll111_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "slur")
                                if event.l1111l1l11_opy_ != "no":
                                    l1l11ll111_opy_.attrib = {"type": event.l1111l1l11_opy_}
                                if event.l1lll1111ll_opy_ != "no":
                                    l1l11ll111_opy_.attrib.update({"number": event.l1lll1111ll_opy_})
                                if event.l11l1111ll_opy_ != "no":
                                    l1l11ll111_opy_.attrib.update({"placement": event.l11l1111ll_opy_})
                            if event.l111ll11l1_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1l11ll111_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "slur")
                                if event.l11l111l11_opy_ != "no":
                                    l1l11ll111_opy_.attrib = {"type": event.l11l111l11_opy_}
                                if event.l11l11l1ll_opy_ != "no":
                                    l1l11ll111_opy_.attrib.update({"number": event.l11l11l1ll_opy_})
                                if event.l1llll1lll1_opy_ != "no":
                                    l1l11ll111_opy_.attrib.update({"placement": event.l1llll1lll1_opy_})
                            if event.l11llll111_opy_ != "no":
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1l111111l_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "technical")
                                l1l1111l1l_opy_ = l111lllll1_opy_.SubElement(l1l111111l_opy_,
                                                                             "fingering").text = event.l11llll111_opy_
                            if event.l1llll1l1l1_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lllll1l11_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "articulations")
                                l1l11l1lll_opy_ = l111lllll1_opy_.SubElement(l1lllll1l11_opy_, "staccato")
                            if event.l1l111l11l_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lllll1l11_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "articulations")
                                l1lll11l111_opy_ = l111lllll1_opy_.SubElement(l1lllll1l11_opy_, "staccatissimo")
                            if event.l1lll1l1lll_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lllll1l11_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "articulations")
                                l11111111l_opy_ = l111lllll1_opy_.SubElement(l1lllll1l11_opy_, "accent")
                            if event.l1l11l1l1l_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lllll1l11_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "articulations")
                                l1llll11l1l_opy_ = l111lllll1_opy_.SubElement(l1lllll1l11_opy_, "breath-mark")
                            if event.l1llll111l1_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1llll1l11l_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "fermata")
                            if event.l11llllll1_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l11ll1llll_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "ornaments")
                                l1llll11111_opy_ = l111lllll1_opy_.SubElement(l11ll1llll_opy_, "trill-mark")
                            if event.l1l111l111_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l11ll1llll_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "ornaments")
                                l1llll1llll_opy_ = l111lllll1_opy_.SubElement(l11ll1llll_opy_, "inverted-mordent")
                                l1llll1llll_opy_.attrib = {"placement": event.l11ll11l1l_opy_}
                                l1llll1llll_opy_.attrib = {"long": event.l1lll1ll11l_opy_}
                            if event.l111l11l11_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l11ll1llll_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "ornaments")
                                l1111l111l_opy_ = l111lllll1_opy_.SubElement(l11ll1llll_opy_, "mordent")
                                l1111l111l_opy_.attrib = {"placement": event.l1lll1ll1ll_opy_}
                                l1111l111l_opy_.attrib = {"long": event.l1l11ll1l1_opy_}
                            if event.l11l1ll111_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lll11ll11_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "arpeggiate")
                                if event.l1lllll11l1_opy_ == "down":
                                    l1lll11ll11_opy_.attrib = {"direction": "down"}
                            if event.l1lllllll11_opy_:
                                if not l1111l1ll1_opy_:
                                    l11ll1ll11_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "notations")
                                    l1111l1ll1_opy_ = True
                                l1lll1l1111_opy_ = l111lllll1_opy_.SubElement(l11ll1ll11_opy_, "two-hands-arpeggiate")
                                if event.l111l1lll1_opy_ == "down":
                                    l1lll1l1111_opy_.attrib = {"direction": "down"}
                            if event.text != "":
                                l11ll1l1l1_opy_ = l111lllll1_opy_.SubElement(l1lll1l1ll1_opy_, "lyric")
                                l11l1l111l_opy_ = l111lllll1_opy_.SubElement(l11ll1l1l1_opy_,
                                                                             "syllabic").text = event.l111llllll_opy_
                                l1lllllllll_opy_ = l111lllll1_opy_.SubElement(l11ll1l1l1_opy_, "text").text = event.text
                        if event.t == "direction":
                            l1llll111ll_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "direction")
                            if event.l111lll11l_opy_ != "no":
                                l1llll111ll_opy_.attrib = {"placement": event.l111lll11l_opy_}
                            for l11lllll11_opy_ in event.l1lll1111l1_opy_:
                                if l11lllll11_opy_.t == "dynamics":
                                    l11l1ll11l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "direction-type")
                                    l111l1ll1l_opy_ = l111lllll1_opy_.SubElement(l11l1ll11l_opy_, "dynamics")
                                    l1111l1111_opy_ = l111lllll1_opy_.SubElement(l111l1ll1l_opy_,
                                                                                 l11lllll11_opy_.l1l11l1ll1_opy_)
                                if l11lllll11_opy_.t == "pedal":
                                    l11l1ll11l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "direction-type")
                                    l11l111lll_opy_ = l111lllll1_opy_.SubElement(l11l1ll11l_opy_, "pedal")
                                    l11l111lll_opy_.attrib = {"type": l11lllll11_opy_.l1l11l1l11_opy_}
                                if l11lllll11_opy_.t == "wedge":
                                    l11l1ll11l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "direction-type")
                                    l1llll1111l_opy_ = l111lllll1_opy_.SubElement(l11l1ll11l_opy_, "wedge")
                                    l1llll1111l_opy_.attrib = {"type": l11lllll11_opy_.l11ll11ll1_opy_}
                                if l11lllll11_opy_.t == "metronome":
                                    l11l1ll11l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "direction-type")
                                    l1lll11l1ll_opy_ = l111lllll1_opy_.SubElement(l11l1ll11l_opy_, "metronome")
                                    if l11lllll11_opy_.l11111l111_opy_ != "no":
                                        l1l111ll11_opy_ = l111lllll1_opy_.SubElement(l1lll11l1ll_opy_,
                                                                                     "beat-unit").text = l11lllll11_opy_.l11111l111_opy_
                                    if l11lllll11_opy_.l1l11lllll_opy_:
                                        l1l111ll11_opy_ = l111lllll1_opy_.SubElement(l1lll11l1ll_opy_, "beat-unit-dot")
                                    if l11lllll11_opy_.l111111ll1_opy_ != "no":
                                        l11l1l11l1_opy_ = l111lllll1_opy_.SubElement(l1lll11l1ll_opy_,
                                                                                     "per-minute").text = l11lllll11_opy_.l111111ll1_opy_
                                if l11lllll11_opy_.t == "sound":
                                    l11lll1l1l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "sound")
                                    if l11lllll11_opy_.l11111l1ll_opy_ != "no":
                                        l11lll1l1l_opy_.attrib = {"tempo": l11lllll11_opy_.l11111l1ll_opy_}
                                    if l11lllll11_opy_.l11l1lll1l_opy_ != "no":
                                        l11lll1l1l_opy_.attrib = {"tempo": l11lllll11_opy_.l11l1lll1l_opy_}
                                if l11lllll11_opy_.t == "words":
                                    l11l1ll11l_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "direction-type")
                                    l1111ll11l_opy_ = l111lllll1_opy_.SubElement(l11l1ll11l_opy_,
                                                                                 "words").text = l11lllll11_opy_.words
                            if event.l11111ll11_opy_ != 1:
                                l11l1l11ll_opy_ = l111lllll1_opy_.SubElement(l1llll111ll_opy_, "staff").text = str(
                                    event.l11111ll11_opy_)
                        if event.t == "backup":
                            l11lll1ll1_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "backup")
                            l11l1ll1ll_opy_ = l111lllll1_opy_.SubElement(l11lll1ll1_opy_, "duration").text = str(
                                event.l11lll1l11_opy_)
                        if event.t == "barline":
                            l11l1ll1l1_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "barline")
                            if event.location != "no":
                                l11l1ll1l1_opy_.attrib = {"location": event.location}
                            if event.l11ll1lll1_opy_ != "no":
                                l1llll1l111_opy_ = l111lllll1_opy_.SubElement(l11l1ll1l1_opy_,
                                                                              "bar-style").text = event.l11ll1lll1_opy_
                            if event.l1l111l1ll_opy_ != "no":
                                l11lll11l1_opy_ = l111lllll1_opy_.SubElement(l11l1ll1l1_opy_, "repeat")
                                l11lll11l1_opy_.attrib = {"direction": event.l1l111l1ll_opy_}
                        if event.t == "print":
                            l1llll1ll1l_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_, "print")
                            if event.l1111l11ll_opy_ != "no":
                                l1llll1ll1l_opy_.attrib = {"new-system": event.l1111l11ll_opy_}
                        if event.t == "karaoke":
                            l11l11ll11_opy_ = l111lllll1_opy_.SubElement(l111l11l1l_opy_,
                                                                         "karaoke").text = event.l111l1l11l_opy_
            elif element.t == "part-list":
                l1llll11lll_opy_ = l111lllll1_opy_.SubElement(root, "part-list")
                for l1l11111l1_opy_ in element.l111l1l1l1_opy_:
                    l1111l1l1l_opy_ = l111lllll1_opy_.SubElement(l1llll11lll_opy_, "score-part")
                    if l1l11111l1_opy_.l111l1l1ll_opy_ != "no":
                        l1111l1l1l_opy_.attrib = {"id": l1l11111l1_opy_.l111l1l1ll_opy_}
                    if l1l11111l1_opy_.l111lll1ll_opy_ != "no":
                        l1lll1l11ll_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_,
                                                                      "part-name").text = l1l11111l1_opy_.l111lll1ll_opy_
                    if l1l11111l1_opy_.l11111ll1l_opy_ != "no":
                        l1l1l1111l_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_,
                                                                     "part-abbreviation").text = l1l11111l1_opy_.l11111ll1l_opy_
                    if l1l11111l1_opy_.l111ll1111_opy_ != "no":
                        l1lll11ll1l_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_, "score-instrument")
                        l1lll11ll1l_opy_.attrib = {"id": l1l11111l1_opy_.l111ll1111_opy_}
                    if l1l11111l1_opy_.l1lllll111l_opy_ != "no":
                        l11l11ll1l_opy_ = l111lllll1_opy_.SubElement(l1lll11ll1l_opy_,
                                                                     "instrument-name").text = l1l11111l1_opy_.l1lllll111l_opy_
                    if l1l11111l1_opy_.l1l11l11ll_opy_ != "no" or l1l11111l1_opy_.l11l11l111_opy_ != "no":
                        l1l1111ll1_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_, "midi-device")
                        l1l1111ll1_opy_.attrib = {"id": l1l11111l1_opy_.l1l11l11ll_opy_,
                                                  "port": l1l11111l1_opy_.l11l11l111_opy_}
                    if l1l11111l1_opy_.l111ll1ll1_opy_ != "no":
                        l1llllll111_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_, "midi-instrument")
                        l1llllll111_opy_.attrib = {"id": l1l11111l1_opy_.l111ll1ll1_opy_}
                    if l1l11111l1_opy_.l111ll11ll_opy_ != "no":
                        l11ll1ll1l_opy_ = l111lllll1_opy_.SubElement(l1llllll111_opy_,
                                                                     "midi-channel").text = l1l11111l1_opy_.l111ll11ll_opy_
                    if l1l11111l1_opy_.l11ll11l11_opy_ != "no":
                        l1l11lll11_opy_ = l111lllll1_opy_.SubElement(l1llllll111_opy_,
                                                                     "midi-program").text = l1l11111l1_opy_.l11ll11l11_opy_
                    if l1l11111l1_opy_.l1lllll1lll_opy_ != "no":
                        l111lll1l1_opy_ = l111lllll1_opy_.SubElement(l1llllll111_opy_,
                                                                     "volume").text = l1l11111l1_opy_.l1lllll1lll_opy_
                    if l1l11111l1_opy_.l1111ll1ll_opy_ != "no":
                        l11ll1l1ll_opy_ = l111lllll1_opy_.SubElement(l1llllll111_opy_,
                                                                     "pan").text = l1l11111l1_opy_.l1111ll1ll_opy_
                    if l1l11111l1_opy_.l1lll111lll_opy_ == True:
                        l11ll1l11l_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_,
                                                                     "braille-ascending-chords").text = "1"
                    elif l1l11111l1_opy_.l1lll111lll_opy_ == False:
                        l11ll1l11l_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_,
                                                                     "braille-ascending-chords").text = "-1"
                    else:
                        l11ll1l11l_opy_ = l111lllll1_opy_.SubElement(l1111l1l1l_opy_,
                                                                     "braille-ascending-chords").text = l1l11111l1_opy_.l1lll111lll_opy_
            elif element.t == "credit":
                l11l11lll1_opy_ = l111lllll1_opy_.SubElement(root, "credit")
                l11l11lll1_opy_.attrib = {"page": "1"}
                if element.l111lll111_opy_ != "no":
                    l111l11ll1_opy_ = l111lllll1_opy_.SubElement(l11l11lll1_opy_,
                                                                 "credit-type").text = element.l111lll111_opy_
                l11ll11lll_opy_ = l111lllll1_opy_.SubElement(l11l11lll1_opy_,
                                                             "credit-words").text = element.l1llll1ll11_opy_
            elif element.t == "braille-global":
                l1l111ll1l_opy_ = l111lllll1_opy_.SubElement(root, "braille-global")
                for event in element.l11l1l1lll_opy_:
                    if event.t == "global-key":
                        l1l111l1l1_opy_ = l111lllll1_opy_.SubElement(l1l111ll1l_opy_, "global-key")
                        l1llll1l1ll_opy_ = l111lllll1_opy_.SubElement(l1l111l1l1_opy_, "global-fifths").text = str(
                            event.l1lll1l1l11_opy_)
                    if event.t == "global-time":
                        l111111lll_opy_ = l111lllll1_opy_.SubElement(l1l111ll1l_opy_, "global-time")
                        l1lll1ll1l1_opy_ = l111lllll1_opy_.SubElement(l111111lll_opy_,
                                                                      "global-beats").text = event.l1l1l11111_opy_
                        l111111l11_opy_ = l111lllll1_opy_.SubElement(l111111lll_opy_,
                                                                     "global-beat-type").text = event.l1111lll11_opy_
                        if event.l11lllll1l_opy_ != "no":
                            l111111lll_opy_.attrib = {"symbol": event.l11lllll1l_opy_}
        l111llll1l_opy_ = minidom.parseString(l111lllll1_opy_.tostring(root)).toprettyxml(indent="   ",
                                                                                          encoding="UTF-8",
                                                                                          standalone="")
        if l1l11ll11l_opy_:
            self._11lllll1_opy_(str(l111llll1l_opy_))
        self._1l1111ll_opy_(l111llll1l_opy_)
        l1l1111lll_opy_ = time.time()
        print("temps model to bxml", l1l1111lll_opy_ - t1)
