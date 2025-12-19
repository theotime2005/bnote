"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json
import socket
import ssl
import threading
from enum import Enum

from bnote.apps.bnote_app import BnoteApp
from bnote.tools.keyboard import Keyboard
import bnote.ui as ui

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, REMOTE_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(REMOTE_APP_LOG)

# Constants
DEFAULT_BRAILLE_DISPLAY_SIZE = 40
RECEIVE_BUFFER_SIZE = 4096
BRAILLE_DOT_BYTE_SHIFT = 8

# Windows Virtual Key Codes for NVDA Remote
VK_BACK = 0x08
VK_TAB = 0x09
VK_RETURN = 0x0D
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12  # ALT key
VK_ESCAPE = 0x1B
VK_SPACE = 0x20
VK_PRIOR = 0x21  # PAGE UP
VK_NEXT = 0x22   # PAGE DOWN
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_INSERT = 0x2D
VK_DELETE = 0x2E
VK_LWIN = 0x5B
VK_APPS = 0x5D
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A
VK_ADD = 0x6B
VK_SUBTRACT = 0x6D
VK_DECIMAL = 0x6E
VK_DIVIDE = 0x6F
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B


class ConnectionMode(Enum):
    """Connection mode for NVDA Remote"""
    MASTER = "master"  # Control remote computer
    SLAVE = "slave"    # Be controlled by remote computer


class RemoteApp(BnoteApp):
    """
    REmote application for controlling computers with NVDA Remote.
    Allows controlling a computer with NVDA software and NVDA Remote extension.
    """

    PROTOCOL_VERSION = 2
    
    # Key mapping from bnote KeyId to Windows VK codes
    KEY_TO_VK_MAP = {
        Keyboard.KeyId.KEY_CARET_UP: VK_UP,
        Keyboard.KeyId.KEY_CARET_DOWN: VK_DOWN,
        Keyboard.KeyId.KEY_CARET_LEFT: VK_LEFT,
        Keyboard.KeyId.KEY_CARET_RIGHT: VK_RIGHT,
        Keyboard.KeyId.KEY_START_DOC: VK_HOME,
        Keyboard.KeyId.KEY_END_DOC: VK_END,
    }
    
    # Key mapping from bnote BrailleFunction to Windows VK codes
    BRAMIGRAPH_TO_VK_MAP = {
        Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: VK_ESCAPE,
        Keyboard.BrailleFunction.BRAMIGRAPH_TAB: VK_TAB,
        Keyboard.BrailleFunction.BRAMIGRAPH_HOME: VK_HOME,
        Keyboard.BrailleFunction.BRAMIGRAPH_END: VK_END,
        Keyboard.BrailleFunction.BRAMIGRAPH_PRIOR: VK_PRIOR,
        Keyboard.BrailleFunction.BRAMIGRAPH_NEXT: VK_NEXT,
        Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: VK_LEFT,
        Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: VK_RIGHT,
        Keyboard.BrailleFunction.BRAMIGRAPH_UP: VK_UP,
        Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: VK_DOWN,
        Keyboard.BrailleFunction.BRAMIGRAPH_INSERT: VK_INSERT,
        Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: VK_DELETE,
        Keyboard.BrailleFunction.BRAMIGRAPH_F1: VK_F1,
        Keyboard.BrailleFunction.BRAMIGRAPH_F2: VK_F2,
        Keyboard.BrailleFunction.BRAMIGRAPH_F3: VK_F3,
        Keyboard.BrailleFunction.BRAMIGRAPH_F4: VK_F4,
        Keyboard.BrailleFunction.BRAMIGRAPH_F5: VK_F5,
        Keyboard.BrailleFunction.BRAMIGRAPH_F6: VK_F6,
        Keyboard.BrailleFunction.BRAMIGRAPH_F7: VK_F7,
        Keyboard.BrailleFunction.BRAMIGRAPH_F8: VK_F8,
        Keyboard.BrailleFunction.BRAMIGRAPH_F9: VK_F9,
        Keyboard.BrailleFunction.BRAMIGRAPH_F10: VK_F10,
        Keyboard.BrailleFunction.BRAMIGRAPH_F11: VK_F11,
        Keyboard.BrailleFunction.BRAMIGRAPH_F12: VK_F12,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD0: VK_NUMPAD0,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD1: VK_NUMPAD1,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD2: VK_NUMPAD2,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD3: VK_NUMPAD3,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD4: VK_NUMPAD4,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD5: VK_NUMPAD5,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD6: VK_NUMPAD6,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD7: VK_NUMPAD7,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD8: VK_NUMPAD8,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD9: VK_NUMPAD9,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_DIVIDE: VK_DIVIDE,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_MULTIPLY: VK_MULTIPLY,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_SUBTRACT: VK_SUBTRACT,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_ADD: VK_ADD,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_COMMA: VK_DECIMAL,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: VK_BACK,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE: VK_SPACE,
        Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: VK_RETURN,
        Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_RETURN: VK_RETURN,
        Keyboard.BrailleFunction.BRAMIGRAPH_LWIN: VK_LWIN,
        Keyboard.BrailleFunction.BRAMIGRAPH_APPS: VK_APPS,
        Keyboard.BrailleFunction.BRAMIGRAPH_MENU: VK_MENU,
    }

    def __init__(self, put_in_function_queue):
        """
        Class constructor
        :param put_in_function_queue: (for multi-threading) queue of functions ask to bnote Internal class
        """
        # Call base class
        super().__init__(put_in_function_queue)
        
        # Connection state
        self._connected = False
        self._connecting = False
        self._socket = None
        self._ssl_socket = None
        self._connection_thread = None
        self._receive_thread = None
        self._running = False
        
        # Connection parameters
        self._host = ""
        self._port = 6837  # Default NVDA Remote relay port
        self._channel = ""
        self._connection_mode = ConnectionMode.SLAVE
        
        # Braille display state
        self._braille_cells = []
        self._braille_display_text = ""
        
        # Remote control state
        self._remote_control_enabled = False
        
        # Menu creation
        self._menu = self.__create_menu()
        
        # Initial document refresh
        self.set_data_line()

    def __create_menu(self):
        """Create the application menu"""
        return ui.UiMenuBar(
            name=_("remote"),
            is_root=True,
            menu_item_list=[
                ui.UiMenuItem(
                    name=_("&connect"),
                    action=self._exec_connect_menu
                ),
                ui.UiMenuItem(
                    name=_("&disconnect"),
                    action=self._exec_disconnect_menu
                ),
                ui.UiMenuItem(
                    name=_("&toggle remote control"),
                    action=self._exec_toggle_remote_control,
                    shortcut_modifier=Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL,
                    shortcut_key=Keyboard.BrailleFunction.BRAMIGRAPH_F2,
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
        """
        self.set_data_line()

    def refresh_document(self):
        """
        To overload if application need to do something when dialogbox or menu are closed.
        """
        self.set_data_line()

    # ---------------
    # Menu functions

    def _exec_connect_menu(self):
        """Show connection dialog"""
        if self._connected:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("already connected"),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
            
        self._current_dialog = ui.UiDialogBox(
            name=_("connect to remote"),
            item_list=[
                ui.UiEditBox(
                    name=_("&host"),
                    value=("host", self._host or "nvdaremote.com")
                ),
                ui.UiEditBox(
                    name=_("&port"),
                    value=("port", str(self._port))
                ),
                ui.UiEditBox(
                    name=_("&channel"),
                    value=("channel", self._channel or "")
                ),
                ui.UiListBox(
                    name=_("&mode"),
                    value=("mode", [_("slave"), _("master")]),
                    current_index=0 if self._connection_mode == ConnectionMode.SLAVE else 1,
                ),
                ui.UiButton(name=_("&connect"), action=self._exec_connect),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_disconnect_menu(self):
        """Disconnect from remote"""
        if not self._connected and not self._connecting:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("not connected"),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
            
        self._disconnect()
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("disconnected"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_about(self):
        """Display information dialog"""
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=_("NVDA Remote application V1.0.0\nControl computers with NVDA Remote"),
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    def _exec_toggle_remote_control(self):
        """Toggle remote control on/off"""
        if not self._connected:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("information"),
                message=_("not connected"),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
        
        self._remote_control_enabled = not self._remote_control_enabled
        status = _("enabled") if self._remote_control_enabled else _("disabled")
        self._current_dialog = ui.UiMessageDialogBox(
            name=_("information"),
            message=f"{_('remote control')} {status}",
            buttons=[
                ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
            ],
            action_cancelable=self._exec_cancel_dialog,
        )

    # --------------------
    # Dialog functions

    def _exec_connect(self):
        """Execute connection with parameters from dialog"""
        log.info("callback:_exec_connect")
        kwargs = self._current_dialog.get_values()
        log.info(f"{kwargs=}")
        
        # Get connection parameters
        self._host = kwargs.get("host", "nvdaremote.com")
        try:
            self._port = int(kwargs.get("port", "6837"))
        except ValueError:
            self._port = 6837
        self._channel = kwargs.get("channel", "")
        
        # Get mode
        mode_index = kwargs.get("mode", 0)
        if isinstance(mode_index, str):
            mode_index = 0 if mode_index == _("slave") else 1
        self._connection_mode = ConnectionMode.SLAVE if mode_index == 0 else ConnectionMode.MASTER
        
        if not self._channel:
            self._current_dialog = ui.UiMessageDialogBox(
                name=_("error"),
                message=_("channel is required"),
                buttons=[
                    ui.UiButton(name=_("&ok"), action=self._exec_cancel_dialog),
                ],
                action_cancelable=self._exec_cancel_dialog,
            )
            return
        
        # Close dialog and connect
        self._current_dialog = None
        self._connect()

    def _connect(self):
        """Establish connection to NVDA Remote relay server"""
        if self._connected or self._connecting:
            return
            
        self._connecting = True
        self._running = True
        
        # Start connection in a separate thread
        self._connection_thread = threading.Thread(target=self._connection_worker, daemon=True)
        self._connection_thread.start()
        
        # Update display
        self._braille_display_text = _("connecting...")
        self.set_data_line()

    def _disconnect(self):
        """Disconnect from NVDA Remote"""
        self._running = False
        self._connected = False
        self._connecting = False
        
        if self._ssl_socket:
            try:
                self._ssl_socket.close()
            except Exception as e:
                log.error(f"Error closing SSL socket: {e}")
            self._ssl_socket = None
            
        if self._socket:
            try:
                self._socket.close()
            except Exception as e:
                log.error(f"Error closing socket: {e}")
            self._socket = None
        
        self._braille_cells = []
        self._braille_display_text = _("disconnected")
        self.set_data_line()

    def _connection_worker(self):
        """Worker thread for handling connection"""
        try:
            log.info(f"Connecting to {self._host}:{self._port}")
            
            # Create socket
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(10.0)
            
            # Wrap with SSL
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            # Explicitly set minimum TLS version for security
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            
            self._ssl_socket = context.wrap_socket(self._socket, server_hostname=self._host)
            self._ssl_socket.connect((self._host, self._port))
            
            log.info("Connected, sending protocol version")
            
            # Send protocol version
            self._send_message("protocol_version", version=self.PROTOCOL_VERSION)
            
            # Send join message
            self._send_message(
                "join",
                channel=self._channel,
                connection_type=self._connection_mode.value
            )
            
            self._connected = True
            self._connecting = False
            self._braille_display_text = _("connected")
            self.set_data_line()
            
            # Start receive thread
            self._receive_thread = threading.Thread(target=self._receive_worker, daemon=True)
            self._receive_thread.start()
            
        except Exception as e:
            log.error(f"Connection error: {e}")
            self._connecting = False
            self._connected = False
            self._braille_display_text = f"{_('connection error')}: {str(e)}"
            self.set_data_line()
            self._disconnect()

    def _receive_worker(self):
        """Worker thread for receiving messages"""
        buffer = b""
        
        while self._running and self._connected:
            try:
                data = self._ssl_socket.recv(RECEIVE_BUFFER_SIZE)
                if not data:
                    log.info("Connection closed by remote")
                    break
                    
                buffer += data
                
                # Process complete messages (separated by newlines)
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if line:
                        self._handle_message(line)
                        
            except socket.timeout:
                continue
            except Exception as e:
                log.error(f"Receive error: {e}")
                break
        
        self._disconnect()

    def _send_message(self, msg_type, **kwargs):
        """Send a message to the remote server"""
        if not self._ssl_socket:
            return
            
        try:
            message = {"type": msg_type}
            message.update(kwargs)
            data = json.dumps(message).encode('utf-8') + b'\n'
            self._ssl_socket.sendall(data)
            log.info(f"Sent message: {msg_type}")
        except Exception as e:
            log.error(f"Error sending message: {e}")

    def _handle_message(self, data):
        """Handle a received message"""
        try:
            message = json.loads(data.decode('utf-8'))
            msg_type = message.get("type")
            
            log.info(f"Received message: {msg_type}")
            
            if msg_type == "channel_joined":
                self._braille_display_text = _("channel joined")
                self.set_data_line()
                
                # Send braille display info
                display_size = len(self._braille_display.get_data_line()[1] or "")
                if display_size == 0:
                    display_size = DEFAULT_BRAILLE_DISPLAY_SIZE
                self._send_message(
                    "set_braille_info",
                    name="bnote",
                    numCells=display_size
                )
                
            elif msg_type == "display":
                # Handle braille display update
                cells = message.get("cells", [])
                self._braille_cells = cells
                self._update_braille_display(cells)
                
            elif msg_type == "client_joined":
                client = message.get("client", {})
                log.info(f"Client joined: {client}")
                
            elif msg_type == "client_left":
                client_id = message.get("client")
                log.info(f"Client left: {client_id}")
                
            elif msg_type == "error":
                error_msg = message.get("message", "unknown error")
                log.error(f"Server error: {error_msg}")
                self._braille_display_text = f"{_('error')}: {error_msg}"
                self.set_data_line()
                
        except Exception as e:
            log.error(f"Error handling message: {e}")

    def _update_braille_display(self, cells):
        """Update braille display with received cells"""
        try:
            # Convert cell values to braille unicode
            braille_text = ""
            for cell in cells:
                # Cell is a dot pattern (0-255)
                # Convert to unicode braille character
                braille_char = chr(0x2800 + cell)
                braille_text += braille_char
            
            self._braille_display_text = braille_text
            self.set_data_line()
            
        except Exception as e:
            log.error(f"Error updating braille display: {e}")

    def _send_braille_input(self, dots, space=False, routing_index=None):
        """Send braille input to remote"""
        if not self._connected:
            return
            
        message_data = {"dots": dots, "space": space}
        if routing_index is not None:
            message_data["routingIndex"] = routing_index
            
        self._send_message("braille_input", **message_data)

    def _send_key(self, vk_code, scan_code, extended, pressed):
        """Send key press/release to remote"""
        if not self._connected:
            return
            
        self._send_message(
            "key",
            vk_code=vk_code,
            scan_code=scan_code,
            extended=extended,
            pressed=pressed
        )

    def _send_modifier_keys(self, modifier, pressed):
        """Send modifier key state to remote"""
        if modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT:
            self._send_key(VK_SHIFT, 0, False, pressed)
        if modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL:
            self._send_key(VK_CONTROL, 0, False, pressed)
        if modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_ALT:
            self._send_key(VK_MENU, 0, False, pressed)
        if modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_WIN:
            self._send_key(VK_LWIN, 0, False, pressed)

    def _forward_key_to_remote(self, vk_code, modifier):
        """Helper method to forward a key with modifiers to remote"""
        # Send modifiers first
        if modifier:
            self._send_modifier_keys(modifier, True)
        # Send key press and release
        self._send_key(vk_code, 0, False, True)
        self._send_key(vk_code, 0, False, False)
        # Release modifiers
        if modifier:
            self._send_modifier_keys(modifier, False)

    # --------------------
    # Key event functions

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
            # Ignore keys up event
            return False
            
        log.info("key_id={}".format(key_id))
        
        # Pass the command to DialogBox / Menu / BrailleDisplay
        done = super(RemoteApp, self).input_command(data, modifier, key_id)
        
        if not done and self._connected and self._remote_control_enabled:
            # Forward command keys to remote when remote control is enabled
            vk_code = self.KEY_TO_VK_MAP.get(key_id)
            if vk_code:
                self._forward_key_to_remote(vk_code, modifier)
                done = True
            
        if not done:
            # Decoding key command for braille display line
            done = self._braille_display.input_command(modifier, key_id)
            
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
        done = super(RemoteApp, self).input_character(modifier, character, data)
        
        if not done and self._connected and self._remote_control_enabled:
            # Forward character input to remote when remote control is enabled
            # Convert braille data to dots value for sending
            # Data format: byte[0] and byte[1] contain braille dot pattern
            if len(data) >= 2:
                dots = data[0] | (data[1] << BRAILLE_DOT_BYTE_SHIFT)
                self._send_braille_input(dots)
            done = True
            
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
        done = super(RemoteApp, self).input_bramigraph(modifier, bramigraph)
        
        if not done and self._connected and self._remote_control_enabled:
            # Forward bramigraph keys to remote when remote control is enabled
            vk_code = self.BRAMIGRAPH_TO_VK_MAP.get(bramigraph)
            if vk_code:
                self._forward_key_to_remote(vk_code, modifier)
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
        done = super(RemoteApp, self).input_interactive(modifier, position, key_type)
        
        if not done and self._connected and self._remote_control_enabled:
            # Send cursor routing to remote
            if key_type == Keyboard.InteractiveKeyType.CURSOR:
                self._send_braille_input(0, False, position - 1)
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
        
        # Call base class decoding
        done = super(RemoteApp, self).input_function(*args, **kwargs)
        return done

    # --------------------
    # Timer event functions
    def on_timer(self):
        """
        Event each seconds
        :return: None
        """
        pass

    # --------------------
    # Document functions
    def set_data_line(self):
        """
        Construct the braille display line from document
        :return: None (self._braille_display.set_data_line is done)
        """
        if self._braille_display_text:
            # Display original braille from remote (no translation)
            braille_static = self._braille_display_text
        else:
            # Display default message (these need translation)
            if self._connected:
                if self._remote_control_enabled:
                    text = _("remote control enabled")
                else:
                    text = _("remote connected")
            elif self._connecting:
                text = _("connecting...")
            else:
                text = _("not connected - use menu to connect")
            braille_static = BnoteApp.lou.to_dots_8(text)
            
        braille_blinking = "\u2800" * len(braille_static)
        self._braille_display.set_data_line(
            None, braille_static, braille_blinking, 0
        )

    def on_close(self):
        """
        Called when application is being closed
        """
        self._disconnect()

    def shutdown(self, focused):
        """
        Called on shutdown
        """
        self._disconnect()
