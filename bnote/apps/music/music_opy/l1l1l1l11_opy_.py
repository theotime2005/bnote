"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import xml.etree.ElementTree as l1lll1l11ll_opy_
from xml.dom import minidom
from .l11ll1l1ll_opy_ import *
import time
class l1l1l1ll1_opy_:
    def __init__ (self, l11ll1ll11_opy_, l111l11l11_opy_, l1ll1l1ll_opy_):
        self._1l11l11l_opy_ = l11ll1ll11_opy_
        self._1l111lll_opy_ = l111l11l11_opy_
        self._1lll111l_opy_ = l1ll1l1ll_opy_
    def create_file(self):
        t1 = time.time()
        l1lll1l1lll_opy_ = False
        if l1lll1l1lll_opy_:
            self._1l111lll_opy_("\nmodel to xml\n")
        root = l1lll1l11ll_opy_.Element("score-partwise")
        root.attrib = {"version":"4.0"}
        #l1lll1ll1l1_opy_ = l1lll1l11ll_opy_.SubElement(root, "defaults")
        #l11l1ll1l1_opy_ = l1lll1l11ll_opy_.SubElement(l1lll1ll1l1_opy_, "lyric-font")
        #l11l1ll1l1_opy_.attrib = {"font-family": "Times New Roman"}
        l1l1llllll1l_opy_ = False
        l1ll11111111_opy_ = False
        for element in self._1lll111l_opy_.l1l111llll_opy_:
            if element.t == "part":
                l1llll11lll_opy_ = l1lll1l11ll_opy_.SubElement(root, "part")
                l1llll11lll_opy_.attrib = {"id":element.l1lll1l11l1_opy_}
                for l1lllll11ll_opy_ in element.l1lllllll11_opy_:
                    l1l111ll11_opy_ = l1lll1l11ll_opy_.SubElement(l1llll11lll_opy_, "measure")
                    l1l111ll11_opy_.attrib = {"number":str(l1lllll11ll_opy_.l11ll111ll_opy_)}
                    l11l1l1111_opy_ = False
                    l11llll1ll_opy_ = False
                    l111ll1l1l_opy_ = False
                    l1l11l1l1l_opy_ = False
                    l111l11ll1_opy_ = False
                    l111ll1111_opy_ = False
                    l11lllll11_opy_ = False
                    for event in l1lllll11ll_opy_.l111111lll_opy_:
                        l111l1111l_opy_ = False
                        if event.t == "attributes":
                            for l11111l1l1_opy_ in event.l1l11l1111_opy_:
                                if l11111l1l1_opy_.t == "divisions":
                                    l11l1l1111_opy_ = True
                                    l11ll11l11_opy_ = str(l11111l1l1_opy_.l111lll1l1_opy_)
                                elif l11111l1l1_opy_.t == "key":
                                    l11llll1ll_opy_ = True
                                    l11l1l1ll1_opy_ = str(l11111l1l1_opy_.l11ll1111l_opy_)
                                    l11l1lllll_opy_ = l11111l1l1_opy_.mode
                                elif l11111l1l1_opy_.t == "time":
                                    l111ll1l1l_opy_ = True
                                    l11llll1l1_opy_ = l11111l1l1_opy_.l1l1l1l1l1_opy_
                                    l1111l111l_opy_ = l11111l1l1_opy_.l1llll1l1l1_opy_
                                    l111lll11l_opy_ = l11111l1l1_opy_.l1l1l1ll1l_opy_
                                elif l11111l1l1_opy_.t == "staves":
                                    l1l11l1l1l_opy_ = True
                                    l11ll11ll1_opy_ = l11111l1l1_opy_.l1lll1l1ll1_opy_
                                elif l11111l1l1_opy_.t == "clef":
                                    l111l11ll1_opy_ = True
                                    l1l1l1l11l_opy_ = l11111l1l1_opy_.sign
                                    l11l1111l1_opy_ = l11111l1l1_opy_.line
                                    l11ll11111_opy_ = l11111l1l1_opy_.l11l1lll11_opy_
                                elif l11111l1l1_opy_.t == "transpose":
                                    l111ll1111_opy_ = True
                                    l1l11l111l_opy_ = str(l11111l1l1_opy_.l111lll1ll_opy_)
                                    l1l1l11ll1_opy_ = str(l11111l1l1_opy_.l1l1l1111l_opy_)
                                    l11l1l1l11_opy_ = str(l11111l1l1_opy_.l111111l1l_opy_)
                                    l1l11l11l1_opy_ = l11111l1l1_opy_.l1lllll1l11_opy_
                                    l1111lll11_opy_ = l11111l1l1_opy_.l11ll1l111_opy_
                        else:
                            if l11l1l1111_opy_ or l11llll1ll_opy_ or l111ll1l1l_opy_ or l1l11l1l1l_opy_ or l111l11ll1_opy_ or l111ll1111_opy_:
                                l11l1ll1ll_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "attributes")
                                if l11l1l1111_opy_:
                                    l1llllllll1_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "divisions").text = l11ll11l11_opy_
                                    l11l1l1111_opy_ = False
                                if l11llll1ll_opy_:
                                    l11l11l1ll_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "key")
                                    l1111l11ll_opy_ = l1lll1l11ll_opy_.SubElement(l11l11l1ll_opy_, "fifths").text = l11l1l1ll1_opy_
                                    if l11l1lllll_opy_ !="no":
                                        l111l1ll1l_opy_ = l1lll1l11ll_opy_.SubElement(l11l11l1ll_opy_, "mode").text = l11l1lllll_opy_
                                    l11llll1ll_opy_ = False
                                if l111ll1l1l_opy_:
                                    l1111111ll_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "time")
                                    l1l11l1l11_opy_ = l1lll1l11ll_opy_.SubElement(l1111111ll_opy_, "beats").text = l11llll1l1_opy_
                                    l11ll1ll1l_opy_ = l1lll1l11ll_opy_.SubElement(l1111111ll_opy_, "beat-type").text = l1111l111l_opy_
                                    if l111lll11l_opy_ != "no":
                                        l1111111ll_opy_.attrib = {"symbol":l111lll11l_opy_}
                                    l111ll1l1l_opy_ = False
                                if l1l11l1l1l_opy_:
                                    l1llll11l1l_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "staves").text = l11ll11ll1_opy_
                                    l1l11l1l1l_opy_ = False
                                if l111l11ll1_opy_:
                                    l111111l11_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "clef")
                                    l1111l1l1l_opy_ = l1lll1l11ll_opy_.SubElement(l111111l11_opy_, "sign").text = l1l1l1l11l_opy_
                                    l11lll1111_opy_ = l1lll1l11ll_opy_.SubElement(l111111l11_opy_, "line").text = l11l1111l1_opy_
                                    if l11ll11111_opy_ !="no":
                                        l1111ll11l_opy_ = l1lll1l11ll_opy_.SubElement(l111111l11_opy_, "clef-octave-change").text = l11ll11111_opy_
                                    l111l11ll1_opy_ = False
                                if l111ll1111_opy_:
                                    l111l1l11l_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll1ll_opy_, "transpose")
                                    l1l11ll11l_opy_ = l1lll1l11ll_opy_.SubElement(l111l1l11l_opy_, "diatonic").text = l1l11l111l_opy_
                                    l11l11l111_opy_ = l1lll1l11ll_opy_.SubElement(l111l1l11l_opy_, "chromatic").text = l1l1l11ll1_opy_
                                    l111l1lll1_opy_ = l1lll1l11ll_opy_.SubElement(l111l1l11l_opy_, "octave-change").text = l11l1l1l11_opy_
                                    if l1l11l11l1_opy_:
                                        l11l11lll1_opy_ = l1lll1l11ll_opy_.SubElement(l111l1l11l_opy_, "double")
                                        if l1111lll11_opy_ != "":
                                            l11l11lll1_opy_.attrib = {"above": l1111lll11_opy_}
                                    l111ll1111_opy_ = False
                        if event.t == "note":
                            l1lllllll1l_opy_ = False
                            l111lll111_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "note")
                            if event.l1lllll1111_opy_:
                                l11l11l1l1_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "grace")
                                if event.l1lll1l111l_opy_ !="missing":
                                    l11l11l1l1_opy_.attrib = {"slash": event.l1lll1l111l_opy_}
                            if event.l1lllllllll_opy_:
                                l1lll1lll1l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "chord")
                            if event.step !="no":
                                l111l11lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "pitch")
                                l11l11ll11_opy_ = l1lll1l11ll_opy_.SubElement(l111l11lll_opy_, "step").text = l1111lll1l_opy_[event.step]
                            if event.l11l11l11l_opy_ !="no":
                                l11111lll1_opy_ = l1lll1l11ll_opy_.SubElement(l111l11lll_opy_, "alter").text = l1llll11ll1_opy_[event.l11l11l11l_opy_]
                            if event.l111ll1l11_opy_ !=100:
                                l1llll11111_opy_ = l1lll1l11ll_opy_.SubElement(l111l11lll_opy_, "octave").text = str(event.l111ll1l11_opy_)
                            if event.rest:
                                l1llll1ll1l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "rest")
                            if event.l1lll1ll1ll_opy_ != 0:
                                l1l1l1llll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "duration").text = str(event.l1lll1ll1ll_opy_)
                            if event.l11ll1l1l1_opy_:
                                l11111111l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "tie")
                                if event.l1llll111ll_opy_ in ["start", "stop"]:
                                    l11111111l_opy_.attrib = {"type": event.l1llll111ll_opy_}
                                elif event.l1llll111ll_opy_ == "stop-start":
                                    l11111111l_opy_.attrib = {"type":"stop"}
                                    l11111111l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "tie")
                                    l11111111l_opy_.attrib = {"type": "start"}
                            if event.l1llll11l11_opy_ != 0:
                                l1l1l1ll11_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "voice").text = str(event.l1llll11l11_opy_)
                            if event.type !="no":
                                l1llll1llll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "type").text = l11l111l1l_opy_[event.type]
                            if event.dot:
                                l11l1ll11l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "dot")
                            if event.l111llll11_opy_ != "no":
                                l1llll1l11l_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "accidental").text = event.l111llll11_opy_
                            if event.l1lllll111l_opy_ !=0 and event.l1l11l11ll_opy_ != 0:
                                l1l1l111l1_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "time-modification")
                                l1l1111ll1_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l111l1_opy_, "actual-notes").text = str(event.l1lllll111l_opy_)
                                l1l1l1l111_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l111l1_opy_, "normal-notes").text = str(event.l1l11l11ll_opy_)
                            if event.l11l11ll1l_opy_ !="no":
                                l1111111l1_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "staff").text = str(event.l11l11ll1l_opy_)
                            if event.l11ll1l1l1_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11l1l11l1_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "tied")
                                if event.l1llll111ll_opy_ in ["start", "stop"]:
                                    l11l1l11l1_opy_.attrib = {"type": event.l1llll111ll_opy_}
                                elif event.l1llll111ll_opy_ == "stop-start":
                                    l11l1l11l1_opy_.attrib = {"type": "stop"}
                                    l11l1l11l1_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "tied")
                                    l11l1l11l1_opy_.attrib = {"type": "start"}
                            if event.l111l11111_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11ll1l11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "slur")
                                if event.l1lll1lll11_opy_ !="no":
                                    l11ll1l11l_opy_.attrib = {"type":event.l1lll1lll11_opy_}
                                if event.l11l111l11_opy_ !="no":
                                    l11ll1l11l_opy_.attrib.update ({"number":event.l11l111l11_opy_})
                                if event.l1lll1l1111_opy_ !="no":
                                    l11ll1l11l_opy_.attrib.update ({"placement":event.l1lll1l1111_opy_})
                            if event.l11lllll1l_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11ll1l11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "slur")
                                if event.l111ll11ll_opy_ !="no":
                                    l11ll1l11l_opy_.attrib = {"type":event.l111ll11ll_opy_}
                                if event.l11l1111ll_opy_ !="no":
                                    l11ll1l11l_opy_.attrib.update ({"number":event.l11l1111ll_opy_})
                                if event.l11111ll1l_opy_ !="no":
                                    l11ll1l11l_opy_.attrib.update ({"placement":event.l11111ll1l_opy_})
                            if event.l1llllll1ll_opy_ !="no":
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11l1ll111_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "technical")
                                l111l1l1ll_opy_ = l1lll1l11ll_opy_.SubElement(l11l1ll111_opy_, "fingering").text = event.l1llllll1ll_opy_
                            if event.l1l1111lll_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11llll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "articulations")
                                l111l111ll_opy_ = l1lll1l11ll_opy_.SubElement(l11llll11l_opy_, "staccato")
                            if event.l1l111lll1_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11llll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "articulations")
                                l111l11l1l_opy_ = l1lll1l11ll_opy_.SubElement(l11llll11l_opy_, "staccatissimo")
                            if event.l11l1l1lll_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11llll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "articulations")
                                l11111l111_opy_ = l1lll1l11ll_opy_.SubElement(l11llll11l_opy_, "accent")
                            if event.l1llll111l1_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11llll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "articulations")
                                l1l11l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l11llll11l_opy_, "breath-mark")
                            if event.l11lll1l11_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l11lll111l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "fermata")
                            if event.l111llll1l_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l1llllll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "ornaments")
                                l111ll1lll_opy_ = l1lll1l11ll_opy_.SubElement(l1llllll11l_opy_, "trill-mark")
                            if event.l111ll11l1_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l1llllll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "ornaments")
                                l1l111111l_opy_ = l1lll1l11ll_opy_.SubElement(l1llllll11l_opy_, "inverted-mordent")
                                l1l111111l_opy_.attrib = {"placement": event.l11l1l111l_opy_}
                                l1l111111l_opy_.attrib = {"long": event.l1l1l1lll1_opy_}
                            if event.l11111l1ll_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l1llllll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "ornaments")
                                l111l1llll_opy_ = l1lll1l11ll_opy_.SubElement(l1llllll11l_opy_, "mordent")
                                l111l1llll_opy_.attrib = {"placement": event.l1l11ll111_opy_}
                                l111l1llll_opy_.attrib = {"long": event.l1lll1lllll_opy_}
                            if event.l1l1111l1l_opy_ or event.l1l1111l11_opy_:
                                if not l1lllllll1l_opy_:
                                    l1111l1lll_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "notations")
                                    l1lllllll1l_opy_ = True
                                l1lllll1l1l_opy_ = l1lll1l11ll_opy_.SubElement(l1111l1lll_opy_, "arpeggiate")
                                if event.l111lllll1_opy_ == "down" or event.l1llllll1l1_opy_ == "down":
                                    l1lllll1l1l_opy_.attrib = {"direction": "down"}
                            if event.text != "":
                                l1111ll1l1_opy_ = l1lll1l11ll_opy_.SubElement(l111lll111_opy_, "lyric")
                                l11ll111l1_opy_ = l1lll1l11ll_opy_.SubElement(l1111ll1l1_opy_, "syllabic").text = event.l1111l1ll1_opy_
                                l1111llll1_opy_ = l1lll1l11ll_opy_.SubElement(l1111ll1l1_opy_, "text").text = event.text
                        elif event.t == "direction":
                            l11lll1l1l_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "direction")
                            if event.l111l1l111_opy_ != "no":
                                l11lll1l1l_opy_.attrib = {"placement": event.l111l1l111_opy_}
                            for l11111l1l1_opy_ in event.l1111l11l1_opy_:
                                if l11111l1l1_opy_.t == "dynamics":
                                    l1l1l11l11_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "direction-type")
                                    l1l1l111ll_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l11l11_opy_, "dynamics")
                                    l1lll1l1l1l_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l111ll_opy_, l11111l1l1_opy_.l1lll1llll1_opy_)
                                if l11111l1l1_opy_.t == "pedal":
                                    l1l1l11l11_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "direction-type")
                                    l11111llll_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l11l11_opy_, "pedal")
                                    l11111llll_opy_.attrib = {"type":l11111l1l1_opy_.l11l1l1l1l_opy_}
                                if l11111l1l1_opy_.t == "wedge":
                                    l1l1l11l11_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "direction-type")
                                    l1llll1l111_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l11l11_opy_, "wedge")
                                    l1llll1l111_opy_.attrib = {"type":l11111l1l1_opy_.l11lll11l1_opy_}
                                if l11111l1l1_opy_.t == "metronome":
                                    l1l1l11l11_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "direction-type")
                                    l111111111_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l11l11_opy_, "metronome")
                                    if l11111l1l1_opy_.l11llll111_opy_ != "no":
                                        l11ll1lll1_opy_ = l1lll1l11ll_opy_.SubElement(l111111111_opy_, "beat-unit").text = l11111l1l1_opy_.l11llll111_opy_
                                    if l11111l1l1_opy_.l1lllll11l1_opy_:
                                        l11ll1lll1_opy_ = l1lll1l11ll_opy_.SubElement(l111111111_opy_, "beat-unit-dot")
                                    if l11111l1l1_opy_.l1l111ll1l_opy_ != "no":
                                        l1lll1l1l11_opy_ = l1lll1l11ll_opy_.SubElement(l111111111_opy_, "per-minute").text = l11111l1l1_opy_.l1l111ll1l_opy_
                                if l11111l1l1_opy_.t == "sound":
                                    l11l1lll1l_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "sound")
                                    if l11111l1l1_opy_.l1l11ll1l1_opy_ != "no":
                                        l11l1lll1l_opy_.attrib = {"tempo":l11111l1l1_opy_.l1l11ll1l1_opy_}
                                    if l11111l1l1_opy_.l11ll11l1l_opy_ != "no":
                                        l11l1lll1l_opy_.attrib = {"tempo":l11111l1l1_opy_.l11ll11l1l_opy_}
                                if l11111l1l1_opy_.t == "words":
                                    l1l1l11l11_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "direction-type")
                                    l111111ll1_opy_ = l1lll1l11ll_opy_.SubElement(l1l1l11l11_opy_, "words").text = l11111l1l1_opy_.words
                            if event.l11l11ll1l_opy_ != 1:
                                l11l1llll1_opy_ = l1lll1l11ll_opy_.SubElement(l11lll1l1l_opy_, "staff").text = str(event.l11l11ll1l_opy_)
                        elif event.t == "backup":
                            l1llll1lll1_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "backup")
                            l1l1l1llll_opy_ = l1lll1l11ll_opy_.SubElement(l1llll1lll1_opy_, "duration").text = str(event.l1lll1ll1ll_opy_)
                        elif event.t == "barline":
                            l11l1l11ll_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "barline")
                            if event.location != "no":
                                l11l1l11ll_opy_.attrib = {"location":event.location}
                            if event.l111ll1ll1_opy_ != "no":
                                l1l1111111_opy_ = l1lll1l11ll_opy_.SubElement(l11l1l11ll_opy_, "bar-style").text = event.l111ll1ll1_opy_
                            if event.l1llll11l111_opy_:
                                l1l1llllll11_opy_ = l1lll1l11ll_opy_.SubElement(l11l1l11ll_opy_, "ending")
                                if event.l1lllll1111l_opy_ != "no":
                                    l1l1llllll11_opy_.attrib = {"number": event.l1lllll1111l_opy_}
                                if event.l1llll111l11_opy_ != "no":
                                    l1l1llllll11_opy_.attrib.update({"type": event.l1llll111l11_opy_})
                            if event.l1lllll1ll1_opy_ != "no":
                                l1llll1111l_opy_ = l1lll1l11ll_opy_.SubElement(l11l1l11ll_opy_, "repeat")
                                l1llll1111l_opy_.attrib = {"direction": event.l1lllll1ll1_opy_}
                        elif event.t == "print":
                            l1lllll1lll_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "print")
                            if event.l1111ll111_opy_ != "no":
                                l1lllll1lll_opy_.attrib = {"new-system":event.l1111ll111_opy_}
                        elif event.t == "sound":
                            print("model to xml sound")
                            l11l1lll1l_opy_ = l1lll1l11ll_opy_.SubElement(l1l111ll11_opy_, "sound")
                            if event.l1l11ll1l1_opy_ != "no":
                                l11l1lll1l_opy_.attrib = {"tempo":event.l1l11ll1l1_opy_}
                            if event.l11ll11l1l_opy_ != "no":
                                l11l1lll1l_opy_.attrib = {"tempo":event.l11ll11l1l_opy_}
            elif element.t == "part-list":
                l1llllll111_opy_ = l1lll1l11ll_opy_.SubElement(root, "part-list")
                for l1l11lllll_opy_ in element.l111l1l1l1_opy_:
                    l1l11llll1_opy_ = l1lll1l11ll_opy_.SubElement(l1llllll111_opy_, "score-part")
                    if l1l11lllll_opy_.l1lll1l11l1_opy_ != "no":
                        l1l11llll1_opy_.attrib = {"id":l1l11lllll_opy_.l1lll1l11l1_opy_}
                    if l1l11lllll_opy_.l111l111l1_opy_ != "no":
                        l1lll1ll11l_opy_ = l1lll1l11ll_opy_.SubElement(l1l11llll1_opy_, "part-name").text = l1l11lllll_opy_.l111l111l1_opy_
                    if l1l11lllll_opy_.l11l111111_opy_ != "no":
                        l111llllll_opy_ = l1lll1l11ll_opy_.SubElement(l1l11llll1_opy_, "part-abbreviation").text = l1l11lllll_opy_.l11l111111_opy_
                    if l1l11lllll_opy_.l11l111ll1_opy_ != "no":
                        l1l11l1ll1_opy_ = l1lll1l11ll_opy_.SubElement(l1l11llll1_opy_, "score-instrument")
                        l1l11l1ll1_opy_.attrib = {"id":l1l11lllll_opy_.l11l111ll1_opy_}
                    if l1l11lllll_opy_.l1l11ll1ll_opy_ != "no":
                        l1l1l11111_opy_ = l1lll1l11ll_opy_.SubElement(l1l11l1ll1_opy_, "instrument-name").text = l1l11lllll_opy_.l1l11ll1ll_opy_
                    if l1l11lllll_opy_.l1l111l111_opy_ != "no" or l1l11lllll_opy_.l1l11111l1_opy_ != "no":
                        l1l1l1l1ll_opy_ = l1lll1l11ll_opy_.SubElement(l1l11llll1_opy_, "midi-device")
                        l1l1l1l1ll_opy_.attrib = {"id":l1l11lllll_opy_.l1l111l111_opy_, "port":l1l11lllll_opy_.l1l11111l1_opy_}
                    if l1l11lllll_opy_.l1l111l1ll_opy_ != "no":
                        l11111ll11_opy_ = l1lll1l11ll_opy_.SubElement(l1l11llll1_opy_, "midi-instrument")
                        l11111ll11_opy_.attrib = {"id":l1l11lllll_opy_.l1l111l1ll_opy_}
                    if l1l11lllll_opy_.l11lll1ll1_opy_ != "no":
                        l1l1l11l1l_opy_ = l1lll1l11ll_opy_.SubElement(l11111ll11_opy_, "midi-channel").text = l1l11lllll_opy_.l11lll1ll1_opy_
                    if l1l11lllll_opy_.l11l11llll_opy_ != "no":
                        l1lll1ll111_opy_ = l1lll1l11ll_opy_.SubElement(l11111ll11_opy_, "midi-program").text = l1l11lllll_opy_.l11l11llll_opy_
                    if l1l11lllll_opy_.l1llll1l1ll_opy_ != "no":
                        l111ll111l_opy_ = l1lll1l11ll_opy_.SubElement(l11111ll11_opy_, "volume").text = l1l11lllll_opy_.l1llll1l1ll_opy_
                    if l1l11lllll_opy_.l11ll11lll_opy_ != "no":
                        l11111l11l_opy_ = l1lll1l11ll_opy_.SubElement(l11111ll11_opy_, "pan").text = l1l11lllll_opy_.l11ll11lll_opy_
            elif element.t == "credit":
                l1llll1ll11_opy_ = l1lll1l11ll_opy_.SubElement(root, "credit")
                l1llll1ll11_opy_.attrib = {"page":"1"}
                if element.l11lll11ll_opy_ !="no":
                    l11ll1llll_opy_ = l1lll1l11ll_opy_.SubElement(l1llll1ll11_opy_, "credit-type").text = element.l11lll11ll_opy_
                l1l111l1l1_opy_ = l1lll1l11ll_opy_.SubElement(l1llll1ll11_opy_, "credit-words").text = element.l1l11lll11_opy_
            elif element.t == "work":
                if not l1l1llllll1l_opy_ and not l1ll11111111_opy_:
                    l1ll1111111l_opy_ = l1lll1l11ll_opy_.SubElement(root, "work")
                if element.l1llll1l1l1l_opy_ !="no":
                    l1l1llllll1l_opy_ = True
                    l1llll1l1l1l_opy_ = element.l1llll1l1l1l_opy_
                if element.l1lllll1lll1_opy_ !="no":
                    l1ll11111111_opy_ = True
                    l1lllll1lll1_opy_ = element.l1lllll1lll1_opy_
        if l1l1llllll1l_opy_:
            l1l1llllllll_opy_ = l1lll1l11ll_opy_.SubElement(l1ll1111111l_opy_, "work-number").text = l1llll1l1l1l_opy_
        if l1ll11111111_opy_:
            l1l1lllllll1_opy_ = l1lll1l11ll_opy_.SubElement(l1ll1111111l_opy_, "work-title").text = l1lllll1lll1_opy_
        l11lll1lll_opy_ = minidom.parseString(l1lll1l11ll_opy_.tostring(root)).toprettyxml(indent="   ", encoding="UTF-8", standalone="")
        if l1lll1l1lll_opy_:
            self._1l111lll_opy_(str(l11lll1lll_opy_))
        self._1l11l11l_opy_ (l11lll1lll_opy_)
        l1111ll1ll_opy_ = time.time()
        print("temps model to xml", l1111ll1ll_opy_-t1)