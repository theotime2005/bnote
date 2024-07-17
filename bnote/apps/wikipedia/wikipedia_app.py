"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import time

import requests
import wikipedia
from bnote.apps.bnote_app import FunctionId, BnoteApp
from bnote.apps.edt.editor_base_app import EditorBaseApp
from bnote.apps.repeated_timer import RepeatedTimer
import bnote.ui as ui
from bnote.tools.keyboard import Keyboard
from bnote.stm32.braille_device_characteristics import braille_device_characteristics


# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, EDITOR_APP_LOG, logging
log = ColoredLogger(__name__)
log.setLevel(EDITOR_APP_LOG)


class WikipediaApp(EditorBaseApp):

    SUMMARY_SENTENCES_COUNT = 10

    def __init__(self, put_in_function_queue, file_name=None, language=None, read_only=True):
        super().__init__(put_in_function_queue, file_name, language, read_only, no_context=True)
        # Current instance of wikipedia dialog box, with items references.
        self._ui_wiki_dialog = None
        self._ui_wiki_find = ""
        self._ui_wiki_suggestions = None
        # Ask to open the dialog box.
        self._put_in_function_queue(FunctionId.FUNCTION_OPEN_WIKIPEDIA_DIALOG)
        # Create reading timer.
        self.timer = RepeatedTimer(1, self.play_timeout)

    def _create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        app_name = _("wikipedia")
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
                        ui.UiMenuItem(name=_("&research"), action=self._exec_research),
                        ui.UiMenuItem(name=_("clean&up"), action=self._exec_cleanup),
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
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def _update_menu_items(self):
        """
        Change the name of the menu item when enter in menu.
        """
        pass

    def play_timeout(self):
        """
        Call each second by repeated timer thread.
        """
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"play_timeout thread id {threading.current_thread().ident}")
        self._put_in_function_queue(FunctionId.FUNCTION_WIKIPEDIA_TIME_OUT)

    def on_play_timer(self):
        """
        Event handle each second by ui thread.
        """
        # if EDITOR_APP_LOG <= logging.ERROR:
        #     log.error(f"on_play_timer thread id {threading.current_thread().ident}")
        if self._current_dialog is not None:
            if self._current_dialog == self._ui_wiki_dialog:
                suggestions = self._update_suggestions()
                if suggestions is not None:
                    self._ui_wiki_suggestions.set_list(suggestions, 0)
                    # Construct braille display.
                    self._ui_wiki_dialog.ask_update_braille_display()
        elif self._ui_wiki_dialog is not None:
            pass
            # Clean up references
            # self._ui_wiki_dialog = None
            # self._ui_wiki_find = ""
            # self._ui_wiki_suggestions = None

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
        # Wikipedia, specific functions
        # Enter : Open wikipedia dialogbox.
        done = False
        if self._current_dialog is None and not self._in_menu:
            # Simple key decoding for Daisy shorcut.
            if bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
                self._exec_wikipedia_dialog()
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
        if function_id == FunctionId.FUNCTION_OPEN_WIKIPEDIA_DIALOG:
            self._exec_wikipedia_dialog()
            done = True
        elif function_id == FunctionId.FUNCTION_WIKIPEDIA_TIME_OUT:
            self.on_play_timer()
            done = True
        else:
            # Call base class decoding.
            done = super().input_function(*args, **kwargs)
        return done

    def _exec_research(self):
        self._exec_wikipedia_dialog()

    def _exec_wikipedia_dialog(self):
        log.critical(f"Wikipedia_dialog")
        # Set wikipedia to current messages language.
        language = braille_device_characteristics.get_message_language_country()[0:2]
        wikipedia.set_lang(language)
        if self._ui_wiki_dialog is None:
            # Create wikipedia dialog box.
            self._ui_wiki_suggestions = ui.UiListBox(name=_("&suggestions"), value=('suggestions', []), current_index=0)
            self._ui_wiki_dialog = ui.UiDialogBox(
                name=_("wikipedia"),
                item_list=[
                    ui.UiEditBox(name=_("&find"), value=('find', "")),
                    self._ui_wiki_suggestions,
                    ui.UiButton(name=_("&ok"), action=self._valid_wikipedia_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                    # ui.UiCheckBox(name=_("summary &only"), value=('summary', False)),
                ],
                action_cancelable=self._exec_cancel_dialog
            )
            self._current_dialog = self._ui_wiki_dialog
        else:
            # Restore wikipedia dialog.
            # Put focus on edit box.
            ui_object = self._ui_wiki_dialog.set_first_focusable_object()
            # Enter in edit mode and select the contains.
            if ui_object:
                ui_object.exec_action()
                ui_object.exec_select_all()
            # Current dialog is wiki dialogbox.
            self._current_dialog = self._ui_wiki_dialog
            # Construct braille display.
            self._ui_wiki_dialog.ask_update_braille_display()

    def _update_suggestions(self):
        result = None
        # Get all dialogbox value.
        kwargs = self._ui_wiki_dialog.get_values()
        find = kwargs['find']
        if self._ui_wiki_find != find:
            try:
                if len(find) == 0:
                    # Search with space to empty the suggestion list
                    result = wikipedia.search(" ")
                else:
                    result = wikipedia.search(find)
            except requests.exceptions.ConnectionError:
                log.error("Wikipedia _update_suggestions: ConnectionError")
            log.critical(f"suggestions = {result}")
        self._ui_wiki_find = find
        return result

    def _valid_wikipedia_dialog(self):
        # Get all dialogbox value.
        kwargs = self._current_dialog.get_values()
        find = kwargs['find']
        wiki_page_title = kwargs['suggestions']
        # summary = kwargs['summary']
        lines = ["", ]
        # Clean up references
        # self._ui_wiki_dialog = None
        # self._ui_wiki_find = ""
        # self._ui_wiki_suggestions = None
        if (wiki_page_title is not None) and len(wiki_page_title) <= 0:
            # No suggestion.
            self._current_dialog = ui.UiInfoDialogBox(message=_("there is no text found in the suggestion's combobox."),
                                                   action=self._exec_cancel_dialog)
            return
        try:
            # if summary:
            #     content = wikipedia.summary(
            #         wiki_page_title, auto_suggest=True, redirect=True, sentences=WikipediaApp.SUMMARY_SENTENCES_COUNT)
            #     log.critical(f"summary = {content}")
            # else:
            page = wikipedia.page(wiki_page_title, auto_suggest=False, redirect=True, )
            content = page.content
            lines = content.split("\n")

        except UnboundLocalError as e:
            # FIXME : Retirer except UnboundLocalError dans les prochaine version pour vérifier si le crash est corrigé.
            #  Dans wikipedia.py, il faudrait avoir en ligne 287 un ligne qui initialise suggestion.
            #  suggestion = article pour eviter une exception en ligne 304...
            #  wikipedia.exceptions.PageError: Page id "Aa_(Hydrologie)" does not match any pages. Try another id!
            #  During handling of the above exception, another exception occurred:
            #  UnboundLocalError: local variable 'suggestion' referenced before assignment
            self.__not_found_text()
        except wikipedia.PageError as e:
            self.__not_found_text()
        except wikipedia.DisambiguationError as e:
            self.__not_found_text()
        except ValueError as e:
            self.__not_found_text()
        except KeyError as e:
            self.__not_found_text()
        finally:
            self.editor = self._create_editor(lines)

    def __not_found_text(self):
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("the text is not found or is ambiguous."
                      " try to chose another item in the suggestion's combobox."),
            action=self._exec_cancel_dialog)

    def _exec_close(self):
        self._killed = True
        self._put_in_function_queue(FunctionId.FUNCTION_CLOSE_WIKIPEDIA, **{'app': self})

    def on_close(self):
        """
        Call just before the application removing from internal menu.
        """
        log.debug("on_close")
        self.timer.stop()
        while self.timer.is_running:
            time.sleep(0.1)
        log.debug("timer is closed")

    def shutdown(self, focused):
        """
        Overload editor_base_app.
        Nothing to do for wikipedia document.
        """
        return
