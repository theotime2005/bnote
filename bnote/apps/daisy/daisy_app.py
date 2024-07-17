"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time
import threading
from pathlib import Path

from bnote.apps.daisy.daisy import DaisyReader
from bnote.apps.daisy.daisy.daisy_read_file import DaisyReadFile
from bnote.apps.edt.editor_base_app import EditorBaseApp
from bnote.apps.edt.edt.editor_daisy import EditorDaisy
from bnote.apps.edt.edt.mp3 import Mp3
from bnote.apps.repeated_timer import RepeatedTimer
import bnote.ui as ui
from bnote.tools.keyboard import Keyboard
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.settings import Settings
from bnote.tools.audio_player import AudioPlayer

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG, logging
log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class DaisyApp(EditorBaseApp):

    MIDI_FILENAME = "new_song.mid"

    def __init__(self, put_in_function_queue, file_name=None, language=None, read_only=True):
        self.read_daisy_file = None
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"Create DaisyApp with {read_only=}")
        # Reading parameters
        self.mp3_file = None
        self.is_reading = False
        self.last_mp3 = Mp3()
        self.timer_enable = False
        self.tag = None
        # Create reading timer.
        self.timer = RepeatedTimer(1, self.play_timeout)
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"DaisyApp thread id : {threading.current_thread().ident}")
        super().__init__(put_in_function_queue, file_name, language, read_only)
        # switch audio channel to 'radio' (default in editor_base is 'speech'
        # In this apps, media volume is used instead.
        self.channel = 'radio'

    @staticmethod
    def known_extension():
        return ".zip",

    def _create_editor(self, lines):
        """
        To overload if editor is not editor.Editor
        """
        return EditorDaisy(self.editor_line_length(), lines)

    def audio(self):
        # Useful to identify 'audio' menu contrainer.
        return True

    def _create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        app_name = _("daisy")
        return ui.UiMenuBar(
            name=app_name,
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&file"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&close"), action=self._exec_close,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                                   shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F4),
                        ui.UiMenuItem(name=_("c&ontents"), action=self._exec_contents),
                        # TODO To activate cleanup, the daisy tags list must be considered.
                        # ui.UiMenuItem(name=_("clean&up"), action=self._exec_cleanup),
                        ui.UiMenuItem(name=_("sta&tistics"), action=self._exec_statistics),
                    ]),
                ui.UiMenuBar(
                    name=_("&edit"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("curs&or"), action=self._exec_cursor),
                        ui.UiMenuItem(name=_("forward in grade2 braille"), action=self._toggle_grade2_from_menu),
                    ]),
                self.create_sub_menu_goto(),
                self.create_sub_menu_find(),
                self.create_sub_menu_bookmark(),
                ui.UiMenuBar(
                    name=_("au&dio"), action=self.audio,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&play"), action=self._exec_play,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='R'),
                        ui.UiMenuItem(name=_("&stop"), action=self._exec_stop, is_hide=True,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                                   shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE),
                        ui.UiMenuItem(name=_("pa&use/resume"), action=self._exec_pause_resume, is_hide=True,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='P'),
                        ui.UiMenuItem(name=_("&volume"), action=self._exec_volume),
                    ]),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def refresh_document(self):
        """
        Overload base class. Call when menu or dialogbox are closed.
        :return: None
        """
        # Audio
        ui_pause_resume = self._menu.get_object(self._exec_pause_resume)
        ui_stop = self._menu.get_object(self._exec_stop)
        if self.editor and self.is_reading:
            if ui_pause_resume is not None:
                ui_pause_resume.unhide()
            if ui_stop is not None:
                ui_stop.unhide()
        else:
            if ui_pause_resume is not None:
                if self.last_mp3 and self.last_mp3.mp3_file is not None:
                    ui_pause_resume.unhide()
                else:
                    ui_pause_resume.hide()
            if ui_stop is not None:
                ui_stop.hide()
        self._refresh_center_braille_display()

    def read_data_file(self, lou, full_file_name, language, add_line, ended, sheet_name=None):
        # EditorBaseApp Overload.
        self.read_daisy_file = DaisyReader(full_file_name)
        return DaisyReadFile(lou, full_file_name, self.read_daisy_file, language, Settings().data, add_line, ended)

    def get_extra_parameters(self, params):
        """
        Returns from read specific files.
        """
        try:
            self.last_mp3 = params['mp3']
            if self.last_mp3 is None:
                raise KeyError
            log.debug(f"last mp3 is {self.last_mp3}")
        except KeyError:
            log.error('ERROR : No mp3 file in specific file !')
            self.last_mp3 = Mp3()

    # Call just before the application removing from internal menu.
    def on_close(self):
        log.debug("on_close")
        self.__stop_reading()
        self.timer.stop()
        while self.timer.is_running:
            time.sleep(0.1)
        log.debug("timer is closed")
        self.save_specific_file(**{'mp3': self.last_mp3})

    def _end_context_save(self, error, doc_file):
        kwargs = {'markers': self.editor.markers(), 'caret': self.editor.caret(),
                  'read_only': self.editor.read_only, 'mp3': self.last_mp3}
        super()._common_end_context_save(error, doc_file, **kwargs)

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

    def input_braille(self, data) -> bool:
        """
        Overload input_braille of bnote_app to do a correct translation of braille to char in dot 6 or 8
        """
        return self._input_braille(
            BnoteApp.keyboard.decode_braille(
                BnoteApp.lou,
                data,
                (self.braille_type == 'grade1') or (self.braille_type == 'grade2')
            ),
            data
        )

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph and return (refresh, object_id).
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        # Daisy reader, specific functions
        # Enter : Play
        # Space : Pause/Resume
        done = False
        if self._current_dialog is None and not self._in_menu:
            # Simple key decoding for Daisy shorcut.
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE:
                self._exec_pause_resume()
                done = True
            elif bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
                self._exec_play()
                done = True
        if not done:
            # Base class treatment.
            done = super().input_bramigraph(modifier, bramigraph)
            if not done:
                # Specific commands treatment (after base class).
                pass
        return done
    # <<< End of key events.

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
        # Here treat the specific FunctionId added by this application.
        if function_id == FunctionId.FUNCTION_SETTINGS_CHANGE:
            # Change radio volume
            if (kwargs['section'] == self.channel) and \
                    ((kwargs['key'] == 'volume_headphone') or (kwargs['key'] == 'volume_hp')):
                AudioPlayer().set_volume()
                log.error(f"volume stored <{AudioPlayer().get_volume()}>")
        if function_id == FunctionId.FUNCTION_DAISY_SUMMARY_ENDED:
            self.daisy_summary(kwargs['summary'])
            done = True
        elif function_id == FunctionId.FUNCTION_DAISY_TIME_OUT:
            self.on_play_timer()
            done = True
        else:
            # Call base class decoding.
            done = super().input_function(*args, **kwargs)
        return done

    def _exec_contents(self):
        # Display an information dialog box.
        self._current_dialog = ui.UiInfoDialogBox(message=_("reading..."))
        self.wait_dialog = True
        summary_thread = threading.Thread(target=self.construct_summary_thread)
        summary_thread.start()

    def construct_summary_thread(self):
        summary = self.read_daisy_file.read_summary()
        self._put_in_function_queue(FunctionId.FUNCTION_DAISY_SUMMARY_ENDED, **{'summary': summary})

    def daisy_summary(self, summary):
        # Get book title as dialogbox name.
        properties = self.read_daisy_file.properties()
        title = properties['title']
        item_list = []
        text_tag_list = []
        for item in summary:
            item_list.append(f"{item[0]}-{item[2].replace('/xa0', ' ')}")
            text_tag_list.append(self.read_daisy_file.tag_from_smil_name(item[1]))
        current_index = self.editor.current_summary_index(text_tag_list)
        if current_index is None:
            current_index = 0
        self._current_dialog = ui.UiDialogBox(
            name=title,
            item_list=[
                ui.UiListBox(name=_("c&ontents"), value=("chapters", item_list), current_index=current_index, extra_parameters=summary),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_summary),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog)
            ],
            action_cancelable=self._exec_cancel_dialog
        )

    def _exec_valid_summary(self):
        kwargs = self._current_dialog.get_values()
        chapters = kwargs["chapters"]
        summary_item = chapters.get_extra_parameters()[chapters.get_index()]
        text_tag = self.read_daisy_file.tag_from_smil_name(summary_item[1])
        self.editor.set_caret_on_tag(text_tag)

    def _exec_play(self):
        # Compute caret position as paragraph index and index in paragraph
        start_pos_caret, end_pos_caret = self.editor.caret_as_paragraph_position()
        current_paragraph_index = end_pos_caret.x
        # paragraph = self.editor.paragraph(current_paragraph_index)
        # log.critical(paragraph)
        daisy_tag = self.editor.daisy_tag(current_paragraph_index)
        # log.critical(f"{daisy_tag=}")
        mp3_param = self.read_daisy_file.mp3_from_tag(daisy_tag)
        if mp3_param is not None:
            self.tag = daisy_tag
            mp3_file, time_offset = mp3_param
            # log.critical(f"{mp3_file=},{time_offset=}")
            self.__play(mp3_file, time_offset)

    def __play(self, mp3_file, time_offset):
        file = Path(mp3_file)
        if not file.exists():
            log.critical(f"Mp3 file to unzip {file.name=}")
            mp3_file = self.read_daisy_file.mp3_file_extract(file.name)
        # log.critical(f"{mp3_file=}")
        AudioPlayer().file_play(mp3_file, 0) # call_back=self.play_audio_call_back_stop())
        self.mp3_file = mp3_file
        AudioPlayer().forward(int(float(time_offset) * 1000))
        time.sleep(3)
        # self.play_timer.start()
        self.is_reading = True
        self.timer_enable = True

    def play_timeout(self):
        """
        Call each second by repeated timer thread.
        """
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"play_timeout thread id {threading.current_thread().ident}")
        self._put_in_function_queue(FunctionId.FUNCTION_DAISY_TIME_OUT)

    def on_play_timer(self):
        """
        Event handle each second by ui thread.
        """
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"on_play_timer thread id {threading.current_thread().ident}")
        if not self.timer_enable:
            return
        if self.is_reading and not AudioPlayer().is_paused():
            if AudioPlayer().is_playing():
                time_offset, duration = AudioPlayer().get_media_player_time()
                self.__move_caret_on_reading(self.mp3_file, time_offset)
            else:
                # Next mp3.
                if not self.__next_mp3():
                    # End of reading.
                    self.__stop_reading()

    def __next_mp3(self):
        if self.mp3_file:
            next_mp3 = self.read_daisy_file.mp3_next(self.mp3_file)
            if next_mp3 is not None:
                # Play the next mp3
                self.mp3_file = next_mp3[0]
                mp3 = self.read_daisy_file.mp3_file_extract(self.mp3_file)
                log.error(f"{next_mp3=}")
                self.__play(mp3, next_mp3[1])
                self.__move_caret_on_reading(next_mp3[0], next_mp3[1])
                return True
            else:
                # End of reading document reaches.
                self.__stop_reading()
                return False

    def __stop_reading(self):
        if AudioPlayer().is_playing() or AudioPlayer().is_paused():
            self.last_mp3.mp3_file = self.mp3_file
            self.last_mp3.mp3_offset, mp3_length = AudioPlayer().get_media_player_time()
            # log.critical(f"{self.last_mp3=}")
            AudioPlayer().stop()
            self.mp3_file = None
            self.is_reading = False
            self.timer_enable = False

    def __move_caret_on_reading(self, mp3_file, time_offset):
        text_tag = self.read_daisy_file.tag_from_offset(mp3_file, str(float(time_offset) / 1000))
        if self.tag != text_tag:
            # Put caret on curent tag.
            self.tag = text_tag
            # Move caret on new tag.
            log.debug(f"set caret on {self.tag=}")
            self.editor.set_caret_on_tag(self.tag)
            # Force refresh.
            self._refresh_center_braille_display()

    def _exec_stop(self):
        self.__stop_reading()

    def _exec_pause_resume(self):
        if self.is_reading:
            if AudioPlayer().is_paused():
                log.debug("Resume")
                AudioPlayer().resume()
                time.sleep(0.1)
                self.timer_enable = True
            else:
                log.debug("Pause")
                AudioPlayer().pause()
                self.timer_enable = False
        else:
            if self.last_mp3.mp3_file is not None:
                # offset in __play is in second.
                log.debug(f"Restart {self.last_mp3.mp3_file=}")
                self.__play(self.last_mp3.mp3_file, self.last_mp3.mp3_offset / 1000)
                # Done by self.__play
                # self.timer_enable = True
    def _exec_statistics(self):
        properties = self.read_daisy_file.properties()
        with self.lock:
            (paragraphs_count, words_count, characters_count) = self.editor.statistics()
        self._current_dialog = ui.UiDialogBox(
            name=_("statistics"),
            item_list=[
                ui.UiEditBox(name=_("duration"),
                          value=("", BnoteApp.braille_form(str(properties['total_time'])))
                          ),
                ui.UiEditBox(name=_("file"),
                          value=("", BnoteApp.braille_form(str(self.get_display_filename())))
                          ),
                ui.UiEditBox(name=_("title"),
                          value=("", BnoteApp.braille_form(properties['title']))
                          ),
                ui.UiEditBox(name=_("author"),
                          value=("", BnoteApp.braille_form(properties['creator']))
                          ),
                ui.UiEditBox(name=_("identifier"),
                          value=("", BnoteApp.braille_form(properties['identifier']))
                          ),
                ui.UiEditBox(name=_("paragraphs"),
                          value=("", BnoteApp.braille_form(str(paragraphs_count)))
                          ),
                ui.UiEditBox(name=_("words"),
                          value=("", BnoteApp.braille_form(str(words_count)))
                          ),
                ui.UiEditBox(name=_("characters"),
                          value=("", BnoteApp.braille_form(str(characters_count)))
                          ),
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )
