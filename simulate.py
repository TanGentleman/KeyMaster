from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH
from keySimulator import KeySimulator
from time import sleep
import string
from typing import Optional

LOGGING_ON = True
LISTENFIRST = False
PRINT_KEYS = False

DEFAULT_STRING = "hey look ma, it's a simulation!"

def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    """
    print(input_string)
    # Define specific replacements
    
    replacements = {
        '\u2028': '\n',  # replace line separator with newline
        # '\u2029': '\n',  # replace paragraph separator with newline
        # add more replacements here if needed
    }
    typable_chars = string.ascii_letters + string.digits + string.punctuation + ' \n\t'
    for c in input_string:
        if c not in typable_chars:
            print(f"Non-typable character:{c}-> {ord(c)}")
    for old, new in replacements.items():
        input_string = input_string.replace(old, new)
    # Filter out non-typable characters
    filtered_string = ''.join(c for c in input_string if c in typable_chars)
    # filtered_string = "test :("
    return filtered_string


def main(input_string: Optional[str] = DEFAULT_STRING, listen_first: bool = LISTENFIRST) -> None:
    """
    This function simulates keystrokes based on the input_string or listens for keystrokes if listen_first is True.
    """
    keystrokes = []
    logger = KeyLogger() if listen_first else KeyLogger(ABSOLUTE_SIM_FILEPATH)
    simulator = KeySimulator()

    if listen_first:
        print("I will say START in 3 seconds...")
        sleep(3)
        print("START!")
        logger.start_listener()
        if logger.keystrokes:
            keystrokes = logger.keystrokes
        else:
            return
    else:
        if input_string is None:
            print("No input string found, and ListenFirst is False")
            return
        if '\n' in input_string:
            print(f"This string has a newline!")
        keystrokes = simulator.generate_keystrokes_from_string(input_string)

    if not keystrokes:
        print("No keystrokes found.")
        return

    if listen_first:
        print("Starting simulation in 5 seconds...")
        sleep(5)

    simulator.simulate_keystrokes(keystrokes)

    if PRINT_KEYS: 
        print(keystrokes)

    if LOGGING_ON:
        if listen_first:
            logger.save_log()
        else:
            if input_string:
                logger.set_internal_log(keystrokes, input_string)
                logger.save_log()

### This supports no-UI Shortcuts integration.
# Create a keyboard shortcut to run a shell script `python simulate.py "*Clipboard*"`
if __name__ == "__main__":
    from sys import argv as args
    length = len(args)
    if length > 1:
        if length > 2:
            raise ValueError("Too many CLI arguments")
        arg_string = args[1]
        if arg_string == 'Test':
            main(None, True)
        elif arg_string == '*Clipboard*':
            from pyperclip import paste as py_paste # type: ignore
            main(filter_non_typable_chars(py_paste()))
        else:
            print("Gotta have a valid argument. Try 'Test' or '*Clipboard*'")
            pass
    else:
        input_string = DEFAULT_STRING
        main(input_string)
