"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json

from mutagen.asf import ASFUnicodeAttribute

from bnote.apps.fman.file_manager import FileManager, BNOTE_FOLDER
from bnote.tools.audio_player import AudioPlayer
from bnote.tools.io_util import Gpio
from bnote.tools.quick_search import QuickSearch
from bnote.tools.settings import Settings
from bnote.tools.volume_speed_dialog_box import VolumeDialogBox
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
from bnote.tools.volume import Volume
import bnote.ui as ui
from pathlib import Path
import mutagen

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, MP3_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(MP3_APP_LOG)

FILE_TYPES = (".wav", ".mp3", ".wma", ".ogg", ".m4a", ".ts")
FOLDER_PLAYLIST = BNOTE_FOLDER / Path("bnote-playlist")


class Mp3App(BnoteApp):
    """
    MP3 player application.
    """

    @staticmethod
    def known_extension():
        return FILE_TYPES

    def __init__(self, put_in_function_queue, **kwargs):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super().__init__(put_in_function_queue)
        # The BrailleLine that will be "current_dir:self.__files[self.__focused_file]"
        self.__ui_line = None
        # menu creation.
        self._menu = self.__create_menu()
        # Current playlist.
        self.__playlist_name = _("no name")
        self.__playlist = None
        self.__playlist_index = -1
        # The QuickSearch instance.
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)
        # hp-headphone survey
        self.current_output = None
        # is playing survey
        self.__timer_param_is_playing = False
        # Create playlist folder if not exists.
        __root_path = FOLDER_PLAYLIST
        if not __root_path.exists():
            try:
                log.info("call Path.mkdir({})".format(__root_path))
                Path.mkdir(__root_path)
            except OSError as e:
                log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__root_path, e))
        # Construct a new playlist if 'filename' or 'filenames' parameters is defined.
        if "filename" in kwargs.keys() or "filenames" in kwargs.keys():
            self.set_list_and_play(**kwargs)

    def set_list_and_play(self, **kwargs):
        log.info(f"{kwargs}")
        if "filename" in kwargs.keys() or "filenames" in kwargs.keys():
            # Clean up the list and insert the filename.
            self.__exec_valid_delete_all_items()
            if "filename" in kwargs.keys():
                self._add_to_playlist(Path(kwargs["filename"]))
            elif "filenames" in kwargs.keys():
                self._add_list_to_playlist(kwargs["filenames"])
            self.__playlist_index = 0
            # start the first item of the list.
            self._exec_playlist()
            # self._exec_play_selected()

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("mp3"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("play &list"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&open"),
                            action=self._exec_open_playlist,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="O",
                        ),
                        ui.UiMenuItem(
                            name=_("&save"),
                            action=self._exec_save_playlist,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="S",
                        ),
                        ui.UiMenuItem(
                            name=_("&delete"), action=self._exec_delete_playlist
                        ),
                        ui.UiMenuItem(
                            name=_("delete &all"), action=self._exec_delete_all_playlist
                        ),
                    ],
                ),
                ui.UiMenuBar(
                    name=_("item"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&add"),
                            action=self._exec_add_item,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="A",
                        ),
                        ui.UiMenuItem(name=_("de&lete"), action=self._exec_delete_item),
                        ui.UiMenuItem(
                            name=_("delete &all"), action=self._exec_delete_all_items
                        ),
                        ui.UiMenuItem(
                            name=_("to the &beginning"),
                            action=self._exec_item_to_beginning,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="H",
                        ),
                        ui.UiMenuItem(
                            name=_("to the &end"),
                            action=self._exec_item_to_end,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="E",
                        ),
                        ui.UiMenuItem(
                            name=_("&up"),
                            action=self._exec_item_up,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="U",
                        ),
                        ui.UiMenuItem(
                            name=_("&down"),
                            action=self._exec_item_down,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="D",
                        ),
                        ui.UiMenuItem(
                            name=_("&properties"), action=self._exec_item_properties
                        ),
                    ],
                ),
                ui.UiMenuBar(
                    name=_("&play"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&item"),
                            action=self._exec_play_selected,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="I",
                        ),
                        ui.UiMenuItem(
                            name=_("&list"),
                            action=self._exec_playlist,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="L",
                        ),
                        ui.UiMenuItem(
                            name=_("&next"),
                            action=self._exec_next,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="F",
                        ),
                        ui.UiMenuItem(
                            name=_("pre&vious"),
                            action=self._exec_previous,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="B",
                        ),
                        ui.UiMenuItem(
                            name=_("&pause"),
                            action=self._exec_pause_resume,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="P",
                        ),
                        ui.UiMenuItem(
                            name=_("s&top"),
                            action=self._exec_stop,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="T",
                        ),
                        ui.UiMenuItem(
                            name=_("&forward (30s)"),
                            action=self._exec_forward,
                            is_hide=False,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="R",
                        ),
                        ui.UiMenuItem(
                            name=_("&backward (10s)"),
                            action=self._exec_backward,
                            is_hide=False,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="C",
                        ),
                        ui.UiMenuItem(
                            name=_("position"),
                            action=self._exec_position,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
                        ),
                        ui.UiMenuItem(name=_("volume"), action=self._exec_volume),
                    ],
                ),
            ],
        )

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self.__create_menu()
        self.__build_braille_line()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        # here, hide/unhide menu items according to application state.
        if self.__playlist is None:
            self._menu.get_object(self._exec_delete_item).hide()
            self._menu.get_object(self._exec_delete_all_items).hide()
            self._menu.get_object(self._exec_item_to_beginning).hide()
            self._menu.get_object(self._exec_item_to_end).hide()
            self._menu.get_object(self._exec_item_up).hide()
            self._menu.get_object(self._exec_item_down).hide()
            self._menu.get_object(self._exec_item_properties).hide()
        else:
            self._menu.get_object(self._exec_delete_item).unhide()
            self._menu.get_object(self._exec_delete_all_items).unhide()
            self._menu.get_object(self._exec_item_to_beginning).unhide()
            self._menu.get_object(self._exec_item_to_end).unhide()
            self._menu.get_object(self._exec_item_up).unhide()
            self._menu.get_object(self._exec_item_down).unhide()
            self._menu.get_object(self._exec_item_properties).unhide()
        if AudioPlayer().is_playing() or AudioPlayer().is_paused():
            log.info("AudioPlayer is playing.")
            self._menu.get_object(self._exec_stop).unhide()
            self._menu.get_object(self._exec_pause_resume).unhide()
            self._menu.get_object(self._exec_position).unhide()
            self._menu.get_object(self._exec_forward).unhide()
            self._menu.get_object(self._exec_backward).unhide()
            if AudioPlayer().is_paused():
                self._menu.rename_item(
                    _("&resume"),
                    Settings().data["system"]["braille_type"],
                    self._exec_pause_resume,
                )
            else:
                self._menu.rename_item(
                    _("p&ause"),
                    Settings().data["system"]["braille_type"],
                    self._exec_pause_resume,
                )
        else:
            log.info("AudioPlayer() is not playing.")
            self._menu.get_object(self._exec_stop).hide()
            self._menu.get_object(self._exec_pause_resume).hide()
            self._menu.get_object(self._exec_position).hide()
            self._menu.get_object(self._exec_forward).hide()
            self._menu.get_object(self._exec_backward).hide()
        if AudioPlayer().playlist_is_playing():
            self._menu.get_object(self._exec_next).unhide()
            self._menu.get_object(self._exec_previous).unhide()
        else:
            self._menu.get_object(self._exec_next).hide()
            self._menu.get_object(self._exec_previous).hide()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        # DP FIXME Check the list items here ! (if someones deleted removes them)
        self.refresh_current_item(True)

    def refresh_current_item(self, rebuild_all=False):
        self.__build_braille_line()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        # Do not try to refresh the braille display if we are in menu or document
        # (because braille_display is the same for all ui).
        if self.in_menu_or_in_dialog():
            return
        # Because braille_display is the same for all ui, we need to reconstruct it.
        self.__ui_line._update_braille_display()

    # ---------------
    # Menu functions.
    def _exec_play_selected(self):
        if self.__playlist:
            AudioPlayer().file_play(
                self.__playlist[self.__playlist_index], self.__playlist_index
            )

    @staticmethod
    def _exec_pause_resume():
        if AudioPlayer().is_playing():
            AudioPlayer().pause()
        else:
            AudioPlayer().resume()

    def _exec_position(self):
        if AudioPlayer().is_playing():
            self._current_dialog = ui.UiDialogBox(
                name=_("editor"),
                item_list=[
                    ui.UiListBox(
                        name=_("&position"),
                        value=("position_value", [str(i) for i in range(0, 100, 5)]),
                    ),
                    ui.UiButton(name=_("&ok"), action=self._exec_valid_position_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def _exec_valid_position_dialog(self):
        kwargs = self._current_dialog.get_values()
        pos_value = kwargs["position_value"]
        if AudioPlayer().is_playing():
            AudioPlayer().set_media_player_position(int(pos_value) / 100)

    def _exec_playlist(self):
        # playlist = [
        #     Path('/home/pi/.bnote/bnote-documents/tests/mp3/Red Hot Chili Peppers (1999) - Californication/14 - Right On Time.mp3'),
        #     Path('/home/pi/.bnote/bnote-documents/tests/mp3/Red Hot Chili Peppers (1999) - Californication/01 - Around The World.mp3'),
        #     # Path('/home/pi/.bnote/bnote-documents/Red Hot Chili Peppers (1999) - Californication/01 - Around The World.mp3')
        #     ]
        # AudioPlayer().playlist_play(playlist)
        if self.__playlist:
            AudioPlayer().playlist_play(self.__playlist)
            # by default after start playlist, display the first.
            self.__playlist_index = 0

    @staticmethod
    def _exec_next():
        AudioPlayer().playlist_next()

    @staticmethod
    def _exec_previous():
        AudioPlayer().playlist_previous()

    @staticmethod
    def _exec_stop():
        AudioPlayer().stop()

    @staticmethod
    def _exec_forward():
        AudioPlayer().forward(30000)

    @staticmethod
    def _exec_backward():
        AudioPlayer().backward(10000)

    # --------------------
    # Key event functions.

    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key.
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = False
        if key_id == Keyboard.KeyId.KEY_NONE:
            # Ignore keys up event.
            return False
        log.debug("key_id={}".format(key_id))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(Mp3App, self).input_command(data, modifier, key_id)
        if not done:
            # command treatment for document.
            # command treatment for document.
            command_switcher = {
                Keyboard.KeyId.KEY_CARET_UP: self.__previous_line,
                Keyboard.KeyId.KEY_CARET_DOWN: self.__next_line,
                Keyboard.KeyId.KEY_START_DOC: self.__first_line,
                Keyboard.KeyId.KEY_END_DOC: self.__last_line,
            }
            function = command_switcher.get(key_id, None)
            if function:
                # Execute the function
                done = function()
                if done:
                    # The current item has changed of presentation.
                    self.__build_braille_line()
        if not done:
            done = self.__ui_line.input_command(modifier, key_id)
            log.info(f"self.__files_braille_line.input_command returns {done=}")
        return done

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param character: unicode char
        :param data: brut braille comb. for advanced treatment
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {character=}")
        done = super(Mp3App, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            self.__quick_search.do_quick_search(character)
            pass
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        bramigraph_switcher = {
            # Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: Editor.Functions.SELECTION_MODE_OFF,
            Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self.__first_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_END: self.__last_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_UP: self.__previous_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: self.__next_line,
            Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: self.__exec_play_stop_selected,
            Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: self._exec_delete_item,
        }
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        done = super(Mp3App, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # command treatment for document.
            # kwargs = BnoteApp.keyboard.decode_modifiers(modifier)
            # Get the function from switcher dictionnary
            function = bramigraph_switcher.get(bramigraph, None)
            if function:
                # Execute the function
                done = function()
                if done:
                    # Refresh
                    self.__build_braille_line()
        return done

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        log.info(f"{modifier=} {position=} {key_type=}")
        done = super(Mp3App, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment for file manager.
            if modifier == 0:
                # Exec function on the files_braille_line to activate parent or child item
                done = self.__ui_line.input_interactive(modifier, position, key_type)
        return done

    def input_function(self, *args, **kwargs) -> bool:
        """
        Call when function is not treated by base class of this class.
        :param args[0]: The function id
        :param kwargs:
        :return: True if function treated.
        """
        log.info("args={} kwargs={}".format(args, kwargs))
        function_id = args[0]
        # Here treat the specific FunctionId added by this application.
        if function_id == FunctionId.FUNCTION_SETTINGS_CHANGE:
            # Change radio volume
            if (kwargs["section"] == "radio") and (
                (kwargs["key"] == "volume_headphone") or (kwargs["key"] == "volume_hp")
            ):
                AudioPlayer().set_volume()
                log.error(f"volume stored <{AudioPlayer().get_volume()}>")
        # call base class decoding.
        done = super(Mp3App, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # --- SURVEY HEAD_PHONE CONNEXION/DECONNEXION
        # log.info("Timer event")
        headphone = Gpio().is_head_phone()
        output_change = False
        if headphone:
            if self.current_output != "headphone":
                log.info("switch to headphone")
                output_change = True
                self.current_output = "headphone"
        elif self.current_output != "hp":
            log.info("switch to hp")
            output_change = True
            self.current_output = "hp"
        # --- SURVEY MENU HIDDEN OR NOT ACCORDING PLAYING
        if AudioPlayer().is_playing() and not self.__timer_param_is_playing:
            self.__timer_param_is_playing = True
            # Update hidden menu items to allow or not allow shortcuts.
            self._update_menu_items()
        elif not AudioPlayer().is_playing() and self.__timer_param_is_playing:
            self.__timer_param_is_playing = False
            # Update hidden menu items to allow or not allow shortcuts.
            self._update_menu_items()
        # --- SURVEY LIST AUTO-REFRESH DURING PLAYING
        if (
            AudioPlayer().is_playing()
            and not self._in_menu
            and self._current_dialog is None
        ):
            braille_display_offset = self.__ui_line.braille_display.get_start_pos()
            index = AudioPlayer().get_playlist_index()
            if index >= 0:
                time, duration = AudioPlayer().get_media_player_time()
                log.info(f"Playing {index=} {time=}, {duration=}")
                if index == self.__playlist_index:
                    # The current line displayed is the playing item.
                    # The current item has changed of presentation.
                    self.__build_braille_line()
                    # Restore the old braille offset.
                    self.__ui_line.braille_display.set_start_pos(braille_display_offset)

    # --------------------
    # Line change.
    def __previous_line(self):
        if self.__playlist is not None and self.__playlist_index > 0:
            self.__playlist_index -= 1
            return True

    def __next_line(self):
        if (
            self.__playlist is not None
            and self.__playlist_index < len(self.__playlist) - 1
        ):
            self.__playlist_index += 1
            return True

    def __first_line(self):
        if self.__playlist is not None and self.__playlist_index > 0:
            self.__playlist_index = 0
            return True

    def __last_line(self):
        if self.__playlist is not None and self.__playlist_index < (
            len(self.__playlist) - 1
        ):
            self.__playlist_index = len(self.__playlist) - 1
            return True

    def _exec_add_item(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert file"),
            item_list=[
                ui.UiFileBox(
                    root=FileManager.get_root_path(), suffix_filter=FILE_TYPES
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_choose_file),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_save_playlist(self, playlist_name=None):
        """
        Save the playlist.
        """
        if self.__playlist is None:
            # Nothing to do on empty playlist.
            return
        if playlist_name is None:
            playlist_name = self.__playlist_name
        self._current_dialog = ui.UiDialogBox(
            name=_("save"),
            item_list=[
                ui.UiEditBox(
                    name=_("playlist"), value=("playlist_name", playlist_name)
                ),
                ui.UiButton(name=_("&save"), action=self.__exec_valid_save_playlist),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __exec_valid_save_playlist(self):
        kwargs = self._current_dialog.get_values()
        playlist_name = Path(FOLDER_PLAYLIST / kwargs["playlist_name"])
        if playlist_name.exists():
            # Ask confirmation.
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_("playlist name exists, do you want overwrite the playlist?"),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"), action=self._exec_save_playlist_yes_dialog
                    ),
                    ui.UiButton(
                        name=_("&no"), action=self._exec_save_playlist_no_dialog
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
                extra_parameters={"playlist_name": playlist_name},
            )
        else:
            self.__save_playlist_name(playlist_name)

    def _exec_save_playlist_yes_dialog(self):
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs}")
        self.__save_playlist_name(playlist_name=kwargs["playlist_name"])

    def _exec_save_playlist_no_dialog(self):
        kwargs = self._current_dialog.get_values()
        # Return to the dialog box to change playlist name.
        self._exec_save_playlist(playlist_name=kwargs["playlist_name"])

    def __save_playlist_name(self, playlist_name):
        if self.__playlist:
            mp3_list = list()
            for mp3_path in self.__playlist:
                mp3_list.append(str(mp3_path))
            try:
                with open(playlist_name, "w") as fp:
                    json.dump(mp3_list, fp)
                self.__playlist_name = playlist_name
            except IOError as er:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=f"Write file IO exception:{er}",
                    action=self._exec_cancel_dialog,
                )

    def _exec_open_playlist(self):
        """
        Read a playlist.
        and check if files are valid.
        """
        self.__exec_open_delete_playlist(function="open")

    def _exec_delete_playlist(self):
        """
        Read a playlist.
        and check if files are valid.
        """
        self.__exec_open_delete_playlist(function="delete")

    @staticmethod
    def __get_list_of_playlist() -> [str]:
        return [f.name for f in FOLDER_PLAYLIST.glob("**/*") if f.is_file()]

    def __exec_open_delete_playlist(self, function):
        if function == "delete":
            name = _("delete")
            action_name = _("&delete")
        else:
            name = _("open")
            action_name = _("&open")
        self._current_dialog = ui.UiDialogBox(
            name=name,
            extra_parameters={"function": function},
            item_list=[
                ui.UiListBox(
                    name=_("playlist"),
                    value=("list_of_playlist", self.__get_list_of_playlist()),
                ),
                ui.UiButton(
                    name=action_name, action=self.__exec_valid_open_delete_playlist
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def __exec_valid_open_delete_playlist(self):
        # Stop player because list changed.
        AudioPlayer().stop()
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs}")
        if kwargs["list_of_playlist"] is not None:
            if kwargs["function"] == "delete":
                # Delete the playlist
                if Path(FOLDER_PLAYLIST / kwargs["list_of_playlist"]).exists():
                    Path(FOLDER_PLAYLIST / kwargs["list_of_playlist"]).unlink()
            else:
                # Open the playlist
                try:
                    with open(
                        Path(FOLDER_PLAYLIST / kwargs["list_of_playlist"]), "r"
                    ) as fp:
                        playlist = json.load(fp)
                    self.__playlist = list()
                    for item in playlist:
                        self.__playlist.append(Path(item))
                    self.__playlist_name = kwargs["list_of_playlist"]
                    removed_number = self.__check_playlist()
                    self.__playlist_index = 0
                    # The current item has changed of presentation.
                    self.__build_braille_line()
                    if removed_number != 0:
                        self._current_dialog = ui.UiInfoDialogBox(
                            message=f"{removed_number} items invalid removed from playlist",
                            action=self._exec_cancel_dialog,
                        )

                except IOError as er:
                    self._current_dialog = ui.UiInfoDialogBox(
                        message=f"Write file IO exception:{er}",
                        action=self._exec_cancel_dialog,
                    )

    def _exec_delete_all_playlist(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("are you sure to delete all saved play list?"),
            buttons=[
                ui.UiButton(
                    name=_("&ok"), action=self.__exec_valid_delete_all_playlist
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    @staticmethod
    def __exec_valid_delete_all_playlist():
        file_list = [f for f in FOLDER_PLAYLIST.glob("**/*") if f.is_file()]
        if file_list:
            for file in file_list:
                file.unlink()

    def __add_to_playlist(self, file_path: Path):
        # Stop player because list changed.
        AudioPlayer().stop()
        if self.__playlist is None:
            self.__playlist = [file_path]
            self.__playlist_index = 0
        else:
            self.__playlist_index += 1
            self.__playlist.insert(self.__playlist_index, file_path)
        log.info(str(self.__playlist[self.__playlist_index]))

    def _exec_choose_file(self):
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        file_path = kwargs["file"]
        self._add_to_playlist(file_path)

    def _add_list_to_playlist(self, file_list):
        # Add all list item with known extension into playlist (sorted by track number).
        audio_items = list()
        for item in file_list:
            if item.is_file():
                file_path = Path(item)
                if file_path.suffix in FILE_TYPES:
                    track_number = int(self.__tracknumber(file_path))
                    audio_items.append((track_number, file_path))
        sorted_list = sorted(audio_items, key=lambda track: track[0])
        for key, value in sorted_list:
            self.__add_to_playlist(value)

    def _add_to_playlist(self, file_path):
        if file_path is None:
            log.info("No file chosen")
        elif file_path.is_dir():
            # ADD A FOLDER.
            log.info(f"folder:{file_path}")
            # Add all file with known extension into playlist.
            self._add_list_to_playlist([item for item in file_path.iterdir()])
            # The current item has changed of presentation.
            self.__build_braille_line()
        elif file_path.is_file():
            # ADD A FILE.
            log.info(f"file:{file_path}")
            self.__add_to_playlist(file_path)
            # The current item has changed of presentation.
            self.__build_braille_line()
        else:
            log.info(f"folder:{file_path}")

    @staticmethod
    def __tracknumber(file):
        properties = Mp3App.__get_properties(str(file))
        if properties is None:
            return 0
        # properties is a dict with keys : album, title, artist, tracknumber, date
        return properties["tracknumber"][0]

    def _exec_delete_all_items(self):
        if self.__playlist:
            # Ask confirmation to delete scores of one level.
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("are you sure to delete the play list {}?").format(
                    self.__playlist[self.__playlist_index]
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&ok"), action=self.__exec_valid_delete_all_items
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def __move_item(self, origin, destination):
        # Stop player because list changed.
        AudioPlayer().stop()
        if self.__playlist and self.__playlist_index >= 0:
            item = self.__playlist.pop(origin)
            self.__playlist_index = destination
            self.__playlist.insert(self.__playlist_index, item)
            return True

    def _exec_item_to_beginning(self):
        return self.__move_item(self.__playlist_index, 0)

    def _exec_item_to_end(self):
        return self.__move_item(self.__playlist_index, len(self.__playlist) - 1)

    def _exec_item_up(self):
        return self.__move_item(self.__playlist_index, self.__playlist - 1)

    def _exec_item_down(self):
        return self.__move_item(self.__playlist_index, self.__playlist + 1)

    def _exec_delete_item(self):
        # Stop player because list changed.
        AudioPlayer().stop()
        if self.__playlist:
            self.__playlist.pop(self.__playlist_index)
            if self.__playlist_index == 0:
                # play list becomes empty.
                self.__playlist_index = -1
                self.__playlist = None
                self.__playlist_name = _("no name")
            elif self.__playlist_index >= len(self.__playlist):
                self.__playlist_index -= 1
            # The current item has changed of presentation.
            self.__build_braille_line()
            return True

    @staticmethod
    def __get_properties(filename: str):
        try:
            # info = mutagen.File(filename, easy=True).StreamInfo()
            # log.debug(f"{info}")
            tag = mutagen.File(filename, easy=True)
            log.debug(f"{tag=}")
            # Check properties validity.
            if tag is None or "title" not in tag.keys():
                return
            # new_tag = dict()
            for key, value in tag.items():
                if isinstance(value[0], ASFUnicodeAttribute):
                    log.error(f"({key=}:{value=}) is ASFUnicodeAttribute")
                    # ignore ASFUnicodeAttribute ?
                    log.error(f"{value[0].value}")
                    return
                # new_tag[key] = value[0].__str__()
            # print(f"{new_tag}")
            # return EasyID3(filename)
            if "tracknumber" not in tag.keys():
                tag["tracknumber"] = ["0"]
            if "artist" not in tag.keys():
                tag["artist"] = ["?"]
            if "date" not in tag.keys():
                tag["date"] = ["?"]
            if "album" not in tag.keys():
                tag["album"] = ["?"]
            return tag
        # Failed to find file attributes.
        except mutagen.id3.ID3NoHeaderError as er:
            log.warning(f"mutagen.id3 = {er}")
        # Failed to open the file...
        except mutagen.MutagenError as er:
            log.warning(f"mutagen error = {er}")

    def _exec_item_properties(self):
        if self.__playlist is None:
            # Nothing to do on empty playlist.
            return
        properties = self.__get_properties(str(self.__playlist[self.__playlist_index]))
        log.error(f"mp3 {properties=}")
        if properties is None:
            # Audio file without properties (like .wav)
            return
        self._current_dialog = ui.UiDialogBox(
            name=_("properties"),
            extra_parameters={"properties": properties},
            item_list=[
                ui.UiEditBox(
                    name=_("tracknumber"),
                    value=("tracknumber", properties["tracknumber"][0]),
                ),
                ui.UiEditBox(name=_("title"), value=("title", properties["title"][0])),
                ui.UiEditBox(
                    name=_("artist"), value=("artist", properties["artist"][0])
                ),
                ui.UiEditBox(name=_("date"), value=("date", properties["date"][0])),
                ui.UiEditBox(name=_("album"), value=("album", properties["album"][0])),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_properties_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_properties_dialog(self):
        # get parameters
        kwargs = self._current_dialog.get_values()
        properties = kwargs["properties"]
        is_changed = False
        if properties["tracknumber"][0] != kwargs["tracknumber"]:
            properties["tracknumber"][0] = kwargs["tracknumber"]
            is_changed = True
        if properties["title"][0] != kwargs["title"]:
            properties["title"] = [kwargs["title"]]
            is_changed = True
        if properties["artist"][0] != kwargs["artist"]:
            properties["artist"] = [kwargs["artist"]]
            is_changed = True
        if properties["date"][0] != kwargs["date"]:
            properties["date"] = [kwargs["date"]]
            is_changed = True
        if properties["album"][0] != kwargs["album"]:
            properties["album"] = [kwargs["album"]]
            is_changed = True
        if is_changed:
            log.info("save file properties")
            properties.save()

    def __exec_valid_delete_all_items(self):
        # Empty list.
        self.__playlist = None
        self.__playlist_name = _("no name")
        self.__playlist_index = -1
        # Stop player because list changed.
        AudioPlayer().stop()
        # The current item has changed of presentation.
        self.__build_braille_line()
        return True

    def __exec_play_stop_selected(self):
        if self.__playlist:
            if AudioPlayer().is_playing():
                AudioPlayer().stop()
            else:
                AudioPlayer().file_play(
                    self.__playlist[self.__playlist_index], self.__playlist_index
                )

    def _exec_volume(self):
        self._current_dialog = VolumeDialogBox(
            _("volume"), _("&value"), self.__save_the_new_volume, channel="radio"
        )

    def __save_the_new_volume(self, volume):
        # Save the new Volume in settings.
        Volume().set_volume(volume, channel="radio")
        Settings().save()
        # Alert internal about settings change.
        headphone = Gpio().is_head_phone()
        if headphone:
            key = "volume_headphone"
        else:
            key = "volume_hp"
        self._put_in_function_queue(
            FunctionId.FUNCTION_SETTINGS_CHANGE, **{"section": "radio", "key": key}
        )

    # --------------------
    # Quick search function.
    def __quick_search_move_call_back(self, text_to_find) -> bool:
        if self.__playlist:
            log.info(f"{text_to_find=}")
            text_to_find = text_to_find.lower()
            # Construct the list of all mp3 files display lines.
            playlist_display_lines = list()
            for item in self.__playlist:
                playlist_display_lines.append(self.__display_file(item))
            # Search from self.__focused_file_index to end of list
            for index, item in enumerate(playlist_display_lines):
                # log.info("file={} index={}".format(item, index))
                if (
                    item.lower().find(text_to_find) == 0
                    and index > self.__playlist_index
                ):
                    # Focus the wanted item
                    self.__playlist_index = index
                    # The current item has changed of presentation.
                    self.__build_braille_line()
                    return True
            # Search from 0 to self.__focused_file_index in the list
            for index, item in enumerate(playlist_display_lines):
                # log.info("file={} index={}".format(item, index))
                if (
                    item.lower().find(text_to_find) == 0
                    and index < self.__playlist_index
                ):
                    # Focus the wanted item
                    self.__playlist_index = index
                    # The current item has changed of presentation.
                    self.__build_braille_line()
                    return True
        return False

    # --------------------
    # Document functions.
    @staticmethod
    def __convert_millis(millis: int) -> str:
        seconds = (millis / 1000) % 60
        minutes = millis / (1000 * 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"

    def __display_file(self, file):
        index = AudioPlayer().get_playlist_index()
        time_string = None
        if index >= 0 and index == self.__playlist_index:
            time, duration = AudioPlayer().get_media_player_time()
            pos = AudioPlayer().get_media_player_position()
            time_string = "/".join(
                (
                    self.__convert_millis(time),
                    self.__convert_millis(duration),
                    f"{int(pos*100):2d}%",
                )
            )
        properties = Mp3App.__get_properties(str(file))
        if properties is None or len(properties["album"]) == 0:
            if time_string:
                return "-".join((time_string, file.name))
            else:
                return file.name
        else:
            # properties is a dict with keys : album, title, artist, tracknumber, date
            properties_string = "-".join(
                (
                    properties["tracknumber"][0],
                    properties["title"][0],
                    properties["artist"][0],
                    properties["date"][0],
                    properties["album"][0],
                )
            )
            if time_string:
                return "-".join((time_string, properties_string))
            else:
                return properties_string

    def get_data_line(self, force_refresh=False) -> (str, str, str, bool):
        """
        Overload get_data_line of BnoteApp.
        Get the braille line of the document area.
        :param force_refresh:
        :return:
          (static_text, static_dots, dynamic_dots) if something changed since the last call or if force_refresh=True
          else return (None, None, None)
        """
        if self.in_menu_or_in_dialog():
            return BnoteApp.get_data_line(self, force_refresh)

        return self.__ui_line.get_data_line(force_refresh)

    def __build_braille_line(self):
        # The BrailleLine that will be "current_dir:self.__files[self.__focused_file]"
        if self.__playlist:
            list_name = self.__display_file(self.__playlist[self.__playlist_index])
        else:
            list_name = _("empty list...")
        self.__ui_line = ui.UiDocumentList(
            parent_name=str(self.__playlist_name),
            parent_action=self._exec_activate_list,
            list_name=str(list_name),
            list_action=self._exec_activate_item,
        )

    def _exec_activate_list(self):
        log.info("<_exec_activate_list>")
        # Nothing to do ?

    def _exec_activate_item(self):
        log.info("<_exec_activate_item>")
        self.__exec_play_stop_selected()

    def __check_playlist(self):
        """
        Check if all file in self.__playlist exists, otherwise remove them from playlist
        Return the number of removed items.
        """
        checked_list = list()
        removed = 0
        for item in self.__playlist:
            if item.exists() and item.is_file():
                checked_list.append(item)
            else:
                removed += 1
        self.__playlist = checked_list
        return removed
