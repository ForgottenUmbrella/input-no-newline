# Input no newline
An implementation of the built-in `input` function that doesn't echo the final
newline character on Enter keypress. This is a repo showcasing my [answer on
StackExchange](http://stackoverflow.com/a/41459565/6379747).

## Functionality
* Handles backspaces and forward deletes
* Handles the Home and End keys to navigate to the beginning and end of
responses
* Handles arrow key navigation
* Handles line history (may be broken)
* Support for Windows, Linux and maybe macOS
* Paste support
* KeyboardInterrupts, EOFErrors and SIGSTPs are raised on certain keypresses
(e.g. Ctrl-C) as expected

All of this was done _without_ the help of PyPy, the Python interpreter written
in Python. I tried to find their implementation of the built-in `input`
function, and I failed, so I had to recreate most of the functionality from
scratch, which was a pain.

A better solution to the problem of getting stuff printed on the same line as
input would be my TerminalHistory repo. Or you could just look through the PyPy
source code yourself and try to create your own function based on it (good luck
with that).

## Usage
    import input_no_newline  # Naming things is hard

    input_no_newline('this is a prompt. proceed? ')
    print('this will be printed on the same line as the previous')

Output:  
    this is a prompt. proceed? foobar this is user inputthis will be printed on
    the same line as the previous


