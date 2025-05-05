"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import codecs
import os
import threading
import xml.sax
from .l11111l1l1_opy_ import l111111111_opy_
from .l1lllllllll_opy_ import l11111ll1l_opy_
from zipfile import BadZipFile


class BadExtensionFile(Exception):
    pass


class MusicReadFile(threading.Thread):
    l11111llll_opy_ = 0
    l111111lll_opy_ = 1
    l111111l11_opy_ = 2

    def __init__(
        self,
        lou,
        l11111l1ll_opy_,
        language,
        l111111l1l_opy_,
        l11111l111_opy_,
        l11111l11l_opy_,
    ):
        threading.Thread.__init__(self)
        self.language = language
        self.lou = lou
        self.l111111l1l_opy_ = l111111l1l_opy_
        self._11111ll11_opy_ = l11111l1ll_opy_
        self.l11111l111_opy_ = l11111l111_opy_
        self.l11111l11l_opy_ = l11111l11l_opy_
        self.state = self.l11111llll_opy_
        self.l11111lll1_opy_ = None
        self.error = None

    def l1l1l111_opy_(self, line):
        self.l11111l111_opy_(line)

    def run(self):
        self.state = self.l111111lll_opy_
        file_name, l1111111ll_opy_ = os.path.splitext(self._11111ll11_opy_)
        if l1111111ll_opy_:
            l1111111ll_opy_ = l1111111ll_opy_.lower()
        l1ll1111l1_opy_ = None
        try:
            if l1111111ll_opy_ == ".bxml":
                encodings = ["utf-8", "latin-1"]
                e = None
                for e in encodings:
                    try:
                        l11111111l_opy_ = codecs.open(
                            self._11111ll11_opy_, "r", encoding=e
                        )
                        l11111111l_opy_.readlines()
                        l11111111l_opy_.seek(0)
                    except UnicodeDecodeError:
                        # log.warning('got unicode error with %s , trying different encoding' % e)
                        pass
                    else:
                        # log.warning('opening the file with encoding:  %s ' % e)
                        break
                self.l11111lll1_opy_ = self._11111ll11_opy_
                l111111ll1_opy_ = l111111111_opy_(
                    self.lou, self._11111ll11_opy_, self.l111111l1l_opy_
                )
                l1ll1111l1_opy_ = l111111ll1_opy_.l1111111l1_opy_(
                    self.l1l1l111_opy_, encoding=e
                )
            elif l1111111ll_opy_ == ".musicxml":
                encodings = ["utf-8", "latin-1"]
                e = None
                for e in encodings:
                    try:
                        l11111111l_opy_ = codecs.open(
                            self._11111ll11_opy_, "r", encoding=e
                        )
                        l11111111l_opy_.readlines()
                        l11111111l_opy_.seek(0)
                    except UnicodeDecodeError:
                        pass
                        # log.warning('got unicode error with %s , trying different encoding' % e)
                    else:
                        # log.warning('opening the file with encoding:  %s ' % e)
                        break
                self.l11111lll1_opy_ = self._11111ll11_opy_
                l1lllllllll_opy_ = l11111ll1l_opy_(
                    self.lou, self._11111ll11_opy_, self.l111111l1l_opy_
                )
                l1ll1111l1_opy_ = l1lllllllll_opy_.l1111111l1_opy_(
                    self.l1l1l111_opy_, encoding=e
                )
            else:
                raise BadExtensionFile(
                    _("file {} type not supported.").format(self._11111ll11_opy_)
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
            self.l11111l11l_opy_(
                self.error, self.l11111lll1_opy_, None, l1ll1111l1_opy_
            )
            self.state = self.l111111l11_opy_
            # log.info("End reading file")
