"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import os
import threading
from .l1111llll1l_opy_ import l1111lll11l_opy_
from .l1lllllll1ll_opy_ import l1llllll1l11_opy_
from .l1lllllll1l1_opy_ import l1llllll1l1l_opy_


class BadExtensionFile(Exception):
    pass


class MusicWriteFile(threading.Thread):
    l11111llll_opy_ = 0
    l111111lll_opy_ = 1
    l111111l11_opy_ = 2

    def __init__(
        self,
        lou,
        settings,
        l11111l1ll_opy_,
        l1ll1111l1_opy_,
        l1111ll1l1l_opy_,
        l1llllllll1l_opy_,
        function,
        extension=None,
    ):
        threading.Thread.__init__(self)
        self._1lllllll11l_opy_ = lou
        self._1llllll1ll1_opy_ = settings
        self._11111ll11_opy_ = l11111l1ll_opy_
        self._1l1l1l1l_opy_ = l1ll1111l1_opy_
        self._1llllllll11_opy_ = l1111ll1l1l_opy_
        self._1lllllll111_opy_ = l1llllllll1l_opy_
        self._1llllll1lll_opy_ = function
        self.extension = extension
        self.state = MusicWriteFile.l11111llll_opy_
        self.error = None

    def run(self):
        self.state = MusicWriteFile.l111111lll_opy_
        file_name, l1111111ll_opy_ = os.path.splitext(self._11111ll11_opy_)
        if l1111111ll_opy_:
            l1111111ll_opy_ = l1111111ll_opy_.lower()
        try:
            if l1111111ll_opy_ == ".bxml":
                l1lllllllll1_opy_ = l1111lll11l_opy_(
                    self._1lllllll11l_opy_,
                    self._11111ll11_opy_,
                    self._1l1l1l1l_opy_,
                    self._1llllll1ll1_opy_,
                )
                self.error = l1lllllllll1_opy_.l1111ll1lll_opy_(self._1llllllll11_opy_)
            elif l1111111ll_opy_ == ".musicxml":
                l1lllllllll1_opy_ = l1llllll1l11_opy_(
                    self._1lllllll11l_opy_,
                    self._11111ll11_opy_,
                    self._1l1l1l1l_opy_,
                    self._1llllll1ll1_opy_,
                )
                self.error = l1lllllllll1_opy_.l1111ll1lll_opy_(self._1llllllll11_opy_)
            elif l1111111ll_opy_ == ".midi" or l1111111ll_opy_ == ".mid":
                l1lllllllll1_opy_ = l1llllll1l1l_opy_(
                    self._1lllllll11l_opy_,
                    self._11111ll11_opy_,
                    self._1l1l1l1l_opy_,
                    self._1llllll1ll1_opy_,
                    self.extension,
                )
                self.error = l1lllllllll1_opy_.l1111ll1lll_opy_(self._1llllllll11_opy_)
            else:
                raise BadExtensionFile(
                    _("file {} type not supported.").format(self._11111ll11_opy_)
                )
        except IOError as error:
            self.error = error
            log.error("Write file IO exception:{}".format(self.error))
        self.state = MusicWriteFile.l111111l11_opy_
        if self._1lllllll111_opy_ is not None:
            self._1lllllll111_opy_(self.error, self._1llllll1lll_opy_)
