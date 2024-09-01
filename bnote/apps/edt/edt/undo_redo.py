"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time
from enum import Enum

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_UNDO_REDO_LOG, logging
from .pos import Pos

log = ColoredLogger(__name__, level=EDITOR_UNDO_REDO_LOG)

# MAXIMUM NUMBER OF OPERATIONS IN UNDO-REDO LIST.
OPERATIONS_MAX_COUNT = 5


class Operation:
    class Type(Enum):
        INSERTION = 1
        INSERTION_MERGEABLE = 2
        DELETION = 3
        DELETION_MERGEABLE = 4

    def __init__(self, op_type, **kwargs):
        self.__type = op_type

        # For insertion : start is the input position
        # for deletion : Characters to delete are between Start and End
        self.__start = kwargs.get('start', None)
        self.__end = kwargs.get('end', None)
        self.__text = kwargs.get('text', None)

        self.__time = time.time()

        if EDITOR_UNDO_REDO_LOG <= logging.INFO:
            log.info("create op:{}".format(self))

    # For print()
    def __str__(self):
        return "undo-redo op:[{}] time[{}] start[{}] end[{}] text[{}]".format(self.__type, self.__time, self.__start,
                                                                              self.__end, self.__text)

    def is_insertion(self):
        return (self.__type == Operation.Type.INSERTION) or (self.__type == Operation.Type.INSERTION_MERGEABLE)

    def is_deletion(self):
        return (self.__type == Operation.Type.DELETION) or (self.__type == Operation.Type.DELETION_MERGEABLE)

    def type(self):
        return self.__type

    def time(self):
        return self.__time

    def start(self):
        return self.__start

    def set_start(self, pos):
        self.__start = pos

    def end(self):
        return self.__end

    def set_end(self, pos):
        self.__end = pos

    def text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text


class UndoRedo:

    def __init__(self):
        self.__operations = []
        self.__current_index = -1

    # For print()
    def __str__(self):
        text = "current index:[{}]".format(self.__current_index)
        for op in self.__operations:
            text += "\n{}".format(op)
        return text

    def _clear_next_op(self):
        """
        Clear all next operation after current index.
        -> No return
        """
        if self.__current_index < len(self.__operations):
            del self.__operations[self.__current_index: len(self.__operations)]

    def _add_new_op(self, op_type, **kwargs):
        """
        Add new operation.
        op_type: Type
        **kwargs=
            start, end: Pos, Pos
            text: str the string deleted or None
        -> No return
        """
        self.__operations.append(Operation(op_type, **kwargs))
        # Control operations number
        if len(self.__operations) > OPERATIONS_MAX_COUNT:
            self.__operation = self.__operations[len(self.__operations) - (OPERATIONS_MAX_COUNT + 1): -1]
        self.__current_index = len(self.__operations)

    def add_char_deletion(self, **kwargs):
        """
        Deletion from start to end position
        to undo char insertion
        **kwargs=
         start, end: Pos, Pos
        -> No return
        """
        if EDITOR_UNDO_REDO_LOG <= logging.INFO:
            log.info("Add char deletion for undo")
        self._clear_next_op()

        # if time between 2 char deletion < 3 sec. concat deletion.
        if self.__current_index > 0:
            op = self.__operations[self.__current_index - 1]
            if (op.type() == Operation.Type.DELETION_MERGEABLE) and (op.time() + 5 > time.time()):
                start = kwargs.get('start', None)
                end = kwargs.get('end', None)
                text = kwargs.get('text', None)
                # Check if contiguous deletion
                if op.end() == start:
                    # Merge deletion
                    op.set_end(end)
                    op.set_text(op.text() + text)
                    return
        # Otherwise, create a new char deletion
        self._add_new_op(Operation.Type.DELETION_MERGEABLE, **kwargs)

    def add_char_insertion(self, **kwargs):
        """
        Deletion from start to end position of text
        to undo char deletion
        **kwargs=
         start, end: Pos, Pos
         text: str
        -> No return
        """
        if EDITOR_UNDO_REDO_LOG <= logging.INFO:
            log.info("Add char insertion for undo")
        self._clear_next_op()
        # if time between 2 char deletion < 3 sec. concat deletion.
        if self.__current_index > 0:
            op = self.__operations[self.__current_index - 1]
            if (op.type() == Operation.Type.INSERTION_MERGEABLE) and (op.time() + 5 > time.time()):
                start = kwargs.get('start', None)
                end = kwargs.get('end', None)
                text = kwargs.get('text', None)
                # Check if contiguous deletion
                if EDITOR_UNDO_REDO_LOG <= logging.DEBUG:
                    log.debug("op:start={} end={}".format(op.start(), op.end()))
                    log.debug("new:start={} end={}".format(start, end))
                if op.start() == end:
                    # Merge deletion
                    op.set_start(start)
                    op.set_text(text + op.text())
                    return
                elif op.start() == start:
                    # Merge deletion
                    op.set_end(Pos(end.x + 1, end.y))
                    op.set_text(op.text() + text)
                    return

        # Otherwise, create a new char deletion
        self._add_new_op(Operation.Type.INSERTION_MERGEABLE, **kwargs)

    def add_deletion(self, **kwargs):
        """
        Deletion from start to end position.
        to undo text insertion.
        start, end: Pos, Pos
        """
        if EDITOR_UNDO_REDO_LOG <= logging.INFO:
            log.info("Add deletion for undo")
        self._clear_next_op()
        self._add_new_op(Operation.Type.DELETION, **kwargs)

    def add_insertion(self, **kwargs):
        """
        insertion from start to end position
        to undo text deletion
        start, end: Pos, Pos
        text: str the string deleted
        """
        if EDITOR_UNDO_REDO_LOG <= logging.INFO:
            log.info("Add insertion for undo")
        self._clear_next_op()
        self._add_new_op(Operation.Type.INSERTION, **kwargs)

    def get_and_decrement_operation(self):
        """
        Get and decrement current index.
        -> Operation
        """
        op = None
        if self.__current_index > 0:
            op = self.__operations[self.__current_index - 1]
            self.__current_index -= 1
        return op

    def get_and_increment_operation(self):
        """
        Get and increment current index.
        -> Operation
        """
        op = None
        if self.__current_index < len(self.__operations):
            op = self.__operations[self.__current_index]
            self.__current_index += 1
        return op


def main():
    log.debug("--------------")
    log.debug("UndoRedo class test:")
    log.debug("--------------")

    undo_redo = UndoRedo()
    undo_redo.add_deletion(start=Pos(0, 1), end=Pos(1, 2))
    undo_redo.add_char_deletion(start=Pos(0, 1), end=Pos(0, 2))
    undo_redo.add_char_deletion(start=Pos(0, 2), end=Pos(0, 3))
    time.sleep(6)
    undo_redo.add_char_deletion(start=Pos(0, 3), end=Pos(0, 4))

    log.debug("undo_redo:[{}]".format(undo_redo))


if __name__ == "__main__":
    main()
