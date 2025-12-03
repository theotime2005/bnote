# Terminal Application

## Overview
The Terminal application allows users to execute shell commands and interact with the bnote device through a command-line interface.

## Features
- Execute shell commands (ls, pwd, whoami, etc.)
- View command output in a scrollable interface
- Command history (stores last executed commands)
- Built-in cd command for directory navigation
- Change working directory through menu
- Clear output functionality

## Usage

### Opening the Terminal
1. Access the application menu (press Applications key)
2. Navigate to "terminal" menu item
3. Press Enter to open the terminal application

### Executing Commands
1. Press Enter (BRAMIGRAPH_SIMPLE_RETURN) to open command dialog
2. Enter your command in the text field
3. Press Execute button to run the command
4. View output on the braille display

### Navigation
- Use Cursor Up/Down keys to scroll through output lines
- Use L/R braille display keys to navigate within a line

### Menu Options
- **Execute command**: Opens dialog to enter and run a command (shortcut: Enter)
- **Clear output**: Clears all terminal output
- **Change directory**: Opens dialog to change working directory
- **Command history**: Shows list of previously executed commands
- **About**: Shows version information (shortcut: F1)

## Implementation Details

### Command Execution
- Commands are executed using Python's `subprocess.run()`
- Timeout: 30 seconds
- Working directory is maintained across commands
- Built-in commands: cd, pwd

### Output Display
- Output is stored line-by-line in `_output_lines` buffer
- Current line position tracked with `_current_line_index`
- Navigation allows scrolling through all output

### Command History
- Stores up to all executed commands
- Accessible through menu
- Shows last 20 commands in history dialog

## Configuration
The terminal app can be configured in Settings:
- `app_terminal`: Set visibility ('invisible', 'main_apps_menu', 'more_apps_menu')

## Files
- `bnote/apps/terminal/__init__.py`: Package initialization
- `bnote/apps/terminal/terminal_app.py`: Main application implementation
- Registered in: `bnote/apps/internal.py`
- Settings: `bnote/tools/settings.py`

## Translation Keys
The following keys are used for internationalization (defined in terminal_app.py):
- "terminal" - Application name
- "execute command" - Command dialog title
- "command" - Command input field label
- "execute" - Execute button
- "cancel" - Cancel button
- "clear output" - Clear menu item
- "change directory" - Directory change dialog
- "path" - Directory path field
- "command history" - History dialog title
- "No command history" - Empty history message
- "information" - About dialog title
- "terminal application V1.0.0" - Version info
- "Command completed" - Success message
- "Error: Command timed out" - Timeout error
- "Directory not found" - CD error

## Version
1.0.0 - Initial implementation
