"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import json
import os

HOME_PATH = "/home/pi/.bnote/braille_learning"
if not os.path.exists(HOME_PATH):
    os.mkdir(HOME_PATH)


def create_file(name):
    f = open(name, "w")
    f.close()


class ManageLevel:
    def __init__(self):
        self.file_name = "{}/level_save.txt".format(HOME_PATH)
        self.data_level = dict()
        self.load_file()

    def load_file(self):
        try:
            with open(self.file_name, "r") as file:
                self.data_level = json.load(file)
        except FileNotFoundError:
            create_file(self.file_name)
        except json.JSONDecodeError:
            create_file(self.file_name)

    def save_file(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data_level, file, indent=4)

    def add_level(self, app, level):
        self.data_level.update({app: level})
        self.save_file()

    def get_level(self, app):
        if self.data_level.get(app) != None:
            return self.data_level[app]
        return False

    def delete_app(self, app):
        if self.data_level.get(app) != None:
            del self.data_level[app]
            self.save_file()


class ManageScore:
    def __init__(self):
        self.file_name = "{}/level_score.txt".format(HOME_PATH)
        self.data_score = dict()
        self.load_file()

    def load_file(self):
        try:
            with open(self.file_name, "r") as file:
                self.data_score = json.load(file)
        except FileNotFoundError:
            create_file(self.file_name)
        except json.JSONDecodeError:
            create_file(self.file_name)

    def save_file(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data_score, file, indent=4)

    def add_score(self, app, level, score):
        if self.data_score.get(app) != None:
            self.data_score[app].update({level: score})
        else:
            self.data_score[app] = {level: score}
        self.save_file()

    def get_score_level(self, app, level):
        if self.data_score.get(app) and self.data_score[app].get(level):
            return self.data_score[app][level]
        return False

    def delete_score(self, app, level):
        if self.data_score.get(app) != None and self.data_score[app].get(level) != None:
            del self.data_score[app][level]
            self.save_file()

    def delete_app(self, app):
        if self.data_score.get(app) != None:
            # print("suppression")
            del self.data_score[app]
            self.save_file()
