"""Provide functions for up and down arrows if readline is installed."""
try:
    import readline
except ImportError:
    import pyreadline as readline
from shared_stuff import move_cursor


def init_history_index():
    """Return index for last element of readline.get_history_item."""
    # One-based index
    return readline.get_current_history_length() + 1


def restore_history(history_index, replaced, cursor_position):
    """Replace 'replaced' with history and return the replacement."""
    try:
        replacement = readline.get_history_item(history_index)
    except IndexError:
        replacement = None
    if replacement is not None:
        move_cursor('right', len(replaced) - cursor_position)
        print('\b \b' * len(replaced), end='', flush=True)
        print(replacement, end='', flush=True)
        return replacement
    return replaced


def store_and_replace_history(history_index, replacement, old_history):
    """Store history and then replace it."""
    old_history[history_index] = readline.get_history_item(history_index)
    try:
        readline.replace_history_item(history_index - 1, replacement)
    except AttributeError:
    # pyreadline is incomplete
        pass


def handle_prev_history(history_index, replaced, old_history,
                        input_replaced, history_modified):
    """Handle some up-arrow logic."""
    try:
        history = readline.get_history_item(history_index - 1)
    except IndexError:
        history = None
    if history is not None:
        if history_index > readline.get_current_history_length():
            readline.add_history(replaced)
            input_replaced = True
        else:
            store_and_replace_history(
                history_index, replaced, old_history)
            history_modified = True
        history_index -= 1
    return (history_index, input_replaced, history_modified)


def handle_next_history(history_index, replaced, old_history,
                        input_replaced, history_modified):
    """Handle some down-arrow logic."""
    try:
        history = readline.get_history_item(history_index + 1)
    except IndexError:
        history = None
    if history is not None:
        store_and_replace_history(history_index, replaced, old_history)
        history_modified = True
        history_index += 1
        input_replaced = (not history_index
                            == readline.get_current_history_length())
    return (history_index, input_replaced, history_modified)


def finalise_history(history_index, response, old_history,
                     input_replaced, history_modified):
    """Change history before the response will be returned elsewhere."""
    try:
        if input_replaced:
            readline.remove_history_item(history_index - 1)
        elif history_modified:
            readline.remove_history_item(history_index - 1)
            readline.add_history(old_history[history_index - 1])
    except AttributeError:
    # pyreadline is also missing remove_history_item
        pass
    readline.add_history(response)
