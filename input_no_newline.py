#!/usr/bin/python3
"""Provide an input function that doesn't echo a newline."""
try:
    from windows_specific import getwch, get_clipboard_data, sigtstp, input_code
except ImportError:
    from unix_specific import getwch, get_clipboard_data, sigtstp, input_code
try:
    from readline_available import (init_history_index, restore_history,
                                    store_and_replace_history,
                                    handle_prev_history, handle_next_history,
                                    finalise_history)
except ImportError:
    from readline_unavailable import (init_history_index, restore_history,
                                      store_and_replace_history,
                                      handle_prev_history, handle_next_history,
                                      finalise_history)
from shared_stuff import ANSI, move_cursor, line_insert


def input_no_newline(prompt=''):  # pylint: disable=too-many-branches, too-many-statements
    """Echo and return user input, except for the newline."""
    print(prompt, end='', flush=True)
    response = ''
    position = 0
    history_index = init_history_index()
    input_replaced = False
    history_modified = False
    replacements = {}

    while True:
        char = getwch()
        if char in input_code['CSI'][0]:
            char = getwch()
            if char == input_code['CSI'][1]:
                # *NIX uses three characters
                char = getwch()
            if char == input_code['up']:
                (history_index, input_replaced, history_modified) = (
                    handle_prev_history(
                        history_index, response, replacements, input_replaced,
                        history_modified
                        )
                    )
                response = restore_history(history_index, response, position)
                position = len(response)
            elif char == input_code['down']:
                (history_index, input_replaced, history_modified) = (
                    handle_next_history(
                        history_index, response, replacements, input_replaced,
                        history_modified
                        )
                    )
                response = restore_history(history_index, response, position)
                position = len(response)
            elif char == input_code['right'] and position < len(response):
                move_cursor('right')
                position += 1
            elif char == input_code['left'] and position > 0:
                move_cursor('left')
                position -= 1
            elif char == input_code['end']:
                move_cursor('right', len(response) - position)
                position = len(response)
            elif char == input_code['home']:
                move_cursor('left', position)
                position = 0
            elif char == input_code['del'][0]:
                if ''.join(input_code['del']) == '3~':
                    # *NIX uses '\x1b[3~' as its del key code, but only
                    # '\x1b[3' has currently been read from sys.stdin
                    getwch()
                backlog = response[position+1 :]
                response = response[:position] + backlog
                line_insert(backlog)
        elif char == input_code['backspace']:
            if position > 0:
                backlog = response[position:]
                response = response[: position-1] + backlog
                print('\b', end='', flush=True)
                position -= 1
                line_insert(backlog)
        elif char == input_code['^C']:
            raise KeyboardInterrupt
        elif char == input_code['^D']:
            raise EOFError
        elif char == input_code['^V']:
            paste = get_clipboard_data()
            backlog = response[position:]
            response = response[:position] + paste + backlog
            position += len(paste)
            line_insert(backlog, extra=paste)
        elif char == input_code['^Z']:
            sigtstp()
        elif char == input_code['enter']:
            finalise_history(history_index, response, replacements,
                             input_replaced, history_modified)
            move_cursor('right', len(response) - position)
            return response
        else:
            backlog = response[position:]
            response = response[:position] + char + backlog
            position += 1
            line_insert(backlog, extra=char)


def main():
    """Called if script isn't imported."""
    print('Hello, ', end='', flush=True)
    name = input_no_newline()  # pylint: disable=unused-variable
    print(', how do you do?')


if __name__ == '__main__':
    main()
