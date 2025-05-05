"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from typing import Dict, Optional


class AnchorElement:
    __slots__ = ["attrs", "count", "outcount"]

    def __init__(self, attrs: Dict[str, Optional[str]], count: int, outcount: int):
        self.attrs = attrs
        self.count = count
        self.outcount = outcount


class ListElement:
    __slots__ = ["name", "num"]

    def __init__(self, name: str, num: int):
        self.name = name
        self.num = num
