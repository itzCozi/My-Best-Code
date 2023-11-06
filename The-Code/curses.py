# CURSES HELPER LIBRARY (change the name of the file to prevent error)
# OS: Windows10
# PY-VERSION: 3.11+
# GITHUB: https://github.com/itzCozi/Helper

try:
  import os, sys
  import curses
  import _curses
  import string
  import ctypes
  import time
  from ctypes import wintypes
except Exception:
  print('Win32 uses a different library, run \'pip install windows-curses\' to fix this.')
  sys.exit(1)

# TODO's
'''
* Make sure all vars use snake_case and funcs use camelCase
'''


class vars:  # Variable container

  def error(error_type: str, var: str = None, type: str = None, runtime_error: str = None):
    if error_type == 'p':
      print(f'PARAMETER: Given variable {var} is not a {type}.')
    elif error_type == 'r':
      print(f'RUNTIME: {runtime_error.capitalize()}.')
    elif error_type == 'u':
      print('UNKNOWN: An unknown error was encountered.')
    return vars.exit_code

  platform = sys.platform
  DEV_MODE = True
  exit_code = None


KEY_MAP: dict = {
  "BACKSPACE": 8,
  "TAB": 9,
  "ENTER": 10,
  "ESCAPE": 27,
  "DOWN": 258,
  "UP": 259,
  "LEFT": 260,
  "RIGHT": 261,
  "HOME": 262,
  "F1": 265,
  "F2": 266,
  "F3": 267,
  "F4": 268,
  "F5": 269,
  "F6": 270,
  "F7": 271,
  "F8": 272,
  "F9": 273,
  "F10": 274,
  "F11": 275,
  "F12": 276,
  "DELETE": 330,
  "INSERT": 331,
  "PAGEDOWN": 338,
  "PAGEUP": 339,
  "END": 358,
}


# Some of this code is a stack overflow paste (idk win32 API)
class keyboard:
  """
  A class for controlling and sending keystrokes

  -----------------------------------------
  |    function            description    |
  |---------------------------------------|
  | pressMouse: Sends a VK input to mouse |
  | releaseMouse: Halt VK signal          |
  | pressKey: Presses given key hex code  |
  | releaseKey: Stop given VK input       |
  | pressAndReleaseKey: N/A               |
  | pressAndReleaseMouse: N/A             |
  | keyboardWrite: Sends vk inputs        |
  -----------------------------------------
  """

  user32 = ctypes.WinDLL('user32', use_last_error=True)
  INPUT_MOUSE = 0
  INPUT_KEYBOARD = 1
  KEYEVENTF_EXTENDEDKEY = 0x0001
  KEYEVENTF_KEYUP = 0x0002
  KEYEVENTF_UNICODE = 0x0004
  KEYEVENTF_SCANCODE = 0x0008
  MAPVK_VK_TO_VSC = 0

  # Reference: msdn.microsoft.com/en-us/library/dd375731
  # Each key value is 4 chars long and formatted in hexadecimal
  vk_codes: dict = {
    # --- Mouse ---
    "left_mouse": 0x01,
    "right_mouse": 0x02,
    "middle_mouse": 0x04,
    "mouse_button1": 0x05,
    "mouse_button2": 0x06,
    # --- Control Keys ---
    "win": 0x5B,  # Left Windows key
    "select": 0x29,
    "pg_down": 0x21,
    "pg_up": 0x22,
    "end": 0x23,
    "home": 0x24,
    "insert": 0x2D,
    "delete": 0x2E,
    "back": 0x08,
    "enter": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "caps": 0x14,
    "escape": 0x1,
    "space": 0x20,
    "tab": 0x09,
    "sleep": 0x5F,
    "zoom": 0xFB,
    "num_lock": 0x90,
    "scroll_lock": 0x91,
    # --- OEM Specific ---
    "plus": 0xBB,
    "comma": 0xBC,
    "minus": 0xBD,
    "period": 0xBE,
    # --- Media ---
    "vol_mute": 0xAD,
    "vol_down": 0xAE,
    "vol_up": 0xAF,
    "next": 0xB0,
    "prev": 0xB1,
    "pause": 0xB2,
    "play": 0xB3,
    # --- Arrow Keys ---
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    # --- Function Keys ---
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "f13": 0x7C,
    "f14": 0x7D,
    "f15": 0x7E,
    # --- Keypad ---
    "pad_0": 0x60,
    "pad_1": 0x61,
    "pad_2": 0x62,
    "pad_3": 0x63,
    "pad_4": 0x64,
    "pad_5": 0x65,
    "pad_6": 0x66,
    "pad_7": 0x67,
    "pad_8": 0x68,
    "pad_9": 0x69,
    # --- Symbols ---
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    # --- Alphanumerical ---
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    "=": 0x6B,
    " ": 0x20,
    ".": 0xBE,
    ",": 0xBC,
    "-": 0x6D,
    "`": 0xC0,
    "/": 0xBF,
    ";": 0xBA,
    "[": 0xDB,
    "]": 0xDD,
    "_": 0x6D,  # Shift
    "|": 0xDC,  # Shift
    "~": 0xC0,  # Shift
    "?": 0xBF,  # Shift
    ":": 0xBA,  # Shift
    "<": 0xBC,  # Shift
    ">": 0xBE,  # Shift
    "{": 0xDB,  # Shift
    "}": 0xDD,  # Shift
    "!": 0x31,  # Shift
    "@": 0x32,  # Shift
    "#": 0x33,  # Shift
    "$": 0x34,  # Shift
    "%": 0x35,  # Shift
    "^": 0x36,  # Shift
    "&": 0x37,  # Shift
    "*": 0x38,  # Shift
    "(": 0x39,  # Shift
    ")": 0x30,  # Shift
    "+": 0x6B,  # Shift
    "\"": 0xDE,  # Shift
    "\'": 0xDE,
    "\\": 0xDC,
    "\n": 0x0D
  }

  # C struct declarations
  wintypes.ULONG_PTR = wintypes.WPARAM
  global MOUSEINPUT, KEYBDINPUT

  class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
      ('dx', wintypes.LONG),
      ('dy', wintypes.LONG),
      ('mouseData', wintypes.DWORD),
      ('dwFlags', wintypes.DWORD),
      ('time', wintypes.DWORD),
      ('dwExtraInfo', wintypes.ULONG_PTR)
    )

  class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
      ('wVk', wintypes.WORD),
      ('wScan', wintypes.WORD),
      ('dwFlags', wintypes.DWORD),
      ('time', wintypes.DWORD),
      ('dwExtraInfo', wintypes.ULONG_PTR)
    )

    def __init__(self, *args, **kwds):
      super(KEYBDINPUT, self).__init__(*args, **kwds)
      # some programs use the scan code even if KEYEVENTF_SCANCODE
      # isn't set in dwFflags, so attempt to map the correct code.
      if not self.dwFlags & keyboard.KEYEVENTF_UNICODE:
        self.wScan = keyboard.user32.MapVirtualKeyExW(
          self.wVk,
          keyboard.MAPVK_VK_TO_VSC,
          0
        )

  class INPUT(ctypes.Structure):

    class _INPUT(ctypes.Union):
      _fields_ = (('ki', KEYBDINPUT), ('mi', MOUSEINPUT))

    _anonymous_ = ('_input',)
    _fields_ = (('type', wintypes.DWORD), ('_input', _INPUT))

  LPINPUT = ctypes.POINTER(INPUT)

  # Helpers
  def _check_count(result, func, args):
    if result == 0:
      raise ctypes.WinError(ctypes.get_last_error())
    return args

  def _lookup(key):
    if key in keyboard.vk_codes:
      return keyboard.vk_codes.get(key)
    else:
      return False

  user32.SendInput.errcheck = _check_count
  user32.SendInput.argtypes = (
    wintypes.UINT,  # nInputs
    LPINPUT,  # pInputs
    ctypes.c_int  # cbSize
  )

  # Functions (most people will only use these)
  def pressMouse(mouse_button: str) -> None:
    """
    Presses a mouse button

    Args:
      mouse_button (str): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    mouse_button_list = ["left_mouse", "right_mouse", "middle_mouse", "mouse_button1", "mouse_button2"]
    if mouse_button not in mouse_button_list:
      vars.error(error_type='r', runtime_error='given key code is not a mouse button')
      return vars.exit_code
    if keyboard._lookup(mouse_button) != False:
      mouse_button = keyboard._lookup(mouse_button)
    elif mouse_button not in keyboard.vk_codes:
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    x = keyboard.INPUT(
      type=keyboard.INPUT_MOUSE,
      mi=MOUSEINPUT(wVk=mouse_button)
    )
    keyboard.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  def releaseMouse(mouse_button: str) -> None:
    """
    Releases a mouse button

    Args:
      mouse_button (str): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    mouse_button_list = ["left_mouse", "right_mouse", "middle_mouse", "mouse_button1", "mouse_button2"]
    if mouse_button not in mouse_button_list:
      vars.error(error_type='r', runtime_error='given key code is not a mouse button')
      return vars.exit_code
    if keyboard._lookup(mouse_button) != False:
      mouse_button = keyboard._lookup(mouse_button)
    elif mouse_button not in keyboard.vk_codes.values():
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    x = keyboard.INPUT(
      type=keyboard.INPUT_MOUSE,
      mi=MOUSEINPUT(
        wVk=mouse_button,
        dwFlags=keyboard.KEYEVENTF_KEYUP
      )
    )
    keyboard.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  def pressKey(key_code: str) -> None:
    """
    Presses a keyboard key

    Args:
      key_code (str): All keys in vk_codes dict are valid
    """
    if keyboard._lookup(key_code) != False:
      key_code = keyboard._lookup(key_code)
    elif key_code not in keyboard.vk_codes.values():
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    x = keyboard.INPUT(
      type=keyboard.INPUT_KEYBOARD,
      ki=KEYBDINPUT(wVk=key_code)
    )
    keyboard.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  def releaseKey(key_code: str) -> None:
    """
    Releases a keyboard key

    Args:
      key_code (str): All keys in vk_codes dict are valid
    """
    if keyboard._lookup(key_code) != False:
      key_code = keyboard._lookup(key_code)
    elif key_code not in keyboard.vk_codes.values():
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    x = keyboard.INPUT(
      type=keyboard.INPUT_KEYBOARD,
      ki=KEYBDINPUT(
        wVk=key_code,
        dwFlags=keyboard.KEYEVENTF_KEYUP
      )
    )
    keyboard.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

  def pressAndReleaseKey(key_code: str) -> None:
    """
    Presses and releases a keyboard key sequentially

    Args:
      key_code (str): All keys in vk_codes dict are valid
    """
    if keyboard._lookup(key_code) != False:
      key_code = keyboard._lookup(key_code)
    elif key_code not in keyboard.vk_codes.values():
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    keyboard.pressKey(key_code)
    time.sleep(0.25)
    keyboard.releaseKey(key_code)

  def pressAndReleaseMouse(mouse_button: str) -> None:
    """
    Presses and releases a mouse button sequentially

    Args:
      mouse_button (str): The button to press accepted: (
        left_mouse,
        right_mouse,
        middle_mouse,
        mouse_button1,
        mouse_button
      )
    """
    mouse_button_list = ["left_mouse", "right_mouse", "middle_mouse", "mouse_button1", "mouse_button2"]
    if mouse_button not in mouse_button_list:
      vars.error(error_type='r', runtime_error='given key code is not a mouse button')
      return vars.exit_code
    original_name = mouse_button  # Keeps the original string before reassignment
    if keyboard._lookup(mouse_button) != False:
      mouse_button = keyboard._lookup(mouse_button)
    elif mouse_button not in keyboard.vk_codes:
      vars.error(error_type='r', runtime_error='given key code is not valid')
      return vars.exit_code
    keyboard.pressMouse(original_name)
    time.sleep(0.25)
    keyboard.releaseMouse(original_name)

  def keyboardWrite(string: str) -> None:
    """
    Writes by sending virtual inputs

    Args:
      string (str): All keys in the 'Alphanumerical' section of vk_codes dict are valid
    """
    str_list = list(string)
    shift_alternate = [
      '|', '~', '?', ':', '{', '}', '\"', '!', '@',
      '#', '$', '%', '^', '&', '*', '(', ')', '+',
      '<', '>', '_'
    ]
    for char in str_list:
      if char not in keyboard.vk_codes and not char.isupper():
        vars.error(error_type='r', runtime_error=f'character: {char} is not in vk_codes map')
        return vars.exit_code
      if char.isupper() or char in shift_alternate:
        keyboard.pressKey('shift')
      else:
        keyboard.releaseKey('shift')
      key_code = keyboard._lookup(char.lower())  # All dict entry's all lowercase
      x = keyboard.INPUT(
        type=keyboard.INPUT_KEYBOARD,
        ki=KEYBDINPUT(wVk=key_code)
      )
      keyboard.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

      y = keyboard.INPUT(
        type=keyboard.INPUT_KEYBOARD,
        ki=KEYBDINPUT(
          wVk=key_code,
          dwFlags=keyboard.KEYEVENTF_KEYUP
        )
      )
      keyboard.user32.SendInput(1, ctypes.byref(y), ctypes.sizeof(y))
    keyboard.releaseKey('shift')  # Incase it is not already released

  @staticmethod
  def altTab() -> None:
    """
    My development test function, just opens alt-tab menu
    """
    keyboard.pressKey(keyboard.vk_codes['alt'])
    keyboard.pressKey(keyboard.vk_codes['tab'])
    keyboard.releaseKey(keyboard.vk_codes['tab'])
    time.sleep(2)
    keyboard.releaseKey(keyboard.vk_codes['alt'])


class color:
  """
  Alter's the consoles color using windows color codes

  ------------------------------
  |    variable    function    |
  |----------------------------|
  | black: var(0)    BLACK()   |
  | blue: var(1)     BLUE()    |
  | green: var(2)    GREEN()   |
  | aqua: var(3)     AQUA()    |
  | red: var(4)      RED()     |
  | purple: var(5)   PURPLE()  |
  | yellow: var(6)   YELLOW()  |
  | white: var(7)    WHITE()   |
  | grey: var(8)     GREY()    |
  ------------------------------
  """

  if 'linux' in vars.platform and vars.DEV_MODE == False:
    print("\n------------------------------------------------ \
    \nTHIS CLASS IS ONLY COMPATIBLE WITH WINDOWS. \
    \nSOME ISSUES MAY BE ENCOUNTERED, ABORTING... \
    \n------------------------------------------------")
    sys.exit(1)

  black = str(0)
  blue = str(1)
  green = str(2)
  aqua = str(3)
  red = str(4)
  purple = str(5)
  yellow = str(6)
  white = str(7)
  grey = str(8)

  # All color reassigns return an empty string, so they can be concatenated
  def BLACK(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.black)}')
    else:
      os.system(f'Color {str(color.black)}0')
    return ''

  def BLUE(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.blue)}')
    else:
      os.system(f'Color {str(color.blue)}0')
    return ''

  def GREEN(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.green)}')
    else:
      os.system(f'Color {str(color.green)}0')
    return ''

  def AQUA(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.aqua)}')
    else:
      os.system(f'Color {str(color.aqua)}0')
    return ''

  def RED(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.red)}')
    else:
      os.system(f'Color {str(color.red)}0')
    return ''

  def PURPLE(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.purple)}')
    else:
      os.system(f'Color {str(color.purple)}0')
    return ''

  def YELLOW(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.yellow)}')
    else:
      os.system(f'Color {str(color.yellow)}0')
    return ''

  def WHITE(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.white)}')
    else:
      os.system(f'Color {str(color.white)}0')
    return ''

  def GREY(fore: bool = True) -> str:
    if not isinstance(fore, bool):
      vars.error(error_type='p', var='fore', type='boolean')
      return vars.exit_code
    if fore:
      os.system(f'Color {str(color.grey)}')
    else:
      os.system(f'Color {str(color.grey)}0')
    return ''

  @staticmethod
  def resetAll() -> str:
    os.system(f'Color {color.black}{color.white}')
    return ''

  @staticmethod
  def clearLine() -> str:
    clearANSI = '\x1b[2K'
    print(clearANSI, end='')
    return ''

  @staticmethod
  def clear() -> str:
    os.system('cls')
    return ''


class funcs:
  """
  The main functions class with helper functions
  for curses all functions are listed below.

  -------------------------------------------------
  |       id        name        doc-string        |
  |-----------------------------------------------|
  | ( 1 ) __init__: Initializes screen            |
  | ( 2 ) setup: Setup and return the screen      |
  | ( 3 ) exit: Exit and restore the console      |
  | ( 4 ) write: Write text to the screen         |
  | ( 5 ) slowWrite: Writes the text slowly       |
  | ( 6 ) centeredWrite: Write centered text      |
  | ( 7 ) hideInput: Hides the users input        |
  | ( 8 ) EZmenu: Outputs an interactive menu     |
  | ( 9 ) maxSize: Gets the X and Y of screen     |
  -------------------------------------------------
  """

  def __init__(self) -> None:
    """
    Initializes screen for functions
    """
    self.scr = curses.initscr()
    self.scr.keypad(True)
    self.scr.clear()
    curses.cbreak()

  @staticmethod
  def setup() -> _curses.window:
    """
    Set up the screen

    Returns:
      _curses.window: A new screen object
    """
    scr = curses.initscr()
    curses.cbreak()
    scr.keypad(True)
    scr.clear()
    return scr

  @staticmethod
  def exit() -> None:
    """
    Safely exits and restore terminal to initial settings
    """
    curses.endwin()

  def write(scr: _curses.window, msg: str, pos: tuple = (0, 0)) -> None:
    """
    Write a message to the screen, window or pad at a position

    Args:
      scr (_curses.window): The screen object
      msg (str): The message to write
      pos (tuple): The position to write the message in, default (0, 0)
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(msg, str):
      vars.error(error_type='p', var='msg', type='string')
      return vars.exit_code
    if not isinstance(pos, tuple):
      vars.error(error_type='p', var='pos', type='tuple')
      return vars.exit_code
    scr.addstr(int(pos[1]), int(pos[0]), msg)
    scr.refresh()

  def slowWrite(scr: _curses.window, text: str, pause: int = 20) -> None:
    """
    Wrapper for curses.addstr() which writes the text slowly

    Args:
      scr (_curses.window): The screen object
      text (str): Text to output
      pause (int): Time to pause
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(text, str):
      vars.error(error_type='p', var='text', type='string')
      return vars.exit_code
    if not isinstance(pause, int):
      vars.error(error_type='p', var='pause', type='integer')
      return vars.exit_code
    for i in range(len(text)):
      scr.addstr(text[i])
      scr.refresh()
      curses.napms(pause)  # Waits the duration of pause in milliseconds

  def centeredWrite(scr: _curses.window, text: str) -> None:
    """
    Writes to the current line but centers the text

    Args:
      scr (_curses.window): The screen object
      text (str): The text to display
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(text, str):
      vars.error(error_type='p', var='text', type='string')
      return vars.exit_code
    width = scr.getmaxyx()[1]
    scr.move(scr.getyx()[0], int(width / 2 - len(text) / 2))
    scr.addstr(text)
    scr.refresh()

  def hideInput(scr: _curses.window, hide_char: str = '*') -> str:
    """
    Hides user's input behind the hide_char symbol and returns string

    Args:
      scr (_curses.window): The screen object
      hide_char (str): A char type string that hides user's input

    Returns:
      str: The string of the hidden input
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(hide_char, str):
      vars.error(error_type='p', var='hide_char', type='string')
      return vars.exit_code
    if not len(hide_char) == 1:
      vars.error('r', runtime_error='variable hide_char is not a char type')

    in_char = 0
    in_str = ''
    curses.noecho()
    mask = str(hide_char)
    if 'linux' in vars.platform:
      NEWLINE = 10  # ASCII integer equal to '\n'
      BACKSPACE = 127  # ASCII integer equal to backspace
    else:  # KEY_MAP is only for windows
      NEWLINE = KEY_MAP['ENTER']
      BACKSPACE = KEY_MAP['BACKSPACE']

    while in_char != NEWLINE:
      in_char = scr.getch()
      # Backspace exception
      if in_char == BACKSPACE:
        if len(in_str) > 0:
          in_str = in_str[:-1]
          cur = scr.getyx()
          scr.move(cur[0], cur[1] - 1)
          scr.clrtobot()
        else:
          continue
      elif in_char > 255:
        continue
      # Output the character
      elif in_char != NEWLINE:
        in_str += chr(in_char)
        if len(hide_char) != 0:
          scr.addch(mask)
        else:
          scr.addch(in_char)
    return in_str

  def cursorBlink(scr: _curses.window, duration: int) -> None:
    """
    Blinks the cursor twice every second

    Args:
      scr (_curses.window): The curses screen object
      duration (int): The amount of seconds to blink
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(duration, int):
      vars.error(error_type='p', var='duration', type='integer')
      return vars.exit_code
    for i in range(duration):
      curses.curs_set(1)
      time.sleep(0.5)
      curses.curs_set(0)
      time.sleep(0.5)

  def EZmenu(scr: _curses.window, menu_items: list) -> str:
    """
    Displays an interactive menu and returns selected item

    Args:
      scr (_curses.window): The screen object
      menu_items (list): The list of menu options

    Returns:
      str: The selected menu item
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    if not isinstance(menu_items, list):
      vars.error(error_type='p', var='menu_items', type='list')
      return vars.exit_code
    scr.clear()
    h, w = scr.getmaxyx()

    def printMenu(selected_row: int, list: list):
      for item in list:
        index = list.index(item)
        x = int(w / 2 - len(item) / 2)
        y = int(h / 2 - len(list) / 2 + index)
        if index == selected_row:
          scr.addstr(y, x, item, curses.A_STANDOUT)
        else:
          scr.addstr(y, x, item)
      scr.refresh()

    curses.curs_set(0)
    current_row = 0
    printMenu(current_row, menu_items)
    loop = True

    while loop == True:
      key = scr.getch()
      scr.clear()

      if key == curses.KEY_UP and current_row > 0:
        current_row -= 1
      elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
        current_row += 1
      elif key in [10, 13]:
        selected = menu_items[current_row]
        break

      printMenu(current_row, menu_items)
    return selected

  def upperInput(scr: _curses.window, hidden: bool = False, can_newline: bool = True) -> str:
    """
    Reads user input until enter key is pressed. Echoes the input in upper case

    Args:
      hidden (bool): If 'True' the output will be masked
      can_newline (bool): If 'True' the input is followed by a newline and the screen is scrolled if necessary

    Returns:
      str: The recorded input as a string
    """

    if 'linux' in vars.platform:
      NEWLINE = 10  # ASCII integer equal to '\n'
      BACKSPACE = 127  # ASCII integer equal to backspace
    else:  # KEY_MAP is only for windows
      NEWLINE = KEY_MAP['ENTER']
      BACKSPACE = KEY_MAP['BACKSPACE']

    curses.noecho()
    char_mask = '*'
    inchar = 0
    instr = ""
    while inchar != NEWLINE:
      inchar = scr.getch()
      # convert lower case to upper
      if inchar > 96 and inchar < 123:
        inchar -= 32
      # deal with backspace
      if inchar == BACKSPACE:
        if len(instr) > 0:
          instr = instr[:-1]
          cur = scr.getyx()
          scr.move(cur[0], cur[1] - 1)
          scr.clrtobot()
        else:
          continue
      elif inchar > 255:
        continue
      # output the character
      elif inchar != NEWLINE:
        instr += chr(inchar)
        if hidden:
          scr.addch(char_mask)
        else:
          scr.addch(inchar)
      elif can_newline:
        scr.addch(NEWLINE)
    else:
      funcs.exit()

    return instr

  def maxSize(scr: _curses.window) -> tuple:
    """
    Returns the width and height of the screen

    Args:
      scr (_curses.window): The screen object

    Returns:
      tuple: The windows height and width (h, w)
    """
    if not isinstance(scr, _curses.window):
      vars.error(error_type='p', var='scr', type='curses window object')
      return vars.exit_code
    height, width = scr.getmaxyx()
    return height, width
