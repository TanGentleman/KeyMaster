from pynput.keyboard import Controller, Key
import time
import numpy as np
from config import ABSOLUTE_SIM_FILENAME
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


sample_string = """1 2 3 4 
# 5 6 7 8
# 9 10 11 12 13."""
def words_from_string(string: str) -> list:
    return string.split()


def simulate_keystrokes(string: str, delay_mean: float, delay_standard_deviation: float):
    keyboard = Controller()
    word_count = 0
    keystrokes = []
    def get_delay(speed_by_multiple:float=None) -> float:
        delay = np.random.normal(delay_mean/(speed_by_multiple or 1), delay_standard_deviation/(speed_by_multiple or 1))
        if delay < MIN_DELAY:
            # print(f"Delay too low: {delay}")
            delay = MIN_DELAY + delay/10
        return delay
    
    for char in string:
        time_diff = 0
        delay1 = get_delay(1)
        delay2 = 0
        key_as_string = ''
        if word_count == MAX_WORDS:
            print(f"Reached max words: {MAX_WORDS}")
            break
        try:
            time.sleep(delay1)
            if char in SPECIAL_KEYS:
                special_key = SPECIAL_KEYS[char]
                key_as_string = str(special_key)
                word_count += 1
                keyboard.press(special_key)
                keyboard.release(special_key)
                # Add delay after a special key
                # Or should delay be at the start of its next key?
                delay2 = get_delay(1.5)
                time.sleep(delay2)
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
            keystrokes.append((key_as_string, None))
        else:
            keystrokes.append((key_as_string, time_diff))
    return keystrokes

def main(input_string=None, logging_on = LOGGING_ON):
    if input_string is None:
        input_string = sample_string

    keystrokes = simulate_keystrokes(input_string, delay_mean=DEFAULT_DELAY_MEAN, delay_standard_deviation=DEFAULT_DELAY_STANDARD_DEVIATION)
    
    if logging_on:
        if keystrokes == []:
            print('No keystrokes to log.')
            return
        print('Simulation complete. Logging keystrokes...')
        from keystrokeLogger import KeystrokeLogger
        logger = KeystrokeLogger()
        logger.set_internal_log(keystrokes, input_string)
        logger.filename = ABSOLUTE_SIM_FILENAME
        success = logger.save_log()
        if success:
            print('Success!')
if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if length > 1:
        # print(f'boop! {length}')
        main(sys.argv[1])
    else:
        main()
