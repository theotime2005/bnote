"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json
from pathlib import Path
from random import randint


class Operation:
    def __init__(self, app_folder):
        self.name = app_folder / Path("tables.ope")
        self.expression = ""
        self.lst_expression = {}

    def load_file(self, table=""):
        if not Path(self.name).exists():
            return False
        with open(self.name, "r") as file:
            expressions = json.load(file)
        if table:
            self.lst_expression = expressions[table]
        else:
            for t in expressions:
                self.lst_expression.update(expressions[t])
        return True

    def get_expression(self):
        number = randint(0, len(self.lst_expression) - 1)
        self.expression = list(self.lst_expression.keys())[number]
        return self.expression

    def test_expression(self, result) -> bool:
        if self.lst_expression[self.expression] == result:
            rls = True
        else:
            rls = False
        return rls

    def get_list_tables(self):
        with open(self.name, "r") as file:
            tables = json.load(file)
        return list(tables.keys())

    def import_file(self, name, replace=False):
        file_importing = open(name, "r", encoding="utf-8")
        if replace:
            file_original = open(self.name, "w", encoding="utf-8")
        else:
            file_original = open(self.name, "a", encoding="utf-8")
        for line in file_importing:
            file_original.write(line)
        file_original.close()
        file_importing.close()
