"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
from pathlib import Path
from bnote.apps.fman.file_manager import FileManager
from bnote.apps.braille_learning.write_word import WriteWord
from bnote.apps.braille_learning.level_manage import ManageLevel, ManageScore
from bnote.apps.braille_learning import app_version
from bnote.tools.audio_player import AudioPlayer
from bnote.tools.speech_wrapper import speak
from bnote.tools.settings import Settings
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
import bnote.ui as ui
# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, WRITE_WORD_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(WRITE_WORD_APP_LOG)

class WriteWordApp(BnoteApp):
    """
    Braille learning application
    """
    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Braille length
        self.length=braille_device_characteristics.get_braille_display_length()
        # English base words or current language
        self.is_english = False
        # Call base class.
        super().__init__(put_in_function_queue)
        # menu creation.
        self._menu = self.__create_menu()
        # document refresh.
        self.file_unable=False
        self.word=""
        self.first_word=""
        self.position=1
        # Définition du dictionnaire de filtrage
        self.level_dict={
            _("A to J in lowercase"): self._get_dict_letter(ord("a"),ord("j")),
            _("A to J in capital letters"): self._get_dict_letter(ord("A"),ord("J")),
            _("A to J"): "{},{}".format(self._get_dict_letter(ord("a"),ord("j")),self._get_dict_letter(ord("A"),ord("J"))),
            _("K to T in lowercase"): self._get_dict_letter(ord("k"),ord("t")),
            _("K to T in capital letters"): self._get_dict_letter(ord("K"),ord("T")),
            _("K to T"): "{},{}".format(self._get_dict_letter(ord("k"),ord("t")),self._get_dict_letter(ord("K"),ord("T"))),
            _("A to T in lowercase"): self._get_dict_letter(ord("a"),ord("t")),
            _("A to T in capital letters"): self._get_dict_letter(ord("A"),ord("T")),
            _("A to T"): "{},{}".format(self._get_dict_letter(ord("a"),ord("t")),self._get_dict_letter(ord("A"),ord("T"))),
            _("A to Z"): "{},{}".format(self._get_dict_letter(ord("a"),ord("z")),self._get_dict_letter(ord("A"),ord("Z"))),
            _("complet"): "",
        }
        self.score=0
        self.letter=ManageLevel().get_level("write word")
        if self.letter==False:
            self._exec_select_level()
        else:
            self.initialize()

    def _get_dict_letter(self, first, last):
        """
        return list of letters
        """
        lst_character=""
        for c in range(first,last):
            lst_character+="{},".format(chr(c))
        lst_character+=chr(last)
        return lst_character

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("word game"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&score"), action=self._exec_score,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&show to this level"), action=self._exec_show_score),
                        ui.UiMenuItem(name=_("&delete to this level"), action=self._exec_delete_score),
                    ]
                ),
                ui.UiMenuItem(name=_("&switch to the next word"), action=self.initialize),
                ui.UiMenuItem(name=_("&change to level"), action=self._exec_select_level),
                ui.UiMenuItem(name=_("switch &language"), action=self._exec_switch_to_english),
                ui.UiMenuItem(name=_("&reset application"), action=self._exec_reset_application),
                ui.UiMenuItem(name=_("&about"), action=self._exec_about,
                           shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                           shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_applications),
            ],
        )

    def _exec_score(self):
        pass

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self.__create_menu()
        # self.__update_document()
        # self.set_data_line()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        next=self._menu.get_object(self.initialize)
        delete = self._menu.get_object(self._exec_reset_application)
        score=self._menu.get_object(self._exec_score)
        braille_type=Settings().data['system']['braille_type']
        if not self.file_unable:
            next.hide()
            delete.hide()
            score.hide()
            self._menu.rename_item(_("&select a level"), braille_type, self._exec_select_level)
        else:
            next.unhide()
            delete.unhide()
            score.unhide()
            self._menu.rename_item(_("&change to level"), braille_type, self._exec_select_level)
        self.set_data_line()

    def initialize(self):
        # On s'occupe d'abord du score
        t=ManageScore().get_score_level("write word", str(self.letter))
        if t:
            self.score=t
        else:
            self.score=0
        self.word=""
        self.first_word=""
        self.position=0
        if self.is_english:
            game = WriteWord(Path(self.get_apps_folder() / Path("braille_learning")), "en_US")
            game.load_file(self.letter, self.length)
        else:
            game=WriteWord(Path(self.get_apps_folder() / Path("braille_learning")), braille_device_characteristics.get_keyboard_language_country())
            if not game.load_file(self.letter, self.length):
                game=WriteWord(Path(self.get_apps_folder() / Path("braille_learning")), "en_US")
                game.load_file(self.letter, self.length)
        if game.lst_word:
            self.file_unable = True
            self.first_word = game.give_file()
            if Settings().data['braille_learning']['use_vocal']=="auto":
                speak(self.first_word)
        else:
            self.file_unable=False
        self.refresh_document()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        self.set_data_line()
        if self.file_unable and Settings().data['braille_learning']['use_vocal']!="no":
            speak(self.first_word)

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        self.set_data_line()

    # ---------------
    # Menu functions.
    def _exec_test_word(self):
        if Settings().data['braille_learning']['keep_spaces']:
            self.word=self.word.strip(" ")
        if self.word==self.first_word:
            audio=AudioPlayer()
            audio.file_play(str(Path(self.get_apps_folder() / Path("braille_learning/tada.wav"))), 0)
            self._current_dialog = ui.UiInfoDialogBox(message=_("good, you have found the good word!!!"), action=self.initialize)
            self.score+=1
            ManageScore().add_score("write word", str(self.letter), self.score)
            return True
        audio = AudioPlayer()
        audio.file_play(str(Path(self.get_apps_folder() / Path("braille_learning/warning.wav"))), 0)
        self._current_dialog=ui.UiInfoDialogBox(message=_("warning, it's {}, not {}").format(self.first_word,self.word), action=self._exec_cancel_dialog)

    def _exec_select_level(self):
        # On définie la liste par là pour permettre un focus directe
        lst=list(self.level_dict.keys())
        if not self.letter:
            index=lst.index(lst[-1])
        else:
            index = lst.index(self.get_key())
        if not index:
            index=0
        self._current_dialog=ui.UiDialogBox(
            name=_("chose your level"),
            item_list=[
                ui.UiListBox(name=_("&level list"), value=("level", lst), current_index=index),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_select_level),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog
        )

    def _exec_switch_to_english(self):
        # used english words database or the database in current language.
        self.is_english = not self.is_english
        self.initialize()

    def _exec_delete_score(self):
        self._current_dialog=ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to erase the score of this level?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_delete_score),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_reset_application(self):
        self._current_dialog=ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to reset the application?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_reset_application),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        # Display an information dialog box.
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("Application {} version {}. {} Theotime Berthod").format(_("word game"), app_version, "Copyright (C)2023"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_applications(self):
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    # --------------------
    # Dialogbox functions.
    def _exec_valid_select_level(self):
        kwargs=self._current_dialog.get_values()
        self.letter=self.level_dict[kwargs['level']].split(",")
        if len(self.letter)==1 and self.letter[0]=="":
            self.letter=[]
        self.initialize()

    def _exec_show_score(self):
        name=self.get_key()
        self._current_dialog=ui.UiInfoDialogBox(message=_("for level {}, the score is {}").format(name, self.score), action=self._exec_cancel_dialog)


    def _exec_valid_delete_score(self):
        ManageScore().delete_score("write word", str(self.letter))
        self.initialize()

    def _exec_valid_reset_application(self):
        self.word=""
        self.first_word=""
        self.file_unable=False
        self.score=0
        ManageLevel().delete_app("write word")
        ManageScore().delete_app("write word")
        self.refresh_document()

    def message(self, message_type):
        AudioPlayer().file_play(str(Path(self.get_apps_folder() / Path("braille_learning/{}.wav".format(message_type)))), 0 )

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
        log.info("key_id={}".format(key_id))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super().input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # TODO to complete
            if self.file_unable and Settings().data['braille_learning']['write_all']:
                if key_id == Keyboard.KeyId.KEY_CARET_LEFT and self.position >= 1:
                    self.position -= 1
                elif key_id == Keyboard.KeyId.KEY_CARET_RIGHT and self.position <= len(self.word)-1:
                    self.position += 1
                self.set_data_line()
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
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super().input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            # TODO to complete
            if self.file_unable:
                if not Settings().data['braille_learning']['write_all'] and self.first_word[self.position] != character:
                    return self.message("error")
                elif not Settings().data['braille_learning']['write_all']:
                    self.message("ok")
                self.word = self.word[:self.position] + character + self.word[self.position:]
                self.position+=1
                self.set_data_line()
                if not Settings().data['braille_learning']['write_all'] and len(self.first_word)==len(self.word):
                    self._exec_test_word()
        return done

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super().input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # TODO to complete
            if self.file_unable:
                if bramigraph==Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE:
                    if not Settings().data['braille_learning']['write_all'] and self.first_word[self.position]!=" ":
                        return self.message("error")
                    elif not Settings().data['braille_learning']['write_all']:
                        self.message("ok")
                    self.word = self.word[:self.position] + " " + self.word[self.position:]
                    self.position+=1
                    self.set_data_line()
                    if not Settings().data['braille_learning']['write_all'] and len(self.first_word) == len(self.word):
                        self._exec_test_word()
                elif bramigraph==Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE and self.position>=1 and Settings().data['braille_learning']['write_all']:
                    self.word=self.word[:self.position-1]+self.word[self.position:]
                    self.position-=1
                    self.set_data_line()
                elif bramigraph==Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN and Settings().data['braille_learning']['write_all']:
                    self._exec_test_word()
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
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super().input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            if self.file_unable:
                if position<=int(self.length/2)-1:
                    if Settings().data['braille_learning']['use_vocal']!=_("no"):
                        speak(self.first_word)
                elif position==int(self.length/2) and Settings().data['braille_learning']['write_all']:
                    self.position=0
                elif position<=int(self.length)/2+len(self.word) and Settings().data['braille_learning']['write_all']:
                    self.position=position-int(self.length/2)-1
                elif position>=int(self.length/2)+len(self.word) and Settings().data['braille_learning']['write_all']:
                    self.position=len(self.word)
                self.set_data_line()
            done = True
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
        # else call base class decoding.
        done = super(WriteWordApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        pass

    def get_key(self):
        lst=""
        for c in self.letter:
            lst+="{},".format(c)
        lst=lst[:-1]
        for key in self.level_dict:
            if self.level_dict[key]==lst:
                return key

    def shutdown(self, focused):
        ManageLevel().add_level("write word", self.letter)

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if not self.file_unable:
            line=_("you must select a level from the menu")
            braille_static = BnoteApp.lou.to_dots_8(line)
            braille_blinking="\u2800"* len(braille_static)
        else:
            space=""
            for i in range(int(self.length/2)-len(self.first_word)):
                space+=" "
            line="".join([
                "{}{}".format(self.first_word,space),
                "{}".format(self.word)
            ])
            braille_static = BnoteApp.lou.to_dots_8(line)
            braille_blinking = "".join([
                "\u2800" * (int(self.length/2)+self.position),
                "\u28C0",
                "\u2800" * (len(braille_static)-(self.length)+self.position)
            ])
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)
