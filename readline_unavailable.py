"""Provide dummy functions for if readline isn't available."""
# pylint: disable-msg=unused-argument


def init_history_index():
    """Return an index of 1 which probably won't ever change."""
    return 1


def restore_history(history_index, replaced, cursor_position):
    """Return the replaced thing without replacing it."""
    return replaced


def store_and_replace_history(history_index, replacement, old_history):
    """Don't store history."""
    pass


def handle_prev_history(history_index, replaced, old_history,
                        input_replaced, history_modified):
    """Return 'input_replaced' and 'history_modified' without change."""
    return (history_index, input_replaced, history_modified)


def handle_next_history(history_index, replaced, old_history,
                        input_replaced, history_modified):
    """Also return 'input_replaced' and 'history_modified'."""
    return (history_index, input_replaced, history_modified)


def finalise_history(history_index, response, old_history,
                     input_replaced, history_modified):
    """Don't change nonexistent history."""
    pass
