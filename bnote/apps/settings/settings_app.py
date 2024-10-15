"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import _thread
import os
import re
import sys
import shutil
import socket
import threading
import time
from collections import OrderedDict
from enum import Enum
from pathlib import Path

import __init__ as version

from apps.bnote_app import BnoteApp, FunctionId
from datetime import datetime

from speech.speech import SpeechManager
from stm32 import stm32_keys
from stm32.braille_device_characteristics import braille_device_characteristics
from stm32.stm32_protocol import Stm32Frame
from tools.mode_examen.examen_manager import Exam
from tools import bt_util
from tools.keyboard import Keyboard
from tools.quick_search import QuickSearch
from tools.settings import Settings, BLUETOOTH_BASE_NAME
from tools.speech_wrapper import speak
from tools.translate import Translate
from tools.volume import Volume
from tools.volume_speed_dialog_box import VolumeDialogBox, SpeedDialogBox
from tools.io_util import Gpio
from ui.ui_checkbox import UiCheckBox
from ui.ui_dialog_box import UiDialogBox
from ui.ui_edit_box import UiEditBox
from ui.ui_list_box import UiListBox
from ui.ui_menu_bar import UiMenuBar
from ui.ui_menu_item import UiMenuItem
from ui.ui_message_dialog_box import UiMessageDialogBox, UiInfoDialogBox
from ui.ui_button import UiButton
import wifi as wifi

# Setup the logger for this file
from debug.colored_log import ColoredLogger, SETTING_APP_LOG
from ui.ui_settings_dialog_box import UiSettingsDialogBox
from ui.ui_list_box import UiListBox
from wifi import WpaSupplicant
from wifi.iwconfig import IwConfig

log = ColoredLogger(__name__)
log.setLevel(SETTING_APP_LOG)


class TestMode(Enum):
    NO_TEST = object()
    TEST_LINE = object()


class SettingsApp(BnoteApp):
    # Timer in second.
    BATTERY_TIMER_TIME_OUT = 3
    """
    Setting application.
    """
    def __init__(self, put_in_function_queue, put_in_stm32_tx_queue):
        # Call base class.
        BnoteApp.__init__(self, put_in_function_queue)

        self.__put_in_stm32_tx_queue = put_in_stm32_tx_queue

        # The key of this dict is a tuple with the 'section' str and the 'key' str used in Settings().
        # The value of this dict is a dict with 'action' and 'action_param', as required in UiMenuItem
        # ('is_hide', 'shortcut_modifier', 'shortcut_key' can be used too)
        self.__action_and_action_param = self.__create_action_and_action_param()

        # test mode
        self.__test_mode = TestMode.NO_TEST
        self.__test_timer = None
        self.__test_step_value = 0

        self.__timer_battery = self.BATTERY_TIMER_TIME_OUT

        # The QuickSearch instance.
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)

        # Version de la sdcard
        self.__sdcard_version = _("unknown")
        if (Path().home() / Path("sdcard_version")).exists():
            with open(Path().home() / Path("sdcard_version"), 'r') as f:
                self.__sdcard_version = f.readline()

        # Bluetooth devices
        self.__computers = []
        self.__paired_devices = dict()  # key = mac address of the device, value = name of the device
        self.__auto_switch_devices = dict()  # key = line_index of the document, value = mac_name of the device.
        # self.__auto_switch_values = {True: _("auto switch"),
        #                              False: _("do nothing")}

        # Menu creation.
        self._menu = self.__create_menu()

        # Document creation
        self.__document_area = []
        self.__document_area_current_line_index = 0

        # Fill the document.
        self.__update_document(update_computers_and_paired_device=True)

        self.refresh_document()

    def __create_action_and_action_param(self):
        # The key of this dict is a tuple with the 'section' str and the 'key' str used in Settings().
        # The value of this dict is a dict with 'action' and 'action_param', as required in UiMenuItem
        # ('is_hide', 'shortcut_modifier', 'shortcut_key' can be used too)
        return {
            ('stm32', 'time'): {'action': self.__dialog_set_time, 'action_param': {"section": 'stm32', "key": 'time'}},
            ('stm32', 'date'): {'action': self.__dialog_set_date, 'action_param': {"section": 'stm32', "key": 'date'}},
            ('speech', 'jack'): {'action': None, },
            ('speech', 'synthesis'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'speech', "key": 'synthesis'}},
            ('speech', 'voice'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'speech', "key": 'voice'}},
            ('speech', 'volume'): {'action': self.__dialog_set_volume, 'action_param': {"section": 'speech', "key": 'volume'}, 'shortcut_modifier': Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, 'shortcut_key': "v"},
            ('speech', 'speed'): {'action': self.__dialog_set_speed, 'action_param': {"section": 'speech', "key": 'speed'}},
            ('stm32', 'usb_a_hid_keyboard'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'usb_a_hid_keyboard'}},
            ('stm32', 'usb_b_hid_keyboard'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'usb_b_hid_keyboard'}},
            ('stm32', 'usb_simul_esys'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'usb_simul_esys'}},
            ('bluetooth', 'bnote_name'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'bluetooth', "key": 'bnote_name'}},
            ('bluetooth', 'bnote_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'bluetooth', "key": 'bnote_visible'}},
            ('bluetooth', "paired_devices"): {'action': self.__dialog_show_paired_devices, 'action_param': {"section": 'bluetooth', "key": "paired_devices"}},
            ('bluetooth', 'auto_switch'): {'action': self.__dialog_set_auto_switch, 'action_param': {"section": 'bluetooth', "key": 'auto_switch'}},
            ('bluetooth', 'speech'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'bluetooth', "key": 'speech'}},
            ('bluetooth', 'bt_simul_esys'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'bluetooth', "key": 'bt_simul_esys'}},
            ('wifi', 'connected_to'): {'action': self.__dialog_set_wifi_connected_settings, 'action_param': {"section": 'wifi', "key": 'connected_to'}},
            ('wifi', 'favorites'): {'action': self.__dialog_set_wifi_favorites_settings, 'action_param': {"section": 'wifi', "key": 'favorites'}},
            ('system', 'braille_type'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'system', "key": 'braille_type'}},
            ('system', 'shortcuts_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'system', "key": 'shortcuts_visible'}},
            ('system', 'games_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'system', "key": 'games_visible'}},
            ('system', 'mp3_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'system', "key": 'mp3_visible'}},
            ('system', 'radio_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'system', "key": 'radio_visible'}},
            ('editor', 'braille_type'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'braille_type'}},
            ('editor', 'line_length'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'line_length'}},
            ('editor', 'forward_display_mode'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'forward_display_mode'}},
            ('editor', 'autoscroll'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'autoscroll'}},
            ('editor', 'cursor_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'cursor_visible'}},
            ('editor', 'dot78_visible'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'editor', "key": 'dot78_visible'}},
            ('math', 'format'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'math', "key": 'format'}},
            ('math', 'precision'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'math', "key": 'precision'}},
            ('math', 'fraction'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'math', "key": 'fraction'}},
            ('math', 'angle'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'math', "key": 'angle'}},
            ('music_xml', 'edit_mode'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'edit_mode'}},
            ('music_xml', 'notes_dots'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'notes_dots'}},
            ('music_xml', 'ascending_chords'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'ascending_chords'}},
            ('music_xml', 'fingering'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'fingering'}},
            ('music_xml', 'clef'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'clef'}},
            ('music_xml', 'parts'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'parts'}},
            ('music_xml', 'measure_b123'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'measure_b123'}},
            ('music_xml', 'measure_number'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'measure_number'}},
            ('music_xml', 'measure_every'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'measure_every'}},
            ('music_xml', 'view'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'view'}},
            ('music_xml', 'section'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'section'}},
            ('music_xml', 'measures_per_section'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'measures_per_section'}},
            ('music_xml', 'words'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'words'}},
            ('music_xml', 'credit_words'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'credit_words'}},
            ('music_xml', 'lyrics'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_xml', "key": 'lyrics'}},
            ('music_bxml', 'edit_mode'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'edit_mode'}},
            ('music_bxml', 'notes_dots'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'notes_dots'}},
            ('music_bxml', 'ascending_chords'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'ascending_chords'}},
            ('music_bxml', 'fingering'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'fingering'}},
            ('music_bxml', 'clef'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'clef'}},
            ('music_bxml', 'parts'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'parts'}},
            ('music_bxml', 'measure_b123'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'measure_b123'}},
            ('music_bxml', 'measure_number'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'measure_number'}},
            ('music_bxml', 'measure_every'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'measure_every'}},
            ('music_bxml', 'view'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'view'}},
            ('music_bxml', 'section'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'section'}},
            ('music_bxml', 'measures_per_section'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'measures_per_section'}},
            ('music_bxml', 'words'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'words'}},
            ('music_bxml', 'credit_words'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'credit_words'}},
            ('music_bxml', 'lyrics'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'lyrics'}},
            ('music_bxml', 'karaoke'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'music_bxml', "key": 'karaoke'}},
            ('agenda', 'display_agenda'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'agenda', "key": 'display_agenda'}},
            ('agenda', 'default_presentation'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'agenda', "key": 'default_presentation'}},
            ('agenda', 'remember_same_day'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'agenda', "key": 'remember_same_day'}},
            ('agenda', 'remember_next_day'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'agenda', "key": 'remember_next_day'}},
            ('stm32', 'language_message'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'language_message'}},
            ('stm32', 'language_keyboard'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'language_keyboard'}},
            ('speech', 'language'): {'action': self.__dialog_set_settings, 'action_param': {"section": 'speech', "key": 'language'}},
            ('wlan', 'country'): {'action': self.__dialog_set_wlan_country, 'action_param': {"section": 'wlan', "key": 'country'}},
            ('stm32', 'keyboard_mode'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_mode'}},
            ('stm32', 'keyboard_b78'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_b78'}},
            ('stm32', 'keyboard_invertion'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_invertion'}},
            ('stm32', 'keyboard_light_press'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_light_press'}},
            ('stm32', 'keyboard_strong_press'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_strong_press'}},
            ('stm32', 'keyboard_consecutive_press'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_consecutive_press'}},
            ('stm32', 'keyboard_double_light_press'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_double_light_press'}},
            ('stm32', 'keyboard_double_strong_press'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'keyboard_double_strong_press'}},
            ('stm32', 'standby_transport'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'standby_transport'}},
            ('stm32', 'standby_shutdown'): {'action': self.__dialog_set_stm32, 'action_param': {"section": 'stm32', "key": 'standby_shutdown'}},
        }

    def __action(self, section, key):
        return self.__action_and_action_param[(section, key)]['action']

    def __action_param(self, section, key):
        return self.__action_and_action_param[(section, key)]['action_param']

    def __create_settings_app_music_xml_menu(self):
        return UiMenuBar(name=_("&musicxml"),
                         menu_item_list=[
                             UiMenuItem(name=_("&edit and play mode"), **self.__action_and_action_param[('music_xml', 'edit_mode')]),
                             UiMenuItem(name=_("notes d&ots"), **self.__action_and_action_param[('music_xml', 'notes_dots')]),
                             UiMenuItem(name=_("&ascending chords"), **self.__action_and_action_param[('music_xml', 'ascending_chords')]),
                             UiMenuItem(name=_("&fingering"), **self.__action_and_action_param[('music_xml', 'fingering')]),
                             UiMenuItem(name=_("&clef"), **self.__action_and_action_param[('music_xml', 'clef')]),
                             UiMenuItem(name=_("&parts"), **self.__action_and_action_param[('music_xml', 'parts')]),
                             UiMenuItem(name=_("&measure b123"), **self.__action_and_action_param[('music_xml', 'measure_b123')]),
                             UiMenuItem(name=_("measure &number"), **self.__action_and_action_param[('music_xml', 'measure_number')]),
                             UiMenuItem(name=_("measure &every"), **self.__action_and_action_param[('music_xml', 'measure_every')]),
                             UiMenuItem(name=_("&view"), **self.__action_and_action_param[('music_xml', 'view')]),
                             UiMenuItem(name=_("&section"), **self.__action_and_action_param[('music_xml', 'section')]),
                             UiMenuItem(name=_("measures per sec&tion"), **self.__action_and_action_param[('music_xml', 'measures_per_section')]),
                             UiMenuItem(name=_("&words"), **self.__action_and_action_param[('music_xml', 'words')]),
                             UiMenuItem(name=_("cre&dit words"), **self.__action_and_action_param[('music_xml', 'credit_words')]),
                             UiMenuItem(name=_("&lyrics"), **self.__action_and_action_param[('music_xml', 'lyrics')]),
                         ])

    def __create_settings_app_music_bxml_menu(self):
        return UiMenuBar(name=_("&bxml"),
                         menu_item_list=[
                             UiMenuItem(name=_("&edit and play mode"), **self.__action_and_action_param[('music_bxml', 'edit_mode')]),
                             UiMenuItem(name=_("notes d&ots"), **self.__action_and_action_param[('music_bxml', 'notes_dots')]),
                             UiMenuItem(name=_("&ascending chords"), **self.__action_and_action_param[('music_bxml', 'ascending_chords')]),
                             UiMenuItem(name=_("&fingering"), **self.__action_and_action_param[('music_bxml', 'fingering')]),
                             UiMenuItem(name=_("&clef"), **self.__action_and_action_param[('music_bxml', 'clef')]),
                             UiMenuItem(name=_("&parts"), **self.__action_and_action_param[('music_bxml', 'parts')]),
                             UiMenuItem(name=_("&measure b123"), **self.__action_and_action_param[('music_bxml', 'measure_b123')]),
                             UiMenuItem(name=_("measure &number"), **self.__action_and_action_param[('music_bxml', 'measure_number')]),
                             UiMenuItem(name=_("measure &every"), **self.__action_and_action_param[('music_bxml', 'measure_every')]),
                             UiMenuItem(name=_("&view"), **self.__action_and_action_param[('music_bxml', 'view')]),
                             UiMenuItem(name=_("&section"), **self.__action_and_action_param[('music_bxml', 'section')]),
                             UiMenuItem(name=_("measures per sec&tion"), **self.__action_and_action_param[('music_bxml', 'measures_per_section')]),
                             UiMenuItem(name=_("&words"), **self.__action_and_action_param[('music_bxml', 'words')]),
                             UiMenuItem(name=_("cre&dit words"), **self.__action_and_action_param[('music_bxml', 'credit_words')]),
                             UiMenuItem(name=_("&lyrics"), **self.__action_and_action_param[('music_bxml', 'lyrics')]),
                             UiMenuItem(name=_("&karaoke"), **self.__action_and_action_param[('music_bxml', 'karaoke')]),
                         ])

    def __create_menu(self):
        hide_v2_menu = not Gpio().gpio_hardware_v2()
        return UiMenuBar(
            name=_("settings"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                UiMenuBar(
                    name=_("&clock"), action=self._exec_clock,
                    menu_item_list=[
                        UiMenuItem(name=_("&time"), **self.__action_and_action_param[('stm32', 'time')]),
                        UiMenuItem(name=_("&date"), **self.__action_and_action_param[('stm32', 'date')]),
                    ]),

                UiMenuBar(
                    name=_("&vocalize"), action=self._exec_synthese,
                    menu_item_list=[
                        UiMenuItem(name=_("&volume"), **self.__action_and_action_param[('speech', 'volume')]),
                        UiMenuItem(name=_("&speed"), **self.__action_and_action_param[('speech', 'speed')]),
                        UiMenuItem(name=_("&language"), **self.__action_and_action_param[('speech', 'language')]),
                        UiMenuItem(name=_("s&ynthesis"), **self.__action_and_action_param[('speech', 'synthesis')]),
                        UiMenuItem(name=_("voi&ce"), **self.__action_and_action_param[('speech', 'voice')]),
                    ]),

                UiMenuBar(
                    name=_("&usb"),
                    menu_item_list=[
                        UiMenuItem(name=_("usb-&a-hid keyboard"), **self.__action_and_action_param[('stm32', 'usb_a_hid_keyboard')]),
                        UiMenuItem(name=_("usb-&b-hid keyboard"), **self.__action_and_action_param[('stm32', 'usb_b_hid_keyboard')]),
                        UiMenuItem(name=_("simulation &esys"), **self.__action_and_action_param[('stm32', 'usb_simul_esys')]),
                    ]),
                UiMenuBar(
                    name=_("&bluetooth"), action=self._exec_bluetooth,
                    menu_item_list=[
                        UiMenuItem(name=_("&name"), **self.__action_and_action_param[('bluetooth', 'bnote_name')]),
                        UiMenuItem(name=_("&visibility"), **self.__action_and_action_param[('bluetooth', 'bnote_visible')]),
                        UiMenuItem(name=_("&paired devices"), **self.__action_and_action_param[('bluetooth', 'paired_devices')]),
                        UiMenuItem(name=_("simulation &esys"), **self.__action_and_action_param[('bluetooth', 'bt_simul_esys')]),
                    ]),
                UiMenuBar(
                    name=_("&wifi"),
                    menu_item_list=[
                        UiMenuItem(name=_("&connected to"), **self.__action_and_action_param[('wifi', 'connected_to')]),
                        UiMenuItem(name=_("&favorites"), **self.__action_and_action_param[('wifi', 'favorites')]),
                        UiMenuItem(name=_("countr&y"), **self.__action_and_action_param[('wlan', 'country')]),
                    ]),
                UiMenuBar(
                    name=_("user &interface"),
                    menu_item_list=[
                        UiMenuItem(name=_("&message language"), **self.__action_and_action_param[('stm32', 'language_message')]),
                        UiMenuItem(name=_("&braille language"), **self.__action_and_action_param[('stm32', 'language_keyboard')]),
                        UiMenuItem(name=_("braille &type"), **self.__action_and_action_param[('system', 'braille_type')]),
                        UiMenuItem(name=_("visible &shortcuts"), **self.__action_and_action_param[('system', 'shortcuts_visible')]),
                        UiMenuItem(name=_("visible &games"), **self.__action_and_action_param[('system', 'games_visible')]),
                        UiMenuItem(name=_("visible &audio"), **self.__action_and_action_param[('system', 'mp3_visible')]),
                        UiMenuItem(name=_("visible &radio"), **self.__action_and_action_param[('system', 'radio_visible')]),
                    ]),

                UiMenuBar(
                    name=_("&editor"), action=self._exec_editor,
                    menu_item_list=[
                        UiMenuItem(name=_("&braille type"), **self.__action_and_action_param[('editor', 'braille_type')]),
                        UiMenuItem(name=_("&line length"), **self.__action_and_action_param[('editor', 'line_length')]),
                        UiMenuItem(name=_("&forward display"), **self.__action_and_action_param[('editor', 'forward_display_mode')]),
                        UiMenuItem(name=_("&autoscroll display"), **self.__action_and_action_param[('editor', 'autoscroll')]),
                        UiMenuItem(name=_("&cursor visible"), **self.__action_and_action_param[('editor', 'cursor_visible')]),
                        UiMenuItem(name=_("&dot78 visible"), **self.__action_and_action_param[('editor', 'dot78_visible')]),
                    ]),

                UiMenuBar(
                    name=_("mat&h"), action=self._exec_math,
                    menu_item_list=[
                        UiMenuItem(name=_("&format"), **self.__action_and_action_param[('math', 'format')]),
                        UiMenuItem(name=_("&precision"), **self.__action_and_action_param[('math', 'precision')]),
                        UiMenuItem(name=_("f&raction"), **self.__action_and_action_param[('math', 'fraction')]),
                        UiMenuItem(name=_("&angle"), **self.__action_and_action_param[('math', 'angle')]),
                    ]),

                UiMenuBar(
                    name=_("&music"), action=self._exec_music,
                    menu_item_list=[
                        self.__create_settings_app_music_xml_menu(),
                        self.__create_settings_app_music_bxml_menu(),
                    ]),

                UiMenuBar(
                    name=_("a&genda"), action=self._exec_agenda,
                    menu_item_list=[
                        UiMenuItem(name=_("display &agenda"), **self.__action_and_action_param[('agenda', 'display_agenda')]),
                        UiMenuItem(name=_("default &presentation"), **self.__action_and_action_param[('agenda', 'default_presentation')]),
                        UiMenuItem(name=_("&report events not done for same day"), **self.__action_and_action_param[('agenda', 'remember_same_day')]),
                        UiMenuItem(name=_("report events not done for &next day"), **self.__action_and_action_param[('agenda','remember_next_day')])
                    ]
                ),

                UiMenuBar(
                    name=_("&keyboard"),
                    menu_item_list=[
                        UiMenuItem(name=_("&mode"), **self.__action_and_action_param[('stm32', 'keyboard_mode')]),
                        UiMenuItem(name=_("b78"), **self.__action_and_action_param[('stm32', 'keyboard_b78')]),
                        UiMenuItem(name=_("&invertion"), **self.__action_and_action_param[('stm32', 'keyboard_invertion')]),
                        UiMenuItem(name=_("&light press"), **self.__action_and_action_param[('stm32', 'keyboard_light_press')]),
                        UiMenuItem(name=_("&strong press"), **self.__action_and_action_param[('stm32', 'keyboard_strong_press')]),
                        UiMenuItem(name=_("&consecutive press"), **self.__action_and_action_param[('stm32', 'keyboard_consecutive_press')]),
                        UiMenuItem(name=_("&double light press"), **self.__action_and_action_param[('stm32', 'keyboard_double_light_press')]),
                        UiMenuItem(name=_("double st&rong press"), **self.__action_and_action_param[('stm32', 'keyboard_double_strong_press')]),

                    ]),

                UiMenuBar(
                    name=_("&standby"),
                    menu_item_list=[
                        UiMenuItem(name=_("&transport"), **self.__action_and_action_param[('stm32', 'standby_transport')]),
                        UiMenuItem(name=_("&shutdown"), **self.__action_and_action_param[('stm32', 'standby_shutdown')]),
                    ]),

                UiMenuBar(
                    name=_("e&xamen mode"),
                    menu_item_list=[
                        UiMenuItem(name=_("&unable the exam mode"), action=self._exec_activate_examen),
                        UiMenuItem(name=_("&disable the exam mode"), action=self._exec_desactivate_examen, is_hide=True)
                    ]),

                UiMenuItem(name=_("&test"), action=self._exec_test),
                UiMenuItem(name=_("&reset"), action=self._exec_reset),
                UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    # self.document_area est une liste de dictionnaire. Chaque dictionnaire contient les infos utiles pour contruire
    # une ligne du document.
    def __append_line_in_document(self, param_label=None, param_value=None, dialog_box_name=None,
                                  dialog_box_param_name=None, section=None, key=None,
                                  auto_refresh_on_timer=False, is_tab_stop=False):
        if section and key:
            self.__document_area.append({"data_line_text": self.format_label_value(param_label, param_value),
                                         "dialog_box_name": dialog_box_name,
                                         "dialog_box_param_name": dialog_box_param_name,
                                         "section": section, "key": key,
                                         "auto_refresh_on_timer": auto_refresh_on_timer, "is_tab_stop": is_tab_stop})
        else:
            self.__document_area.append({"data_line_text": self.format_label_value(param_label, param_value),
                                         "dialog_box_name": dialog_box_name,
                                         "dialog_box_param_name": dialog_box_param_name,
                                         "section": section, "key": key,
                                         "auto_refresh_on_timer": auto_refresh_on_timer, "is_tab_stop": is_tab_stop})

    def __update_document(self, update_computers_and_paired_device=False):
        # Bluetooth paired-devices
        if update_computers_and_paired_device:
            self.__update_computers_and_paired_devices()

        self.__document_area = []
        if Settings().data['mode examen']['actif']:
            self.__append_line_in_document(param_label=_("examen mode"), param_value=_("actif"))
            self.__append_line_in_document(param_label=_("time"), param_value=self.__get_time_value())
            self.__append_line_in_document(param_label=_("date"), param_value=self.__get_date_value())
        else:
            self.__append_line_in_document(param_label=_("time"), param_value=self.__get_time_value(), dialog_box_name=_('time'), dialog_box_param_name=_('time'), section='stm32', key='time', auto_refresh_on_timer=True, is_tab_stop=True)
            self.__append_line_in_document(param_label=_("date"), param_value=self.__get_date_value(), dialog_box_name=_('date'), dialog_box_param_name=_('date'), section='stm32', key='date')

        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("battery"), param_value=self.__get_battery_value(), auto_refresh_on_timer=True, is_tab_stop=True)

        if not Settings().data['mode examen']['actif']:
            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("synthesis"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("volume"), param_value=self.__get_volume_value(), dialog_box_name=_('volume'), dialog_box_param_name=_("&value"), section='speech', key='volume', auto_refresh_on_timer=True,)
            self.__append_line_in_document(param_label=_("speed"), param_value=self.__get_settings_value('speech', 'speed'), dialog_box_name=_('speed'), dialog_box_param_name=_("&value"), section='speech', key='speed')
            self.__append_line_in_document(param_label=_("language"), param_value=self.__get_speech_language_value(), dialog_box_name=_("language"), dialog_box_param_name=_("language"), section='speech', key='language', auto_refresh_on_timer=True)
            self.__append_line_in_document(param_label=_("synthesis"), param_value=self.__get_settings_value('speech', 'synthesis'), dialog_box_name=_("synthesis"), dialog_box_param_name=_("&synthesis"), section='speech', key='synthesis')
            self.__append_line_in_document(param_label=_("voice"), param_value=self.__get_settings_value('speech', 'voice'), dialog_box_name=_("voice"), dialog_box_param_name=_("&voice"), section='speech', key='voice')
            if Gpio().gpio_hardware_v2():
                # Show only for bnote v2.
                self.__append_line_in_document(param_label=_("jack"), param_value=self.__get_jack_value(), auto_refresh_on_timer=True)

        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("usb"), is_tab_stop=True)
        self.__append_line_in_document(param_label=_("keyboard USB-A-HID"), param_value=self.__get_stm32_value('stm32', 'usb_a_hid_keyboard'), dialog_box_name=_("keyboard"), dialog_box_param_name=_("usb-a hid mode"), section='stm32', key='usb_a_hid_keyboard')
        self.__append_line_in_document(param_label=_("keyboard USB-B-HID"), param_value=self.__get_stm32_value('stm32', 'usb_b_hid_keyboard'), dialog_box_name=_("keyboard"), dialog_box_param_name=_("usb-b hid mode"), section='stm32', key='usb_b_hid_keyboard')
        self.__append_line_in_document(param_label=_("simulation esys"), param_value=self.__get_stm32_value('stm32', 'usb_simul_esys'), dialog_box_name=_("simulation esys"), dialog_box_param_name=_("simulation esys"), section='stm32', key='usb_simul_esys')

        if Settings().data['mode examen']['actif'] and Exam().examen['bluetooth'] or not Settings().data['mode examen']['actif']:
            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("bluetooth"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("name"), param_value=self.__get_bluetooth_name_value(), dialog_box_name=_('bluetooth'), dialog_box_param_name=_("&bnote name"), section='bluetooth', key='bnote_name')
            self.__append_line_in_document(param_label=_("visible"), param_value=self.__get_bluetooth_visible_value(), dialog_box_name=_('bluetooth'), dialog_box_param_name=_("&bnote visible"), section='bluetooth', key='bnote_visible')
            self.__append_line_in_document(param_label=_("paired devices"), param_value=self.__get_bluetooth_pairing_value(), dialog_box_name=_('bluetooth'), dialog_box_param_name=_("&paired devices"), section='bluetooth', key="paired_devices")
            # Bluetooth move automatically in application when screen reader connect
            self.__auto_switch_devices = dict()
            auto_switch_device = Settings().data['bluetooth']['auto_switch']
            for key, value in self.__paired_devices.items():
                auto_switch_value = self.__bluetooth_auto_switch()[self.mac_name(key, value) in auto_switch_device]
                log.debug(f"{key=} {value=} {auto_switch_value=}")
                self.__append_line_in_document(param_label=value, param_value=auto_switch_value, dialog_box_name=_("bluetooth auto switch"), dialog_box_param_name=value, section='bluetooth', key='auto_switch')
                self.__document_area[len(self.__document_area) - 1]['mac_name'] = self.mac_name(key, value)
                # log.debug(f"mac_name={self.mac_name(key, value)}")
                # log.debug(f"{len(self.__document_area)=}")
                # log.debug(f"{self.__document_area[len(self.__document_area) - 1]['mac_name']=}")
            self.__append_line_in_document(param_label=_("simulation esys"), param_value=self.__get_settings_value('bluetooth', 'bt_simul_esys'), dialog_box_name=_("simulation esys"), dialog_box_param_name=_("simulation &esys"), section='bluetooth', key='bt_simul_esys')

        self.__append_line_in_document()
        # ip address
        self.__append_line_in_document(param_label=_("wifi"), is_tab_stop=True)
        self.__append_line_in_document(param_label=_("connected to"), param_value=self.__get_wifi_connected_to(), dialog_box_name=_("connected to"), dialog_box_param_name=_("&connected"), section='wifi', key='connected_to')
        self.__append_line_in_document(param_label=_("favorites"), param_value=self.__get_wifi_favorites(), dialog_box_name=_("favorites"), dialog_box_param_name=_("&favorites"), section='wifi', key='favorites')
        self.__append_line_in_document(param_label=_("ip address"), param_value=SettingsApp.get_ip(), auto_refresh_on_timer=True)
        self.__append_line_in_document(param_label=_("country"), param_value=self.__get_wlan_country_value(), dialog_box_name=_("wlan country"), dialog_box_param_name=_("wlan country"), section='wlan', key='country')

        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("user interface"), is_tab_stop=True)
        self.__append_line_in_document(param_label=_("message language"), param_value=self.__get_message_language_country_value(), dialog_box_name=_("language"), dialog_box_param_name=_("message"), section='stm32', key='language_message', auto_refresh_on_timer=True)
        self.__append_line_in_document(param_label=_("braille language"), param_value=self.__get_keyboard_language_country_value(), dialog_box_name=_("language"), dialog_box_param_name=_("braille"), section='stm32', key='language_keyboard', auto_refresh_on_timer=True)
        self.__append_line_in_document(param_label=_("braille type"), param_value=self.__get_settings_value('system', 'braille_type'), dialog_box_name=_("user interface"), dialog_box_param_name=_("&braille type"), section='system', key='braille_type')
        self.__append_line_in_document(param_label=_("visible shortcuts"), param_value=self.__get_settings_value('system', 'shortcuts_visible'), dialog_box_name=_("user interface"), dialog_box_param_name=_("visible &shortcuts"), section='system', key='shortcuts_visible')
        if not Settings().data['mode examen']['actif']:
            self.__append_line_in_document(param_label=_("visible games"), param_value=self.__get_settings_value('system', 'games_visible'), dialog_box_name=_("user interface"), dialog_box_param_name=_("visible &games"), section='system', key='games_visible')
            self.__append_line_in_document(param_label=_("visible audio"), param_value=self.__get_settings_value('system', 'mp3_visible'), dialog_box_name=_("user interface"), dialog_box_param_name=_("visible &audio"), section='system', key='mp3_visible')
            self.__append_line_in_document(param_label=_("visible radio"), param_value=self.__get_settings_value('system', 'radio_visible'), dialog_box_name=_("user interface"), dialog_box_param_name=_("visible &radio"), section='system', key='radio_visible')

        if Settings().data['mode examen']['actif'] and Exam().examen['editor'] or not Settings().data['mode examen']['actif']:
            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("editor"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("braille type"), param_value=self.__get_settings_value('editor', 'braille_type'), dialog_box_name=_('editor'), dialog_box_param_name=_("&braille type"), section='editor', key='braille_type')
            self.__append_line_in_document(param_label=_("line length"), param_value=self.__get_settings_value('editor', 'line_length'), dialog_box_name=_('editor'), dialog_box_param_name=_("lines &length"), section='editor', key='line_length')
            self.__append_line_in_document(param_label=_("forward display"), param_value=self.__get_settings_value('editor', 'forward_display_mode'), dialog_box_name=_('editor'), dialog_box_param_name=_("&forward display"), section='editor', key='forward_display_mode')
            self.__append_line_in_document(param_label=_("autoscroll display"), param_value=self.__get_settings_value('editor', 'autoscroll'), dialog_box_name=_('editor'), dialog_box_param_name=_("&autoscroll display"), section='editor', key='autoscroll')
            self.__append_line_in_document(param_label=_("cursor visible"), param_value=self.__get_settings_value('editor', 'cursor_visible'), dialog_box_name=_('editor'), dialog_box_param_name=_("&cursor visible"), section='editor', key='cursor_visible')
            self.__append_line_in_document(param_label=_("dot78 visible"), param_value=self.__get_settings_value('editor', 'dot78_visible'), dialog_box_name=_('editor'), dialog_box_param_name=_("&dot 78 visible"), section='editor', key='dot78_visible')

        if Settings().data['mode examen']['actif'] and Exam().examen['math'] or not Settings().data['mode examen']['actif']:
            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("math"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("format"), param_value=self.__get_settings_value('math', 'format'), dialog_box_name=_("math"), dialog_box_param_name=_("&format"), section='math', key='format')
            self.__append_line_in_document(param_label=_("precision"), param_value=self.__get_settings_value('math', 'precision'), dialog_box_name=_("math"), dialog_box_param_name=_("&precision"), section='math', key='precision')
            self.__append_line_in_document(param_label=_("fraction"), param_value=self.__get_settings_value('math', 'fraction'), dialog_box_name=_("math"), dialog_box_param_name=_("&fraction result"), section='math', key='fraction')
            self.__append_line_in_document(param_label=_("angle"), param_value=self.__get_settings_value('math', 'angle'), dialog_box_name=_("math"), dialog_box_param_name=_("&angle"), section='math', key='angle')

        if not Settings().data['mode examen']:
            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("music"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("musicxml edit and play mode"), param_value=self.__get_settings_value('music_xml', 'edit_mode'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&edit and play mode"), section='music_xml', key='edit_mode')
            self.__append_line_in_document(param_label=_("musicxml notes dots"), param_value=self.__get_settings_value('music_xml', 'notes_dots'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&notes dots"), section='music_xml', key='notes_dots')
            self.__append_line_in_document(param_label=_("musicxml ascending chords"), param_value=self.__get_settings_value('music_xml', 'ascending_chords'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&ascending chords"), section='music_xml', key='ascending_chords')
            self.__append_line_in_document(param_label=_("musicxml fingering"), param_value=self.__get_settings_value('music_xml', 'fingering'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&fingering"), section='music_xml', key='fingering')
            self.__append_line_in_document(param_label=_("musicxml clef"), param_value=self.__get_settings_value('music_xml', 'clef'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&clef"), section='music_xml', key='clef')
            self.__append_line_in_document(param_label=_("musicxml parts"), param_value=self.__get_settings_value('music_xml', 'parts'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&parts"), section='music_xml', key='parts')
            self.__append_line_in_document(param_label=_("musicxml measure b123"), param_value=self.__get_settings_value('music_xml', 'measure_b123'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&measure b123"), section='music_xml', key='measure_b123')
            self.__append_line_in_document(param_label=_("musicxml measure number"), param_value=self.__get_settings_value('music_xml', 'measure_number'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&measure number"), section='music_xml', key='measure_number')
            self.__append_line_in_document(param_label=_("musicxml measure every"), param_value=self.__get_settings_value('music_xml', 'measure_every'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&measure every"), section='music_xml', key='measure_every')
            self.__append_line_in_document(param_label=_("musicxml view"), param_value=self.__get_settings_value('music_xml', 'view'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&view"), section='music_xml', key='view')
            self.__append_line_in_document(param_label=_("musicxml section"), param_value=self.__get_settings_value('music_xml', 'section'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&section"), section='music_xml', key='section')
            self.__append_line_in_document(param_label=_("musicxml measures per section"), param_value=self.__get_settings_value('music_xml', 'measures_per_section'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&measures per section"), section='music_xml', key='measures_per_section')
            self.__append_line_in_document(param_label=_("musicxml words"), param_value=self.__get_settings_value('music_xml', 'words'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&words"), section='music_xml', key='words')
            self.__append_line_in_document(param_label=_("musicxml credit words"), param_value=self.__get_settings_value('music_xml', 'credit_words'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&credit words"), section='music_xml', key='credit_words')
            self.__append_line_in_document(param_label=_("musicxml lyrics"), param_value=self.__get_settings_value('music_xml', 'lyrics'), dialog_box_name=_("music xml"), dialog_box_param_name=_("&lyrics"), section='music_xml', key='lyrics')
            self.__append_line_in_document(param_label=_("bxml edit and play mode"), param_value=self.__get_settings_value('music_bxml', 'edit_mode'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&edit and play mode"), section='music_bxml', key='edit_mode')
            self.__append_line_in_document(param_label=_("bxml notes dots"), param_value=self.__get_settings_value('music_bxml', 'notes_dots'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&notes dots"), section='music_bxml', key='notes_dots')
            self.__append_line_in_document(param_label=_("bxml ascending chords"), param_value=self.__get_settings_value('music_bxml', 'ascending_chords'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&ascending chords"), section='music_bxml', key='ascending_chords')
            self.__append_line_in_document(param_label=_("bxml fingering"), param_value=self.__get_settings_value('music_bxml', 'fingering'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&fingering"), section='music_bxml', key='fingering')
            self.__append_line_in_document(param_label=_("bxml clef"), param_value=self.__get_settings_value('music_bxml', 'clef'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&clef"), section='music_bxml', key='clef')
            self.__append_line_in_document(param_label=_("bxml parts"), param_value=self.__get_settings_value('music_bxml', 'parts'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&parts"), section='music_bxml', key='parts')
            self.__append_line_in_document(param_label=_("bxml measure b123"), param_value=self.__get_settings_value('music_bxml', 'measure_b123'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&measure b123"), section='music_bxml', key='measure_b123')
            self.__append_line_in_document(param_label=_("bxml measure number"), param_value=self.__get_settings_value('music_bxml', 'measure_number'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&measure number"), section='music_bxml', key='measure_number')
            self.__append_line_in_document(param_label=_("bxml measure every"), param_value=self.__get_settings_value('music_bxml', 'measure_every'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&measure every"), section='music_bxml', key='measure_every')
            self.__append_line_in_document(param_label=_("bxml view"), param_value=self.__get_settings_value('music_bxml', 'view'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&view"), section='music_bxml', key='view')
            self.__append_line_in_document(param_label=_("bxml section"), param_value=self.__get_settings_value('music_bxml', 'section'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&section"), section='music_bxml', key='section')
            self.__append_line_in_document(param_label=_("bxml measures per section"), param_value=self.__get_settings_value('music_bxml', 'measures_per_section'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&measures per section"), section='music_bxml', key='measures_per_section')
            self.__append_line_in_document(param_label=_("bxml words"), param_value=self.__get_settings_value('music_bxml', 'words'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&words"), section='music_bxml', key='words')
            self.__append_line_in_document(param_label=_("bxml credit words"), param_value=self.__get_settings_value('music_bxml', 'credit_words'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&credit words"), section='music_bxml', key='credit_words')
            self.__append_line_in_document(param_label=_("bxml lyrics"), param_value=self.__get_settings_value('music_bxml', 'lyrics'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&lyrics"), section='music_bxml', key='lyrics')
            self.__append_line_in_document(param_label=_("bxml karaoke"), param_value=self.__get_settings_value('music_bxml', 'karaoke'), dialog_box_name=_("music bxml"), dialog_box_param_name=_("&karaoke"), section='music_bxml', key='karaoke')

            self.__append_line_in_document()
            self.__append_line_in_document(param_label=_("agenda"), is_tab_stop=True)
            self.__append_line_in_document(param_label=_("display agenda"), param_value=self.__get_settings_value('agenda', 'display_agenda'), dialog_box_name=_("agenda"), dialog_box_param_name=_("&display"), section='agenda', key='display_agenda')
            if Settings().data['agenda']['display_agenda']:
                self.__append_line_in_document(param_label=_("default presentation"), param_value=self.__get_settings_value('agenda', 'default_presentation'), dialog_box_name=_("agenda"), dialog_box_param_name=_("&presentation"), section='agenda', key='default_presentation')
                self.__append_line_in_document(param_label=_("at startup, report events not done for same day"), param_value=self.__get_settings_value('agenda', 'remember_same_day'), dialog_box_name=_("agenda"), dialog_box_param_name=_("remember events for same day"), section='agenda', key='remember_same_day')
                self.__append_line_in_document(param_label=_("at startup, report events not done for next day"), param_value=self.__get_settings_value('agenda', 'remember_next_day'), dialog_box_name=_("agenda"), dialog_box_param_name=_("remember events for next day"), section='agenda', key='remember_next_day')

        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("keyboards"), is_tab_stop=True)
        self.__append_line_in_document(param_label=_("mode"), param_value=self.__get_stm32_value('stm32', 'keyboard_mode'), dialog_box_name=_("keyboard"), dialog_box_param_name=_("braille keyboard mode"), section='stm32', key='keyboard_mode')
        self.__append_line_in_document(param_label=_("b78"), param_value=self.__get_stm32_value('stm32', 'keyboard_b78'), dialog_box_name=_("keyboard"), dialog_box_param_name=_("braille keyboard b78"), section='stm32', key='keyboard_b78')
        self.__append_line_in_document(param_label=_("invertion"), param_value=self.__get_stm32_value('stm32', 'keyboard_invertion'), dialog_box_name=_("keyboard"), dialog_box_param_name=_("inversion"), section='stm32', key='keyboard_invertion')
        self.__append_line_in_document(param_label=_("light press"), param_value=self.__get_stm32_value('stm32', 'keyboard_light_press'), dialog_box_name=_("routing keyboard"), dialog_box_param_name=_("light press"), section='stm32', key='keyboard_light_press')
        self.__append_line_in_document(param_label=_("strong press"), param_value=self.__get_stm32_value('stm32', 'keyboard_strong_press'), dialog_box_name=_("routing keyboard"), dialog_box_param_name=_("strong press"), section='stm32', key='keyboard_strong_press')
        self.__append_line_in_document(param_label=_("consecutive press"), param_value=self.__get_stm32_value('stm32', 'keyboard_consecutive_press'), dialog_box_name=_("routing keyboard"), dialog_box_param_name=_("consecutive"), section='stm32', key='keyboard_consecutive_press')
        self.__append_line_in_document(param_label=_("double light press"), param_value=self.__get_stm32_value('stm32', 'keyboard_double_light_press'), dialog_box_name=_("routing keyboard"), dialog_box_param_name=_("double light"), section='stm32', key='keyboard_double_light_press')
        self.__append_line_in_document(param_label=_("double strong press"), param_value=self.__get_stm32_value('stm32', 'keyboard_double_strong_press'), dialog_box_name=_("routing keyboard"), dialog_box_param_name=_("double strong"), section='stm32', key='keyboard_double_strong_press')

        # Standby
        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("standby"), is_tab_stop=True)
        self.__append_line_in_document(param_label=_("transport timeout minute (0 none)"), param_value=self.__get_stm32_value('stm32', 'standby_transport'), dialog_box_name=_("standby"), dialog_box_param_name=_("transport"), section='stm32', key='standby_transport', auto_refresh_on_timer=True)
        self.__append_line_in_document(param_label=_("shutdown timeout minute (0 none)"), param_value=self.__get_stm32_value('stm32', 'standby_shutdown'), dialog_box_name=_("standby"), dialog_box_param_name=_("shutdown"), section='stm32', key='standby_shutdown', auto_refresh_on_timer=True)

        # Versions
        self.__append_line_in_document()
        self.__append_line_in_document(param_label=_("versions"), is_tab_stop=True)
        # braille display length, subtype and serial number.
        option_str = ""
        if braille_device_characteristics.is_esysuite_option():
            option_str = "esysuite"
        device_sub_type = self.__device_sub_type(False)
        braille_note = "b.note {} {} {} ({})".format(
            braille_device_characteristics.get_braille_display_length(),
            device_sub_type[braille_device_characteristics.get_sub_type()],
            braille_device_characteristics.get_serial_number(),
            option_str
        )
        if Settings().data['mode examen']['actif']:
            braille_note=braille_note+" "+_("examen mode")
        self.__append_line_in_document(param_label=_("device type"), param_value=braille_note)
        # b.note version
        self.__append_line_in_document(param_label=_("applications"), param_value=version.__version__)
        # Firmware version
        self.__append_line_in_document(param_label=_("firmware"), param_value=braille_device_characteristics.get_firmware_version())
        # SDCard version
        self.__append_line_in_document(param_label=_("sdcard"), param_value=self.__sdcard_version)
        self.__append_line_in_document(param_label=_("sdcard space"), param_value=self.__get_disk_space_value())
        # Device generation
        self.__append_line_in_document(param_label=_("generation 2"), param_value=self.__get_hardware_value())


        # Kernel version
        x = os.popen("uname -srm")
        text_echo = x.readlines()
        log.debug("kernel version =>{}".format(text_echo))
        for line in text_echo:
            self.__append_line_in_document(param_label=line.replace("\n", ""))
        log.info("version : <{}>".format(self.__document_area))

        # Check self.__document_area_current_line_index because of removed bluetooth adaptor from the paired device
        # can invalidate self.__document_area_current_line_index.
        if self.__document_area_current_line_index >= len(self.__document_area):
            self.__document_area_current_line_index = len(self.__document_area) - 1

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self.__create_menu()
        self.__update_document(update_computers_and_paired_device=True)
        self.__refresh_braille_display()

    def on_timer(self):
        if (self.__test_mode == TestMode.NO_TEST) and not self._in_menu and self._current_dialog is None and \
                self.__document_area[self.__document_area_current_line_index]["auto_refresh_on_timer"] is True:

            self.__update_document()
            self.__refresh_braille_display(self._braille_display.get_start_pos())

            self.__timer_battery = self.__timer_battery - 1
            if not (self.__timer_battery % self.BATTERY_TIMER_TIME_OUT):
                self.__timer_battery = self.BATTERY_TIMER_TIME_OUT
                self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BATTERY, data=b''))

    # This method can be time consuming
    def __update_computers_and_paired_devices(self):
        self.__computers = []
        self.__paired_devices = bt_util.get_paired_devices()
        for key, value in self.__paired_devices.items():
            self.__computers.append(value)

    def __get_settings_value(self, section, key, in_braille=False):
        value = Settings().data[section][key]
        if isinstance(value, bool):
            value = self.__ui_bool_values_dict()[value]
        try:
            # log.error(f"{section=} {key=} {value=}")
            return self.__translation_settings_dict(in_braille=in_braille)[(section, key)][value]
        except KeyError as e:
            pass
        return "{}".format(value)

    @staticmethod
    def split_mac_name(bt_mac_name):
        if len(bt_mac_name.split(" ")) >= 2:
            return bt_mac_name.split(" ")[0], " ".join(bt_mac_name.split(" ")[1:])

        return "", ""

    @staticmethod
    def mac_name(mac, name):
        return " ".join((mac, name))

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip_addr = s.getsockname()[0]
        except Exception:
            ip_addr = '127.0.0.1'
        finally:
            s.close()
        return ip_addr

    def __get_stm32_value(self, section, key, in_braille=False):
        try:
            return self.__translation_settings_dict(in_braille=in_braille)[(section, key)][self.__get_stm32_current_value(section, key)]
        except KeyError as e:
            try:
                value = self.__get_stm32_current_value(section, key)
                # Pour retourner les valeur int (('stm32', 'standby_transport') et ('stm32', 'standby_shutdown')).
                if isinstance(value, str):
                    return value
            except KeyError as error:
                log.error(f"{error=} => return \"{_('unknown')}\"")
                pass

            log.error(f"{e=} => return \"{_('unknown')}\"")
            return _("unknown")

    def __get_stm32_current_value(self, section, key):
        values = {('stm32', 'usb_a_hid_keyboard'): braille_device_characteristics.get_usb_hid_mode(0),
                  ('stm32', 'usb_b_hid_keyboard'): braille_device_characteristics.get_usb_hid_mode(1),
                  ('stm32', 'usb_simul_esys'): braille_device_characteristics.get_usb_simul_esys(),
                  ('stm32', 'keyboard_mode'): braille_device_characteristics.get_keyboard_mode(),
                  ('stm32', 'keyboard_b78'): braille_device_characteristics.get_keyboard_b78(),
                  ('stm32', 'keyboard_invertion'): braille_device_characteristics.get_keyboard_inversion(),
                  ('stm32', 'keyboard_light_press'): braille_device_characteristics.get_keyboard_routing_light_press(),
                  ('stm32', 'keyboard_strong_press'): braille_device_characteristics.get_keyboard_routing_strong_press(),
                  ('stm32', 'keyboard_consecutive_press'): braille_device_characteristics.get_keyboard_routing_consecutive_press(),
                  ('stm32', 'keyboard_double_light_press'): braille_device_characteristics.get_keyboard_routing_double_light_press(),
                  ('stm32', 'keyboard_double_strong_press'): braille_device_characteristics.get_keyboard_routing_double_strong_press(),
                  ('stm32', 'standby_transport'): braille_device_characteristics.get_standby_transport(),
                  ('stm32', 'standby_shutdown'): braille_device_characteristics.get_standby_shutdown(),
                  ('stm32', 'language_message'): braille_device_characteristics.get_message_language_country(),
                  ('stm32', 'language_keyboard'): braille_device_characteristics.get_keyboard_language_country(),
                  }

        return values[(section, key)]

    def __set_stm32_current_value(self, section, key, value):
        set_value_function = {('stm32', 'usb_a_hid_keyboard'): self.__set_usb_a_hid_mode,
                              ('stm32', 'usb_b_hid_keyboard'): self.__set_usb_b_hid_mode,
                              ('stm32', 'usb_simul_esys'): self.__set_usb_simul_esys,
                              ('stm32', 'keyboard_mode'): self.__set_keyboard_mode,
                              ('stm32', 'keyboard_b78'): self.__set_keyboard_b78,
                              ('stm32', 'keyboard_invertion'): self.__set_keyboard_inversion,
                              ('stm32', 'keyboard_light_press'): self.__set_keyboard_routing_light_press,
                              ('stm32', 'keyboard_strong_press'): self.__set_keyboard_routing_strong_press,
                              ('stm32', 'keyboard_consecutive_press'): self.__set_keyboard_routing_consecutive_press,
                              ('stm32', 'keyboard_double_light_press'): self.__set_keyboard_routing_double_light_press,
                              ('stm32', 'keyboard_double_strong_press'): self.__set_keyboard_routing_double_strong_press,
                              ('stm32', 'standby_transport'): self.__set_standby_transport,
                              ('stm32', 'standby_shutdown'): self.__set_standby_shutdown,
                              ('stm32', 'language_message'): self.__set_language_message,
                              ('stm32', 'language_keyboard'): self.__set_language_keyboard,

                              }
        function = set_value_function.get((section, key), None)
        if function:
            function(value)

    def __set_usb_hid_mode(self, index, value):
        braille_device_characteristics.set_usb_hid_mode(index, value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_USB_HID_MODE,
                                                data=braille_device_characteristics.get_usb_hid_mode_raw_data()))

    def __set_usb_a_hid_mode(self, value):
        self.__set_usb_hid_mode(0, value)

    def __set_usb_b_hid_mode(self, value):
        self.__set_usb_hid_mode(1, value)

    def __set_usb_simul_esys(self, value):
        braille_device_characteristics.set_usb_simul_esys(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_USB_SIMUL_ESYS,
                                                data=braille_device_characteristics.get_usb_simul_esys_raw_data()))

    def __set_keyboard_mode(self, value):
        braille_device_characteristics.set_keyboard_mode(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BRAILLE_KEYBOARD_MODE,
                                                data=braille_device_characteristics.get_keyboard_mode_raw_data()))

    def __set_keyboard_b78(self, value):
        braille_device_characteristics.set_keyboard_b78(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BRAILLE_KEYBOARD_B78,
                                                data=braille_device_characteristics.get_keyboard_b78_raw_data()))

    def __set_keyboard_inversion(self, value):
        braille_device_characteristics.set_keyboard_inversion(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_COMMAND_INVERTED_MODE,
                                                data=braille_device_characteristics.get_keyboard_inversion_raw_data()))

    def __set_keyboard_routing_light_press(self, value):
        braille_device_characteristics.set_keyboard_routing_light_press(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_INTERACTIVE_KEYS_MODE,
                                                data=braille_device_characteristics.get_keyboard_routing_mode_raw_data()))

    def __set_keyboard_routing_strong_press(self, value):
        braille_device_characteristics.set_keyboard_routing_double_strong_press(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_INTERACTIVE_KEYS_MODE,
                                                data=braille_device_characteristics.get_keyboard_routing_mode_raw_data()))

    def __set_keyboard_routing_consecutive_press(self, value):
        braille_device_characteristics.set_keyboard_routing_consecutive_press(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_INTERACTIVE_KEYS_MODE,
                                                data=braille_device_characteristics.get_keyboard_routing_mode_raw_data()))

    def __set_keyboard_routing_double_light_press(self, value):
        braille_device_characteristics.set_keyboard_routing_double_light_press(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_INTERACTIVE_KEYS_MODE,
                                                data=braille_device_characteristics.get_keyboard_routing_mode_raw_data()))

    def __set_keyboard_routing_double_strong_press(self, value):
        braille_device_characteristics.set_keyboard_routing_double_strong_press(value)
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_INTERACTIVE_KEYS_MODE,
                                                data=braille_device_characteristics.get_keyboard_routing_mode_raw_data()))

    def __set_standby_transport(self, value):
        braille_device_characteristics.set_standby_transport(str(value))
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_STANDBY,
                                                data=braille_device_characteristics.get_standby_raw_data()))

    def __set_standby_shutdown(self, value):
        braille_device_characteristics.set_standby_shutdown(str(value))
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_STANDBY,
                                                data=braille_device_characteristics.get_standby_raw_data()))

    def __set_language_message(self, value):
        # Save the new settings.
        braille_device_characteristics.set_message_language_country(value.encode())
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_DEVICE_LANGUAGE,
                                                data=braille_device_characteristics.get_message_language_country().encode()))

    def __set_language_keyboard(self, value):
        # Save the new settings.
        braille_device_characteristics.set_keyboard_language_country(value.encode())
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_KEYBOARD_LANGUAGE,
                                                data=braille_device_characteristics.get_keyboard_language_country().encode()))

    @staticmethod
    def __get_time_value():
        now = datetime.now()
        return "{}:{}:{}".format(f"{now.hour:02d}", f"{now.minute:02d}", f"{now.second:02d}")

    @staticmethod
    def __get_date_value():
        now = datetime.now()
        return "{}/{}/{}".format(f"{now.day:02d}", f"{now.month:02d}", now.year)

    def __get_battery_value(self):
        capacity = braille_device_characteristics.get_battery_remaining_capacity()
        voltage = braille_device_characteristics.get_battery_voltage()
        intensity = braille_device_characteristics.get_battery_intensity()
        state = braille_device_characteristics.get_battery_state()
        states = self.__battery_states(False)
        return "{}% {} {}A {}V".format(capacity, states[state], intensity / 1000, voltage / 1000)

    @staticmethod
    def __get_volume_value():
        return str(Volume().get_volume())

    def __get_jack_value(self):
        # False is "No"
        return self.__ui_bool_values_dict()[Gpio().gpio_head_phone()]

    def __get_hardware_value(self):
        # False is "No"
        return self.__ui_bool_values_dict()[Gpio().gpio_hardware_v2()]

    def __get_disk_space_value(self):
        total, used, free = shutil.disk_usage("/")
        # 2 ** 10 = 1024(1 KB)
        # 2 ** 20 = 1048576(1 MB)
        # 2 ** 30 = 1073741824(1 GB)
        msg = _("Total: {:.1f} GiB, Used: {:.1f} GiB, Free: {:.1f} GiB").format(total // (2 ** 30), used // (2 ** 30), free // (2 ** 30))
        return msg

    @staticmethod
    def __get_bluetooth_name_value():
        bt_name_in_ps = Settings().data['bluetooth']['bnote_name']
        return bt_util.bluetooth_pretty_host_name() if bt_name_in_ps == "" else bt_name_in_ps

    def __get_bluetooth_visible_value(self):
        return self.__ui_bool_values_dict()[Settings().data['bluetooth']['bnote_visible']]

    def __get_bluetooth_pairing_value(self):
        return " ".join(self.__computers)

    @staticmethod
    def __get_message_language_country_value():
        languages = SettingsApp.__languages()
        if braille_device_characteristics.get_message_language_country() in languages.keys():
            return languages[braille_device_characteristics.get_message_language_country()]
        else:
            return braille_device_characteristics.get_message_language_country()

    @staticmethod
    def __get_keyboard_language_country_value():
        languages = SettingsApp.__languages()
        if braille_device_characteristics.get_keyboard_language_country() in languages.keys():
            return languages[braille_device_characteristics.get_keyboard_language_country()]
        else:
            return braille_device_characteristics.get_keyboard_language_country()

    @staticmethod
    def __get_speech_language_value():
        languages = SettingsApp.__languages()
        if Settings().data['speech']['language'] in languages.keys():
            return languages[Settings().data['speech']['language']]
        else:
            return Settings().data['speech']['language']

    @staticmethod
    def __get_wlan_countries_and_country():
        wpa = WpaSupplicant()
        country = wpa.country()
        countries_dict = wpa.countries()
        try:
            country_string = countries_dict[country]
        except KeyError:
            country_string = "?"
        return country_string, countries_dict

    @staticmethod
    def __get_wlan_country_value():
        country_string, countries_dict = SettingsApp.__get_wlan_countries_and_country()
        return country_string

    def format_label_value(self, label, value):
        if label is None:
            label = " "
        # FIXME : petit path pour remplacer une ligne vide par une ligne avec " " (sinon pas de refresh de la part de ?braille_display?
        if len(label) == 0:
            label = " "
        if value is None:
            return BnoteApp.braille_form(label)
        else:
            if isinstance(value, bool):
                value = self.__ui_bool_values_dict()[value]

            return BnoteApp.braille_form("".join([label, ": ", str(value)]))

    # FIXME : A remplacer par autre chose ou pas ??? car la signature de braille_form diffère de celle de la classe de base.
    #  cf https://stackoverflow.com/questions/66130676/signature-does-not-match-base-method-in-class
    def braille_form(self, in_braille, text):
        if in_braille:
            return BnoteApp.braille_form(text)
        return text

    def __battery_states(self, in_braille):
        return {braille_device_characteristics.BatteryState.UNKNOWN: self.braille_form(in_braille, _("unknown")),
                braille_device_characteristics.BatteryState.INACTIVE: self.braille_form(in_braille, _("inactive")),
                braille_device_characteristics.BatteryState.DISCHARGING: self.braille_form(in_braille,
                                                                                           _("discharging")),
                braille_device_characteristics.BatteryState.CHARGING: self.braille_form(in_braille, _("charging")),
                braille_device_characteristics.BatteryState.FAST_CHARGING:
                    self.braille_form(in_braille, _("fast charging")),
                braille_device_characteristics.BatteryState.OUT_OF_ORDER: self.braille_form(in_braille,
                                                                                            _("out of order"))}

    def __device_sub_type(self, in_braille):
        return {
            braille_device_characteristics.DeviceSubType.UNKNOWN: self.braille_form(in_braille, _("unknown")),
            braille_device_characteristics.DeviceSubType.STANDARD: self.braille_form(in_braille, _("standard")),
            braille_device_characteristics.DeviceSubType.LIGHT: self.braille_form(in_braille, _("light")),
            braille_device_characteristics.DeviceSubType.BASIC: self.braille_form(in_braille, _("basic")),
            braille_device_characteristics.DeviceSubType.BASIC_LIGHT: self.braille_form(in_braille, _("basic light")),
            braille_device_characteristics.DeviceSubType.KEYBOARD: self.braille_form(in_braille, _("keyboard"))
            }

    @staticmethod
    def __languages(filter_with_availables_translation=False, filter_with_available_speech_languages=False,
                    force_key=None):
        available_languages = Translate.availables_translations()
        available_speech_languages = SpeechManager().available_speech_languages()

        if filter_with_availables_translation:
            if force_key:
                available_languages.append(force_key)
            filtered_languages_dict = {k: v for (k, v) in Translate.languages_dict.items() if k in available_languages}
            return OrderedDict(sorted(filtered_languages_dict.items(), key=lambda t: t[1]))

        if filter_with_available_speech_languages:
            if force_key:
                available_speech_languages.append(force_key)
            filtered_languages_dict = {k: v for (k, v) in Translate.languages_dict.items() if k in available_speech_languages}
            return OrderedDict(sorted(filtered_languages_dict.items(), key=lambda t: t[1]))

        return OrderedDict(sorted(Translate.languages_dict.items(), key=lambda t: t[1]))

    def __get_tr_settings_value_and_valid_values(self, section, key, current_value, in_braille=True):
        switcher = self.__translation_settings_dict(in_braille=in_braille)

        valid_values_dict = switcher.get((section, key), None)

        log.debug(f"{section=} {key=}")
        log.debug(f"{valid_values_dict=}")
        if valid_values_dict:
            log.debug(f"{current_value=}")
            if current_value not in valid_values_dict:
                valid_values_dict[current_value] = _("unknown")
            log.debug(f"{current_value=} {valid_values_dict[current_value]=} {list(valid_values_dict.values())=}")
            return valid_values_dict[current_value], list(valid_values_dict.values())

        # Pour tout ce qui n'a pas besoin d'être traduit (int / bool)...
        return current_value, Settings().VALID_VALUES

    def __get_tr_stm32_value_and_valid_values(self, section, key, current_value, in_braille=True):
        switcher = self.__translation_settings_dict(in_braille=in_braille)

        valid_values_dict = switcher.get((section, key), None)

        if valid_values_dict:
            if current_value not in valid_values_dict:
                valid_values_dict[current_value] = _("unknown")

            return valid_values_dict[current_value], list(valid_values_dict.values())

        # Pour tout ce qui n'a pas besoin d'être traduit (int / bool)...
        # return current_value, Settings().VALID_VALUES
        return current_value, None


    # def __get_current_value_from_translated_one(self, section, key, current_translated_value):
    #     valid_values_dict = self.__translation_settings_dict().get((section, key), None)
    #     if valid_values_dict:
    #         value = [k for (k, val) in valid_values_dict.items() if val == current_translated_value]
    #         if len(value) == 1:
    #             return value[0]

    def __translation_settings_dict(self, in_braille=True):
        translated_dict = {
            ('math', 'angle'): {'degree': _('degree'), 'radian': _('radian')},
            ('math', 'format'): {"standard": _("standard"), 'scientific': _('scientific')},
            ('music_xml', 'notes_dots'): {"8_dots": _("8 dots"), "6_dots": _("6 dots"), "6_dots_with_group": _("6 dots with group")},
            ('music_xml', 'parts'): {"name": _("name"), "id": _("id"), "abbreviation": _("abbreviation")},
            ('music_xml', 'view'): {"by_section": _("by section"), "by_part": _("by part")},
            ('music_xml', 'section'): {"total_part": _("total part"), "system": _("system"), "number": _("number")},
            ('music_xml', 'lyrics'): {"no": _("no"), "after_each_note": _("after each note"), "before_each_section": _("before each section"), "after_each_section": _("after each section")},
            ('music_bxml', 'notes_dots'): {"8_dots": _("8 dots"), "6_dots": _("6 dots"), "6_dots_with_group": _("6 dots with group")},
            ('music_bxml', 'parts'): {"name": _("name"), "id": _("id"), "abbreviation": _("abbreviation")},
            ('music_bxml', 'view'): {"by_section": _("by section"), "by_part": _("by part")},
            ('music_bxml', 'section'): {"total_part": _("total part"), "system": _("system"), "number": _("number")},
            ('music_bxml', 'lyrics'): {"no": _("no"), "after_each_note": _("after each note"), "before_each_section": _("before each section"), "after_each_section": _("after each section")},
            ('system', 'braille_type'): {'dot-8': _("dot 8"), 'grade1': _("grade 1"), 'grade2': _("grade 2")},
            ('editor', 'braille_type'): {'dot-8': _("dot 8"), 'grade1': _("grade 1"), 'grade2': _("grade 2")},
            ('editor', 'forward_display_mode'): {'normal': _('normal'), 'significative': _('significative')},
            # ('stm32', 'usb_hid_keyboard'): {braille_device_characteristics.UsbHidMode.UNKNOWN: _("unknown"),
            ('stm32', 'usb_a_hid_keyboard'): {braille_device_characteristics.UsbHidMode.KEYS_SEND_TO_SCREEN_READER: _("send to screen reader"),
                                            braille_device_characteristics.UsbHidMode.USB_HID_KEYBOARD_ACTIF: _("active")},
            ('stm32', 'usb_b_hid_keyboard'): {braille_device_characteristics.UsbHidMode.KEYS_SEND_TO_SCREEN_READER: _("send to screen reader"),
                                            braille_device_characteristics.UsbHidMode.USB_HID_KEYBOARD_ACTIF: _("active")},
            ('stm32', 'usb_simul_esys'): self.__ui_bool_values_dict(),
            # ('stm32', 'keyboard_mode'): {braille_device_characteristics.KeyboardMode.UNKNOWN: _("unknown"),
            ('stm32', 'keyboard_mode'): {braille_device_characteristics.KeyboardMode.STANDARD: _("standard"),
                                         braille_device_characteristics.KeyboardMode.UNIMANUEL_1: _("unimanual1"),
                                         braille_device_characteristics.KeyboardMode.UNIMANUEL_2: _("unimanual2"),
                                         braille_device_characteristics.KeyboardMode.UNIMANUEL_3: _("unimanual3"),
                                         braille_device_characteristics.KeyboardMode.UNIMANUEL_4: _("unimanual4")},
            # ('stm32', 'keyboard_b78'): {braille_device_characteristics.KeyboardB78.UNKNOWN: _("unknown"),
            ('stm32', 'keyboard_b78'): {braille_device_characteristics.KeyboardB78.CHARACTER: _("character"),
                                        braille_device_characteristics.KeyboardB78.FUNCTION: _("function")},
            ('stm32', 'keyboard_invertion'): self.__ui_bool_values_dict(),
            ('stm32', 'keyboard_light_press'): self.__routine_mode(),
            ('stm32', 'keyboard_strong_press'): self.__routine_mode(),
            ('stm32', 'keyboard_consecutive_press'): self.__routine_mode(),
            ('stm32', 'keyboard_double_light_press'): self.__routine_mode(),
            ('stm32', 'keyboard_double_strong_press'): self.__routine_mode(),
            ('stm32', 'language_message'): self.__language_message(),
            ('stm32', 'language_keyboard'): self.__language_keyboard(),
            ('speech', 'language'): self.__language_speech(),
            ('speech', 'synthesis'): self.__language_synthesis(),
            ('speech', 'voice'): self.__language_voice(),
            ('bluetooth', 'auto_switch'): self.__bluetooth_auto_switch(),

            # ('stm32', ""): {"": _(""), "": _(""), "": _(""), "": _(""), "": _(""), "": _(""), "": _(""), "": _("")},

            ('agenda','default_presentation'): {"standard": _("standard"), "not done": _("not done"), "today": _("today"), "calendar":_("calendar")},
        }

        # Convert the translated value str using the braille_type (dot-8, grade-1 or grade-2
        if in_braille:
            for key, value in translated_dict.items():
                for k, v in value.items():
                    translated_dict[key][k] = self.braille_form(in_braille, v)

        return translated_dict

    @staticmethod
    def __routine_mode():
        return {braille_device_characteristics.RoutineMode.NONE: _("none"),
                braille_device_characteristics.RoutineMode.FORWARD_BACKWARD: _("backward-forward"),
                braille_device_characteristics.RoutineMode.CLIC: _("click"),
                braille_device_characteristics.RoutineMode.DOUBLE_CLIC: _("double click"),
                braille_device_characteristics.RoutineMode.WINDOWS_KEY: _("windows key"),
                braille_device_characteristics.RoutineMode.APP_KEY: _("context menu")}

    @staticmethod
    def __language_message():
        languages_dict = SettingsApp.__languages(filter_with_availables_translation=True,
                                                 force_key=braille_device_characteristics.get_message_language_country())
        if not braille_device_characteristics.get_message_language_country() in languages_dict:
            languages_dict[
                braille_device_characteristics.get_message_language_country()] = braille_device_characteristics.get_message_language_country()

        return languages_dict

    @staticmethod
    def __language_keyboard():
        languages_dict = SettingsApp.__languages(force_key=braille_device_characteristics.get_keyboard_language_country())
        if not braille_device_characteristics.get_keyboard_language_country() in languages_dict:
            languages_dict[
                braille_device_characteristics.get_keyboard_language_country()] = braille_device_characteristics.get_keyboard_language_country()

        return languages_dict

    @staticmethod
    def __language_speech():
        languages_dict = SettingsApp.__languages(filter_with_available_speech_languages=True,
                                                 force_key=braille_device_characteristics.get_keyboard_language_country())
        if not braille_device_characteristics.get_keyboard_language_country() in languages_dict:
            languages_dict[
                braille_device_characteristics.get_keyboard_language_country()] = braille_device_characteristics.get_keyboard_language_country()

        return languages_dict

    @staticmethod
    def __language_synthesis():
        return SpeechManager.language_synthesis(Settings().data['speech']['language'])

    @staticmethod
    def __language_voice():
        return SpeechManager.language_voice(
            Settings().data['speech']['language'], Settings().data['speech']['synthesis'])

    @staticmethod
    def __bluetooth_auto_switch():
        return {True: _("auto switch"), False: _("do nothing")}

    @staticmethod
    def __ui_bool_values_dict():
        return {True: UiCheckBox("fake", ("id", True)).get_str_value()[1],
                False: UiCheckBox("fake", ("id", False)).get_str_value()[1]}

    # ---------------
    # Menu functions.
    # def __dialog_set_settings(self, *args, **kwargs):
    def __dialog_set_settings(self, section, key, **kwargs):
        log.debug(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Open the dialog box to set {section=} {key=} {kwargs=}")
        log.debug(f"{self.__document_area_current_line_index=}")
        index = -1
        for line in self.__document_area:
            # log.debug(f"{line=}")
            index += 1
            if section == line["section"] and key == line["key"]:
                self.__document_area_current_line_index = index
                value = Settings().data[section][key]

                if "old_value" in kwargs:
                    value = kwargs["old_value"]
                tr_value, tr_valid_values = self.__get_tr_settings_value_and_valid_values(section, key, value)
                self._current_dialog = UiSettingsDialogBox(line["dialog_box_name"], line["dialog_box_param_name"],
                                                           tr_value, tr_valid_values,
                                                           self._exec_settings_ok_dialog, self._exec_cancel_dialog)
                break

    def __dialog_set_stm32(self, section, key, **kwargs):
        log.debug(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Open the dialog box to set {section=} {key=} {kwargs=}")

        index = -1
        for line in self.__document_area:
            # log.error(f"{line=}")
            index += 1
            if section == line["section"] and key == line["key"]:
                self.__document_area_current_line_index = index
                value = self.__get_stm32_current_value(section, key)
                if "old_value" in kwargs:
                    value = kwargs["old_value"]
                tr_value, tr_valid_values = self.__get_tr_stm32_value_and_valid_values(section, key, value)
                self._current_dialog = UiSettingsDialogBox(line["dialog_box_name"], line["dialog_box_param_name"],
                                                           tr_value, tr_valid_values,
                                                           self._exec_stm32_ok_dialog, self._exec_cancel_dialog)
                break

    def __dialog_set_wlan_country(self, section, key, **kwargs):
        country_string, countries_dict = SettingsApp.__get_wlan_countries_and_country()
        self._current_dialog = UiSettingsDialogBox("wlan country", "wlan country",
                                                   country_string, list(countries_dict.values()),
                                                   self._exec_wlan_country_ok_dialog, self._exec_cancel_dialog)

    # Les lignes d'auto switch ne sont pas accessibles depuis un élément de menu.
    # => Pas besoin de chercher self.__document_area_current_line_index
    def __dialog_set_auto_switch(self, section, key, **kwargs):
        log.debug(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Open the dialog box to set {section=} {key=} {kwargs=}")
        log.debug(f"{self.__document_area_current_line_index=}")

        line = self.__document_area[self.__document_area_current_line_index]
        value = self.__document_area[self.__document_area_current_line_index]["mac_name"] in Settings().data[section][key]

        if "old_value" in kwargs:
            value = kwargs["old_value"]

        tr_value, tr_valid_values = self.__get_tr_settings_value_and_valid_values(section, key, value)
        self._current_dialog = UiSettingsDialogBox(line["dialog_box_name"], line["dialog_box_param_name"],
                                                   tr_value, tr_valid_values,
                                                   self._exec_auto_switch_ok_dialog, self._exec_cancel_dialog)

    def __dialog_show_paired_devices(self, section, key, **kwargs):
        self.__update_computers_and_paired_devices()
        index = -1
        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiListBox(name=self.__document_area[self.__document_area_current_line_index]["dialog_box_param_name"],
                          value=("host", self.__computers)
                          ),
                UiButton(name=_("&ok"), action=self.__exec_bluetooth_paired_device_cancel_dialog),
                UiButton(name=_("&remove"), action=self.__remove_bluetooth_paired_device)
            ],
            action_cancelable=self.__exec_bluetooth_paired_device_cancel_dialog,
        )

    def __exec_bluetooth_paired_device_cancel_dialog(self):
        log.info("callback:__exec_bluetooth_paired_device_cancel_dialog")
        # Il faut reconstruire la liste car la boite de dialogue a pu modifier les computers_and_pair_devices...
        self.__update_document(update_computers_and_paired_device=True)
        self.__refresh_braille_display()

    def __remove_bluetooth_paired_device(self):
        kwargs = self._current_dialog.get_values()
        ui_spin = self._current_dialog.set_first_focusable_object()

        log.debug(f"{kwargs=}")
        log.debug(f"{ui_spin=}")
        log.debug(f"{ui_spin.get_index()=}")
        log.debug(f"{ui_spin.get_value()=}")

        # We can have more than 1 computers with the same name in the bluetooth neighborhood.
        wanted_index = ui_spin.get_index()
        wanted_value = kwargs['host']
        log.info(f"wanted_value={wanted_value}")
        if wanted_value is not None:
            index = 0
            log.info(f"self.__paired_devices.items()={self.__paired_devices.items()}")
            for key, value in self.__paired_devices.items():
                if index == wanted_index and value == wanted_value:
                    log.debug(f"ok found {value=}")

                    bt_util.remove_paired_device(key)
                    del self.__paired_devices[key]
                    del self.__computers[index]

                    self.__update_document(update_computers_and_paired_device=True)
                    self.__refresh_braille_display()

                    break
                index += 1
        # Replace l'afficheur sur "appareils couplés" pour voir que çà a fonctionné.
        self.__dialog_show_paired_devices(section='bluetooth', key="paired_devices")

    def __change_bluetooth_name(self):
        wanted_bt_name = Settings().data['bluetooth']['bnote_name']
        current_bt_name = bt_util.bluetooth_pretty_host_name()

        # On veut toujours avoir un nom qui commence par param_setting.BLUETOOTH_BASE_NAME
        if not wanted_bt_name.startswith(BLUETOOTH_BASE_NAME) and len(wanted_bt_name) != 0:
            wanted_bt_name = BLUETOOTH_BASE_NAME + wanted_bt_name

        if wanted_bt_name != current_bt_name:
            # Change le pretty hostname
            bt_util.set_bluetooth_pretty_host_name(wanted_bt_name)
            # Mémorise le changement dans param_setting
            Settings().data['bluetooth']['bnote_name'] = wanted_bt_name
            Settings().save()

            self._current_dialog = UiMessageDialogBox(
                name=_("information"),
                message=_("bnote must restart for the name change to take effect."),
                buttons=[
                    UiButton(name=_("&ok"), action=self.__exec_restart_now)],
                action_cancelable=self._exec_cancel_dialog,
            )

    def __exec_restart_now(self):
        # tell user reboot in progress.
        self._current_dialog = UiInfoDialogBox(message=_("restarting..."))
        self._put_in_function_queue(FunctionId.RESTART_PLEASE)
        return True, None

    def __get_wifi_connected_to(self):
        iw_config = IwConfig()
        ssid = iw_config.ssid()
        return ssid

    def __get_wifi_favorites(self):
        ssids = wifi.WpaSupplicant().ssids()
        return ' '.join(ssids)

    def __dialog_set_wifi_connected_settings(self, section, key, **kwargs):
        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiButton(name=_("&deconnect-connect"), action=self._exec_valid_set_wifi_connected_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __dialog_set_wifi_favorites_settings(self, section, key, **kwargs):
        if 'wpa' in kwargs:
            wpa = kwargs['wpa']
        else:
            wpa = wifi.WpaSupplicant()
        if 'index' in kwargs:
            index = kwargs['index']
        else:
            index = 0
        ssids = wpa.ssids()

        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiListBox(name=_("ssid"),
                          value=('ssid', ssids),
                          current_index=index,
                          extra_parameters={'wpa': wpa},
                          ),
                UiButton(name=_("&ok"), action=self._exec_valid_set_wifi_favorites_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                UiButton(name=_("&set first"), action=self._exec_first_wifi_favorites_dialog),
                UiButton(name=_("&remove"), action=self._exec_remove_wifi_favorites_dialog),
                UiButton(name=_("&add"), action=self._exec_add_wifi_favorites_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_set_wifi_connected_dialog(self):
        """
        Deconnexion - Reconnexion
        """
        wifi.activate()

    def _exec_valid_set_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        ui_list = kwargs['ssid']
        wpa = ui_list.get_extra_parameters()['wpa']
        # save new config file.
        wpa.save()
        # wifi deconnexion-reconnexion
        wifi.activate()

    def __wifi_favorites_dialog_parameters(self):
        kwargs = self._current_dialog.get_values()
        ui_list = kwargs['ssid']
        index = ui_list.get_index()
        wpa = ui_list.get_extra_parameters()['wpa']
        return index, wpa

    def _exec_first_wifi_favorites_dialog(self):
        index, wpa = self.__wifi_favorites_dialog_parameters()
        wpa.set_first(index)
        # Refresh the dialog box
        self.__dialog_set_wifi_favorites_settings(section='wifi', key='favorites', index=0, wpa=wpa)

    def _exec_remove_wifi_favorites_dialog(self):
        index, wpa = self.__wifi_favorites_dialog_parameters()
        wpa.delete(index)
        # Refresh the dialog box
        self.__dialog_set_wifi_favorites_settings(section='wifi', key='favorites', index=0, wpa=wpa)

    def _exec_add_wifi_favorites_dialog(self, **kwargs):
        if 'wpa' in kwargs:
            wpa = kwargs['wpa']
            insert_index = kwargs['insert_index']
            ssid = kwargs['ssid']
        else:
            insert_index, wpa = self.__wifi_favorites_dialog_parameters()
            ssid = ""
        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiEditBox(name=_("ssid"),
                          value=('ssid', ssid)
                          ),
                UiEditBox(name=_("password"),
                          value=('password', "")
                          ),
                UiButton(name=_("&add"), action=self._exec_valid_add_wifi_favorites_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_add_wifi_favorites_dialog),
                UiButton(name=_("&scan"), action=self._exec_scan_add_wifi_favorites_dialog),
            ],
            action_cancelable=self._exec_cancel_add_wifi_favorites_dialog,
            extra_parameters={'wpa': wpa, 'index_insert': insert_index},
        )

    def _exec_scan_add_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        index_insert = kwargs['index_insert']
        wpa = kwargs['wpa']
        _thread.start_new_thread(self.scan_wifi, ((wpa, index_insert), self.scan_wifi_ended))
        self._current_dialog = UiInfoDialogBox(_("scanning..."))

    def scan_wifi_ended(self, wpa_and_index, ssids):
        log.info(f"scan done <{ssids}")
        self._put_in_function_queue(FunctionId.FUNCTION_END_SCAN_WIFI, **{'wpa_and_index': wpa_and_index, 'ssids': ssids})

    def _end_scan_wifi(self, **kwargs):
        wpa, insert_index = kwargs['wpa_and_index']
        ssids = kwargs['ssids']
        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiListBox(name=_("ssid"),
                          value=('ssid', ssids),
                          current_index=0,
                          extra_parameters={'wpa': wpa, 'insert_index': insert_index},
                          ),
                UiButton(name=_("&ok"), action=self._exec_valid_scan_wifi_favorites_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_scan_wifi_favorites_dialog),
            ],
            action_cancelable=self._exec_cancel_scan_wifi_favorites_dialog,
            extra_parameters={'wpa': wpa, 'insert_index': insert_index},
        )

    def _exec_cancel_scan_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        ui_list = kwargs['ssid']
        wpa = ui_list.get_extra_parameters()
        self._exec_add_wifi_favorites_dialog(wpa=wpa, insert_index=kwargs['insert_index'], ssid="")

    def _exec_valid_scan_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        ui_list = kwargs['ssid']
        ssid = ui_list.get_value_at_index()
        kwarg = ui_list.get_extra_parameters()
        if ssid is not None:
            self._exec_add_wifi_favorites_dialog(wpa=kwarg['wpa'], insert_index=kwarg['insert_index'], ssid=ssid)

    @staticmethod
    def scan_wifi(wpa_and_index, end_scan):
        ssids = []
        try:
            cells = wifi.Cell.all(wifi.interface())
            for cell in cells:
                ssids.append(cell.ssid)
        except wifi.InterfaceError:
            # Ignore exception for scanning.
            pass
        # Give feedback
        end_scan(wpa_and_index=wpa_and_index, ssids=ssids)

    def _exec_valid_add_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        wpa = kwargs['wpa']
        insert_index = kwargs['index_insert']
        # if insert_index == -1 because empty list insert item at index 0
        if insert_index < 0:
            insert_index = 0
        ssid = kwargs['ssid']
        if ssid and (len(ssid) > 0):
            password = kwargs['password']
            psk = wpa.encrypt_password(ssid, password)
            wpa.add(insert_index, ssid, psk)
        # Refresh the dialog box
        self.__dialog_set_wifi_favorites_settings(section='wifi', key='favorites', index=insert_index, wpa=wpa)

    def _exec_cancel_add_wifi_favorites_dialog(self):
        kwargs = self._current_dialog.get_values()
        wpa = kwargs['wpa']
        insert_index = kwargs['index_insert']
        # Refresh the dialog box
        self.__dialog_set_wifi_favorites_settings(section='wifi', key='favorites', index=insert_index, wpa=wpa)

    def __dialog_set_time(self, section, key, **kwargs):
        log.debug(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        hour = self.braille_form(True, str(datetime.now().hour))
        minute = self.braille_form(True, str(datetime.now().minute))
        second = self.braille_form(True, str(datetime.now().second))

        if 'hour' in kwargs:
            hour = kwargs['hour']
        if 'minute' in kwargs:
            minute = kwargs['minute']
        if 'second' in kwargs:
            second = kwargs['second']

        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiEditBox(name=_("hours"),
                          value=("hour", hour)
                          ),
                UiEditBox(name=_("minutes"),
                          value=("minute", self.braille_form(True, str(minute)))
                          ),
                UiEditBox(name=_("seconds"),
                          value=("second", self.braille_form(True, str(second)))
                          ),
                UiButton(name=_("&ok"), action=self._exec_valid_set_time_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_set_time_dialog(self):
        kwargs = self._current_dialog.get_values()

        try:
            hour = int(kwargs['hour'])
            minute = int(kwargs['minute'])
            second = int(kwargs['second'])
        except ValueError:
            kwargs.update({"section": 'stm32', "key": 'time'})
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__dialog_set_time,
                action_param=kwargs,
            )
            return

        # Try to set the now datetime with the new value.
        try:
            log.info(f"{hour}:{minute}:{second}")
            now = datetime.now()
            now.replace(hour=hour, minute=minute, second=second)
        except ValueError:
            kwargs.update({"section": 'stm32', "key": 'time'})
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__dialog_set_time,
                action_param=kwargs,
            )
            return

        self.__change_clock_date_and_time(hour=hour, minute=minute, second=second)

    def __dialog_set_date(self, section, key, **kwargs):
        log.debug(f"OK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        day = self.braille_form(True, str(datetime.now().day))
        month = self.braille_form(True, str(datetime.now().month))
        year = self.braille_form(True, str(datetime.now().year))

        if 'day' in kwargs:
            day = kwargs['day']
        if 'month' in kwargs:
            month = kwargs['month']
        if 'year' in kwargs:
            year = kwargs['year']

        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        self._current_dialog = UiDialogBox(
            name=self.__document_area[self.__document_area_current_line_index]["dialog_box_name"],
            item_list=[
                UiEditBox(name=_("day"),
                          value=("day", day)
                          ),
                UiEditBox(name=_("month"),
                          value=("month", self.braille_form(True, str(month)))
                          ),
                UiEditBox(name=_("year"),
                          value=("year", self.braille_form(True, str(year)))
                          ),
                UiButton(name=_("&ok"), action=self._exec_valid_set_date_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_set_date_dialog(self):
        kwargs = self._current_dialog.get_values()

        try:
            day = int(kwargs['day'])
            month = int(kwargs['month'])
            year = int(kwargs['year'])
        except ValueError:
            kwargs.update({"section": 'stm32', "key": 'date'})
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__dialog_set_date,
                action_param=kwargs,
            )
            return

        # Try to set the now datetime with the new value.
        try:
            log.info(f"{day}:{month}:{year}")
            now = datetime.now()
            now.replace(day=day, month=month, year=year)
        except ValueError:
            kwargs.update({"section": 'stm32', "key": 'date'})
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__dialog_set_date,
                action_param=kwargs,
            )
            return

        self.__change_clock_date_and_time(day=day, month=month, year=year)

    def __change_clock_date_and_time(self, *args, **kwargs) -> (bool, object()):
        # Init default value with the current datetime values.
        now = datetime.now()
        hour, minute, second, day, month, year = now.hour, now.minute, now.second, now.day, now.month, now.year

        # Change the current datetime value with the ones passed in kwargs.
        if 'hour' in kwargs:
            hour = kwargs['hour']
        if 'minute' in kwargs:
            minute = kwargs['minute']
        if 'second' in kwargs:
            second = kwargs['second']
        if 'day' in kwargs:
            day = kwargs['day']
        if 'month' in kwargs:
            month = kwargs['month']
        if 'year' in kwargs:
            year = kwargs['year']

        try:
            # Change the datetime with the new value and send it to stm32 if values are correct.
            now = now.replace(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
            new_date_time = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
            # Cancel the timer else if new time < current time timer is dead for (current time - new time)
            if BnoteApp.one_second_timer:
                BnoteApp.one_second_timer.cancel()
                BnoteApp.one_second_timer = None
            self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_DEVICE_DATE_AND_TIME, data=new_date_time.encode()))
        except ValueError:
            pass

    def __dialog_set_volume(self, section, key, **kwargs):
        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        dialog_box_name = self.__document_area[self.__document_area_current_line_index]["dialog_box_name"]
        edit_box_name = self.__document_area[self.__document_area_current_line_index]['dialog_box_param_name']
        self._current_dialog = VolumeDialogBox(dialog_box_name, edit_box_name, self.__save_the_new_volume)

    # Appelé depuis input_command
    def __volume_down_from_shortcut(self):
        level = VolumeDialogBox.volume_down(channel='speech')
        self.__save_the_new_volume(level)

    def __volume_up_from_shortcut(self):
        level = VolumeDialogBox.volume_up(channel='speech')
        self.__save_the_new_volume(level)

    def __save_the_new_volume(self, volume):
        # Save the new Volume in settings.
        Volume().set_volume(volume)
        Settings().save()
        # Alert internal about settings change.
        headphone = Gpio().is_head_phone()
        if headphone:
            key = 'volume_headphone'
        else:
            key = 'volume_hp'
        self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": 'speech', "key": key})

    def __dialog_set_speed(self, section, key, **kwargs):
        # Sync the current line to the right line index
        self._move_document_area_current_line_index_to(section=section, key=key)

        dialog_box_name = self.__document_area[self.__document_area_current_line_index]["dialog_box_name"]
        edit_box_name = self.__document_area[self.__document_area_current_line_index]['dialog_box_param_name']
        self._current_dialog = SpeedDialogBox(dialog_box_name, edit_box_name, self.__save_the_new_speed,
                                              Settings().data['speech']['speed'],
                                              Settings().VALID_VALUES['speech']['speed'])

    def __speed_down_from_shortcut(self):
        current_speed = Settings().data['speech']['speed']
        new_speed = SpeedDialogBox.speed_down(current_speed, Settings().VALID_VALUES['speech']['speed'])
        if new_speed != current_speed:
            Settings().data['speech']['speed'] = new_speed
            Settings().save()
            self.refresh_document()

    def __speed_up_from_shortcut(self):
        current_speed = Settings().data['speech']['speed']
        new_speed = SpeedDialogBox.speed_up(current_speed, Settings().VALID_VALUES['speech']['speed'])
        if new_speed != current_speed:
            Settings().data['speech']['speed'] = new_speed
            Settings().save()
            self.refresh_document()

    def __save_the_new_speed(self, new_speed):
        # Save the new speed in settings.
        try:
            Settings().data['speech']['speed'] = int(new_speed)
            Settings().save()

            # Alert internal about settings change.
            self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": 'speech', "key": 'speed'})
        except ValueError:
            pass

    # Timer must be recreate each time.
    def __test_step(self):
        log.info("__test_step on timer\n\r")
        if self.__test_timer:
            self.__test_timer.cancel()
            self.__test_timer = None

        if self.__test_mode == TestMode.NO_TEST:
            # Test ended.
            return

        if (self.__test_step_value % 2) == 0:
            static_dots = "\u28FF" * braille_device_characteristics.get_braille_display_length()
            braille_blinking = "\u2800" * len(static_dots)
            self.set_braille_display_dots_line(static_dots, braille_blinking, 0)
        else:
            static_dots = "\u2800" * braille_device_characteristics.get_braille_display_length()
            braille_blinking = "\u2800" * len(static_dots)
            self.set_braille_display_dots_line(static_dots, braille_blinking, 0)

        self.__test_step_value += 1

        self.__test_timer = threading.Timer(1, self.__test_step)
        self.__test_timer.start()

    def _exec_test(self):
        log.info("_test called !!!")
        self.__test_mode = TestMode.TEST_LINE
        self.__test_step_value = 0
        self.__test_step()

    def _exec_reset(self):
        # Ask confirmation.
        self._current_dialog = UiMessageDialogBox(
            name=_("warning"),
            message=_("do you want to reset parameters?"),
            buttons=[
                UiButton(name=_("&yes"), action=self.__exec_reset_yes_dialog),
                UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __exec_reset_yes_dialog(self):
        # Remove settings file
        Settings().reset()
        self.__update_document(False)
        # Reset firmware parameters
        self.__put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_RESET_PARAMETERS))

        # Close all editors
        # self._put_in_function_queue(FunctionId.FUNCTION_INTERNAL_CLOSE_ALL_EDITOR)

    def _exec_activate_examen(self):
        self._current_dialog=UiDialogBox(
            name=_("unable exam mode"),
            item_list=[
                UiEditBox(name=_("&password"), value=("mdp", "")),
                UiEditBox(name=_("confirme pass&word"), value=("confirme", "")),
                UiCheckBox(name=_("&bluetooth"), value=("bluetooth", True)),
                UiCheckBox(name=_("e&xplorer"), value=("explorer", True)),
                UiCheckBox(name=_("&editor"), value=("editor", False)),
                UiCheckBox(name=_("ca&lculator"), value=("math", False)),
                UiButton(name=_("&ok"), action=self._exec_valid_activate_examen),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_activate_examen(self):
        kwargs=self._current_dialog.get_values()
        self._current_dialog=UiInfoDialogBox(message=_("activation and restarting..."))
        if not kwargs['explorer'] and kwargs['editor']:
            self._current_dialog=UiInfoDialogBox(message=_("If you prohibit access to the explorer, you cannot use the editor"), action=self._exec_activate_examen)
            return False
        elif not kwargs['editor'] and kwargs['math']:
            self._current_dialog=UiInfoDialogBox(message=_("If the editor is not activated, you cannot use the calculator."), action=self._exec_activate_examen)
            return False
        if kwargs['mdp']==kwargs['confirme']:
            return Exam().activate_examen(password=kwargs['mdp'], bluetooth=kwargs['bluetooth'], explorer=kwargs['explorer'], editor=kwargs['editor'], math=kwargs['math'])
        else:
            self._current_dialog=UiInfoDialogBox(message=_("Passwords are different, try again."), action=self._exec_activate_examen)

    def _exec_desactivate_examen(self):
        self._current_dialog=UiDialogBox(
            name=_("disable exam mode"),
            item_list=[
                UiEditBox(name=_("&password"), value=("mdp", "")),
                UiButton(name=_("&ok"), action=self._exec_valid_desactivate_examen),
                UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_desactivate_examen(self):
        kwargs=self._current_dialog.get_values()
        if Exam().test_password(kwargs['mdp']):
            self._current_dialog=UiInfoDialogBox(message=_("desactivation and shutdown..."))
            Exam().desactivate_examen()
            self._put_in_function_queue(FunctionId.ASK_SHUTDOWN)
        else:
            self._current_dialog=UiInfoDialogBox(message=_("Invalid password!"), action=self._exec_cancel_dialog)

    def _exec_application(self):
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    # --------------------
    # Dialogbox functions.

    def _exec_cancel_dialog(self):
        log.info("callback:_exec_cancel_dialog")

    def _exec_wlan_country_ok_dialog(self, new_value):
        section = self.__document_area[self.__document_area_current_line_index]["section"]
        key = self.__document_area[self.__document_area_current_line_index]["key"]
        country_string, countries_dict = SettingsApp.__get_wlan_countries_and_country()
        pos = list(countries_dict.values()).index(new_value)
        if new_value != country_string:
            country_code = list(countries_dict.keys())[pos]
            WpaSupplicant().set_country(country_code)
            # Ask reboot.
            self._current_dialog = UiInfoDialogBox(
                message=_("you need to shutdown b.note for the changes to take effect"),
                action=self._exec_cancel_dialog(),
            )

    def _exec_settings_ok_dialog(self, new_value):
        log.debug(f"callback:_exec_settings_ok_dialog {new_value=}")
        section = self.__document_area[self.__document_area_current_line_index]["section"]
        key = self.__document_area[self.__document_area_current_line_index]["key"]
        valid_values = Settings().VALID_VALUES[section][key]
        valid_values_dict = self.__translation_settings_dict().get((section, key), None)
        # log.error(f"{valid_values=}")
        # log.error(f"{valid_values_dict=}")

        data_is_valid = False

        if isinstance(Settings().data[section][key], bool):
            if new_value in valid_values:
                data_is_valid = True
        elif isinstance(Settings().data[section][key], int):
            try:
                new_value = int(new_value)
                if new_value in valid_values:
                    data_is_valid = True
            except ValueError:
                pass
        elif isinstance(Settings().data[section][key], str):
            if isinstance(valid_values, list) or isinstance(valid_values, tuple):
                # self.__get_current_value_from_translated_one(section, key, new_value)
                if valid_values_dict:
                    value = [k for (k, val) in valid_values_dict.items() if val == new_value]
                    if len(value) == 1:
                        new_value = value[0]
                        data_is_valid = True
                elif new_value in valid_values:
                    data_is_valid = True
            elif isinstance(Settings().VALID_VALUES[section][key], re.Pattern):
                # If the validation value is a re.Pattern, the new_value string must match
                # with the pattern to be accepted.
                if Settings().VALID_VALUES[section][key].match(new_value):
                    Settings().data[section][key] = new_value
                    data_is_valid = True
        if not data_is_valid:
            invalid_value_message = _("value not valid...")
            if isinstance(Settings().data[section][key], int):
                if isinstance(valid_values, range):
                    invalid_value_message = _("value not valid. It must be between {} and {}.").format(
                        valid_values.start, valid_values.stop - 1)

            self._current_dialog = UiInfoDialogBox(
                message=invalid_value_message,
                action=self.__dialog_set_settings,
                action_param={"section": section, "key": key, "old_value": new_value},
            )
            return

        # Save the new valid value
        Settings().data[section][key] = new_value
        Settings().save()

        # Renaming the bluetooth requires a reboot.
        if (section == 'bluetooth') and (key == 'bnote_name'):
            self.__change_bluetooth_name()

        # Alert internal about settings change.
        self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": section, "key": key})

        # Automatic language changement when message language is modified.
        if (section == 'stm32') and (key == 'message'):
            if new_value in SpeechManager().available_speech_languages():
                section = 'speech'
                key = 'language'
                Settings().data[section][key] = new_value
                Settings().save()
                # Alert internal about settings change.
                self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": section, "key": key})

        # Automatic voice changement when synthesis language is modified.
        if (section == 'speech') and (key == 'synthesis'):
            Settings().data['speech']['voice'] = SpeechManager().default_voice(
                Settings().data['speech']['language'], Settings().data['speech']['synthesis'])

        # log.error(f"New synthesis language : {Settings().data['speech']['language']}")
        # log.error(f"New synthesis : {Settings().data['speech']['synthesis']}")
        # log.error(f"New voice : {Settings().data['speech']['voice']}")

        # Automatic speech synthesis and speech voice changement when speech language is changed.
        if (section == 'speech') and (key == 'language'):
            Settings().data['speech']['synthesis'] = SpeechManager().default_speech_synthesis(
                Settings().data['speech']['language'])
            Settings().data['speech']['voice'] = SpeechManager().default_voice(
                Settings().data['speech']['language'], Settings().data['speech']['synthesis'])

        if (section == 'system') and (key == 'shortcuts_visible'):
            # Alert internal about settings change.
            self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{'section': section, 'key': key})

    def _exec_stm32_ok_dialog(self, new_value):
        log.info(f"callback:_exec_stm32_ok_dialog {new_value=}")

        section = self.__document_area[self.__document_area_current_line_index]["section"]
        key = self.__document_area[self.__document_area_current_line_index]["key"]
        valid_values_dict = self.__translation_settings_dict().get((section, key), None)

        data_is_valid = False

        if valid_values_dict:
            value = [k for (k, val) in valid_values_dict.items() if val == new_value]
            if len(value) == 1:
                new_value = value[0]
                data_is_valid = True
        else:
            if section == 'stm32' and (key == 'standby_transport' or key == 'standby_shutdown'):
                # ca doit être un int
                try:
                    new_value = int(new_value)
                    data_is_valid = True
                except ValueError:
                    pass

        if not data_is_valid:
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__action_on_current_line,
                action_param={"section": section, "key": key, "old_value": new_value},
            )
            return

        # Save the new_value in the stm32
        self.__set_stm32_current_value(section, key, new_value)

    def _exec_auto_switch_ok_dialog(self, new_value):
        log.info(f"callback:_exec_auto_switch_ok_dialog {new_value=}")

        section = self.__document_area[self.__document_area_current_line_index]["section"]
        key = self.__document_area[self.__document_area_current_line_index]["key"]
        valid_values_dict = self.__translation_settings_dict().get((section, key), None)
        data_is_valid = False

        if valid_values_dict:
            value = [k for (k, val) in valid_values_dict.items() if val == new_value]
            if len(value) == 1:
                new_value = value[0]
                data_is_valid = True

        if not data_is_valid:
            self._current_dialog = UiInfoDialogBox(
                message=_("value not valid..."),
                action=self.__dialog_set_settings,
                action_param={"section": section, "key": key, "old_value": new_value},
            )
            return

        # Save the new valid value
        if new_value:
            # Append mac_name in the auto_switch list
            if self.__document_area[self.__document_area_current_line_index]["mac_name"] not in Settings().data[section][key]:
                Settings().data[section][key].append(self.__document_area[self.__document_area_current_line_index]["mac_name"])
        else:
            # remove mac_name from the auto_switch list
            if self.__document_area[self.__document_area_current_line_index]["mac_name"] in Settings().data[section][key]:
                Settings().data[section][key].remove(self.__document_area[self.__document_area_current_line_index]["mac_name"])
        Settings().save()

    # --------------------
    # Key event functions.

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = False
        if key_id != Keyboard.KeyId.KEY_NONE:
            log.info("key_id={}".format(key_id))

            if self.__test_mode != TestMode.NO_TEST:
                # if key_id == Keyboard.KeyId.KEY_MENU:
                # Stop the display test.
                self.__test_mode = TestMode.NO_TEST
                # Ask braille refresh
                return True

            # Pass the command to DialogBox / Menu / BrailleDisplay
            done = BnoteApp.input_command(self, data, modifier, key_id)
            # Decoding key command for file manager document
            if not done:
                log.info(f"Do something with {modifier=} {key_id=} {data=}")
                command_switcher = {
                    (0, Keyboard.KeyId.KEY_CARET_UP): self._caret_up,
                    (0, Keyboard.KeyId.KEY_CARET_DOWN): self._caret_down,
                    (0, Keyboard.KeyId.KEY_CARET_RIGHT): self._caret_next_part,
                    (0, Keyboard.KeyId.KEY_CARET_LEFT): self._caret_previous_part,
                    (0, Keyboard.KeyId.KEY_START_DOC): self._caret_start_of_document,
                    (0, Keyboard.KeyId.KEY_END_DOC): self._caret_end_of_document,
                    (0, Keyboard.KeyId.KEY_FORWARD): self._forward_display,
                    (0, Keyboard.KeyId.KEY_BACKWARD): self._backward_display,
                    (0, Keyboard.KeyId.KEY_SPEECH_VOLUME_DOWN): self.__volume_down_from_shortcut,
                    (0, Keyboard.KeyId.KEY_SPEECH_VOLUME_UP): self.__volume_up_from_shortcut,
                    (0, Keyboard.KeyId.KEY_SPEECH_SPEED_DOWN): self.__speed_down_from_shortcut,
                    (0, Keyboard.KeyId.KEY_SPEECH_SPEED_UP): self.__speed_up_from_shortcut,
                }
                # Get the function from switcher dictionary.
                settings_function = command_switcher.get((modifier, key_id), None)
                if settings_function:
                    # Execute the function
                    settings_function()
                    done = True
        return done

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param character: unicode char
        :param data: brut braille comb. for advanced treatment
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {character=}")
        done = BnoteApp.input_character(self, modifier, character, data)
        if not done:
            log.info(f"Do something with {modifier=} {character=} {data=}")
            if modifier == 0:
                done = self.__quick_search.do_quick_search(character)
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        done = BnoteApp.input_bramigraph(self, modifier, bramigraph)
        if not done:
            log.info(f"Do something with {modifier=} {bramigraph=}")
            function_switcher = {
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_LEFT): self._caret_previous_part,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT): self._caret_next_part,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_UP): self._caret_up,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_DOWN): self._caret_down,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB): self._caret_previous_part,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_TAB): self._caret_next_part,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_F3): self.__quick_search.do_quick_search_again,
                # (0, Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE): self.__quick_search.clear,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_HOME): self._caret_start_of_document,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_END): self._caret_end_of_document,
                (0, Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN): self.__action_on_current_line,

                (Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_LEFT): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT): self._caret_right,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_UP): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_DOWN): self._caret_down,

                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_LEFT): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT): self._caret_right,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_UP): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_DOWN): self._caret_down,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_HOME): self._caret_start_of_document,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, Keyboard.BrailleFunction.BRAMIGRAPH_END): self._caret_end_of_document,

                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL + Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_LEFT): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL + Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT): self._caret_right,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL + Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_UP): self._caret_up,
                (Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL + Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT, Keyboard.BrailleFunction.BRAMIGRAPH_DOWN): self._caret_down,
            }

            settings_function = function_switcher.get((modifier, bramigraph), None)
            if settings_function:
                # Execute the function
                settings_function()
                done = True
        return done

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        log.debug(f"{modifier=} {position=} {key_type=}")
        done = super(SettingsApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            if key_type == Keyboard.InteractiveKeyType.CLIC:
                self.__action_on_current_line()
                done = True
        return done

    def input_function(self, *args, **kwargs):
        """
        Function from elf._function_queue of bnote_start.py
        :param args:
        :param kwargs:
        :return: True if function done
        """
        if not len(args):
            return False
        function_id = args[0]
        done = False
        if function_id == FunctionId.FUNCTION_END_SCAN_WIFI:
            self._end_scan_wifi(**kwargs)
            done = True
        else:
            # Call base class decoding.
            done = super(SettingsApp, self).input_function(*args, **kwargs)
        return done

    # DEPLACEMENTS DANS LE DOCUMENT.
    def _forward_display(self):
        log.debug("_forward_display")
        if not self._braille_display.forward():
            self._caret_down()

    def _backward_display(self):
        log.debug("_backward_display")
        if not self._braille_display.backward():
            self._caret_up()

    # Call the method to sync the self.__document_area_current_line_index to the wanted menu item
    def _move_document_area_current_line_index_to(self, section, key):
        index = -1
        for line in self.__document_area:
            index += 1
            if section == line["section"] and key == line["key"]:
                self.__document_area_current_line_index = index
                break

    def _caret_up(self):
        log.debug("_caret_up")
        if self.__document_area_current_line_index > 0:
            self.__document_area_current_line_index -= 1
            log.debug("line_index:{}".format(self.__document_area_current_line_index))
            self.__refresh_braille_display()

    def _caret_down(self):
        log.debug("_caret_down")
        if self.__document_area_current_line_index + 1 < len(self.__document_area):
            self.__document_area_current_line_index += 1
            log.debug("line_index:{}".format(self.__document_area_current_line_index))
            self.__refresh_braille_display()

    def _caret_left(self):
        log.debug("_caret_left")
        self._backward_display()

    def _caret_right(self):
        log.debug("_caret_right")
        self._forward_display()

    def _caret_start_of_document(self):
        self.__document_area_current_line_index = 0
        self.__refresh_braille_display()

    def _caret_end_of_document(self):
        self.__document_area_current_line_index = len(self.__document_area) - 1
        self.__refresh_braille_display()

    def _caret_previous_part(self):
        for index in range(self.__document_area_current_line_index, -1, -1):
            if self.__document_area[index]['is_tab_stop'] and index != self.__document_area_current_line_index:
                self.__document_area_current_line_index = index
                self.__update_document()
                self.__refresh_braille_display()
                break

    def _caret_next_part(self):
        for index in range(self.__document_area_current_line_index, len(self.__document_area)):
            if self.__document_area[index]['is_tab_stop'] and index != self.__document_area_current_line_index:
                self.__document_area_current_line_index = index
                self.__update_document()
                self.__refresh_braille_display()
                break

    def __quick_search_move_call_back(self, text_to_find) -> bool:
        text_to_find = text_to_find.lower()

        # Search from self._line_index to end of list
        for index, line in enumerate(self.__document_area):
            if line["data_line_text"].lower().find(text_to_find) != -1 and \
                    index >= self.__document_area_current_line_index:
                self.__document_area_current_line_index = index
                self.__refresh_braille_display()
                return True

        # Search from 0 to self.__focused_file_index in the list
        for index, line in enumerate(self.__document_area):
            if line["data_line_text"].lower().find(text_to_find) != -1 and \
                    index < self.__document_area_current_line_index:
                self.__document_area_current_line_index = index
                self.__refresh_braille_display()
                return True

        return False

    def __action_on_current_line(self, **kwargs):
        if self.__document_area_current_line_index in range(0, len(self.__document_area)):
            section = self.__document_area[self.__document_area_current_line_index]["section"]
            key = self.__document_area[self.__document_area_current_line_index]["key"]
            log.info(f"action on {section=} {key=}")
            if section and key:
                the_action_and_action_param = self.__action_and_action_param[(section, key)]
                the_action_and_action_param['action'](**the_action_and_action_param['action_param'])

    def set_data_line(self, text, start):
        braille_static = BnoteApp.lou.to_dots_8(text)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(text, braille_static, braille_blinking, start)

    # Refresh braille display
    def __refresh_braille_display(self, offset=0):
        log.debug("_refresh_braille_display line<{}>".format(self.__document_area_current_line_index))

        text = self.__document_area[self.__document_area_current_line_index]["data_line_text"]
        braille_type = Settings().data['system']['braille_type']
        if (braille_type == 'grade1') or (braille_type == 'grade2'):
            static_dots = BnoteApp.lou.to_dots_6(text)
        else:
            static_dots = BnoteApp.lou.to_dots_8(text)

        braille_blinking = "\u2800" * len(static_dots)
        self._braille_display.set_data_line(text, static_dots, braille_blinking, offset)

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each app if necessary.
        """
        self.__update_document()
        self.__refresh_braille_display()

    # Function for hide menu
    def _exec_clock(self):
        pass
    def _exec_synthese(self):
        pass
    def _exec_bluetooth(self):
        pass
    def _exec_editor(self):
        pass
    def _exec_math(self):
        pass
    def _exec_music(self):
        pass
    def _exec_agenda(self):
        pass

    def refresh_examen(self):
        if not Exam().examen['bluetooth']:
            self._menu.get_object(self._exec_bluetooth).hide()
        if not Exam().examen['editor']:
            self._menu.get_object(self._exec_editor).hide()
            self._menu.get_object(self._exec_math).hide()
        elif not Exam().examen['math']:
            self._menu.get_object(self._exec_math).hide()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        if Settings().data['mode examen']['actif']:
            self._menu.get_object(self._exec_desactivate_examen).unhide()
            self._menu.get_object(self._exec_activate_examen).hide()
            self._menu.get_object(self._exec_clock).hide()
            self._menu.get_object(self._exec_synthese).hide()
            self._menu.get_object(self._exec_music).hide()
            self._menu.get_object(self._exec_agenda).hide()
            self._menu.get_object(self._exec_reset).hide()
            self.refresh_examen()
        # else:
        #     self._menu.get_object(self._exec_desactivate_examen).hide()
        #     self._menu.get_object(self._exec_activate_examen).unhide()
        #     self._menu.get_object(self._exec_clock).unhide()
        #     self._menu.get_object(self._exec_synthese).unhide()
        #     self._menu.get_object(self._exec_editor).unhide()
        #     self._menu.get_object(self._exec_math).unhide()
        #     self._menu.get_object(self._exec_music).unhide()
        #     self._menu.get_object(self._exec_agenda).unhide()
        #     self._menu.get_object(self._exec_reset).unhide()
        self.__update_document()
        self.__refresh_braille_display()
