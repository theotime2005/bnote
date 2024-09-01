"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


class BadExtensionFile(Exception):
    pass


class BadNewFileName(Exception):
    pass


class BadSheet(Exception):
    pass


class SelectSheet(Exception):
    def __init__(self, message, sheet_list):
        self.sheet_list = sheet_list
        self.message = message
        super().__init__(self.message)
