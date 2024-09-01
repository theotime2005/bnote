"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import threading
import time
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.tools.keyboard import Keyboard
from bnote.tools.audio_player import AudioPlayer
import bnote.ui as ui
# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, TIMER_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(TIMER_APP_LOG)


class TimerApp(BnoteApp):
    """
    Timer application.
    """

    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # App information
        self.version = "1.1.6"
        # Call base class.
        super().__init__(put_in_function_queue)
        # menu creation.
        self._menu = self.__create_menu()
        # Marker point
        self.marker = {}
        # Timer indicator
        self.timer = None
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.centiseconds = 0
        self.mode = ""
        self.is_starting = False
        self.refresh_document()
        # Space number
        self.space = 0

    def __create_menu(self):
        # Instantiate menu (A menu bar with 1 sub menu of 2 menu items and one menu item).
        return ui.UiMenuBar(
            name=_("timer"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuItem(name=_("start/stop"), action=self.start_stop,
                              shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                              shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN),
                ui.UiMenuBar(
                    name=_("&marker"), action=self._exec_marker,
                    menu_item_list=[
                        ui.UiMenuItem(name=_("add &marker"), action=self._exec_add_marker,
                                      shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                                      shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE),
                        ui.UiMenuItem(name=_("&show markers"), action=self._exec_show_marker),
                    ]
                ),
                ui.UiMenuItem(name=_("&clear"), action=self._exec_clear,
                              shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                              shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE),
                ui.UiMenuItem(name=_("&launch timer"), action=self._exec_timer),
                ui.UiMenuItem(name=_("&about"), action=self._exec_about,
                              shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                              shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1),
            ],
        )

    def _exec_marker(self):
        return True

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
        if self.hours == 0 and self.minutes == 0 and self.seconds == 0 or self.mode != "chrono":
            self._menu.get_object(self._exec_marker).hide()
        else:
            self._menu.get_object(self._exec_marker).unhide()
        self.set_data_line()

    def rebuild_document(self):
        """
        Call when enter or re-enter in application.
        To overload by each apps if necessary.
        """
        self.refresh_document()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        self._update_menu_items()
        self.set_data_line()

    # ---------------
    # Menu functions.
    def _exec_add_marker(self, temps="", nom=""):
        if not temps:
            temps = "{}:{}:{}.{}".format(self.hours, self.minutes, self.seconds, self.centiseconds)
        self._current_dialog = ui.UiDialogBox(
            name=_("add marker point"),
            item_list=[
                ui.UiEditBox(name=_("&marker name"), value=("name", nom)),
                ui.UiButton(name=_("c&reate"), action=self._exec_valid_add_marker,
                            action_param={'temps': temps}),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_ask_replace(self, temps, nom):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("a marker already exists at this location, would you like to replace it?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_ask_replace,
                            action_param={'temps': temps, 'nom': nom}),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_show_marker(self):
        list_item = [
            ui.UiListBox(name=_("&marker list"), value=("marker", list(self.marker)), current_index=0),
        ]
        if self.marker:
            list_item += [
                ui.UiButton(name=_("show &name"), action=self._exec_show_text_marker),
                ui.UiButton(name=_("&rename"), action=self._exec_rename_marker),
                ui.UiButton(name=_("&delete"), action=self._exec_delete_marker),
            ]
        list_item += [
            ui.UiButton(name=_("&close"), action=self._exec_cancel_dialog),
        ]
        self._current_dialog = ui.UiDialogBox(
            name=_("marker list"),
            item_list=list_item,
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_rename_marker(self):
        kwargs = self._current_dialog.get_values()
        name = self.marker[kwargs['marker']]
        self._current_dialog = ui.UiDialogBox(
            name=_("rename marker"),
            item_list=[
                ui.UiEditBox(name=_("&marker name"), value=("marker", name)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_rename_marker,
                            action_param={'temps': kwargs['marker']}),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_clear(self):
        self.is_starting = False
        self.cancel_timer()
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.centiseconds = 0
        self.mode = ""
        self.marker = {}
        self.refresh_document()

    def _exec_timer(self):
        self.is_starting = False
        self._current_dialog = ui.UiDialogBox(
            name=_("create timer"),
            item_list=[
                ui.UiEditBox(name=_("&hours"), value=("hours", "0")),
                ui.UiEditBox(name=_("&minutes"), value=("minutes", "0")),
                ui.UiEditBox(name=_("&seconds"), value=("seconds", "0")),
                ui.UiButton(name=_("&start"), action=self._exec_valid_timer),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        # Display an information dialog box.
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("timer application, version {}, copyright (C)2023 Theotime Berthod.").format(self.version),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_time_rapidly(self):
        self._current_dialog = ui.UiInfoDialogBox(
            message="{}:{}:{}.{}".format(self.hours, self.minutes, self.seconds, self.centiseconds),
            action=self._exec_cancel_dialog)

    # --------------------
    # Dialogbox functions.
    def _exec_valid_add_marker(self, temps):
        kwargs = self._current_dialog.get_values()
        if self.marker.get(temps):
            return self._exec_ask_replace(temps, kwargs['name'])
        self.marker[temps] = kwargs['name']

    def _exec_valid_ask_replace(self, temps, nom):
        self.marker[temps] = nom

    def _exec_show_text_marker(self):
        kwargs = self._current_dialog.get_values()
        self._current_dialog = ui.UiInfoDialogBox(message=self.marker[kwargs['marker']], action=self._exec_show_marker)

    def _exec_delete_marker(self):
        kwargs = self._current_dialog.get_values()
        self.marker.pop(kwargs['marker'])
        self._exec_show_marker()

    def _exec_valid_rename_marker(self, temps):
        kwargs = self._current_dialog.get_values()
        self.marker[temps] = kwargs['marker']

    def _exec_valid_timer(self):
        kwargs = self._current_dialog.get_values()
        try:
            self.hours = int(kwargs['hours'])
            self.minutes = int(kwargs['minutes'])
            self.seconds = int(kwargs['seconds'])
        except ValueError:
            self._current_dialog = ui.UiInfoDialogBox(message=_("you must enter numerical values"),
                                                      action=self._exec_cancel_dialog)
            return
        if not self.hours and not self.minutes and not self.seconds:
            self._current_dialog = ui.UiInfoDialogBox(message=_("you cannot start the timer at 0."),
                                                      action=self._exec_cancel_dialog)
            return
        self.mode = "timer"
        self.is_starting = True
        self.start_timer()
        self.refresh_document()

    def _exec_end_timer(self):
        self._exec_clear()
        audio = AudioPlayer()
        audio.file_play("apps/timer/sound.mp3", 0)
        self._current_dialog = ui.UiInfoDialogBox(message=_("the time is elapsed!!!"), action=audio.stop)
        self._put_in_function_queue(FunctionId.FUNCTION_END_TIMER)

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
        done = super(TimerApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            # TODO to complete
            pass
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
        done = super(TimerApp, self).input_character(modifier, character, data)
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
        done = super(TimerApp, self).input_bramigraph(modifier, bramigraph)
        if not done:
            # braille function treatment for document.
            # TODO to complete
            pass
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
        done = super(TimerApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            position -= 1
            if position > self.space:
                self.start_stop()
            elif position < self.space and self.mode:
                self._exec_time_rapidly()
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
        done = super(TimerApp, self).input_function(*args, **kwargs)
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

    def start_stop(self):
        if self.mode == "timer":
            return False
        if not self.is_starting:
            self.is_starting = True
            if not self.mode:
                self.mode = "chrono"
            self.start_timer()
        else:
            self.cancel_timer()
            self.is_starting = False
        self.refresh_document()

    def __one_second_callback(self):
        if self.timer:
            self.start_timer()
        if self.is_starting:
            if self.mode == "chrono":
                self.add()
            elif self.mode == "timer":
                take_off = self.take_off()
                if not take_off:
                    self.is_starting = False
                    self.cancel_timer()
                    self._exec_end_timer()

    def start_timer(self):
        self.timer = threading.Timer(1 / 100, self.__one_second_callback)
        self.timer.start()

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def add(self):
        self.centiseconds += 1
        if self.centiseconds == 100:
            self.seconds += 1
            self.centiseconds = 0
        if self.seconds >= 60:
            self.minutes += 1
            self.seconds = 0
            self.centiseconds = 0
        if self.minutes >= 60:
            self.hours += 1
            self.minutes = 0
            self.seconds = 0
            self.centiseconds = 0
        self.refresh_document()

    def take_off(self):
        if self.seconds == 1 and self.minutes == 0 and self.hours == 0:
            self.seconds -= 1
            return False
        self.centiseconds -= 1
        if self.centiseconds == -1:
            self.centiseconds = 99
            self.seconds -= 1
        if self.seconds == -1:
            self.minutes -= 1
            self.seconds = 59
            self.centiseconds = 99
        if self.minutes == -1:
            self.hours -= 1
            self.minutes = 59
            self.seconds = 59
            self.centiseconds = 99
        self.refresh_document()
        return True

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if self.is_starting:
            line = _("{}:{}:{} started").format(self.hours, self.minutes, self.seconds)
        else:
            if self.hours == 0 and self.minutes == 0 and self.seconds == 0:
                line = _("{}:{}:{}.{} fixed").format(self.hours, self.minutes, self.seconds, self.centiseconds)
            else:
                line = _("{}:{}:{}.{} paused").format(self.hours, self.minutes, self.seconds, self.centiseconds)
        for i in range(len(line)):
            if line[i] == " ":
                self.space = i
                break
        braille_static = BnoteApp.lou.to_dots_8(line)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)
