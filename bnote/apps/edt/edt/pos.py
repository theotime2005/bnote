"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


# -----------------------------------------------
# Position definition
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def new(pos):
        return Pos(pos.x, pos.y)

    # For print()
    def __repr__(self):
        return "[x:{}, y:{}]".format(self.x, self.y)

    # eq comparison
    def __eq__(self, other):
        if not isinstance(other, Pos):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y

    # not equal comparison
    def __ne__(self, other):
        return not self.__eq__(other)

    # (<) lower than comparison
    def __lt__(self, other):
        if not isinstance(other, Pos):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.y < other.y:
            return True
        elif self.y == other.y and self.x < other.x:
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
        if not isinstance(other, Pos):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.y > other.y:
            return True
        elif self.y == other.y and self.x > other.x:
            return True
        return False

    # (>=) greater or equal comparison
    def __ge__(self, other):
        if self == other:
            return True
        else:
            return self > other
