"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from bnote.tools.audio_player import AudioPlayer
from bnote.tools.io_util import Gpio
from bnote.tools.quick_search import QuickSearch
from bnote.tools.settings import Settings
from bnote.tools.volume_speed_dialog_box import VolumeDialogBox
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
from bnote.tools.volume import Volume
import bnote.ui as ui
from bnote.apps.media.radio import Radio, RADIO_SERVER_URL
# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, RADIO_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(RADIO_APP_LOG)


class RadioApp(BnoteApp):
    """
    Skeleton application.
    """
    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super().__init__(put_in_function_queue)
        # menu creation.
        self._menu = self.__create_menu()
        # radio list.
        self.radio = Radio()
        er, radio_dict = self.radio.get_local_list()
        if er or len(radio_dict) == 0:
            self.__radio_list = None
        else:
            self.__radio_list = sorted(list(radio_dict.keys()))
        self.__radio_index = 0
        # document refresh.
        self.set_data_line()
        # hp-headphone survey
        self.current_output = None
        # current values of radio dialog.
        self.dialog_radio_name = ""
        self.dialog_radio_url = ""
        # The QuickSearch instance.
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("radio"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&radio"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&radio by url"), action=self._exec_radio_dialog,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='U'),
                        ui.UiMenuItem(name=_("&delete radio"), action=self.__delete_radio,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                                   shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE),
                        ui.UiMenuItem(name=_("&web update list"), action=self._exec_web_update_list,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='N'),
                        # ui.UiMenuItem(name=_("&local update list"), action=self._exec_local_update_list),
                    ]),
                ui.UiMenuBar(
                    name=_("&play"),
                    menu_item_list=[
                        ui.UiMenuItem(name=_("&start"), action=self.__exec_play_radio,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='L'),
                        ui.UiMenuItem(name=_("&stop"), action=self._exec_stop,
                                   shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL, shortcut_key='T'),
                        ui.UiMenuItem(name=_("&volume"), action=self._exec_volume),
                    ]),
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
        To overload by each app if necessary.
        """
        self.set_data_line()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        # Refresh
        self.set_data_line()

    # ---------------
    # Menu functions.
    def _exec_stop(self):
        self.radio.stop_radio()

    def _exec_web_update_list(self):
        er, radios = self.radio.get_web_list(RADIO_SERVER_URL)
        if er:
            self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        else:
            if radios is None or len(radios) == 0:
                self.__radio_list = None
            else:
                self.__radio_list = sorted(list(radios.keys()))

    def _exec_local_update_list(self):
        er, radios = self.radio.get_local_list()
        if er:
            self._current_dialog = ui.UiInfoDialogBox(message=er.__str__(), action=self._exec_cancel_dialog)
        else:
            self.__radio_list = sorted(list(radios.keys()))

    def _exec_radio_dialog(self):
        self._current_dialog = ui.UiDialogBox(
            name=_("add radio"),
            item_list=[
                ui.UiEditBox(name=_("name"),
                          value=('name', BnoteApp.braille_form(self.dialog_radio_name))
                          ),
                ui.UiEditBox(name=_("url"),
                          # value=('url', BnoteApp.braille_form("http://direct.fipradio.fr/live/fip-webradio6.mp3"))
                          value=('url', BnoteApp.braille_form(self.dialog_radio_url))
                          ),
                ui.UiButton(name=_("&play"), action=self._exec_radio_by_url),
                ui.UiButton(name=_("add to &list"), action=self._add_radio_by_url),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_radio_by_url(self):
        kwarg = self._current_dialog.get_values()
        self.dialog_radio_url = kwarg['url']
        self.radio.start_radio(self.dialog_radio_url)

    def _add_radio_by_url(self):
        kwarg = self._current_dialog.get_values()
        self.dialog_radio_name = kwarg['name']
        self.dialog_radio_url = kwarg['url']
        if self.dialog_radio_name in self.__radio_list:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("are you sure to replace the radio {}").format(self.dialog_radio_name),
                buttons=[
                    ui.UiButton(name=_("&yes"), action=self.__exec_valid_add_radio),
                    ui.UiButton(name=_("&no"), action=self._exec_radio_dialog),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            self.__exec_valid_add_radio()

    def __exec_valid_add_radio(self):
        # Add radio to the list
        radio_dict = self.radio.add_radio(self.dialog_radio_name, self.dialog_radio_url, 'user')
        if radio_dict:
            self.__radio_list = sorted(list(radio_dict.keys()))
            self.__radio_index = self.__radio_list.index(self.dialog_radio_name)
            # re-write the user file
            self.radio.write_user_file()

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
        done = super(RadioApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # command treatment for document.
            command_switcher = {
                Keyboard.KeyId.KEY_CARET_UP: self.__previous_line,
                Keyboard.KeyId.KEY_CARET_DOWN: self.__next_line,
                Keyboard.KeyId.KEY_START_DOC:  self.__first_line,
                Keyboard.KeyId.KEY_END_DOC: self.__last_line,
            }
            function = command_switcher.get(key_id, None)
            if function:
                # Execute the function
                done = function()
                if done:
                    # Refresh
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
        done = super(RadioApp, self).input_character(modifier, character, data)
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
            Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: self.__exec_play_stop_radio,
            Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: self.__delete_radio,
        }
        log.info("modifier={} bramigraph={}".format(modifier, bramigraph))
        done = super(RadioApp, self).input_bramigraph(modifier, bramigraph)
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
                    self.set_data_line()
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
        done = super(RadioApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            self.__exec_play_stop_radio()
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
        if function_id == FunctionId.FUNCTION_SETTINGS_CHANGE:
            # Change radio volume
            if self.radio.is_playing() and (kwargs['section'] == 'radio') and \
                    ((kwargs['key'] == 'volume_headphone') or (kwargs['key'] == 'volume_hp')):
                self.radio.set_volume()
                log.error(f"volume stored <{AudioPlayer().get_volume()}>")
        # else call base class decoding.
        done = super(RadioApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        headphone = Gpio().is_head_phone()
        output_change = False
        if headphone:
            if self.current_output != 'headphone':
                output_change = True
                self.current_output = 'headphone'
        elif self.current_output != 'hp':
            output_change = True
            self.current_output = 'hp'
        if output_change:
            self.radio.restart_radio()

    # --------------------
    # Line change.
    def __previous_line(self):
        if self.__radio_list is not None and self.__radio_index > 0:
            self.__radio_index -= 1
            return True

    def __next_line(self):
        if self.__radio_list is not None and self.__radio_index < len(self.__radio_list) -1:
            self.__radio_index += 1
            return True

    def __first_line(self):
        if self.__radio_list is not None and self.__radio_index > 0:
            self.__radio_index = 0
            return True

    def __last_line(self):
        if self.__radio_list is not None and self.__radio_index < (len(self.__radio_list) - 1):
            self.__radio_index = len(self.__radio_list) - 1
            return True

    def __exec_play_stop_radio(self):
        if self.__radio_list is not None:
            if self.radio.is_playing_radio(self.__radio_list[self.__radio_index]):
                self.radio.stop_radio()
            else:
                self.radio.play_radio(self.__radio_list[self.__radio_index])
            return True

    def __exec_play_radio(self):
        # self.radio.start_radio(url="http://direct.fipradio.fr/live/fip-webradio6.mp3")
        if self.__radio_list is not None:
            self.radio.play_radio(self.__radio_list[self.__radio_index])
            return True

    def __delete_radio(self):
        if self.__radio_list:
            # Ask confirmation to delete scores of one level.
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("are you sure to delete the radio {}").format(self.__radio_list[self.__radio_index]),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self.__exec_valid_delete_radio),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )

    def __exec_valid_delete_radio(self):
        if self.__radio_list is not None:
            self.radio.delete_radio(self.__radio_list[self.__radio_index])
            self.__radio_list.pop(self.__radio_index)
            if len(self.__radio_list) <= self.__radio_index:
                if self.__radio_index == 0:
                    # Empty list.
                    self.__radio_list = None
                else:
                    self.__radio_index -= 1
            return True

    def _exec_volume(self):
        self._current_dialog = VolumeDialogBox(_('volume'), _("&value"), self.__save_the_new_volume, channel='radio')

    def __save_the_new_volume(self, volume):
        # Save the new Volume in settings.
        Volume().set_volume(volume, channel='radio')
        Settings().save()
        # Alert internal about settings change.
        headphone = Gpio().is_head_phone()
        if headphone:
            key = 'volume_headphone'
        else:
            key = 'volume_hp'
        self._put_in_function_queue(FunctionId.FUNCTION_SETTINGS_CHANGE, **{'section':'radio', 'key':key})

    # --------------------
    # Quick search function.
    def __quick_search_move_call_back(self, text_to_find) -> bool:
        log.info(f"{text_to_find=}")
        text_to_find = text_to_find.lower()
        if self.__radio_list:
            # Search from self.__focused_file_index to end of list
            for index, radio in enumerate(self.__radio_list):
                # log.info("file={} index={}".format(radio, index))
                if radio.lower().find(text_to_find) == 0 and index > self.__radio_index:
                    # Focus the wanted item
                    self.__radio_index = index
                    # Refresh the braille display
                    self.set_data_line()
                    return True
            # Search from 0 to self.__focused_file_index in the list
            for index, radio in enumerate(self.__radio_list):
                # log.info("file={} index={}".format(radio, index))
                if radio.lower().find(text_to_find) == 0 and index < self.__radio_index:
                    # Focus the wanted item
                    self.__radio_index = index
                    # Refresh the braille display
                    self.set_data_line()
                    return True
        return False

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        line = _("empty list...")
        if self.__radio_list:
            if self.__radio_index >= len(self.__radio_list):
                # If index overflow, set it to 0.
                self.__radio_index = 0
            line = self.__radio_list[self.__radio_index]
            log.info(f"{line=}")
        braille_static = BnoteApp.lou.to_dots_8(line)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)




