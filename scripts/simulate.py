# Standard library imports
from time import sleep
from typing import List

# KeyMaster imports
from classes.keyLogger import KeyLogger
from classes.keySimulator import KeySimulator
from utils.config import ABSOLUTE_SIM_FILEPATH
from utils.validation import Keystroke, clean_string, keystrokes_to_string

VALIDATE_STRING = True

LOGGING_DEFAULT = True
PRINT_KEYS = False
DEFAULT_STRING = "hey look ma, it's a simulation!"
ALLOW_UNICODE = True

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
    if legit:
        log_string = input_string
    else:
        print("Using keystrokes instead of input string.")
        log_string = keystrokes_to_string(keystrokes)
    logger.set_internal_log(keystrokes, log_string)
    return logger.save_log()

def listen_main(disable=False, logging = LOGGING_DEFAULT) -> None:
    keystrokes = []
    logger = KeyLogger()
    keystrokes = listen_for_keystrokes(logger)
    if not keystrokes:
        print("No keystrokes found.")
        return
    if PRINT_KEYS:
        print(keystrokes)
    if logging:
        logger.save_log()
    if disable:
        print("Simulation disabled.")
        return

    print("Starting simulation in 5 seconds...")
    sleep(5)
    simulate_keystrokes(keystrokes)

def simulate_from_string(input_string: str, disable = False, logging = LOGGING_DEFAULT) -> None:
    keystrokes = generate_keystrokes_from_string(input_string)
    if not keystrokes:
        print("No keystrokes found.")
        return
    if logging:
        saved = validate_and_save_keystrokes(keystrokes, input_string)
        if not saved:
            print("Did not save to logfile.")
    if disable:
        print("Simulation disabled.")
        return
    simulate_keystrokes(keystrokes)

def clipboard_main(disable = False, logging = LOGGING_DEFAULT) -> None:
    from pyperclip import paste as py_paste # type: ignore
    clipboard_contents = py_paste()
    if not clipboard_contents:
        print("No text found in clipboard.")
        return None
    if ALLOW_UNICODE:
        input_string = clipboard_contents
    else:
        input_string = clean_string(clipboard_contents)
    simulate_from_string(input_string, disable, logging)

### UI-less Shortcuts integration.
# Create a keyboard shortcut to run shell script `python -m scripts.simulate.py -c`
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Add logging flag
    parser.add_argument("--no-log", "-n", default=False, action='store_true', help="Disable logging")
    parser.add_argument("--disable", "-d", default=False, action='store_true', help="Disable simulation")
    parser.add_argument("--clipboard", "-c", action='store_true', help="Use clipboard as input")
    parser.add_argument("--listen", "-l", action='store_true', help="Listen for input")
    parser.add_argument("--string", "-s", default=DEFAULT_STRING, help="The string to simulate")

    args = parser.parse_args()

    logging = not(args.no_log)
    disable = args.disable
    input_string = args.string
    if logging:
        print("Logging ON.")
    else:
        print("Logging OFF.")
    if disable:
        print("Simulation OFF.")
    
    if args.clipboard:
        clipboard_main(disable, logging)
    elif args.listen:
        listen_main(disable, logging)
    else:
        simulate_from_string(input_string, disable, logging)
