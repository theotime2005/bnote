"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json
import logging
import os
import re
from pathlib import Path
from bnote.apps.fman.file_manager import BNOTE_FOLDER
from bnote.tools.singleton_meta import SingletonMeta

# The settings file is located in the home() folder, thus it is not deleted by software update.
SETTINGS_FILE = BNOTE_FOLDER / Path("settings.txt")

BLUETOOTH_BASE_NAME = "Esys-bnote-"

# les paramètres sont organisés sous la forme section / key / value
# Les valeurs sont accéssibles par le biais du singleton Settings :
# Settings().data["section"]["key"]

# Settings().data['math']['precision'] = 2
# Settings().data['math']['format'] = 'scientific'

# Les valeurs par défaut sont dans self.DEFAULT_VALUES et les valeurs valides dans self.VALID_VALUES


# from https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self.DEFAULT_VALUES = {
            "system": {
                "braille_type": "dot-8",
                "auto_sync_date": False,
                "spaces_in_label": False,
                "shortcuts_visible": False,
                "app_explorer": "main_apps_menu",
                "app_settings": "main_apps_menu",
                "app_agenda": "invisible",
                "app_radio": "invisible",
                "app_mp3": "invisible",
                "app_wikipedia": "invisible",
                "app_timer": "invisible",
                "app_translator": "invisible",
                "app_write_word": "invisible",
                "app_operation": "invisible",
                "app_mines": "invisible",
                "app_mastermind": "invisible",
                "developer": False,
                "debug": False,
            },
            "explorer": {
                "empty_bluetooth_shutdown": False,
                "empty_trash_shutdown": False,
                "number_recent_files": 10,
            },
            "editor": {
                "braille_type": "dot-8",
                "line_length": 80,
                "dot78_visible": True,
                "cursor_visible": True,
                "forward_display_mode": "normal",
                "autoscroll": 5,
            },
            "math": {
                "angle": "radian",
                "fraction": True,
                "precision": 2,
                "format": "scientific",
            },
            "music_xml": {
                "edit_mode": "read",
                "braille_type": "dot-8",
                "notes_dots": "6_dots_with_group",
                "ascending_chords": True,
                "fingering": True,
                "clef": True,
                "parts": "name",
                "measure_b123": False,
                "measure_number": False,
                "measure_every": 1,
                "view": "by_section",
                "section": "total_part",
                "measures_per_section": 8,
                "words": True,
                "credit_words": True,
                "lyrics": "no",
            },
            "music_bxml": {
                "edit_mode": "read",
                "braille_type": "dot-8",
                "notes_dots": "6_dots_with_group",
                "ascending_chords": True,
                "fingering": True,
                "clef": True,
                "parts": "name",
                "measure_b123": False,
                "measure_number": False,
                "measure_every": 1,
                "view": "by_section",
                "section": "number",
                "measures_per_section": 8,
                "words": True,
                "credit_words": True,
                "lyrics": "no",
                "karaoke": True,
            },
            "speech": {
                "volume_headphone": 40,
                "volume_hp": 55,
                "speed": 110,
                "language": "fr_FR",
                "synthesis": "cerence",
                "voice": "audrey",
            },
            "radio": {"volume_headphone": 40, "volume_hp": 55},
            "bluetooth": {
                "bnote_visible": True,
                "bnote_name": "",
                "auto_switch": [],
                "bt_simul_esys": True,
            },
            "agenda": {"default_presentation": "standard", "remember": "no"},
            "braille_learning": {
                "use_vocal": "auto",
                "keep_spaces": False,
                "write_all": True,
            },
            "update": {"auto_check": False},
            "eole": {"user_name": "", "token": ""},
            "translator": {"base_language": "French", "translate_language": "English"},
            "stm32": {
                "name": "",
                "len": 0,
                "firmware": "",
                "serial": "",
            },
            "ai_eurobraille": {
                "username": "",
                "password": "",
                "token": "",
            },
        }

        self.VALID_VALUES = {
            "system": {
                "braille_type": ("dot-8", "grade1", "grade2"),
                "auto_sync_date": (False, True),
                "spaces_in_label": (True, False),
                "shortcuts_visible": (True, False),
                "app_explorer": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_settings": ("main_apps_menu", "more_apps_menu"),
                "app_agenda": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_radio": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_mp3": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_timer": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_translator": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_wikipedia": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_write_word": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_operation": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_mines": ("invisible", "main_apps_menu", "more_apps_menu"),
                "app_mastermind": ("invisible", "main_apps_menu", "more_apps_menu"),
                "developer": (True, False),
                "debug": (True, False)
            },
            "explorer": {
                "empty_bluetooth_shutdown": (True, False),
                "empty_trash_shutdown": (True, False),
                "number_recent_files": range(1, 31),
            },
            "editor": {
                "braille_type": ("dot-8", "grade1", "grade2"),
                "line_length": range(1, 161),
                "dot78_visible": (True, False),
                "cursor_visible": (True, False),
                "forward_display_mode": ("normal", "significative"),
                "autoscroll": range(2, 120),
            },
            "math": {
                "angle": ("degree", "radian"),
                "fraction": (True, False),
                "precision": range(0, 9),
                "format": ("scientific", "normal"),
            },
            "music_xml": {
                "edit_mode": ("expert", "read", "edit", "listen"),
                "braille_type": ("dot-8", "grade1"),
                "notes_dots": ("8_dots", "6_dots", "6_dots_with_group"),
                "ascending_chords": (False, True),
                "fingering": (False, True),
                "clef": (False, True),
                "parts": ("name", "abbreviation"),
                "measure_b123": (False, True),
                "measure_number": (False, True),
                "measure_every": range(1, 101),
                "view": ("by_section", "by_part"),
                "section": ("total_part", "system", "number"),
                "measures_per_section": range(1, 101),
                "words": (False, True),
                "credit_words": (False, True),
                "lyrics": (
                    "no",
                    "after_each_note",
                    "before_each_section",
                    "after_each_section",
                ),
            },
            "music_bxml": {
                "edit_mode": ("expert", "read", "edit", "listen"),
                "braille_type": ("dot-8", "grade1"),
                "notes_dots": ("8_dots", "6_dots", "6_dots_with_group"),
                "ascending_chords": (False, True),
                "fingering": (False, True),
                "clef": (False, True),
                "parts": ("name", "abbreviation"),
                "measure_b123": (False, True),
                "measure_number": (False, True),
                "measure_every": range(1, 101),
                "view": ("by_section", "by_part"),
                "section": ("total_part", "system", "number"),
                "measures_per_section": range(1, 101),
                "words": (False, True),
                "credit_words": (False, True),
                "lyrics": (
                    "no",
                    "after_each_note",
                    "before_each_section",
                    "after_each_section",
                ),
                "karaoke": (False, True),
            },
            "speech": {
                "volume_headphone": range(0, 101),
                "volume_hp": range(0, 101),
                "speed": range(40, 241),
                "language": ("fr_FR",),
                "synthesis": ("picotts", "mbrola", "espeak", "cerence"),
                "voice": ("default",),
            },
            "radio": {"volume_headphone": range(0, 101), "volume_hp": range(0, 101)},
            "bluetooth": {
                "bnote_visible": (True, False),
                "bnote_name": re.compile(".*"),
                "auto_switch": [],
                "bt_simul_esys": (True, False),
            },
            "agenda": {
                "default_presentation": ("standard", "not_done", "today", "calendar"),
                "remember": ("no", "same", "tomorrow", "same_tomorrow"),
            },
            "braille_learning": {
                "use_vocal": ("auto", "ask", "no"),
                "keep_spaces": (True, False),
                "write_all": (True, False),
            },
            "update": {"auto_check": (True, False)},
            "eole": {"user_name": "", "token": ""},
            "stm32": {
                "name": "",
                "len": range(0, 81),
                "firmware": "",
                "serial": "",
            },
            "ai_eurobraille": {
                "username": "",
                "password": "",
                "token": "",
            },
        }
        self.data = dict()

        if not Path(SETTINGS_FILE).exists():
            # Create default values
            self.data = self.DEFAULT_VALUES
            # Save the values
            self.save()
        else:
            self.load()

    def save(self):
        data_on_disk = None
        try:
            with open(SETTINGS_FILE, "r") as json_file:
                data_on_disk = json.load(json_file)
        except:
            pass

        # If nothing change, it's not usefull to rewrite on sdcard.
        if data_on_disk == self.data:
            return

        with open(SETTINGS_FILE, "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def load(self):
        try:
            with open(SETTINGS_FILE, "r") as json_file:
                self.data = json.load(json_file)
        except (FileNotFoundError, TypeError, json.JSONDecodeError) as exception:
            # print(f"{exception=}")
            # print("Use default values")
            pass

        # print(f"{self.data=}")
        # print(f"{len(self.data)=}")
        # print(f"{self.DEFAULT_VALUES=}")
        # print(f"{len(self.DEFAULT_VALUES)=}")

        # Update missing values in the json file with default embedded values (when developer add new data).
        for key, values in self.DEFAULT_VALUES.items():
            self.data.setdefault(key, values)
            for k, v in values.items():
                self.data[key].setdefault(k, v)

        # print(f"{self.data=}")
        # print(f"{len(self.data)=}")

        # Save the data to reflect the possible change from setdefault()
        self.save()

    # delete the settings file and reload default value.
    def reset(self):
        if os.path.exists(SETTINGS_FILE):
            # Remove the file using the os.remove() method
            os.remove(SETTINGS_FILE)
            # Clear the current data. data will be init to the defaut values by the next laod()
            self.data = dict()

        self.load()

    def export_settings(self, path):
        with open("{}.bnote".format(path), "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def import_settings(self, path):
        # Import file
        try:
            with open(path, "r") as json_file:
                imported_data = json.load(json_file)
        except (FileNotFoundError, TypeError, json.JSONDecodeError) as exception:
            # print(f"{exception=}")
            # print("File not found.")
            return

        # Update self.data with imported data
        self.data.update(imported_data)

        # Save the updated data
        self.save()
        self.load()
        return True
