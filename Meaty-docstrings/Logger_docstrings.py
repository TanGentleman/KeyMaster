from typing import Optional, List, Union
from pynput.keyboard import Key, KeyCode
from validation import Keystroke
class KeyLogger:
    """
    A class used to log keystrokes and calculate delays between each keypress.
    This class is responsible for capturing and storing keystrokes values and timings.
    It also keeps track of the total number of words typed and the entire string of characters typed.
    """
def __init__(self, filename: Optional[str] = "") -> None:
        """
        Initialize the KeyLogger.

        Args:
            filename (str, optional): The filename to save the log to.
            Defaults to ABSOLUTE_REG_FILEPATH.
            None value treated as null path.
        """
def reset(self) -> None:
        """
        Clear the current state of the logger.
        Keystrokes, the typed string, and the word count will be set to default values.
        """
def on_press(self, keypress: Union[Key, KeyCode, None]) -> None:
        """
        Handles key press events and logs valid Keystroke events.

        This function is called whenever a key is pressed. 
        It validates the keypress and appends the data
        KeyLogger attributes modified: keystrokes, typed_string, word_count, prev_time

        Args:
            keypress (Keypress): The key press event to handle.
        """
def stop_listener_condition(self, keypress: Union[Key, KeyCode]) -> bool:
        """
        Function to determine whether to stop the listener.

        Args:
            keypress (Keypress): The key press event to handle.

        Returns:
            bool: True if the listener should stop, False otherwise.
        """
def on_release(self, keypress: Union[Key, KeyCode, None]) -> None:
        """
        Handles key release events. Stop the listener when stop condition is met.

        Args:
            keypress (Keypress): The key press event to handle.

        Returns:
            False or None: False if the maximum word count is reached. This stops the listener.
        """
def start_listener(self) -> None:
        """
        Function to start the key listener.
        The listener will only stop when stop_listener_condition returns True.
        """
def is_log_legit(self, keystrokes: List[Keystroke], input_string: str) -> bool:
        """
        Validates the input string and keystrokes to ensure well formatted Log.

        This function ensures keystrokes are correctly formatted and input string is nonempty.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to validate.
            input_string (str): The input string to validate.

        Returns:
            bool: True if the input is valid Log material, False otherwise.
        """
def set_internal_log(self, keystrokes: List[Keystroke], input_string: str) -> bool:
        """
        Replace the internal log with the provided keystrokes and input string.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to replace self.keystrokes with.
            input_string (str): The input string to replace self.typed_string with.

        Returns:
            bool: True if state successfully replaced. False if arguments invalid.
        """
def save_log(self, reset: bool = False) -> bool:
        """
        Function to save the log to a file.

        Args:
            reset (bool, optional): Whether to reset the logger after saving the log. Defaults to False.

        Returns:
            bool: True if the log was saved successfully, False otherwise.
        """