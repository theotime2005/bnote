"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


class Coordinates:
    """
    Coordinates definition
    A column, a line and a paragraph (0 based)
    """

    def __init__(self, column, line, paragraph):
        self.paragraph = paragraph
        self.line = line
        self.column = column

    # For print()
    def __str__(self):
        return "[col:{}, lin:{} par:{}]".format(self.column, self.line, self.paragraph)

    # eq comparison
    def __eq__(self, other):
        if not isinstance(other, Coordinates):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.paragraph == other.paragraph and self.line == other.line and self.column == other.column

    # not equal comparison
    def __ne__(self, other):
        return not self.__eq__(other)

    # (<) lower than comparison
    def __lt__(self, other):
        if not isinstance(other, Coordinates):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.paragraph < other.paragraph:
            return True
        elif self.paragraph == other.paragraph:
            if self.line < other.line:
                return True
            elif self.line == other.line and self.column < other.column:
                return True
        return False

    # (<=) lower or equal comparison
    def __le__(self, other):
        if self == other:
            return True
        else:
            return self < other

    # (>) greater than comparison
    def __gt__(self, other):
        if not isinstance(other, Coordinates):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.paragraph > other.paragraph:
            return True
        elif self.paragraph == other.paragraph:
            if self.line > other.line:
                return True
            elif self.line == other.line and self.column > other.column:
                return True
        return False

    # (>=) greater or equal comparison
    def __ge__(self, other):
        if self == other:
            return True
        else:
            return self > other
