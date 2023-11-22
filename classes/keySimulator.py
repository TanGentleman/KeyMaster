# Standard library imports
from time import time as get_time
from time import sleep
from numpy import random
from typing import List, Dict

# Third party imports
from pynput.keyboard import Controller

# KeyMaster imports
from utils.config import  MIN_DELAY, SIM_SPEED_MULTIPLE, SIM_DELAY_MEAN, SIM_DELAY_STD_DEV, SIM_MAX_WORDS, sim_encoded_char_dict
from utils.config import SPECIAL_KEYS, WEIRD_KEYS, STOP_KEY, SIM_DISABLE, SHIFTED_CHARS, SHIFT_SPEED, SIM_MAX_DURATION
from utils.validation import Keystroke, Key

import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

class KeySimulator:
    """
    A class used to simulate keystrokes and log them.

    Attributes:
        speed_multiplier (float or int): The speed multiplier.
        delay_mean (float): The mean delay between keystrokes.
        delay_standard_deviation (float): The standard deviation of the delay between keystrokes.
        max_words (int): The maximum number of words to simulate.
        min_delay (float): The minimum delay between keystrokes.
        whitespace_keys (dict): A dictionary of whitespace characters and their corresponding keys.
        special_keys (dict): A dictionary of special keys and their corresponding keys.
        encoded_char_dict (dict): A dictionary of encoded characters and their corresponding strings.
        disabled (bool): Whether or not the simulation is disabled.
        max_duration (float): The maximum duration of the simulation.
    """

    def __init__(self, disabled = SIM_DISABLE, max_duration = SIM_MAX_DURATION,
                 speed_multiplier: float | int = SIM_SPEED_MULTIPLE, max_words: int = SIM_MAX_WORDS, 
                 min_delay: float = MIN_DELAY, delay_mean: float = SIM_DELAY_MEAN, delay_standard_deviation: float = SIM_DELAY_STD_DEV,
                 encoded_char_dict = sim_encoded_char_dict, special_keys: Dict[str, Key] = SPECIAL_KEYS) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
        self.disabled = disabled
        self.max_duration = max_duration
        self.speed_multiplier = speed_multiplier
        self.delay_mean = delay_mean
        self.delay_standard_deviation = delay_standard_deviation
        self.max_words = max_words
        self.min_delay = min_delay
        self.encoded_char_dict = encoded_char_dict
        self.special_keys = special_keys
    
    def calculate_delay(self, speed_multiple: float | int | None) -> float:
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
            logging.error(f"Invalid speed multiplier: {speed_multiple}. Setting to 1")
            speed_multiple = 1
        delay = random.normal(self.delay_mean/(speed_multiple), self.delay_standard_deviation/speed_multiple)
        if delay < self.min_delay:
            # print(f"Delay too low: {delay}")
            delay = self.min_delay + delay/10
        return round(delay, 4)
    
    def generate_keystrokes_from_string(self, string: str) -> List[Keystroke]:
        """
        Generate valid Keystrokes from a string. Output object can be simulated.

        Returns:
            List[Keystroke]: A list of keystrokes.
        """
        # The rest of the code from the simulate_keystrokes function goes here.
        keystrokes: List[Keystroke] = []
        word_count = 0

        string_length = len(string)
        for i in range(string_length):
            if word_count == self.max_words:
                logging.info(f"Reached max words: {self.max_words}")
                break
            char = string[i]
            keystroke = self.generate_keystroke(char)
            if keystroke is None:
                continue
            if char == ' ':
                word_count += 1
            if not keystrokes:
                last_key = None
            else:
                last_key = keystrokes[-1].key
            # Lambda function to check if a key is eligible to have shift before it
            shift_eligible = lambda k: (k is None or k == ' ') or (k not in SHIFTED_CHARS and not k.isupper())

            # Check if a shift key needs to be added
            if shift_eligible(last_key):
                if char.isupper() or (char in SHIFTED_CHARS):
                    logging.info(f"Inserting shift before key: {char}")
                    # Add a shift keypress
                    if keystrokes == []:
                        time = None
                    else:
                        time = SHIFT_SPEED
                    key = 'Key.shift'
                    keystrokes.append(Keystroke(key, time))
            if keystrokes == []:
                keystroke.time = None
            keystrokes.append(keystroke)
            # Should I stop generation at stop key too?
            if char == STOP_KEY:
                logging.warning('STOP key found. Halting keystroke generation.')
                break

        return keystrokes
    
    def generate_keystroke(self, char: str) -> Keystroke | None:
        """
        Generate a single keystroke from a character.
        :param char: The character to generate a keystroke for.             
        :return: A Keystroke object or  None if the character is invalid.
        """
        if len(char) != 1:
            logging.error(f"generate_keystroke: Character length is not 1: {char}")
            return None
        delay1 = self.calculate_delay(1)
        delay2 = self.calculate_delay(1.5)
        key_string = ''

        if char in self.encoded_char_dict:
            key_string = str(self.encoded_char_dict[char])

        elif char.isprintable():
            # Add '' around the character
            key_string = f"'{char}'"
        else:
            logging.error(f"generate_keystroke: Non-printable character: {char} -> {ord(char)}")
            return None
        delay = delay1 + delay2
        return Keystroke(key_string, delay)
    
    
    def simulate_keystrokes(self, keystrokes: List[Keystroke]) -> None:
        """
        Function to simulate the given keystrokes.

        Args:
            keystrokes (List[Keystroke], optional): The list of keystrokes to simulate. 
        """
        if not keystrokes:
            logging.error("No keystrokes found.")
            return
        if self.disabled:
            logging.error("Simulation disabled.")
            return
        keyboard = Controller()
        special_key_dict = self.special_keys
        start_time = get_time()
        none_count = 0
        for keystroke in keystrokes:
            if not keystroke.valid:
                logging.error(f"Invalid key: {keystroke.key}")
                continue
            # Check if max duration has been reached
            if get_time() - start_time > self.max_duration:
                logging.info(f"Max duration reached: {self.max_duration} seconds")
                break

            key = keystroke.key
            time = keystroke.time
            if time is None:
                none_count += 1
                if none_count > 1:
                    logging.error('Critical error: None value marks first character. Only use once')
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
                if key in special_key_dict:
                    keyboard.tap(special_key_dict[key])
                elif key in WEIRD_KEYS:
                    keyboard.type(WEIRD_KEYS[key])
                else:
                    key = key.strip("\'")
                    # IMPORTANT. This string may should have '' around it (Not required)
                    # My implementation throughout should ensure it gets logged with single quotes.
                    keyboard.type(key)

                if key == STOP_KEY:
                    logging.warning('STOP key found. Stopping simulation.')
                    break
            except Exception as e:
                logging.critical(f"An error occurred: {e}")
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