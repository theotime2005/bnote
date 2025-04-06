"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from enum import Enum

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, KEYBOARD_LOG

log = ColoredLogger(__name__)
log.setLevel(KEYBOARD_LOG)


class Keyboard:
    class KeyId(Enum):
        KEY_NONE = object()

        KEY_SPEECH_VOLUME_DOWN = object()
        KEY_SPEECH_VOLUME_UP = object()

        KEY_SPEECH_SPEED_DOWN = object()
        KEY_SPEECH_SPEED_UP = object()

        KEY_START_DOC = object()
        KEY_END_DOC = object()

        # 4 Keys bloc on the left
        KEY_MENU = object()
        KEY_ACTION = object()
        KEY_BACKWARD = object()
        KEY_FORWARD = object()

        # 4 Keys bloc on the right
        KEY_CARET_UP = object()
        KEY_CARET_DOWN = object()
        KEY_CARET_LEFT = object()
        KEY_CARET_RIGHT = object()

        # 3 special combinaisons for media controls.
        KEY_MEDIA_VOLUME_DOWN = object()
        KEY_MEDIA_VOLUME_UP = object()
        KEY_MEDIA_MUTE = object()

        # Special combinaison keys KEY_MENU and KEY_BACKWARD
        KEY_APPLICATIONS = object()

        # Special combinaison key to autoscroll the braille display.
        KEY_AUTOSCROLL = object()

        KEY_TOGGLE_GRADE2 = object()

        # Paragraphes commands
        KEY_PREVIOUS_PARAGRAPHE = object()
        KEY_NEXT_PARAGRAPHE = object()

    class BrailleType(Enum):
        UNKNOWN = object()
        CHARACTER = object()
        FUNCTION = object()

    class BrailleModifier:
        BRAILLE_FLAG_NONE = 0x00
        BRAILLE_FLAG_SHIFT = 0x01
        BRAILLE_FLAG_CTRL = 0x02
        BRAILLE_FLAG_ALT = 0x04
        BRAILLE_FLAG_WIN = 0x08
        BRAILLE_FLAG_INS = 0x10
        BRAILLE_FLAG_BRAMIGRAPH = 0x80

    class BrailleFunction(Enum):
        BRAMIGRAPH_NONE = object()

        BRAMIGRAPH_ESCAPE = object()
        BRAMIGRAPH_TAB = object()
        BRAMIGRAPH_SHIFT_TAB = object()
        BRAMIGRAPH_NUMPAD_RETURN = object()
        BRAMIGRAPH_NUMPAD7 = object()
        BRAMIGRAPH_HOME = object()
        BRAMIGRAPH_NUMPAD1 = object()
        BRAMIGRAPH_END = object()
        BRAMIGRAPH_NUMPAD9 = object()
        BRAMIGRAPH_PRIOR = object()
        BRAMIGRAPH_NUMPAD3 = object()
        BRAMIGRAPH_NEXT = object()
        BRAMIGRAPH_NUMPAD4 = object()
        BRAMIGRAPH_LEFT = object()
        BRAMIGRAPH_NUMPAD6 = object()
        BRAMIGRAPH_RIGHT = object()
        BRAMIGRAPH_NUMPAD8 = object()
        BRAMIGRAPH_UP = object()
        BRAMIGRAPH_NUMPAD2 = object()
        BRAMIGRAPH_DOWN = object()
        BRAMIGRAPH_INSERT = object()
        BRAMIGRAPH_NUMPAD0 = object()
        BRAMIGRAPH_NUMPAD_COMMA = object()
        BRAMIGRAPH_DELETE = object()
        BRAMIGRAPH_F1 = object()
        BRAMIGRAPH_F2 = object()

        BRAMIGRAPH_F3 = object()
        BRAMIGRAPH_F4 = object()
        BRAMIGRAPH_F5 = object()
        BRAMIGRAPH_F6 = object()
        BRAMIGRAPH_F7 = object()
        BRAMIGRAPH_F8 = object()
        BRAMIGRAPH_F9 = object()
        BRAMIGRAPH_F10 = object()
        BRAMIGRAPH_F11 = object()
        BRAMIGRAPH_F12 = object()

        BRAMIGRAPH_NUMPAD_DIVIDE = object()
        BRAMIGRAPH_NUMPAD_MULTIPLY = object()
        BRAMIGRAPH_NUMPAD_SUBSTRACT = object()
        BRAMIGRAPH_NUMPAD_ADD = object()
        BRAMIGRAPH_NUMPAD5 = object()

        BRAMIGRAPH_CAPSLOCKON = object()
        BRAMIGRAPH_CAPSLOCKOFF = object()
        BRAMIGRAPH_NUMLOCKON = object()
        BRAMIGRAPH_NUMLOCKOFF = object()
        BRAMIGRAPH_SHIFT = object()
        BRAMIGRAPH_CONTROL = object()
        BRAMIGRAPH_MENU = object()
        BRAMIGRAPH_LWIN = object()
        BRAMIGRAPH_APPS = object()
        BRAMIGRAPH_CTRL_PRESSED = object()
        BRAMIGRAPH_CTRL_RELEASED = object()
        BRAMIGRAPH_MENU_PRESSED = object()
        BRAMIGRAPH_MENU_RELEASED = object()

        BRAMIGRAPH_SIMPLE_BACKSPACE = object()
        BRAMIGRAPH_SIMPLE_SPACE = object()
        BRAMIGRAPH_SIMPLE_RETURN = object()
        BRAMIGRAPH_PRINT_SCREEN = object()
        BRAMIGRAPH_BREAK = object()

        @staticmethod
        def get_bramigraph_label(bramigraph):
            functions_label = {
                Keyboard.BrailleFunction.BRAMIGRAPH_ESCAPE: "escape",
                Keyboard.BrailleFunction.BRAMIGRAPH_TAB: "tab",
                Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT_TAB: "shift tab",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_RETURN: "numpad enter",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD7: "numpad 7",
                Keyboard.BrailleFunction.BRAMIGRAPH_HOME: "numpad home",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD1: "numpad 1",
                Keyboard.BrailleFunction.BRAMIGRAPH_END: "end",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD9: "numpad 9",
                Keyboard.BrailleFunction.BRAMIGRAPH_PRIOR: "page up",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD3: "numpad 3",
                Keyboard.BrailleFunction.BRAMIGRAPH_NEXT: "page down",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD4: "numpad 4",
                Keyboard.BrailleFunction.BRAMIGRAPH_LEFT: "left",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD6: "numpad 6",
                Keyboard.BrailleFunction.BRAMIGRAPH_RIGHT: "right",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD8: "numpad 8",
                Keyboard.BrailleFunction.BRAMIGRAPH_UP: "up",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD2: "numpad 2",
                Keyboard.BrailleFunction.BRAMIGRAPH_DOWN: "down",
                Keyboard.BrailleFunction.BRAMIGRAPH_INSERT: "insert",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD0: "numpad 0",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_COMMA: "numpad .",
                Keyboard.BrailleFunction.BRAMIGRAPH_DELETE: "delete",
                Keyboard.BrailleFunction.BRAMIGRAPH_F1: "F1",
                Keyboard.BrailleFunction.BRAMIGRAPH_F2: "F2",
                Keyboard.BrailleFunction.BRAMIGRAPH_F3: "F3",
                Keyboard.BrailleFunction.BRAMIGRAPH_F4: "F4",
                Keyboard.BrailleFunction.BRAMIGRAPH_F5: "F5",
                Keyboard.BrailleFunction.BRAMIGRAPH_F6: "F6",
                Keyboard.BrailleFunction.BRAMIGRAPH_F7: "F7",
                Keyboard.BrailleFunction.BRAMIGRAPH_F8: "F8",
                Keyboard.BrailleFunction.BRAMIGRAPH_F9: "F9",
                Keyboard.BrailleFunction.BRAMIGRAPH_F10: "F10",
                Keyboard.BrailleFunction.BRAMIGRAPH_F11: "F11",
                Keyboard.BrailleFunction.BRAMIGRAPH_F12: "F12",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_DIVIDE: "numpad /",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_MULTIPLY: "numpad *",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_SUBSTRACT: "numpad -",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD_ADD: "numpad +",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMPAD5: "numpad 5",
                Keyboard.BrailleFunction.BRAMIGRAPH_CAPSLOCKON: "capslock on",
                Keyboard.BrailleFunction.BRAMIGRAPH_CAPSLOCKOFF: "capslock off",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMLOCKON: "numlock on",
                Keyboard.BrailleFunction.BRAMIGRAPH_NUMLOCKOFF: "numlock off",
                Keyboard.BrailleFunction.BRAMIGRAPH_SHIFT: "shift",
                Keyboard.BrailleFunction.BRAMIGRAPH_CONTROL: "ctrl",
                Keyboard.BrailleFunction.BRAMIGRAPH_MENU: "alt",
                Keyboard.BrailleFunction.BRAMIGRAPH_LWIN: "left win",
                Keyboard.BrailleFunction.BRAMIGRAPH_APPS: "apps",
                Keyboard.BrailleFunction.BRAMIGRAPH_CTRL_PRESSED: "ctrl down",
                Keyboard.BrailleFunction.BRAMIGRAPH_CTRL_RELEASED: "ctrl up",
                Keyboard.BrailleFunction.BRAMIGRAPH_MENU_PRESSED: "alt down",
                Keyboard.BrailleFunction.BRAMIGRAPH_MENU_RELEASED: "alt up",
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE: "backspace",
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE: "space",
                Keyboard.BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN: "return",
                Keyboard.BrailleFunction.BRAMIGRAPH_PRINT_SCREEN: "print screen",
                Keyboard.BrailleFunction.BRAMIGRAPH_BREAK: "break",
            }
            try:
                return functions_label[bramigraph]
            except ValueError as er:
                return "unknow"

    class InteractiveKeyType(Enum):
        CLIC = object()
        REPEAT = object()
        DOUBLE_CLIC = object()
        # FIXME : le type sera plutôt quelque chose comme çà
        # CLIC = object()
        # STRONG_CLIC = object()
        # DOUBLE_CLIC = object()
        # STRONG_DOUBLE_CLIC = object()

    def __init__(self):
        log.info("Keyboard")
        self.caps_lock = False

    # Used by decode_braille.
    braille_functions_switcher = {
        # Edition
        0x0100: BrailleFunction.BRAMIGRAPH_SIMPLE_BACKSPACE,  # 9
        0x0200: BrailleFunction.BRAMIGRAPH_SIMPLE_SPACE,  # A
        0x0300: BrailleFunction.BRAMIGRAPH_SIMPLE_RETURN,  # 9A
        0x0214: BrailleFunction.BRAMIGRAPH_INSERT,  # 35A
        0x0224: BrailleFunction.BRAMIGRAPH_DELETE,  # 36A
        # Navigaton
        0x0207: BrailleFunction.BRAMIGRAPH_HOME,  # 123A
        0x0238: BrailleFunction.BRAMIGRAPH_END,  # 456A
        0x0202: BrailleFunction.BRAMIGRAPH_LEFT,  # 2A
        0x0210: BrailleFunction.BRAMIGRAPH_RIGHT,  # 5A
        0x0208: BrailleFunction.BRAMIGRAPH_UP,  # 4A
        0x0220: BrailleFunction.BRAMIGRAPH_DOWN,  # 6A
        0x0205: BrailleFunction.BRAMIGRAPH_PRIOR,  # 13A
        0x0228: BrailleFunction.BRAMIGRAPH_NEXT,  # 46A
        # Numpad
        0x0121: BrailleFunction.BRAMIGRAPH_NUMPAD1,  # 169
        0x0123: BrailleFunction.BRAMIGRAPH_NUMPAD2,  # 1269
        0x0129: BrailleFunction.BRAMIGRAPH_NUMPAD3,  # 1469
        0x0139: BrailleFunction.BRAMIGRAPH_NUMPAD4,  # 14569
        0x0131: BrailleFunction.BRAMIGRAPH_NUMPAD5,  # 1569
        0x012B: BrailleFunction.BRAMIGRAPH_NUMPAD6,  # 12469
        0x013B: BrailleFunction.BRAMIGRAPH_NUMPAD7,  # 124569
        0x0133: BrailleFunction.BRAMIGRAPH_NUMPAD8,  # 12569
        0x012A: BrailleFunction.BRAMIGRAPH_NUMPAD9,  # 2469
        0x013C: BrailleFunction.BRAMIGRAPH_NUMPAD0,  # 34569
        0x010C: BrailleFunction.BRAMIGRAPH_NUMPAD_DIVIDE,  # 349
        0x0114: BrailleFunction.BRAMIGRAPH_NUMPAD_MULTIPLY,  # 359
        0x0124: BrailleFunction.BRAMIGRAPH_NUMPAD_SUBSTRACT,  # 369
        0x0116: BrailleFunction.BRAMIGRAPH_NUMPAD_ADD,  # 2359
        0x0102: BrailleFunction.BRAMIGRAPH_NUMPAD_COMMA,  # 29
        0x011C: BrailleFunction.BRAMIGRAPH_NUMPAD_RETURN,  # 3459
        0x022D: BrailleFunction.BRAMIGRAPH_PRINT_SCREEN,  # 1346A
        0x0209: BrailleFunction.BRAMIGRAPH_BREAK,  # 14A
        # Others
        0x021B: BrailleFunction.BRAMIGRAPH_ESCAPE,  # 1245A
        0x0232: BrailleFunction.BRAMIGRAPH_TAB,  # 256A
        0x0216: BrailleFunction.BRAMIGRAPH_SHIFT_TAB,  # 235A
        0x010F: BrailleFunction.BRAMIGRAPH_LWIN,  # 12349
        0x0130: BrailleFunction.BRAMIGRAPH_APPS,  # 569
        # Functions
        0x0101: BrailleFunction.BRAMIGRAPH_F1,  # 19
        0x0103: BrailleFunction.BRAMIGRAPH_F2,  # 129
        0x0109: BrailleFunction.BRAMIGRAPH_F3,  # 149
        0x0119: BrailleFunction.BRAMIGRAPH_F4,  # 1459
        0x0111: BrailleFunction.BRAMIGRAPH_F5,  # 159
        0x010B: BrailleFunction.BRAMIGRAPH_F6,  # 1249
        0x011B: BrailleFunction.BRAMIGRAPH_F7,  # 12459
        0x0113: BrailleFunction.BRAMIGRAPH_F8,  # 1259
        0x010A: BrailleFunction.BRAMIGRAPH_F9,  # 249
        0x011A: BrailleFunction.BRAMIGRAPH_F10,  # 2459
        0x0105: BrailleFunction.BRAMIGRAPH_F11,  # 139
        0x0107: BrailleFunction.BRAMIGRAPH_F12,  # 1239
        # Switches
        0x0140: BrailleFunction.BRAMIGRAPH_CAPSLOCKON,  # 79
        0x0180: BrailleFunction.BRAMIGRAPH_CAPSLOCKOFF,  # 89
        0x0104: BrailleFunction.BRAMIGRAPH_NUMLOCKON,  # 39
        0x0120: BrailleFunction.BRAMIGRAPH_NUMLOCKOFF,  # 69
        0x0240: BrailleFunction.BRAMIGRAPH_SHIFT,  # 7A
        0x02C0: BrailleFunction.BRAMIGRAPH_CONTROL,  # 78A
        0x0280: BrailleFunction.BRAMIGRAPH_MENU,  # 8A
        0x02C1: BrailleFunction.BRAMIGRAPH_CTRL_PRESSED,  # 178A
        0x02C8: BrailleFunction.BRAMIGRAPH_CTRL_RELEASED,  # 478A
        0x0281: BrailleFunction.BRAMIGRAPH_MENU_PRESSED,  # 18A
        0x0288: BrailleFunction.BRAMIGRAPH_MENU_RELEASED,  # 48A
    }

    # decode braille comb from spi protocol in a modifier and a value
    def decode_braille(self, lou, data, is_grade_1_or_2=False) -> (int, int, int):
        # use int for modifier allows logical operations.
        modifier = int.from_bytes(data[3:4], "big")
        log.debug("modifier={:x}".format(modifier))

        if modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_BRAMIGRAPH:
            # BRAMIGRAPH conversion
            # modifier BRAILLE_FLAG_BRAMIGRAPH is removed from modifiers list.
            braille_function = Keyboard.braille_functions_switcher.get(
                int.from_bytes(data[4:6], "big"),
                Keyboard.BrailleFunction.BRAMIGRAPH_NONE,
            )
            if braille_function == Keyboard.BrailleFunction.BRAMIGRAPH_CAPSLOCKON:
                self.caps_lock = True
            elif braille_function == Keyboard.BrailleFunction.BRAMIGRAPH_CAPSLOCKOFF:
                self.caps_lock = False
            return (
                Keyboard.BrailleType.FUNCTION,
                modifier & ~Keyboard.BrailleModifier.BRAILLE_FLAG_BRAMIGRAPH,
                braille_function,
            )

        else:
            # Use lib louis to convert braille comb to char.
            if lou:
                if is_grade_1_or_2:
                    ch = lou.to_text_6(lou.byte_to_unicode_braille(data[1:2]))
                else:
                    ch = lou.to_text_8(lou.byte_to_unicode_braille(data[1:2]))
                if ("a" <= ch <= "z") and (
                    (modifier & Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT)
                    or self.caps_lock
                ):
                    # convert to uppercase
                    ch = ch.upper()
            else:
                ch = 0
            # older version character is data[5]
            # ch = data[5]
            # Convert braille comb. to char.
            log.info("Character:{}".format(ch))

            return Keyboard.BrailleType.CHARACTER, modifier, ch
        # return Keyboard.BrailleType.UNKNOWN, 0, 0

    # Used by decode_command.
    command_switcher = {
        0x0001: KeyId.KEY_CARET_UP,
        0x0002: KeyId.KEY_CARET_DOWN,
        0x0004: KeyId.KEY_CARET_RIGHT,
        0x0008: KeyId.KEY_CARET_LEFT,
        0x0010: KeyId.KEY_APPLICATIONS,
        0x0020: KeyId.KEY_MENU,
        0x0100: KeyId.KEY_FORWARD,
        0x0200: KeyId.KEY_BACKWARD,
        0x0009: KeyId.KEY_START_DOC,  # right bloc, key up + right bloc, key left
        0x0005: KeyId.KEY_END_DOC,  # right bloc, key up + right bloc, key right
        0x000A: KeyId.KEY_SPEECH_VOLUME_DOWN,  # right bloc, key down + right bloc, key left
        0x0006: KeyId.KEY_SPEECH_VOLUME_UP,  # right bloc, key down + right bloc, key right
        0x00C0: KeyId.KEY_SPEECH_SPEED_DOWN,  # left bloc, key left + left bloc, key right
        0x000C: KeyId.KEY_SPEECH_SPEED_UP,  # right bloc, key left + right bloc, key right
        0x00A0: KeyId.KEY_MEDIA_VOLUME_DOWN,  # left bloc, key down + Left bloc, key left
        0x0060: KeyId.KEY_MEDIA_VOLUME_UP,  # left bloc, key down + Left bloc, key right
        0x0090: KeyId.KEY_MEDIA_MUTE,  # left bloc, key up + left bloc, key left
        0x0050: KeyId.KEY_TOGGLE_GRADE2,  # left bloc, key up + left bloc, key right
        0x0030: KeyId.KEY_AUTOSCROLL,  # left bloc, key up + left bloc, key down
        0x0011: KeyId.KEY_PREVIOUS_PARAGRAPHE,  # left bloc, key down + right bloc, key up
        0x0012: KeyId.KEY_NEXT_PARAGRAPHE,  # left bloc, key down + right bloc, key down
        # right bloc, key up + right bloc, key down => not used, too difficult to type
        # left bloc, key up + left bloc, key down => not used, too difficult to type
    }

    # return : (modifiers, keysId)
    @staticmethod
    def decode_command(data) -> (int, int):
        # log.error("data1={}".format(int.from_bytes(data[0:1], 'big')))
        # log.error("data2={}".format(int.from_bytes(data[1:2], 'big')))
        # log.error("data3={}".format(int.from_bytes(data[2:3], 'big')))
        log.debug("Command key data={}".format(data))
        return int.from_bytes(data[0:1], "big"), Keyboard.command_switcher.get(
            int.from_bytes(data[1:3], "big"), Keyboard.KeyId.KEY_NONE
        )

    @staticmethod
    def decode_modifiers(modifiers):
        kwarg = {"shift": False, "ctrl": False, "alt": False, "win": False}
        if (modifiers & Keyboard.BrailleModifier.BRAILLE_FLAG_SHIFT) != 0:
            kwarg["shift"] = True
        if (modifiers & Keyboard.BrailleModifier.BRAILLE_FLAG_CTRL) != 0:
            kwarg["ctrl"] = True
        if (modifiers & Keyboard.BrailleModifier.BRAILLE_FLAG_ALT) != 0:
            kwarg["alt"] = True
        if (modifiers & Keyboard.BrailleModifier.BRAILLE_FLAG_WIN) != 0:
            kwarg["win"] = True
        return kwarg

    # Used by decode_interactive.
    interactive_type_switcher = {
        0x01: InteractiveKeyType.CLIC,
        0x03: InteractiveKeyType.DOUBLE_CLIC,
    }

    # Decode the interactive data and return (position, key_type) of the interactive key
    def decode_interactive(self, data) -> (int, object()):
        log.debug("Interactive key data={}".format(data))
        modifiers = int.from_bytes(data[0:1], "big")
        key_type = int.from_bytes(data[1:2], "big")
        position = int.from_bytes(data[2:3], "big")
        return modifiers, position, Keyboard.interactive_type_switcher.get(key_type)
