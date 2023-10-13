from pynput.keyboard import Controller, Key
from time import sleep
import numpy as np
from config import ABSOLUTE_SIM_FILEPATH, Keystroke
from typing import List

class KeystrokeSimulator:
    """
    A class used to simulate keystrokes and log them if required.
    """

    DEFAULT_DELAY_MEAN = 0.07
    DEFAULT_DELAY_STANDARD_DEVIATION = 0.02
    MAX_WORDS = 300
    MIN_DELAY = 0.03

    SPECIAL_KEYS = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }

    def __init__(self, logging_on=True):
        """
        Initialize the KeystrokeSimulator.

        Args:
            logging_on (bool, optional): A flag indicating whether to log the keystrokes. Defaults to True.
        """
        self.logging_on = logging_on

    def simulate_keystrokes(self, string: str, delay_mean: float, delay_standard_deviation: float) -> List[Keystroke]:
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
                raise ValueError(f"Speed by multiple must be greater than 0. Received {speed_by_multiple}")
            delay = np.random.normal(delay_mean / (speed_by_multiple), delay_standard_deviation / speed_by_multiple)
            if delay < self.MIN_DELAY:
                delay = self.MIN_DELAY + delay / 10
            return delay

        for char in string:
            delay1 = get_delay(1)
            delay2 = get_delay(1.5)
            key_as_string = ''

            if word_count == self.MAX_WORDS:
                print(f"Reached max words: {self.MAX_WORDS}")
                break

            try:
                sleep(delay1)
                if char in self.SPECIAL_KEYS:
                    special_key = self.SPECIAL_KEYS[char]
                    key_as_string = str(special_key)
                    word_count += 1
                    keyboard.press(special_key)
                    keyboard.release(special_key)
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

    def log_keystrokes(self, keystrokes: List[Keystroke], input_string: str) -> bool:
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

    def simulate_and_log_keystrokes(self, input_string: str):
        """
        Simulate keystrokes and log them if required.

        Args:
            input_string (str): The string to simulate keystrokes from.
        """
        keystrokes = self.simulate_keystrokes(
            input_string,
            delay_mean=self.DEFAULT_DELAY_MEAN,
            delay_standard_deviation=self.DEFAULT_DELAY_STANDARD_DEVIATION
        )
        if self.logging_on:
            self.log_keystrokes(keystrokes, input_string)
        return keystrokes

if __name__ == "__main__":
    import sys

    length = len(sys.argv)
    if length > 1:
        KeystrokeSimulator().simulate_and_log_keystrokes(sys.argv[1])
    else:
        KeystrokeSimulator().simulate_and_log_keystrokes("hey look ma, a simulation!")
