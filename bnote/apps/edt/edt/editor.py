"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

# -----------------------------------------------
# Editor file
# This file gathering all functions to navigate and modify a text

# clipboard
from bnote.tools.settings import Settings
from .undo_redo import UndoRedo
from bnote.tools.clipboard import copy, paste

from .color import Formatting
from enum import Enum
from .caret import Caret
from .markers import Markers
from .paragraphs import Paragraphs
from .pos import Pos
from enum import Enum

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_LOG, logging

log = ColoredLogger(__name__, level=EDITOR_LOG)

# Arbitrary lines number definition for page up/down and ctrl page up/down.
STEP_FOR_CTRL_PAGE = 50
STEP_FOR_PAGE = 20


class EditorIterator:
    def __init__(self, editor):
        # Team object reference
        self._editor = editor
        # member variable to keep track of current index
        self._index = 0
        # Compute caret position as paragraph index and index in paragraph
        self._start_pos, self._end_pos = self._editor.caret_as_paragraph_position()
        # print(self._start_pos, self._end_pos)

    def __next__(self):
        """
        Get the next paragraph
        -> Paragraph
           int index of start selection
           int index of end selection
        """
        if self._index < self._editor.paragraphs_count():
            paragraph = self._editor.paragraph(self._index)
            start = None
            end = None
            if self._index == self._start_pos.x:
                start = self._start_pos.y
                if self._index == self._end_pos.x:
                    end = self._end_pos.y
                else:
                    end = len(paragraph.paragraph_text())
            elif self._index == self._end_pos.x:
                end = self._end_pos.y
                start = 0
            # index to next line
            self._index += 1
            return paragraph, start, end
        # End of Iteration
        raise StopIteration


class Editor:
    # Subclass >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    class Functions(Enum):
        # Function without argument.
        MOVE_UP = object()
        MOVE_DOWN = object()
        MOVE_RIGHT = object()
        MOVE_LEFT = object()
        MOVE_HOME = object()
        MOVE_END = object()

        PAGE_UP = object()
        PAGE_DOWN = object()

        PUT_CARET = object()

        SELECT_ALL = object()
        SELECT_WORD = object()

        SELECTION_MODE_TOGGLE = object()
        SELECTION_MODE_ON = object()
        SELECTION_MODE_OFF = object()
        BACKSPACE = object()
        SPACE = object()
        DELETE = object()
        COPY = object()
        CUT = object()
        PASTE = object()
        CARRIAGE_RETURN = object()
        TAB = object()
        MARKER = object()
        UNDO = object()
        REDO = object()

        # Functions with one argument.
        PUT_STRING = object()
        PUT_STRING_BETWEEN_SPACES = object()

        # Function find and replace
        FIND = object()
        REPLACE_AND_FIND = object()
        REPLACE_ALL = object()

        # Debug functions
        PRINT_LINE = object()
        KILL_THREAD = object()

        # Additional functions not treated by editor
        WRITE_FILE = object()

    # Subclass <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Switcher >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def function(self, function, **kwarg):
        """
        The entry point in editor for all functions
        **arg = **{shift=True/False Ctrl=True/False}
        """
        # Get the function from switcher dictionary
        func = self.__switcher.get(function, None)
        # Execute the function
        if func is not None:
            if (
                function != Editor.Functions.REPLACE_AND_FIND
                and function != Editor.Functions.REPLACE_ALL
            ):
                # Reset selection_by_find indicator for all editor function except replace function.
                self._is_selection_by_find = False
            if EDITOR_LOG <= logging.INFO:
                log.info(f"key: {function=} Function{func}")
            return func(**kwarg)
        else:
            if EDITOR_LOG <= logging.WARNING:
                log.warning("Unknown function <{}> ???".format(function))
            return False

    # Switcher <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Constructor
    def __init__(self, width, lines, is_read_only=False):
        # One list of lines with a predefined width as integer
        if isinstance(width, bytes):
            i_width = int.from_bytes(width, "big")
        else:
            i_width = width
        self._paragraphs = Paragraphs(i_width, lines)
        # One caret
        self._caret = Caret()
        # Markers
        self._markers = Markers()
        # Selection mode
        self._is_selection = False
        # Selection by find
        # This flag is set when a selection is defined by find_next or find_previous function.
        # This flag is reset by all editor's function except find and replace function.
        self._is_selection_by_find = False
        # Undo-redo queue of editor operations.
        self.undo_redo = UndoRedo()
        # Read only flag
        self.read_only = is_read_only
        # caret change flag (for graphical refresh)
        self._is_caret_change = False
        # Function switcher.
        self.__switcher = {
            # Caret movement
            Editor.Functions.MOVE_UP: self._move_up,
            Editor.Functions.MOVE_DOWN: self._move_down,
            Editor.Functions.MOVE_RIGHT: self._move_right,
            Editor.Functions.MOVE_LEFT: self._move_left,
            Editor.Functions.MOVE_HOME: self._move_home,
            Editor.Functions.MOVE_END: self._move_end,
            Editor.Functions.PAGE_UP: self._page_up,
            Editor.Functions.PAGE_DOWN: self._page_down,
            Editor.Functions.PUT_CARET: self._put_caret,
            # Selection
            Editor.Functions.SELECT_ALL: self._select_all,
            Editor.Functions.SELECT_WORD: self._select_word,
            # Editor parameters
            Editor.Functions.SELECTION_MODE_TOGGLE: self._toggle_selection_mode,
            Editor.Functions.SELECTION_MODE_ON: self._selection_mode_on,
            Editor.Functions.SELECTION_MODE_OFF: self._selection_mode_off,
            # Marker functions
            Editor.Functions.MARKER: self._marker,
            # Find and replace
            Editor.Functions.FIND: self._find,
            Editor.Functions.REPLACE_AND_FIND: self._replace_and_find,
            Editor.Functions.REPLACE_ALL: self._replace_all,
            # Editing functions
            Editor.Functions.BACKSPACE: self._backspace,
            Editor.Functions.SPACE: self._space,
            Editor.Functions.DELETE: self._delete,
            Editor.Functions.COPY: self._copy,
            Editor.Functions.CUT: self._cut,
            Editor.Functions.PASTE: self._paste,
            Editor.Functions.CARRIAGE_RETURN: self._carriage_return,
            Editor.Functions.TAB: self._tab,
            Editor.Functions.PUT_STRING: self._put_string,
            Editor.Functions.PUT_STRING_BETWEEN_SPACES: self._put_string_between_spaces,
            Editor.Functions.UNDO: self._undo,
            Editor.Functions.REDO: self._redo,
            # Debug functions
            Editor.Functions.PRINT_LINE: self.print_line,
        }

    # Returns the Iterator object
    def __iter__(self):
        return EditorIterator(self)

    def paragraph(self, index):
        """
        Get paragraph at paragraph index.
        index: int paragraph index
        -> Paragraph
        """
        return self._paragraphs.paragraph(index)

    def set_is_modified(self, value):
        """
        Clear or Set is_modified flag for document.
        """
        self._paragraphs.is_modified = value

    def set_is_caret_change(self):
        """
        set caret change state.
        """
        self._is_caret_change = True

    def is_caret_change_and_clear(self):
        """
        Return caret change state and clear the flag.
        -> bool
        """
        value = self._is_caret_change
        self._is_caret_change = False
        return value

    def is_modified(self):
        """
        Return document state.
        -> bool
        """
        return self._paragraphs.is_modified

    def clean_up(self):
        """
        Remote consecutive blank line, keep only one.
        -> bool True if at least a remove as been done.
        """
        if self.read_only:
            return False
        index = 0
        res = False
        is_previous_line_empty = False
        while index < self._paragraphs.paragraphs_count():
            paragraph = self._paragraphs.paragraph(index)
            if not paragraph.paragraph_text().strip():
                if is_previous_line_empty:
                    # Remove the line
                    self._paragraphs.delete_paragraph(index, self._markers)
                    res = True
                    # Next paragraph as now the same index
                else:
                    # Current line is empty.
                    is_previous_line_empty = True
                    # Next paragraph
                    index += 1
            else:
                # Current line is not empty.
                is_previous_line_empty = False
                # Next paragraph
                index += 1
        if res:
            # Document is modified
            self.set_is_modified(True)
        # Put caret at the beginning of document.
        self._move_start_of_document(False)
        self.set_is_caret_change()
        return res

    # For print()
    def __repr__(self):
        text = "Document"
        # Display all lines.
        text += self._paragraphs.__str__()
        text += self._caret.__str__()
        return text

    def resize_line_length(self, line_length):
        """
        Reformat all document according to the new line length.
        """
        if not self._caret.is_selection_empty():
            # If a selection is done, we forget it.
            self._caret.clear_selection_from_end()
        new_pos = self._paragraphs.resize_line_length(self._caret.end, line_length)
        self._caret.update_caret_after_moving_up_or_down(new_pos, False)
        self.set_is_caret_change()

    def caret_as_paragraph_position(self) -> (Pos, Pos):
        """
        Get the caret as 2 Pos(paragraph index in document, character index in paragraph)
        -> Pos(paragraph index in document, character index in paragraph) of start caret (the first)
           Pos(paragraph index in document, character index in paragraph) of end caret (the last)
        """
        end_pos = self._paragraphs.paragraph_and_character_index(self._caret.last())
        if self._caret.is_selection_empty():
            start_pos = end_pos
        else:
            start_pos = self._paragraphs.paragraph_and_character_index(
                self._caret.first()
            )
        return start_pos, end_pos

    def editor_braille_line(self, line_index=None) -> (str, bytes):
        if line_index is None:
            line_index = self._caret.end.y
        line = self._paragraphs.line(line_index)
        line_length = len(line)
        dots = bytearray(line_length)
        last_x = 0
        # Add caret or selection.
        if self._caret.is_selection_empty():
            # No selection
            if line_index == self._caret.end.y:
                if Settings().data["editor"]["cursor_visible"]:
                    dots[self._caret.end.x : self._caret.end.x + 1] = b"\xC0"
                else:
                    dots[self._caret.end.x : self._caret.end.x + 1] = b"\x00"
                last_x = self._caret.end.x + 1
        else:
            # selection active
            if line_index == self._caret.first().y:
                if self._caret.start.y == self._caret.end.y:
                    # selection in a part of the line
                    first_x = self._caret.first().x
                    last_x = self._caret.last().x + 1
                else:
                    # selection on the end of line
                    first_x = self._caret.first().x
                    last_x = line_length

            elif (self._caret.first().y < line_index) and (
                line_index < self._caret.last().y
            ):
                first_x = 0
                last_x = line_length

            elif line_index == self._caret.last().y:
                if self._caret.start.y == self._caret.end.y:
                    # selection in a part of the line
                    first_x = self._caret.first().x
                    last_x = self._caret.last().x + 1
                else:
                    # selection on the start of line
                    first_x = 0
                    last_x = self._caret.last().x + 1

            else:
                # No selection for this line.
                first_x = last_x = 0

            # Set flashing dots on all caret cells.
            dots[first_x:last_x] = b"\xC0" * (last_x - first_x)
        # Add markers
        log.info(f"{line_index=}")
        coo = self._paragraphs.coo_from_pos(Pos(0, line_index))
        log.info("coo={}".format(str(coo)))
        # Calculate the index in the paragraph from Pos
        index = self._paragraphs.paragraph(coo.paragraph).index_from_coordinates(
            Pos(coo.column, coo.line)
        )
        log.info(f"paragraph={coo.paragraph} {index=}")
        markers = self._markers.markers_list(
            coo.paragraph, start_index=index, end_index=index + line_length
        )
        log.info(f"{markers=}")
        for marker in markers:
            dots[marker - index] = ord(b"\xFF")

        if last_x > line_length:
            # Add space at the end of the line for caret
            line += " "

        return line, dots

    def get_line(self) -> (str, int, int):
        line = self._paragraphs.line(self._caret.end.y)
        line_length = len(line)
        if self._caret.is_selection_empty():
            # No selection
            first_x = self._caret.end.x
            last_x = self._caret.end.x + 1
        else:
            # selection active
            if self._caret.start.y == self._caret.end.y:
                # selection in a part of the line
                first_x = self._caret.first().x
                last_x = self._caret.last().x + 1
            elif self._caret.first().y == self._caret.end.y:
                # selection on the end of line
                first_x = self._caret.first().x
                last_x = line_length
            else:
                # selection on the start of line
                first_x = 0
                last_x = self._caret.last().x
        if last_x > line_length:
            # Add space at the end of the line for caret
            line += " "
        return line, first_x, last_x

    def print_line(self):
        id, line, first_x, last_x = self.get_line()

        print(
            "Line[{}{}{}{}{}] {}".format(
                line[0:first_x],
                Formatting.Underlined,
                line[first_x:last_x],
                Formatting.Reset_Underlined,
                line[last_x : len(line)],
                self._caret,
            )
        )

    def paragraphs_count(self) -> int:
        """
        Get the number of paragraphs in the document.
        -> int
        """
        return self._paragraphs.paragraphs_count()

    def lines_count(self) -> int:
        """
        get the number of lines in the document.
        -> int
        """
        return self._paragraphs.lines_count()

    def last_paragraph_lines_count(self) -> int:
        """
        get the number of lines in the last paragraph.
        -> int
        """
        return self._paragraphs.last_paragraph_lines_count()

    def caret(self) -> Caret:
        """
        get document caret
        (Editor resources access for write file)
        """
        return self._caret

    def set_caret(self, caret):
        """
        set the caret of document.
        (check validity)
        """
        # Verify caret position.
        self._caret.start = self._paragraphs.check_pos(caret.start)
        self._caret.end = self._paragraphs.check_pos(caret.end)
        self.set_is_caret_change()

    def set_caret_on_paragraph(self, index):
        """
        put the caret  at the start of a paragraph
        index: int paragraph index (0 based)
        -> no return
        """
        line_index = self._paragraphs.lines_count(paragraph_index=index)
        self._caret.start = Pos(0, line_index)
        self._caret.end = Pos(0, line_index)
        self.set_is_caret_change()

    def markers(self) -> Markers:
        """
        get Document's markers
        """
        return self._markers

    def set_markers(self, markers):
        """
        set document's Markers
        markers : Markers
        """
        self._markers = markers

    def paragraph_text(self, index):
        """
        get the paragraph text.
        index: paragraph index in document
        -> str
        """
        return self._paragraphs.paragraph_text(index)

    def paragraph_pos(self, paragraph_index, offset):
        """
        compute coordinate from index of paragraph and an offset in paragraph
        -> pos (column, line in editor)
        """
        return self._paragraphs.paragraph_pos(paragraph_index, offset)

    def start_cursor_paragraph_index(self):
        """
        get first paragraph index of the selection.
        -> int (paragraph index in document)
        """
        return self._paragraphs.paragraph_index(self._caret.start)

    def end_cursor_paragraph_index(self):
        """
        get last paragraph index of the selection.
        -> int (paragraph index in document)
        """
        return self._paragraphs.paragraph_index(self._caret.end)

    def current_paragraph_index(self):
        """
        get first paragraph index of the selection.
        -> int (paragraph index in document)
        """
        return self._paragraphs.paragraph_index(self._caret.start)

    def current_paragraph_and_line_index(self):
        """
        get paragraph index in document and index of line in paragraph at caret.end.
        -> Pos(paragraph index and index of line in paragraph)
        """
        return self._paragraphs.paragraph_and_line_index(self._caret.end)

    def offset_in_paragraph(self, pos: Pos):
        """
        get offset in paragraph for a given Pos(line, column)
        Returns: Pos pos.x=line_index, pos.y=character_index_in_paragraph
        """
        end_pos = self._paragraphs.paragraph_and_character_index(pos)
        return end_pos

    def append_paragraph(self, paragraph):
        """
        add a paragraph at the end of editor.
        line:str (the paragraph content)
        """
        self._paragraphs.append(paragraph)

    def statistics(self):
        """
        get document information.
        -> (paragraphs count, words count, characters count)
        """
        return self._paragraphs.statistics()

    def _move_up(self, **kwargs):
        """
        move caret up with trying to keep x caret position.
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move up with control.
                return self._move_previous_paragraph(shift)
        # move up without control.
        return self._move_previous_line(shift)

    def _move_down(self, **kwargs):
        """
        move caret down with trying to keep x caret position.
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        # start_time = time.time()
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move down with control.
                return self._move_next_paragraph(shift)
        # move down without control.
        next_line = self._move_next_line(shift)
        # log.critical("--- move down in %s seconds ---" % (time.time() - start_time))
        return next_line

    def _move_right(self, **kwargs):
        """
        move caret to right, line change if necessary.
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move right with control.
                return self._move_next_word(shift)
        # move right without control.
        return self._move_next_char(shift)

    def _move_left(self, **kwargs):
        """
        move caret to left, line change if necessary
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move left with control.
                return self._move_previous_word(shift)
        # move left without control.
        return self._move_previous_char(shift)

    def _move_home(self, **kwargs):
        """
        move caret to home of document
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move home with control.
                return self._move_start_of_document(shift)
        # move home without control.
        return self._move_start_of_line(shift)

    def _move_end(self, **kwargs):
        """
        move caret to end of document
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # move end with control.
                return self._move_end_of_document(shift)
        # move end without control.
        return self._move_end_of_line(shift)

    @staticmethod
    def __page_jump(**kwargs):
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # page with control.
                return STEP_FOR_CTRL_PAGE
        return STEP_FOR_PAGE

    def _page_up(self, **kwargs):
        """
        move caret to page up
        the move is STEP_FOR_PAGE or STEP_FOR_CTRL_PAGE
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        jump = self.__page_jump(**kwargs)
        while jump != 0:
            if not self._move_previous_line(shift):
                break
            jump -= 1
        return True

    def _page_down(self, **kwargs):
        """
        move caret to page down
        the move is STEP_FOR_PAGE or STEP_FOR_CTRL_PAGE
        **kwargs: **{"shift":True/False, "ctrl":True/False}
        """
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        jump = self.__page_jump(**kwargs)
        while jump != 0:
            if not self._move_next_line(shift):
                break
            jump -= 1
        return True

    def _move_next_char(self, shift=None):
        """
        move caret to the next character.
        change of line or paragraph if necessary.
        """
        sel = shift or self._is_selection
        if not self._caret.is_selection_empty() and not sel:
            # Move right on selection, put cursor at the beginning of the selection.
            new_pos = self._caret.last()
        else:
            new_pos = self._paragraphs.move_right(self._caret.end)

        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_previous_char(self, shift=None):
        """
        move caret to the previous character.
        change of line or paragraph if necessary.
        """
        sel = shift or self._is_selection
        if not self._caret.is_selection_empty() and not sel:
            # Move right on selection, put cursor at the beginning of the selection.
            new_pos = self._caret.first()
        else:
            new_pos = self._paragraphs.move_left(self._caret.end)
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_previous_line(self, shift=None):
        """
        move caret to the previous line.
        x position is change of line or paragraph if necessary.
        """
        new_pos = self._paragraphs.move_up(self._caret.end, self._caret.old_x)
        if new_pos == self._caret.end:
            if EDITOR_LOG <= logging.WARNING:
                log.warning("Start of document reached !")
            return False
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving_up_or_down(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_next_line(self, shift=None):
        """
        move caret to the next line.
        x position is change of line or paragraph if necessary.
        """
        new_pos = self._paragraphs.move_down(self._caret.end, self._caret.old_x)
        if new_pos == self._caret.end:
            if EDITOR_LOG <= logging.WARNING:
                log.warning("End of document reached !")
            return False
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving_up_or_down(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_start_of_line(self, shift=None):
        """
        move caret to start of line.
        """
        sel = shift or self._is_selection
        if EDITOR_LOG <= logging.INFO:
            log.info("Move to start of line, selection<{}>".format(sel))
        self._caret.update_caret_after_moving(Pos(0, self._caret.end.y), sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_end_of_line(self, shift=None):
        """
        move caret to end of line.
        """
        new_pos = self._paragraphs.move_end_of_line(self._caret.end)
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_start_of_document(self, shift=None):
        """
        move caret to start of document.
        """
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(Pos(0, 0), sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_end_of_document(self, shift=None):
        """
        move caret to end of document.
        """
        new_pos = self._paragraphs.move_end_of_document(self._caret.end)
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_previous_paragraph(self, shift=None):
        """
        move caret to the previous paragraph.
        """
        new_pos = self._paragraphs.move_previous_paragraph(self._caret.end)
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_next_paragraph(self, shift=None):
        """
        move caret to the next paragraph.
        -> bool : False if no move
        """
        res = False
        new_pos = self._paragraphs.move_next_paragraph(self._caret.end)
        if new_pos != self._caret.end:
            # Not already on last paragraph
            # Set caret on new paragraph.
            sel = shift or self._is_selection
            self._caret.update_caret_after_moving(new_pos, sel)
            self.set_is_caret_change()
            res = True
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return res

    def _move_previous_word(self, shift=None):
        """
        move caret to the previous word.
        -> bool : always True
        """
        new_pos = self._paragraphs.move_previous_word(self._caret.end)
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _move_next_word(self, shift=None):
        """
        move caret to the next word.
        -> bool : always True
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("move_next_word")
        new_pos = self._paragraphs.move_next_word(self._caret.end)
        if EDITOR_LOG <= logging.INFO:
            log.info("old_pos<{}>, new_pos<{}>".format(self._caret.end, new_pos))
        sel = shift or self._is_selection
        self._caret.update_caret_after_moving(new_pos, sel)
        self.set_is_caret_change()
        if EDITOR_LOG <= logging.INFO:
            log.info("caret:{}".format(self._caret))
        return True

    def _put_caret(self, **kwargs) -> bool:
        """
        move caret to the position.
        **kwarg: **{ "pos"=Pos}
        -> bool False if failed
        """
        # kwarg decoding
        if "pos" in kwargs:
            pos = kwargs["pos"]
            if EDITOR_LOG <= logging.INFO:
                log.info("new caret {}".format(pos))
            coo = self._paragraphs.coo_from_pos(pos)
            if coo.paragraph == -1:
                return False

            # Check column
            line_length = len(self._paragraphs.line(pos.y))
            if line_length < pos.x:
                pos.x = line_length

            self._caret.update_caret_after_moving(pos, self._is_selection)
            self.set_is_caret_change()
            if EDITOR_LOG <= logging.INFO:
                log.info("caret:{}".format(self._caret))
            return True
        else:
            return False

    def _select_all(self, **kwargs):
        """
        select entire document.
        -> bool: always true
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("select all")
        self._move_start_of_document(False)
        self._move_end_of_document(True)
        return True

    def _select_word(self, **kwargs):
        """
        select the word at position.
        **kwargs: **{'pos'=Pos}
        """
        if "pos" in kwargs:
            pos = kwargs["pos"]
            if EDITOR_LOG <= logging.INFO:
                log.info("select word from pos {}".format(pos))
            start_pos, end_pos = self._paragraphs.select_word(pos)
            if start_pos:
                self._caret.start = start_pos
                self._caret.end = end_pos
                self._caret.old_x = end_pos.x
                self.set_is_caret_change()
                return True
            else:
                return False
        else:
            return False

    # Toggle selection mode and return the new mode.
    def _toggle_selection_mode(self, **kwargs) -> bool:
        """
        toogle selection mode (F8 and Esc keys)
        **kwargs= **{}
        -> bool: True if on
        """
        self._is_selection = not self._is_selection
        if self._is_selection:
            if EDITOR_LOG <= logging.WARNING:
                log.warning("start selection mode")
        else:
            if EDITOR_LOG <= logging.WARNING:
                log.warning("stop selection mode")
        return self._is_selection

    def _selection_mode_on(self, **kwargs):
        """
        set selection mode (F8 and Esc keys)
        **kwargs= **{}
        """
        self._is_selection = True
        return True

    def _selection_mode_off(self, **kwargs):
        """
        clear selection mode (F8 and Esc keys)
        **kwargs= **{}
        """
        self._is_selection = False
        return True

    def selection_mode(self) -> bool:
        """
        get selection mode (F8 and Esc keys)
        -> bool: True if on
        """
        return self._is_selection

    def _put_string_between_spaces(self, **kwargs) -> bool:
        """
        insert string and a space before and after the string.
        **kwargs= **{'text':str}
        -> bool if operation done successfully.
        """
        if EDITOR_LOG <= logging.DEBUG:
            log.debug("Insertion between space of <{}>".format(kwargs))
        if self.read_only:
            return False
        text = str()
        if "text" in kwargs:
            text = kwargs["text"]
        if text and len(text) > 0:
            new_str = text
            # Delete selection if necessary.
            self._delete_selection_with_undo()
            char_before, char_after = self._paragraphs.characters(self._caret.end)
            if EDITOR_LOG <= logging.INFO:
                log.info(
                    "character before is <{}>, after is <{}>".format(
                        char_before, char_after
                    )
                )
            if text[0] != " " and char_before is not None and char_before != " ":
                # Insert a space before insertion point.
                new_str = " " + new_str
            if (
                text[len(text) - 1] != " "
                and char_after is not None
                and char_after != " "
            ):
                # Insert a space after insertion point.
                new_str += " "
            return self.__put_string(new_str)
        else:
            return False

    def _undo(self, **kwargs):
        if self.read_only:
            return False
        op = self.undo_redo.get_and_decrement_operation()
        if EDITOR_LOG <= logging.INFO:
            log.info("undo operation: {}".format(op))
        if op:
            if op.is_deletion():
                if EDITOR_LOG <= logging.INFO:
                    log.info("Delete to do from {} to {}".format(op.start(), op.end()))
                self._caret.start = op.start()
                self._caret.end = op.end()
                return self._delete_selection_without_undo()
            elif op.is_insertion():
                if EDITOR_LOG <= logging.INFO:
                    log.info("Insert to do from {}".format(op.start()))
                self._caret.start = op.start()
                self._caret.end = self._caret.start
                text = op.text()
                if text is not None:
                    lines = text.split("\n")
                    return self._insert_strings_without_undo(lines)
        return False

    def _redo(self, **kwargs):
        if self.read_only:
            return False
        op = self.undo_redo.get_and_increment_operation()
        if EDITOR_LOG <= logging.INFO:
            log.info("redo operation: {}".format(op))
        if op:
            if op.is_deletion():
                if EDITOR_LOG <= logging.INFO:
                    log.info("Insert to do from {}".format(op.start()))
                self._caret.start = op.start()
                self._caret.end = self._caret.start
                text = op.text()
                if text is not None:
                    lines = text.split("\n")
                    return self._insert_strings_without_undo(lines)
            elif op.is_insertion():
                if EDITOR_LOG <= logging.INFO:
                    log.info("Delete to do from {} to {}".format(op.start(), op.end()))
                self._caret.start = op.start()
                self._caret.end = op.end()
                return self._delete_selection_without_undo()
        return False

    def _put_string(self, **kwargs):
        """
        insert a multi string (separate by \n) or a string or a char in document at caret position.
        **kwargs= **{'text':str}
        -> bool if operation done successfully.
        """
        text = str()
        if "text" in kwargs:
            text = kwargs["text"]
        return self.__put_string(text)

    def __put_string(self, text):
        if self.read_only:
            return False
        if text and len(text) > 0:
            text = text.replace("\r", "")
            lines = text.split("\n")
            # insertion carriage return or a line or some lines.
            return self._insert_strings_with_undo(lines)
        else:
            return False

    def _carriage_return(self, **kwargs):
        """
        insert a carriage retrun in document at caret position.
        generally, split a paragraph in two.
        **kwargs: **{}
        -> bool if operation done successfully.
        """
        return self.__put_string("\n")

    def _tab(self, **kwargs):
        """
        insert a tabulation at caret position.
        spaces_number = 8 - (self._caret.end.x % 8)
        **kwargs: **{}
        -> bool if operation done successfully.
        """
        return self.__put_string("\t")

    def _backspace(self, **kwargs):
        """
        do backspace in document at caret position.
        **kwargs: **{}
        -> bool if operation done successfully.
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("backspace with {}".format(kwargs))
        if not self._caret.is_selection_empty():
            return self._delete_selection_with_undo()
        else:
            # Traditional backspace (delete character at caret's left (merge line if necessary)
            new_pos = self._paragraphs.move_left(self._caret.end)
            if new_pos != self._caret.end:
                self._caret.update_caret_after_moving(new_pos, False)
                self.set_is_caret_change()
                if EDITOR_LOG <= logging.INFO:
                    log.info("delete a character")
                return self.__delete()

    def _space(self, **kwargs):
        """
        insert a space in document at caret position.
        **kwargs: **{}
        -> bool if operation done successfully.
        """
        return self.__put_string(" ")

    def _delete(self, **kwargs):
        """
        delete char or selection
        **kwargs: **{}
        """
        return self.__delete()

    def __delete(self):
        if self.read_only:
            return False
        # Reset selection mode anyway
        self._is_selection = False
        if not self._caret.is_selection_empty():
            return self._delete_selection_with_undo()
        else:
            # Delete a character.
            save_caret = Caret(self._caret)
            self._move_next_char(None)
            move_caret = Caret(self._caret)
            self._caret = save_caret
            deleted_char = self._paragraphs.selection(self._caret.end, move_caret.end)
            if EDITOR_LOG <= logging.INFO:
                log.info(
                    "add_char_insertion start={}, end={}, char={}".format(
                        self._caret.end, move_caret.end, deleted_char
                    )
                )
            self.undo_redo.add_char_insertion(
                start=self._caret.end, end=move_caret.end, text=deleted_char
            )
            # delete a char between 2 paragraph => merge the 2 paragraph
            new_pos = self._paragraphs.delete_char(self._caret.end, self._markers)
            self.set_is_caret_change()
            self._caret.update_caret_after_moving(new_pos, False)
            return True

    def _copy(self, **kwargs):
        """
        copy selection into clipboard
        **kwargs: **{}
        """
        return self.__copy()

    def selection(self):
        """
        Get text selected.
        Return: str
        """
        if not self._caret.is_selection_empty():
            # Selection is not empty => Copy it
            return self._paragraphs.selection(self._caret.first(), self._caret.last())

    def __copy(self):
        # Reset selection mode anyway
        self._is_selection = False
        if not self._caret.is_selection_empty():
            # Selection is not empty => Copy it
            copy(self._paragraphs.selection(self._caret.first(), self._caret.last()))
            return True
        else:
            return False

    # delete selection
    def _delete_selection_without_undo(self):
        return self._delete_selection(False)

    def _delete_selection_with_undo(self):
        return self._delete_selection(True)

    def _delete_selection(self, with_undo):
        if self.read_only:
            return False
        # Reset selection mode anyway
        self._is_selection = False
        if not self._caret.is_selection_empty():
            if with_undo:
                deleted_text = self._paragraphs.selection(
                    self._caret.first(), self._caret.last()
                )
                self.undo_redo.add_insertion(
                    start=self._caret.first(), end=self._caret.last(), text=deleted_text
                )
            # Selection is not empty => Delete it
            new_pos = self._paragraphs.delete_selection(
                self._caret.first(), self._caret.last(), self._markers
            )
            self._caret.update_caret_after_moving(new_pos, False)
            self.set_is_caret_change()
            return True
        else:
            return False

    def _paste(self, **kwargs):
        """
        paste clipboard at caret.
        **kwargs: **{}
        """
        if self.read_only:
            return False
        # If selection, delete it. (Reset selection mode anyway)
        self._delete_selection_with_undo()
        # Paste text from clipboard.
        text = paste()
        if text is not None:
            lines = text.split("\n")
            return self._insert_strings_with_undo(lines)
        return False

    def _cut(self, **kwargs):
        """
        copy selection into clipboard and delete it
        **kwargs: **{}
        -> bool: False if selection is empty.
        """
        if self.read_only:
            return False
        if not self._caret.is_selection_empty():
            # Selection is not empty => Copy and delete it.
            self.__copy()
            # If selection, delete it. (Reset selection mode anyway)
            return self._delete_selection_with_undo()
        else:
            return False

    def _insert_strings_without_undo(self, strings):
        """
        insert strings or char without undo
        strings: str with possible \n
        """
        return self._insert_strings(strings, False)

    def _insert_strings_with_undo(self, strings):
        """
        insert strings or char with undo
        strings: str with possible \n
        """
        return self._insert_strings(strings, True)

    def _insert_strings(self, strings, with_undo):
        """
        insert strings or char
        strings: str with possible \n
        with_undo: True/False
        -> bool: always True
        """
        if self.read_only:
            return False
        # Delete selection if necessary. (Reset selection mode anyway)
        self._delete_selection_with_undo()
        # Insert text strings.
        start_insert = self._caret.end
        new_pos = self._paragraphs.insert_strings(start_insert, self._markers, strings)
        # Handle undo.
        if with_undo:
            if (len(strings) == 1) and (len(strings[0]) == 1):
                self.undo_redo.add_char_deletion(
                    start=start_insert, end=new_pos, text=strings[0]
                )
            else:
                self.undo_redo.add_deletion(
                    start=start_insert, end=new_pos, text="\n".join(strings)
                )

        self._caret.update_caret_after_moving(new_pos, False)
        self.set_is_caret_change()
        return True

    def _marker(self, **kwargs):
        """
        marker function :
        **kwargs: **{"shift":True/False, "ctrl":True/False}
            | shift | ctrl | function
            |       |      | goto next marker
            |   x   |      | goto previous marker
            |       |   x  | add marker
            |   x   |   x  | clear marker
        -> bool: operation done successfully.
        """
        # kwarg decoding
        shift = False
        if "shift" in kwargs:
            shift = kwargs["shift"]
        if "ctrl" in kwargs:
            if kwargs["ctrl"]:
                # marker with control.
                if shift:
                    return self._clear_marker()
                else:
                    return self._add_marker()
        # marker without control.
        if shift:
            return self._previous_marker()
        else:
            return self._next_marker()

    def _add_marker(self):
        """
        add marker from caret position, if marker exists remove it.
        -> bool: True if added, False if already exists
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("add marker caret:{}".format(self._caret))
        coo = self._paragraphs.coo_from_pos(self._caret.end)
        if EDITOR_LOG <= logging.INFO:
            log.info("marker coordinate:{}".format(coo))
        if self._markers.add_marker(coo, self._paragraphs.paragraph(coo.paragraph)):
            return True
        else:
            return self._remove_marker()

    def _remove_marker(self):
        """
        remove markers at caret position.
        -> bool: always True
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("remove marker caret:{}".format(self._caret))
        coo = self._paragraphs.coo_from_pos(self._caret.end)
        self._markers.remove_marker(coo, self._paragraphs.paragraph(coo.paragraph))
        return True

    def _clear_marker(self):
        """
        clear all markers.
        -> bool: always True
        """
        self._markers.clear_marker()
        return True

    def _next_marker(self):
        """
        put caret on next marker.
        -> bool: always True
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("next marker caret:{}".format(self._caret))
        coo = self._paragraphs.coo_from_pos(self._caret.end)
        if EDITOR_LOG <= logging.INFO:
            log.info("next marker coo:{}".format(coo))
        coo = self._markers.next_marker(coo, self._paragraphs)
        if EDITOR_LOG <= logging.INFO:
            log.info("after next marker coo:{}".format(coo))
        new_pos = self._paragraphs.pos_from_coo(coo)
        if EDITOR_LOG <= logging.INFO:
            log.info("after next marker:{}".format(new_pos))
        self._caret.update_caret_after_moving(new_pos, False)
        self.set_is_caret_change()
        return True

    def _previous_marker(self):
        """
        put caret on previous marker.
        -> bool: always True
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("previous marker caret:{}".format(self._caret))
        coo = self._paragraphs.coo_from_pos(self._caret.end)
        if EDITOR_LOG <= logging.INFO:
            log.info("previous marker coo:{}".format(coo))
        coo = self._markers.previous_marker(coo, self._paragraphs)
        if EDITOR_LOG <= logging.INFO:
            log.info("after previous marker coo:{}".format(coo))
        new_pos = self._paragraphs.pos_from_coo(coo)
        if EDITOR_LOG <= logging.INFO:
            log.info("after previous marker:{}".format(new_pos))
        self._caret.update_caret_after_moving(new_pos, False)
        self.set_is_caret_change()
        return True

    def _find(self, **kwargs):
        """
        put selection on string to find.
        **kwarg:**{
            "shift": True for reverse search.
            "replace_parameters": FindParameters.
            }
        """
        # kwarg decoding
        if ("shift" in kwargs) and kwargs["shift"]:
            return self._find_previous(kwargs["replace_parameters"])
        return self._find_next(kwargs["replace_parameters"])

    def _find_next(self, find_parameters):
        """
        put selection on string to find.
            find_parameters: FindParameters.
        -> True if caret change
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("find next<{}>".format(find_parameters))
        save_caret = Caret(self._caret)
        if not self._caret.is_selection_empty():
            # If a selection is done, we forget it.
            self._caret.clear_selection_from_last()
        (deb_pos, end_pos) = self._paragraphs.find_next(
            self._caret.end, find_parameters
        )
        if deb_pos != end_pos:
            # New selection found.
            if self._is_selection:
                # New selection is extended from end
                self._caret.start = save_caret.start
                self._caret.end = end_pos
            else:
                # New selection is the found seq.
                self._caret.start = deb_pos
                self._caret.end = end_pos
                self._is_selection_by_find = True
            if EDITOR_LOG <= logging.INFO:
                log.info("Seq. found at <{}>".format(self._caret))
            self.set_is_caret_change()
            return True
        else:
            # Seq not found.
            if EDITOR_LOG <= logging.INFO:
                log.info("Seq. not found")
            return False

    def _find_previous(self, find_parameters) -> bool:
        """
        put selection on string to find (reverse search).
            find_parameters: FindParameters.
        -> True if caret change
        """
        if EDITOR_LOG <= logging.INFO:
            log.info("find previous<{}>".format(find_parameters))
        save_caret = Caret(self._caret)
        if not self._caret.is_selection_empty():
            # If a selection is done, we forget it.
            self._caret.clear_selection_from_first()
        (deb_pos, end_pos) = self._paragraphs.find_previous(
            self._caret.end, find_parameters
        )
        if deb_pos != end_pos:
            # New selection found.
            if self._is_selection:
                # New selection is extended from end
                self._caret.start = save_caret.start
                self._caret.end = end_pos
            else:
                self._caret.start = deb_pos
                self._caret.end = end_pos
                self._is_selection_by_find = True
            self.set_is_caret_change()
            return True
        else:
            # Seq not found.
            return False

    def _replace_and_find(self, **kwargs):
        """
        put selection on string to find.
        **kwarg:**{
            "shift": True for reverse search.
            "replace_parameters": FindParameters.
            }
        """
        # kwarg decoding
        if ("shift" in kwargs) and kwargs["shift"]:
            return self._replace_and_previous(kwargs["replace_parameters"])
        return self._replace_and_next(kwargs["replace_parameters"])

    def _replace_and_next(self, replace_parameters):
        if self.read_only:
            return False
        if EDITOR_LOG <= logging.INFO:
            log.info("replace and next<{}>".format(replace_parameters))
        if not self._caret.is_selection_empty() and self._is_selection_by_find:
            # Delete selection
            self.__delete()
            # Insert replacement text
            self.__put_string(replace_parameters.replace_seq)
            # Find next
            return self._find_next(replace_parameters)
        else:
            # Replace not allowed.
            return False

    def _replace_and_previous(self, replace_parameters):
        if self.read_only:
            return False
        if EDITOR_LOG <= logging.INFO:
            log.info("replace and previous<{}>".format(replace_parameters))
        if not self._caret.is_selection_empty() and self._is_selection_by_find:
            # Delete selection
            self.__delete()
            # Insert replacement text
            self._insert_strings_with_undo(replace_parameters.replace_seq)
            # Find next
            return self._find_previous(replace_parameters)
        else:
            # Replace not allowed.
            return False

    def _replace_all(self, **kwargs) -> bool:
        """
        put selection on string to find.
        **kwarg:**{
            "replace_parameters": FindParameters.
            }
        -> bool: True if at least one replacement done.
        """
        if self.read_only:
            return False
        replace_parameters = kwargs["replace_parameters"]
        if EDITOR_LOG <= logging.INFO:
            log.info("replace all<{}>".format(replace_parameters))
        if not self._caret.is_selection_empty() and self._is_selection_by_find:
            # Replace the current selection and search the next.
            self._replace_and_next(replace_parameters)
        else:
            # No selection, search the next and return False if nothing found.
            result = self._find_next(replace_parameters)
            if not result:
                return False

        while not self._caret.is_selection_empty() and self._is_selection_by_find:
            # Replace all seq and find the next.
            self._replace_and_next(replace_parameters)

        # At least one replacement has been done => Return true.
        return True


# -----------------------------------------------
# Unitary test
def main():
    pass


if __name__ == "__main__":
    main()
