"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.apps.bnote_app import BnoteApp
import bnote.apps.edt.edt as editor
from bnote.tools.keyboard import Keyboard
from bnote.tools.settings import Settings
from .ui_container import UiContainer
from bnote.stm32.braille_device_characteristics import braille_device_characteristics

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiMultiLinesBox(UiContainer):
    """
    Multi lines editBox dialog.

    NOTE: When the value_id of an edit box is "", this editbox is not editable.
    """

    def __init__(self, name, value, no_grade=False, is_read_only=False):
        kwargs = {
            "braille_type": Settings().data["system"]["braille_type"],
            "name": name,
            "action": None,
        }
        self._no_grade = no_grade
        # Call base class.
        super().__init__(**kwargs)
        # manage value.
        self._value_id, value_text = value
        lines = value_text.split("\n")
        self._editor = editor.Editor(
            Settings().data["editor"]["line_length"], lines, is_read_only=is_read_only
        )
        self._editing = False
        # caret for forward and backward display function.
        self.is_moving_display = False
        self.moving_display_caret = None

    def replace_text(self, text):
        caret = self._editor.caret()
        lines = text.split("\n")
        self._editor = editor.Editor(
            Settings().data["editor"]["line_length"],
            lines,
            is_read_only=self._editor.read_only,
        )
        self._editor.set_caret(caret)

    def get_presentation(self):
        """
        Construct presentation for an object
        :return: (name in text, name in braille, braille blinking dots list of id of braille length
        """
        if self._is_hide:
            return None, None, None, None
        elif not self._editing:
            # Convert braille to text.
            return super().get_presentation()
        else:
            # Multi lines edit box is displayed as container.
            raise ValueError("Big error !")

    def get_focused_object(self):
        """
        Overload UiContainer function.
        UiMultiLibnesBox has no focused objects
        :return: self
        """
        return self

    # ---------------
    # braille display functions.
    def _refresh_braille_display(self, offset=0, line_index=None):
        """
        Refresh braille display
        :param offset:
        :param line_index:
        :return:
        """
        if self._editor:
            (line, dots) = self._editor.editor_braille_line(line_index)
            blink_dots = BnoteApp.lou.byte_to_unicode_braille(dots)
            if self._braille_type and (
                (self._braille_type == "grade1") or (self._braille_type == "grade2")
            ):
                static_dots = BnoteApp.lou.to_dots_6(line)
            else:
                static_dots = BnoteApp.lou.to_dots_8(line)
            UiContainer.braille_display.set_data_line(
                line, static_dots, blink_dots, offset
            )

    def _refresh_center_braille_display(self):
        """
        Refresh braille display and center display at caret position.
        :param:
        :return:
        """
        self._refresh_braille_display()
        UiContainer.braille_display.center(self._editor.caret().end.x)

    def _update_braille_display(self):
        log.debug(f"_update_braille_display <{self._name}>")
        self._refresh_braille_display()

    def get_value(self):
        cnt = 0
        document = ""
        while True:
            line = self._editor.paragraph_text(cnt)
            if line is None:
                break
            else:
                document = "\n".join((document, line))
            cnt += 1
        return self._value_id, document

    def exec_action(self) -> (bool, bool):
        """
        Action on object. Switch in/out edition
        :return: (Treated, stay in menu)
        """
        self.__switch_edit_mode()
        return True, True

    def is_editing(self):
        return self._editing

    def __switch_edit_mode(self):
        # Switch edit mode.
        self._editing = not self._editing
        parent = self.get_parent()
        if self._editing:
            # Multi lines edit box becomes a root container.
            parent.set_root(False)
            self.set_root(True)
            self.ask_update_braille_display()
        else:
            # Multi lines edit box becomes a child.
            parent.set_root(True)
            self.set_root(False)
            parent.ask_update_braille_display()

    def on_focus_lost(self, with_speaking):
        """
        When edit box lost the focus, it turns off also editing mode.
        :param with_speaking:
        :return:
        """
        # edit mode turn off
        self._editing = False
        super().on_focus_lost(with_speaking)

    def exec_command(self, modifier, key_id) -> (bool, bool):
        """
        Do what needs to be done for this command key and return (refresh, object_id).
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        log.info(f"input_command on edit box {self._name}")
        treated, in_menu = False, True
        if self._editing:
            kwargs = Keyboard.decode_modifiers(modifier)
            if kwargs["alt"]:
                # alt+key not treated.
                return False, True

            if key_id == Keyboard.KeyId.KEY_MENU:
                # End of edition
                self.exec_action()
                return True, True
            # Decoding key command for braille display line.
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_BACKWARD):
                self._backward_display()
                treated = True
            elif (modifier == 0) and (key_id == Keyboard.KeyId.KEY_FORWARD):
                self._forward_display()
                treated = True
            else:
                command_switcher = {
                    Keyboard.KeyId.KEY_CARET_UP: (
                        editor.Editor.Functions.MOVE_UP,
                        None,
                    ),
                    Keyboard.KeyId.KEY_CARET_DOWN: (
                        editor.Editor.Functions.MOVE_DOWN,
                        None,
                    ),
                    Keyboard.KeyId.KEY_CARET_RIGHT: (
                        editor.Editor.Functions.MOVE_RIGHT,
                        None,
                    ),
                    Keyboard.KeyId.KEY_CARET_LEFT: (
                        editor.Editor.Functions.MOVE_LEFT,
                        None,
                    ),
                    Keyboard.KeyId.KEY_START_DOC: (
                        editor.Editor.Functions.MOVE_HOME,
                        {"shift": False, "ctrl": True},
                    ),
                    Keyboard.KeyId.KEY_END_DOC: (
                        editor.Editor.Functions.MOVE_END,
                        {"shift": False, "ctrl": True},
                    ),
                }

                (editor_function, new_kwargs) = command_switcher.get(
                    key_id, (None, None)
                )
                if editor_function:
                    # Execute the function
                    if new_kwargs:
                        # Overload shift and ctrl parameters
                        kwargs.update(new_kwargs)
                    self._editor.function(editor_function, **kwargs)
                    # Refresh braille display
                    self._refresh_center_braille_display()
                    treated = True

        return treated, in_menu

    def exec_character(self, modifier, character, data) -> (bool, bool):
        """
        Do what needs to be done for this braille modifier and character.
        :param modifier: keyboard modifiers
        :param character: character
        :param data: data from protocol
        :return: (Treated, stay in menu)
        """
        log.info(f"{modifier=} {character=} {data=}")
        if self._editing:
            kwargs = Keyboard.decode_modifiers(modifier)
            if kwargs["alt"]:
                # Let alt+c to change focus on dialog box.
                return False, True
            elif kwargs["ctrl"]:
                # Shortcut Ctrl+... decoding.
                return self.__exec_ctrl_character(kwargs, character)
            else:
                # Modifiers could be transmitted ?
                self._editor.function(
                    editor.Editor.Functions.PUT_STRING, **{"text": character}
                )
                # Refresh braille display
                self._refresh_center_braille_display()
            return True, True
        return False, True

    def __exec_ctrl_character(self, kwargs, character):
        """
        Treat Ctrl+char shortcuts.
        :return: (Treated, stay in menu)
        """
        character_switcher = {
            "a": editor.Editor.Functions.SELECT_ALL,
            "c": editor.Editor.Functions.COPY,
            "v": editor.Editor.Functions.PASTE,
            "x": editor.Editor.Functions.CUT,
            "y": editor.Editor.Functions.REDO,
            "z": editor.Editor.Functions.UNDO,
        }
        # Get the function from switcher dictionnary
        editor_function = character_switcher.get(character, None)
        if editor_function:
            # Execute the function
            self._editor.function(editor_function, **kwargs)
            # Refresh braille display
            self._refresh_center_braille_display()
        return True, True

    def exec_bramigraph(self, modifier, bramigraph) -> (bool, bool):
        """
        Do what needs to be done for this bramigraph key.
        :param modifier: command modifiers
        :param key_id: command value
        :return: (Treated, stay in menu)
        """
        if self._editing:
            # command treatment for document.
            kwargs = BnoteApp.keyboard.decode_modifiers(modifier)
            if kwargs["alt"]:
                # If Alt... => No treatment
                return False, True
            # If escape and not in selection of text => Exit edition
            if not self._editor.selection_mode() and (
                bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE
            ):
                return self.exec_action()
            bramigraph_switcher = {
                Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: editor.Editor.Functions.SELECTION_MODE_OFF,
                Keyboard.BrailleFunction.BRAMIGRAPH_TAB: editor.Editor.Functions.TAB,
                Keyboard.BrailleFunction.BRAMIGRAPH_HOME: editor.Editor.Functions.MOVE_HOME,
                Keyboard.BrailleFunction.BRAMIGRAPH_END: editor.Editor.Functions.MOVE_END,
                Keyboard.BrailleFunction.BRAMIGRAPH_PRIOR: editor.Editor.Functions.PAGE_UP,
                Keyboard.BrailleFunction.BRAMIGRAPH_NEXT: editor.Editor.Functions.PAGE_DOWN,
                Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: editor.Editor.Functions.MOVE_LEFT,
                Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: editor.Editor.Functions.MOVE_RIGHT,
                Keyboard.BrailleFunction.BRAMIGRAPH_UP: editor.Editor.Functions.MOVE_UP,
                Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: editor.Editor.Functions.MOVE_DOWN,
                Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: editor.Editor.Functions.DELETE,
                Keyboard.BrailleFunction.BRAMIGRAPH_F2: editor.Editor.Functions.MARKER,
                # Keyboard.BrailleFunction.BRAMIGRAPH_F3: editor.Editor.Functions.FIND,
                # Keyboard.BrailleFunction.BRAMIGRAPH_F4: editor.Editor.Functions.REPLACE_AND_FIND,
                # Keyboard.BrailleFunction.BRAMIGRAPH_F5: editor.Editor.Functions.REPLACE_ALL,
                Keyboard.BrailleFunction.BRAMIGRAPH_F8: editor.Editor.Functions.SELECTION_MODE_ON,
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: editor.Editor.Functions.BACKSPACE,
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE: editor.Editor.Functions.SPACE,
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: editor.Editor.Functions.CARRIAGE_RETURN,
            }

            # command treatment for document.
            kwargs = BnoteApp.keyboard.decode_modifiers(modifier)
            # Get the function from switcher dictionnary
            editor_function = bramigraph_switcher.get(bramigraph, None)
            if editor_function:
                # Execute the function
                self._editor.function(editor_function, **kwargs)
                # Refresh braille display
                self._refresh_center_braille_display()
                return True, True
            log.warning(
                "No function for bramigraph editbox defined for {}".format(bramigraph)
            )
        return super().exec_bramigraph(modifier, bramigraph)

    def do_interactive(self, modifier, relative_pos, key_type) -> (bool, bool):
        """
        Exec on interactive clic
        :param modifier: bits field (see Keyboard.BrailleModifier)
        :param relative_pos: pos in object (based 1)
        :param key_type: see Keyboard.InteractiveKeyType
        :return: (Treated, stay in menu)
        """
        log.info(f"Clic on objet {self._name}, {relative_pos=}")
        if self._editing:
            if key_type == Keyboard.InteractiveKeyType.DOUBLE_CLIC:
                # Kill grade2 mode
                # DP FIXME Something to do when interactive key press on grade2 braille display.
                # self._is_forward_grade2 = False
                # Kill moving display without caret mode.
                self.is_moving_display = False
                self._editor.function(
                    editor.Editor.Functions.SELECT_WORD,
                    **{
                        "pos": editor.Pos(
                            UiContainer.braille_display.get_start_pos()
                            + relative_pos
                            - 1,
                            self._editor.caret().end.y,
                        )
                    },
                )
            else:
                # if self.is_moving_display:
                # Kill moving display without caret mode.
                #    self.is_moving_display = False
                #    line = self.moving_display_caret.end.y
                # else:
                line = self._editor.caret().end.y
                self._editor.function(
                    editor.Editor.Functions.PUT_CARET,
                    **{
                        "pos": editor.Pos(
                            UiContainer.braille_display.get_start_pos()
                            + relative_pos
                            - 1,
                            line,
                        )
                    },
                )
            # Refresh braille display (useful after caret move)
            self.end_move_display(None, UiContainer.braille_display.get_start_pos())
        return True, True

    def _backward_display(self):
        log.info("backward display")
        # Backward in grade0
        if self._editor.caret().is_selection_empty():
            # Move caret if no selection.
            self._backward_display_with_caret_moving()
        else:
            if not self.is_moving_display:
                self.moving_display_caret = self._editor.caret()
                self.is_moving_display = True

            save_caret = editor.Caret(self._editor.caret())
            self._editor.set_caret(self.moving_display_caret)
            self._backward_display_with_caret_moving(save_caret)

    def _backward_display_with_caret_moving(self, save_caret=None):
        if UiContainer.braille_display.backward():
            log.info("backward on line")
            self._editor.function(
                editor.Editor.Functions.PUT_CARET,
                **{
                    "shift": False,
                    "ctrl": False,
                    "pos": editor.Pos(
                        UiContainer.braille_display.get_start_pos(),
                        self._editor.caret().end.y,
                    ),
                },
            )
        else:
            # line change.
            log.info("backward on line change => goto start of the new line")
            self._editor.function(
                editor.Editor.Functions.MOVE_UP, **{"shift": False, "ctrl": False}
            )
            self._editor.function(
                editor.Editor.Functions.MOVE_HOME, **{"shift": False, "ctrl": False}
            )
            # Compute braille offset position
            (line, dots) = self._editor.editor_braille_line(self._editor.caret().end.y)
            offset = 0
            braille_display_length = (
                braille_device_characteristics.get_braille_display_length()
            )
            if line and (len(line) > braille_display_length):
                offset = len(line) - braille_display_length
            self._editor.function(
                editor.Editor.Functions.PUT_CARET,
                **{
                    "shift": False,
                    "ctrl": False,
                    "pos": editor.Pos(offset, self._editor.caret().end.y),
                },
            )
            UiContainer.braille_display.set_start_pos(offset)
        # Refresh braille display (useful after caret move)
        log.debug(
            "Backward offset{}".format(UiContainer.braille_display.get_start_pos())
        )
        self.end_move_display(save_caret, UiContainer.braille_display.get_start_pos())

    def _forward_display(self):
        log.info("forward display")
        # Forward in grade0
        if self._editor.caret().is_selection_empty():
            # Move caret if no selection.
            self._forward_display_with_caret_moving()
        else:
            # if selection, create a moving_display_caret
            if not self.is_moving_display:
                self.moving_display_caret = self._editor.caret()
                self.is_moving_display = True

            save_caret = editor.Caret(self._editor.caret())
            self._editor.set_caret(self.moving_display_caret)
            self._forward_display_with_caret_moving(save_caret)

    def _forward_display_with_caret_moving(self, save_caret=None):
        braille_offset = UiContainer.braille_display.get_start_pos()
        if UiContainer.braille_display.forward():
            log.info("Forward on line")
            braille_offset = UiContainer.braille_display.get_start_pos()
            # Put caret at the start of display.
            self._editor.function(
                editor.Editor.Functions.PUT_CARET,
                **{
                    "shift": False,
                    "ctrl": False,
                    "pos": editor.Pos(braille_offset, self._editor.caret().end.y),
                },
            )
        else:
            # line change.
            log.info("Forward on line change")
            while True:
                if self._editor.function(
                    editor.Editor.Functions.MOVE_DOWN, **{"shift": False, "ctrl": False}
                ):
                    # Move to the start of the line
                    self._editor.function(
                        editor.Editor.Functions.MOVE_HOME,
                        **{"shift": False, "ctrl": False},
                    )
                    braille_offset = 0
                    (new_line, dots) = self._editor.editor_braille_line(
                        self._editor.caret().end.y
                    )
                    new_line = new_line.replace(" ", "")
                    if (
                        Settings().data["editor"]["forward_display_mode"] == "normal"
                    ) or new_line != "":
                        # Line not empty, it is the right one.
                        break
                else:
                    break
        # Refresh braille display
        log.debug("Forward offset{}".format(braille_offset))
        self.end_move_display(save_caret, braille_offset)

    def end_move_display(self, save_caret, braille_offset):
        line_index = None
        if save_caret:
            self.moving_display_caret = editor.Caret(self._editor.caret())
            line_index = self._editor.caret().end.y
            log.info("line to display is {}".format(line_index))
            self._editor.set_caret(save_caret)
        self._refresh_braille_display(braille_offset, line_index)
