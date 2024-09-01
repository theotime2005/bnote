"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import json
from json import JSONEncoder
from pathlib import Path
from ast import literal_eval
# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, MINES_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(MINES_APP_LOG)


class Scores:
    SCORES_MAX = 3

    def __init__(self, scores_array=None):
        if scores_array:
            self.scores = scores_array
        else:
            self.scores = []

    def __str__(self):
        text = ""
        for value, name in self.scores:
            text = "".join([text, str(value), "-", name, "\n"])
        return text

    def text_scores(self):
        text = []
        for value, name in self.scores:
            text.append("".join([str(value), "-", name]))

    def is_better_score(self, value):
        """
        check if a new score is better than current scores
        : return: -1 if scores is not better otherwise 0 to n for score order
        """
        order = 0
        # Check if score is greater than value to insert.
        for score_value, score_name in self.scores:
            if value > score_value:
                order += 1
        if order < Scores.SCORES_MAX:
            return order
        else:
            return -1

    def add_score(self, name, value) -> bool:
        """
        add score to the scoreslist.
        :param
         value: The score value
         name: The score name
        :return: False if score could not be added.
        """
        if len(self.scores) < Scores.SCORES_MAX:
            self.scores.append((value, name))
            self.scores.sort(key=lambda t: t[0])
            return True
        # Check if score is greater than value to insert.
        score_value, score_name = self.scores[len(self.scores) - 1]
        if value < score_value:
            self.scores[len(self.scores) - 1] = (value, name)
            self.scores.sort(key=lambda t: t[0])
            return True
        return False

    def scores_list(self):
        """
        : return: string list of score under "value - name"
        """
        scores_list = []
        for score_value, score_name in self.scores:
            scores_list.append("".join([str(score_value), "-", score_name]))
        return scores_list

    def delete(self) -> bool:
        self.scores = []
        return True

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class HighScores:

    def __init__(self, filename):
        self.filename = filename
        # Create default values
        self.data = {'level_1': Scores(), 'level_2': Scores(), 'level_3': Scores()}
        if Path(filename).exists():
            self.__load()

    def __load(self):
        try:
            with open(self.filename, 'r') as json_file:
                data = json_file.read()
        except FileNotFoundError as exception:
            log.error(f"{exception=}")
            data = {}
            pass
        log.info(data)
        data_table = data.split("\nlevel\n")
        log.info(data_table)
        scores_json = json.loads(data_table[1])
        score1 = Scores(literal_eval(scores_json)['scores'])
        self.data['level_1'] = score1
        scores_json = json.loads(data_table[2])
        self.data['level_2'] = Scores(literal_eval(scores_json)['scores'])
        scores_json = json.loads(data_table[3])
        self.data['level_3'] = Scores(literal_eval(scores_json)['scores'])

    def __save(self):
        data_on_disk = None
        # Construct JSON data
        data = ""
        for key, scores in self.data.items():
            level_scores = json.dumps(scores.toJson(), indent=4)
            data = "\nlevel\n".join([data, level_scores])
        log.info(data)
        try:
            with open(self.filename, 'r') as json_file:
                data_on_disk = json.load(json_file)
        except:
            pass
        if data_on_disk == data:
            log.info(f"PAS BESOIN D'USER la SDCARD CAR PAS DE MODIF....")
            return
        log.info(f"Write data on disk")
        with open(self.filename, 'w') as json_file:
            json_file.write(data)

    def delete_score(self, level):
        res = self.data[level].delete()
        self.__after_change(res)

    def is_better_score(self, level, value):
        """
        check if a new score is better than current scores
        : return: -1 if scores is not better otherwise 0 to n for score order
        """
        return self.data[level].is_better_score(value)

    def add_score(self, level, name, value):
        res = self.data[level].add_score(name, value)
        self.__after_change(res)

    def __after_change(self, res):
        if res:
            self.__save()
        return res

    def scores_list(self, level):
        """
        : return: string list of score under "value - name"
        """
        return self.data[level].scores_list()

    def display_scores(self, level):
        if self.data[level] is None:
            return ["empty"]
        else:
            return self.data[level].__str__()


def test():
    filename = ".highscores"
    scores = HighScores(filename)
    # scores.add_score('level_1', 'toto', 10)
    # scores.add_score('level_1', 'titi', 5)
    # scores.add_score('level_1', 'titi', 20)
    # scores.add_score('level_1', 'toto', 8)
    print(scores)

    # scores = Scores()
    # scores.add_score('toto', 10)
    # scores.add_score('titi', 5)
    # scores.add_score('titi', 20)
    # print(scores)
    # scores.add_score('toto', 8)
    # print(scores)
    # scoresJSONData = json.dumps(scores.toJson(), indent=4)
    # print(scoresJSONData)
    # # Let's load it using the load method to check if we can decode it or not.
    # print("Decode JSON formatted Data")
    # scoresJSON = json.loads(scoresJSONData)
    # print(scores)
    # scores_dict = literal_eval(scoresJSON)
    # new_scores = Scores(scores_dict['scores'])
    # print(new_scores)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()
