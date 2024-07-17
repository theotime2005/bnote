"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from .pos import Pos
from .coordinates import Coordinates
from .paragraph import Paragraph

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_PARAGRAPH_LOG, logging
log = ColoredLogger(__name__, level=EDITOR_PARAGRAPH_LOG)


class Paragraphs:

    def __init__(self, width, paragraphs=None):
        self._width = width
        self._paragraphs = []
        # Use to create paragraph with an unique id.
        self.__paragraph_id = 1
        if paragraphs:
            for paragraph in paragraphs:
                self.append(paragraph)
        # modification indicator
        self.is_modified = False

    # For print()
    def __repr__(self):
        text = "--------------\r\n"
        text += f"Document of {len(self._paragraphs)} paragraphs\r\n"
        for index, paragraph in enumerate(self._paragraphs):
            text += paragraph.__str__()
        text += "--------------\r\n"
        return text

    def statistics(self):
        """
        Document statistics.
        -> paragraphs count, words count, character counts: int, int, int
        """
        word_count = 0
        character_count = 0
        index = 0
        for index, paragraph in enumerate(self._paragraphs):
            (p_word_count, p_character_count) = paragraph.statistics()
            word_count += p_word_count
            character_count += p_character_count
        return index + 1, word_count, character_count

    def paragraph_text(self, index):
        """
            Return the paragraph text.
            index: int paragraph order
            -> str
        """
        if index < len(self._paragraphs):
            text = self._paragraphs[index].paragraph_text()
            if text is not None:
                return text
            else:
                return ""
        else:
            return None

    def paragraph(self, index) -> Paragraph:
        """
            Return the paragraph at index.
            index: int paragraph order
            -> Paragraph
        """
        return self._paragraphs[index]

    def paragraph_pos(self, paragraph_index, offset):
        """
            compute coordinate from index of paragraph and an offset in paragraph
            -> pos (column, line in editor)
        """
        lines = 0
        paragraph = None
        for index, paragraph in enumerate(self._paragraphs):
            if index < paragraph_index:
                lines += paragraph.lines_count()
            else:
                break
        if paragraph:
            pos = paragraph.coordinates_from_index(offset)
        else:
            # It is not a wished case.
            pos = Pos(0, 0)
        pos.y += lines
        return pos

    @staticmethod
    def _remove_control_chars(s):
        """
        Filter all characters lesser than space code at the exception of tab code ('\t')
        """
        # return ''.join([c for c in s if ord(c) > 31 or ord(c) == 9])
        return ''.join([c for c in s if ((ord(c) > 31) or (c == '\t'))])

    def create_paragraph(self, paragraph:str):
        """
        Add a paragraph to the collection.
        Give it an unique Id.
        """
        paragraph = Paragraph(self._remove_control_chars(paragraph), self.__paragraph_id, self._width)
        self.__paragraph_id += 1
        return paragraph

    def append(self, paragraph):
        """
        Append a new paragraph to collection with a line of text converted into multi-line paragraph.
        this function is used to construct document model.
        line: text of a paragraph
        -> No return
        """
        self._paragraphs.append(self.create_paragraph(paragraph))

    def lines_count(self, paragraph_index=None):
        """
        Get the number of lines in the document when paragraph are justified.
        paragraph_index: int (zero based paragraph index to reach) default is None
        (if paragraph_index==0 the number of lines returned is 0)
        -> int number of lines
        """
        lines = 0
        if (paragraph_index is not None) and (paragraph_index == 0):
            return lines
        for index, paragraph in enumerate(self._paragraphs):
            lines += paragraph.lines_count()
            if (paragraph_index is not None) and (index >= paragraph_index - 1):
                break
        return lines

    def last_paragraph_lines_count(self):
        """
        Get the number of lines of the last justified paragraph.
        -> int : Number of lines (1 to n)
        """
        return self._paragraphs[-1].lines_count()

    def resize_line_length(self, pos, line_length):
        """
            Reformat paragraph with a new line length
            line_length: int is the new line length
            pos:Pos(x,y) is the current position
            -> Pos(x,y) the new position
        """
        if self._width != line_length:
            self._width = line_length
            # Save current caret as #paragraph and #index in paragraph.
            coo = self.coo_from_pos(pos)
            # Resize all lines
            for index, paragraph in enumerate(self._paragraphs):
                if coo.paragraph == index:
                    pos = paragraph.resize_line_length(line_length, Pos(coo.column, coo.line))
                    coo.column = pos.x
                    coo.line = pos.y
                else:
                    paragraph.resize_line_length(line_length)

            # Restore current caret
            pos = self.pos_from_coo(coo)
        return pos

    def paragraphs_count(self):
        """
        Get the number of paragraphs in document.
        -> int
        """
        return len(self._paragraphs)

    def paragraph_index(self, pos):
        """
        Get the paragraph index at pos
        pos: Pos(column, line)
        -> int paragraph index
        """
        coo = self.coo_from_pos(pos)
        return coo.paragraph

    def paragraph_and_line_index_from_pos(self, pos):
        """
        Get the paragraph at pos
        pos: Pos(column, line)
        -> paragraph
        -> current line index in paragraph
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            return coo.line, self._paragraphs[coo.paragraph]

    def paragraph_and_line_index(self, pos):
        """
            get paragraph index in document and index of line in paragraph at caret.end.
            pos: Pos(column, line)
            -> Pos(paragraph index and index of line in paragraph)
        """
        coo = self.coo_from_pos(pos)
        # index = self._paragraphs[coo.paragraph].index_from_coordinates(Pos(coo.column, coo.line))
        # index is index in paragraph of the beginning of the line.
        index = self._paragraphs[coo.paragraph].index_from_coordinates(Pos(0, coo.line))
        return Pos(coo.paragraph, index)

    def paragraph_and_character_index(self, pos):
        """
        Get the paragraph index and paragraph text offset at pos
        -> Pos(int paragraph index, int char offset in concat paragraph)
        """
        coo = self.coo_from_pos(pos)
        # index = self._paragraphs[coo.paragraph].index_from_coordinates(Pos(coo.column, coo.line))
        # index is index in paragraph of the beginning of the line.
        index = self._paragraphs[coo.paragraph].index_from_coordinates(Pos(0, coo.line))
        return Pos(coo.paragraph, index + coo.column)

    def coo_from_pos(self, pos):
        """
        Compute coordinate (column, line, paragraph) from pos (column, line in editor)
        pos: Pos(column, line)
        -> Coordinates(Column, Line, Paragraph) may be Coordinates(-1, -1, -1)
        """
        coo = Coordinates(pos.x, pos.y, 0)
        while coo.paragraph < len(self._paragraphs):
            count = self._paragraphs[coo.paragraph].lines_count()
            if coo.line > 0 and coo.line >= count:
                coo.line -= count
                coo.paragraph += 1
            else:
                return coo
        return Coordinates(-1, -1, -1)

    def pos_from_coo(self, coo):
        """
        Compute pos (column, line in editor) from coordinate (column, line, paragraph)
        coo: Coordinates(Column, Line, Paragraph)
        -> pos: Pos(column, line)
        """
        pos = Pos(coo.column, 0)
        par = 0
        while par < coo.paragraph:
            pos.y += self._paragraphs[par].lines_count()
            par += 1
        pos.y += coo.line
        return pos

    def check_pos(self, pos):
        """
        Verify a pos in editor.
        pos: Pos(column, line)
        -> Pos(column, line) pos or nearest pos
        """
        coo = self.coo_from_pos(pos)
        if coo == Coordinates(-1, -1, -1):
            return self.move_end_of_document(pos)
        if coo.line >= self._paragraphs[coo.paragraph].lines_count():
            return self.move_end_of_document(pos)
        if coo.column > len(self._paragraphs[coo.paragraph].line(coo.line)):
            coo.column = len(self._paragraphs[coo.paragraph].line(coo.line))

        return self.pos_from_coo(coo)

    def move_right(self, pos):
        """
        Move pos to right with line change.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            new_pos = Pos(coo.column, coo.line)
            if self._paragraphs[coo.paragraph].move_right(new_pos):
                # stay inside the current paragraph
                coo.line = new_pos.y
                coo.column = new_pos.x
                pos = self.pos_from_coo(coo)
            elif coo.paragraph < len(self._paragraphs) - 1:
                # Next paragraph
                coo.column = 0
                coo.line = 0
                coo.paragraph += 1
                pos = self.pos_from_coo(coo)
        # End of document
        return pos

    def move_left(self, pos):
        """
        Move pos to left with line change.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            new_pos = Pos(coo.column, coo.line)
            if self._paragraphs[coo.paragraph].move_left(new_pos):
                # stay inside the current paragraph
                coo.line = new_pos.y
                coo.column = new_pos.x
                pos = self.pos_from_coo(coo)
            elif coo.paragraph > 0:
                # change of paragraph
                coo.paragraph -= 1
                coo.line = self._paragraphs[coo.paragraph].last_line()
                coo.column = self._paragraphs[coo.paragraph].last_column(coo.line)
                pos = self.pos_from_coo(coo)
        return pos

    def move_up(self, pos, old_x):
        """
        Move pos up.
        pos: Pos(column, line)
        old_x: wished column
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            new_pos = Pos(coo.column, coo.line)
            new_pos = self._paragraphs[coo.paragraph].move_up(new_pos, old_x)
            if new_pos.y != -1:
                # stay inside the current paragraph
                coo.line = new_pos.y
                coo.column = new_pos.x
                pos = self.pos_from_coo(coo)
            elif coo.paragraph > 0:
                # change of paragraph
                coo.paragraph -= 1
                coo.line = self._paragraphs[coo.paragraph].last_line()
                coo.column = self._paragraphs[coo.paragraph].move_column(coo.line, old_x)
                pos = self.pos_from_coo(coo)
        return pos

    def move_down(self, pos, old_x):
        """
        Move pos down.
        pos: Pos(column, line)
        old_x: wished column
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            new_pos = Pos(coo.column, coo.line)
            new_pos = self._paragraphs[coo.paragraph].move_down(new_pos, old_x)
            if new_pos.y != -1:
                # stay inside the current paragraph
                coo.line = new_pos.y
                coo.column = new_pos.x
                pos = self.pos_from_coo(coo)
            elif coo.paragraph < len(self._paragraphs) - 1:
                # Next paragraph
                coo.line = 0
                coo.paragraph += 1
                coo.column = self._paragraphs[coo.paragraph].move_column(coo.line, old_x)
                pos = self.pos_from_coo(coo)
        return pos

    # move end of line
    def move_end_of_line(self, pos):
        """
        Move to end of line.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            pos.x = self._paragraphs[coo.paragraph].last_column(coo.line)
        return pos

    def move_end_of_paragraph(self, pos):
        """
        Move to end of paragraph.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph != -1:
            pos = self._paragraphs[coo.paragraph].end_of_paragraph()
            coo.column = pos.x
            coo.line = pos.y
        return self.pos_from_coo(coo)

    # move end of document
    def move_end_of_document(self, pos):
        """
        Move to end of document.
        pos: Pos(column, line) (not used)
        -> Pos(column, line) new pos
        """
        coo = Coordinates(0, 0, len(self._paragraphs) - 1)
        if coo.paragraph != -1:
            pos = self._paragraphs[len(self._paragraphs) - 1].end_of_paragraph()
            coo.column = pos.x
            coo.line = pos.y
        return self.pos_from_coo(coo)

    def move_previous_paragraph(self, pos):
        """
        Move to previous paragraph or go to the start of current paragraph.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.line != 0 or coo.column != 0:
            # If not at the start of paragraph goto this position.
            coo.line = 0
            coo.column = 0
        elif coo.paragraph > 0:
            # backward of one paragraph.
            coo.paragraph -= 1
        pos = self.pos_from_coo(coo)
        return pos

    def move_next_paragraph(self, pos):
        """
        Move to next paragraph or go to the end of last paragraph.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if coo.paragraph < self.paragraphs_count() - 1:
            # forward of one paragraph.
            coo.paragraph += 1
            # Goto the the start of paragraph.
            coo.line = 0
            coo.column = 0
        else:
            return self.move_end_of_paragraph(pos)
        pos = self.pos_from_coo(coo)
        return pos

    def move_previous_word(self, pos):
        """
        Move to previous word.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        pos = self._paragraphs[coo.paragraph].move_previous_word(Pos(coo.column, coo.line))
        if pos == Pos(-1, -1):
            if coo.paragraph > 0:
                # backward of one paragraph.
                coo.paragraph -= 1
                # Goto at the end of paragraph
                pos = self._paragraphs[coo.paragraph].end_of_paragraph()
                coo.line = pos.y
                coo.column = pos.x
                return self.move_previous_word(self.pos_from_coo(coo))
            else:
                return Pos(0, 0)
        else:
            return self.pos_from_coo(Coordinates(pos.x, pos.y, coo.paragraph))

    def move_next_word(self, pos):
        """
        Move to next word.
        pos: Pos(column, line)
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        paragraph_pos = self._paragraphs[coo.paragraph].move_next_word(Pos(coo.column, coo.line))
        if paragraph_pos == Pos(-1, -1):
            if coo.paragraph < self.paragraphs_count() - 1:
                # forward of one paragraph.
                coo.paragraph += 1
                # Goto start of paragraph.
                paragraph_pos.x = 0
                paragraph_pos.y = 0
            else:
                # Reach end of document
                return self.move_end_of_document(pos)
        pos = self.pos_from_coo(Coordinates(paragraph_pos.x, paragraph_pos.y, coo.paragraph))
        return pos

    def characters(self, pos):
        """
            Get before and after pos input point.
            pos is char index in paragraph.
            -> char before, char after (may be None)
        """
        coo = self.coo_from_pos(pos)
        return self._paragraphs[coo.paragraph].characters(Pos(coo.column, coo.line))

    def select_word(self, pos):
        """
            select the current word at pos.
            pos (x, y) are position in paragraph.
            -> (Pos: start index of word in paragraph, Pos: end index of word in paragraph)
            may be (None, None)
        """
        coo = self.coo_from_pos(pos)
        start_pos, end_pos = self._paragraphs[coo.paragraph].select_word(Pos(coo.column, coo.line))
        if start_pos:
            if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                log.info("word position {}, {}".format(start_pos, end_pos))
            return self.pos_from_coo(Coordinates(start_pos.x, start_pos.y, coo.paragraph)), \
                   self.pos_from_coo(Coordinates(end_pos.x, end_pos.y, coo.paragraph))
        else:
            return None, None

    def line(self, line_index):
        """
        Get the text of a line identified by index (0 to n) in a justified document.
        line_index: int
        -> str
        """
        # print("index:{}".format(line_index))
        coo = self.coo_from_pos(Pos(0, line_index))
        # print(coo)
        if coo.paragraph != -1:
            return self._paragraphs[coo.paragraph].line(coo.line)
        return ""

    def id(self, line_index):
        """
        Get id of the paragraph referenced by line_index.
        line_index: int
        -> int id (0 if id not found)
        """
        coo = self.coo_from_pos(Pos(0, line_index))
        # print(coo)
        if coo.paragraph != -1:
            return self._paragraphs[coo.paragraph].id()
        return 0

    def insert_strings(self, pos, markers, strings):
        """
        Insert a string at pos.
        pos: Pos(column, line)
        markers: Markers of document
        strings: str[]
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        if EDITOR_PARAGRAPH_LOG <= logging.INFO:
            log.info("insert strings <{}> at coo<{}> pos<{}>".format(strings, coo, pos))
        # tag paragraphs as modified.
        self.is_modified = True
        if len(strings) == 1:
            s = self._remove_control_chars(strings[0])
            # Insert the text in current paragraph
            new_pos = self._paragraphs[coo.paragraph].insert_string(Pos(coo.column, coo.line), s)
            # update markers positions after insertion of some characters in a line.
            markers.insert_char_in_paragraph(coo, self._paragraphs[coo.paragraph], len(s))
            # update caret position.
            coo.line = new_pos.y
            coo.column = new_pos.x
            if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                log.info("single text paragraph insertion modification at coo<{}> pos<{}>".format(coo, pos))
        else:
            after_string = ""
            if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                log.info("lines number is {}".format(len(strings)))
            markers_saved = None
            for num, string in enumerate(strings):
                if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                    log.info("insert paragraph<{}>".format(string))
                s = self._remove_control_chars(string)
                if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                    log.info("filtered paragraph<{}>".format(string))
                    log.info("current line is {}, lines number is {}".format(num, len(strings)))
                if num == 0:
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("insert first paragraph")
                    # Insert the first line and create paragraph for others.
                    new_pos = self._paragraphs[coo.paragraph].insert_string(Pos(coo.column, coo.line), s)
                    # update markers positions after insertion of some characters in a line.
                    markers.insert_char_in_paragraph(coo, self._paragraphs[coo.paragraph], len(s))
                    after_string = self._paragraphs[coo.paragraph].split_paragraph(new_pos)
                    # save markers positions in after_string.
                    markers_saved = markers.extract(coo, Paragraph(after_string, 0, self._width), len(after_string))
                    coo.line = new_pos.y
                    coo.column = new_pos.x
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("first paragraph insertion at coo<{}> pos<{}>".format(strings, coo, pos))
                elif num != len(strings) - 1:
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("insert not first, not  last paragraph")
                    # last line to insert
                    coo.paragraph += 1
                    self._paragraphs.insert(coo.paragraph, self.create_paragraph(s))
                    # Update markers positions after paragraph insertion
                    markers.insert_paragraphs(coo, 1)
                    # inc offset order of all next paragraph
                    # Cette ligne ne correspond pas à une méthode existante ?
                    # Dans bnote non plus ?
                    #self._inc_offset_order(coo.paragraph + 1, 1)
                    if after_string != "":
                        # Replace the markers situated in after_string area
                        markers.replace(coo, markers_saved, len(s))
                        new_pos = Pos(0, 0)
                    else:
                        new_pos = self._paragraphs[coo.paragraph].end_of_paragraph()
                    coo.line = new_pos.y
                    coo.column = new_pos.x
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("next paragraph insertion modification at coo<{}> pos<{}>".format(coo, pos))
                else:
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("insert last paragraph")
                    coo.paragraph += 1
                    # Insert a new empty line
                    self._paragraphs.insert(coo.paragraph, self.create_paragraph(s + after_string))
                    # Update markers positions after paragraph insertion
                    markers.insert_paragraphs(coo, 1)
                    if after_string != "":
                        # Replace the markers situated in after_string area
                        markers.replace(coo, markers_saved, len(s))
                        after_string = ""
                    index = len(s)
                    new_pos = self._paragraphs[coo.paragraph].coordinates_from_index(index)
                    coo.line = new_pos.y
                    coo.column = new_pos.x
                    if EDITOR_PARAGRAPH_LOG <= logging.INFO:
                        log.info("last paragraph insertion modification at coo<{}> pos<{}>".format(coo, pos))
        pos = self.pos_from_coo(coo)
        return pos

    def delete_char(self, pos, markers):
        """
        Delete a character at pos.
        pos: Pos(column, line)
        markers: Markers of document
        -> Pos(column, line) new pos
        """
        coo = self.coo_from_pos(pos)
        paragraph_pos = Pos(coo.column, coo.line)
        # tag paragraphs as modified.
        self.is_modified = True
        if self._paragraphs[coo.paragraph].is_end(paragraph_pos):
            # merge 2 paragraph.
            if coo.paragraph + 1 < len(self._paragraphs):
                new_pos = self._paragraphs[coo.paragraph].merge(paragraph_pos, self._paragraphs[coo.paragraph + 1])
                self._paragraphs.pop(coo.paragraph + 1)
                # Update markers after one paragraph deletion (fusion of 2 paragraph)
                markers.delete_paragraphs(coo, 1)
                coo.line = new_pos.y
                coo.column = new_pos.x
                return self.pos_from_coo(coo)
        else:
            # Update markers after character deletion in a paragraph
            markers.delete_char_in_paragraph(coo, self._paragraphs[coo.paragraph], 1)
            # remove a character in the current paragraph.
            new_pos = self._paragraphs[coo.paragraph].delete_char(paragraph_pos)
            coo.line = new_pos.y
            coo.column = new_pos.x
            return self.pos_from_coo(coo)
        return pos

    def delete_selection(self, start, end, markers):
        """
        Delete a selection from start to end.
        start: Pos(column, line)
        end: Pos(column, line)
        markers: Markers of document
        -> Pos(column, line) new pos
        """
        coo_start = self.coo_from_pos(start)
        coo_end = self.coo_from_pos(end)
        # tag paragraphs as modified.
        self.is_modified = True
        if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
            log.debug("step0 {}".format(markers))

        if coo_start.paragraph == coo_end.paragraph:
            # Delete a part of a paragraph.
            # Update markers after character deletion in a paragraph
            index_start = self._paragraphs[coo_start.paragraph].index_from_coordinates(
                Pos(coo_start.column, coo_start.line))
            index_end = self._paragraphs[coo_start.paragraph].index_from_coordinates(Pos(coo_end.column, coo_end.line))
            markers.delete_char_in_paragraph(coo_start, self._paragraphs[coo_start.paragraph],
                                             index_end - index_start)
            if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
                log.debug("coo_start.paragraph == coo_end.paragraph {}".format(markers))
            # Do deletion.
            new_pos = self._paragraphs[coo_start.paragraph]. \
                delete(Pos(coo_start.column, coo_start.line), Pos(coo_end.column, coo_end.line))
            coo_start.line = new_pos.y
            coo_start.column = new_pos.x
            return self.pos_from_coo(coo_start)
        else:
            # delete multiple lines
            # Step 1 : Delete the end of first paragraph
            # Update markers after character deletion of the end of first paragraph
            index_start = self._paragraphs[coo_start.paragraph].index_from_coordinates(
                Pos(coo_start.column, coo_start.line))
            index_end = self._paragraphs[coo_start.paragraph].index_from_coordinates(
                self._paragraphs[coo_start.paragraph].end_of_paragraph())
            markers.delete_char_in_paragraph(coo_start, self._paragraphs[coo_start.paragraph], index_end - index_start)
            if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
                log.debug("step1 {}".format(markers))

            # Do deletion.
            new_pos = self._paragraphs[coo_start.paragraph]. \
                delete(Pos(coo_start.column, coo_start.line), self._paragraphs[coo_start.paragraph].end_of_paragraph())

            # Step 2 : Delete entire paragraphs.
            # Update markers
            coo_current = Coordinates(coo_start.column, coo_start.line, coo_start.paragraph + 1)
            markers.delete_paragraphs(coo_current, coo_end.paragraph - coo_current.paragraph)
            # Delete paragraphs
            while coo_current.paragraph < coo_end.paragraph:
                # delete complete paragraph
                self._paragraphs.pop(coo_start.paragraph + 1)
                coo_current.paragraph += 1
                if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
                    log.debug("step2 {}".format(markers))
            # Step 3 : Delete the beginning of the last paragraph
            coo_current = Coordinates(0, 0, coo_start.paragraph + 1)
            # Update Markers after deletion of the beginning of the paragraph.
            index_end = self._paragraphs[coo_current.paragraph].index_from_coordinates(
                Pos(coo_end.column, coo_end.line))
            markers.delete_char_in_paragraph(coo_current, self._paragraphs[coo_current.paragraph], index_end)
            if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
                log.debug("step3 {}".format(markers))
            # Do deletion.
            self._paragraphs[coo_current.paragraph].delete(Pos(0, 0), Pos(coo_end.column, coo_end.line))

            # Step 4 : Merge the first and the last paragraph not deleted
            # Update markers before merging.
            markers.merge_paragraph(coo_start, self._paragraphs[coo_start.paragraph])
            if EDITOR_PARAGRAPH_LOG <= logging.DEBUG:
                log.debug("step4 {}".format(markers))
            # Do merging.
            new_pos = self._paragraphs[coo_start.paragraph]. \
                merge(Pos(coo_start.column, coo_start.line), self._paragraphs[coo_start.paragraph + 1])
            self._paragraphs.pop(coo_start.paragraph + 1)
            coo_start.line = new_pos.y
            coo_start.column = new_pos.x
            return self.pos_from_coo(coo_start)

    def delete_paragraph(self, index, markers):
        """
        Delete paragraph
        index: paragraph index (0 to n)
        markers: Markers of document
        -> True if done, None otherwise
        """
        if index < len(self._paragraphs):
            coo = Coordinates(0, 0, index)
            self._paragraphs.pop(index)
            markers.delete_paragraphs(coo, 1)
            return True

    def selection(self, start, end):
        """
        Get the selection, a multi line text (each line separate by \r\n)
        start: Pos(column, line)
        end: Pos(column, line)
        -> str
        """
        coo_start = self.coo_from_pos(start)
        coo_end = self.coo_from_pos(end)
        if coo_start.paragraph == coo_end.paragraph:
            # extract a part of a paragraph
            text = self._paragraphs[coo_start.paragraph]. \
                text(Pos(coo_start.column, coo_start.line), Pos(coo_end.column, coo_end.line))
        else:
            # Extract multi-line
            # Extract the end of first paragraph
            text = self._paragraphs[coo_start.paragraph]. \
                text(Pos(coo_start.column, coo_start.line), self._paragraphs[coo_start.paragraph].end_of_paragraph())
            current_paragraph = coo_start.paragraph + 1
            while current_paragraph < coo_end.paragraph:
                # extract complete paragraph
                text += "\r\n" + self._paragraphs[current_paragraph].concat_paragraph()
                current_paragraph += 1
            # extract the start of the last paragraph
            text += "\r\n" + self._paragraphs[current_paragraph]. \
                text(Pos(0, 0), Pos(coo_end.column, coo_end.line))
        if EDITOR_PARAGRAPH_LOG <= logging.INFO:
            log.info("Selection:{}".format(text))
        return text

    def selection(self, start, end):
        """
        Get the selection, a multi line text (each line separate by \r\n)
        start: Pos(column, line)
        end: Pos(column, line)
        -> str
        """
        coo_start = self.coo_from_pos(start)
        coo_end = self.coo_from_pos(end)
        if coo_start.paragraph == coo_end.paragraph:
            # extract a part of a paragraph
            text = self._paragraphs[coo_start.paragraph]. \
                text(Pos(coo_start.column, coo_start.line), Pos(coo_end.column, coo_end.line))
        else:
            # Extract multi-line
            # Extract the end of first paragraph
            text = self._paragraphs[coo_start.paragraph]. \
                text(Pos(coo_start.column, coo_start.line), self._paragraphs[coo_start.paragraph].end_of_paragraph())
            current_paragraph = coo_start.paragraph + 1
            while current_paragraph < coo_end.paragraph:
                # extract complete paragraph
                text += "\r\n" + self._paragraphs[current_paragraph].concat_paragraph()
                current_paragraph += 1
            # extract the start of the last paragraph
            text += "\r\n" + self._paragraphs[current_paragraph]. \
                text(Pos(0, 0), Pos(coo_end.column, coo_end.line))
        log.info("Selection:{}".format(text))
        return text

    def find_next(self, pos, find_parameters):
        """
        Find the next FindParameters criteria
        pos: Pos(x,y) the current position where the search begins
        find_parameters: an instance of FindParameters
        -> (start: Pos(x,y) the start position, end: Pos(x,y) the end position)
        if not found (pos, pos) is the input pos
        """
        coo = self.coo_from_pos(pos)
        current_paragraph = coo.paragraph
        (start, end) = self._paragraphs[current_paragraph].find_next(Pos(coo.column, coo.line), find_parameters)
        while start == end and current_paragraph < len(self._paragraphs) - 1:
            current_paragraph += 1
            (start, end) = self._paragraphs[current_paragraph].find_next(Pos(0, 0), find_parameters)
        if start == end:
            # Not found, return 2 equal original position
            return pos, pos
        else:
            return self.pos_from_coo(Coordinates(start.x, start.y, current_paragraph)), self.pos_from_coo(
                Coordinates(end.x, end.y, current_paragraph))

    def find_previous(self, pos, find_parameters):
        """
        Find the previous FindParameters criteria
        pos: Pos(x,y) the current position where the search begins
        find_parameters: an instance of FindParameters
        -> (start: Pos(x,y) the start position, end: Pos(x,y) the end position)
        if not found (pos, pos) is the input pos
        """
        coo = self.coo_from_pos(pos)
        current_paragraph = coo.paragraph
        (start, end) = self._paragraphs[current_paragraph].find_previous(Pos(coo.column, coo.line), find_parameters)
        while start == end and current_paragraph > 0:
            current_paragraph -= 1
            paragraph = self._paragraphs[current_paragraph]
            (start, end) = paragraph.find_previous(
                Pos(paragraph.last_column(paragraph.last_line()), paragraph.last_line()), find_parameters)
        if start == end:
            # Not found, return 2 identicals original position
            return pos, pos
        else:
            return self.pos_from_coo(Coordinates(start.x, start.y, current_paragraph)), self.pos_from_coo(
                Coordinates(end.x, end.y, current_paragraph))

