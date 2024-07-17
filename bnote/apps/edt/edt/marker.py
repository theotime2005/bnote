"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


class Marker:
    """ Marker class :
            A marker is composed with :
             - An index in the paragraph text
             - An index in the paragraphs list
    """

    def __init__(self, index, paragraph):
        self.paragraph = paragraph
        self.index = index

    # For print()
    def __str__(self):
        return "[Marker: index{} par{} ".format(self.index, self.paragraph)

    # eq comparison
    def __eq__(self, other):
        if not isinstance(other, Marker):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.paragraph == other.paragraph and self.index == other.index

    # not equal comparison
    def __ne__(self, other):
        return not self.__eq__(other)

    # (<) lower than comparison
    def __lt__(self, other):
        if not isinstance(other, Marker):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.paragraph < other.paragraph:
            return True
        elif self.paragraph == other.paragraph and self.index < other.index:
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
        if not isinstance(other, Marker):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.paragraph > other.paragraph:
            return True
        elif self.paragraph == other.paragraph and self.index > other.index:
            return True
        return False

    # (>=) greater or equal comparison
    def __ge__(self, other):
        if self == other:
            return True
        else:
            return self > other

