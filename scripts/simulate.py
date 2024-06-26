# Standard library imports
import argparse

from time import sleep

# KeyMaster imports
from classes.key_collector import KeyLogger
from classes.key_generator import KeyGenerator
from utils.validation import KeystrokeList
from utils.helpers import clean_string
from utils.settings import DEFAULT_DISABLE_SIMULATION, DEFAULT_LOGGING, DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, DEFAULT_STRING, DEFAULT_SIM_INITIAL_LAG

PRINT_KEYS = False


def listen_for_keystrokes(logger: KeyLogger) -> KeystrokeList:
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
        return KeystrokeList()


def simulate_keystrokes(
        keystrokes: KeystrokeList,
        disable=DEFAULT_DISABLE_SIMULATION,
        allow_newlines=DEFAULT_ALLOW_NEWLINES,
        allow_unicode=DEFAULT_ALLOW_UNICODE) -> None:
    """
    Test the KeyGenerator class by simulating keystrokes from a string.
    """
    simulator = KeyGenerator(
        disable=disable,
        allow_newlines=allow_newlines,
        allow_unicode=allow_unicode)
    simulator.simulate_keystrokes(keystrokes)


def keystrokes_from_string(
        input_string: str,
        allow_newlines=DEFAULT_ALLOW_NEWLINES,
        allow_unicode=DEFAULT_ALLOW_UNICODE) -> KeystrokeList:
    keystrokes = KeystrokeList()
    if not input_string:
        print("No input string provided.")
        return keystrokes
    simulator = KeyGenerator(
        disable=True,
        allow_newlines=allow_newlines,
        allow_unicode=allow_unicode)
    keystrokes = simulator.keystrokes_from_string(input_string)
    if keystrokes.is_empty():
        print("No keystrokes found.")
        return keystrokes
    return keystrokes


def validate_and_save_keystrokes(
        keystrokes: KeystrokeList,
        input_string: str) -> bool:
    logger = KeyLogger('SIM')
    legit = logger.is_loggable(keystrokes, input_string)
    if legit:
        log_string = input_string
    else:
        print("Using keystrokes instead of input string.")
        log_string = keystrokes.to_string()
    logger.set_internal_log(keystrokes, log_string)
    return logger.save_log()


def listen_main(
        # NOTE: Default initial lag is hardcoded to 5s for now
        disable=DEFAULT_DISABLE_SIMULATION,
        logging=DEFAULT_LOGGING,
        allow_newlines=DEFAULT_ALLOW_NEWLINES,
        allow_unicode=DEFAULT_ALLOW_UNICODE,
        initial_lag: int | float = 3) -> None:
    logger = KeyLogger()
    keystrokes = listen_for_keystrokes(logger)
    if keystrokes.is_empty():
        print("No keystrokes found.")
        return
    if PRINT_KEYS:
        print(keystrokes)
    if logging:
        logger.save_log()
    if disable:
        print("Simulation disabled.")
        return

    print(f"Starting simulation in {initial_lag} seconds...")
    sleep(initial_lag)
    simulate_keystrokes(keystrokes, disable, allow_newlines, allow_unicode)


def simulate_from_string(
        input_string: str,
        disable=DEFAULT_DISABLE_SIMULATION,
        logging=DEFAULT_LOGGING,
        allow_newlines=DEFAULT_ALLOW_NEWLINES,
        allow_unicode=DEFAULT_ALLOW_UNICODE,
        initial_lag=float(DEFAULT_SIM_INITIAL_LAG)) -> None:
    if not input_string:
        print("No input string provided.")
        return
    keystrokes = keystrokes_from_string(
        input_string, allow_newlines, allow_unicode)
    if logging:
        saved = validate_and_save_keystrokes(keystrokes, input_string)
        if not saved:
            print("Did not save to logfile.")
    if disable:
        print("Simulation disabled.")
        return
    if keystrokes.is_empty():
        print("No keystrokes found.")
        return
    print(f"Starting simulation in {initial_lag} seconds...")
    sleep(initial_lag)
    simulate_keystrokes(keystrokes, disable, allow_newlines, allow_unicode)


def clipboard_main(
        # NOTE: Default initial lag is hardcoded to 0.5s for now
        disable=DEFAULT_DISABLE_SIMULATION,
        logging=DEFAULT_LOGGING,
        allow_newlines=DEFAULT_ALLOW_NEWLINES,
        allow_unicode=DEFAULT_ALLOW_UNICODE,
        initial_lag=0.5) -> None:
    from pyperclip import paste as py_paste  # type: ignore
    clipboard_contents = py_paste()
    if not clipboard_contents:
        print("No text found in clipboard.")
        return None
    input_string = clipboard_contents
    if not allow_unicode:
        print("Removing non-ASCII characters from clipboard contents.")
        print(f"Clipboard contents: {input_string[:5]}[?...]")
        input_string = clean_string(input_string)
    if not input_string:
        print("No valid string found in clipboard.")
        return
    simulate_from_string(
        input_string,
        disable,
        logging,
        allow_newlines,
        allow_unicode,
        initial_lag)

# UI-less Shortcuts integration.
# Create a keyboard shortcut to run shell script `python -m
# scripts.simulate.py -c`


def main():
    parser = argparse.ArgumentParser()
    # Add flag
    parser.add_argument(
        "--disable",
        "-d",
        default=DEFAULT_DISABLE_SIMULATION,
        action='store_true',
        help="Disable simulation")
    parser.add_argument(
        "--no-log",
        "-n",
        default=not (DEFAULT_LOGGING),
        action='store_true',
        help="Disable logging")
    parser.add_argument(
        "--no-newlines",
        "-nn",
        default=not (DEFAULT_ALLOW_NEWLINES),
        action='store_true',
        help="Disable simulating newlines")
    parser.add_argument(
        "--no-unicode",
        "-nu",
        default=not (DEFAULT_ALLOW_UNICODE),
        action='store_true',
        help="Disable simulating unicode")

    # Choose script to run
    parser.add_argument(
        "--clipboard",
        "-c",
        action='store_true',
        help="Use clipboard as input")
    parser.add_argument(
        "--listen",
        "-l",
        action='store_true',
        help="Listen for input")
    parser.add_argument(
        "--string",
        "-s",
        default=DEFAULT_STRING,
        help="The string to simulate")

    args = parser.parse_args()

    disable = args.disable
    logging = not (args.no_log)
    allow_newlines = not (args.no_newlines)
    allow_unicode = not (args.no_unicode)
    input_string = args.string

    if disable:
        print("Simulation OFF.")
    if logging:
        print("Logging ON.")
    else:
        print("Logging OFF.")
    if allow_newlines:
        print("Simulating newlines ON.")
    if not allow_unicode:
        print("Simulating unicode OFF.")
    if input_string != DEFAULT_STRING:
        print(f"Input string: {input_string[:5]} [+]")
    if args.clipboard:
        clipboard_main(disable, logging, allow_newlines, allow_unicode)
    elif args.listen:
        listen_main(disable, logging, allow_newlines, allow_unicode)
    else:
        simulate_from_string(
            input_string,
            disable,
            logging,
            allow_newlines,
            allow_unicode)


if __name__ == "__main__":
    main()
