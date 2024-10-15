"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import string
from .pos import Pos


# -----------------------------------------------
# Caret definition
class Caret:
    def __init__(self, caret=None):
        if caret:
            self.start = Pos(caret.start.x, caret.start.y)
            self.end = Pos(caret.end.x, caret.end.y)
            self.old_x = caret.old_x
        else:
            self.start = Pos(0, 0)
            self.end = Pos(0, 0)
            self.old_x = 0

    # For print()
    def __str__(self):
        return "Caret start[{}] end[{}]".format(self.start, self.end)

    # Check if a selection is done.
    def is_selection_empty(self):
        if self.start == self.end:
            return True
        else:
            return False

    # clear selection from the end of selection according to its direction.
    def clear_selection_from_end(self):
        self.start = Pos.new(self.end)

    # clear selection from the first coordinate.
    def clear_selection_from_first(self):
        self.start = self.first()
        self.end = Pos.new(self.start)

    # clear selection from the last coordinate.
    def clear_selection_from_last(self):
        self.start = self.last()
        self.end = Pos.new(self.start)

    # return the first caret pos
    def first(self):
        if self.start > self.end:
            return self.end
        else:
            return self.start

    # return the last caret pos
    def last(self):
        if self.start > self.end:
            return self.start
        else:
            return self.end

    def update_caret_after_moving_up_or_down(self, new_pos, is_selection):
        self.end = new_pos
        if not is_selection:
            # Start pos follow end pos if not in selection mode
            self.clear_selection_from_end()

    def update_caret_after_moving(self, new_pos, is_selection):
        self.update_caret_after_moving_up_or_down(new_pos, is_selection)
        self.old_x = self.end.x

    def xml_render(self):
        caret_template = string.Template('    <caret start_x="${sx}" start_y="${sy}" end_x="${ex}" end_y="${ey}" />')
        return [caret_template.substitute(sx=self.start.x, sy=self.start.y, ex=self.end.x, ey=self.end.y)]

