"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json

import requests
from requests_oauthlib import OAuth2Session

from bnote.apps.eole.eole_access_token import EoleAccessToken
from bnote.tools.singleton_meta import SingletonMeta

NOT_A_VALID_ACCESS_TOKEN = "not_a_valid_access_token"

# "Process finished with exit code 137" : https://python-forum.io/thread-36967.html
# To solve "Process finished with exit code 137" when downloaded big files, the swap file size must be increase.
# See how to do it on page : https://siebert.ovh/gnu_linux:raspberry:augmenter_la_taille_du_swap_sur_le_raspberry_pi
# Seems to be ok with a “CONF_SWAPSIZE=500”

# Réglage des timout out pour les requêtes faites à Eole (pour éviter les blocages quand Internet non accessible)
# 0.5 seconde est une valeur recommandée pour ne pas bloquer l'utilisateur trop longtemps
# quand le site n'est pas accessible (ou qu'il n'y a pas de connection Internet disponible)
CONNECTION_TIMEOUT = 0.5
READ_TIMEOUT = 5
TIMEOUT = (CONNECTION_TIMEOUT, READ_TIMEOUT)


class EoleApi(metaclass=SingletonMeta):
    """
    This class implement the acces to the eole library.

    Methods
    -------
        def __init__(self, user_name, password, url_api="https://eole.avh.asso.fr/api/v1"):

        def set_user(self, user_name, password) -> bool:
            Update the user_name and password. Cleanup all data associated to a previous user_name / password.

        def has_valid_token_access(self) -> bool:
            Return true if we have valid token access.

        def search(self, search=None, genre=None, author=None, title=None, age_range=None, isbn=None, created_at_after=None,
               created_at_before=None, updated_at_after=None, updated_at_before=None, dewey=None, original_language=None,
               language=None, description=None, editor=None, notice_id=None, adaptation=None, support=None, duration_after=None,
               duration_before=None, auto_build_the_list=True, max_items=100) -> {}:

               Return a dictionary with the result of the search.

       def download(self, file_name) -> (bool, str)

    """

    def __init__(self, url_api="https://eole.avh.asso.fr/api/v1"):
        self.__url_api = url_api
        self.__eole_access_token = None
        self.__token = {
            "access_token": NOT_A_VALID_ACCESS_TOKEN,
            "token_type": "Bearer",
        }
        # Instanciate an OAuth2Session without token to give earlier access to API that do not need authentication.
        # No need to be authenticated to call get_genre()
        self.__session = OAuth2Session()

    def set_url_api(self, url_api):
        self.__url_api = url_api

    def set_access_token(self, access_token):
        self.__token["access_token"] = access_token
        self.__session = OAuth2Session(token=self.__token)
        # print(f"{self.__session.headers=}")

    def access_token(self):
        return self.__token["access_token"]

    def init_access_token_from_user_password(self, user_name, password) -> (bool, str):
        self.__token["access_token"] = NOT_A_VALID_ACCESS_TOKEN
        if self.__eole_access_token is None:
            self.__eole_access_token = EoleAccessToken(
                user_name, password, url_api=self.__url_api
            )
        else:
            self.__eole_access_token.set_user(user_name, password)
        access_token, error_success_message = (
            self.__eole_access_token.acquire_access_token()
        )
        if access_token:
            self.__token["access_token"] = access_token
            self.__session = OAuth2Session(token=self.__token)
        return self.__eole_access_token.has_valid_token_access(), error_success_message

    def has_valid_token_access(self) -> bool:
        if self.__token["access_token"] != NOT_A_VALID_ACCESS_TOKEN:
            return True
        if self.__eole_access_token:
            return self.__eole_access_token.has_valid_token_access()
        return False

    def download(self, url_name, file_name) -> (bool, str):
        # print(f"Downloading {url_name=}")
        # print(f"{file_name=}")
        # print(f"Please wait : FIXME => Ajouter un compteur de téléchargement...")
        if self.has_valid_token_access():
            response = self.__session.get(url_name, timeout=TIMEOUT)
            # print(f"{response.status_code=}")
            if response.status_code == 200:
                try:
                    with open(file_name, "wb") as my_file:
                        my_file.write(response.content)
                    return True, ""
                except IOError as e:
                    print(f"{e.strerror=}")
                    return False, e.strerror
                    pass
            else:
                # print(f"{response.content=}")
                return False, "server response = {} - {]".format(
                    response.status_code, response.content.decode("utf-8")
                )

        return False, NOT_A_VALID_ACCESS_TOKEN

    # Used for the first try
    # eole_api.get("https://eole.avh.asso.fr/api/v1/my_history")
    def get(self, url, **kwargs):
        return self.__session.get(url, **kwargs)

    # FIXME : A compléter
    def my_history(self) -> dict:
        if self.has_valid_token_access():
            response = self.__session.get(
                "/".join((self.__url_api, "my_history")), timeout=TIMEOUT
            )
            print(f"{response.status_code=}")
            response_dict = response.json()
            print(f"{response_dict=}")
            return response_dict

        return dict()

    # Implementation of :
    # https://eole.avh.asso.fr/sites/all/modules/custom/avh_api_opds/swagger/dist/index.html#/Recherche/get_api_v1_search
    def search(
        self,
        search=None,
        genre=None,
        author=None,
        title=None,
        age_range=None,
        isbn=None,
        created_at_after=None,
        created_at_before=None,
        updated_at_after=None,
        updated_at_before=None,
        dewey=None,
        original_language=None,
        language=None,
        description=None,
        editor=None,
        notice_id=None,
        adaptation=None,
        support=None,
        duration_after=None,
        duration_before=None,
        auto_build_the_list=True,
        max_items=100,
    ) -> {}:
        # Suite aux essais sur l'API EOLE, le champ search masque les champs author et title. Ce qui est normal car
        # le champ search correspond à une recherche sur les champs titre et auteur d'un livre.
        params = {}
        if search:  # not None and not empty
            params.update({"search": search})
        else:
            if author:  # not None and not empty
                params.update({"author": author})
            if title:  # not None and not empty
                params.update({"title": title})

        extra_params = {
            "genre": genre,
            "ageRange": age_range,
            "isbn": isbn,
            "createdAt[after]": created_at_after,
            "createdAt[before]": created_at_before,
            "updatedAt[after]": updated_at_after,
            "updatedAt[before]": updated_at_before,
            "dewey": dewey,
            "originalLanguage": original_language,
            "language": language,
            "description": description,
            "editor": editor,
            "noticeId": notice_id,
            "adaptation": adaptation,
            "support": support,
            "duration[after]": duration_after,
            "duration[before]": duration_before,
        }

        # Create the filtered_extra_params with {key: value} of extra_params where value is not None or empty.
        filtered_extra_params = dict()
        for key, value in extra_params.items():
            if value:  # not None and not empty
                filtered_extra_params[key] = value

        # Add the filtered_extra_params to params
        params.update(filtered_extra_params)
        # print(f'{params=}')

        # Call the search API
        response = self.__session.get(
            "/".join((self.__url_api, "search")), timeout=TIMEOUT, params=params
        )
        # print(f"{response.status_code=}")
        # print(f"{response.content=}")

        response_dict = response.json()

        if response.status_code == 200:
            if auto_build_the_list:
                if (
                    "metadata" in response_dict
                    and "numberOfItems" in response_dict["metadata"]
                ):
                    numbers_of_items = response_dict["metadata"]["numberOfItems"]
                    # print(f"Found {response_dict['metadata']['numberOfItems']}")
                    if 0 < numbers_of_items <= max_items:
                        # Call the recursive method ONLY if less than max_items result
                        # Do NOT try to get all items. There is more than 70000 publications (70000 books) and the time
                        # that will cause to do 70000 / 3 = 23333 requests (3 publications are returned per request)
                        publications = self.__extract_items(
                            "publications", response_dict
                        )
                        # print(f"{publications=}")
                        response_dict = {
                            "metadata": response_dict["metadata"],
                            "publications": publications,
                        }

        return response_dict

    # Recursive method to grab a list of items with multiple requests (3 items are returned per request).
    # items_name can be 'publications' when call by search()
    # items_name can be 'navigation' when call by get_genre()
    def __extract_items(self, items_name, response_dict) -> []:
        items = []
        if items_name in response_dict:
            items = response_dict[items_name]

        if "links" in response_dict:
            next_url = None
            for link in response_dict["links"]:
                if link["rel"] == "next":
                    next_url = link["href"]

            if next_url is not None:
                resp = self.__session.get(next_url, timeout=TIMEOUT)
                if resp.status_code == 200:
                    resp_dict = resp.json()
                    items.extend(self.__extract_items(items_name, resp_dict))

        return items

    def get_genre(self) -> {}:
        # Call the genre API
        response = self.__session.get(
            "/".join((self.__url_api, "choix-genre-moteur-de-recherche/genre")),
            timeout=TIMEOUT,
        )
        # print(f"{response.status_code=}")
        # print(f"{response.content=}")

        response_dict = response.json()

        if response.status_code == 200:
            if (
                "metadata" in response_dict
                and "numberOfItems" in response_dict["metadata"]
            ):
                numbers_of_items = response_dict["metadata"]["numberOfItems"]
                # print(f"Found {response_dict['metadata']['numberOfItems']}")
                if 0 < numbers_of_items:
                    # Call the recursive method to grab known genres
                    navigations = self.__extract_items("navigation", response_dict)
                    # print(f"{publications=}")
                    return {
                        "metadata": response_dict["metadata"],
                        "genres": navigations,
                    }

        return response_dict

    @staticmethod
    def save_genre(filename, response_dict):
        data_on_disk = None
        try:
            with open(filename, "r") as json_file:
                data_on_disk = json.load(json_file)
        except Exception as e:
            # print(f"LOAD {e=}")
            pass
        finally:
            # If nothing change, it's not usefull to rewrite the file.
            if data_on_disk == response_dict:
                return
            try:
                # Write the response dict with genre info
                with open(filename, "w") as json_file:
                    json.dump(response_dict, json_file, indent=4)
            except Exception as e:
                # print(f"DUMP {e=}")
                pass
            finally:
                pass

    @staticmethod
    def load_genre(filename) -> dict:
        response_dict = dict()
        try:
            with open(filename, "r") as json_file:
                response_dict = json.load(json_file)
        finally:
            return response_dict

    # Send a request to google to check if Internet is available or not
    @staticmethod
    def is_connected_to_internet():
        try:
            requests.get("https://www.google.com", timeout=0.5)
            return True
        except Exception as e:
            # print(f"{e=}")
            return False


if __name__ == "__main__":
    if EoleApi().is_connected_to_internet():
        print("Vous êtes connecté à Internet.")
    else:
        print("Vous n'êtes pas connecté à Internet.")

    the_user_name = "eurobraille_user1"
    the_password = "fake_password"

    # Init via access_token
    EoleApi().set_access_token("fake_access_token")

    # or init via login / password (to retrieve automatically the access_token)
    # EoleApi().init_access_token_from_user_password(the_user_name, the_password)

    # the_response = eole_api.get("https://eole.avh.asso.fr/api/v1/my_history")
    # the_response = EoleApi().my_history()
    # if the_response:
    #     response_json = the_response.json()
    #     print(f"{the_response.status_code=}")
    #     print(f"{response_json=}")

    # result = EoleApi().search(search="asimov", max_items=5)
    result = EoleApi().search(search="kundera", max_items=5)

    if "publications" in result:
        number_of_items = len(result["publications"])
        print(f"{number_of_items=}")
        # Download the first publication found...
        wanted_publication = result["publications"][0]
        print(f"{wanted_publication=}")
        for link in wanted_publication["links"]:
            print(f"{link=}")
            if "type" in link and link["type"] == "application/zip":
                # the_response = eole_api.get(link['href'])
                # print(f"{the_response.status_code=}")
                # if the_response.status_code == 200:
                #     open('mon_troisième_livre.zip', 'wb').write(the_response.content)
                # else:
                #     print(f"{the_response.content=}")
                success, message = EoleApi().download(
                    link["href"], wanted_publication["metadata"]["archive"]
                )
                print(f"{success=} {message=}")

    # the_response = eole_api.get("https://eole.avh.asso.fr/api/v1/my_history")
    the_response = EoleApi().my_history()
    print(f"{the_response=}")
