"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import xml.etree.ElementTree as l1ll111111_opy_
from xml.dom import minidom
from .l11111ll1_opy_ import *
class l11111l11_opy_:
    def __init__ (self, l1l11lll1l_opy_, l1l111l1l1_opy_, l1l1ll1ll_opy_):
        self._1l111lll_opy_ = l1l11lll1l_opy_
        self._1l1l1l1l_opy_ = l1l111l1l1_opy_
        self._1l1lll11_opy_ = l1l1ll1ll_opy_
    def create_file(self):
        self._1l1l1l1l_opy_("\nmodel to xml\n")
        root = l1ll111111_opy_.Element("score-partwise")
        root.attrib = {"version":"2.0"}
        l111l1ll1_opy_ = l1ll111111_opy_.SubElement(root, "defaults")
        l1111lll1_opy_ = l1ll111111_opy_.SubElement(l111l1ll1_opy_, "lyric-font")
        l1111lll1_opy_.attrib = {"font-family": "Times New Roman"}
        for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
            if element.t == "credit":
                l1lll1ll11_opy_ = l1ll111111_opy_.SubElement(root, "credit")
                l1lll1ll11_opy_.attrib = {"page":"1"}
                if element.l1111l11l_opy_ !="no":
                    l1l111111l_opy_ = l1ll111111_opy_.SubElement(l1lll1ll11_opy_, "credit-type").text = element.l1111l11l_opy_
                l1l111lll1_opy_ = l1ll111111_opy_.SubElement(l1lll1ll11_opy_, "credit-words").text = element.l11l111l1_opy_
            if element.t == "part-list":
                l1l1ll1l1l_opy_ = l1ll111111_opy_.SubElement(root, "part-list")
                for l1ll11ll11_opy_ in element.l1lll11ll1_opy_:
                    l11l1ll1l_opy_ = l1ll111111_opy_.SubElement(l1l1ll1l1l_opy_, "score-part")
                    if l1ll11ll11_opy_.l1ll11lll1_opy_ != "no":
                        l11l1ll1l_opy_.attrib = {"id":l1ll11ll11_opy_.l1ll11lll1_opy_}
                    if l1ll11ll11_opy_.l1lllll111_opy_ != "no":
                        l1l1ll11l1_opy_ = l1ll111111_opy_.SubElement(l11l1ll1l_opy_, "part-name").text = l1ll11ll11_opy_.l1lllll111_opy_
                    if l1ll11ll11_opy_.l111l1l11_opy_ != "no":
                        l111lllll_opy_ = l1ll111111_opy_.SubElement(l11l1ll1l_opy_, "part-abbreviation").text = l1ll11ll11_opy_.l111l1l11_opy_
                    if l1ll11ll11_opy_.l11ll1111_opy_ != "no":
                        l1l1111l11_opy_ = l1ll111111_opy_.SubElement(l11l1ll1l_opy_, "score-instrument")
                        l1l1111l11_opy_.attrib = {"id":l1ll11ll11_opy_.l11ll1111_opy_}
                    if l1ll11ll11_opy_.l1l1l1l111_opy_ != "no":
                        l1l111ll1l_opy_ = l1ll111111_opy_.SubElement(l1l1111l11_opy_, "instrument-name").text = l1ll11ll11_opy_.l1l1l1l111_opy_
                    if l1ll11ll11_opy_.l1l11l1ll1_opy_ != "no" or l1ll11ll11_opy_.l1l1l1llll_opy_ != "no":
                        l1l1l111ll_opy_ = l1ll111111_opy_.SubElement(l11l1ll1l_opy_, "midi-device")
                        l1l1l111ll_opy_.attrib = {"id":l1ll11ll11_opy_.l1l11l1ll1_opy_, "port":l1ll11ll11_opy_.l1l1l1llll_opy_}
                    if l1ll11ll11_opy_.l1lll1l1ll_opy_ != "no":
                        l1ll111l11_opy_ = l1ll111111_opy_.SubElement(l11l1ll1l_opy_, "midi-instrument")
                        l1ll111l11_opy_.attrib = {"id":l1ll11ll11_opy_.l1lll1l1ll_opy_}
                    if l1ll11ll11_opy_.l1llll1l1l_opy_ != "no":
                        l1l11l11l1_opy_ = l1ll111111_opy_.SubElement(l1ll111l11_opy_, "midi-channel").text = l1ll11ll11_opy_.l1llll1l1l_opy_
                    if l1ll11ll11_opy_.l11111l1l_opy_ != "no":
                        l1ll1l1111_opy_ = l1ll111111_opy_.SubElement(l1ll111l11_opy_, "midi-program").text = l1ll11ll11_opy_.l11111l1l_opy_
                    if l1ll11ll11_opy_.l11ll1l1l_opy_ != "no":
                        l1111l1ll_opy_ = l1ll111111_opy_.SubElement(l1ll111l11_opy_, "volume").text = l1ll11ll11_opy_.l11ll1l1l_opy_
                    if l1ll11ll11_opy_.l1lll111l1_opy_ != "no":
                        l11l111ll_opy_ = l1ll111111_opy_.SubElement(l1ll111l11_opy_, "pan").text = l1ll11ll11_opy_.l1lll111l1_opy_
            if element.t == "part":
                l1ll1lll1l_opy_ = l1ll111111_opy_.SubElement(root, "part")
                l1ll1lll1l_opy_.attrib = {"id":element.l1ll11lll1_opy_}
                for l11l11l11_opy_ in element.l11l1llll_opy_:
                    l1l1l11ll1_opy_ = l1ll111111_opy_.SubElement(l1ll1lll1l_opy_, "measure")
                    l1l1l11ll1_opy_.attrib = {"number":str(l11l11l11_opy_.l1l111l111_opy_)}
                    l1ll1l11l1_opy_ = False
                    l1ll1ll1ll_opy_ = False
                    l1111ll11_opy_ = False
                    l1lllllll1_opy_ = False
                    l111ll1ll_opy_ = False
                    l1l11l1l1l_opy_ = False
                    for event in l11l11l11_opy_.l11llll11_opy_:
                        l1ll1l1l11_opy_ = False
                        if event.t == "attributes":
# l11l11ll1_opy_ l11l1l1l1_opy_ l11l1lll1_opy_ element to be l1l11l11ll_opy_ to l1ll1l111l_opy_ l1l1l11l1l_opy_ in the l11111lll_opy_ order
                            for l1l1ll1l11_opy_ in event.l1l1lll11l_opy_:
                                if l1l1ll1l11_opy_.t == "divisions":
                                    l1ll1l11l1_opy_ = True
                                    l1111l1l1_opy_ = str(l1l1ll1l11_opy_.l1llll11l1_opy_)
                                if l1l1ll1l11_opy_.t == "key":
                                    l1ll1ll1ll_opy_ = True
                                    l11l11l1l_opy_ = str(l1l1ll1l11_opy_.l1l1l1l1l1_opy_)
                                    l1l1l1111l_opy_ = l1l1ll1l11_opy_.mode
                                if l1l1ll1l11_opy_.t == "time":
                                    l1111ll11_opy_ = True
                                    l1l11lll11_opy_ = l1l1ll1l11_opy_.l1l11l1111_opy_
                                    l111l11ll_opy_ = l1l1ll1l11_opy_.l1l11ll111_opy_
                                    l11ll1l11_opy_ = l1l1ll1l11_opy_.l1ll1llll1_opy_
                                if l1l1ll1l11_opy_.t == "staves":
                                    l1lllllll1_opy_ = True
                                    l1l1l1l11l_opy_ = l1l1ll1l11_opy_.l1l1lll111_opy_
                                if l1l1ll1l11_opy_.t == "clef":
                                    l111ll1ll_opy_ = True
                                    l1lll111ll_opy_ = l1l1ll1l11_opy_.sign
                                    l1ll11l111_opy_ = l1l1ll1l11_opy_.line
                                    l1lllll1ll_opy_ = l1l1ll1l11_opy_.l1l1ll1111_opy_
                        else:
# l1ll1l111l_opy_ l1l11llll1_opy_ to have l1l111l1ll_opy_ in the l11111lll_opy_ order for l1l1l11l1l_opy_
                            if l1ll1l11l1_opy_ or l1ll1ll1ll_opy_ or l1111ll11_opy_ or l1lllllll1_opy_ or l111ll1ll_opy_:
                                l1l1l1lll1_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "attributes")
                                if l1ll1l11l1_opy_:
                                    l11ll11ll_opy_ = l1ll111111_opy_.SubElement(l1l1l1lll1_opy_, "divisions").text = l1111l1l1_opy_
                                    l1ll1l11l1_opy_ = False
                                if l1ll1ll1ll_opy_:
                                    l11llll1l_opy_ = l1ll111111_opy_.SubElement(l1l1l1lll1_opy_, "key")
                                    l1l11lllll_opy_ = l1ll111111_opy_.SubElement(l11llll1l_opy_, "fifths").text = l11l11l1l_opy_
                                    if l1l1l1111l_opy_ !="no":
                                        l1l1lll1l1_opy_ = l1ll111111_opy_.SubElement(l11llll1l_opy_, "mode").text = l1l1l1111l_opy_
                                    l1ll1ll1ll_opy_ = False
                                if l1111ll11_opy_:
                                    l1ll11llll_opy_ = l1ll111111_opy_.SubElement(l1l1l1lll1_opy_, "time")
                                    l11l1l1ll_opy_ = l1ll111111_opy_.SubElement(l1ll11llll_opy_, "beats").text = l1l11lll11_opy_
                                    l1ll1l1l1l_opy_ = l1ll111111_opy_.SubElement(l1ll11llll_opy_, "beat-type").text = l111l11ll_opy_
                                    if l11ll1l11_opy_ != "no":
                                        l1ll11llll_opy_.attrib = {"symbol":l11ll1l11_opy_}
                                    l1111ll11_opy_ = False
                                if l1lllllll1_opy_:
                                    l1l1111lll_opy_ = l1ll111111_opy_.SubElement(l1l1l1lll1_opy_, "staves").text = l1l1l1l11l_opy_
                                    l1lllllll1_opy_ = False
                                if l111ll1ll_opy_:
                                    l1lll1l111_opy_ = l1ll111111_opy_.SubElement(l1l1l1lll1_opy_, "clef")
                                    l1lll1llll_opy_ = l1ll111111_opy_.SubElement(l1lll1l111_opy_, "sign").text = l1lll111ll_opy_
                                    l1l11111l_opy_ = l1ll111111_opy_.SubElement(l1lll1l111_opy_, "line").text = l1ll11l111_opy_
                                    if l1lllll1ll_opy_ !="no":
                                        l11ll11l1_opy_ = l1ll111111_opy_.SubElement(l1lll1l111_opy_, "clef-octave-change").text = l1lllll1ll_opy_
                                    l111ll1ll_opy_ = False
                        if event.t == "note":
                            l1lllll11l_opy_ = False
                            l11lll11l_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "note")
                            if event.l1ll1ll11l_opy_:
                                l1ll1l11ll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "grace")
                            if event.l1lll1l1l1_opy_:
                                l1ll1l11ll_opy_.attrib = {"slash":"yes"}
                            if event.l1lll1l1l1_opy_ == "no":
                                l1ll1l11ll_opy_.attrib = {"slash":"no"}
                            if event.l11ll1lll_opy_:
                                l111lll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "chord")
                            if event.step !="no":
                                l11llllll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "pitch")
                                l1l1111ll_opy_ = l1ll111111_opy_.SubElement(l11llllll_opy_, "step").text = l1l11ll1ll_opy_[event.step]
                            if event.l1111l111_opy_ !="no":
                                l1l1l11lll_opy_ = l1ll111111_opy_.SubElement(l11llllll_opy_, "alter").text = l111111ll_opy_[event.l1111l111_opy_]
                            if event.l1l1llllll_opy_ !=100:
                                l1l11111l1_opy_ = l1ll111111_opy_.SubElement(l11llllll_opy_, "octave").text = str(event.l1l1llllll_opy_)
                            if event.rest:
                                l111lll1l_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "rest")
                            if event.l1l1ll1ll1_opy_ != 0:
                                l1l11l1l11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "duration").text = str(event.l1l1ll1ll1_opy_)
                            if event.l1l11l111l_opy_:
                                l1llll11ll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "tie")
                                if event.l1l111l11l_opy_ !="no":
                                    l1llll11ll_opy_.attrib = {"type":event.l1l111l11l_opy_}
                            if event.l11lll1l1_opy_ != 0:
                                l111l1lll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "voice").text = str(event.l11lll1l1_opy_)
                            if event.type !="no":
                                l111l1111_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "type").text = l1ll1111l1_opy_[event.type]
                            if event.dot:
                                l1ll11l1l1_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "dot")
                            if event.l1l11ll1l1_opy_ != "no":
                                l1ll11l1ll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "accidental").text = event.l1l11ll1l1_opy_
                            if event.l1ll1lll11_opy_ !=0 and event.l1l1ll1lll_opy_ != 0:
                                l1l1lllll1_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "time-modification")
                                l1llll1111_opy_ = l1ll111111_opy_.SubElement(l1l1lllll1_opy_, "actual-notes").text = str(event._11ll1ll1_opy_)
                                l1llll1l11_opy_ = l1ll111111_opy_.SubElement(l1l1lllll1_opy_, "normal-notes").text = str(event._11l1ll11_opy_)
                            if event.l1l1ll111l_opy_ !="no":
                                l1l1llll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "staff").text = str(event.l1l1ll111l_opy_)
                            if event.l1l11l111l_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l1lll1lll1_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "tied")
                                if event.l1l111l11l_opy_ !="no":
                                    l1lll1lll1_opy_.attrib = {"type":event.l1l111l11l_opy_}
                            if event.l111llll1_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l1l1l11l11_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "slur")
                                if event.l111ll11l_opy_ !="no":
                                    l1l1l11l11_opy_.attrib = {"type":event.l111ll11l_opy_}
                                if event.l1l11l1lll_opy_ !="no":
                                    l1l1l11l11_opy_.attrib.update ({"number":event.l1l11l1lll_opy_})
                                if event.l1lll1111l_opy_ !="no":
                                    l1l1l11l11_opy_.attrib.update ({"placement":event.l1lll1111l_opy_})
                            if event.l11l1111l_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l1l1l11l11_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "slur")
                                if event.l1l111111_opy_ !="no":
                                    l1l1l11l11_opy_.attrib = {"type":event.l1l111111_opy_}
                                if event.l1lll11lll_opy_ !="no":
                                    l1l1l11l11_opy_.attrib.update ({"number":event.l1lll11lll_opy_})
                                if event.l1111111l_opy_ !="no":
                                    l1l1l11l11_opy_.attrib.update ({"placement":event.l1111111l_opy_})
                            if event.l1l1l1l1ll_opy_ !="no":
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l1lllll1l1_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "technical")
                                l1ll1l1lll_opy_ = l1ll111111_opy_.SubElement(l1lllll1l1_opy_, "fingering").text = event.l1l1l1l1ll_opy_
                            if event.l11lll111_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l11lll1ll_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "articulations")
                                l11111111_opy_ = l1ll111111_opy_.SubElement(l11lll1ll_opy_, "staccato")
                            if event.l11lllll1_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l11lll1ll_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "articulations")
                                l111l111l_opy_ = l1ll111111_opy_.SubElement(l11lll1ll_opy_, "staccatissimo")
                            if event.l1l1111l1l_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l11lll1ll_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "articulations")
                                l111l11l1_opy_ = l1ll111111_opy_.SubElement(l11lll1ll_opy_, "accent")
                            if event.l1ll11111l_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l11lll1ll_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "articulations")
                                l111ll1l1_opy_ = l1ll111111_opy_.SubElement(l11lll1ll_opy_, "breath-mark")
                            if event.l1ll1l1ll1_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l1l1111111_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "fermata")
                            if event.l1l11ll11l_opy_:
                                if not l1lllll11l_opy_:
                                    l1l111ll11_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "notations")
                                    l1lllll11l_opy_ = True
                                l11ll111l_opy_ = l1ll111111_opy_.SubElement(l1l111ll11_opy_, "ornaments")
                                l1l1l11111_opy_ = l1ll111111_opy_.SubElement(l11ll111l_opy_, "trill-mark")
                            if event.text != "":
                                l1ll1lllll_opy_ = l1ll111111_opy_.SubElement(l11lll11l_opy_, "lyric")
                                l1ll1ll1l1_opy_ = l1ll111111_opy_.SubElement(l1ll1lllll_opy_, "syllabic").text = event._1llllll1l_opy_
                                l1l1l1ll1l_opy_ = l1ll111111_opy_.SubElement(l1ll1lllll_opy_, "text").text = event.text
                        if event.t == "direction":
                            l1ll11ll1l_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "direction")
                            if event.l1lll11l11_opy_ != "no":
                                l1ll11ll1l_opy_.attrib = {"placement":event.l1lll11l11_opy_}
                            for l1l1ll1l11_opy_ in event.l11l1l111_opy_:
                                if l1l1ll1l11_opy_.t == "dynamics":
                                    l1ll111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "direction-type")
                                    l1l1111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll111ll1_opy_, "dynamics")
                                    l111l1l1l_opy_ = l1ll111111_opy_.SubElement(l1l1111ll1_opy_, l1l1ll1l11_opy_.l1ll11l11l_opy_)
                                if l1l1ll1l11_opy_.t == "pedal":
                                    l1ll111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "direction-type")
                                    l11l11111_opy_ = l1ll111111_opy_.SubElement(l1ll111ll1_opy_, "pedal")
                                    l11l11111_opy_.attrib = {"type":l1l1ll1l11_opy_.l1llllll11_opy_}
                                if l1l1ll1l11_opy_.t == "wedge":
                                    l1ll111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "direction-type")
                                    l1l1llll1l_opy_ = l1ll111111_opy_.SubElement(l1ll111ll1_opy_, "wedge")
                                    l1l1llll1l_opy_.attrib = {"type":l1l1ll1l11_opy_.l1l1111l1_opy_}
                                if l1l1ll1l11_opy_.t == "metronome":
                                    l1ll111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "direction-type")
                                    l11l11lll_opy_ = l1ll111111_opy_.SubElement(l1ll111ll1_opy_, "metronome")
                                    if l1l1ll1l11_opy_.l1llll111l_opy_ != "no":
                                        l1llll1lll_opy_ = l1ll111111_opy_.SubElement(l11l11lll_opy_, "beat-unit").text = l1l1ll1l11_opy_.l1llll111l_opy_
                                    if l1l1ll1l11_opy_.l1ll1ll111_opy_:
                                        l1llll1lll_opy_ = l1ll111111_opy_.SubElement(l11l11lll_opy_, "beat-unit-dot")
                                    if l1l1ll1l11_opy_.l111111l1_opy_ != "no":
                                        l11l1l11l_opy_ = l1ll111111_opy_.SubElement(l11l11lll_opy_, "per-minute").text = l1l1ll1l11_opy_.l111111l1_opy_
                                if l1l1ll1l11_opy_.t == "sound":
                                    l1l1l111l1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "sound")
                                    if l1l1ll1l11_opy_.l1l11111ll_opy_ != "no":
                                        l1l1l111l1_opy_.attrib = {"tempo":l1l1ll1l11_opy_.l1l11111ll_opy_}
                                    if l1l1ll1l11_opy_.l1l111llll_opy_ != "no":
                                        l1l1l111l1_opy_.attrib = {"tempo":l1l1ll1l11_opy_.l1l111llll_opy_}
                                if l1l1ll1l11_opy_.t == "words":
                                    l1ll111ll1_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "direction-type")
                                    l1ll111lll_opy_ = l1ll111111_opy_.SubElement(l1ll111ll1_opy_, "words").text = l1l1ll1l11_opy_.words
                            if event.l1l1ll111l_opy_ != 1:
                                l1111ll1l_opy_ = l1ll111111_opy_.SubElement(l1ll11ll1l_opy_, "staff").text = str(event.l1l1ll111l_opy_)
                        if event.t == "backup":
                            l111ll111_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "backup")
                            l1l11l1l11_opy_ = l1ll111111_opy_.SubElement(l111ll111_opy_, "duration").text = str(event.l1l1ll1ll1_opy_)
                        if event.t == "barline":
                            l1lll11111_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "barline")
                            if event.location != "no":
                                l1lll11111_opy_.attrib = {"location":event.location}
                            if event.l1ll1111ll_opy_ != "no":
                                l1ll111l1l_opy_ = l1ll111111_opy_.SubElement(l1lll11111_opy_, "bar-style").text = event.l1ll1111ll_opy_
                            if event.l1llll1ll1_opy_ != "no":
                                l1111llll_opy_ = l1ll111111_opy_.SubElement(l1lll11111_opy_, "repeat")
                                l1111llll_opy_.attrib = {"direction":event.l1llll1ll1_opy_}
                        if event.t == "print":
                            l1lll1l11l_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "print")
                            if event.l1llllllll_opy_ != "no":
                                l1lll1l11l_opy_.attrib = {"new-system":event.l1llllllll_opy_}
                        if event.t == "karaoke":
                            l1l1l1ll11_opy_ = l1ll111111_opy_.SubElement(l1l1l11ll1_opy_, "karaoke").text = event.l1l1lll1ll_opy_
        l1lll11l1l_opy_ = minidom.parseString(l1ll111111_opy_.tostring(root)).toprettyxml(indent="   ", encoding="UTF-8", standalone="")
#        self._1l1l1l1l_opy_ (l1lll11l1l_opy_)
        self._1l111lll_opy_ (l1lll11l1l_opy_)