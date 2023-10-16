from pynput.keyboard import Controller
from time import sleep
import numpy as np
from config import  MIN_DELAY, SIM_SPEED_MULTIPLE, SIM_DELAY_MEAN, SIM_DELAY_STD_DEV, SIM_MAX_WORDS, SIM_WHITESPACE_DICT, SIM_MAP_CHARS
from config import SPECIAL_KEYS, WEIRD_KEYS, STOP_KEY

from typing import List, Union, Optional
from validation import Keystroke
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

    def __init__(self, speed_multiplier: Union[float, int] = SIM_SPEED_MULTIPLE, max_words: int = SIM_MAX_WORDS, 
                 delay_mean: float = SIM_DELAY_MEAN, delay_standard_deviation: float = SIM_DELAY_STD_DEV,
                 min_delay: float = MIN_DELAY, whitespace_keys: dict = SIM_WHITESPACE_DICT, 
                 char_map = SIM_MAP_CHARS, special_keys: dict = SPECIAL_KEYS,
                 disabled = False) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
        self.speed_multiplier = speed_multiplier
        self.delay_mean = delay_mean
        self.delay_standard_deviation = delay_standard_deviation
        self.max_words = max_words
        self.min_delay = min_delay
        self.whitespace_keys = whitespace_keys
        self.special_keys = special_keys
        self.char_map = char_map
        self.disabled = disabled
    
    def calculate_delay(self, speed_multiple: Union[float, int, None]) -> float:
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
    
    def generate_keystrokes_from_string(self, string: str) -> List[Keystroke]:
        """
        Generate valid Keystrokes from a string. Output object can be simulated.

        Returns:
            List[Keystroke]: A list of keystrokes.
        """
        # The rest of the code from the simulate_keystrokes function goes here.
        keystrokes: List[Keystroke] = []
        word_count = 0

        for char in string:
            if word_count == self.max_words:
                print(f"Reached max words: {self.max_words}")
                break
            keystroke = self.generate_keystroke(char)
            if keystroke is None:
                continue
            if keystroke.key == ' ':
                word_count += 1
            if keystrokes == []:
                keystroke.time = None
            keystrokes.append(keystroke)

        return keystrokes
    
    def generate_keystroke(self, char: str) -> Optional[Keystroke]:
        """
        Generate a single keystroke from a character.
        """
        delay1 = self.calculate_delay(1)
        delay2 = self.calculate_delay(1.5)
        key_as_string = ''

        if char in self.char_map:
            key_as_string = str(self.char_map[char])
            # print(f"Found char: {char} | {self.char_map[char]} | {key_as_string}")
        elif char.isprintable():
            key_as_string = char
        else:
            return None
        delay = round(delay1 + delay2, 4)
        return Keystroke(key_as_string, delay)
    
    def simulate_keystrokes(self, keystrokes: List[Keystroke]) -> None:
        """
        Function to simulate the given keystrokes.

        Args:
            keystrokes (List[Keystroke], optional): The list of keystrokes to simulate. 
        """
        if not keystrokes:
            print("No keystrokes found.")
            return
        if self.disabled:
            print("Simulation disabled.")
            return

        keyboard = Controller()
        none_count = 0
        for keystroke in keystrokes:
            if not keystroke.valid:
                print(f"Invalid key: {keystroke.key}")
                continue
            key = keystroke.key
            time = keystroke.time
            if time is None:
                none_count += 1
                if none_count > 1:
                    print('Critical error: None value marks first character. Only use once')
                    break
                # What should this time diff be?
                delay = 0.0
            else:
                delay = time
                # If time difference is greater than 3 seconds, set diff to 3.x seconds with decimal coming from delay
                if self.speed_multiplier > 0:
                    delay = delay / self.speed_multiplier
                if delay > 3:
                    delay = 3 + (delay / 1000)
            try:
                if delay > 0:
                    sleep(delay)  # Wait for the time difference between keystrokes
                if key in self.special_keys:
                    keyboard.press(self.special_keys[key])
                    keyboard.release(self.special_keys[key])
                elif key in WEIRD_KEYS:
                    keyboard.type(WEIRD_KEYS[key])
                else:
                    keyboard.type(key.strip("\'"))  # Type the character

                if key == STOP_KEY:
                    print('STOP key found. Stopping simulation.')
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    
def main(input_string:str = "hey look ma, a simulation!"):
    """
    Simulate keystrokes from a string and log them.

    Args:
        input_string (str): The string to simulate.
    """
    simulator = KeySimulator()
    keystrokes = simulator.generate_keystrokes_from_string(input_string)
    simulator.simulate_keystrokes(keystrokes)
    return keystrokes

if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if length > 1:
        # print(f'boop! {length}')
        main(sys.argv[1])
    else:
        main()