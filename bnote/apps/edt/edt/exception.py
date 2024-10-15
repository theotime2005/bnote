

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


