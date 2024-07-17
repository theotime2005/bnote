"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os.path
from pathlib import Path
import threading
import time
from bnote.apps.agenda.agenda_app import AgendaApp
from bnote.apps.bt.bluetooth_app import BluetoothApp
from bnote.apps.fman.file_manager import FileManager
from bnote.apps.fman.file_manager_app import FileManagerApp
from bnote.apps.edt.editor_app import EditorApp
import bnote.apps.edt.edt as editor
from bnote.apps.media.mp3_app import Mp3App
from bnote.apps.music.music_app import MusicApp
from bnote.apps.daisy.daisy_app import DaisyApp
from bnote.apps.settings.settings_app import SettingsApp
from bnote.apps.skeleton.skeleton_app import SkeletonApp
from bnote.apps.timer.timer_app import TimerApp
from bnote.apps.wikipedia.wikipedia_app import WikipediaApp
from bnote.speech.speech import SpeechManager
from bnote.stm32 import stm32_keys
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.stm32.stm32_protocol import Stm32Frame
from bnote.apps.games.mines_app import MinesApp
from bnote.apps.games.master_mind_app import MasterMindApp
from bnote.apps.braille_learning.write_word_app import WriteWordApp
from bnote.apps.braille_learning.operation_app import OperationApp
from bnote.apps.media.radio_app import RadioApp
from bnote.apps.translator.translator_app import TranslatorApp
from bnote.tools.audio_player import AudioPlayer
from bnote.tools.keyboard import Keyboard
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools import crash_report
from bnote.tools.settings import Settings
from bnote.tools.volume import Volume
from bnote.tools.volume_speed_dialog_box import VolumeDialogBox
import bnote.ui as ui
# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, INTERNAL_LOG
import bnote.__init__ as version

log = ColoredLogger(__name__)
log.setLevel(INTERNAL_LOG)


class Internal:
    class AppDescriptor:
        def __init__(self, parent, name, action, is_hide, is_auto_switch):
            # '' is item in main menu, 'sub_menu' if sub menu, '<parent menu>' if submenu item.
            self.parent = parent
            # translated name.
            self.name = name
            # action on menu function.
            self.action = action
            # Define if at first display this app is hide or not. (This parameter is not dynamically change)
            self.is_hide = is_hide
            # Define if this application is exclude or not to application switch wirh shorcut (Ctrl+Tab or Ctrl+Shift+Tab)
            self.is_auto_switch = is_auto_switch
            # Current app. instance (Dynamically change for someones)
            self.instance = None

    def __init__(self, lou, put_in_function_queue, put_in_stm32_tx_queue):
        # Applications descriptor.
        self.apps_descriptor = {
            'usb_1': self.AppDescriptor('', _("usb-&a"), self._exec_usb_1, is_hide=False, is_auto_switch=False),
            'usb_2': self.AppDescriptor('', _("usb-&b"), self._exec_usb_2, is_hide=False, is_auto_switch=False),
            'bluetooth_1': self.AppDescriptor('', "bluetooth_&1", self._exec_bluetooth_1, is_hide=True, is_auto_switch=False),
            'bluetooth_2': self.AppDescriptor('', "bluetooth_&2", self._exec_bluetooth_2, is_hide=True, is_auto_switch=False),
            'bluetooth_3': self.AppDescriptor('', "bluetooth_&3", self._exec_bluetooth_3, is_hide=True, is_auto_switch=False),
            'bluetooth_4': self.AppDescriptor('', "bluetooth_&4", self._exec_bluetooth_4, is_hide=True, is_auto_switch=False),
            'editor_1': self.AppDescriptor('', "editor_&5", self._exec_editor_1, is_hide=True, is_auto_switch=True),
            'editor_2': self.AppDescriptor('', "editor_&6", self._exec_editor_2, is_hide=True, is_auto_switch=True),
            'editor_3': self.AppDescriptor('', "editor_&7", self._exec_editor_3, is_hide=True, is_auto_switch=True),
            'editor_4': self.AppDescriptor('', "editor_&8", self._exec_editor_4, is_hide=True, is_auto_switch=True),
            'editor_5': self.AppDescriptor('', "editor_&9", self._exec_editor_5, is_hide=True, is_auto_switch=True),
            'explorer': self.AppDescriptor('', self.__app_translate('explorer'), self._exec_explorer, is_hide=False, is_auto_switch=True),
            'settings': self.AppDescriptor('', self.__app_translate('settings'), self._exec_settings, is_hide=False, is_auto_switch=True),
            'agenda': self.AppDescriptor('', self.__app_translate('agenda'), self._exec_agenda, is_hide=False, is_auto_switch=True),
            'radio': self.AppDescriptor('', self.__app_translate('radio'), self._exec_radio, is_hide=False, is_auto_switch=True),
            'mp3': self.AppDescriptor('', self.__app_translate('mp3'), self._exec_mp3, is_hide=False, is_auto_switch=True),
            'wikipedia': self.AppDescriptor('', self.__app_translate('wikipedia'), self._exec_wikipedia, is_hide=False, is_auto_switch=True),
            'timer': self.AppDescriptor('', self.__app_translate('timer'), self._exec_timer, is_hide=False, is_auto_switch=True),
            'translator': self.AppDescriptor('', _("trans&lator"), self._exec_translator, is_hide=False, is_auto_switch=True),
            'write_word': self.AppDescriptor('', self.__app_translate('write_word'), self._exec_write_word, is_hide=False, is_auto_switch=True),
            'operation': self.AppDescriptor('', self.__app_translate('operation'), self._exec_operation, is_hide=False, is_auto_switch=True),
            'mines': self.AppDescriptor('', self.__app_translate('mines'), self._exec_mines, is_hide=False, is_auto_switch=True),
            'mastermind': self.AppDescriptor('', self.__app_translate('mastermind'), self._exec_mastermind, is_hide=False, is_auto_switch=True),
            'skeleton': self.AppDescriptor('', self.__app_translate('skeleton'), self._exec_skeleton, is_hide=False, is_auto_switch=True),
            'more_apps_menu': self.AppDescriptor('sub_menu', self.__app_translate('more_apps_menu'), self._more_apps_menu, is_hide=False, is_auto_switch=True),
            'explorer_2': self.AppDescriptor('more_apps_menu', self.__app_translate('explorer_2'), self._exec_explorer_2, is_hide=False, is_auto_switch=True),
            'settings_2': self.AppDescriptor('more_apps_menu', self.__app_translate('settings_2'), self._exec_settings_2, is_hide=False, is_auto_switch=True),
            'agenda_2': self.AppDescriptor('more_apps_menu', self.__app_translate('agenda_2'), self._exec_agenda_2, is_hide=False, is_auto_switch=True),
            'radio_2': self.AppDescriptor('more_apps_menu', self.__app_translate('radio_2'), self._exec_radio_2, is_hide=False, is_auto_switch=True),
            'mp3_2': self.AppDescriptor('more_apps_menu', self.__app_translate('mp3_2'), self._exec_mp3_2, is_hide=False, is_auto_switch=True),
            'wikipedia_2': self.AppDescriptor('more_apps_menu', self.__app_translate('wikipedia_2'), self._exec_wikipedia_2, is_hide=False, is_auto_switch=True),
            'timer_2': self.AppDescriptor('more_apps_menu', self.__app_translate('timer_2'), self._exec_timer_2, is_hide=False, is_auto_switch=True),
            'translator_2': self.AppDescriptor('more_apps_menu', _("trans&lator"), self._exec_translator_2, is_hide=False, is_auto_switch=True),
            'write_word_2': self.AppDescriptor('more_apps_menu', self.__app_translate('write_word_2'), self._exec_write_word_2, is_hide=False, is_auto_switch=True),
            'operation_2': self.AppDescriptor('more_apps_menu', self.__app_translate('operation_2'), self._exec_operation_2, is_hide=False, is_auto_switch=True),
            'mines_2': self.AppDescriptor('more_apps_menu', self.__app_translate('mines_2'), self._exec_mines_2, is_hide=False, is_auto_switch=True),
            'mastermind_2': self.AppDescriptor('more_apps_menu', self.__app_translate('mastermind_2'), self._exec_mastermind_2, is_hide=False, is_auto_switch=True),
        }
        self.apps_editor = ('editor_1', 'editor_2', 'editor_3', 'editor_4', 'editor_5')
        self.apps_bluetooth = ('bluetooth_1', 'bluetooth_2', 'bluetooth_3', 'bluetooth_4')
        # Filter some apps exclude for next/previous apps function
        self.apps = ('usb_1', 'usb_2', *self.apps_bluetooth)
        self.lou = lou
        self._put_in_function_queue = put_in_function_queue
        self._put_in_stm32_tx_queue = put_in_stm32_tx_queue
        self._previous_command_key_data = b"\x00\x00"
        # Construct menu_item_list from bnote.apps_list
        menu_item_list = []
        for key, app_descriptor in self.apps_descriptor.items():
            # Construct main menu bar : Add all apps except games and media and b.braille
            if app_descriptor.parent == '':
                menu_item_list.append(
                    ui.UiMenuItem(
                        name=app_descriptor.name,
                        action=app_descriptor.action,
                        shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_WIN,
                        shortcut_key=self._shortcut_from_label(app_descriptor.name),
                        is_hide=app_descriptor.is_hide
                    )
                )
        # Add apps submenu
        for key, app_descriptor in self.apps_descriptor.items():
            if app_descriptor.parent == 'sub_menu':
                submenu_items = []
                for submenu_key, submenu_app_descriptor in self.apps_descriptor.items():
                    if submenu_app_descriptor.parent == key:
                        submenu_items.append(ui.UiMenuItem(name=submenu_app_descriptor.name, action=submenu_app_descriptor.action))
                # Add 'braille_learning' sub menu
                menu_item_list.append(
                    ui.UiMenuBar(name=app_descriptor.name, action=app_descriptor.action, menu_item_list=submenu_items),
                )
        # Add turn off sub-menu
        menu_item_list.append(ui.UiMenuItem(name=_("transport"), action=self._exec_ask_transport)),
        menu_item_list.append(ui.UiMenuItem(name=_("shutdown"), action=self._exec_ask_shutdown)),
        # Add menu bar title.
        self._menu = ui.UiMenuBar(
            name=_("applications-") + version.__version__,
            is_root=True,
            menu_item_list=menu_item_list
        )
        # When self._current_app is None the apps menu bar is displayed.
        self._current_app = None
        self.set_current_app(None)
        # Define the root menu bar.
        self._menu.reset_container()
        # Hide games and media if disable in settings
        self.__hide_unhide_menu_items()

        # Check crash report.
        report_a_crash = crash_report.crash_encountered()
        # Create apps instance.
        self.apps_descriptor["explorer"].instance = FileManagerApp(self._put_in_function_queue,
                                                                   report_a_crash=report_a_crash)
        if report_a_crash:
            # Automatically open the explorer if a crash has occurred.
            self._exec_explorer()
        else:
            # Delete the tmp folder at each clean start.
            FileManager.clear_tmp_file()

        # Démarre le time 1 seconde.
        self.start_one_second_timer()

        # Autorize le vocal
        SpeechManager().enable()

        # Start the MidiPlayer
        # MidiPlayer()

        # Save braille_device_caracteristics into settings
        Settings().data['stm32']['name'] = braille_device_characteristics.get_name()
        Settings().data['stm32']['len'] = braille_device_characteristics.get_braille_display_length()
        Settings().data['stm32']['firmware'] = braille_device_characteristics.get_firmware_version()
        Settings().data['stm32']['serial'] = braille_device_characteristics.get_serial_number()
        Settings().save()

        # Verify agenda events only if not crash
        if not report_a_crash:
            self.verify_agenda_or_restore_editor()

    def verify_agenda_or_restore_editor(self):
        if Settings().data['agenda']['remember'] == "same" or Settings().data['agenda']['remember'] == "same_tomorrow":
            if AgendaApp(self._put_in_function_queue).ask_event_same_day():
                self._exec_agenda()
                return self._put_in_function_queue(FunctionId.FUNCTION_AGENDA_SAME_DAY)
        elif Settings().data['agenda']['remember'] == "tomorrow" or Settings().data['agenda']['remember'] == "same_tomorrow":
            if AgendaApp(self._put_in_function_queue).ask_event_next_day():
                self._exec_agenda()
                return self._put_in_function_queue(FunctionId.FUNCTION_AGENDA_NEXT_DAY)
        return self.restore_editor()

    def restore_editor(self):
        if editor.Context.is_integrity_then_delete():
            while True:
                editor_app = EditorApp(self._put_in_function_queue, None)
                filename = editor_app.get_filename()
                if filename:
                    self.__add_editor_app(language="FR", filename=Path(filename), editor_app=editor_app)
                    if editor_app.was_focused():
                        self.set_current_app(editor_app)
                else:
                    break
        else:
            # Clean up all context files.
            editor.Context.clean_up_context_files()
            return self._put_in_function_queue(FunctionId.APPLICATIONS)

    def __str__(self):
        return "{}".format(self._menu)

    @staticmethod
    def _shortcut_from_label(name):
        # '&' treatment, use '\u2800' as temporary character.
        pos = name.find('&')
        shortcut = ""
        if pos >= 0:
            shortcut = name[pos + 1].lower()
        return shortcut

    @staticmethod
    def __app_translate(key):
        translations = {
            "explorer": _("&explorer"),
            "settings": _("&settings"),
            "agenda": _("a&genda"),
            "radio": _("&radio"),
            "mp3": _("au&dio"),
            "wikipedia": _("wi&kipedia"),
            "timer": _("&timer"),
            "translator": _("trans&lator"),
            "write_word": _("&word game"),
            "operation": _("mat&h game"),
            "mines": _("&mines"),
            "mastermind": _("mas&termind"),
            "skeleton": _("s&keleton"),
            "more_apps_menu": _("m&ore apps..."),
        }
        # Handle keys ending with "_2" the same way
        if key.endswith("_2"):
            key = key[:-2]
        translation = translations.get(key)
        if translation is None:
            log.error(f"Unknown translation for {key}")
        # Return "?" for unknown keys
        return translation or "?"

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        braille_type = Settings().data["system"]['braille_type']
        self._menu.set_braille_type(braille_type)
        self._menu.set_name(_("applications-") + version.__version__)
        # translate apps menu.
        for key, app_descriptor in self.apps_descriptor.items():
            if not ((key in self.apps_editor) or (key in self.apps_bluetooth) or (key == 'usb_1') or (key == 'usb_2')):
                # Retranslate all menu app items except editor, bluetooth and usb apps.
                self._menu.rename_item(self.__app_translate(key), braille_type, app_descriptor.action)
        # Translate each app.
        for descriptor in self.apps_descriptor.values():
            app = descriptor.instance
            if app:
                app.translate_ui()

    def usb_app_name_changed(self, data):
        """
        Customized usb apps with the name of screen reader connected.
        """
        usb_a_name, usb_b_name = data
        log.info(f"usb name changed {usb_a_name=} {usb_b_name=}")
        braille_type = Settings().data["system"]['braille_type']
        if usb_a_name == "":
            self._menu.rename_item(_("usb_&a"), braille_type, self.apps_descriptor['usb_1'].action)
        else:
            self._menu.rename_item(usb_a_name, braille_type, self.apps_descriptor['usb_1'].action)
        if usb_b_name == "":
            self._menu.rename_item(_("usb_&b"), braille_type, self.apps_descriptor['usb_2'].action)
        else:
            self._menu.rename_item(usb_b_name, braille_type, self.apps_descriptor['usb_2'].action)
        if not self._current_app:
            # Refresh menu.
            self._menu.ask_update_braille_display()
    def reset_app_menu(self):
        if not self._current_app:
            self._menu.reset_container()

    def __hide_unhide_menu_items(self):
        hidden_menu = [
            ('app_explorer', self._exec_explorer, self._exec_explorer_2),
            ('app_settings', self._exec_settings, self._exec_settings_2),
            ('app_mp3', self._exec_mp3, self._exec_mp3_2),
            ('app_radio', self._exec_radio, self._exec_radio_2),
            ('app_wikipedia', self._exec_wikipedia, self._exec_wikipedia_2),
            ('app_mines', self._exec_mines, self._exec_mines_2),
            ('app_mastermind', self._exec_mastermind, self._exec_mastermind_2),
            ('app_timer', self._exec_timer, self._exec_timer_2),
            ('app_translator', self._exec_translator, self._exec_translator_2),
            ('app_agenda', self._exec_agenda, self._exec_agenda_2),
            ('app_write_word', self._exec_write_word, self._exec_write_word_2),
            ('app_operation', self._exec_operation, self._exec_operation_2),
        ]
        # Hide/unhide application in main menu/more apps menu.
        for app_key, action_1, action_2 in hidden_menu:
            if Settings().data['system'][app_key] == 'main_apps_menu':
                self._menu.get_object(action_1).unhide()
                self._menu.get_object(action_2).hide()
            elif Settings().data['system'][app_key] == 'more_apps_menu':
                self._menu.get_object(action_1).hide()
                self._menu.get_object(action_2).unhide()
            else:
                self._menu.get_object(action_1).hide()
                self._menu.get_object(action_2).hide()
        if Settings().data['system']['developer']:
            self._menu.get_object(self._exec_skeleton).unhide()
        else:
            self._menu.get_object(self._exec_skeleton).hide()
        if self._menu.get_object(self._more_apps_menu).unhide_object_count() == 0:
            self._menu.get_object(self._more_apps_menu).hide()
        else:
            self._menu.get_object(self._more_apps_menu).unhide()

    def set_current_app(self, application):
        self._current_app = application
        if self._current_app:
            if isinstance(self._current_app, BluetoothApp):
                if self._current_app.activate_channel():
                    self._put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BLUETOOTH_FUNCTION_ENTER, data=b''))
            else:
                self._current_app.refresh_app()
        else:
            # Display from start of menu
            self._menu.reset_container()
            # Hide media and games if disable in settings
            self.__hide_unhide_menu_items()

        # Force la sortie du BT si par exemple le screenreader est à l'origine de la destruction du BT (veille
        # du smartphone ou arret PC)
        if not self._current_app or not isinstance(self._current_app, BluetoothApp):
            self._put_in_stm32_tx_queue(Stm32Frame(key=stm32_keys.KEY_BLUETOOTH_FUNCTION_EXIT, data=b''))

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        if self._current_app:
            # Display current application.
            return self._current_app.get_data_line(force_refresh)
        else:
            # Display apps menu bar.
            return self._menu.get_data_line(force_refresh)

    def _exec_application_menu(self):
        log.info("_exec_application_menu")
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    def _exec_usb_1(self):
        """
        Switch to usb mode
        :return: (None, MainAppId.USB)
        """
        log.info("exec_usb")
        self._menu.reset_container()
        self._put_in_function_queue(FunctionId.USB, channel=1)

    def _exec_usb_2(self):
        """
        Switch to usb mode
        :return: (None, MainAppId.USB)
        """
        log.info("exec_usb")
        self._menu.reset_container()
        self._put_in_function_queue(FunctionId.USB, channel=2)

    def _exec_explorer(self):
        log.info("exec_explorer")
        app_instance = self.apps_descriptor['explorer'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_explorer_2(self):
        self._exec_explorer()

    def _exec_agenda(self):
        log.info("exec_agenda")
        if not self.apps_descriptor['agenda'].instance:
            self.apps_descriptor['agenda'].instance = AgendaApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['agenda'].instance)

    def _exec_agenda_2(self):
        self._exec_agenda()

    def _exec_write_word(self):
        log.info("exec_write_word")
        if not self.apps_descriptor['write_word'].instance:
            self.apps_descriptor['write_word'].instance = WriteWordApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['write_word'].instance)

    def _exec_write_word_2(self):
        self._exec_write_word()

    def _exec_operation(self):
        log.info("exec_operation")
        if not self.apps_descriptor['operation'].instance:
            self.apps_descriptor['operation'].instance = OperationApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['operation'].instance)

    def _exec_operation_2(self):
        self._exec_operation()

    def _exec_skeleton(self):
        log.info("exec_skeleton")
        if not self.apps_descriptor['skeleton'].instance:
            self.apps_descriptor['skeleton'].instance = SkeletonApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['skeleton'].instance)

    def _exec_timer(self):
        if not self.apps_descriptor['timer'].instance:
            self.apps_descriptor['timer'].instance=TimerApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['timer'].instance)

    def _exec_timer_2(self):
        self._exec_timer()

    def _exec_translator(self, **kwargs):
        if not self.apps_descriptor['translator'].instance:
            self.apps_descriptor['translator'].instance = TranslatorApp(self._put_in_function_queue, **kwargs)
        else:
            self.apps_descriptor['translator'].instance.change_source(**kwargs)
        self.set_current_app(self.apps_descriptor['translator'].instance)

    def _exec_translator_2(self, **kwargs):
        return self._exec_translator(**kwargs)

    def _exec_radio(self):
        log.info("exec_radio")
        if not self.apps_descriptor['radio'].instance:
            self.apps_descriptor['radio'].instance = RadioApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['radio'].instance)

    def _exec_radio_2(self):
        self._exec_radio()

    def _exec_mp3(self, **kwargs):
        log.info("exec_mp3")
        if not self.apps_descriptor['mp3'].instance:
            self.apps_descriptor['mp3'].instance = Mp3App(self._put_in_function_queue, **kwargs)
        else:
            self.apps_descriptor['mp3'].instance.set_list_and_play(**kwargs)
        self.set_current_app(self.apps_descriptor['mp3'].instance)

    def _exec_mp3_2(self, **kwargs):
        self._exec_mp3()

    def _exec_wikipedia(self, **kwargs):
        if not self.apps_descriptor['wikipedia'].instance:
            self.apps_descriptor['wikipedia'].instance = WikipediaApp(self._put_in_function_queue, **kwargs)
        self.set_current_app(self.apps_descriptor['wikipedia'].instance)

    def _exec_wikipedia_2(self, **kwargs):
        self._exec_wikipedia()

    def _exec_mines(self):
        log.info("exec_mines")
        if not self.apps_descriptor['mines'].instance:
            self.apps_descriptor['mines'].instance = MinesApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['mines'].instance)

    def _exec_mines_2(self):
        self._exec_mines()

    def _exec_mastermind(self):
        log.info("exec_mastermind")
        if not self.apps_descriptor['mastermind'].instance:
            self.apps_descriptor['mastermind'].instance = MasterMindApp(self._put_in_function_queue)
        self.set_current_app(self.apps_descriptor['mastermind'].instance)

    def _exec_mastermind_2(self):
        self._exec_mastermind()

    def _more_apps_menu(self):
        pass

    def _exec_editor_1(self):
        log.info("_exec_editor_1")
        app_instance = self.apps_descriptor['editor_1'].instance
        if app_instance:
            self.set_current_app(app_instance)
        # self.set_current_app.refresh_current_item(True)

    def _exec_editor_2(self):
        log.info("_exec_editor_2")
        app_instance = self.apps_descriptor['editor_2'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_editor_3(self):
        log.info("_exec_editor_3")
        app_instance = self.apps_descriptor['editor_3'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_editor_4(self):
        log.info("_exec_editor_4")
        app_instance = self.apps_descriptor['editor_4'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_editor_5(self):
        log.info("_exec_editor_5")
        app_instance = self.apps_descriptor['editor_5'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_bluetooth_1(self):
        log.info("_exec_bluetooth_1")
        app_instance = self.apps_descriptor['bluetooth_1'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_bluetooth_2(self):
        log.info("_exec_bluetooth_2")
        app_instance = self.apps_descriptor['bluetooth_2'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_bluetooth_3(self):
        log.info("_exec_bluetooth_3")
        app_instance = self.apps_descriptor['bluetooth_3'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_bluetooth_4(self):
        log.info("_exec_bluetooth_4")
        app_instance = self.apps_descriptor['bluetooth_4'].instance
        if app_instance:
            self.set_current_app(app_instance)

    def _exec_settings(self):
        log.info("exec_settings")
        if not self.apps_descriptor['settings'].instance:
            self.apps_descriptor['settings'].instance = SettingsApp(self._put_in_function_queue,
                                                                    self._put_in_stm32_tx_queue)
        self.set_current_app(self.apps_descriptor['settings'].instance)

    def _exec_settings_2(self):
        self._exec_settings()

    def _exec_ask_transport(self):
        log.info("exec_transport")
        self._menu.reset_container()
        self._put_in_function_queue(FunctionId.ASK_TRANSPORT)

    def _exec_ask_shutdown(self):
        log.info("exec_shutdown")

        self._put_in_function_queue(FunctionId.ASK_SHUTDOWN)

    def _goto_bluetooth_device(self, **kwargs):
        bt_connect={
            0: self._exec_bluetooth_1(),
            1: self._exec_bluetooth_2(),
            2: self._exec_bluetooth_3(),
            3: self._exec_bluetooth_4()
        }
        bt_connect[kwargs['device']]
        self._put_in_function_queue(FunctionId.FUNCTION_BLUETOOTH_WRITE, **kwargs)

    def __one_second_callback(self):
        self._put_in_function_queue(FunctionId.FUNCTION_ONE_SECOND_TIMER_ELAPSED)
        if BnoteApp.one_second_timer:
            self.start_one_second_timer()

    def start_one_second_timer(self):
        BnoteApp.one_second_timer = threading.Timer(1, self.__one_second_callback)
        BnoteApp.one_second_timer.start()

    def cancel_one_second_timer(self):
        # log.critical("cancel_one_second_timer !!!!!!!!!!!!!!!!!!!")
        if BnoteApp.one_second_timer:
            # log.critical(f"time={time.time()}")
            BnoteApp.one_second_timer.cancel()
            BnoteApp.one_second_timer = None
            # log.critical(f"time={time.time()}")

    @staticmethod
    def stop_speaking_if_crash():
        SpeechManager().disable()

    # @staticmethod
    # def stop_midi_thread():
    #    MidiPlayer().stop_midi_thread()

    def __change_editor_name(self, app_instance, new_file, old_file):
        self.apps_descriptor['explorer'].instance.remove_locked_file(old_file)
        self.apps_descriptor['explorer'].instance.append_locked_file(new_file)
        # rename menu item.
        editor_apps = self.__get_used_dynamic_apps(self.apps_editor)
        for editor_app in editor_apps:
            if app_instance == self.apps_descriptor[editor_app].instance:
                ui_object = self._menu.get_object_from_action(self.apps_descriptor[editor_app].action)
                ui_object.rename_without_shortcut(Path(app_instance.get_filename()).name)
                break

    def input_function(self, *args, **kwargs) -> bool:
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
        if self._current_app:
            # FUNCTION ON CURRENT_APP.
            if function_id == FunctionId.FUNCTION_ONE_SECOND_TIMER_ELAPSED:
                # Call on_timer on the current BNoteApp application.
                self._current_app.on_timer()
                done = True
        if not done:
            if 'app' in kwargs.keys():
                # FUNCTION DESTINED TO A SPECIFIC APP. CURRENT APP.
                app_instance = kwargs['app']
                if function_id == FunctionId.FUNCTION_SAVE_AND_DELETE_ORIGINAL:
                    log.error(f"change locked file from {app_instance.get_original_filename()} to {app_instance.get_filename()}")
                    self.__change_editor_name(app_instance, app_instance.get_filename(), app_instance.get_original_filename())
                    # pass function to concerned editor.
                    done = app_instance.input_function(*args, **kwargs)
                elif function_id == FunctionId.FUNCTION_CHANGE_LOCKED_FILE:
                    log.error(f"FUNCTION_CHANGE_LOCKED_FILE {kwargs['old_file']=} {kwargs['new_file']=}")
                    self.__change_editor_name(app_instance, kwargs['new_file'], kwargs['old_file'])
                    done = True
                else:
                    done = kwargs['app'].input_function(*args, **kwargs)
                # Refresh app menu or current app.
                self.__refresh_display_after_function()
            else:
                if self._current_app:
                    # FUNCTION DESTINED TO THE CURRENT APP.
                    done = self._current_app.input_function(*args, **kwargs)
        if not done:
            # FUNCTION NOT TREATED BY CURRENT APP OR DESTINED APP.
            done = True
            if function_id != FunctionId.FUNCTION_ONE_SECOND_TIMER_ELAPSED:
                # Log all function except FUNCTION_ONE_SECOND_TIMER_ELAPSED
                log.info("function to treat args={} kwargs={}".format(args, kwargs))
            if function_id == FunctionId.APPLICATIONS:
                self.set_current_app(None)
                self._menu.ask_update_braille_display()
            elif function_id==FunctionId.FUNCTION_RESTOR_AFTER_AGENDA:
                self.restore_editor()
                self.__refresh_display_after_function()
            elif function_id==FunctionId.FUNCTION_END_TIMER:
                self._exec_timer()
            elif function_id==FunctionId.FUNCTION_OPEN_BLUETOOTH:
                self._goto_bluetooth_device(**kwargs)
            elif function_id == FunctionId.SHUTDOWN:
                self.__exec_shutdown()
            elif function_id == FunctionId.FUNCTION_OPEN_TRANSLATOR:
                self._exec_translator(**kwargs)
            elif function_id == FunctionId.FUNCTION_SETTINGS_CHANGE:
                self.__settings_change(**kwargs)
            elif function_id == FunctionId.OPEN_THE_FILE_PLEASE:
                self.__add_editor_app(**kwargs)
            elif function_id == FunctionId.OPEN_THE_MP3_FILE_PLEASE:
                self._exec_mp3(**kwargs)
            elif function_id == FunctionId.FUNCTION_CLOSE_EDITOR:
                self.__remove_editor_app(**kwargs)
            elif function_id == FunctionId.FUNCTION_CLOSE_WIKIPEDIA:
                self.apps_descriptor['wikipedia'].instance = None
                self.set_current_app(None)
            elif function_id == FunctionId.FUNCTION_INTERNAL_NEXT_APP:
                self.__next_app()
            elif function_id == FunctionId.FUNCTION_INTERNAL_PREVIOUS_APP:
                self.__prev_app()
            elif function_id == FunctionId.RESTART_PLEASE:
                self.__restart_app()
            elif function_id == FunctionId.FUNCTION_ONE_SECOND_TIMER_ELAPSED:
                # Here: treatment each seconds if necessary.
                # This decoding is done to avoid a trace each second.
                pass
            elif function_id == FunctionId.FUNCTION_DELETE_ORIGINAL:
                # The file deletion for imported file as .odt, .docx... is removed
                # FileManager.delete_file(kwargs['filename'])
                # Synch current explorer file on the .txt file.
                self.apps_descriptor['explorer'].instance.synch_to_file(Path(str(kwargs['filename']) + ".txt"))
                self.__refresh_display_after_function()
            elif function_id == FunctionId.FUNCTION_APPEND_BLUETOOTH:
                self.__add_bluetooth_app(*args, **kwargs)
            elif function_id == FunctionId.FUNCTION_REMOVE_BLUETOOTH:
                self.__remove_bluetooth_app(*args, **kwargs)
            else:
                log.warning(f"UNKNOWN FUNCTION {function_id}???")
                done = False
        return done

    def input_braille(self, data) -> bool:
        """
        Do what needs to be done for this braille key and return (refresh, object_id).
        :param data: braillekey from bnote.stm32
        :return: True if command treated, otherwise False
        """
        done = False
        # Globals shortcuts works only outside bluetooth app.
        if self._current_app and not isinstance(self._current_app, BluetoothApp):
            (braille_type, braille_modifier, braille_value) = BnoteApp.keyboard.decode_braille(BnoteApp.lou, data)
            log.info(f"{braille_type=} {braille_modifier=} {braille_value=}")
            if braille_modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_WIN:
                if braille_type == Keyboard.BrailleType.FUNCTION and \
                        braille_value == Keyboard.BrailleFunction.BRAMIGRAPH_LWIN:
                    self._put_in_function_queue(FunctionId.APPLICATIONS)
                    return True
                else:
                    # Windows+letter
                    ui_object = self.__do_global_shortcut(braille_value)
                    if ui_object:
                        treated, in_menu = ui_object.exec_action()
                        if not in_menu and self._current_app:
                            self._current_app.refresh_app()
                            return True
        # Volume control.
        (braille_type, braille_modifier, braille_value) = BnoteApp.keyboard.decode_braille(BnoteApp.lou, data)
        if braille_modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL \
                and braille_type == Keyboard.BrailleType.CHARACTER:
            if str(braille_value) == "-":
                # Anyhow, this key does volume down.
                done = self.__volume_down_from_shortcut()
                return done
            elif str(braille_value) == "+":
                # Anyhow, this key does volume up.
                done = self.__volume_up_from_shortcut()
                return done
            # elif key_id == Keyboard.KeyId.KEY_MEDIA_MUTE:
            #     # Anyhow, this key does volume mute.
            #     done = self.__mute_from_shortcut()

        # General braille event treatment.
        if self._current_app:
            log.info("call self._apps[self._current_app_index].input_character({})".format(data))
            done = self._current_app.input_braille(data)
        else:
            if braille_type == Keyboard.BrailleType.CHARACTER:
                done = self._menu.input_character(braille_modifier, str(braille_value), data)
            elif braille_type == Keyboard.BrailleType.FUNCTION:
                done = self._menu.input_bramigraph(braille_modifier, braille_value)
        return done

    def __do_global_shortcut(self, character):
        # Find object of menu.
        ui_object = self._menu.decode_shortcut(character)
        if ui_object:
            # Get app action
            action = self.__get_app_from_ui_object(ui_object)
            return ui_object
        return None

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = False
        if key_id == Keyboard.KeyId.KEY_MEDIA_VOLUME_DOWN:
            # Anyhow, this key does volume down.
            done = self.__volume_down_from_shortcut()
        elif key_id == Keyboard.KeyId.KEY_MEDIA_VOLUME_UP:
            # Anyhow, this key does volume up.
            done = self.__volume_up_from_shortcut()
        elif key_id == Keyboard.KeyId.KEY_MEDIA_MUTE:
            # Anyhow, this key does volume mute.
            done = self.__mute_from_shortcut()
        elif self._current_app is not None:
            log.info("call self._apps[self._current_app_index].input_command({})".format(data))
            done = self._current_app.input_command(data, modifier, key_id)
        else:
            if key_id != Keyboard.KeyId.KEY_NONE:
                if key_id == Keyboard.KeyId.KEY_APPLICATIONS:
                    # EXCEPTION: On applications menu bar KEY_APPLICATIONS display the main level.
                    menu = self._menu.get_root()
                    menu.switch_to_parent(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
                    # Reconstruct braille display.
                    self._menu.ask_update_braille_display()
                    done = True
                else:
                    done = self._menu.input_command(modifier=modifier, key_id=key_id)
        return done

    # Call from input_command
    def __volume_down_from_shortcut(self):
        level = VolumeDialogBox.volume_down(channel='radio', with_voice_feedback=False)
        self.__save_the_new_volume(level)
        return True

    def __volume_up_from_shortcut(self):
        level = VolumeDialogBox.volume_up(channel='radio', with_voice_feedback=False)
        self.__save_the_new_volume(level)
        return True

    @staticmethod
    def __mute_from_shortcut():
        if AudioPlayer().is_paused():
            AudioPlayer().resume()
        else:
            AudioPlayer().pause()
        return True

    @staticmethod
    def __save_the_new_volume(volume):
        # Save the new Volume in settings.
        Volume().set_volume(volume, channel='radio')
        Settings().save()
        AudioPlayer().set_volume()

    def input_interactive(self, data) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        (modifier, position, key_type) = BnoteApp.keyboard.decode_interactive(data)
        log.info(f"interactive key {modifier=} {position=} {key_type=}")
        if self._current_app is not None:
            if isinstance(self._current_app, BluetoothApp):
                done = self._current_app.exec_interactive(data)
            else:
                done = self._current_app.input_interactive(modifier, position, key_type)
        else:
            in_menu = self._menu.input_interactive(modifier, position, key_type)
            if not in_menu:
                # Stay in application selector
                self.reset_app_menu()
            done = True
        return done

    def __restart_app(self):
        # Do the things to terminate bnote from internal point of view.
        self.terminate_bnote()
        # Corrige #76 (message "redémarrage..." pas toujours visible quand on fait une mise à jour)
        time.sleep(1)
        os.popen('/usr/sbin/reboot -h now')

    def terminate_bnote(self):
        # First of all, Engage the shutdown process for apps (save user documents files if needed)
        self.shutdown_apps()
        # Stop the vocal
        SpeechManager().disable()
        # Stop the MidiPlayer thread
        # MidiPlayer().stop_midi_thread()
        # Unmount the usb flash drives
        FileManagerApp.unmount_all_usb_flash_drive()
        # Cancel the one second timer to be able to quit the program.
        self.cancel_one_second_timer()

    def shutdown_apps(self):
        for app_descriptor in self.apps_descriptor.values():
            if app_descriptor.instance:
                # Notify all applications.
                app_descriptor.instance.shutdown(self._current_app == app_descriptor.instance)
        for app_descriptor in self.apps_descriptor.values():
            if app_descriptor.instance:
                # Wait shutdown process of all applications.
                log.info("Shutdown on {}".format(app_descriptor.instance))
                while not app_descriptor.instance.shutdown_ended():
                    time.sleep(0.1)
        # Write integrity file to specify successfull shutdown.
        editor.Context.write_integrity_file()
        log.info("Shutdown process ended")

    @staticmethod
    def __exec_shutdown():
        # Execute shutdown only on RPi (not on dev's PC).
        os.popen('/usr/sbin/shutdown -h now')

    def __settings_change(self, **kwargs):
        if ((kwargs['section'] == 'system') and (kwargs['key'] == 'braille_type'))\
                or ((kwargs['section'] == 'system') and (kwargs['key'] == 'shortcuts_visible'))\
                or ((kwargs['section'] == 'system') and (kwargs['key'] == 'spaces_in_label')):
            # Reconstruct menu if braille switch to dot8, grade1 or grade2
            self.translate_ui()

    def __next_app(self):
        if not self._current_app:
            # No current app defined. => No action
            return True, None
        step = 1
        for key, app_descriptor in self.apps_descriptor.items():
            if step == 1:
                # Find current_app descriptor
                if self._current_app == app_descriptor.instance:
                    step = 2
            elif app_descriptor.is_auto_switch and app_descriptor.instance:
                # Activate the next application
                self.set_current_app(app_descriptor.instance)
                return True, None
        # Find the first application
        if step == 2:
            for key, app_descriptor in self.apps_descriptor.items():
                if app_descriptor.is_auto_switch and app_descriptor.instance:
                    # Activate the next application
                    self.set_current_app(app_descriptor.instance)
                    return True, None
        return True, None

    def __prev_app(self):
        if not self._current_app:
            # No current app defined. => No action
            return True, None
        step = 1
        for key, app_descriptor in reversed(self.apps_descriptor.items()):
            if step == 1:
                # Find current_app descriptor
                if self._current_app == app_descriptor.instance:
                    step = 2
            elif app_descriptor.is_auto_switch and app_descriptor.instance:
                # Activate the next application
                self.set_current_app(app_descriptor.instance)
                return True, None
        # Find the first application
        if step == 2:
            for key, app_descriptor in reversed(self.apps_descriptor.items()):
                if app_descriptor.is_auto_switch and app_descriptor.instance:
                    # Activate the next application
                    self.set_current_app(app_descriptor.instance)
                    return True, None
        return True, None

    def _get_app_descritor_from_action(self, action):
        # Find current app descriptor
        for key, app_descriptor in self.apps_descriptor.items():
            if app_descriptor.action == action:
                return key, app_descriptor
        return None

    def __get_available_dynamic_apps(self, apps_list):
        """
        get first menu object hidden of an application list
        :param apps_list:  is
          self.apps_editor = ['editor_1', 'editor_2', 'editor_3', 'editor_4', 'editor_5']
            or self.apps_bluetooth = ['bluetooth_1', 'bluetooth_2', 'bluetooth_3', 'bluetooth_4']
        :return: app_descriptor, ui_object
        """
        for app_id in apps_list:
            ui_object = self._menu.get_object(self.apps_descriptor[app_id].action)
            if ui_object.is_hide():
                return self.apps_descriptor[app_id], ui_object
        return None, None

    def __get_app_from_ui_object(self, ui_object):
        """
        get action associated to the ui_object of an application.
        :param ui_object:
        :return: action (callback function)
        """
        action = ui_object.get_action()
        for app_descriptor in self.apps_descriptor.values():
            if app_descriptor.action == action:
                return action
        return None

    def __get_used_dynamic_apps(self, apps_list):
        """
        get first menu object not hidden of an application list
        :param apps_list:  is
          self.apps_editor = ['editor_1', 'editor_2', 'editor_3', 'editor_4', 'editor_5']
            or self.apps_bluetooth = ['bluetooth_1', 'bluetooth_2', 'bluetooth_3', 'bluetooth_4']
        :return: sub apps_list
        """
        apps = [app for app in apps_list if not self._menu.get_object(self.apps_descriptor[app].action).is_hide()]
        return apps

    @staticmethod
    def __split_mac_name(bt_mac_name):
        if len(bt_mac_name.split(" ")) >= 2:
            return bt_mac_name.split(" ")[0], " ".join(bt_mac_name.split(" ")[1:])
        return "", ""

    def __add_bluetooth_app(self, *args, **kwargs):
        log.info(f"{kwargs=}")
        if 'id' in kwargs and 'name' in kwargs:
            id_ = kwargs['id']
            mac_name = kwargs['name']
            mac, name = self.__split_mac_name(mac_name)

            # Activate one available bluetooth app.
            log.info(f"{name=}")
            app_descriptor, ui_object = self.__get_available_dynamic_apps(self.apps_bluetooth)
            if ui_object:
                ui_object.unhide()
                ui_object.rename_without_shortcut(name)
                # Create bluetooth app instance.
                app_descriptor.instance = BluetoothApp(self._put_in_function_queue, self._put_in_stm32_tx_queue, id_)

            # Add to bluetooth_list
            BnoteApp.bluetooth_devices.update({id_: name})

            # Switch automatically to the incoming bluetooth connection.
            if mac_name in Settings().data['bluetooth']['auto_switch']:
                self._menu.set_focus(ui_object)
                self.set_current_app(app_descriptor.instance)
            else:
                # Refresh menu or current app.
                self.__refresh_display_after_function()

    def __add_editor_app(self, language, filename, read_only=None, editor_app=None):
        """
        activate an editor
        :param filename: PosixPath
        :return:
        """
        ui_object = None
        if editor_app is None:
            # Check if file already exist.

            editor_apps = self.__get_used_dynamic_apps(self.apps_editor)
            for used_editor_app in editor_apps:
                log.info(f"{filename=}=?{self.apps_descriptor[used_editor_app].instance.get_filename()=}")
                if filename == Path(self.apps_descriptor[used_editor_app].instance.get_filename()):
                    # This File is already open
                    log.info("file already open")
                    app_descriptor = self.apps_descriptor[used_editor_app]
                    ui_object = self._menu.get_object(self.apps_descriptor[used_editor_app].action)
        if ui_object is None:
            app_descriptor, ui_object = self.__get_available_dynamic_apps(self.apps_editor)
            if ui_object:
                ui_object.unhide()
                if read_only:
                    app_name = "*-" + filename.name
                else:
                    app_name = filename.name
                ui_object.rename_without_shortcut(app_name)
                # Create editor app instance.
                if editor_app:
                    app_descriptor.instance = editor_app
                else:
                    (shortname, extension) = os.path.splitext(filename)
                    if extension:
                        extension = extension.lower()
                    if extension in MusicApp.known_extension():
                        app_descriptor.instance = MusicApp(self._put_in_function_queue, filename, language)
                    elif extension in DaisyApp.known_extension():
                        app_descriptor.instance = DaisyApp(self._put_in_function_queue, filename, language)
                    else:
                        app_descriptor.instance = EditorApp(self._put_in_function_queue, filename, language, read_only)
                # Update locked file of file manager.
                # DP FIXME les locked_file peuvent être obtenus en listant
                #  self.__get_used_dynamic_apps(self.apps_editor), ce serait moins chiant à gérer.
                self.apps_descriptor['explorer'].instance.append_locked_file(filename)
        # Switch automatically to the editor.
        self._menu.set_focus(ui_object)
        self.set_current_app(app_descriptor.instance)

    def __remove_bluetooth_app(self, *args, **kwargs):
        if 'id' in kwargs:
            id_ = kwargs['id']
            bluetooth_apps = self.__get_used_dynamic_apps(self.apps_bluetooth)
            for bluetooth_app in bluetooth_apps:
                if self.apps_descriptor[bluetooth_app].instance.get_bluetooth_id() == id_:
                    if self._current_app == self.apps_descriptor[bluetooth_app].instance:
                        # Return to applications selector if the removed app. is the current app.
                        self.set_current_app(None)
                        self._menu.reset_container()
                    # Remove app
                    self.apps_descriptor[bluetooth_app].instance = None
                    # Current object will be hidden, return to app menu.
                    ui_object = self._menu.get_object_from_action(self.apps_descriptor[bluetooth_app].action)
                    ui_object.hide()
                    # Remove from bluetooth list
                    BnoteApp.bluetooth_devices.pop(id_)
                    # Refresh menu or current app.
                    self.__refresh_display_after_function()
                    break

    def __remove_editor_app(self, *args, **kwargs):
        editor_instance = kwargs['app']
        # Notify the application to close.
        editor_instance.on_close()
        # Remove editor for app list
        editor_apps = self.__get_used_dynamic_apps(self.apps_editor)
        for editor_app in editor_apps:
            if editor_instance == self.apps_descriptor[editor_app].instance:
                ui_object = self._menu.get_object_from_action(self.apps_descriptor[editor_app].action)
                ui_object.hide()
                # Unlock the file
                self.apps_descriptor['explorer'].instance.remove_locked_file(editor_instance.get_filename())
                if self._current_app == editor_instance:
                    # Return to applications selector if the removed app. is the current app.
                    self.set_current_app(None)
                    self._menu.reset_container()
                # Remove app
                self.apps_descriptor[editor_app].instance = None
                # Refresh menu or current app.
                self.__refresh_display_after_function()
                break

    def __refresh_display_after_function(self):
        if not self._current_app:
            # Refresh menu.
            self._menu.ask_update_braille_display()
        else:
            # Refresh current app.
            self._current_app.refresh_app()
