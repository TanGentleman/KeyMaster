from pynput.keyboard import Controller, Key
from time import sleep
import numpy as np
from config import ABSOLUTE_SIM_FILEPATH, Keystroke
from typing import List
### SIMULATION CONFIG ###
DEFAULT_DELAY_MEAN = 0.07
DEFAULT_DELAY_STANDARD_DEVIATION = 0.02
MAX_WORDS = 300
MIN_DELAY = 0.03

LOGGING_ON = True
ALLOW_ENTER_AND_TAB = True

if ALLOW_ENTER_AND_TAB:
    SPECIAL_KEYS = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }
else:
    SPECIAL_KEYS = {' ': Key.space}

def words_from_string(string: str) -> List[str]:
    return string.split()

def simulate_keystrokes(string: str, delay_mean: float, delay_standard_deviation: float) -> List[Keystroke]:
    """
    Simulate keystrokes from a string.

    Args:
        string (str): The string to simulate.
        delay_mean (float): The mean delay between keystrokes.
        delay_standard_deviation (float): The standard deviation of the delay between keystrokes.

    Returns:
        List[Keystroke]: A list of keystrokes.
    """
    keyboard = Controller()
    word_count = 0
    keystrokes: List[Keystroke] = []
    def get_delay(speed_by_multiple: float = 1) -> float:
        # Ensure speed_by_multiple > 0
        if speed_by_multiple is None:
            speed_by_multiple = 1
        elif speed_by_multiple <= 0:
            # ERROR
            raise ValueError(f"Speed by multiple must be greater than 0. Received {speed_by_multiple}")
        delay = np.random.normal(delay_mean/(speed_by_multiple), delay_standard_deviation/speed_by_multiple)
        if delay < MIN_DELAY:
            # print(f"Delay too low: {delay}")
            delay = MIN_DELAY + delay/10
        return delay
    
    for char in string:
        delay1 = get_delay(1)
        delay2 = get_delay(1.5)
        key_as_string = ''
        if word_count == MAX_WORDS:
            print(f"Reached max words: {MAX_WORDS}")
            break
        try:
            sleep(delay1)
            if char in SPECIAL_KEYS:
                special_key = SPECIAL_KEYS[char]
                key_as_string = str(special_key)
                word_count += 1
                keyboard.press(special_key)
                keyboard.release(special_key)
                # Add delay after a special key
                # Or should delay be at the start of its next key?
                sleep(delay2)
            elif char.isprintable():
                key_as_string = char
                keyboard.type(char)
            else:
                continue
        except Exception as e:
            print(f"An error occurred while typing the character: {e}")
            continue

        time_diff = round(delay1 + delay2, 4)
        if keystrokes == []:
            keystrokes.append(Keystroke(key_as_string, None))
        else:
            keystrokes.append(Keystroke(key_as_string, time_diff))
    return keystrokes

def log_keystrokes(keystrokes: List[Keystroke], input_string:str) -> bool:
    """
    Log keystrokes to a file.
    """
    if keystrokes == [] or input_string == '':
        print('No keystrokes to log.')
        return False
    
    print('Simulation complete. Logging keystrokes...')
    from keystrokeLogger import KeystrokeLogger
    logger = KeystrokeLogger(filename=ABSOLUTE_SIM_FILEPATH)
    logger.set_internal_log(keystrokes, input_string)
    success = logger.save_log()
    if success:
        print('Success!')
    else:
        print('Failed to log keystrokes.')
    return success


def main(input_string:str = "hey look ma, a simulation!", logging_on = LOGGING_ON):
    keystrokes = simulate_keystrokes(input_string, delay_mean=DEFAULT_DELAY_MEAN, delay_standard_deviation=DEFAULT_DELAY_STANDARD_DEVIATION)
    if logging_on:
        log_keystrokes(keystrokes, input_string)
    return keystrokes
if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if length > 1:
        # print(f'boop! {length}')
        main(sys.argv[1])
    else:
        main()
