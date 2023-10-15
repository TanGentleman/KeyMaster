from keySimulator import main as simulate
from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH

LOGGING_ON = True

### This file is used for Shortcuts. For instance, I have a keyboard shortcut to run a shell script `python simulate.py "$(pbpaste)"`
if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if length > 1:
        input_string = sys.argv[1]
        keys = simulate(input_string)
        if LOGGING_ON:
            logger = KeyLogger(ABSOLUTE_SIM_FILEPATH)
            logger.set_internal_log(keys, input_string)
            success = logger.save_log()
            if success:
                print("Successfully saved keystrokes to file.")
            else:
                print("Failed to save keystrokes to file.")
    else:
        keys = simulate()
