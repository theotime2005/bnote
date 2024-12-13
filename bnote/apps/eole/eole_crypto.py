"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
import machineid

from bnote.tools.singleton_meta import SingletonMeta

MASTER_KEY = "!onfaitcommeonaditen2024aussi"


# See this article for short explanation of Fernet : https://cryptography.io/en/latest/fernet/
class EoleCrypto(metaclass=SingletonMeta):
    def __init__(self, user_name):
        # Inspiration from class Fernet of cryptography package
        #     def generate_key(cls) -> bytes:
        #         return base64.urlsafe_b64encode(os.urandom(32))
        # The os.random(32) is replaced by the 'hash32' of our cooked master password.

        # see https://docs.python.org/3/library/hashlib.html#usage
        m = hashlib.sha256()
        m.update("-".join((MASTER_KEY, user_name, machineid.id())).encode("utf-8"))
        key = base64.urlsafe_b64encode(m.digest())
        # print(f"{key=}")
        self.__fernet = Fernet(key)

    def encrypt(self, plaintext: str):
        return self.__fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str):
        try:
            return self.__fernet.decrypt(ciphertext).decode("utf-8")
        except InvalidToken:
            return ""


if __name__ == "__main__":

    the_user_name = "eurobraille_user1"
    print()
    print(f"{the_user_name=}")
    the_ciphertext = EoleCrypto(the_user_name).encrypt("hello world")
    print(f"{the_ciphertext=}")
    the_plaintext = EoleCrypto(the_user_name).decrypt(the_ciphertext)
    print(f"{the_plaintext=}")

    the_user_name = "toto"
    print()
    print(f"{the_user_name=}")
    the_ciphertext = EoleCrypto(the_user_name).encrypt("hello world")
    print(f"{the_ciphertext=}")
    the_plaintext = EoleCrypto(the_user_name).decrypt(the_ciphertext)
    print(f"{the_plaintext=}")

    the_user_name = "bob"
    print()
    print(f"{the_user_name=}")
    the_ciphertext = EoleCrypto(the_user_name).encrypt("hello world")
    print(f"{the_ciphertext=}")
    the_plaintext = EoleCrypto(the_user_name).decrypt(the_ciphertext)
    print(f"{the_plaintext=}")

    the_user_name = "alice"
    print()
    print(f"{the_user_name=}")
    the_ciphertext = EoleCrypto(the_user_name).encrypt("hello world")
    print(f"{the_ciphertext=}")
    the_plaintext = EoleCrypto(the_user_name).decrypt(the_ciphertext)
    print(f"{the_plaintext=}")
