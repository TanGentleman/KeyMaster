from keyLogger import KeyLogger
from config import ABSOLUTE_SIM_FILEPATH
from keySimulator import KeySimulator
LOGGING_ON = False

LISTENFIRST = False
from time import sleep

DEFAULT_STRING = "hey look ma, a simulation!"
def main(input_string, ListenFirst = LISTENFIRST):
    if input_string:
        ListenFirst = False
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
    print(keystrokes)
    if LOGGING_ON:
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
        if args[1] == 'Test':
            main(None, True)
        else:
            input_string = args[1]
            main(input_string)
    else:
        input_string = DEFAULT_STRING
        main(input_string)
