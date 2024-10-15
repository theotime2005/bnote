"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import json
import logging
import os
import re
from pathlib import Path
from apps.fman.file_manager import BNOTE_FOLDER
from tools.singleton_meta import SingletonMeta

# The settings file is located in the home() folder, thus it is not deleted by software update.
SETTINGS_FILE = BNOTE_FOLDER / Path("settings.txt")

BLUETOOTH_BASE_NAME = "Esys-bnote-"

# les paramètres sont organisés sous la forme section / key / value
# Les valeurs sont accéssibles par le biais du singleton Settings :
# Settings().data["section"]["key"]

#Settings().data['math']['precision'] = 2
#Settings().data['math']['format'] = 'scientific'

# Les valeurs par défaut sont dans self.DEFAULT_VALUES et les valeurs valides dans self.VALID_VALUES


# from https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self.DEFAULT_VALUES = {'system': {'braille_type': 'dot-8', 'shortcuts_visible': False, 'games_visible': True, 'mp3_visible': True, 'radio_visible': True, 'developer': False},
                               'editor': {'braille_type': 'dot-8', 'line_length': 80, 'dot78_visible': True,
                                          'cursor_visible': True, 'forward_display_mode': 'normal',
                                          'autoscroll': 5},
                               'math': {'angle': 'radian', 'fraction': True, 'precision': 2, 'format': 'scientific'},
                               'music_xml': {'edit_mode' : False, 'notes_dots' : '6_dots_with_group', 'ascending_chords' : True, 'fingering' : True, 'clef' : True, 'parts' : 'name', 'measure_b123' : False, 'measure_number' : False, 'measure_every' : 1, 'view' : "by_section", 'section' : "total_part", 'measures_per_section' : 8, 'words' : True, 'credit_words' : True, 'lyrics' : 'no'},
                               'music_bxml': {'edit_mode' : False, 'notes_dots' : '6_dots_with_group', 'ascending_chords' : True, 'fingering' : True, 'clef' : True, 'parts' : 'name', 'measure_b123' : False, 'measure_number' : False, 'measure_every' : 1, 'view' : 'by_section', 'section' : 'number', 'measures_per_section' : 8, 'words' : True, 'credit_words' : True, 'lyrics' : 'no', 'karaoke' : True},
                               'speech': {'volume_headphone': 40, 'volume_hp': 55, 'speed': 110, 'language': "fr_FR",
                                          'synthesis': 'cerence', 'voice': 'audrey'},
                               'radio': {'volume_headphone': 40, 'volume_hp': 55},
                               'bluetooth': {'bnote_visible': True, 'bnote_name': "", 'auto_switch': [], 'bt_simul_esys': True},
                               'agenda': {'display_agenda': False, 'default_presentation':'standard', 'remember_same_day':False, 'remember_next_day':False},
                               'mode examen': {'actif': False},
                               }

        self.VALID_VALUES = {'system': {'braille_type': ('dot-8', 'grade1', 'grade2'), 'shortcuts_visible': (True, False), 'games_visible': (True, False),
                                        'mp3_visible': (True, False), 'radio_visible': (True, False),
                                        'developer': (True, False)},
                             'editor': {'braille_type': ('dot-8', 'grade1', 'grade2'), 'line_length': range(1, 161),
                                        'dot78_visible': (True, False), 'cursor_visible': (True, False),
                                        'forward_display_mode': ('normal', 'significative'),
                                        'autoscroll': range(2, 120)},
                             'math': {'angle': ('degree', 'radian'), 'fraction': (True, False),
                                      'precision': range(0, 9), 'format': ('scientific', 'normal')},
                             'music_xml': {'edit_mode' : (False, True), 
                                           'notes_dots': ('8_dots', '6_dots', '6_dots_with_group'),
                                           'ascending_chords': (False, True),
                                           'fingering': (False, True),
                                           'clef': (False, True),
                                           'parts': ('name', 'id', 'abbreviation'),
                                           'measure_b123': (False, True),
                                           'measure_number': (False, True),
                                           'measure_every': range(1, 101),
                                           'view': ("by_section", "by_part"),
                                           'section': ("total_part", "system", "number"),
                                           'measures_per_section': range(1, 101),
                                           'words': (False, True),
                                           'credit_words': (False, True),
                                           'lyrics': ("no", "after_each_note", "before_each_section", "after_each_section")},
                             'music_bxml': {'edit_mode' : (False, True),
                                            'notes_dots': ('8_dots','6_dots', '6_dots_with_group'),
                                            'ascending_chords': (False, True),
                                            'fingering': (False, True),
                                            'clef': (False, True),
                                            'parts': ('name', 'id', 'abbreviation'),
                                            'measure_b123': (False, True),
                                            'measure_number': (False, True),
                                            'measure_every': range(1, 101),
                                            'view': ("by_section", "by_part"),
                                            'section': ('total_part', 'system', 'number'),
                                            'measures_per_section': range(1, 101),
                                            'words': (False, True),
                                            'credit_words': (False, True),
                                            'lyrics': ("no", "after_each_note", "before_each_section", "after_each_section"),
                                            'karaoke': (False, True)},
                             'speech': {'volume_headphone': range(0, 101), 'volume_hp': range(0, 101),
                                        'speed': range(40, 241),
                                        'language': ("fr_FR",),
                                        'synthesis': ('picotts', 'mbrola', 'espeak', "cerence"),
                                        'voice': ("default",),
                                        },
                             'radio': {'volume_headphone': range(0, 101), 'volume_hp': range(0, 101)},
                             'bluetooth': {'bnote_visible': (True, False),
                                           'bnote_name': re.compile('.*'),
                                           'auto_switch': [],
                                           'bt_simul_esys': (True, False)},
                             'agenda': {'display_agenda':(True, False),
                                        'default_presentation': ('standard', 'not done', 'today','calendar'),
                                        'remember_same_day': (True, False),
                                        'remember_next_day':(True, False)},
                             'mode examen': {'actif': (False, True)},
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
            with open(SETTINGS_FILE, 'r') as json_file:
                data_on_disk = json.load(json_file)
        except:
            pass

        # If nothing change, it's not usefull to rewrite on sdcard.
        if data_on_disk == self.data:
            return

        with open(SETTINGS_FILE, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    def load(self):
        try:
            with open(SETTINGS_FILE, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError as exception:
            print(f"{exception=}")
            print("Use default values")
            pass
        except json.JSONDecodeError as exception:
            print(f"{exception=}")
            print("Use default values")
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
