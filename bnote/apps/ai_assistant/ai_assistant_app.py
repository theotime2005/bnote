"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import random
import requests
import time
from enum import Enum

from bnote.apps.ai_assistant.ai_eurobraille import AiEurobraille, AiEurobrailleCrypto
from bnote.apps.bnote_app import FunctionId, BnoteApp
from bnote.apps.edt.editor_base_app import EditorBaseApp
import bnote.apps.edt.edt as editor
import bnote.ui as ui
from bnote.apps.edt.edt import Caret
from bnote.tools.keyboard import Keyboard

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG, logging
from bnote.tools.settings import Settings

log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class AiAssistantApp(EditorBaseApp):
    class ParsingState(Enum):
        NOTHING = 0
        ME = 1
        AI = 2

    MAX_WORD_COUNT = 1000
    # MAX_WORD_COUNT = 1000
    # Try RENEW_TOKEN_MAX_RETRY time to renew automatically an expired JWT token
    RENEW_TOKEN_MAX_RETRY = 2
    # Try CREATE_ACCOUNT_MAX_RETRY time to create an account for this bnote (can be usefully after a server restart)
    CREATE_ACCOUNT_MAX_RETRY = 2
    # Try ERROR401_MAX_RETRY time to get a response from server (try to avoid user bothering)
    ERROR401_MAX_RETRY = 2

    USER_PROMPT_MARKER = ":?:"
    AI_REPLY_MARKER = ":-:"

    def __init__(self, put_in_function_queue, file_name=None, language=None, read_only=True):
        super().__init__(put_in_function_queue, file_name, language, read_only, no_context=True)
        # Current instance of ai assistant dialog box, with items references.
        self._ui_ai_assistant_dialog = None
        self._ui_server_unavailable_or_no_internet_dialog = None
        self._ui_server_error_message_dialog = None
        self.renew_token_count = 0
        self.create_account_count = 0
        self.error_401_count = 0
        self.message = ""
        self.chat = []
        self.start_of_me_question_saved_caret = Caret()
        self.start_of_ai_response_saved_caret = Caret()
        self.wait_ai_answer = False

        # Wait editor to be ready
        while self.editor is None:
            time.sleep(0.01)

        # Fill the chat from previous saved session
        self.init_chat_from_editor()

        # Instantiates the singleton
        AiEurobraille(AiEurobrailleCrypto(random.seed).decrypt(Settings().data['ai_eurobraille']['username']),
                      AiEurobrailleCrypto(random.seed).decrypt(Settings().data['ai_eurobraille']['password']),
                      AiEurobrailleCrypto(random.seed).decrypt(Settings().data['ai_eurobraille']['token']),)
        Settings().data['ai_eurobraille']['username'] = AiEurobrailleCrypto(random.seed).encrypt(
            AiEurobraille().username)
        Settings().data['ai_eurobraille']['password'] = AiEurobrailleCrypto(random.seed).encrypt(
            AiEurobraille().password)
        Settings().data['ai_eurobraille']['token'] = AiEurobrailleCrypto(random.seed).encrypt(AiEurobraille().token)
        Settings().save()

    @staticmethod
    def known_extension():
        return ".ai_txt",

    @staticmethod
    def read_data_file(lou, full_file_name, language, add_line, ended, sheet_name=None):
        return editor.ReadFile(lou, full_file_name, language, add_line, ended, sheet_name)

    def write_data_file(self, lou, full_file_name, get_line, on_end, function):
        return editor.WriteFile(full_file_name, get_line, on_end, function)

    def _create_menu(self):
        # Instantiate menu.
        app_name = _("ai assistant")
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
                        ui.UiMenuItem(name=_("&save"), action=self._exec_my_save,
                                      shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='S'),
                        ui.UiMenuItem(name=_("sta&tistics"), action=self._exec_statistics),

                    ]),
                ui.UiMenuBar(
                    name=_("&edit"),
                    menu_item_list=[
                        *self.create_sub_menu_selection(),
                        *[
                            ui.UiMenuItem(name=_("curs&or"), action=self._exec_cursor),
                            ui.UiMenuItem(name=_("forward in grade2 braille"), action=self._toggle_grade2_from_menu),
                        ],
                    ]),
                self.create_sub_menu_goto(),
                self.create_sub_menu_find(),
                self.create_sub_menu_bookmark(),
                self.create_sub_menu_vocalize(),
                ui.UiMenuBar(
                    name=_("a&ccount"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&renew access token"), action=self._exec_renew_access_token),
                    ]),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def _exec_my_save(self):
        self._exec_save()

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        pass

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
        # AiAssistant, specific functions
        # Enter : Open AiAssistant dialogbox.
        done = False
        if self._current_dialog is None and not self._in_menu:
            # Simple key decoding for Daisy shorcut.
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
                # Open the dialog when the user can ask a new question
                if not self.wait_ai_answer:
                    self._exec_ai_assistant_dialog()
                done = True
        if not done:
            done = super().input_bramigraph(modifier, bramigraph)
        if not done:
            # Specific commands treatment.
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

        if function_id == FunctionId.FUNCTION_GET_RESPONSE_AI_ASSISTANT:
            self._exec_get_chat_response()
            return True

        # Call base class decoding.
        done = super().input_function(*args, **kwargs)
        return done

    def _exec_ssl_cert_verification_error(self, e):
        self._ui_server_unavailable_or_no_internet_dialog = ui.UiInfoDialogBox(
            message=_("unable to verify your certificate. Check if your bnote is on the correct date and time."),
            action=self._exec_cancel_dialog_and_cleanup_text
        )
        self._current_dialog = self._ui_server_unavailable_or_no_internet_dialog
        self.refresh_app()

    def _exec_server_unavailable_or_no_internet(self, e):
        if AiEurobraille().is_connected_to_internet():
            # print(f"{e=}")

            if isinstance(e, requests.exceptions.ConnectTimeout):
                self._ui_server_unavailable_or_no_internet_dialog = ui.UiInfoDialogBox(
                    message=_("eurobraille server responds too slowly."),
                    action=self._exec_cancel_dialog_and_cleanup_text
                )
            elif isinstance(e, requests.exceptions.ReadTimeout):
                self._ui_server_unavailable_or_no_internet_dialog = ui.UiInfoDialogBox(
                    message=_("ai server unavailable or responding too slowly."),
                    action=self._exec_cancel_dialog_and_cleanup_text
                )
            else:
                self._ui_server_unavailable_or_no_internet_dialog = ui.UiInfoDialogBox(
                    message=_("error = ") + f"{e}",
                    action=self._exec_cancel_dialog_and_cleanup_text
                )
        else:
            self._ui_server_unavailable_or_no_internet_dialog = ui.UiInfoDialogBox(
                message=_("no internet."),
                action=self._exec_cancel_dialog_and_cleanup_text
            )
        self._current_dialog = self._ui_server_unavailable_or_no_internet_dialog
        self.refresh_app()

    def _exec_server_error_message_dialog(self, response):
        if response.status_code == 404:
            message = _("error 404 - not found")
        elif response.status_code == 429:
            if response.text == "Unauthorized: quota_1":
                message = _("you have used your daily quota. Try again tomorrow.")
            elif response.text == "Unauthorized: quota_2":
                message = _("you have used your weekly quota. Try again next monday.")
            elif response.text == "Unauthorized: quota_3":
                message = _("you have used your monthly quota. Try again next month.")
            elif response.text == "Unauthorized: quota_4":
                message = _("you have used your annual quota. Try again next year.")
        elif response.status_code == 503:
            message=_("eurobraille server unavailable.")
        else:
            message = "".join((_("error = "), " ", str(response.status_code), " - ", response.text))

        self._ui_server_error_message_dialog = ui.UiInfoDialogBox(
            message=message,
            action=self._exec_cancel_dialog_and_cleanup_text
        )
        self._current_dialog = self._ui_server_error_message_dialog
        self.refresh_app()

    def _exec_cancel_dialog_and_cleanup_text(self):
        with self.lock:
            self.editor.read_only = False
            # Move the caret to the start of me question (that need to be removed if error)
            self.editor.set_caret(self.start_of_me_question_saved_caret)
            # Select text from the start of the waiting message to the end of the document.
            self.editor.function(editor.Editor.Functions.MOVE_END, **{'shift': True, 'ctrl': True})
            # Delete the ai waiting message
            self.editor.function(editor.Editor.Functions.BACKSPACE, **{})
            # Remove the empty paragraph.
            self.editor.function(editor.Editor.Functions.BACKSPACE, **{})
            # The user can ask a new question
            self.wait_ai_answer = False
            self._current_dialog = None
        self.refresh_app()

    def _exec_ai_assistant_dialog(self):
        # log.critical(f"_exec_ai_assistant_dialog")

        if self._ui_ai_assistant_dialog is None:
            # Create ai assistant dialog box.
            self._ui_ai_assistant_dialog = ui.UiDialogBox(
                name=_("ai assistant"),
                item_list=[
                    ui.UiEditBox(name=_("&message"), value=('message', "")),
                    ui.UiButton(name=_("&ok"), action=self._valid_ai_assistant_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog
            )
            self._current_dialog = self._ui_ai_assistant_dialog
        else:
            # Restore ai assistant  dialog.
            # Put focus on edit box.
            ui_object = self._ui_ai_assistant_dialog.set_first_focusable_object()
            # Enter in edit mode and select the contains.
            if ui_object:
                ui_object.exec_action()
                ui_object.exec_select_all()
            # Current dialog is ai assistant  dialogbox.
            self._current_dialog = self._ui_ai_assistant_dialog
            # Construct braille display.
            self._ui_ai_assistant_dialog.ask_update_braille_display()

    def _valid_ai_assistant_dialog(self):
        # Get all dialogbox value.
        kwargs = self._current_dialog.get_values()

        # First check size chat limit
        with self.lock:
            (paragraphs_count, words_count, characters_count) = self.editor.statistics()
            # log.error(f"{words_count=}")
            if words_count + len(kwargs['message'].split()) > AiAssistantApp.MAX_WORD_COUNT:
                # Ask confirmation to delete scores of one level.
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=_(
                        "you have reached the maximum chat size. You can start a new one by close this current one."),
                    buttons=[ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog), ],
                    action_cancelable=self._exec_cancel_dialog,
                )
                return

        # Get the question
        self.message = kwargs['message']
        self.chat.append({"role": "user", "content": f"{self.message}"}, )

        # Append the user test
        with self.lock:
            self.editor.read_only = False
            # Move the caret to the end of the document
            self.editor.function(editor.Editor.Functions.MOVE_END, **{'shift': False, 'ctrl': True})
            # Save the caret pos to revert the user question in the document if an error with the server occurs.
            self.start_of_me_question_saved_caret = Caret(self.editor.caret())
            # Append the user text
            self.editor.function(editor.Editor.Functions.PUT_STRING,
                                 **{'text': "".join(("\n", self.USER_PROMPT_MARKER, self.message))})
            # Append Carrier return and save the caret position.
            self.editor.function(editor.Editor.Functions.PUT_STRING,
                                 **{'text': "\n"})
            # Save the caret pos to replace the waiting message with the response.
            self.start_of_ai_response_saved_caret = Caret(self.editor.caret())
            # Append waiting message
            self.editor.function(editor.Editor.Functions.PUT_STRING,
                                 **{'text': "".join(("\n", self.AI_REPLY_MARKER, _("please wait...")))})
            # Move the caret to the start of the waiting message
            self.editor.set_caret(self.start_of_ai_response_saved_caret)
            self.editor.read_only = True
            # The user cannot ask a new question while answer is pending
            self.wait_ai_answer = True

        # Show it on braille.
        last_paragraph_index = self.editor.paragraphs_count() - 1
        if last_paragraph_index != -1:
            self.editor.set_caret_on_paragraph(last_paragraph_index)

        # Call chatGPT via a function to be able to refresh the document during processing.
        self._put_in_function_queue(FunctionId.FUNCTION_GET_RESPONSE_AI_ASSISTANT)

    def _exec_get_chat_response(self):
        response = None
        success = False
        try:
            # Pass the message to ai.
            (success, response) = AiEurobraille().get_chat_response(self.chat)
        except requests.exceptions.SSLError as e:
            # print(f"except requests.exceptions.SSLError : {e=}")
            self._exec_ssl_cert_verification_error(e)
        except ValueError as e:
            self.__server_error()
        except KeyError as e:
            self.__server_error()
        except requests.exceptions.ConnectTimeout as e:
            # print(f"except requests.exceptions.ConnectTimeout : {e=}")
            self._exec_server_unavailable_or_no_internet(e)
        except requests.exceptions.RequestException as e:
            # print(f"except requests.exceptions.RequestException : {e=}")
            self._exec_server_unavailable_or_no_internet(e)
        finally:
            if response is not None:
                if not success:
                    if isinstance(response, requests.Response):
                        if (response.status_code == 401 and response.text == "Unauthorized" and
                                self.renew_token_count < self.RENEW_TOKEN_MAX_RETRY):
                            # Don't bother user with token renew
                            self.renew_token_count += 1
                            (s, r) = AiEurobraille().get_token()
                            if not s:
                                # Don't bother user with login creation
                                (s, r) = AiEurobraille().create_login()
                                if s:
                                    Settings().data['ai_eurobraille']['username'] = AiEurobrailleCrypto(
                                        random.seed).encrypt(AiEurobraille().username)
                                    Settings().data['ai_eurobraille']['password'] = AiEurobrailleCrypto(
                                        random.seed).encrypt(AiEurobraille().password)
                                    # Try again to get a token
                                    (s, r) = AiEurobraille().get_token()

                            # Save the token if success.
                            if s:
                                Settings().data['ai_eurobraille']['token'] = (AiEurobrailleCrypto(random.seed).
                                                                              encrypt(AiEurobraille().token))
                                Settings().save()
                            return self._exec_get_chat_response()
                        elif response.status_code == 401 and self.error_401_count < self.ERROR401_MAX_RETRY:
                            # Don't bother user with error 401 if it can be recovered automatically
                            self.error_401_count += 1
                            return self._exec_get_chat_response()
                        elif (response.status_code == 500 and response.text == "Eurobraille server: User not found" and
                              self.create_account_count < self.CREATE_ACCOUNT_MAX_RETRY):
                            # Don't bother user with account creation
                            self.create_account_count += 1
                            if AiEurobraille().create_login():
                                if AiEurobraille().get_token():
                                    Settings().data['ai_eurobraille']['username'] = AiEurobrailleCrypto(
                                        random.seed).encrypt(AiEurobraille().username)
                                    Settings().data['ai_eurobraille']['password'] = AiEurobrailleCrypto(
                                        random.seed).encrypt(AiEurobraille().password)
                                    Settings().data['ai_eurobraille']['token'] = AiEurobrailleCrypto(
                                        random.seed).encrypt(AiEurobraille().token)
                                    Settings().save()
                            return self._exec_get_chat_response()
                        else:
                            # Put error message in message dialog box
                            self._exec_server_error_message_dialog(response)

                # Update document and chat data
                with self.lock:
                    self.editor.read_only = False
                    if success:
                        # reset error counters.
                        self.renew_token_count = 0
                        self.create_account_count = 0
                        self.error_401_count = 0
                        # Move the caret to the start of the waiting message
                        self.editor.set_caret(self.start_of_ai_response_saved_caret)
                        # Select text from the start of the waiting message to the end of the document.
                        self.editor.function(editor.Editor.Functions.MOVE_END, **{'shift': True, 'ctrl': True})
                        # Append the ai response
                        self.editor.function(editor.Editor.Functions.PUT_STRING,
                                             **{'text': "".join((self.AI_REPLY_MARKER, response))})
                        # Move the caret on the start of the paragraph
                        self.editor.set_caret(self.start_of_ai_response_saved_caret)
                        self.editor.read_only = True
                        # Append Ai response to the chat
                        self.chat.append({"role": "assistant", "content": f"{response}"}, )
                    else:
                        # Move the caret to the start of the question that failed
                        self.editor.set_caret(self.start_of_me_question_saved_caret)
                        # Select text from the start of the question to the end of the document.
                        self.editor.function(editor.Editor.Functions.MOVE_END, **{'shift': True, 'ctrl': True})
                        self.editor.read_only = True
                        # Remove the last question (that have no answer) from the chat
                        self.chat.pop()

                # The user can ask a new question
                self.wait_ai_answer = False

                # Refresh the change on the document.
                self.refresh_app()

    def __server_error(self):
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("unable to communicate with the server. Check your Internet connexion."),
            action=self._exec_cancel_dialog)

    def _exec_renew_access_token(self):
        # Don't bother user with login creation
        (s, r) = AiEurobraille().create_login()
        if s:
            Settings().data['ai_eurobraille']['username'] = AiEurobrailleCrypto(
                random.seed).encrypt(AiEurobraille().username)
            Settings().data['ai_eurobraille']['password'] = AiEurobrailleCrypto(
                random.seed).encrypt(AiEurobraille().password)
            # Get a new token
            (s, r) = AiEurobraille().get_token()
            # Save the token if success.
            if s:
                Settings().data['ai_eurobraille']['token'] = (AiEurobrailleCrypto(random.seed).
                                                              encrypt(AiEurobraille().token))
                Settings().save()

        message = _("unable to renew access token.")
        if s:
            message = _("access token successfully renewed.")

        self._current_dialog = ui.UiInfoDialogBox(
            message=message,
            action=self._exec_cancel_dialog)

    def init_chat_from_editor(self):
        state = self.ParsingState.NOTHING
        current_text = ""
        for paragraph_index in range(0, self.editor.paragraphs_count()):
            paragraph = self.editor.paragraph(paragraph_index)
            paragraph_text = paragraph.paragraph_text()
            if paragraph_text.startswith(self.USER_PROMPT_MARKER):
                if state == self.ParsingState.AI:
                    self.append_assistant_content_in_chat(current_text)
                elif state == self.ParsingState.ME:
                    self.append_user_content_in_chat(current_text)

                state = self.ParsingState.ME
                current_text = paragraph_text
            elif paragraph_text.startswith(self.AI_REPLY_MARKER):
                if state == self.ParsingState.ME:
                    self.append_user_content_in_chat(current_text)
                elif state == self.ParsingState.AI:
                    self.append_assistant_content_in_chat(current_text)

                state = self.ParsingState.AI
                current_text = paragraph_text
            else:
                if state == self.ParsingState.ME or state == self.ParsingState.AI:
                    current_text = "".join((current_text, paragraph_text))

        if state == self.ParsingState.ME:
            self.append_user_content_in_chat(current_text)
        elif state == self.ParsingState.AI:
            self.append_assistant_content_in_chat(current_text)

        if (self.editor.paragraphs_count() == 1) and (len(self.editor.paragraph_text(0)) == 0):
            self._append_instructions()

    def append_assistant_content_in_chat(self, text):
        if text.startswith(self.AI_REPLY_MARKER):
            text = text.replace(self.AI_REPLY_MARKER, "", 1)
        self.chat.append({"role": "assistant", "content": text})

    def append_user_content_in_chat(self, text):
        if text.startswith(self.USER_PROMPT_MARKER):
            text = text.replace(self.USER_PROMPT_MARKER, "", 1)
        self.chat.append({"role": "user", "content": text})

    def _append_instructions(self):
        with self.lock:
            # If the file is empty, append the short tutorial
            self.editor.read_only = False
            self.editor.function(editor.Editor.Functions.PUT_STRING,
                                 **{'text': _("press the Enter key to start a chat with Eurobraille AI...")})
            # Move the caret on the start of the paragraph
            self.editor.set_caret(self.start_of_ai_response_saved_caret)
            self.editor.read_only = True

    def shutdown(self, focused):
        """
        Overload editor_base_app.
        Nothing to do for wikipedia document.
        """
        return
