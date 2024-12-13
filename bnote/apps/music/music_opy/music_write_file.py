"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import os
import threading
from .l1ll1ll1l_opy_ import l1ll11lll_opy_
from .l1ll1111l_opy_ import l1ll11l11_opy_
from .l1lll111l_opy_ import l1ll1lll1_opy_


class BadExtensionFile(Exception):
    pass


class MusicWriteFile(threading.Thread):
    l1ll1l1l1_opy_ = 0
    l1l1lllll_opy_ = 1
    l1ll11111_opy_ = 2

    def __init__(
        self,
        lou,
        settings,
        l1l1lll1l_opy_,
        l1ll1l1ll_opy_,
        l1ll1ll11_opy_,
        l1l1llll1_opy_,
        function,
        extension=None,
    ):
        threading.Thread.__init__(self)
        self._1ll111ll_opy_ = lou
        self._1l1lll11_opy_ = settings
        self._1ll1llll_opy_ = l1l1lll1l_opy_
        self._1ll1l11l_opy_ = l1ll1l1ll_opy_
        self._1ll111l1_opy_ = l1ll1ll11_opy_
        self._1ll11ll1_opy_ = l1l1llll1_opy_
        self._1ll1l111_opy_ = function
        self.extension = extension
        self.state = MusicWriteFile.l1ll1l1l1_opy_
        self.error = None

    def run(self):
        self.state = MusicWriteFile.l1l1lllll_opy_
        l1l1ll1ll_opy_, l1l1ll1l1_opy_ = os.path.splitext(self._1ll1llll_opy_)
        if l1l1ll1l1_opy_:
            l1l1ll1l1_opy_ = l1l1ll1l1_opy_.lower()
        try:
            if l1l1ll1l1_opy_ == ".bxml":
                l1lll1111_opy_ = l1ll11lll_opy_(
                    self._1ll111ll_opy_,
                    self._1ll1llll_opy_,
                    self._1ll1l11l_opy_,
                    self._1l1lll11_opy_,
                )
                self.error = l1lll1111_opy_.l1ll11l1l_opy_(self._1ll111l1_opy_)
            elif l1l1ll1l1_opy_ == ".musicxml":
                l1lll1111_opy_ = l1ll11l11_opy_(
                    self._1ll111ll_opy_,
                    self._1ll1llll_opy_,
                    self._1ll1l11l_opy_,
                    self._1l1lll11_opy_,
                )
                self.error = l1lll1111_opy_.l1ll11l1l_opy_(self._1ll111l1_opy_)
            elif l1l1ll1l1_opy_ == ".midi" or l1l1ll1l1_opy_ == ".mid":
                l1lll1111_opy_ = l1ll1lll1_opy_(
                    self._1ll111ll_opy_,
                    self._1ll1llll_opy_,
                    self._1ll1l11l_opy_,
                    self._1l1lll11_opy_,
                    self.extension,
                )
                self.error = l1lll1111_opy_.l1ll11l1l_opy_(self._1ll111l1_opy_)
            else:
                raise BadExtensionFile(
                    _("file {} type not supported.").format(self._1ll1llll_opy_)
                )
        except IOError as error:
            self.error = error
            log.error("Write file IO exception:{}".format(self.error))
        self.state = MusicWriteFile.l1ll11111_opy_
        if self._1ll11ll1_opy_ is not None:
            self._1ll11ll1_opy_(self.error, self._1ll1l111_opy_)
