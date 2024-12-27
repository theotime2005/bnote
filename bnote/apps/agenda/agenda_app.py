"""
 bnote project
 Author : Theotime Berthod
 Date : 2024-11-17
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import datetime
from bnote.apps.agenda.agenda import *
from bnote.apps.bnote_app import BnoteApp, FunctionId
from bnote.apps.fman.file_manager import FileManager

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, AGENDA_APP_LOG
import bnote.ui as ui
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from bnote.tools.quick_search import QuickSearch

log = ColoredLogger(__name__)
log.setLevel(AGENDA_APP_LOG)


class AgendaApp(BnoteApp):
    """
    Agenda application
    """

    def __init__(self, put_in_function_queue):
        """
        Class construtor
        :param put_in_function_queue:  (for multi-threading) queue of functions ask to bnote Internal class
        """
        # app information
        self.version = "2024-11-17"
        # Filter creation
        self.dater = ""
        self.filter = False
        self.lst_treatment = []
        self.lst_filter = []
        self.lst = []
        self.index = 0
        # dictionarry for done and not done
        self.todo_dic = {
            "0": _("not done"),
            "1": _("done"),
        }
        # Call base class.
        super(AgendaApp, self).__init__(put_in_function_queue)
        # menu creation.
        self._menu = self.__create_menu()
        self.refresh_document()
        # Quick search function
        self.__quick_search = QuickSearch(self.__quick_search_move_call_back)
        # Settings application
        if (
            Settings().data["agenda"]["default_presentation"] != "standard"
            and Settings().data["agenda"]["default_presentation"] != "calendar"
        ):
            self.filter = Settings().data["agenda"]["default_presentation"]
        elif Settings().data["agenda"]["default_presentation"] == "calendar":
            self.dater = self.get_date()
            self.filter = "calendar"

    def __create_menu(self):
        return ui.UiMenuBar(
            name=_("agenda") + "-" + self.version,
            is_root=True,
            menu_item_list=[
                ui.UiMenuBar(
                    name=_("&event"),
                    action=self.event,
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&new"),
                            action=self._exec_add_event,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="N",
                        ),
                        ui.UiMenuItem(
                            name=_("&modify"), action=self._exec_modify_event
                        ),
                        ui.UiMenuItem(
                            name=_("&change status"),
                            action=self._exec_comute_todo,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="T",
                        ),
                        ui.UiMenuItem(
                            name=_("&delete"),
                            action=self._exec_delete_event,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                        ),
                        ui.UiMenuItem(
                            name=_("delete e&xpired events"),
                            action=self._exec_delete_event_expired,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_DELETE,
                        ),
                        ui.UiMenuItem(
                            name=_("delete &completed events"),
                            action=self._exec_delete_done,
                        ),
                    ],
                ),
                ui.UiMenuBar(
                    name=_("&goto"),
                    action=self.goto,
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&previous week"),
                            action=self._previous_week,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB,
                        ),
                        ui.UiMenuItem(
                            name=_("&next week"),
                            action=self._next_week,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                            shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_TAB,
                        ),
                        ui.UiMenuItem(
                            name=_("previous d&ay"), action=self._previous_day
                        ),
                        ui.UiMenuItem(name=_("next &day"), action=self._next_day),
                    ],
                ),
                ui.UiMenuBar(
                    name=_("fi&nd"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("find &date"),
                            action=self._exec_find_date,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="D",
                        ),
                        ui.UiMenuItem(
                            name=_("find in a&genda"),
                            action=self._exec_find_event,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="F",
                        ),
                    ],
                ),
                ui.UiMenuBar(
                    name=_("agenda &gestion"),
                    menu_item_list=[
                        ui.UiMenuItem(
                            name=_("&import agenda file"),
                            action=self._exec_import_agenda,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="I",
                        ),
                        ui.UiMenuItem(
                            name=_("&export agenda file"),
                            action=self._exec_export_agenda,
                            shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                            shortcut_key="E",
                        ),
                        ui.UiMenuItem(
                            name=_("e&mpty agenda"), action=self._exec_empty_agenda
                        ),
                    ],
                ),
                ui.UiMenuItem(
                    name=_("a&bout"),
                    action=self._exec_about,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1,
                ),
                ui.UiMenuItem(name=_("&applications"), action=self._exec_application),
            ],
        )

    def event(self):
        pass

    def goto(self):
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
        self.construct_list()
        self.hide_item()
        if self.filter == "not done date" or self.filter == "find element":
            self._menu.get_object(self._exec_add_event).hide()
            if not self.lst:
                self.restart_after_ask()
        else:
            self._menu.get_object(self._exec_add_event).unhide()
        if self.filter == "mode":
            self._menu.get_object(self.event).hide()
        else:
            self._menu.get_object(self.event).unhide()
        self.set_data_line()

    def construct_list(self):
        """ "
        Constructe the document to display
        Change form of list depended the value of display
        """
        if not edition.verify_file():
            self.alert_error()
            return False
        self.lst_treatment = edition.import_data()
        self.lst = []
        self.lst_filter = []
        if self.filter == False:
            self.standard_presentation()
        elif self.filter == "all":
            self._present_all()
        elif self.filter == "not_done":
            self._present_todo()
        elif self.filter == "today":
            self._present_today()
        elif self.filter == "date":
            self._present_find_date(self.dater)
        elif self.filter == "not done date":
            self._present_remember(self.dater)
        elif self.filter == "find element":
            self.find_dict[self.criter](self.find, self.todo)
        elif self.filter == "mode":
            self._select_mode()

    def alert_error(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_(
                "your agenda file is corrupt. You can copy the file in your document folder, but app can't open it. What do you want to do?"
            ),
            buttons=[
                ui.UiButton(name=_("&save and delete file"), action=self.error_agenda),
                ui.UiButton(name=_("&erase agenda"), action=self._exec_valid_empty),
            ],
            action_cancelable=self._exec_application,
        )

    def error_agenda(self):
        f = open("/home/pi/.bnote/my_agenda.csv", "r", encoding="utf-8")
        reader = f.read()
        f.close()
        f = open(
            "/home/pi/.bnote/bnote-documents/" + _("agenda saving") + ".csv",
            "w",
            encoding="utf-8",
        )
        f.write(reader)
        f.close()
        create_file()
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("the file has been correctly copy and the agenda has clear"),
            action=self._exec_cancel_dialog,
        )

    def hide_item(self):
        if self.lst and self.filter != "mode":
            self._menu.get_object(self.goto).unhide()
            self._menu.get_object(self._exec_comute_todo).unhide()
            self._menu.get_object(self._exec_modify_event).unhide()
            self._menu.get_object(self._exec_delete_event).unhide()
            self._menu.get_object(self._exec_delete_event_expired).unhide()
            self._menu.get_object(self._exec_delete_done).unhide()
        else:
            self._menu.get_object(self.goto).hide()
            self._menu.get_object(self._exec_comute_todo).hide()
            self._menu.get_object(self._exec_modify_event).hide()
            self._menu.get_object(self._exec_delete_event).hide()
            self._menu.get_object(self._exec_delete_event_expired).hide()
            self._menu.get_object(self._exec_delete_done).hide()
        if self.lst_treatment:
            self._menu.get_object(self._exec_export_agenda).unhide()
        else:
            self._menu.get_object(self._exec_export_agenda).hide()
        if (
            self.filter == "calendar"
            or self.filter == "today"
            or self.filter == "mode"
            or self.filter == "date"
        ):
            self._menu.get_object(self.goto).hide()
        else:
            self._menu.get_object(self.goto).unhide()
        return True

    def _exec_application(self):
        log.info("_exec_applications")
        self._put_in_function_queue(FunctionId.APPLICATIONS)

    def standard_presentation(self, number=False):
        """
        Present only event for today and events for after daies
        """
        value = 0
        for event in self.lst_treatment:
            if self.compare_date(event.date):
                if not number:
                    self.lst_filter.append(event)
                    self.lst.append(
                        self.get_name_day(event.date)
                        + " "
                        + self.todo_dic[event.todo]
                        + "-"
                        + event.subject
                        + ": "
                        + event.content
                    )
                else:
                    value += 1
        if number:
            if value >= 1:
                return value
            else:
                return ""

    def _present_all(self, number=False):
        """ "
        Constructe the list in chronologic order
        """
        log.info("_present_date")
        value = 0
        for event in self.lst_treatment:
            if not number:
                self.lst.append(
                    self.get_name_day(event.date)
                    + " "
                    + self.todo_dic[event.todo]
                    + "-"
                    + event.subject
                    + ": "
                    + event.content
                )
            else:
                value += 1
        if number:
            if value >= 1:
                return value
            else:
                return ""

    def _present_todo(self, number=False):
        """
        Constructe the list with only not done event
        Return self.lst with only event not done, Using the find function to use editions functions.
        """
        log.info("_exec_present_todo")
        value = 0
        for event in self.lst_treatment:
            if self.compare_date(event.date) and event.todo == "0":
                if not number:
                    self.lst_filter.append(event)
                    self.lst.append(
                        self.get_name_day(event.date)
                        + " "
                        + event.subject
                        + ": "
                        + event.content
                    )
                else:
                    value += 1
        if number:
            if value >= 1:
                return value
            else:
                return ""

    def _present_remember(self, date):
        for event in self.lst_treatment:
            if event.date == date and event.todo == "0":
                self.lst_filter.append(event)
                self.lst.append(event.subject + ": " + event.content)

    def _present_today(self, number=False):
        """
        Display only event for the currently day
        """
        log.info("_present_today")
        value = 0
        for event in self.lst_treatment:
            if event.date == self.get_date():
                if not number:
                    self.lst_filter.append(event)
                    self.lst.append(
                        self.todo_dic[event.todo]
                        + "-"
                        + event.subject
                        + ": "
                        + event.content
                    )
                else:
                    value += 1
        if len(self.lst_filter) > 0:
            return True
        elif number:
            if value >= 1:
                return value
            else:
                return ""

    def open_date(self):
        self.filter = "date"
        self._present_find_date(self.dater)
        self.refresh_document()

    def _present_find_date(self, date):
        """
        Filter events with date entered in argument
        """
        log.info("_present_find_date")
        for event in self.lst_treatment:
            if event.date == date:
                self.lst_filter.append(event)
                self.lst.append(
                    self.todo_dic[event.todo]
                    + ": "
                    + event.subject
                    + "-"
                    + event.content
                )
        if len(self.lst_filter) > 0:
            return True

    def _select_mode(self):
        self.lst = [
            _("from today's ({})").format(self.standard_presentation(True)),
            _("for today ({})").format(self._present_today(True)),
            _("not done ({})").format(self._present_todo(True)),
            _("all agenda ({})").format(self._present_all(True)),
            _("calendar {}").format(self.get_name_day(self.get_date(), complete=True)),
        ]
        return True

    def open_mode(self):
        mode_dict = {
            0: self._exec_standard_display,
            1: self._exec_today,
            2: self._exec_display_not_done,
            3: self._exec_show_all,
            4: self._exec_show_calendar,
        }
        mode_dict[self.index]()
        self.refresh_document()
        return True

    # ---------------
    # Menu functions.

    def _exec_add_event(self, date="", subject="", content=""):
        log.info("add event")
        # On s'occupe d'abord de la date
        if date:
            date = date.split("/")
            date = [
                date[2],
                date[1],
                date[0],
            ]
        elif self.filter == "calendar" or self.filter == "date":
            date_converter = self.dater.split("/")
            date = [date_converter[2], date_converter[1], date_converter[0]]
        else:
            date = self.get_next_day()
        # On s'occupe du sujet et du contenu impossible d'utiliser le _("") dans la définition de fonction
        if not subject:
            subject = _("title of event")
        if not content:
            content = _("content of event")
        self._current_dialog = ui.UiDialogBox(
            name=_("new event"),
            item_list=[
                # Dialog for date[
                ui.UiEditBox(name=_("&day"), value=("day", date[2])),
                ui.UiEditBox(name=_("&month"), value=("month", date[1])),
                ui.UiEditBox(name=_("&year"), value=("year", date[0])),
                # Treatment of others
                ui.UiEditBox(name=_("&subject"), value=("subject", subject)),
                ui.UiEditBox(name=_("co&ntent"), value=("content", content)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_add_event),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_delete_event(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to delete this event of your agenda?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_delete),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_comute_todo(self):
        index = self._use_filter("index")
        edition.comute_todo(index)

    def _exec_modify_event(self, date="", subject="", content="", todo=""):
        if not self.lst:
            return False
        log.info("modify event")
        index = self._use_filter(("index"))
        event = self.lst_treatment[index]
        # Convert value of todo in bool only if is not a repeat of function
        if not todo:
            if event.todo == "0":
                todo = False
            else:
                todo = True
        # Get event informations only if is not repeat
        if not date:
            date = event.date.split("/")
        else:
            date = date.split("/")
        if not subject:
            subject = event.subject
        if not content:
            content = event.content
        self._current_dialog = ui.UiDialogBox(
            name=_("modify event"),
            item_list=[
                ui.UiEditBox(name=_("&day"), value=("day", date[0])),
                ui.UiEditBox(name=_("&month"), value=("month", date[1])),
                ui.UiEditBox(name=_("&year"), value=("year", date[2])),
                ui.UiEditBox(name=_("&subject"), value=("subject", subject)),
                ui.UiEditBox(name=_("co&ntent"), value=("content", content)),
                ui.UiCheckBox(name=_("&is done"), value=("todo", todo)),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_modification),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_delete_event_expired(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to erase these events?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_delete_expired),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_delete_done(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("do you really want to delete the done events?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_delete_done),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_standard_display(self):
        self.index = 0
        self.filter = False
        self.refresh_document()

    def _exec_show_all(self):
        self.index = 0
        self.filter = "all"
        self.refresh_document()

    def _exec_display_not_done(self):
        self.index = 0
        self.filter = "not_done"
        self.refresh_document()

    def _exec_today(self):
        self.index = 0
        self.filter = "today"
        self.refresh_document()

    def _exec_find_date(self, day="", month="", year=""):
        self._current_dialog = ui.UiDialogBox(
            name=_("find date"),
            item_list=[
                ui.UiEditBox(name=_("&day"), value=("day", day)),
                ui.UiEditBox(name=_("&month"), value=("month", month)),
                ui.UiEditBox(name=_("&year"), value=("year", year)),
                ui.UiButton(name=_("fi&nd"), action=self._exec_valid_find_date),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_find_event(self, txt="", criter_index=0, only_not_done=False):
        self._current_dialog = ui.UiDialogBox(
            name=_("find"),
            item_list=[
                ui.UiEditBox(
                    name=_("&element to find"), value=("string character", txt)
                ),
                ui.UiListBox(
                    name=_("cri&terion"),
                    value=("criter", [_("all"), _("subject"), _("content")]),
                    current_index=criter_index,
                ),
                ui.UiCheckBox(name=_("&not done"), value=("filter", only_not_done)),
                ui.UiButton(name=_("fi&nd"), action=self._exec_valid_find_element),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_show_calendar(self):
        if self.filter != "date":
            self.dater = self.get_date()
        self.filter = "calendar"
        self.refresh_document()

    def _exec_goto_select_mode(self):
        if self.filter == "not done date":
            return False
        filter = self.filter
        filter_dict = {
            False: 0,
            "today": 1,
            "not_done": 2,
            "all": 3,
            "calendar": 4,
        }
        if self.filter == "find element":
            self.index = 0
        else:
            self.index = filter_dict[filter]
        self.filter = "mode"
        self.refresh_document()

    def _exec_import_agenda(self, path=FileManager.get_root_path()):
        list_item = [
            ui.UiFileBox(root=path, suffix_filter=(".csv")),
            ui.UiButton(name=_("&import"), action=self._exec_valid_import_file),
        ]
        if path == FileManager.get_root_path():
            list_item += [
                ui.UiButton(
                    name=_("usb &key"),
                    action=self._exec_import_agenda,
                    action_param={"path": FileManager.get_usb_flash_drive_path()},
                ),
            ]
        else:
            list_item += [
                ui.UiButton(name=_("my &documents"), action=self._exec_import_agenda),
            ]
        list_item += [
            ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
        ]
        self._current_dialog = ui.UiDialogBox(
            name=_("import agenda"),
            item_list=list_item,
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_export_agenda(self, name="", path=None):
        if path == True:
            path = self._current_dialog.get_values()["file"]
        if not name:
            d = self.get_date().split("/")
            d = "{} {} {}".format(d[2], d[1], d[0])
            name = _("My agenda {}").format(d)
        if not path:
            index_path = 0
        else:
            index_path = 1
        self._current_dialog = ui.UiDialogBox(
            name=_("export agenda"),
            item_list=[
                ui.UiFileEditBox(name=_("&file name"), value=("name", name)),
                ui.UiListBox(
                    name=_("file &location"),
                    value=("location", [_("my documents"), _("choose folder")]),
                    current_index=index_path,
                ),
                ui.UiButton(
                    name=_("&next"),
                    action=self._exec_export_next,
                    action_param={"path": path, "first": False},
                ),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_export_next(self, name="", path=None, first=True):
        if not name:
            kwargs = self._current_dialog.get_values()
            name = kwargs["name"]
        if not first and kwargs["location"] == _("my documents"):
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_(
                    "the file will be exported to the my documents folder. Do you want to continue?"
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&yes"),
                        action=self._exec_valid_export,
                        action_param={
                            "name": name,
                            "path": FileManager.get_root_path(),
                        },
                    ),
                    ui.UiButton(
                        name=_("&no"),
                        action=self._exec_export_agenda,
                        action_param={"name": name},
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return True
        if not path:
            path = FileManager.get_root_path()
        lst = [
            ui.UiFileBox(root=path, suffix_filter=""),
            ui.UiButton(
                name=_("&export"),
                action=self._exec_valid_export,
                action_param={"name": name},
            ),
            ui.UiButton(
                name=_("&back"),
                action=self._exec_export_agenda,
                action_param={"name": name, "path": True},
            ),
            ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
        ]
        if path == FileManager.get_root_path():
            lst += [
                ui.UiButton(
                    name=_("usb &key"),
                    action=self._exec_export_next,
                    action_param={
                        "name": name,
                        "path": FileManager.get_usb_flash_drive_path(),
                    },
                ),
            ]
        elif path == FileManager.get_usb_flash_drive_path():
            lst += [
                ui.UiButton(
                    name=_("my &documents"),
                    action=self._exec_export_next,
                    action_param={"name": name, "path": FileManager.get_root_path()},
                ),
            ]
        else:
            lst += [
                ui.UiButton(
                    name=_("my &documents"),
                    action=self._exec_export_next,
                    action_param={"name": name, "path": FileManager.get_root_path()},
                ),
                ui.UiButton(
                    name=_("usb &key"),
                    action=self._exec_export_next,
                    action_param={
                        "name": name,
                        "path": FileManager.get_usb_flash_drive_path(),
                    },
                ),
            ]
        self._current_dialog = ui.UiDialogBox(
            name=_("select a destination folder"),
            item_list=lst,
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_empty_agenda(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("warning"),
            message=_("are you sure you want to delete all content of the agenda?"),
            buttons=[
                ui.UiButton(name=_("&yes"), action=self._exec_valid_empty),
                ui.UiButton(name=_("&no"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("about agenda"),
            message=_(
                "agenda, version {}, copyright (C){} Theotime Berthod.\nIn collaboration with Eurobraille.\nFor suggestions or problems, contact Eurobraille or directly the application developer to {}."
            ).format(
                self.version, datetime.datetime.now().year, "acres.louer.0l@icloud.com"
            ),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )
        return True

    # --------------------
    # Dialogbox functions.

    def _exec_valid_add_event(self):
        kwargs = self._current_dialog.get_values()
        # composition of date
        date_compose = kwargs["day"] + "/" + kwargs["month"] + "/" + kwargs["year"]
        test = self.test_date(date_compose)
        if test != True:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=test,
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_add_event,
                        action_param={
                            "date": date_compose,
                            "subject": kwargs["subject"],
                            "content": kwargs["content"],
                        },
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return False
        elif ";" in kwargs["subject"] or ";" in kwargs["content"]:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("you can't use the ';' in text"),
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_add_event,
                        action_param={
                            "date": date_compose,
                            "subject": kwargs["subject"],
                            "content": kwargs["content"],
                        },
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return False
        return edition.add_element(date_compose, kwargs["subject"], kwargs["content"])

    def _exec_valid_delete(self):
        log.warning("delete event")
        index = self._use_filter("index")
        edition.delete_element(index)

    def _exec_valid_empty(self):
        log.warning("erasing file")
        if create_file() == True:
            text = _("the agenda has been correctly deleted.")
            self.restart_after_ask()
            log.info("success file created")
        else:
            text = _("unable to delete the file, an unexpected error occurred.")
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=text,
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_valid_modification(self):
        kwargs = self._current_dialog.get_values()
        date_compose = kwargs["day"] + "/" + kwargs["month"] + "/" + kwargs["year"]
        test = self.test_date(date_compose)
        if test != True:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=test,
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_modify_event,
                        action_param={
                            "date": date_compose,
                            "subject": kwargs["subject"],
                            "content": kwargs["content"],
                            "todo": kwargs["todo"],
                        },
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return False
        elif ";" in kwargs["subject"] or ";" in kwargs["content"]:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("you can't use the ';' in text"),
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_add_event,
                        action_param={
                            "date": date_compose,
                            "subject": kwargs["subject"],
                            "content": kwargs["content"],
                            "todo": kwargs["todo"],
                        },
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        if kwargs["todo"] == True:
            todo = "1"
        else:
            todo = "0"
        index = self._use_filter("index")
        return edition.modify_element(
            index, date_compose, kwargs["subject"], kwargs["content"], todo
        )

    def _exec_valid_delete_expired(self):
        lst = edition.import_data()
        if not self.compare_date(lst[0].date):
            edition.delete_element(0)
            return self._exec_valid_delete_expired()
        return False

    def _exec_valid_delete_done(self):
        lst = edition.import_data()
        for i in range(len(lst)):
            if lst[i].todo == "1":
                edition.delete_element(i)
                return self._exec_valid_delete_done()
        return False

    def _exec_valid_find_date(self):
        kwargs = self._current_dialog.get_values()
        date_compose = kwargs["day"] + "/" + kwargs["month"] + "/" + kwargs["year"]
        test = self.test_date(date_compose)
        if test != True:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=test,
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_find_date,
                        action_param={
                            "day": kwargs["day"],
                            "month": kwargs["month"],
                            "year": kwargs["year"],
                        },
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return False
        if date_compose[1] == "/":
            date_compose = "0" + date_compose
        if date_compose[4] == "/":
            date_compose = date_compose[:3] + "0" + date_compose[3:]
        self.dater = date_compose
        self.filter = "calendar"

    def _exec_valid_find_element(self):
        kwargs = self._current_dialog.get_values()
        # dico pour le rappel de la boîte de dialogue
        dico_number = {
            _("all"): 0,
            _("subject"): 1,
            _("content"): 2,
        }
        self.find_dict = {
            _("all"): self.find_element,
            _("subject"): self.find_subject,
            _("content"): self.find_content,
        }
        self.find = kwargs["string character"]
        self.criter = kwargs["criter"]
        self.todo = kwargs["filter"]
        test = self.find_dict[self.criter](self.find, self.todo)
        if test:
            if test == 1:
                number = _("1 event found")
            else:
                number = _("{} events found").format(test)
            self._current_dialog = ui.UiInfoDialogBox(
                message=number, action=self._exec_cancel_dialog
            )
            self.filter = "find element"
            self.index = 0
            return True
        self._current_dialog = ui.UiInfoDialogBox(
            message=_("no event found"),
            action=self._exec_find_event,
            action_param={
                "txt": kwargs["string character"],
                "criter_index": dico_number[kwargs["criter"]],
                "only_not_done": kwargs["filter"],
            },
        )
        return False

    def _exec_valid_import_file(self):
        log.warning("importing file")
        kwargs = self._current_dialog.get_values()
        self._current_dialog = ui.UiInfoDialogBox(message=_("importing..."))
        file = kwargs["file"]
        if file.is_file():
            importer = edition.import_other_file(file)
            if importer == False:
                text_name = _("warning")
                text = _(
                    "the file {} does not comply with the application's convention. Refer to the documentation for more information."
                ).format(file)
                log.error("file not imported")
                self._current_dialog = ui.UiMessageDialogBox(
                    name=text_name,
                    message=text,
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )
                return False
            elif type(importer) == int:
                text_name = _("information")
                if importer == 1:
                    text = _(
                        "the file was correctly imported, with the exception of 1 event that already existed."
                    )
                else:
                    text = _(
                        "the file was correctly imported, with the exception of {} events that already existed."
                    ).format(importer)
            else:
                text_name = _("information")
                text = _("the file has been correctly imported")
            log.info("file imported")
            self._current_dialog = ui.UiMessageDialogBox(
                name=text_name,
                message=text,
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        return True

    def _exec_valid_export(self, name, path=None):
        if not path:
            kwargs = self._current_dialog.get_values()
            path = kwargs["file"]
            if not path:
                self._current_dialog = ui.UiInfoDialogBox(
                    message=_("select folder"),
                    action=self._exec_export_agenda,
                    action_param={"name": name},
                )
                return
        exporter = edition.export_file(name, path)
        if exporter == True:
            log.info("success file exported")
            self._current_dialog = ui.UiInfoDialogBox(
                message=_("the file has been correctly exported in {} folder").format(
                    path
                ),
                action=self._exec_cancel_dialog,
            )
        elif exporter == "exist":
            log.error("file exsists")
            if path == FileManager.get_root_path():
                path = None
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("warning"),
                message=_(
                    "this file already exists, try with another name or delete the previous file"
                ),
                buttons=[
                    ui.UiButton(
                        name=_("&ok"),
                        action=self._exec_export_agenda,
                        action_param={"name": name, "path": path},
                    ),
                    ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
        else:
            log.error("file not exported")
            self._current_dialog = ui.UiInfoDialogBox(
                name=_("warning"),
                message=_(
                    "error during the exportation, verify your agenda and try again"
                ),
                action=self._exec_cancel_dialog,
            )

    def ask_event_same_day(self):
        self.lst_filter = []
        if self._present_today() == True:
            value = 0
            for idx in range(len(self.lst_filter)):
                if self.lst_filter[idx].todo == "0":
                    value += 1
            if value > 0:
                if value == 1:
                    number = _("you have 1 event not done for today.")
                elif value > 1:
                    number = _("you have {} events not done for today.").format(value)
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("information"),
                    message=number,
                    buttons=[
                        ui.UiButton(name=_("&display"), action=self.display_same_day),
                        ui.UiButton(name=_("&close"), action=self.close_after_same_day),
                    ],
                    action_cancelable=self.close_after_same_day,
                )
                return value
        return False

    def display_same_day(self):
        self.dater = self.get_date()
        self.filter = "not done date"

    def close_after_same_day(self):
        if (
            Settings().data["agenda"]["remember"] == "tomorrow"
            or Settings().data["agenda"]["remember"] == "same_tomorrow"
        ):
            if self.ask_event_next_day():
                return self.ask_event_next_day()
        self._exec_application()
        return self._put_in_function_queue(FunctionId.FUNCTION_RESTOR_AFTER_AGENDA)

    def ask_event_next_day(self):
        self.lst_filter = []
        if self._present_find_date(self.get_date(datetime.timedelta(days=1))):
            value = 0
            for idx in range(len(self.lst_filter)):
                if self.lst_filter[idx].todo == "0":
                    value += 1
            if value > 0:
                if value == 1:
                    number = _("you have 1 event not done for tomorrow.")
                elif value > 1:
                    number = _("you have {} events not done for tomorrow.").format(
                        value
                    )
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("warning"),
                    message=number,
                    buttons=[
                        ui.UiButton(name=_("&display"), action=self.display_next_day),
                        ui.UiButton(name=_("&close"), action=self.close_after_next_day),
                    ],
                    action_cancelable=self.close_after_next_day,
                )
                return True
        return False

    def close_after_next_day(self):
        self._exec_application()
        return self._put_in_function_queue(FunctionId.FUNCTION_RESTOR_AFTER_AGENDA)

    def display_next_day(self):
        self.dater = self.get_date(datetime.timedelta(days=1))
        self.filter = "not done date"

    # ---------------
    # Filter functions

    def _use_filter(self, type):
        """
        return lst corresponding to filter
        """
        if self.filter != "all":
            log.info("activate filter")
            lst_new = self.lst_filter
            index_new = self.find_test(self.lst_treatment, self.lst_filter[self.index])
        elif self.filter == "all":
            log.info("filter off")
            lst_new = self.lst_treatment
            index_new = self.index
        if type == "list":
            return lst_new
        else:
            return index_new

    def find_test(self, lst, cible):
        for idx in range(len(lst)):
            if lst[idx] == cible:
                return idx
        return False

    def compare_date(self, date) -> bool:
        """
        Compare the date with the current date.
        Return True if the given date is superior or equal to the current date, False otherwise.
        """
        # Obtenir la date actuelle et la date fournie sous forme de listes [jour, mois, année]
        current_date = list(map(int, self.get_date().split("/")))
        given_date = list(map(int, date.split("/")))

        # Comparaison des dates (année, puis mois, puis jour)
        if given_date[2] > current_date[2]:
            return True
        elif given_date[2] == current_date[2]:
            if given_date[1] > current_date[1]:
                return True
            elif given_date[1] == current_date[1]:
                if given_date[0] >= current_date[0]:
                    return True
        return False

    def test_date(self, date_teste):
        if date_teste[0] == "/":
            text = _("a date is composed of a day, a month and a year.")
            return text
        elif "//" in date_teste:
            text = _("a date is composed of a day, a month and a year.")
            return text
        elif date_teste[-1] == "/":
            text = _("a date is composed of a day, a month and a year.")
            return text
        date = edition.verify_date(date_teste)
        if date != True:
            if date == "invalid characters" or date == "invalid length":
                text = _("a date is composed of numbers, seperate with /")
            elif date == "invalid day":
                text = _("the days range from 01 to 31.")
            elif date == "invalid month":
                text = _("12 months ago, numbered from 01 to 12.")
            return text
        return True

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
        done = super(AgendaApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
        if not done:
            # command treatment for document.
            command_switcher = {
                Keyboard.KeyId.KEY_START_DOC: self._first_event,
                Keyboard.KeyId.KEY_END_DOC: self._last_event,
                Keyboard.KeyId.KEY_BACKWARD: self.display_filter,
            }
            if self.filter != "calendar":
                command_switcher[Keyboard.KeyId.KEY_CARET_UP] = self._previous_event
                command_switcher[Keyboard.KeyId.KEY_CARET_DOWN] = self._next_event
                if self.filter != "mode":
                    command_switcher[Keyboard.KeyId.KEY_CARET_LEFT] = self._previous_day
                    command_switcher[Keyboard.KeyId.KEY_CARET_RIGHT] = self._next_day
            else:
                command_switcher[Keyboard.KeyId.KEY_CARET_UP] = (
                    self.past_to_previous_day
                )
                command_switcher[Keyboard.KeyId.KEY_CARET_DOWN] = self.past_to_next_day
                command_switcher[Keyboard.KeyId.KEY_CARET_LEFT] = (
                    self.past_to_previous_week
                )
                command_switcher[Keyboard.KeyId.KEY_CARET_RIGHT] = (
                    self.past_to_next_week
                )
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
        done = super(AgendaApp, self).input_character(modifier, character, data)
        if not done:
            # Document input character treatment.
            if self.filter != "calendar":
                self.__quick_search.do_quick_search(character)

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if command treated, otherwise False
        """
        bramigraph_switcher = {
            Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self._first_event,
            Keyboard.BrailleFunction.BRAMIGRAPH_END: self._last_event,
            Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: self.restart_after_ask,
        }
        if self.filter != "calendar":
            if self.filter != "date":
                bramigraph_switcher[
                    Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE
                ] = self._exec_goto_select_mode
            else:
                bramigraph_switcher[
                    Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE
                ] = self._exec_show_calendar
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN] = (
                self._exec_modify_event
            )
            if self.filter != "mode":
                bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_LEFT] = (
                    self._previous_day
                )
                bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT] = (
                    self._next_day
                )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_UP] = (
                self._previous_event
            )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_DOWN] = (
                self._next_event
            )
        else:
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN] = (
                self.open_date
            )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_UP] = (
                self.past_to_previous_day
            )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_DOWN] = (
                self.past_to_next_day
            )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_LEFT] = (
                self.past_to_previous_week
            )
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT] = (
                self.past_to_next_week
            )
            bramigraph_switcher[
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE
            ] = self._exec_goto_select_mode
        if self.filter == "mode":
            bramigraph_switcher[Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN] = (
                self.open_mode
            )
            bramigraph_switcher[
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE
            ] = False
        done = super(AgendaApp, self).input_bramigraph(modifier, bramigraph)
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
        done = super(AgendaApp, self).input_interactive(modifier, position, key_type)
        if not done:
            # interactive key treatment
            if self.filter == "calendar":
                self.open_date()
            elif self.filter == "mode":
                self.open_mode()
            else:
                self._exec_modify_event()
            done = True
        return done

    def input_function(self, *args, **kwargs) -> bool:
        """
        Call when function is not treated by base class of this class.
        :param args[0]: The function id
        :param kwargs:
        :return: True if function treated.
        """
        function_id = args[0]
        # Here treat the specific FunctionId added by this application.
        if function_id == FunctionId.FUNCTION_AGENDA_SAME_DAY:
            return self.ask_event_same_day()
        elif function_id == FunctionId.FUNCTION_AGENDA_NEXT_DAY:
            return self.ask_event_next_day()
        # else call base class decoding.
        else:
            return super(AgendaApp, self).input_function(*args, **kwargs)

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        # log.info("Timer event")
        self.get_date()

    # --------------------
    # Date event functions.

    def get_date(self, day_value=datetime.timedelta(days=0)):
        """
        Get date and constructe.
        """
        now = str(datetime.datetime.now() + day_value)
        now = now.split(" ")
        now = now[0]
        now = now.split("-")
        date = now[2] + "/" + now[1] + "/" + now[0]
        return date

    def get_next_day(self):
        """
        Get date of next day
        Return: date of next day
        """
        date = str(datetime.datetime.today() + datetime.timedelta(days=1))
        date = date.split(" ")
        date = date[0].split("-")
        return date

    def get_name_day(self, date, complete=False):
        date_found = date.split("/")
        date_name = datetime.datetime(
            int(date_found[2]), int(date_found[1]), int(date_found[0])
        ).weekday()
        name_day_dict = {
            0: _("monday"),
            1: _("tuesday"),
            2: _("wednesday"),
            3: _("thursday"),
            4: _("friday"),
            5: _("saturday"),
            6: _("sunday"),
        }
        month_dict = {
            "01": _("january"),
            "02": _("february"),
            "03": _("march"),
            "04": _("april"),
            "05": _("may"),
            "06": _("june"),
            "07": _("july"),
            "08": _("august"),
            "09": _("september"),
            "10": _("october"),
            "11": _("november"),
            "12": _("december"),
        }
        if complete == True:
            return (
                name_day_dict[date_name]
                + " "
                + date_found[0]
                + " "
                + month_dict[date_found[1]]
                + " "
                + date_found[2]
            )
        return name_day_dict[date_name] + " " + date

    def get_number_week(self, date):
        date = date.split("/")
        number = (
            datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            .isocalendar()
            .week
        )
        return number

    def _next_event(self):
        if self.index < len(self.lst) - 1:
            self.index += 1
            return True

    def _previous_event(self):
        if self.index > 0:
            self.index -= 1
            return True

    def _first_event(self):
        if self.index != 0:
            self.index = 0
            return True
        elif self.filter == "calendar":
            self.dater = self.get_date()
            return True

    def _last_event(self):
        if self.filter == "calendar":
            self.dater = self.get_date()
            return True
        if self.index == len(self.lst) - 1:
            return False
        else:
            self.index = len(self.lst) - 1
            return True

    def _next_week(self):
        if (
            self.index == len(self.lst)
            or self.filter == "today"
            or self.filter == "calendar"
        ):
            return False
        lst = self._use_filter("list")
        start = self.get_number_week(lst[self.index].date)
        for idx in range(self.index, len(lst)):
            test = self.get_number_week(lst[idx].date)
            if test != start:
                self.index = idx
                return True

    def _previous_week(self):
        if (
            self.index == len(self.lst)
            or self.filter == "today"
            or self.filter == "calendar"
        ):
            return False
        lst = self._use_filter("list")
        value = self.index - 1
        start = self.get_number_week(lst[self.index].date)
        for idx in range(0, self.index):
            test = self.get_number_week(lst[value].date)
            if test != start:
                if value == 0 or self.get_number_week(lst[value - 1].date) != test:
                    self.index = value
                    return True
                second = self.get_number_week(lst[value].date)
                for j in range(0, value):
                    if self.get_number_week(lst[j].date) == second:
                        self.index = j
                        return True
            value -= 1

    def _next_day(self):
        if (
            self.index == len(self.lst)
            or self.filter == "today"
            or self.filter == "calendar"
        ):
            return False
        lst = self._use_filter("list")
        for idx in range(self.index, len(lst)):
            if lst[idx].date != lst[self.index].date:
                self.index = idx
                return True

    def _previous_day(self):
        if (
            self.index == len(self.lst)
            or self.filter == "today"
            or self.filter == "calendar"
        ):
            return False
        lst = self._use_filter("list")
        value = self.index - 1
        for idx in range(0, self.index):
            if lst[value].date != lst[self.index].date:
                self.index = value
                return True
            value -= 1

    def find_subject(self, text_to_find, todo=False):
        text_to_find = text_to_find.lower()
        value = 0
        for idx, element in enumerate(self.lst_treatment):
            if todo and element.todo == "1":
                if element.subject.lower().find(text_to_find) == 0:
                    value += 1
                    self.lst_filter.append(element)
                    self.lst.append(
                        self.get_name_day(element.date)
                        + " "
                        + self.todo_dic[element.todo]
                        + ": "
                        + element.subject
                        + "-"
                        + element.content
                    )
            elif element.subject.lower().find(text_to_find) == 0:
                value += 1
                self.lst_filter.append(element)
                self.lst.append(
                    self.get_name_day(element.date)
                    + " "
                    + self.todo_dic[element.todo]
                    + ": "
                    + element.subject
                    + "-"
                    + element.content
                )
        if value >= 1:
            return value
        return False

    def find_content(self, text_to_find, todo=False):
        text_to_find = text_to_find.lower()
        value = 0
        for idx, element in enumerate(self.lst_treatment):
            if todo and element.todo == "1":
                if element.content.lower().find(text_to_find) >= 0:
                    value += 1
                    self.lst_filter.append(element)
                    self.lst.append(
                        self.get_name_day(element.date)
                        + " "
                        + self.todo_dic[element.todo]
                        + ": "
                        + element.subject
                        + "-"
                        + element.content
                    )
            elif element.content.lower().find(text_to_find) >= 0:
                value += 1
                self.lst_filter.append(element)
                self.lst.append(
                    self.get_name_day(element.date)
                    + " "
                    + self.todo_dic[element.todo]
                    + ": "
                    + element.subject
                    + "-"
                    + element.content
                )
        if value >= 1:
            return value
        return False

    def find_element(self, text_to_find, todo=False):
        text_to_find = text_to_find.lower()
        value = 0
        for idx, element in enumerate(self.lst_treatment):
            if todo and element.todo == "1":
                if (
                    element.subject.lower().find(text_to_find) >= 0
                    or element.content.lower().find(text_to_find) >= 0
                ):
                    value += 1
                    self.lst_filter.append(element)
                    self.lst.append(
                        self.get_name_day(element.date)
                        + " "
                        + self.todo_dic[element.todo]
                        + ": "
                        + element.subject
                        + "-"
                        + element.content
                    )
            elif (
                element.subject.lower().find(text_to_find) >= 0
                or element.content.lower().find(text_to_find) >= 0
            ):
                value += 1
                self.lst_filter.append(element)
                self.lst.append(
                    self.get_name_day(element.date)
                    + " "
                    + self.todo_dic[element.todo]
                    + ": "
                    + element.subject
                    + "-"
                    + element.content
                )
        if value >= 1:
            return value
        return False

    def __quick_search_move_call_back(self, text_to_find):
        if not self.lst:
            return False
        text_to_find = text_to_find.lower()
        if self.filter == "mode":
            lst = self.lst
        else:
            lst = self._use_filter("list")
        # find between index and end of list
        for index, element in enumerate(lst):
            if self.filter == "mode":
                if element.lower().find(text_to_find) == 0 and index > self.index:
                    self.index = index
                    self.set_data_line()
                    return True
            else:
                if (
                    element.subject.lower().find(text_to_find) == 0
                    and index > self.index
                    or element.content.lower().find(text_to_find) == 0
                    and index > self.index
                ):
                    self.index = index
                    self.set_data_line()
                    return True
        # find between first element of list and element focused
        for index, element in enumerate(lst):
            if self.filter == "mode":
                if element.lower().find(text_to_find) == 0 and index < self.index:
                    self.index = index
                    self.set_data_line()
                    return True
            else:
                if (
                    element.subject.lower().find(text_to_find) == 0
                    and index < self.index
                    or element.content.lower().find(text_to_find) == 0
                    and index < self.index
                ):
                    self.index = index
                    self.set_data_line()
                    return True
        return False

    def past_to_next_day(self):
        """
        Change self.dater and give the value of next day
        """
        date = self.dater.split("/")
        date = str(
            datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            + datetime.timedelta(days=1)
        )
        date = date.split(" ")
        date = date[0]
        date = date.split("-")
        self.dater = date[2] + "/" + date[1] + "/" + date[0]
        return True

    def past_to_previous_day(self):
        """
        change self.dater to back day
        """
        date = self.dater.split("/")
        date = str(
            datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            - datetime.timedelta(days=1)
        )
        date = date.split(" ")
        date = date[0]
        date = date.split("-")
        self.dater = date[2] + "/" + date[1] + "/" + date[0]
        return True

    def past_to_next_week(self):
        """
        Change self.dater to next week
        """
        date = self.dater.split("/")
        date = str(
            datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            + datetime.timedelta(weeks=1)
        )
        date = date.split(" ")
        date = date[0]
        date = date.split("-")
        self.dater = date[2] + "/" + date[1] + "/" + date[0]
        return True

    def past_to_previous_week(self):
        """
        Change self.dater to back week
        """
        date = self.dater.split("/")
        date = str(
            datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            - datetime.timedelta(weeks=1)
        )
        date = date.split(" ")
        date = date[0]
        date = date.split("-")
        self.dater = date[2] + "/" + date[1] + "/" + date[0]
        return True

    def get_calendar(self):
        self.lst = []
        self.lst_filter = []
        display = self.get_name_day(self.dater, complete=True)
        if self.dater == self.get_date():
            display = _("today") + " " + display
        if self._present_find_date(self.dater) and self.lst_filter:
            display = " *" + display + " "
            if len(self.lst) == 1:
                display += _("1 event")
            else:
                display += _("{} events").format(len(self.lst))
            value = 0
            for i in self.lst_filter:
                if i.todo == "0":
                    value += 1
            if value > 0:
                display += " (" + _("{} not done").format(value) + ")"
        display += "."
        return display

    def restart_after_ask(self):
        """
        Only for specials situations
        """
        if self.filter == "not done date":
            log.info(("restarting apps"))
            self.__init__(self._put_in_function_queue)
            self.refresh_document()

    # --------------------
    # Document functions.
    def set_data_line(self, line=""):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if self.filter == "calendar":
            line = line + self.get_calendar()
        elif self.filter == "mode":
            line += _("Show") + " " + self.lst[self.index]
        else:
            if self.lst:
                if self.index <= len(self.lst) - 1:
                    line = line + self.lst[self.index]
                else:
                    self.index = len(self.lst) - 1
                    line = line + self.lst[self.index]
            else:
                line = line + _("no event...")
        braille_type = Settings().data["system"]["braille_type"]
        text, braille_static, pos = BnoteApp.lou.convert_to_braille(braille_type, line)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(line, braille_static, braille_blinking, 0)

    def display_filter(self):
        if self.filter == False:
            displayer = _("agenda")
        elif self.filter == "today":
            displayer = _("today")
        elif self.filter == "not_done":
            displayer = _("event not done")
        elif self.filter == "all":
            displayer = _("all")
        elif self.filter == "date":
            displayer = _("to do for {}").format(
                self.get_name_day(self.dater, complete=True)
            )
        elif self.filter == "not done date" and self.dater == self.get_date(
            datetime.timedelta(days=1)
        ):
            displayer = _("to do for tomorrow")
        elif self.filter == "not done date" and self.dater == self.get_date():
            displayer = _("to do for today")
        elif self.filter == "calendar":
            displayer = _("calendar")
        elif self.filter == "find element":
            displayer = _("find {}").format(self.find)
        elif self.filter == "mode":
            displayer = _("select the display")
        return self.set_data_line(displayer + ": ")
