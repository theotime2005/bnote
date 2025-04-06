"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

# This is a sample Python script.

from enum import Enum
import random

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, MINES_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(MINES_APP_LOG)


class Mines:

    NO_MINE_UNHIDE = 0
    NO_MINE_HIDE = 1
    MINE_UNHIDE = 2
    MINE_HIDE = 3
    MINE_DECLARED = 4

    __display_char = {
        NO_MINE_UNHIDE: "-",
        NO_MINE_HIDE: "*",
        MINE_UNHIDE: "!",
        MINE_HIDE: "*",
        MINE_DECLARED: "x",
    }

    def __init__(self, line, column, mines):
        self._nb_line = line
        self._nb_column = column
        # self.state_table contains the state of each position of tables (see __display_char).
        # self.discovered_table contains the number of each mines proximity.
        self.state_table, self.discovered_table = self.__create_table(
            line, column, mines
        )

    def nb_line(self):
        return self._nb_line

    def nb_column(self):
        return self._nb_column

    def __create_table(self, nb_line, nb_column, mines):
        """

        :param nb_line:
        :param nb_column:
        :param mines:
        :return: state_table, discovered_table
          state_table contains the state of each case of table (see display_char)
          state_discovered contins the value of mine at proximity for each case.
        """
        log.info(f"{nb_line=} {nb_column=} {mines=}")
        table = [[Mines.NO_MINE_HIDE] * nb_column for i in range(nb_line)]
        discovered_table = [[0] * nb_column for i in range(nb_line)]
        # Inject mines.
        cases_number = nb_line * nb_column
        mines_list = [random.randrange(0, cases_number - 1, 1) for i in range(mines)]
        log.info(f"{table}")
        log.info(f"{mines_list=}")
        for mine_pos in mines_list:
            log.info(f"line={int(mine_pos / nb_column)}")
            log.info(f"column={int(mine_pos % nb_column)}")
            table[int(mine_pos / nb_column)][
                int(mine_pos % nb_column)
            ] = Mines.MINE_HIDE
        # Construct discovered table.
        for line in range(0, nb_line):
            for column in range(0, nb_column):
                discovered_table[line][column] = self.__eval_pos(
                    table, line, column, nb_line, nb_column
                )
        return table, discovered_table

    def print_tables(self):
        return "\n".join(
            [
                "-------------------",
                f"state{self.state_table}",
                f"disco{self.discovered_table}",
                "-------------------",
            ]
        )

    @staticmethod
    def __eval_pos(state_table, line, column, nb_line, nb_column):
        counter = 0
        for offset_line in (-1, 0, 1):
            for offset_column in (-1, 0, 1):
                if not (offset_line == 0 and offset_column == 0):
                    pos_line = line + offset_line
                    pos_column = column + offset_column
                    if pos_line in range(0, nb_line) and pos_column in range(
                        0, nb_column
                    ):
                        if state_table[pos_line][pos_column] == Mines.MINE_HIDE:
                            counter += 1
        return counter

    def discovered_all(self):
        """
        Discovered entire game.
        """
        for line in range(0, self._nb_line):
            for column in range(0, self._nb_column):
                if self.state_table[line][column] == Mines.MINE_HIDE:
                    self.state_table[line][column] = Mines.MINE_UNHIDE
                elif self.state_table[line][column] == Mines.NO_MINE_HIDE:
                    self.state_table[line][column] = Mines.NO_MINE_UNHIDE

    def is_all_discovered(self):
        for line in range(0, self._nb_line):
            for column in range(0, self._nb_column):
                if self.state_table[line][column] == Mines.NO_MINE_HIDE:
                    return False
        return True

    def discovered_pos(self, line, column):
        """
        Discovered a position
        :param line: the line in table (0 based)
        :param column: the column in table (0 based)
        :return:
            -1 if pos is a mine
            0 if pos already unhide
            1 if pos is discovered
        """
        if not (
            line in range(0, self._nb_line) and column in range(0, self._nb_column)
        ):
            return 0
        if (
            self.state_table[line][column] == Mines.MINE_HIDE
            or self.state_table[line][column] == Mines.MINE_UNHIDE
        ):
            return -1
        elif self.state_table[line][column] == Mines.NO_MINE_UNHIDE:
            return 0
        elif self.state_table[line][column] == Mines.NO_MINE_HIDE:
            # unhide part
            self.state_table[line][column] = Mines.NO_MINE_UNHIDE
            if self.discovered_table[line][column] == 0:
                self.discovered_pos(line - 1, column - 1)
                self.discovered_pos(line - 1, column)
                self.discovered_pos(line - 1, column + 1)
                self.discovered_pos(line, column - 1)
                self.discovered_pos(line, column + 1)
                self.discovered_pos(line + 1, column - 1)
                self.discovered_pos(line + 1, column)
                self.discovered_pos(line + 1, column + 1)
            return 1

    def bomb_at_pos(self, line, column):
        """
        Mark a bomb.
        :param line: the line in table (0 based)
        :param column: the column in table (0 based)
        :return:
            -1 if is not a mine
            0 if is a mine
        """
        if self.state_table[line][column] == Mines.MINE_HIDE:
            self.state_table[line][column] = Mines.MINE_UNHIDE
            return 0
        else:
            return -1

    def display_line(self, line):
        display_line = ""
        for column in range(0, self._nb_column):
            if (self.state_table[line][column] == Mines.NO_MINE_UNHIDE) and (
                self.discovered_table[line][column] != 0
            ):
                display_line = "".join(
                    [display_line, str(self.discovered_table[line][column])]
                )
            else:
                display_line = "".join(
                    [display_line, Mines.__display_char[self.state_table[line][column]]]
                )
        return display_line


def print_test(name):
    # Use a breakpoint in the code line below to debug your script.
    log.info(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.
    mine = Mines(5, 10, 10)
    print(mine.print_tables())
    mine.discovered_pos(line=1, column=2)
    print(mine.print_tables())
    print(">>>>>>>>>>>>>>>")
    for line in range(0, mine._nb_line):
        log.info(f"Line: <{mine.display_line(line)}>")
    log.info("<<<<<<<<<<<<<<<")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_test("PyCharm")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
