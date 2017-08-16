"""Functions and variables for Debian-based Linux distros and macOS."""
import sys
import os
import tty
import signal
import termios
from shared_stuff import ANSI

def getwch():
    """Return a single character from user input without echoing.

    ActiveState code, adapted from
    <http://code.activestate.com/recipes/134892> by Danny Yoo under
    the Python Software Foundation license.
    """
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(file_descriptor)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return char


def get_clipboard_data():
    """Return nothing; *NIX systems automagically change sys.stdin."""
    return ''


def sigtstp():
    """Suspend the script."""
    os.kill(os.getpid(), signal.SIGTSTP)


input_code = {
    **ANSI,
    'CSI': ['\x1b', '['],
    'backspace': '\x7f',
    'del': ['3', '~'],
    }
