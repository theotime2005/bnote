"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import mido
import datetime
import time
from os import path
import shlex
import subprocess
import threading
from pathlib import Path

from bnote.apps.edt.editor_base_app import EditorBaseApp
from bnote.apps.music.braille_dots import *
import bnote.ui as ui

# To use or not opy module
import bnote.apps.music.music_opy as music
import bnote.apps.edt.edt as editor
from bnote.tools.keyboard import Keyboard
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.settings import Settings
from bnote.tools.audio_player import AudioPlayer

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class MusicApp(EditorBaseApp):

    MIDI_FILENAME = "new_song.mid"

    def __init__(
        self, put_in_function_queue, file_name=None, language=None, read_only=False
    ):
        # Autorise ou non l'écriture dans le fichier si les paramètres correspondent
        read_only = not self.enable_write(file_name)
        # TB  Filtrez l'édition svp
        super().__init__(put_in_function_queue, file_name, language, read_only)
        self.opened_file_name = file_name
        self._score = None
        # switch audio channel to 'radio' (default in editor_base is 'speech'
        # In this apps, media volume is used instead.
        self.channel = "radio"
        # affiche ou masque les menus d'export, d'insertion et d'audio
        extention = str(file_name).split(".")[-1]
        if (
            extention == "bxml"
            and Settings().data["music_bxml"]["edit_mode"] in ["read", "listen"]
        ) or (
            extention == "musicxml"
            and Settings().data["music_xml"]["edit_mode"] in ["read", "listen"]
        ):
            self._menu.get_object(self.export).hide()
            self._menu.get_object(self.insert).hide()
        if (
            extention == "bxml" and Settings().data["music_bxml"]["edit_mode"] == "read"
        ) or (
            extention == "musicxml"
            and Settings().data["music_xml"]["edit_mode"] == "read"
        ):
            self._menu.get_object(self.audio).hide()
        # On masque l'avance en braille abrégé inutile en musique
        self._menu.get_object(self._toggle_grade2_from_menu).hide()

    def read_file_ended(self, error, file_name, sheet_list, score=None):
        super().read_file_ended(error, file_name, sheet_list, score)
        self._score = score

    @staticmethod
    def enable_write(file):
        """
        If Edit mode is False the user can't modify the score
        """
        extention = str(file).split(".")[-1]
        if extention == "bxml" and Settings().data["music_bxml"]["edit_mode"] in [
            "read",
            "listen",
        ]:
            return False
        elif extention == "musicxml" and Settings().data["music_xml"][
            "edit_mode"
        ] not in ["expert", "edit"]:
            return False
        return True

    @staticmethod
    def known_extension():
        return ".bxml", ".musicxml"

    def export(self):
        return True

    def insert(self):
        return True

    def audio(self):
        return True

    def _create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("music"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&file"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&close"),
                            action=self._exec_close,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4,
                        ),
                        ui.UiMenuItem(
                            name=_("&save"),
                            action=self._exec_save,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="S",
                        ),
                        ui.UiMenuBar(
                            name=_("&export"),
                            action=self.export,
                            menu_item_list=[
                                ui.UiMenuItem(
                                    name=_("&musicxml"),
                                    action=self._exec_export_musicxml,
                                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                                    shortcut_key="M",
                                ),
                                ui.UiMenuItem(
                                    name=_("&bxml"),
                                    action=self._exec_export_bxml,
                                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                                    shortcut_key="B",
                                ),
                            ],
                        ),
                        ui.UiMenuItem(
                            name=_("&properties"), action=self._exec_properties
                        ),
                        ui.UiMenuItem(
                            name=_("sta&tistics"), action=self._exec_statistics
                        ),
                    ],
                ),
                self.create_sub_menu_edit(),
                ui.UiMenuBar(
                    name=_("&insert"),
                    action=self.insert,
                    menu_item_list=[
                        self.create_sub_menu_text(),
                        ui.UiMenuItem(
                            name=_("&key signature"),
                            action=self._exec_insert_key_signature,
                        ),
                        ui.UiMenuItem(name=_("&clef"), action=self._exec_insert_clef),
                        self.create_sub_menu_musical_content(),
                        self.create_sub_menu_game_details(),
                        ui.UiMenuItem(name=_("&bar"), action=self._exec_insert_bar),
                        self.create_sub_menu_accord(),
                        self.create_sub_menu_keyboard_signs(),
                        ui.UiMenuItem(
                            name=_("&octave sign"), action=self._exec_insert_octave
                        ),
                    ],
                ),
                self.create_sub_menu_find_replace(),
                self.create_sub_menu_bookmark(),
                ui.UiMenuBar(
                    name=_("au&dio"),
                    action=self.audio,
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&play"),
                            action=self._exec_play_score,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="R",
                        ),
                        ui.UiMenuItem(
                            name=_("&stop"),
                            action=self._exec_stop_play_score,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE,
                        ),
                        ui.UiMenuItem(
                            name=_("pa&use"),
                            action=self._exec_pause_play_score,
                            is_hide=True,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="P",
                        ),
                        ui.UiMenuItem(name=_("&volume"), action=self._exec_volume),
                        ui.UiMenuItem(name=_("&speed"), action=self._exec_speed),
                    ],
                ),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def _exec_properties(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("properties"),
            item_list=[
                ui.UiMultiLinesBox(
                    name=_("&infos"),
                    value=("message", "midi\nline 2\nline 3"),
                    is_read_only=False,
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_sample_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_sample_dialog(self):
        log.info("callback:_exec_valid_sample_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")

    def create_sub_menu_text(self):
        return ui.UiMenuBar(
            name=_("&text"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&title"),
                    action=self._exec_insert_title,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="T",
                ),
                ui.UiMenuItem(
                    name=_("&sub title"),
                    action=self._exec_insert_sub_title,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="S",
                ),
                ui.UiMenuItem(
                    name=_("&composer"),
                    action=self._exec_insert_composer,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="C",
                ),
                ui.UiMenuItem(
                    name=_("&lyricist"),
                    action=self._exec_insert_lyricist,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="Y",
                ),
                ui.UiMenuItem(
                    name=_("&credit words"),
                    action=self._exec_insert_text,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="W",
                ),
                ui.UiMenuItem(
                    name=_("&part"),
                    action=self._exec_insert_part,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="P",
                ),
                ui.UiMenuItem(
                    name=_("&lyrics"),
                    action=self._exec_insert_lyrics,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="L",
                ),
                ui.UiMenuItem(
                    name=_("&karaoke"),
                    action=self._exec_insert_karaoke,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
                    + Keyboard.BrailleModifier.BRAILLE_FLAG_ALT,
                    shortcut_key="K",
                ),
            ],
        )

    def create_sub_menu_keyboard_signs(self):
        return ui.UiMenuBar(
            name=_("&keyboard signs"),
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&fingering"), action=self._exec_insert_keyboard_fingering
                ),
                ui.UiMenuItem(
                    name=_("&pedal"), action=self._exec_insert_keyboard_pedal
                ),
            ],
        )

    def create_sub_menu_game_details(self):
        return ui.UiMenuBar(
            name=_("&game details"),
            menu_item_list=[
                ui.UiMenuItem(name=_("&nuance"), action=self._exec_insert_nuance),
            ],
        )

    def create_sub_menu_musical_content(self):
        return ui.UiMenuBar(
            name=_("&musical content"),
            menu_item_list=[
                ui.UiMenuItem(name=_("insert &note"), action=self._exec_insert_note),
                ui.UiMenuItem(name=_("insert &rest"), action=self._exec_insert_silence),
                ui.UiMenuItem(
                    name=_("rythmic &groups"), action=self._exec_insert_rythmic_groups
                ),
                ui.UiMenuItem(
                    name=_("&alteration"), action=self._exec_insert_alteration
                ),
            ],
        )

    def create_sub_menu_accord(self):
        return ui.UiMenuBar(
            name=_("acco&rd"),
            menu_item_list=[
                ui.UiMenuItem(name=_("&interval"), action=self._exec_insert_interval),
                ui.UiMenuItem(
                    name=_("&measure in-accord"),
                    action=self._exec_insert_measure_in_accord,
                ),
            ],
        )

    @staticmethod
    def read_data_file(lou, full_file_name, language, add_line, ended, sheet_name=None):
        return music.MusicReadFile(
            lou, full_file_name, language, Settings().data, add_line, ended
        )

    def write_data_file(self, lou, full_file_name, get_line, on_end, function):
        extension = str(Path(self.opened_file_name.suffix)).replace(".", "")
        if extension is None:
            log.error("write_data_file extension is None !")
        return music.MusicWriteFile(
            lou,
            Settings().data,
            full_file_name,
            self._score,
            get_line,
            on_end,
            function,
            extension,
        )

    def _transform_text_to_braille(self, line):
        """
        Overload editor_base_app function.
        !! Not !! Transform the line to a text line in grade1 or grade2 according to the parameter.
        """
        return line

    def _transform_braille_to_text(self, line):
        """
        !! Not !! Transform the line in text grade1 or grade2 to text according to the parameter.
        """
        return line

    # ---------------
    # Key event functions.
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
        # Here treat the specific FunctionId added by this application.
        if function_id == FunctionId.FUNCTION_SETTINGS_CHANGE:
            # Change radio volume
            if (kwargs["section"] == "radio") and (
                (kwargs["key"] == "volume_headphone") or (kwargs["key"] == "volume_hp")
            ):
                AudioPlayer().set_volume()
                log.error(f"volume stored <{AudioPlayer().get_volume()}>")
        # Call base class decoding.
        done = super().input_function(*args, **kwargs)
        return done

    # >>> Key events
    def input_command(self, data, modifier, key_id) -> bool:
        """
        Does what is expected for this command key
        :param data: ?
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param key_id: (see Keyboard.KeyId)
        :return: True if command treated, otherwise False
        """
        done = super().input_command(data, modifier, key_id)
        if not done:
            # Specific commands treatment.
            pass
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        done = super().input_bramigraph(modifier, bramigraph)
        if not done:
            # Specific commands treatment.
            pass
        return done

    # <<< End of key events.

    # >>> Specifics menu actions.
    # def _exec_shutdown(self):
    #     self.shutdown(True)

    def _exec_play_score(self):
        # Display save in progress...
        self._current_dialog = ui.UiInfoDialogBox(message=_("saving..."))
        # Delete the previous file if exists.
        if Path(MusicApp.MIDI_FILENAME).exists():
            Path(MusicApp.MIDI_FILENAME).unlink()
        # Write the new midi file.
        extension = str(Path(self.opened_file_name.suffix)).replace(".", "")
        write_file = music.MusicWriteFile(
            BnoteApp.lou,
            Settings().data,
            MusicApp.MIDI_FILENAME,
            self._score,
            self._get_line,
            self._end_save_midi,
            FunctionId.FUNCTION_CLOSE_DIALOG_BOX,
            extension,
        )
        write_file.start()
        # After saving the file _end_save_midi is called.

    def _end_save_midi(self, error, function):
        log.warning("_end_save() called !")
        if error is None:
            # play file
            # MidiPlayer().play(MusicApp.MIDI_FILENAME, Gpio().is_head_phone())
            AudioPlayer().midi_play(MusicApp.MIDI_FILENAME)
            # Unhide Stop menu item
            self._menu.get_object(self._exec_stop_play_score).unhide()
            # Unhide Pause menu item
            self._menu.get_object(self._exec_pause_play_score).unhide()
            # Close the dialog box
            self._put_in_function_queue(function)
        else:
            # Error during write file => Display an error dialog box
            log.error("file save error : {}".format(error))
            self.last_error = error
            self._put_in_function_queue(FunctionId.FUNCTION_DISPLAY_LAST_ERROR)

    def _exec_stop_play_score(self):
        AudioPlayer().stop()
        # Hide Stop menu item
        self._menu.get_object(self._exec_stop_play_score).hide()
        # Hide Pause menu item
        self._menu.get_object(self._exec_pause_play_score).hide()

    def _exec_pause_play_score(self):
        if AudioPlayer().is_paused():
            AudioPlayer().resume()
        else:
            AudioPlayer().pause()

    def _exec_export_musicxml(self):
        path_file = Path(self._file_name)
        file_name = path_file.parent.joinpath(Path(path_file.stem + ".musicxml"))
        self.__export(file_name)

    def _exec_export_bxml(self):
        path_file = Path(self._file_name)
        file_name = path_file.parent.joinpath(Path(path_file.stem + ".bxml"))
        self.__export(file_name)

    def __export(self, file_name):
        if Path(file_name).exists():
            self._current_dialog = ui.UiInfoDialogBox(
                message=_(
                    f"file {file_name.name} already exists, do you want to overwrite it ?"
                ),
                action=self._exec_write_file,
                action_param={"file_name": file_name},
            )
            return
        else:
            self._exec_write_file(file_name)

    def _exec_write_file(self, file_name=None):
        self._original_file_name = self._file_name
        self._file_name = file_name
        # Force file to be written.
        self.editor.set_is_modified(True)
        self._exec_save()
        # change the currently opened file in internal list.
        self._put_in_function_queue(
            FunctionId.FUNCTION_CHANGE_LOCKED_FILE,
            **{
                "app": self,
                "old_file": self._original_file_name,
                "new_file": file_name,
            },
        )

    # Insert dialog function
    # Function to convert signs in braille 8 dots
    def convert_to_8_dots(self, part):
        part = self.lou.to_text_8(part)
        return part

    # Function to insert text in document
    def insert_in_document(self, content):
        with self.lock:
            self.editor.function(
                editor.Editor.Functions.PUT_STRING, **{"text": content}
            )

    # Dialog box to insert title
    def _exec_insert_title(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(name=_("&title"), value=("title", _("score's title"))),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_title_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_title_dialog(self):
        log.info("callback:_exec_valid_title_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["title"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b2345) + text_convert
        )

    # Dialog box to insert sub title
    def _exec_insert_sub_title(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(
                    name=_("&sub title"), value=("sub title", _("score's sub title"))
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_sub_title_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_sub_title_dialog(self):
        log.info("callback:_exec_valid_sub_title_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["sub title"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b234) + text_convert
        )

    # Dialog box to insert composer
    def _exec_insert_composer(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(
                    name=_("&composer"), value=("composer", _("score's composer"))
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_composer_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_composer_dialog(self):
        log.info("callback:_exec_valid_composer_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["composer"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b14) + text_convert
        )

    # Dialog box to insert lyricist
    def _exec_insert_lyricist(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(
                    name=_("&lyricist"), value=("lyricist", "score's lyricist")
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_lyricist_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_lyricist_dialog(self):
        log.info("callback:_exec_valid_lyricist_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["lyricist"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b123) + text_convert
        )

    # Dialog box to insert simple text
    def _exec_insert_text(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(
                    name=_("&text"), value=("text", _("text outside of the score"))
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_text_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_text_dialog(self):
        log.info("callback:_exec_valid_text_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["text"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b2456) + text_convert
        )

    # Dialog box to insert part name
    def _exec_insert_part(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(name=_("part &name"), value=("part", _("new part"))),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_part_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_part_dialog(self):
        log.info("callback:_exec_valid_part_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        # on créé des variables représentant les signes de main gauche et droite au piano, pour faciliter création de partie
        part_right_hand = self.lou.to_text_8(b46 + b345)
        part_left_hand = self.lou.to_text_8(b456 + b345)
        # On insert une condition qui 'ninsert que les signe main gauche ou droite si ceci sont saisis ou que les mots clef sont utilisés.
        # Attention, il faudra traduir ces mots clef et bien les préciser dans la doc, pour aider les utilisateurs
        if kwargs["part"] == _("piano-right") or kwargs["part"] == part_right_hand:
            self.insert_in_document(part_right_hand)
        elif kwargs["part"] == _("piano-left") or kwargs["part"] == part_left_hand:
            self.insert_in_document(part_left_hand)
        else:
            text_original = kwargs["part"]
            text_convert = ""
            for character in text_original:
                if ord(character) == 32:
                    character = chr(160)
                    text_convert += character
                else:
                    text_convert += character
            self.insert_in_document(
                self.convert_to_8_dots(b56 + 2 * b23 + b1234) + text_convert
            )

    # Dialog box to insert lyrics
    def _exec_insert_lyrics(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(name=_("&lyrics"), value=("lyrics", "...")),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_lyrics_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_lyrics_dialog(self):
        log.info("callback:_exec_valid_lyrics_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["lyrics"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(self.convert_to_8_dots(b56 + b23) + text_convert)

    # Dialog box to insert karaoke text
    def _exec_insert_karaoke(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(name=_("&karaoke"), value=("karaoke", "...")),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_karaoke_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_karaoke_dialog(self):
        log.info("callback:_exec_valid_karaokai_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        text_original = kwargs["karaoke"]
        text_convert = ""
        for character in text_original:
            if ord(character) == 32:
                character = chr(160)
                text_convert += character
            else:
                text_convert += character
        self.insert_in_document(
            self.convert_to_8_dots(b56 + 2 * b23 + b13) + text_convert
        )

    # Dialog box to insert keyboard fingering
    def _exec_insert_keyboard_fingering(self):
        # On donne les même noms que dans le fichier "english music terms" en gardant le toute lettre pour égalité entre les langues (litalien par exemple)
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("choose &finger"),
                    value=(
                        "finger",
                        [
                            _("first finger"),
                            _("second finger"),
                            _("third finger"),
                            _("fourth finger"),
                            _("fifth finger"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"),
                    action=self._exec_valid_insert_keyboard_fingering_dialog,
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_keyboard_fingering_dialog(self):
        log.info("callback:_exec_valid_text_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        finger_dic = {
            _("first finger"): b1,
            _("second finger"): b12,
            _("third finger"): b123,
            _("fourth finger"): b2,
            _("fifth finger"): b13,
        }
        self.insert_in_document(self.convert_to_8_dots(finger_dic[kwargs["finger"]]))

    # Dialog box to insert pedal signs
    def _exec_insert_keyboard_pedal(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("&pedal"),
                    value=(
                        "pedal",
                        [
                            _("pedal down"),
                            _("pedal up"),
                            _("pedal under note"),
                            _("half-pedal"),
                            _("pedal up as soon as chord is struck"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"),
                    action=self._exec_valid_insert_keyboard_pedal_dialog,
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_keyboard_pedal_dialog(self):
        log.info("callback:_exec_valid_insert_keyboard_pedal_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        pedal_dic = {
            _("pedal down"): b126 + b14,
            _("pedal up"): b16 + b14,
            _("pedal under note"): b16 + b126 + b14,
            _("half-pedal"): b5 + b126 + b14,
            _("pedal up as soon as chord is struck"): b5 + b16 + b14,
        }
        self.insert_in_document(self.convert_to_8_dots(pedal_dic[kwargs["pedal"]]))

    # Dialog box to insert alteration
    def _exec_insert_alteration(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &alteration of note"),
                    value=("alteration", [_("flat"), _("natural"), _("sharp")]),
                    current_index=1,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_alteration_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_alteration_dialog(self):
        kwargs = self._current_dialog.get_values()
        alteration_dic = {_("flat"): b126, _("natural"): b16, _("sharp"): b146}
        self.insert_in_document(
            self.convert_to_8_dots(alteration_dic[kwargs["alteration"]])
        )

    # Dialog box to insert key signature
    def _exec_insert_key_signature(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &tonality"),
                    value=(
                        "key",
                        [
                            _("do (+)/la (-)"),
                            _("re flat (+)/la sharp (-)"),
                            _("re (+)/si (-)"),
                            _("mi flat (+)/do (-)"),
                            _("mi (+)/do sharp (-)"),
                            _("fa (+)/re (-)"),
                            _("sol flat (+)/re sharp (-)"),
                            _("sol (+)/mi (-)"),
                            _("la flat (+)/fa (-)"),
                            _("la (+)/fa sharp (-)"),
                            _("si flat (+)/sol (-)"),
                            _("si (+)/la sharp (-)"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"),
                    action=self._exec_valid_insert_key_signature_dialog,
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_key_signature_dialog(self):
        log.info("callback:_exec_valid_insert_key_signature_dialog")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        part_sharp = b146
        part_flat = b126
        signature_dic = {
            _("do (+)/la (-)"): b3456 + b1245 + b16,
            _("re flat (+)/la sharp (-)"): b3456 + b15 + part_flat,
            _("re (+)/si (-)"): 2 * part_sharp,
            _("mi flat (+)/do (-)"): 3 * part_flat,
            _("mi (+)/do sharp (-)"): b3456 + b145 + part_sharp,
            _("fa (+)/re (-)"): part_flat,
            _("sol flat (+)/re sharp (-)"): b3456 + b124 + part_flat,
            _("sol (+)/mi (-)"): part_sharp,
            _("la flat (+)/fa (-)"): b3456 + b145 + part_flat,
            _("la (+)/fa sharp (-)"): 3 * part_sharp,
            _("si flat (+)/sol (-)"): 2 * part_flat,
            _("si (+)/la sharp (-)"): b3456 + b15 + part_sharp,
        }
        self.insert_in_document(self.convert_to_8_dots(signature_dic[kwargs["key"]]))

    # Dialog box to insert octaves signs
    def _exec_insert_octave(self):
        # On donne les même noms que dans le fichier "english music terms" en gardant le toute lettre pour égalité entre les langues (litalien par exemple)
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select an &octave"),
                    value=(
                        "octave",
                        [
                            _("a below first octave"),
                            _("first octave"),
                            _("second octave"),
                            _("third octave"),
                            _("fourth octave (medium)"),
                            _("fifth octave"),
                            _("sixth octave"),
                            _("seventh octave"),
                            _("eighth octave"),
                        ],
                    ),
                    current_index=4,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_octave_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_octave_dialog(self):
        log.info("callback:_exec_valid_insert_octave")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        octave_dic = {
            _("a below first octave"): 2 * b4,
            _("first octave"): b4,
            _("second octave"): b45,
            _("third octave"): b456,
            _("fourth octave (medium)"): b5,
            _("fifth octave"): b46,
            _("sixth octave"): b56,
            _("seventh octave"): b6,
            _("eighth octave"): b6 * 2,
        }
        self.insert_in_document(self.convert_to_8_dots(octave_dic[kwargs["octave"]]))

    # Dialog box to insert nuance
    def _exec_insert_nuance(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select a &nuance"),
                    value=(
                        "nuance",
                        [
                            _("crescendo"),
                            _("pianissimo"),
                            _("piano"),
                            _("mezzo piano"),
                            _("mezzo forte"),
                            _("forte"),
                            _("fortissimo"),
                            _("diminuendo"),
                        ],
                    ),
                    current_index=2,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_nuance_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_nuance_dialog(self):
        log.info("callback:_exec_valid_insert_simple_nuance")
        # Read parameters of dialog box.
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        nuance = kwargs["nuance"]
        if nuance == _("pianissimo"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b1234 * 2))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("piano"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b1234))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("mezzo piano"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b134 + b1234))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == "mezzo forte":
            self.insert_in_document(self.convert_to_8_dots(b345 + b134 + b124))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("forte"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b124))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("fortissimo"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b124 * 2))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("diminuendo"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b145 + b345 + b256))
            for character in range(2):
                self.editor.function(
                    editor.Editor.Functions.MOVE_LEFT, **{"shift": False, "ctrl": False}
                )
                # Refresh braille display (useful after caret move)
                self._refresh_braille_display(self._braille_display.get_start_pos())
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write, and after the end of the nuance. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif nuance == _("crescendo"):
            self.insert_in_document(self.convert_to_8_dots(b345 + b14 + b345 + b25))
            for character in range(2):
                self.editor.function(
                    editor.Editor.Functions.MOVE_LEFT, **{"shift": False, "ctrl": False}
                )
                # Refresh braille display (useful after caret move)
                self._refresh_braille_display(self._braille_display.get_start_pos())
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write, and after the end of the nuance. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    # Dialog box to insert note
    def _exec_insert_note(self):
        # On donne les notes en langage américain, il faudra les traduires pour chaques langues
        # On part du la (a en anglais) jusqu'au sol (g en anglais) mais on met l'index sur do (c en anglais)
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &note"),
                    value=(
                        "note",
                        [_("a"), _("b"), _("c"), _("d"), _("e"), _("f"), _("g")],
                    ),
                    current_index=2,
                ),
                ui.UiListBox(
                    name=_("select &value of note"),
                    value=(
                        "duration",
                        [
                            _("whole"),
                            _("half"),
                            _("quarter"),
                            _("eighth"),
                            _("16th"),
                            _("32nd"),
                            _("64th"),
                            _("128th"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_note_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_note_dialog(self):
        kwargs = self._current_dialog.get_values()
        note = kwargs["note"]
        note_quarter_dic = {
            _("c"): ord(b1456),
            _("d"): ord(b156),
            _("e"): ord(b1246),
            _("f"): ord(b12456),
            _("g"): ord(b1256),
            _("a"): ord(b246),
            _("b"): ord(b2456),
        }
        value_note_dic = {
            _("whole"): chr(note_quarter_dic[note] + 4),
            _("half"): chr(note_quarter_dic[note] - 28),
            _("quarter"): chr(note_quarter_dic[note]),
            _("eighth"): chr(note_quarter_dic[note] - 32),
            _("16th"): chr(note_quarter_dic[note] + 68),
            _("32nd"): chr(note_quarter_dic[note] + 36),
            _("64th"): chr(note_quarter_dic[note] + 64),
            _("128th"): chr(note_quarter_dic[note] + 32),
        }
        self.insert_in_document(
            self.convert_to_8_dots(value_note_dic[kwargs["duration"]])
        )

    # Dialog box to insert silence
    def _exec_insert_silence(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select a &rest type"),
                    value=(
                        "type",
                        [
                            _("whole rest"),
                            _("half rest"),
                            _("quarter rest"),
                            _("eighth rest"),
                            _("16th rest"),
                            _("32nd rest"),
                            _("64th rest"),
                            _("128th rest"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_silence_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_silence_dialog(self):
        kwargs = self._current_dialog.get_values()
        silence_dic = {
            _("whole rest"): b134,
            _("half rest"): b136,
            _("quarter rest"): b1236,
            _("eighth rest"): b1346,
            _("16th rest"): b1347,
            _("32nd rest"): b1367,
            _("64th rest"): b12367,
            _("128th rest"): b13467,
        }
        self.insert_in_document(self.convert_to_8_dots(silence_dic[kwargs["type"]]))

    # Dialog box to insert bars
    def _exec_insert_bar(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &bar"),
                    value=(
                        "type",
                        [
                            _("measure"),
                            _("end of composition"),
                            _("end of section"),
                            _("simple repetition of fragment"),
                            _("repeat fragment with prima and seconda volta"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_bar_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_bar_dialog(self):
        kwargs = self._current_dialog.get_values()
        bar = kwargs["type"]
        if bar == _("measure"):
            self.insert_in_document(self.convert_to_8_dots(b123))
        elif bar == _("end of composition"):
            self.insert_in_document(self.convert_to_8_dots(b126 + b13))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_("do you want to save your document now?"),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_save),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif bar == _("end of section"):
            self.insert_in_document(self.convert_to_8_dots(b126 + b13 + b3))
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_("do you want to save your document now?"),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_save),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif bar == _("simple repetition of fragment"):
            self.insert_in_document(self.convert_to_8_dots(b126 + b2356 + b126 + b23))
            for character in range(2):
                self.editor.function(
                    editor.Editor.Functions.MOVE_LEFT, **{"shift": False, "ctrl": False}
                )
                # Refresh braille display (useful after caret move)
                self._refresh_braille_display(self._braille_display.get_start_pos())
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you must put an octave sign before continuing to write, do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif bar == _("repeat fragment with prima and seconda volta"):
            part_start = self.lou.to_text_8(b126 + b2356)
            part_prima = self.lou.to_text_8(b3456 + b2)
            part_seconda = self.lou.to_text_8(b3456 + b23)
            self.insert_in_document(
                part_start + "\n" + part_prima + "\n" + part_seconda
            )
            for character in range(2):
                self.editor.function(
                    editor.Editor.Functions.MOVE_UP, **{"shift": False, "ctrl": False}
                )
                # Refresh braille display (useful after caret move)
                self._refresh_braille_display(self._braille_display.get_start_pos())
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "you need to put an octave sign before continuing to write, and after prima, and seconda signs. do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    # Dialog box to insert interval
    def _exec_insert_interval(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &interval"),
                    value=(
                        "interval",
                        [
                            _("seconde"),
                            _("third"),
                            _("fourth"),
                            _("fifth"),
                            _("sixth"),
                            _("seventh"),
                            _("octave"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_interval_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_interval_dialog(self):
        kwargs = self._current_dialog.get_values()
        interval_dic = {
            _("seconde"): b34,
            _("third"): b346,
            _("fourth"): b3456,
            _("fifth"): b35,
            _("sixth"): b356,
            _("seventh"): b25,
            _("octave"): b36,
        }
        self.insert_in_document(
            self.convert_to_8_dots(interval_dic[kwargs["interval"]])
        )

    # Dialog box to insert measure in-accord
    def _exec_insert_measure_in_accord(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiEditBox(
                    name=_("enter the number of &voice"), value=("number", "2")
                ),
                ui.UiCheckBox(name=_("&full-measure in-accord"), value=("type", True)),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_measure_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_measure_dialog(self):
        kwargs = self._current_dialog.get_values()
        type = kwargs["type"]
        number_first = kwargs["number"]
        number_first = str(number_first)
        number = ""
        # on vérifie que le champ contient bien des chiffres, sans quoi, on risque d'avoir un crash au moment de la conversion
        for character in number_first:
            if ord(character) >= 58 or ord(character) <= 47:
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_("you must enter an integer."),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
                return False
            else:
                number += character
        number = int(number)
        number = number - 1
        if number < 1:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_("you must insert a minimum of 2 voices."),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            if type == True:
                part = b126 + b345
                self.insert_in_document(self.convert_to_8_dots(part * number))
                for i in range(len(part) * number):
                    self.editor.function(
                        editor.Editor.Functions.MOVE_LEFT,
                        **{"shift": False, "ctrl": False},
                    )
                    # Refresh braille display (useful after caret move)
                    self._refresh_braille_display(self._braille_display.get_start_pos())
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_(
                        "the cursor is place before the accord sign, don't forget to put an octave sign after all measure in-accord signs."
                    ),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
            elif type == False:
                # part_beginning=b46+b13
                # part_midle=b5+b2
                # part_end=b46+b13
                # part = self.lou.to_text_8(part_beginning+part_midle*number+part_end)
                # with self.lock:
                #     self.editor.function(editor.Editor.Functions.PUT_STRING, **{'text': part})
                # for i in range(len(part)):
                #     self.editor.function(editor.Editor.Functions.MOVE_LEFT, **{'shift': False, 'ctrl': False})
                #     # Refresh braille display (useful after caret move)
                #     self._refresh_braille_display(self._braille_display.get_start_pos())
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_(
                        "sorry, but part-measure in-accord is not suported for the moment."
                    ),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )

    # Dialog box to insert clefs
    def _exec_insert_clef(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("select &clef"),
                    value=("clef", [_("treble"), _("alto"), _("basse")]),
                    current_index=0,
                ),
                ui.UiCheckBox(name=_("in &part"), value=("type", False)),
                ui.UiListBox(
                    name=_("clef &line"),
                    value=(
                        "line",
                        [
                            _("default"),
                            _("first line"),
                            _("second line"),
                            _("third line"),
                            _("fourth line"),
                            _("fifth line"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiListBox(
                    name=_("add small &8?"),
                    value=("8", [_("below"), _("no"), _("above")]),
                    current_index=1,
                ),
                ui.UiButton(
                    name=_("&insert"), action=self._exec_valid_insert_clef_dialog
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_clef_dialog(self):
        kwargs = self._current_dialog.get_values()
        clef_dic = {
            _("treble"): b345 + b34,
            _("alto"): b345 + b346,
            _("basse"): b345 + b3456,
        }
        line_dic = {
            _("default"): "",
            _("first line"): b4,
            _("second line"): b45,
            _("third line"): b456,
            _("fourth line"): b5,
            _("fifth line"): b46,
        }
        small_8_dic = {_("below"): b3456 + b236, _("no"): "", _("above"): b3456 + b125}
        clef_begin = self.lou.to_text_8(b123)
        clef_in = self.lou.to_text_8(b13)
        if kwargs["type"] == False:
            if (
                kwargs["clef"] == _("alto")
                and kwargs["8"] != _("no")
                or kwargs["line"] != _("default")
                and kwargs["8"] != _("no")
            ):
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_(
                        "you cant select this options. This settings does not exist."
                    ),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
                return False
            self.insert_in_document(
                self.convert_to_8_dots(
                    clef_dic[kwargs["clef"]] + line_dic[kwargs["line"]]
                )
                + clef_begin
                + self.convert_to_8_dots(small_8_dic[kwargs["8"]])
                + " "
            )
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_(
                    "you must enter an octave sign to show the height of note. Do you want to display the octave list?"
                ),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self._exec_insert_octave),
                    ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        elif kwargs["type"] == True:
            if kwargs["clef"] == _("alto") or kwargs["8"] != _("no"):
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_(
                        "you cant select this options. This settings does not exist."
                    ),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
            else:
                self.insert_in_document(
                    self.convert_to_8_dots(
                        clef_dic[kwargs["clef"]] + line_dic[kwargs["line"]]
                    )
                    + clef_in
                )

    # Dialog box to insert rythmic groups
    def _exec_insert_rythmic_groups(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("insert"),
            item_list=[
                ui.UiListBox(
                    name=_("&rythm type"),
                    value=(
                        "rythm",
                        [
                            _("group of 2 notes"),
                            _("triplet"),
                            _("group of 4 notes"),
                            _("group of 5 notes"),
                            _("group of 6 notes"),
                            _("group of 7 notes"),
                            _("group of 8 notes"),
                            _("group of 9 notes"),
                            _("group of 10 notes"),
                        ],
                    ),
                    current_index=0,
                ),
                ui.UiButton(
                    name=_("&insert"),
                    action=self._exec_valid_insert_rythmic_groups_dialog,
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_insert_rythmic_groups_dialog(self):
        kwargs = self._current_dialog.get_values()
        rythm_dic = {
            _("group of 2 notes"): b456 + b23 + b3,
            _("triplet"): b23,
            _("group of 4 notes"): b456 + b256 + b3,
            _("group of 5 notes"): b456 + b26 + b3,
            _("group of 6 notes"): b123 + b235 + b3,
            _("group of 7 notes"): b456 + b2356 + b3,
            _("group of 8 notes"): b456 + b236 + b3,
            _("group of 9 notes"): b456 + b35 + b3,
            _("group of 10 notes"): b456 + b2 + b356 + b3,
        }
        self.insert_in_document(self.convert_to_8_dots(rythm_dic[kwargs["rythm"]]))

    # end of insert dialog function

    # ---------------
    # braille display functions.
    def _convert_line_to_dots(self, line):
        """
        Convert the text line to braille according to braille type.
        This method is overload by music editor.
        """
        static_dots = BnoteApp.lou.to_dots_8(line)
        return self._mask_dot_78(static_dots)
