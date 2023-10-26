from config import  MIN_DELAY, SIM_SPEED_MULTIPLE, SIM_DELAY_MEAN, SIM_DELAY_STD_DEV, SIM_MAX_DURATION
from config import SIM_MAX_WORDS, sim_whitespace_dict, sim_map_chars, SPECIAL_KEYS, SIM_DISABLE

from typing import List, Union, Optional, Dict
from validation import Keystroke, Key
class KeySimulator:
    """
    A class used to simulate keystrokes and log them.

    Attributes:
        delay_mean (float): The mean delay between keystrokes.
        delay_standard_deviation (float): The standard deviation of the delay between keystrokes.
        max_words (int): The maximum number of words to simulate.
        min_delay (float): The minimum delay between keystrokes.
        logging_on (bool): A flag indicating whether to log keystrokes.
        special_keys (dict): A dictionary mapping special key strings to their corresponding keys.
    """
def __init__(self, speed_multiplier: Union[float, int] = SIM_SPEED_MULTIPLE, max_words: int = SIM_MAX_WORDS, 
                 delay_mean: float = SIM_DELAY_MEAN, delay_standard_deviation: float = SIM_DELAY_STD_DEV,
                 min_delay: float = MIN_DELAY, whitespace_keys: dict = sim_whitespace_dict, 
                 char_map = sim_map_chars, special_keys: Dict[str, Key] = SPECIAL_KEYS,
                 disabled = SIM_DISABLE, max_duration = SIM_MAX_DURATION) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
def calculate_delay(self, speed_multiple: Union[float, int, None]) -> float:
        """
        Get a normally distributed delay between keystrokes.

        Args:
            speed_multiple: The speed multiplier.

        Returns:
            float: The delay between keystrokes.
        """
def generate_keystrokes_from_string(self, string: str) -> List[Keystroke]:
        """
        Generate valid Keystrokes from a string. Output object can be simulated.

        Returns:
            List[Keystroke]: A list of keystrokes.
        """
def generate_keystroke(self, char: str) -> Optional[Keystroke]:
        """
        Generate a single keystroke from a character.
        """
def simulate_keystrokes(self, keystrokes: List[Keystroke]) -> None:
        """
        Function to simulate the given keystrokes.

        Args:
            keystrokes (List[Keystroke], optional): The list of keystrokes to simulate. 
        """
def main(input_string:str = "hey look ma, a simulation!"):
    """
    Simulate keystrokes from a string and log them.

    Args:
        input_string (str): The string to simulate.
    """