"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import subprocess
from pathlib import Path
from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
import bnote.ui as ui

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, SKELETON_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(SKELETON_APP_LOG)


class TerminalApp(BnoteApp):
    """
    Terminal application for executing commands and viewing output.
    """

    def __init__(self, put_in_function_queue):
        """
        Class constructor
        :param put_in_function_queue: (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class.
        super().__init__(put_in_function_queue)
        
        # Command history
        self._command_history = []
        self._history_index = -1
        
        # Current command input
        self._current_command = ""
        
        # Output buffer (stores command + output pairs)
        self._output_lines = []
        self._current_line_index = 0
        
        # Working directory
        self._working_directory = Path.home()
        
        # menu creation.
        self._menu = self.__create_menu()
        
        # Initial prompt
        self._add_prompt()
        self.set_data_line()

    def __create_menu(self):
        # Instantiate menu (A menu bar with menu items).
        return ui.UiMenuBar(
            name=_("terminal"),
            # Call on ESC bramigraph key
            is_root=True,
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&execute command"),
                    action=self._exec_command_dialog,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,
                ),
                ui.UiMenuItem(
                    name=_("&clear output"),
                    action=self._exec_clear,
                ),
                ui.UiMenuItem(
                    name=_("change &directory"),
                    action=self._exec_change_directory,
                ),
                ui.UiMenuItem(
                    name=_("command &history"),
                    action=self._exec_show_history,
                ),
                ui.UiMenuItem(
                    name=_("&about"),
                    action=self._exec_about,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_NONE,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F1,
                ),
            ],
        )

    def translate_ui(self):
        """
        Do the translation according to the current translation
        """
        self._in_menu = False
        self._menu = self.__create_menu()

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
        self.set_data_line()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        :return:
        """
        self.set_data_line()

    # ---------------
    # Menu functions.
    
    def _exec_command_dialog(self):
        """
        Display dialog to enter a command.
        """
        self._current_dialog = ui.UiDialogBox(
            name=_("execute command"),
            item_list=[
                ui.UiEditBox(
                    name=_("&command"),
                    value=("command", "")
                ),
                ui.UiButton(name=_("&execute"), action=self._exec_run_command),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_run_command(self):
        """
        Execute the command entered in the dialog.
        """
        kwargs = self._current_dialog.get_values()
        command = kwargs.get("command", "").strip()
        
        if command:
            self._execute_command(command)

    def _execute_command(self, command):
        """
        Execute a shell command and display the output.
        :param command: The command string to execute
        """
        log.info(f"Executing command: {command}")
        
        # Add to history
        if command and (not self._command_history or self._command_history[-1] != command):
            self._command_history.append(command)
        self._history_index = len(self._command_history)
        
        # Add command to output
        self._output_lines.append(f"$ {command}")
        
        # Handle built-in cd command
        if command.startswith("cd "):
            path_str = command[3:].strip()
            if not path_str:
                path_str = str(Path.home())
            
            try:
                new_path = Path(path_str)
                if not new_path.is_absolute():
                    new_path = self._working_directory / new_path
                new_path = new_path.resolve()
                
                if new_path.exists() and new_path.is_dir():
                    self._working_directory = new_path
                    self._output_lines.append(f"Changed directory to: {self._working_directory}")
                else:
                    self._output_lines.append(f"Error: Directory not found: {new_path}")
            except Exception as e:
                self._output_lines.append(f"Error: {str(e)}")
        elif command == "pwd":
            self._output_lines.append(str(self._working_directory))
        else:
            # Execute external command
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=str(self._working_directory),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = result.stdout.strip()
                error = result.stderr.strip()
                
                if output:
                    for line in output.split('\n'):
                        self._output_lines.append(line)
                
                if error:
                    for line in error.split('\n'):
                        self._output_lines.append(f"Error: {line}")
                
                if not output and not error:
                    self._output_lines.append(_("Command completed"))
                    
            except subprocess.TimeoutExpired:
                self._output_lines.append(_("Error: Command timed out"))
            except Exception as e:
                self._output_lines.append(f"Error: {str(e)}")
        
        # Add new prompt
        self._add_prompt()
        
        # Move to the last line
        self._current_line_index = len(self._output_lines) - 1
        
        # Update display
        self.set_data_line()

    def _add_prompt(self):
        """
        Add a command prompt to the output.
        """
        prompt = f"{self._working_directory.name}$ "
        self._output_lines.append(prompt)

    def _exec_clear(self):
        """
        Clear the terminal output.
        """
        self._output_lines = []
        self._current_line_index = 0
        self._add_prompt()
        self.set_data_line()

    def _exec_change_directory(self):
        """
        Display dialog to change directory.
        """
        self._current_dialog = ui.UiDialogBox(
            name=_("change directory"),
            item_list=[
                ui.UiEditBox(
                    name=_("&path"),
                    value=("path", str(self._working_directory))
                ),
                ui.UiButton(name=_("&ok"), action=self._exec_do_change_directory),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_do_change_directory(self):
        """
        Change the working directory.
        """
        kwargs = self._current_dialog.get_values()
        path_str = kwargs.get("path", "").strip()
        
        if path_str:
            try:
                new_path = Path(path_str)
                if not new_path.is_absolute():
                    new_path = self._working_directory / new_path
                new_path = new_path.resolve()
                
                if new_path.exists() and new_path.is_dir():
                    self._working_directory = new_path
                    self._output_lines.append(f"Changed directory to: {self._working_directory}")
                    self._add_prompt()
                    self._current_line_index = len(self._output_lines) - 1
                    self.set_data_line()
                else:
                    # Show error in dialog
                    self._current_dialog = ui.UiMessageDialogBox(
                        name=_("error"),
                        message=_("Directory not found"),
                        buttons=[
                            ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                        ],
                        action_cancelable=self._exec_cancel_dialog,
                    )
            except Exception as e:
                self._current_dialog = ui.UiMessageDialogBox(
                    name=_("error"),
                    message=str(e),
                    buttons=[
                        ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                    ],
                    action_cancelable=self._exec_cancel_dialog,
                )

    def _exec_show_history(self):
        """
        Display command history.
        """
        if not self._command_history:
            history_text = _("No command history")
        else:
            history_text = "\n".join(
                f"{i+1}. {cmd}" for i, cmd in enumerate(self._command_history[-20:])
            )
        
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("command history"),
            message=history_text,
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        """
        Display an information dialog box.
        """
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("terminal application V1.0.0"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

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
        done = super(TerminalApp, self).input_command(data, modifier, key_id)
        if not done:
            # Decoding key command for braille display line.
            done = self._braille_display.input_command(modifier, key_id)
            
            # Navigation through output
            if not done:
                if key_id == Keyboard.KeyId.KEY_CARET_UP:
                    if self._current_line_index > 0:
                        self._current_line_index -= 1
                        self.set_data_line()
                        done = True
                elif key_id == Keyboard.KeyId.KEY_CARET_DOWN:
                    if self._current_line_index < len(self._output_lines) - 1:
                        self._current_line_index += 1
                        self.set_data_line()
                        done = True
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
        done = super(TerminalApp, self).input_character(modifier, character, data)
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
        done = super(TerminalApp, self).input_bramigraph(modifier, bramigraph)
        
        # Quick access to execute command dialog
        if not done and bramigraph == Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN:
            self._exec_command_dialog()
            done = True
        
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
        done = super(TerminalApp, self).input_interactive(modifier, position, key_type)
        return done

    def input_function(self, *args, **kwargs) -> bool:
        """
        Call when function is not treated by base class of this class.
        :param args[0]: The function id
        :param kwargs:
        :return: True if function treated.
        """
        log.info("args={} kwargs={}".format(args, kwargs))
        # Call base class decoding.
        done = super(TerminalApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions.
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        pass

    # --------------------
    # Document functions.
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if self._output_lines:
            # Display current line
            text = self._output_lines[self._current_line_index]
        else:
            text = _("Terminal ready")
        
        braille_static = BnoteApp.lou.to_dots_8(text)
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(
            text, braille_static, braille_blinking, 0
        )
