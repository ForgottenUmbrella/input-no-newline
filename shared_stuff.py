"""Provide platform-independent functions and variables."""
ANSI = {
    'CSI': '\x1b[',
    'up': 'A',
    'down': 'B',
    'right': 'C',
    'left': 'D',
    'end': 'F',
    'home': 'H',
    'enter': '\r',
    '^C': '\x03',
    '^D': '\x04',
    '^V': '\x16',
    '^Z': '\x1a',
    }


def move_cursor(direction, count=1):
    """Move the text cursor 'count' times in the specified direction."""
    if direction not in ['up', 'down', 'right', 'left']:
        raise ValueError("direction should be either 'up', 'down', 'right' "
                         "or 'left'")
    # A 'count' of zero still moves the cursor, so this needs to be
    # tested for.
    if count != 0:
        print(ANSI['CSI'] + str(count) + ANSI[direction], end='', flush=True)


def line_insert(text, extra=''):
    """Insert text between terminal line and reposition cursor."""
    if not extra:
    # It's not guaranteed that the new line will completely overshadow
    # the old one if there is no extra. Maybe something was 'deleted'?
        move_cursor('right', len(text) + 1)
        print('\b \b' * (len(text)+1), end='', flush=True)
    print(extra + text, end='', flush=True)
    move_cursor('left', len(text))
