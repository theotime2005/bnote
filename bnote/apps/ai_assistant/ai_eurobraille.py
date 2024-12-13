"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import base64
import ctypes
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Union
import tempfile

from cryptography.fernet import Fernet, InvalidToken
import machineid
import requests

from bnote.tools.singleton_meta import SingletonMeta
from bnote.stm32.braille_device_characteristics import braille_device_characteristics

# Réglage des timout out pour les requêtes faites au serveur eurobraille
CONNECTION_TIMEOUT = 5
READ_TIMEOUT = 10
TIMEOUT = (CONNECTION_TIMEOUT, READ_TIMEOUT)


class AiEurobraille(metaclass=SingletonMeta):
    BASE_URL = "https://api.eurobraille.fr:3003"
    # BASE_URL = "http://192.168.1.31"

    def __init__(self, username="", password="", token=""):
        self.username = username
        self.password = password
        self.token = token
        self.libbnp = None

        if not self.username or not self.password:
            self.create_login()
        if not self.token:
            self.get_token()

    # Send a request to google to check if Internet is available or not
    @staticmethod
    def is_connected_to_internet():
        try:
            requests.get("https://www.google.com", timeout=0.5)
            return True
        except Exception as e:
            # print(f"{e=}")
            return False

    def create_login(self) -> (bool, Union[None, requests.Response]):
        success = False
        try:
            response = requests.post(
                f"{AiEurobraille.BASE_URL}/create_login",
                json={
                    "uuid": machineid.id(),
                    "serial": braille_device_characteristics.get_serial_number(),
                },
                timeout=TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                self.username = data["username"]
                self.password = data["password"]
                success = True

        except requests.exceptions.RequestException as e:
            response = e.response

        return success, response

    def get_token(self) -> (bool, Union[None, requests.Response]):
        success = False
        response = None
        try:
            response = requests.post(
                f"{AiEurobraille.BASE_URL}/login",
                json={"username": self.username, "password": self.password},
                timeout=TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]
                success = True

        except requests.exceptions.RequestException as e:
            response = e.response

        return success, response

    def get_chat_response(self, chat) -> (bool, Union[str, requests.Response]):
        success = False

        # Recover error during user creation caused by invalid bnote date and time.
        if not self.username or not self.password:
            self.create_login()
        if not self.token:
            self.get_token()

        # Appel à l'API AI avec le token
        response = self.call_chat_ai_api(chat)
        if response is not None:
            if response.status_code == 200:
                data = response.json()
                response = data["choices"][0]["message"]["content"]
                success = True

        return success, response

    # call with history
    def call_chat_ai_api(self, chat):
        if self.libbnp is None:
            # Download libbnp.so if needed
            if not Path("/usr/lib/libbnp.so").exists():
                if self.is_connected_to_internet():
                    response = self.download_libbnp()
                    if response.status_code != 200:
                        return response

            self.init_libbnp()

        request_id = b""
        if self.libbnp is not None:
            request_id_ptr = self.libbnp.compute_request_id(
                json.dumps(chat, indent=4).encode("utf-8")
            )
            request_id = ctypes.cast(request_id_ptr, ctypes.c_char_p).value
            self.libbnp.free_c_string(request_id_ptr)

        return requests.post(
            f"{AiEurobraille.BASE_URL}/ai_chat_completions",
            json={"chat": chat},
            headers={
                "Authorization": f"Bearer {self.token}",
                "username": self.username,
                "request_id": request_id.decode("utf-8"),
            },
            timeout=TIMEOUT,
        )

    def download_libbnp(self):
        try:
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_lib_path = Path(tmpdirname) / "libbnp.so"
                response = requests.get(
                    f"{AiEurobraille.BASE_URL}/download", stream=True, timeout=TIMEOUT
                )
                if response.status_code == 200:
                    with open(temp_lib_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                # else:
                #     print(f'Erreur lors du téléchargement du fichier: {response.status_code} - {response.text}')

                command = ["sudo", "mv", temp_lib_path, "/usr/lib/libbnp.so"]
                with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
                    # Wait execution.
                    output, error = process.communicate()
                    # print(f"{output=}")
                    # print(f"{error=}")

            return response
        except requests.exceptions.RequestException as e:
            # print(f"download_libbnp Erreur: {e}")
            raise

    def init_libbnp(self):
        if self.libbnp is None:
            if Path("/usr/lib/libbnp.so").exists():
                # Load the library used to compute the request id, to be able to continue a conversation with ai.
                self.libbnp = ctypes.CDLL("/usr/lib/libbnp.so")

                # Declare functions arg types and restype.
                self.libbnp.free_c_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
                self.libbnp.compute_request_id.restype = ctypes.POINTER(ctypes.c_char)
                self.libbnp.compute_request_id.argtypes = [ctypes.c_char_p]


class AiEurobrailleCrypto(metaclass=SingletonMeta):
    def __init__(self, seed):
        self.seed = seed
        m = hashlib.sha256()
        m.update(
            "-".join(
                (
                    "8b933ca227c63deb1a676cd482832a6292d6d1533dda4fbd3e1d2fd8f422cd40",
                    machineid.id(),
                )
            ).encode("utf-8")
        )
        key = base64.urlsafe_b64encode(m.digest())
        self.__fernet = Fernet(key)

    def encrypt(self, plaintext: str):
        return self.__fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str):
        try:
            return self.__fernet.decrypt(ciphertext).decode("utf-8")
        except InvalidToken:
            return ""
