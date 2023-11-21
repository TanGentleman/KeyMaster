from torch import log_
from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH
from validation import clean_string, Keystroke
from keySimulator import KeySimulator
from time import sleep
from typing import List

LOGGING_ON = True
PRINT_KEYS = False
DEFAULT_STRING = "hey look ma, it's a simulation!"

ALLOW_UNICODE = True

VALIDATE_WITH_PARSER = True
if VALIDATE_WITH_PARSER:
	from keyParser import KeyParser

def listen_for_keystrokes(logger: KeyLogger) -> List[Keystroke] | None:
    """
    Test the KeyLogger class by listening for keystrokes.
    """
    print("I will say START in 3 seconds...")
    sleep(3)
    print("START!")
    logger.start_listener()
    if logger.keystrokes:
        keystrokes = logger.keystrokes
        return keystrokes
    else:
        return None

def simulate_keystrokes(keystrokes: List[Keystroke]) -> None:
    """
    Test the KeySimulator class by simulating keystrokes from a string.
    """
    simulator = KeySimulator()
    simulator.simulate_keystrokes(keystrokes)

def generate_keystrokes_from_string(input_string: str) -> List[Keystroke] | None:
    if not input_string:
        print("No input string provided.")
        return None
    simulator = KeySimulator(disabled=True)
    keystrokes = simulator.generate_keystrokes_from_string(input_string)
    if not keystrokes:
        print("No keystrokes found.")
        return None
    return keystrokes

def validate_and_save_keystrokes(keystrokes: List[Keystroke], input_string: str) -> bool:
    logger = KeyLogger(ABSOLUTE_SIM_FILEPATH)
    legit = logger.is_log_legit(keystrokes, input_string)
    if not legit:
        if VALIDATE_WITH_PARSER and KeyParser is not None:
            print("Replacing string with keystroke validated copy for log!")
            parser = KeyParser(None)
            log_string = parser.keystrokes_to_string(keystrokes)
        else:
            print("WARNING: Internal log may not match keystrokes!")
            log_string = input_string
    log_string = input_string
    logger.set_internal_log(keystrokes, log_string)
    return logger.save_log()

def listen_main() -> None:
    keystrokes = []
    logger = KeyLogger()
    keystrokes = listen_for_keystrokes(logger)
    if not keystrokes:
        print("No keystrokes found.")
        return
    print("Starting simulation in 5 seconds...")
    sleep(5)

    if PRINT_KEYS:
        print(keystrokes)
    if LOGGING_ON:
        logger.save_log()

def simulate_from_string(input_string: str) -> None:
    keystrokes = generate_keystrokes_from_string(input_string)
    if not keystrokes:
        print("No keystrokes found.")
        return
    simulate_keystrokes(keystrokes)
    if LOGGING_ON:
        saved = validate_and_save_keystrokes(keystrokes, input_string)
        if not saved:
            print("Did not save to logfile.")

def clipboard_main() -> None:
    from pyperclip import paste as py_paste # type: ignore
    clipboard_contents = py_paste()
    if not clipboard_contents:
        print("No text found in clipboard.")
        return None
    if ALLOW_UNICODE:
        input_string = clipboard_contents
    else:
        input_string = clean_string(clipboard_contents)
    simulate_from_string(input_string)
### This supports no-UI Shortcuts integration.
# Create a keyboard shortcut to run a shell script `python simulate.py "*Clipboard*"`
if __name__ == "__main__":
    from sys import argv as args
    length = len(args)
    if length > 1:
        if length > 2:
            raise ValueError("Too many CLI arguments")
        arg_string = args[1]
        if arg_string == 'listen':
            listen_main()
        elif arg_string == '*Clipboard*':
            clipboard_main()
        else:
            print("Gotta have a valid argument. Try 'Test' or '*Clipboard*'")
            pass
    else:
        simulate_from_string(DEFAULT_STRING)