from pynput.keyboard import Controller, Key
import time
import numpy as np
DEFAULT_DELAY_MEAN = 0.07
DEFAULT_DELAY_STANDARD_DEVIATION = 0.02
MAX_WORDS = 500
MIN_DELAY = 0.035

ALLOW_ENTER_AND_TAB = False

if ALLOW_ENTER_AND_TAB:
    SPECIAL_KEYS = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }
else:
    SPECIAL_KEYS = {' ': Key.space}

# sample_string = """Today, there are some endangered animals on Earth. It means that we can find only a few of them around us. Some examples are whales, pandas, tigers and Asian elephants. Humans destroy the natural homes of the animals in the forests, lakes, and plains. When the number of people on Earth increases, they need more place for living. They cut down trees and destroy lakes. They make homes and roads instead. Then the animals won't have a place to live. They will die out. The Iranian cheetah is among these animals. This wild animal lives only in the plains of Iran. Now there are only a few Iranian cheetahs alive. If people take care of them, there is hope for this beautiful animal to live. Recently, families pay more attention to nature, students learn about saving wildlife, and some hunters don't go hunting anymore. In this way, the number of cheetahs is going to increase in the future."""
sample_string = """1 2 3 4 \n 5 6 7 8 9 
10 11 12 13 14 15."""
def words_from_string(string: str) -> list:
    return string.split()


def simulate_keystrokes(string: str, delay_mean: float, delay_standard_deviation: float):
    keyboard = Controller()

    def get_delay(speed_by_multiple:float=None) -> float:
        delay = np.random.normal(delay_mean/(speed_by_multiple or 1), delay_standard_deviation/(speed_by_multiple or 1))
        if delay < MIN_DELAY:
            print('beep small delay')
            delay = MIN_DELAY + delay/10
        return delay
    word_count = 0
    delay1 = 0
    delay2 = 0
    time_diff = 0

    keystrokes = []
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
                key_as_string = str(special_key)
                word_count += 1
                special_key = SPECIAL_KEYS[char]
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
        time_diff = delay1 + delay2
        print(f"Typed: {char} | Delay: {time_diff}")

def main(input_string=None):
    if input_string is None:
        input_string = sample_string
    # words = words_from_string(input_string)
    simulate_keystrokes(input_string, delay_mean=DEFAULT_DELAY_MEAN, delay_standard_deviation=DEFAULT_DELAY_STANDARD_DEVIATION)

if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if length > 1:
        # print(f'boop! {length}')
        main(sys.argv[1])
    else:
        main()
