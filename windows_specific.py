"""Windows-specific functions and variables for input_no_newline."""
import ctypes
from msvcrt import getwch  # pylint: disable=import-error, unused-import
from shared_stuff import ANSI

try:
    import colorama  # pylint: disable=import-error
except ImportError:
    kernel32 = ctypes.windll.kernel32
    # Enable ANSI support
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
else:
    colorama.init()


def get_clipboard_data():
    """Return string previously copied from Windows clipboard.

    Adapted from <http://stackoverflow.com/a/23285159/6379747>.
    """
    CF_TEXT = 1
    user32 = ctypes.windll.user32
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            kernel32.GlobalUnlock(data_locked)
    finally:
        user32.CloseClipboard()
    return text.value


def sigtstp():
    """Raise EOFError from Ctrl-Z since SIGTSTP doesn't exist."""
    raise EOFError


input_code = {
    **ANSI,
    'CSI': [['\xe0', '\x00'], ''],
    'up': 'H',
    'down': 'P',
    'right': 'M',
    'left': 'K',
    'end': 'O',
    'home': 'G',
    'backspace': '\b',
    'del': 'S',
    }
