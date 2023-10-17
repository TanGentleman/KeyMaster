from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH
from keySimulator import KeySimulator
from time import sleep
import string
LOGGING_ON = False

LISTENFIRST = False
PRINT_KEYS = False

DEFAULT_STRING = "hey look ma, \n it's a simulation!"

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


def main(input_string:str, ListenFirst = LISTENFIRST):
    if input_string:
        ListenFirst = False
        if '\n' in input_string:
            print(f"This string has a newline!")
    keystrokes = []
    if ListenFirst:
        print("I will say START in 3 seconds...")
        sleep(3)
        logger = KeyLogger()
        print("START!")
        logger.start_listener()
        if logger.keystrokes:
            keystrokes = logger.keystrokes
            print("STOPPED LISTENING!")
            simulator = KeySimulator()
        else:
            return
    else:
        if input_string is None:
            input_string = DEFAULT_STRING
        simulator = KeySimulator()
        keystrokes = simulator.generate_keystrokes_from_string(input_string)
    if not keystrokes:
        print("No keystrokes found.")
        return
    if ListenFirst:
        print("Starting simulation in 5 seconds...")
        sleep(5)
    simulator.simulate_keystrokes(keystrokes)
    if PRINT_KEYS: print(keystrokes)
    if input_string and LOGGING_ON:
        logger = KeyLogger(ABSOLUTE_SIM_FILEPATH)
        logger.set_internal_log(keystrokes, input_string)
        success = logger.save_log()
        if success:
            print("Successfully saved keystrokes to file.")
        else:
            print("Failed to save keystrokes to file.")
    pass
### This file is used for Shortcuts. For instance, I have a keyboard shortcut to run a shell script `python simulate.py "$(pbpaste)"`
if __name__ == "__main__":
    from sys import argv as args
    length = len(args)
    if length > 1:
        if length > 2:
            # raise error
            raise ValueError("Too many CLI arguments")
        # make sure string is utf-8
        arg_string = args[1]
        if arg_string == 'Test':
            main(None, True)
        elif arg_string == '*Clipboard*':
            import pyperclip
            main(filter_non_typable_chars(pyperclip.paste()))
        else:
            print("Gotta have a valid argument. Try 'Test' or '*Clipboard*'")
            pass
    else:
        input_string = DEFAULT_STRING
        main(input_string)
