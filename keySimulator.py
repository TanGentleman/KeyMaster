from pynput.keyboard import Controller, Key
from time import sleep
import numpy as np
from config import ABSOLUTE_SIM_FILEPATH
from typing import List, Optional, Union
from validation import is_key_valid, Keystroke
from keyLogger import KeyLogger
class KeySimulator:
    """
    A class used to simulate keystrokes and log them.

    Attributes:
        delay_mean (float): The mean delay between keystrokes.
        delay_standard_deviation (float): The standard deviation of the delay between keystrokes.
        max_words (int): The maximum number of words to simulate.
        min_delay (float): The minimum delay between keystrokes.
        logging_on (bool): A flag indicating whether to log keystrokes.
        allow_enter_and_tab (bool): A flag indicating whether to allow enter and tab keys.
        special_keys (dict): A dictionary mapping special characters to their corresponding keys.
    """

    def __init__(self, delay_mean: float = 0.07, delay_standard_deviation: float = 0.02, max_words: int = 300,
                  min_delay: float = 0.03, logging_on: bool = True, allow_enter_and_tab: bool = True) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
        self.speed_multiplier = 1
        self.delay_mean = delay_mean
        self.delay_standard_deviation = delay_standard_deviation
        self.max_words = max_words
        self.min_delay = min_delay
        self.logging_on = logging_on
        self.allow_enter_and_tab = allow_enter_and_tab
        self.special_keys = {' ': Key.space}
        if self.allow_enter_and_tab:
            self.special_keys.update({
                '\n': Key.enter,
                '\t': Key.tab,
            })
    
    def get_delay(self, speed_multiple: Union[float, int, None]) -> float:
        """
        Get a normally distributed delay between keystrokes.

        Args:
            speed_multiple: The speed multiplier.

        Returns:
            float: The delay between keystrokes.
        """
        # Ensure speed_by_multiple > 0
        if speed_multiple is None:
            speed_multiple = self.speed_multiplier
            
        speed_multiple = float(speed_multiple)
        if speed_multiple <= 0:
            # ERROR
            print(f"Speed by multiple must be greater than 0. Received {speed_multiple}")
            speed_multiple = 1
        delay = np.random.normal(self.delay_mean/(speed_multiple), self.delay_standard_deviation/speed_multiple)
        if delay < self.min_delay:
            # print(f"Delay too low: {delay}")
            delay = self.min_delay + delay/10
        return delay
    
    def simulate_keystrokes(self, string: str) -> List[Keystroke]:
        """
        Simulate keystrokes from a string.

        Args:
            string (str): The string to simulate.

        Returns:
            List[Keystroke]: A list of keystrokes.
        """
        # The rest of the code from the simulate_keystrokes function goes here.
        keyboard = Controller()
        keystrokes: List[Keystroke] = []
        
        word_count = 0
        for char in string:
            delay1 = self.get_delay(1)
            delay2 = self.get_delay(1.5)
            key_as_string = ''
            if word_count == self.max_words:
                print(f"Reached max words: {self.max_words}")
                break
            try:
                sleep(delay1)
                if char in self.special_keys:
                    special_key = self.special_keys[char]
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

            if keystrokes == []:
                keystrokes.append(Keystroke(key_as_string, None))
            else:
                time_diff = round(delay1 + delay2, 4)
                keystrokes.append(Keystroke(key_as_string, time_diff))
        return keystrokes
    
    def log_keystrokes(self, keystrokes: List[Keystroke], input_string:str) -> bool:
        """
        Log keystrokes to a file.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to log.
            input_string (str): The input string.

        Returns:
            bool: True if the keystrokes were logged successfully, False otherwise.
        """
        if keystrokes == [] or input_string == '':
            print('No keystrokes to log.')
            return False
        
        print('Simulation complete. Logging keystrokes...')
        logger = KeyLogger(filename=ABSOLUTE_SIM_FILEPATH)
        logger.set_internal_log(keystrokes, input_string)
        success = logger.save_log()
        if success:
            print('Success!')
        else:
            print('Failed to log keystrokes.')
        return success

    def main(self, input_string:str = "hey look ma, a simulation!"):
        """
        Simulate keystrokes from a string and log them.

        Args:
            input_string (str): The string to simulate.
        """
        keystrokes = self.simulate_keystrokes(input_string)
        if self.logging_on:
            self.log_keystrokes(keystrokes, input_string)
        return keystrokes
