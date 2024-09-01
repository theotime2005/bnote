"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_PARAGRAPH_LOG, logging
from .pos import Pos

log = ColoredLogger(__name__, level=EDITOR_PARAGRAPH_LOG)


class Paragraph(object):
    '''
    Un paragraphe possède un identifiant qui lui est propre.

    Un paragraphe est découpé en ligne de 2 types
    Les lignes dont la fin remplace un espace
    Les lignes dont la fin ne remplace pas un espace (cas de la dernière ligne)
    '''

    def __init__(self, paragraph, id, width):
        self._id = id
        self._lines = []
        self._lines_count = 0
        self._width = width
        self._justify(paragraph)
        self._is_modified = True

    # For print()
    def __repr__(self):
        text = f"Paragraph of {self.lines_count()} lines, id:{self._id}, modified:{self._is_modified}\n"
        for index, line in enumerate(self._lines):
            text += f"    ({len(line)}){line}\r\n"
        return text

    def id(self):
        """
        Get paragraph's id.
        -> int
        """
        return self._id

    def is_modified_and_reset(self):
        """
        Current modified state of paragraph and reset the flag.
        """
        current_value = self._is_modified
        self._is_modified = False
        return current_value

    def statistics(self) -> (int, int):
        """
           Characteristics of paragraph.
           -> (int:words_count, int:characters_count)
        """
        characters_count = 0
        words_count = 0
        for line in self._lines:
            characters_count += len(line) + 1
            words_count += len(line.split())
        # The last line have not a space replace by a CRLF at the end.
        characters_count -= 1
        return words_count, characters_count

    def lines_count(self):
        """
            Number of lines in paragraph.
            -> int : Number of lines (1 to n)
        """
        if len(self._lines) == 0:
            # An empty paragraph is a paragraph of one empty line.
            return 1
        else:
            return len(self._lines)

    def line(self, index):
        """
            Return the text of one line of the paragraph.
            index is the zero based line index in paragraph.
            -> str (may be "")
        """
        if len(self._lines) > 0:
            return self._lines[index]
        else:
            return ""

    def characters(self, pos):
        """
            Get before and after pos input point.
            pos is char index in paragraph.
            -> char before, char after (may be None)
        """
        char_after = None
        char_before = None
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        if index > 0:
            char_before = paragraph[index - 1]
        if index < len(paragraph):
            char_after = paragraph[index]
        return char_before, char_after

    def last_line(self):
        """
            Returns index of the last line of this paragraph.
            -> int (zero based)
        """
        if len(self._lines) > 0:
            return len(self._lines) - 1
        else:
            return 0

    def last_column(self, line):
        """
            Returns index of last character of the line (+1 for cursor position)
            line is line index (zero based)
            -> int (zero based)
        """
        try:
            return len(self._lines[line])
        except IndexError:
            return 0

    def coordinates_from_index(self, index):
        """
            Calculate coordinates of a character indexed in the paragraph.
            index is char index (zero based)
            -> Pos : character position (x, y) in paragraph at given index.
        """
        pos = Pos(0, 0)
        y = 0
        line_ok = True
        while index > len(self._lines[y]):
            index -= len(self._lines[y]) + 1
            y += 1
            if len(self._lines) <= y:
                # y not reach.
                line_ok = False
                break
            pos.y += 1
        if line_ok:
            pos.x = index
        else:
            # y not reach, coordinates at the end of the last line.
            if y > 0:
                pos.x = len(self._lines[y - 1])
            else:
                pos.x = len(self._lines[y])
        return pos

    def index_from_coordinates(self, pos):
        """
            Calculate the index in the paragraph from Pos
            pos:Pos is character position (x, y) in paragraph.
            -> int: char index in paragraph (zero based)
        """
        index = 0
        y = 0
        if len(self._lines) > 0:
            while pos.y > y:
                index += len(self._lines[y]) + 1
                y += 1
            index += pos.x
        return index

    def concat_paragraph(self):
        """
            Construct a string with all paragraph lines.
            -> str where end of line are replaced by space.
        """
        paragraph = ""
        for index, line in enumerate(self._lines):
            if index == 0:
                paragraph += line
            else:
                paragraph += " " + line
        return paragraph

    def move_right(self, pos):
        """
            move pos to right.
            pos (x, y) are position in paragraph.
            -> True (pos is changed), False (pos is at the end of paragraph)
        """
        if pos.y < len(self._lines) and pos.x < len(self._lines[pos.y]):
            pos.x += 1
            return True
        elif pos.y < len(self._lines) - 1:
            pos.x = 0
            pos.y += 1
            return True
        else:
            # End of paragraph
            return False

    def move_left(self, pos):
        """
            move pos to left.
            pos (x, y) are position in paragraph.
            -> True (pos is changed), False (pos is at the end of paragraph)
        """
        if pos.x == 0:
            if pos.y != 0:
                pos.y -= 1
                pos.x = len(self._lines[pos.y])
                return True
            else:
                return False
        else:
            pos.x -= 1
            return True

    # pos are relative position in paragraph.
    def move_up(self, pos, old_x):
        """
            move pos to up.
            pos (x, y) are position in paragraph.
            old_x is the column position we would like to reach.
            -> Pos is the new pos in paragraph. Pos(-1, -1) already at the last line.
        """
        if pos.y != 0:
            pos.y -= 1
            if old_x > len(self._lines[pos.y]):
                pos.x = len(self._lines[pos.y])
            else:
                pos.x = old_x
            return pos
        else:
            return Pos(-1, -1)

    def move_down(self, pos, old_x):
        """
            move pos to down.
            pos (x, y) are position in paragraph.
            old_x is the column position we would like to reach.
            -> Pos is the new pos in paragraph. Pos(-1, -1) already at the first line.
        """
        if pos.y < len(self._lines) - 1:
            pos.y += 1
            if old_x > len(self._lines[pos.y]):
                pos.x = len(self._lines[pos.y])
            else:
                pos.x = old_x
            return pos
        else:
            return Pos(-1, -1)

    def move_previous_word(self, pos):
        """
            move to the previous word.
            pos (x, y) are position in paragraph.
            -> Pos is the new pos in paragraph. Pos(-1, -1) already at the first position.
        """
        if pos.x == 0 and pos.y == 0:
            # already at the first position in paragraph.
            return Pos(-1, -1)
        # backward in the paragraph
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        index -= 1
        # pass all space
        while index > 0 and paragraph[index] == ' ':
            index -= 1
        # pass all no space
        while index > 0 and paragraph[index] != ' ':
            index -= 1
        # forward on the first char of the word.
        if index > 0:
            index += 1
        return self.coordinates_from_index(index)

    def move_next_word(self, pos):
        """
            move to the next word.
            pos (x, y) are position in paragraph.
            -> Pos is the new pos in paragraph. Pos(-1, -1) already at the last position.
        """
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()

        # pass all no space
        while index < len(paragraph) and paragraph[index] != ' ':
            index += 1
        # pass all space
        while index < len(paragraph) and paragraph[index] == ' ':
            index += 1
        if index == len(paragraph):
            # already on the last word of paragraph.
            return Pos(-1, -1)
        else:
            return self.coordinates_from_index(index)

    def select_word(self, pos):
        """
            select the current word at pos.
            pos (x, y) are position in paragraph.
            -> (Pos: start index of word in paragraph, Pos: end index of word in paragraph).
        """
        if EDITOR_PARAGRAPH_LOG <= logging.INFO:
            log.info("select word at {}".format(pos))
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        if (len(paragraph) < index) or (paragraph[index] == ' '):
            return None, None
        # backward until space or beginning of the line
        while index > 0 and paragraph[index] != ' ':
            index -= 1
        if paragraph[index] == ' ':
            index += 1
        start_index = index
        while index < len(paragraph) and paragraph[index] != ' ':
            index += 1
        end_index = index
        return self.coordinates_from_index(start_index), self.coordinates_from_index(end_index)

    def move_column(self, line, old_x):
        """
            Try to return the better column in a line of the paragraph.
            line is the line index (zero based)
            old_x is the wished position.
        """
        if len(self._lines) == 0:
            # Empty line.
            return 0
        if line >= len(self._lines) or not self._lines[line]:
            #  Bad line index or self._lines[line] not defined.
            return 0
        if old_x > len(self._lines[line]):
            return len(self._lines[line])
        else:
            return old_x

    def end_of_paragraph(self):
        """
            Return end of paragraph position.
            -> Pos (x, y)
        """
        if len(self._lines) > 0:
            return Pos(self.last_column(len(self._lines) - 1), len(self._lines) - 1)
        else:
            return Pos(0, 0)

    def is_end(self, pos):
        """
            Check if position is at the end of the paragraph.
            pos: Pos(x,y) position in paragraph
            -> bool True or False
        """
        return pos == self.end_of_paragraph()

    def insert_string(self, pos, string):
        """
            insert a string in the paragraph at pos.
            pos: Pos(x,y) position in paragraph
            string: str
            -> Pos(x,y) position after insertion.
        """
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        paragraph = paragraph[0:index] + string + paragraph[index:len(paragraph)]
        index += len(string)
        self._is_modified = True
        self._justify(paragraph)
        return self.coordinates_from_index(index)

    def delete_char(self, pos):
        """
            Delete a character at pos
            pos: Pos(x,y) position in paragraph
            -> Pos(x,y) after deletion
        """
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        if index + 1 >= len(paragraph):
            paragraph = paragraph[0:index]
        else:
            paragraph = paragraph[0:index] + paragraph[index + 1:len(paragraph)]
        self._is_modified = True
        self._justify(paragraph)
        return self.coordinates_from_index(index)

    def delete(self, start, end):
        """
            Delete a character at pos
            start: Pos(x,y) start position of deletion in paragraph
            end: Pos(x,y) end position of deletion in paragraph
            -> Pos(x,y) after deletion
        """
        start_index = self.index_from_coordinates(start)
        end_index = self.index_from_coordinates(end)
        paragraph = self.concat_paragraph()
        if end_index > len(paragraph):
            paragraph = paragraph[0:start_index]
        else:
            paragraph = paragraph[0:start_index] + paragraph[end_index:len(paragraph)]
        self._is_modified = True
        self._justify(paragraph)
        return self.coordinates_from_index(start_index)

    def paragraph_text(self):
        """
            Return a line of text with all characters of paragraph.
        """
        return self.concat_paragraph()

    def text(self, start, end):
        """
            Return a part of text between 2 coordinates.
            start: Pos(x,y) start position of extraction in paragraph
            end: Pos(x,y) end position of extraction in paragraph
            -> str: the extracted string.
        """
        start_index = self.index_from_coordinates(start)
        end_index = self.index_from_coordinates(end)
        paragraph = self.concat_paragraph()
        return paragraph[start_index:end_index]

    def split_paragraph(self, pos):
        """
            Reduce the paragraph until pos and return the deleted string
            pos: Pos(x,y) reduction position in paragraph
            -> str : The removed string (current paragraph is modified)
        """
        index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        string = paragraph[index:len(paragraph)]
        paragraph = paragraph[0:index]
        self._is_modified = True
        self._justify(paragraph)
        return string

    def merge(self, pos, paragraph):
        """
            add to itself a paragraph at pos
            pos: Pos(x,y) is the input position
            paragraph: Paragraph is the paragraph to merge
            -> pos: Pos(x,y) is the new pos
        """
        index = self.index_from_coordinates(pos)
        paragraph1 = self.concat_paragraph()
        paragraph2 = paragraph.concat_paragraph()
        self._is_modified = True
        self._justify(paragraph1 + paragraph2)
        return self.coordinates_from_index(index)

    def resize_line_length(self, line_length, pos=None):
        """
            Reformat paragraph with a new line length
            line_length: int is the new line length
            pos:Pos(x,y) is the current position (maybe None)
            -> Pos(x,y) the new position (maybe None)
        """
        index = 0
        if pos:
            # save index in paragraph.
            index = self.index_from_coordinates(pos)
        paragraph = self.paragraph_text()
        self._width = line_length
        self._is_modified = True
        self._justify(paragraph)
        if pos:
            # save index in paragraph.
            return self.coordinates_from_index(index)

    def _justify(self, paragraph):
        """
            Construct the lines list of a paragraph.
            The space are used to cut the paragraph in line, if no space are present
            the line could exceed the line limit.
            paragraph: str is the text of paragraph
            self._width is the current line length of the paragraph
            -> self._lines is construct
        """
        length = 0
        self._lines = list()
        line = ""
        words = paragraph.split(' ')
        for index, word in enumerate(words):
            if index == 0:
                # Insert first word without space
                line += word
                length += len(word)
            elif length + len(word) < self._width:
                # Insert a space and the word
                line += " " + word
                length += 1 + len(word)
            else:
                # Line changement
                self._lines.append(line)
                line = word
                length = len(word)
        self._lines.append(line)

    def find_next(self, pos, find_parameters):
        """
            find the FindParameters criteria
            pos: Pos(x,y) the current position where the search begins
            find_parameters: an  instance of FindParameters
            -> (pos: Pos(x,y) the start position, pos: Pos(x,y) the end position)
            if not found (pos, pos) is the input pos
        """
        start_index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        index = find_parameters.find(paragraph, start_index)
        if index == -1:
            return pos, pos
        else:
            pos = self.coordinates_from_index(index)
            return self.coordinates_from_index(index), self.coordinates_from_index(
                index + len(find_parameters.edit_seq))

    def find_previous(self, pos, find_parameters):
        """
            reverse find the FindParameters criteria
            pos: Pos(x,y) the current position where the search begins
            find_parameters: an  instance of FindParameters
            -> (pos: Pos(x,y) the start position, pos: Pos(x,y) the end position)
            if not found (pos, pos) is the input pos
        """
        start_index = self.index_from_coordinates(pos)
        paragraph = self.concat_paragraph()
        # Find first case.
        index = find_parameters.find(paragraph, 0)
        last_index = index
        while index != -1 and index < start_index:
            # find others cases until reach the last.
            last_index = index
            index = find_parameters.find(paragraph, index + 1)
        if last_index == -1 or index >= start_index:
            return pos, pos
        else:
            pos = self.coordinates_from_index(last_index)
            return self.coordinates_from_index(last_index), self.coordinates_from_index(
                last_index + len(find_parameters.edit_seq))
