"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import unicodedata

from bnote.apps.bnote_app import BnoteApp
from bnote.braille.braille_display import BrailleDisplay
from bnote.tools.keyboard import Keyboard
from .ui_object import UiObject

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiContainer(UiObject):
    """
    The user's interface container (a menu container, a dialog box)
    """

    CONTAINER_PARENT_SEPARATOR = ":"
    CONTAINER_CHILD_SEPARATOR = " "

    object_id = 1
    braille_display = BrailleDisplay()
    id_array_objects = []

    def __init__(self, **kwargs):
        # **kwargs treatment.
        super().__init__(**kwargs)
        self.ui_objects = []
        # add id to container object
        self.set_id(UiContainer.object_id)
        UiContainer.object_id += 1
        parameters = {
            "ui_objects": self.__set_objects,
            "focused_object": self.__set_focus_from_index,
        }
        for name, value in parameters.items():
            # log.info(f"{name=}, {value=}")
            if name in kwargs:
                value(kwargs[name])

        # Each root container has the same BrailleDisplay
        if self._is_root:
            self._update_braille_display()

    def __set_objects(self, ui_objects):
        self.ui_objects = ui_objects

        for ui_object in self.ui_objects:
            # Give an id to each child object.
            ui_object.set_id(UiContainer.object_id)
            UiContainer.object_id += 1
            # Give a parent to each object.
            ui_object.set_parent(self)

        # Put focus on first object.
        self.ui_objects[0].on_focus(with_speaking=False)

    def __set_focus_from_index(self, index):
        """
        Set the focus on one object.
        This function is used only during instantiation.
        :param index:
        :return:
        """
        for ui_index, ui_object in enumerate(self.ui_objects):
            if ui_index >= index:
                if not ui_object.is_hide():
                    self.set_focus(ui_object)
                    return
        if index > 0:
            # index corresponding to a hidden object and all next hidden are also hide
            # find one object from the first.
            self.__set_focus_from_index(0)
        else:
            raise ValueError("Empty container or container with all items hidden.")

    def set_focus(self, ui_object):
        ui_focused_object = self.get_focused_object()
        if ui_focused_object:
            if ui_focused_object != ui_object:
                ui_focused_object.on_focus_lost(with_speaking=False)
                ui_object.on_focus(with_speaking=False)
        else:
            ui_object.on_focus(with_speaking=False)

    def get_object_from_id(self, ui_id):
        for ui_object in self.ui_objects:
            if ui_object.get_id() == ui_id:
                return ui_object

    def get_object_from_action(self, action):
        for ui_object in self.ui_objects:
            if ui_object.get_action() == action:
                return ui_object

    def unhide_object_count(self) -> int:
        """
        Return the count of non hide object menu for a given container.
        (Do not recurse in sub container.)
        """
        count = 0
        for ui_object in self.ui_objects:
            if not ui_object.is_hide():
                count += 1
        return count

    def ask_update_braille_display(self):
        self._update_braille_display()

    def _update_braille_display(self):
        log.debug(f"_update_braille_display <{self._name}>")
        root_container = self.get_root()
        if root_container != self:
            root_container._update_braille_display()
        else:
            (
                text_objects,
                braille_objects,
                braille_blinking_objects,
                id_array_objects,
            ) = self.get_presentation()
            pos = self.__get_focused_object_pos_from_id(id_array_objects)
            UiContainer.id_array_objects = id_array_objects
            UiContainer.braille_display.set_data_line(
                text_objects, braille_objects, braille_blinking_objects, pos
            )

    """
    Return the display offset of focused object from id_array_object given by get_presentation.
    """

    def __get_focused_object_pos_from_id(self, id_array_objects):
        # DP FIXME optimize the research of focused object...
        focused_object_id = self.ui_objects[self._get_focused_object_index()].get_id()
        for index, id in enumerate(id_array_objects):
            if id == focused_object_id:
                focused_object = self.get_focused_object()
                index += focused_object.presentation_offset()
                return index
        return -1

    def _get_focused_object_index(self):
        for index, ui_object in enumerate(self.ui_objects):
            if ui_object.is_focused():
                return index
        return 0

    def get_focused_object(self):
        for ui_object in self.ui_objects:
            if ui_object.is_focused():
                return ui_object
        return None

    def _set_focused_object(self, ui_object):
        focused_index = self._get_focused_object_index()
        self.ui_objects[focused_index].on_focus_lost(with_speaking=False)
        ui_object.on_focus(with_speaking=False)

    def _set_focused_object_to_first(self):
        self.__set_focus_from_index(0)

    def get_data_line(self, force_refresh=False) -> (str, str, str):
        text_objects, braille_objects, braille_blinking_objects = (
            UiContainer.braille_display.get_data_line(force_refresh)
        )
        return text_objects, braille_objects, braille_blinking_objects

    def get_object(self, action):
        """
        Find ui_object assigned to one action.
        :param action: app function
        :return: ui_object or None
        """
        if self._action == action:
            return self
        for ui_object in self.ui_objects:
            if ui_object.get_action() == action:
                return ui_object
            elif isinstance(ui_object, UiContainer):
                child_object = ui_object.get_object(action)
                if child_object:
                    return child_object
        return None

    def rename_item(self, name, braille_type, action):
        ui_object = self.get_object(action)
        if ui_object:
            ui_object.set_braille_type(braille_type)
            ui_object.set_name(name)

    def reset_container(self):
        """
        Reset menubar, the root becomes the up-level container and focused object is the first child
        :return: None
        """
        root_container = self.get_root()
        if (root_container is not None) and (root_container != self):
            root_container.set_root(False)
        # Defines first parent container as root, focus its first object and update display.
        self.switch_to_root_of_root_menu()

    def get_root(self):
        parent = self
        grand_parent = self
        while parent:
            grand_parent = parent
            if parent.is_root():
                return parent
            parent = parent.get_parent()
        return grand_parent.__get_root_child()

    def __get_root_child(self):
        for child in self.ui_objects:
            if child.is_root():
                return child
            elif isinstance(child, UiContainer):
                root = child.__get_root_child()
                if root:
                    return root
        return None

    def get_presentation(self):
        """
        Construct presentation for an object
        :return: (text, braille static dots, braille blinking, dots list of id of braille length
        """
        text_objects, braille_objects, braille_blinking_objects, id_array_objects = (
            super().get_presentation()
        )
        if self._is_root:
            text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(
                self._braille_type, UiContainer.CONTAINER_PARENT_SEPARATOR
            )
            first_loop = True
            for ui_object in self.ui_objects:
                text_object, braille_object, braille_blinking, id_array_object = (
                    ui_object.get_presentation()
                )
                # text_object is None for hidden object.
                if text_object:
                    text_objects = text_separator.join([text_objects, text_object])
                    braille_objects = braille_separator.join(
                        [braille_objects, braille_object]
                    )
                    braille_blinking_objects = ("\u2800" * len(braille_separator)).join(
                        [braille_blinking_objects, braille_blinking]
                    )
                    id_array_objects = [
                        *id_array_objects,
                        *([0] * len(braille_separator)),
                        *id_array_object,
                    ]
                    if first_loop:
                        # First separator (parent:child) is different of next (child child...)
                        text_separator, braille_separator, pos = (
                            BnoteApp.lou.convert_to_braille(
                                self._braille_type,
                                UiContainer.CONTAINER_CHILD_SEPARATOR,
                            )
                        )
                        first_loop = False
        return text_objects, braille_objects, braille_blinking_objects, id_array_objects

    def input_alt_shortcut(self, character) -> bool:
        ui_object = self.get_shortcut_char_in_label(character)
        if ui_object:
            # Put main menu as root
            self.reset_container()
            # Find shortcut => set focus and execute action on this object.
            self._set_focused_object(ui_object)
            self._action_on_focused_object()
            return True
        return False

    def get_shortcut_char_in_label(self, character) -> UiObject:
        character = self._unaccented_text(character)
        for ui_object in self.ui_objects:
            if not ui_object.is_hide() and ui_object.shortcut == character:
                return ui_object
        return None

    def exec_menu_item_key(self, modifier, key):
        if isinstance(key, str):
            key = self._unaccented_text(key)
            # Remove Shift modifier to valid Ctrl+c or Ctrl+Shift+C
            if (
                modifier
                == Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT
                + Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
            ):
                modifier = Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL
        for ui_object in self.ui_objects:
            if not ui_object.is_hide():
                if isinstance(ui_object, UiContainer):
                    if ui_object.exec_menu_item_key(modifier, key):
                        return True
                elif ui_object.check_menu_item_key(modifier, key):
                    # Find shortcut => execute action on this object.
                    ui_object.exec_action()
                    return True
        return False

    def input_character(self, modifier, character, data) -> bool:
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier:
        :param character:
        :return: True if stay
        """
        root_container = self.get_root()
        if root_container is None:
            raise ValueError("No root container ?")
        else:
            treated, in_menu = self.get_focused_object().exec_character(
                modifier, character, data
            )
            if not treated:
                treated, in_menu = root_container.exec_character(
                    modifier, character, data
                )
        return in_menu

    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character and return (refresh, object_id).
        :param modifier:
        :param character:
        :return: (Treated, stay in menu)
        """
        treated, in_menu = False, True
        # Check shortcut key.
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_ALT:
            ui_object = self.get_shortcut_char_in_label(character)
            if ui_object:
                # Find shortcut => set focus and execute action on this object.
                self._set_focused_object(ui_object)
                treated, in_menu = self._action_on_focused_object(
                    Keyboard.BrailleModifier.BRAILLE_FLAG_NONE
                )
        return treated, in_menu

    def input_bramigraph(self, modifier, bramigraph) -> bool:
        """
        Do what needs to be done for this modifier and bramigraph.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param bramigraph: braille function (see Keyboard.BrailleFunction)
        :return: True if stay in menu
        """
        root_container = self.get_root()
        if root_container is None:
            raise ValueError("No root container ?")
        else:
            # Exec input_bramigraph on focused child.
            treated, in_menu = root_container.get_focused_object().exec_bramigraph(
                modifier, bramigraph
            )
            if not treated:
                treated, in_menu = root_container.exec_bramigraph(modifier, bramigraph)
        return in_menu

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this command key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        treated, in_menu = False, True
        if self == self.get_root():
            # if not treated on focused child, try to treat it on container
            switcher = {
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: self._action_on_focused_object,
                Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: self._end_of_container,
                Keyboard.BrailleFunction.BRAMIGRAPH_MENU: self.switch_to_parent,
                Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: self._focus_to_left,
                Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: self._focus_to_right,
                Keyboard.BrailleFunction.BRAMIGRAPH_HOME: self._focus_to_first,
                Keyboard.BrailleFunction.BRAMIGRAPH_END: self._focus_to_last,
                Keyboard.BrailleFunction.BRAMIGRAPH_TAB: self._tab,
                Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB: self._shift_tab,
            }
            func = switcher.get(bramigraph, None)
            if func is not None:
                # Execute function
                treated, in_menu = func(modifier)
                if in_menu:
                    # Reconstruct braille display.
                    self.ask_update_braille_display()
        return treated, in_menu

    def input_command(self, modifier, key_id) -> bool:
        """
        Do what needs to be done for this command key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: True if stay in menu
        """
        root_container = self.get_root()
        if root_container is None:
            raise ValueError("No root container ?")
        else:
            # Exec input_command on focused child.
            treated, in_menu = root_container.get_focused_object().exec_command(
                modifier, key_id
            )
            if not treated:
                treated, in_menu = root_container.exec_command(modifier, key_id)
        return in_menu

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        treated, in_menu = False, True
        if self == self.get_root():
            # if not treated on focused child, try to treat it on container
            switcher = {
                Keyboard.KeyId.KEY_ACTION: self._action_on_focused_object,
                Keyboard.KeyId.KEY_CARET_RIGHT: self._focus_to_right,
                Keyboard.KeyId.KEY_CARET_LEFT: self._focus_to_left,
                Keyboard.KeyId.KEY_MENU: self.switch_to_parent,
            }
            func = switcher.get(key_id, None)
            if func is not None:
                # Execute function
                treated, in_menu = func(modifier)
                if in_menu:
                    # Reconstruct braille display.
                    self.ask_update_braille_display()
            else:
                UiContainer.braille_display.input_command(modifier, key_id)
                treated = in_menu = True
        return treated, in_menu

    def input_interactive(self, modifier, position, key_type) -> bool:
        """
        Do what needs to be done for this modifier and cursor routine event.
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param position: index of key (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: True if command treated, otherwise False
        """
        in_menu = False
        if isinstance(self, UiContainer):
            root_container = self.get_root()
            if root_container is None:
                raise ValueError("No root container ?")
            else:
                treated, in_menu = root_container.do_interactive(
                    modifier, position, key_type
                )
        return in_menu

    def do_interactive(self, modifier, position, key_type) -> (bool, bool):
        treated, in_menu = False, True
        if self == self.get_root():
            # Determine the clicked object.
            line_pos = position + UiContainer.braille_display.get_start_pos() - 1
            if (modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE) and (
                line_pos < len(UiContainer.id_array_objects)
            ):
                object_id = UiContainer.id_array_objects[line_pos]
                log.info(f"interactive pos={line_pos}, object_id={object_id}")
                if self.get_id() == object_id:
                    # Clic on container.
                    ui_object = self
                else:
                    ui_object = self.get_object_from_id(object_id)
                if ui_object:
                    relative_pos = 0
                    for index in range(line_pos, 0, -1):
                        if object_id == UiContainer.id_array_objects[index]:
                            relative_pos += 1
                        else:
                            break
                    log.info(f"clicked object is {ui_object._name}")
                    # Do interactive key on object after give it the focus.
                    if not ui_object.is_focused():
                        self.get_focused_object().on_focus_lost(with_speaking=False)
                        ui_object.on_focus(with_speaking=False)
                    treated, in_menu = ui_object.exec_interactive(
                        modifier, relative_pos, key_type
                    )
        return treated, in_menu

    def _tab(self, modifier):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            return self._focus_to_right(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
        elif modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT:
            return self._focus_to_left(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
        else:
            # With other flags, the function is not treated.
            return False, True

    def _shift_tab(self, modifier):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            return self._focus_to_left(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
        elif modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT:
            return self._focus_to_right(Keyboard.BrailleModifier.BRAILLE_FLAG_NONE)
        else:
            # With other flags, the function is not treated.
            return False, True

    def _action_on_focused_object(
        self, modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE
    ) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            if self._is_root:
                ui_object = self.get_focused_object()
                return ui_object.exec_action()
            else:
                # Activate container
                return self.exec_action()
        return True, True

    def _focus_to_right(self, modifier) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            index = self._get_focused_object_index()
            self.ui_objects[index].on_focus_lost(with_speaking=False)
            new_index = self._find_next_visible_object(index)
            if new_index < 0:
                # Return to the first child
                new_index = self._find_next_visible_object(-1)
            self.ui_objects[new_index].on_focus(with_speaking=False)
        return True, True

    def _focus_to_left(self, modifier) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            index = self._get_focused_object_index()
            self.ui_objects[index].on_focus_lost(with_speaking=False)
            new_index = self._find_previous_visible_object(index)
            if new_index < 0:
                # Return to the last child
                new_index = self._find_previous_visible_object(len(self.ui_objects))
            self.ui_objects[new_index].on_focus(with_speaking=False)
        return True, True

    def _focus_to_first(self, modifier) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            index = self._get_focused_object_index()
            self.ui_objects[index].on_focus_lost(with_speaking=False)
            new_index = self._find_next_visible_object(-1)
            self.ui_objects[new_index].on_focus(with_speaking=False)
        return True, True

    def _focus_to_last(self, modifier) -> (bool, bool):
        """
        :return: (Treated, stay in menu)
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            index = self._get_focused_object_index()
            self.ui_objects[index].on_focus_lost(with_speaking=False)
            new_index = self._find_previous_visible_object(len(self.ui_objects))
            self.ui_objects[new_index].on_focus(with_speaking=False)
        return True, True

    def _end_of_container(self, modifier) -> (bool, bool):
        """
        Call by bramigraph escape, exept in menu this method do nothing, we stay in the container.
        :return: (Treated, stay in menu)
        """
        return True, True

    def switch_to_parent(self, modifier) -> (bool, bool):
        """
        Call when the parent menu bar become the root menu bar
        :return: (Treated, stay in menu)
        """
        self._switch_to_parent(modifier)
        # Anyway stay in container
        return True, True

    def _switch_to_parent(self, modifier) -> bool:
        """
        Return True is switch to parent is done (when self is not the root).
        """
        if modifier == Keyboard.BrailleModifier.BRAILLE_FLAG_NONE:
            parent = self._parent
            if parent and not parent.is_root():
                # The current root is not self
                self._is_root = False
                parent.set_as_root()
                return True
            else:
                # switch to parent is done on root.
                return False
        # Do nothing, switch_to_parent with modifier.
        return True

    def _find_next_visible_object(self, index) -> int:
        index += 1
        while index < len(self.ui_objects):
            if not self.ui_objects[index].is_hide():
                return index
            else:
                index += 1
        return -1

    def _find_previous_visible_object(self, index) -> int:
        index -= 1
        while index >= 0:
            if not self.ui_objects[index].is_hide():
                return index
            else:
                index -= 1
        return -1

    def set_as_root(self):
        """
        Defines self as root and reconstruct braille display.
        :return: None
        """
        self._is_root = True
        self._update_braille_display()

    def switch_to_root_of_root_menu(self):
        """
        Defines the up level menu as root, focus on the first object and reconstruct braille display.
        :return: None
        """
        self._is_root = False
        parent = self._parent
        if parent:
            parent.switch_to_root_of_root_menu()
        else:
            self._set_focused_object_to_first()
            self.set_as_root()

    def decode_shortcut(self, character):
        """
        Search the shortcut of an item in a container (recurse in sub container)
        """
        for ui_object in self.ui_objects:
            if ui_object.shortcut == character:
                log.info(f"{character=} is shortcut of {ui_object.name()}")
                return ui_object
            if isinstance(ui_object, UiContainer):
                # log.critical(f"{ui_object.name()=}")
                # for object in ui_object.ui_objects:
                #    log.critical(f"{object.name()=}")
                child_object = ui_object.decode_shortcut(character)
                if child_object is not None:
                    return child_object
        return None
