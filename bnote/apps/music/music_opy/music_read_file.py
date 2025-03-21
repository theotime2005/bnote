"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import codecs
import os
import threading
import xml.sax
from .l11ll1l11ll_opy_ import l11ll1l1l1l_opy_
from .l11l1l1l1ll_opy_ import l11l1l1l1l1_opy_
from zipfile import BadZipFile


class BadExtensionFile(Exception):
    pass


class MusicReadFile(threading.Thread):
    l1ll1l1l1_opy_ = 0
    l1l1lllll_opy_ = 1
    l1ll11111_opy_ = 2

    def __init__(
        self,
        lou,
        l1l1lll1l_opy_,
        l11l1l11l11_opy_,
        l1l111lll_opy_,
        l11l1l11l1l_opy_,
        l11l1l11ll1_opy_,
    ):
        threading.Thread.__init__(self)
        self.l11l1l11l11_opy_ = l11l1l11l11_opy_
        self.lou = lou
        self.l1l111lll_opy_ = l1l111lll_opy_
        self._1ll1llll_opy_ = l1l1lll1l_opy_
        self.l11l1l11l1l_opy_ = l11l1l11l1l_opy_
        self.l11l1l11ll1_opy_ = l11l1l11ll1_opy_
        self.state = self.l1ll1l1l1_opy_
        self.l11l1l111l1_opy_ = None
        self.error = None

    def l1l1llll1ll_opy_(self, line):
        self.l11l1l11l1l_opy_(line)

    def run(self):
        self.state = self.l1l1lllll_opy_
        l1l1ll1ll_opy_, l1l1ll1l1_opy_ = os.path.splitext(self._1ll1llll_opy_)
        if l1l1ll1l1_opy_:
            l1l1ll1l1_opy_ = l1l1ll1l1_opy_.lower()
        l1ll1l1ll_opy_ = None
        try:
            if l1l1ll1l1_opy_ == ".bxml":
                l11l1l1l111_opy_ = ["utf-8", "latin-1"]
                e = None
                for e in l11l1l1l111_opy_:
                    try:
                        l11l1l111ll_opy_ = codecs.open(
                            self._1ll1llll_opy_, "r", encoding=e
                        )
                        l11l1l111ll_opy_.readlines()
                        l11l1l111ll_opy_.seek(0)
                    except UnicodeDecodeError:
                        # log.warning('got unicode error with %s , trying different encoding' % e)
                        pass
                    else:
                        # log.warning('opening the file with encoding:  %s ' % e)
                        break
                self.l11l1l111l1_opy_ = self._1ll1llll_opy_
                l11l1l11lll_opy_ = l11ll1l1l1l_opy_(
                    self.lou, self._1ll1llll_opy_, self.l1l111lll_opy_
                )
                l1ll1l1ll_opy_ = l11l1l11lll_opy_.l1ll1l11l1l_opy_(
                    self.l1l1llll1ll_opy_, encoding=e
                )
            elif l1l1ll1l1_opy_ == ".musicxml":
                l11l1l1l111_opy_ = ["utf-8", "latin-1"]
                e = None
                for e in l11l1l1l111_opy_:
                    try:
                        l11l1l111ll_opy_ = codecs.open(
                            self._1ll1llll_opy_, "r", encoding=e
                        )
                        l11l1l111ll_opy_.readlines()
                        l11l1l111ll_opy_.seek(0)
                    except UnicodeDecodeError:
                        pass
                        # log.warning('got unicode error with %s , trying different encoding' % e)
                    else:
                        # log.warning('opening the file with encoding:  %s ' % e)
                        break
                self.l11l1l111l1_opy_ = self._1ll1llll_opy_
                l11l1l1l1ll_opy_ = l11l1l1l1l1_opy_(
                    self.lou, self._1ll1llll_opy_, self.l1l111lll_opy_
                )
                l1ll1l1ll_opy_ = l11l1l1l1ll_opy_.l1ll1l11l1l_opy_(
                    self.l1l1llll1ll_opy_, encoding=e
                )
            else:
                raise BadExtensionFile(
                    _("file {} type not supported.").format(self._1ll1llll_opy_)
                )
        except AttributeError as error:
            self.error = error
        except ValueError as error:
            self.error = error
        except IOError as error:
            self.error = error
        except BadExtensionFile as error:
            self.error = error
        except BadZipFile as error:
            self.error = error
        except xml.sax.SAXException as error:
            self.error = error
        finally:
            self.l11l1l11ll1_opy_(
                self.error, self.l11l1l111l1_opy_, None, l1ll1l1ll_opy_
            )
            self.state = self.l1ll11111_opy_
            # log.info("End reading file")
