from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH
from validation import clean_string
from keySimulator import KeySimulator
from time import sleep

LOGGING_ON = True
LISTENFIRST = False
PRINT_KEYS = False
DEFAULT_STRING = "hey look ma, it's a simulation!"

## RINSE TO SIMULATE HUMAN INPUT (Removes unicode characters)
RINSE_STRING = True


def main(listen_first: bool = LISTENFIRST, input_string: str = DEFAULT_STRING) -> None:
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
            print(f"This string contains newlines!")
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
                # WARNING: The internal log may not match! Your clipboard string may be longer.
                logger.set_internal_log(keystrokes, '*CLIPBOARD*:' + input_string)
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
            main(True)
        elif arg_string == '*Clipboard*':
            from pyperclip import paste as py_paste # type: ignore
            if not py_paste():
                print("No text found in clipboard.")
                pass
            else:
                if RINSE_STRING:
                    main(False, clean_string(py_paste()))
                else:
                    main(False, py_paste())
        else:
            print("Gotta have a valid argument. Try 'Test' or '*Clipboard*'")
            pass
    else:
        input_string = DEFAULT_STRING
        main(False, input_string)
