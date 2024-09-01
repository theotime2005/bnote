"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from collections import OrderedDict
from pathlib import Path

import requests

import bnote.ui as ui
from bnote.apps.eole.eole_api import EoleApi
from bnote.apps.fman.file_manager import BNOTE_FOLDER

# Nombre de publications qui vont être récupérées pour construire la ui.UiListBox avec les résultats.
# Ne pas mettre une valeur trop élevée (car on ne récupère que 3 publications par requête)
MAX_PUBLICATION_COUNT = 100

# The genre file is located in the home() folder, thus it is not deleted by software update.
GENRE_FILE = BNOTE_FOLDER / Path("genre.json")


class EoleSearchDialogBox(ui.UiDialogBox):
    def __init__(self, is_eole_simplified_search, exec_show_summary, exec_download, exec_display_error_dialog,
                 exec_cancel_eole_dialog):
        self.__is_eole_simplified_search = is_eole_simplified_search
        self._exec_display_error_dialog = exec_display_error_dialog
        self._support_value = OrderedDict([
            (_("Human voice and Full daisy (braille + synthesis voice)"), ""),
            (_("Human voice only"), "1"),
            (_("Full daisy (braille + synthesis voice)"), "2")
        ])

        self._age = OrderedDict([
            (_("All"), ""),
            (_("Adult"), "adulte"),
            (_("0 to 4 years"), "0 à 4 ans"),
            (_("5 to 8 years"), "5 à 8 ans"),
            (_("9 to 12 years"), "9 à 12 ans"),
            (_("13 years and over"), "13 ans et plus"),
        ])

        self._genre = self._build_genre_dict()

        self._result = OrderedDict()
        # This ui list box will be updated, once the search button is pressed.
        self._result_listbox = ui.UiListBox(name=_("result"), value=("result", list(self._result.keys())))

        if self.__is_eole_simplified_search:
            item_list = [
                ui.UiListBox(name=_("support"), value=("support", list(self._support_value.keys()))),
                ui.UiEditBox(name=_("search for authors, titles and abstracts"), value=("search", "")),
                ui.UiButton(name=_("&search"), action=self._exec_search, is_auto_close=False),
                self._result_listbox,
                ui.UiButton(name=_("&summary"), action=exec_show_summary, is_auto_close=False),
                ui.UiButton(name=_("&download"), action=exec_download, is_auto_close=False),
                ui.UiButton(name=_("&close"), action=exec_cancel_eole_dialog)
            ]
            pass
        else:
            item_list = [
                ui.UiListBox(name=_("support"), value=("support", list(self._support_value.keys()))),
                ui.UiEditBox(name=_("title"), value=("title", "")),
                ui.UiEditBox(name=_("author"), value=("author", "")),
                ui.UiEditBox(name=_("editor"), value=("editor", "")),
                ui.UiEditBox(name=_("summary"), value=("summary", "")),

                ui.UiListBox(name=_("genre"), value=("genre", list(self._genre.keys()))),
                ui.UiListBox(name=_("age"), value=("age", list(self._age.keys()))),
                ui.UiButton(name=_("&search"), action=self._exec_search, is_auto_close=False),
                self._result_listbox,
                ui.UiButton(name=_("&summary"), action=exec_show_summary, is_auto_close=False),
                ui.UiButton(name=_("&download"), action=exec_download, is_auto_close=False),
                ui.UiButton(name=_("&close"), action=exec_cancel_eole_dialog)
            ]

        kwargs = {
            'name': _("Eole"),
            "item_list": item_list,
            "action_cancelable": exec_cancel_eole_dialog,
        }
        super().__init__(**kwargs)

    @staticmethod
    def _build_genre_dict():
        # Load the genre dict from file to speed up the display of the dialog box
        # (EoleApi().get_genre() takes 5 around secondes)
        result = EoleApi().load_genre(GENRE_FILE)
        if len(result) == 0:
            try:
                # Get the genre from the eole server (takes around 5 secondes)
                result = EoleApi().get_genre()
                # Save the genre response in a json file.
                EoleApi().save_genre(GENRE_FILE, result)
            except Exception as e:
                pass

        genre = OrderedDict([(_("All"), "")])

        if 'genres' in result:
            number_of_items = len(result['genres'])
            for i in range(number_of_items):
                title = str(result['genres'][i]['title'])
                genre[title] = title

        genre = OrderedDict(sorted(genre.items(), key=lambda t: t[1]))
        genre.move_to_end(_("All"), last=False)
        return genre

    def _exec_search(self):
        search, genre, author, title, age_range, support, editor, description = None, None, None, None, None, None, None, None

        values = self.get_values()

        if 'search' in values:
            search = values['search']
        if 'genre' in values:
            genre = self._genre[values['genre']]
        if 'author' in values:
            author = values['author']
        if 'title' in values:
            title = values['title']
        if 'age' in values:
            age_range = self._age[values['age']]
        if 'support' in values:
            support = self._support_value[values['support']]
        if 'editor' in values:
            editor = values['editor']
        if 'summary' in values:
            description = values['summary']

        error_message = None
        result = dict
        try:
            result = EoleApi().search(search=search, support=support, genre=genre, author=author, title=title,
                                      age_range=age_range, editor=editor, description=description,
                                      max_items=MAX_PUBLICATION_COUNT)
        except requests.exceptions.ReadTimeout as e:
            if EoleApi().is_connected_to_internet():
                error_message = _("eole library is unavailable...")
            else:
                error_message = _("no internet...")

            pass
        except Exception as e:
            print(f"{e=}")
            error_message = _("unexpected error ({})".format(str(e)))
            pass

        # Empty previous search result
        self._result = OrderedDict()
        publication_count = 0

        if error_message is not None:
            # Update the result list values
            self._result_listbox.set_list(list(self._result.keys()), 0)
            # Display the error message.
            self._exec_display_error_dialog(error_message=error_message)
            pass
        else:
            if 'metadata' in result and 'numberOfItems' in result['metadata']:
                publication_count = result['metadata']['numberOfItems']
            if publication_count > MAX_PUBLICATION_COUNT:
                message = _("to many result (found {} and maxi is {})".format(publication_count, MAX_PUBLICATION_COUNT))
                self._result[message] = ""
            elif publication_count == 0:
                message = _("no results...")
                self._result[message] = ""
            elif 'publications' in result:
                number_of_items = len(result['publications'])
                # print(f"{number_of_items=}")
                if number_of_items <= MAX_PUBLICATION_COUNT:
                    for i in range(number_of_items):
                        title = str(result['publications'][i]['metadata']['title'])
                        author = str(result['publications'][i]['metadata']['author'])
                        message = " | ".join((title, author))
                        self._result[message] = result['publications'][i]

            # print(f"{self._result.keys()=}")
            # Update the result list values
            self._result_listbox.set_list(list(self._result.keys()), 0)
            # Set the focus to the result (easier for user to see that the result change)
            self.set_focus(self._result_listbox)

    def get_summary(self):
        values = self.get_values()
        current_data = dict()
        if 'result' in values and values['result'] in self._result:
            current_data = self._result[values['result']]
        # print(f'get_summary() : {current_data=}')
        if 'metadata' in current_data and 'description' in current_data['metadata']:
            return current_data['metadata']['description']

        return None

    def get_download_info(self):
        url_name, file_name = (None, None)
        values = self.get_values()
        current_data = dict()
        if 'result' in values and values['result'] in self._result:
            current_data = self._result[values['result']]
        if 'links' in current_data:
            for link in current_data['links']:
                # print(f"{link=}")
                # print(f"{current_data['metadata']=}")
                # print(f"{current_data['metadata']['archive']=}")
                if 'type' in link and link['type'] == "application/zip":
                    # print(f"{current_data['metadata']=}")
                    # print(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if 'href' in link and 'metadata' in current_data and 'archive' in current_data['metadata']:
                        url_name = link['href']
                        file_name = Path(current_data['metadata']['archive'])

        return url_name, file_name

# FIXME : cette exception se produit quand Eole est inaccessible. C'est la même exception que quand l'accès Internet bloquée sur box Orange)
# e=ConnectTimeout(MaxRetryError("HTTPSConnectionPool(host='eole.avh.asso.fr', port=443): Max retries exceeded with url: /api/v1/search?author=freud (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x6cc96088>, 'Connection to eole.avh.asso.fr timed out. (connect timeout=0.5)'))"))
