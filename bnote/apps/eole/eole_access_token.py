"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import base64
from typing import Optional

import requests
from requests import Response

# Réglage des timout out pour les requêtes faites à Eole (pour éviter les blocages quand Internet non accessible)
# 0.5 seconde est une valeur recommandée pour ne pas bloquer l'utilisateur trop longtemps
# quand le site n'est pas accessible (ou qu'il n'y a pas de connection Internet disponible)
CONNECTION_TIMEOUT = 0.5
READ_TIMEOUT = 5
TIMEOUT = (CONNECTION_TIMEOUT, READ_TIMEOUT)


class EoleAccessToken:
    """
    This class implements the retrieval of an OAuth2 authentification token for devices that do not have a web browser.

    ...

    Attributes
    ----------
    user_name : str
        the user_name used to sign in
    password : str
        the password used to sign in
    url_api : str
        url of the eole api
    token_access : str
        the access token that we want to get

    Methods
    -------
    def set_user(self, user_name, password):
        Update the user_name and password. Cleanup all data associated to a previous user_name / password.

    def has_valid_token_access(self) -> bool:
        Return true if we have valid token access.

    def acquire_access_token(self) -> Optional[str]:
        Acquire the access token for a user_name and password.
        The Access Token is obtained by implementing Part VIII "Acquire an access from devices without browser"
        of the document "ÉOLE API Usage guide V1.4 - Eurobraille.docx
        return the access token or None.

    def get_access_token(self) -> Optional[str]:
        Return the access token associated to this device or None.
    """

    def __init__(self, user_name, password, url_api="https://eole.avh.asso.fr/api/v1",
                 device_code_path="device/code", device_token_path="device/token"):
        self.__user_name = user_name
        self.__password = password
        self.__url_api = url_api
        self.__device_code_path = device_code_path
        self.__device_token_path = device_token_path
        # These following datas must be clear if self.__user_name / self.__password change
        self.__client_id = base64.b64encode(self.__user_name.encode('utf-8')).decode('utf-8')
        self.__device_code = None
        self.__user_code = None
        self.__verification_uri = None
        self.__expire_in = 0
        self.__interval = 0
        self.__auth_uri = None
        self.__sign_in_successfully = False
        self.__token_access = None

    def __cleanup_data(self):
        # These data must be clear if self.__user_name / self.__password change
        self.__client_id = None
        self.__device_code = None
        self.__user_code = None
        self.__verification_uri = None
        self.__expire_in = 0
        self.__interval = 0
        self.__auth_uri = None
        self.__sign_in_successfully = False
        self.__token_access = None

    def has_valid_token_access(self) -> bool:
        if self.__token_access is None:
            return False
        # print(f"token is valid : {self.__token_access=}")
        return True

    def get_access_token(self) -> Optional[str]:
        return self.__token_access

    def set_user(self, user_name, password):
        self.__user_name = user_name
        self.__password = password
        # cleanup the datas related to the user_name / password
        self.__cleanup_data()
        # Compute self.__client_id from self.__user_name
        self.__client_id = base64.b64encode(self.__user_name.encode('utf-8')).decode('utf-8')

    def acquire_access_token(self) -> (Optional[str], str):
        error_message = "OK"
        # print(f">> acquire_access_token() :")
        # cleanup the datas related to the user_name / password
        self.__cleanup_data()
        # Compute self.__client_id from self.__user_name
        self.__client_id = base64.b64encode(self.__user_name.encode('utf-8')).decode('utf-8')

        try:
            # Start the exchange to get the Access Token by implementing
            # Part VIII "Acquire an access from devices without browser" of the document
            # "ÉOLE API Usage guide V1.4 - Eurobraille.docx"
            response = self.__get_verification_uri()
            if response and response.status_code == 200:
                response = self.__get_auth_uri()
                if response and response.status_code == 200:
                    response = self.__sign_in()
                    if response and response.status_code == 200 and self.__sign_in_successfully:
                        self.__token_access, error_message = self.__get_token_access()
        except Exception as e:
            print(f"acquire_access_token() => {e=}")
            error_message = e
            self.__cleanup_data()

        return self.__token_access, error_message

    def __get_verification_uri(self) -> Optional[Response]:
        """__get_verification_uri():
        Implement the step 3 of the doc (get a verification_uri, a device_code and a user_code).
        """
        # print(f">> __get_verification_uri() :")
        if self.__url_api and self.__device_code_path and self.__client_id:
            # client_id must be the b64 encoding of the user_name.
            params = {"client_id": f"{self.__client_id}"}
            # print(f"{params=}")
            # default url is "https://eole.avh.asso.fr/api/v1/device/code"
            response = requests.get("/".join((self.__url_api, self.__device_code_path)), timeout=TIMEOUT, params=params)
            response_json = response.json()
            # print(f"{response.status_code=}")
            # print(f"{response_json=}")
            if response.status_code == 200:
                if 'access' in response_json and response_json['access'] == 'TRUE':
                    if 'data' in response_json:
                        if 'device_code' in response_json['data']:
                            self.__device_code = response_json['data']['device_code']
                        if 'user_code' in response_json['data']:
                            self.__user_code = response_json['data']['user_code']
                        if 'verification_uri' in response_json['data']:
                            self.__verification_uri = response_json['data']['verification_uri']
                        if 'expire_in' in response_json['data']:
                            self.__expire_in = response_json['data']['expire_in']
                        if 'interval' in response_json['data']:
                            self.__interval = response_json['data']['interval']
            return response
        # print("__get_verification_uri returns None")
        return None

    def __get_auth_uri(self) -> Optional[Response]:
        """__get_auth_uri():
        Implement step 4 of the doc (get an auth_uri)
        """
        # print(f">> __get_auth_uri() :")
        if self.__verification_uri:
            response = requests.get(self.__verification_uri, timeout=TIMEOUT)
            response_json = response.json()
            # print(f"{response.status_code=}")
            # print(f"{response_json=}")
            if response.status_code == 200:
                if 'auth_uri' in response_json:
                    self.__auth_uri = response_json['auth_uri']
            return response
        # print("__get_auth_uri returns None")
        return None

    def __sign_in(self) -> Optional[Response]:
        """__sign_in():
        Implement step 5 of the doc (Sign in using username and password)
        """
        # print(f">> __sign_in() :")
        if self.__auth_uri:
            data = {'username': f"{self.__user_name}", 'password': f"{self.__password}"}
            # print(f"{data=}")
            response = requests.post(self.__auth_uri, timeout=TIMEOUT, data=data)
            response_json = response.json()
            # print(f"{response.status_code=}")
            # print(f"{response_json=}")
            if 'access' in response_json:
                if response_json['access'] == 'TRUE':
                    self.__sign_in_successfully = True
            return response
        # print("__sign_in returns None")
        return None

    def __get_token_access(self) -> (Optional[str], str):
        """__get_token_access():
        Implement step 6 of the doc (Call the OPDS flux and get the token_access)
        """
        error_success_message = "OK"
        # print(f">> __get_token_access() :")
        if self.__sign_in_successfully and self.__url_api and self.__device_token_path:
            params = {'client_id': f"{self.__client_id}", 'device_code': f"{self.__device_code}",
                      'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}
            # default url is 'https://eole.avh.asso.fr/api/v1/device/token'
            response = requests.get('/'.join((self.__url_api, self.__device_token_path)), timeout=TIMEOUT,
                                    params=params)
            response_json = response.json()
            # print(f"{response.status_code=}")
            # print(f"{response_json=}")
            if 'token_access' in response_json:
                self.__token_access = response_json['token_access']
                # print(f"{self.__token_access=}")
            elif 'error' in response_json:
                error_success_message = response_json['error']

            return self.__token_access, error_success_message
        # print("__get_token_access returns None")
        return None, "Error in step 6"


if __name__ == '__main__':
    the_user_name = 'eurobraille_user1'
    the_password = 'fake_password'

    print(f"eole_access_token = EoleAccessToken({the_user_name=}, {the_password=})")
    eole_access_token = EoleAccessToken(user_name=the_user_name, password=the_password)

    access_token = eole_access_token.acquire_access_token()
    print(f"{access_token=}")
