from pynput.keyboard import Controller
from time import sleep
import numpy as np
from config import ABSOLUTE_SIM_FILEPATH, DEFAULT_DELAY_MEAN, DEFAULT_DELAY_STANDARD_DEVIATION, SIM_MAX_WORDS, MIN_DELAY, SIM_LOGGING_ON, SIM_SPECIAL_KEYS
from typing import List, Union
from validation import Keystroke
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
        special_keys (dict): A dictionary mapping special characters to their corresponding keys.
    """

    def __init__(self, speed_multiplier: Union[float, int] = 1, delay_mean: float = DEFAULT_DELAY_MEAN, delay_standard_deviation: float = DEFAULT_DELAY_STANDARD_DEVIATION, 
                 max_words: int = SIM_MAX_WORDS, min_delay: float = MIN_DELAY, logging_on: bool = SIM_LOGGING_ON, 
                 special_keys: dict = SIM_SPECIAL_KEYS) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
        self.speed_multiplier = speed_multiplier
        self.delay_mean = delay_mean
        self.delay_standard_deviation = delay_standard_deviation
        self.max_words = max_words
        self.min_delay = min_delay
        self.logging_on = logging_on
        self.special_keys = special_keys
    
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
        Log keystrokes to simulation logfile.

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

if __name__ == "__main__":
    import sys
    simulator = KeySimulator()
    length = len(sys.argv)
    if length > 1:
        # print(f'boop! {length}')
        simulator.main(sys.argv[1])
    else:
        simulator.main()