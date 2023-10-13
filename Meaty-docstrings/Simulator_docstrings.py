from typing import List, Union
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
        allow_enter_and_tab (bool): A flag indicating whether to allow enter and tab keys.
        special_keys (dict): A dictionary mapping special characters to their corresponding keys.
    """
def __init__(self, delay_mean: float = 0.07, delay_standard_deviation: float = 0.02, max_words: int = 300,
                  min_delay: float = 0.03, logging_on: bool = True, allow_enter_and_tab: bool = True) -> None:
        """
        Initialize the KeySimulator with the given parameters.
        """
def get_delay(self, speed_multiple: Union[float, int, None]) -> float:
        """
        Get a normally distributed delay between keystrokes.

        Args:
            speed_multiple: The speed multiplier.

        Returns:
            float: The delay between keystrokes.
        """
def simulate_keystrokes(self, string: str) -> List[Keystroke]:
        """
        Simulate keystrokes from a string.

        Args:
            string (str): The string to simulate.

        Returns:
            List[Keystroke]: A list of keystrokes.
        """
def log_keystrokes(self, keystrokes: List[Keystroke], input_string:str) -> bool:
        """
        Log keystrokes to a file.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to log.
            input_string (str): The input string.

        Returns:
            bool: True if the keystrokes were logged successfully, False otherwise.
        """
def main(self, input_string:str = "hey look ma, a simulation!"):
        """
        Simulate keystrokes from a string and log them.

        Args:
            input_string (str): The string to simulate.
        """