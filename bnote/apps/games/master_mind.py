"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import random
from bnote.apps.bnote_app import BnoteApp

from bnote.debug.colored_log import ColoredLogger, MASTERMIND_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(MASTERMIND_APP_LOG)


class MasterMind(BnoteApp):
    __color_char = [1, 2, 3, 4, 5, 6]

    def __init__(self, token, is_duplicate):
        self.__nb_tokens = token
        self._tokens_to_find = self.__create_game(token, is_duplicate)
        log.error(f"{self._tokens_to_find=}")

    def nb_tokens(self):
        return self.__nb_tokens

    def tokens_to_find(self):
        return self._tokens_to_find

    @staticmethod
    def __create_game(token, is_duplicate):
        token_to_find = []
        if is_duplicate:
            token_to_find = [
                random.randrange(MasterMind.__color_char[0],
                                 MasterMind.__color_char[len(MasterMind.__color_char) - 1], 1) for i in range(token)]
        else:
            while len(token_to_find) < token:
                new_token = random.randrange(MasterMind.__color_char[0],
                                             MasterMind.__color_char[len(MasterMind.__color_char) - 1] + 1)
                if not (new_token in token_to_find):
                    token_to_find.append(new_token)
        return token_to_find

    def check_tokens(self, tokens):
        if tokens is None:
            return False
        if len(tokens) != self.__nb_tokens:
            return False
        for token in tokens:
            if not (token in MasterMind.__color_char):
                return False
        return True

    def check_proposition(self, tokens) -> (int, int):
        """
        :param: tokens []
        :return : (in position, exist)
        """
        tokens_in_position = 0
        tokens_exist = 0
        for index, token in enumerate(self._tokens_to_find):
            if tokens[index] == token:
                tokens_in_position += 1
        # Duplicate array
        tokens_to_check = self._tokens_to_find[0: len(self._tokens_to_find)]
        for index, token in enumerate(tokens):
            if token in tokens_to_check:
                tokens_exist += 1
                tokens_to_check.remove(token)
        return tokens_in_position, tokens_exist

    def display_proposition(self, tokens):
        data = ""
        for token in tokens:
            data = "".join([data, str(token)])
        tokens_in_position, tokens_exist = self.check_proposition(tokens)
        res = f"{tokens_in_position}/{tokens_exist}"
        data = " ".join([data, res])
        return data


def print_test():
    mastermind = MasterMind(4, True)
    print(f"{mastermind._tokens_to_find=}")
    mastermind = MasterMind(4, False)
    print(f"{mastermind._tokens_to_find=}")
    mastermind._tokens_to_find = [1, 0, 0, 2]
    print(f"{mastermind.check_tokens([])=}")
    print(f"{mastermind.check_tokens([1])=}")
    print(f"{mastermind.check_tokens([1, 2, 3, 4])=}")
    proposition = [0, 0, 3, 2]
    print(f"{mastermind._tokens_to_find=}")
    print(f"{proposition=}")
    tokens_in_position, tokens_exist = mastermind.check_proposition(proposition)
    print(f"{tokens_in_position}/{tokens_exist}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_test()
