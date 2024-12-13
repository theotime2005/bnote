"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time

import requests
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
from bnote.tools.clipboard import copy
from bnote.tools.translate import Translate
from translate import Translator
from bnote.tools.settings import Settings
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
import bnote.ui as ui

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, TRANSLATOR_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(TRANSLATOR_APP_LOG)


# pip install translate
class TranslatorApp(BnoteApp):
    """
    Translation application.
    """

    def __init__(self, put_in_function_queue, **kwargs):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super(TranslatorApp, self).__init__(put_in_function_queue)
        # menu creation.
        self._menu = self.__create_menu()
        # Languages list
        self.language_dict = {
            "Afrikaans": "af",
            "Arabic": "ar",
            "Bulgarian": "bg",
            "Croatian": "hr",
            "Czech": "cs",
            "Danish": "da",
            "English": "en",
            "French": "fr",
            "German": "de",
            "Greek": "el",
            "Hebrew": "he",
            "Italian": "it",
            "Island": "is",
            "Lithuanian": "lt",
            "Norwegian": "nb",
            "Dutch": "nl",
            "Polish": "pl",
            "Portuguese": "pt",
            "Russian": "ru",
            "Slovenian": "sl",
            "Spanish": "es",
            "Swedish": "sv",
            "Xhosa": "xh",
            "Zulu": "zu",
        }
        # Translation
        self.is_to_translation = False
        self.source_text = kwargs.get("source", "")
        self.cible_text = ""
        self.base_language = Settings().data["translator"]["base_language"]
        self.language_translate = Settings().data["translator"]["translate_language"]
        # self.base_language = self.get_language()
        self.refresh_document()

    def get_language(self):
        device_language = braille_device_characteristics.get_message_language_country()
        language = device_language.split("_")[0].upper()
        for key, value in self.language_dict.items():
            if value == language:
                return key

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("translator"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&chose languages"), action=self._exec_chose_languages
                ),
                ui.UiMenuItem(
                    name=_("&invert languages"), action=self._exec_invers_language
                ),
                ui.UiMenuItem(name=_("&send to"), action=self._exec_send_translation),
                ui.UiMenuItem(name=_("&clear"), action=self._exec_clear),
            ],
        )

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
        self.set_data_line()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        self._exec_enter_text()
        self.refresh_document()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        self.set_data_line()

    def change_source(self, **kwargs):
        if kwargs.get("source"):
            self.source_text = kwargs["source"]

    # ---------------
    # Menu functions.
    def _exec_enter_text(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("enter text"),
            item_list=[
                ui.UiEditBox(
                    name=_("&text to translate"), value=("text", self.source_text)
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_enter_text),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_chose_languages(self):
        lst_language = list(self.language_dict.keys())
        if not self.base_language:
            index_from = 0
        else:
            index_from = lst_language.index(self.base_language)
        if not self.language_translate:
            index_to = 0
        else:
            index_to = lst_language.index(self.language_translate)
        self._current_dialog = ui.UiDialogBox(
            name=_("chose languages"),
            item_list=[
                ui.UiListBox(
                    name=_("&source"),
                    value=("source", lst_language),
                    current_index=index_from,
                ),
                ui.UiListBox(
                    name=_("&target"),
                    value=("target", lst_language),
                    current_index=index_to,
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_chose_languages),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_invers_language(self):
        # Changing languages
        first = self.base_language
        last = self.language_translate
        self.language_translate = first
        self.base_language = last
        Settings().data["translator"]["base_language"] = self.base_language
        Settings().data["translator"]["translate_language"] = self.language_translate

        # Changing text
        self.source_text = self.cible_text
        self.do_translation()

    def _exec_copy(self):
        copy(self.cible_text)
        self._current_dialog = ui.UiInfoDialogBox(
            _("translation copy to the clipboard"), action=self._exec_cancel_dialog
        )

    def _exec_send_translation(self):
        if not BnoteApp.bluetooth_devices:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("not device connected"), action=self._exec_cancel_dialog
            )
            return
        bluetooth_devices = list(BnoteApp.bluetooth_devices.values())
        self._current_dialog = ui.UiDialogBox(
            name=_("send text to"),
            item_list=[
                ui.UiListBox(
                    name=_("&device"),
                    value=("device", bluetooth_devices),
                    current_index=0,
                ),
                ui.UiListBox(
                    name=_("language &encoding"),
                    value=("encoding", list(Translate.languages_dict.values())),
                    current_index=0,
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_send_translation),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    # --------------------
    # Dialogbox functions.
    def _exec_cancel_dialog(self):
        log.info("callback:_exec_cancel_dialog")
        # Close the dialog box is automatic after button execution.

    def _exec_valid_enter_text(self):
        kwargs = self._current_dialog.get_values()
        if self.source_text == kwargs["text"]:
            self.is_to_translation = True
            return self.set_data_line()
        self.source_text = kwargs["text"]
        if not self.base_language or not self.language_translate:
            self._exec_chose_languages()
        else:
            self._put_in_function_queue(FunctionId.FUNCTION_TRANSLATOR)

    def _exec_valid_chose_languages(self):
        kwargs = self._current_dialog.get_values()
        self.base_language = kwargs["source"]
        self.language_translate = kwargs["target"]
        Settings().data["translator"]["base_language"] = self.base_language
        Settings().data["translator"]["translate_language"] = self.language_translate
        if self.source_text:
            self._put_in_function_queue(FunctionId.FUNCTION_TRANSLATOR)

    def _exec_valid_send_translation(self):
        kwargs = self._current_dialog.get_values()
        id_ = None
        language = None
        for key in BnoteApp.bluetooth_devices:
            if BnoteApp.bluetooth_devices[key] == kwargs["device"]:
                id_ = key
                break
        for language in Translate.languages_dict:
            if language == kwargs["encoding"]:
                break
        if id_ and language:
            self._put_in_function_queue(
                FunctionId.FUNCTION_OPEN_BLUETOOTH,
                **{"device": id_, "text": self.cible_text, "encoding": language},
            )

    # --------------------
    # Key event functions.

    def _exec_clear(self):
        # Clear page
        self.__init__(self._put_in_function_queue)

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
        done = super(TranslatorApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # TODO to complete
            if self.source_text:
                if (
                    key_id == Keyboard.KeyId.KEY_CARET_UP
                    or key_id == Keyboard.KeyId.KEY_CARET_LEFT
                ):
                    self.is_to_translation = False
                    self.set_data_line()
                elif (
                    key_id == Keyboard.KeyId.KEY_CARET_DOWN
                    or key_id == Keyboard.KeyId.KEY_CARET_RIGHT
                ):
                    self.is_to_translation = True
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
        done = super(TranslatorApp, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            # TODO to complete
            pass
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
        done = super(TranslatorApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # TODO to complete
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
                if not self.is_to_translation:
                    self._exec_enter_text()
                else:
                    self._exec_copy()
            elif (
                bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_TAB
                or bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB
            ):
                self.comute_text()
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
        done = super(TranslatorApp, self).input_interactive(
            modifier, position, key_type
        )
        if not done:
            # interactive key treatment
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
        if function_id == FunctionId.FUNCTION_TRANSLATOR:
            self._current_dialog = ui.UiInfoDialogBox(_("translating..."))
            time.sleep(1.0)
            done = self.do_translation()
            self._current_dialog = None
        elif function_id == FunctionId.FUNCTION_ASK_LANGUAGE:
            done = self._exec_chose_languages()
        else:
            # else call base class decoding.
            done = super(TranslatorApp, self).input_function(*args, **kwargs)
        return done

    def comute_text(self):
        if not self.source_text:
            return False
        self.is_to_translation = not self.is_to_translation
        self.set_data_line()

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        pass

    # --------------------
    # Document functions.
    def do_translation(self):
        # Theo: La traduction ne peut dépasser 500 caractères. Est-ce qu'on bloque ou est-ce qu'on couppe?
        if len(self.source_text) >= 500:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("you cannot translate text with more than 500 characters."),
                action=self._exec_enter_text,
            )
        try:
            self.cible_text = Translator(
                self.language_dict[self.language_translate],
                self.language_dict[self.base_language],
            ).translate(self.source_text)
            self.is_to_translation = True
            self.set_data_line()
        except requests.ConnectionError:
            self._current_dialog = ui.UiInfoDialogBox(
                message=_(
                    "the connection to the translation service failed. Check your connexion and try again."
                ),
                action=self._exec_cancel_dialog,
            )

    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if self.is_to_translation:
            line = _("Translation ({}): {}").format(
                self.language_translate, self.cible_text
            )
        else:
            line = _("Source ({}): {}").format(self.base_language, self.source_text)
        braille_static = BnoteApp.lou.to_dots_8(line)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)
