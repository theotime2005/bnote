"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from random import randint
from pathlib import Path


class WriteWord:
    def __init__(self, app_folder, language):
        self.name = Path(app_folder / Path("lex_{}.ww".format(language)))
        self.lst_word = []
        self.language = language

    def load_file(self, letter=[], size=0):
        filename = self.name
        if not filename.exists():
            return False
        f = open(filename, "r", encoding="utf-8")
        for line in f:
            if len(line[:-1]) < int(size / 2) - 1:
                if letter and self.verify(line[:-1], letter):
                    self.lst_word.append(line[:-1])
                elif not letter:
                    self.lst_word.append(line[:-1])
        return True

    def verify(self, word, letter) -> bool:
        for c in word:
            if not c in letter:
                return False
        return True

    def give_file(self):
        return self.lst_word[randint(0, len(self.lst_word)) - 1]

    def import_file(self, file_name, replace=False):
        file_importing = open(file_name, "r", encoding="utf-8")
        filename = self.name
        if replace or not filename.exists():
            file_original = open(filename, "w", encoding="utf-8")
        else:
            file_original = open(filename, "a", encoding="utf-8")
        for line in file_importing:
            if line[-1] == "\n":
                line = line[:-1]
            if replace or not line in file_original:
                file_original.write("{}\n".format(line))
        return True
