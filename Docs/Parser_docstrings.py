from typing import List, Optional, Dict
from validation import Log, Keystroke
class KeyParser:
    """
    A class used to parse and analyze keystroke logs.

    Attributes:
        filename (str): The name of the file to load logs from.
        logs (list): The list of logs loaded from the file.
        exclude_outliers (bool): A flag indicating whether to exclude outliers.
    """
def __init__(self, filename: Optional[str] = '', exclude_outliers: bool = True) -> None:
        """
        Initialize the KeyParser and load logs.

        Args:
            filename (str, optional): The name of the file to load logs from. Defaults to ABSOLUTE_REG_FILEPATH.
            exclude_outliers (bool, optional): A flag indicating whether to exclude outliers. Defaults to True.
        """
def extract_logs(self) -> List[Log]:
        """
        Reads logfile and extracts logs.

        Returns:
            list: A list of logs loaded from the file. If an error occurs, an empty list is returned.
        """
def check_membership(self, identifier: str) -> bool:
        """
        Check if a log with the identifier exists in the loaded logs.

        Args:
            identifier (str): The UUID or exact string to check for.

        Returns:
            bool: True if a log with the given UUID or exact string exists, False otherwise.
        """
def id_by_index(self, index: int) -> Optional[str]:
        """
        Get the ID of the log at a given index. 
        Index begins at 1, as labeled in method print_strings.

        Args:
            index (int): The index of the log to get the ID of.

        Returns:
            str or None: The ID of the log at the given index. If no such log is found, None is returned.
        """
def id_from_substring(self, keyword: str) -> Optional[str]:
        """
        Get the ID of the first log that contains a given substring.

        Args:
            keyword (str): The substring to search for.

        Returns:
            str or None: The ID of the first log that contains the substring. If no such log is found, None is returned.
        """
def get_strings(self, identifier: Optional[str] = None) -> List[str]:
        """
        Get a list of all strings in the logs. If an identifier is provided, 
        only the associated string is included.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of all strings in the logs. If an identifier is provided, 
            the list contains the string associated with that identifier. 
            If the identifier is not found, an empty list is returned.
        """
def print_strings(self, identifier: Optional[str] = None, truncate: int = 25) -> None:
        """
        Prints strings from logs. If 'identifier' is provided, prints associated string.
        Strings longer than 'truncate' value are appended with "...[truncated]".

        Args:
            identifier (str, optional): The UUID or exact string to check for.
            truncate (int, optional): Maximum length for printed strings. Defaults to 25.
        """
def get_only_times(self, identifier: Optional[str] = None, exclude_outliers: Optional[bool] = None) -> List[float]:
        """
        Get a list of all keystroke delay times.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            List[float]: A list of float values.
        """
def wpm(self, identifier: Optional[str] = None) -> Optional[float]:
        """
        Calculate the average words per minute.
        Formula is CPM/5, where CPM is characters per minute.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If no characters are found, None is returned.
        """
def get_highest_keystroke_times(self, identifier: Optional[str] = None) -> List[float]:
        """
        Get the highest keystroke time for each log.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of float values.
        """
def get_average_delay(self, identifier: Optional[str] = None) -> Optional[float]:
        """
        Get the average time between keystrokes.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If no keystroke times are found, None is returned.
        """
def get_std_deviation(self, identifier: Optional[str] = None) -> Optional[float]:
        """
        Get the standard deviation of the time between keystrokes.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If insufficient keystrokes are found, None is returned.
        """
def visualize_keystroke_times(self, identifier: Optional[str] = None, keystrokes: Optional[List[Keystroke]] = None, 
                                  exclude_outliers: Optional[bool] = None) -> None:
        """
        Plots the average keystroke time for each character.

        Args:
            identifier (str, optional): The UUID or exact string to check for.
            keystrokes (list, optional): A list of Keystroke items.
            exclude_outliers (bool, optional): A flag indicating whether to exclude outliers.
        """
def get_keystrokes(self, identifier: Optional[str] = None) -> List[Keystroke]:
        """
       Get a list of all keystrokes in the logs.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of Keystroke items.
        """
def map_chars_to_times(self, keystrokes: Optional[List[Keystroke]] = None, exclude_outliers: Optional[bool] = None) -> Dict[str, float]:
        """
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            keystrokes (list, optional): A list of Keystroke items.

        Returns:
            dict: A dictionary mapping each character to its average keystroke time.
        """

def keystrokes_to_string(self, keystrokes: List[Keystroke]) -> str:
    """
    Converts a list of Keystroke objects into a string, taking into account special keys.

    Args:
        keystrokes (List[Keystroke]): A list of Keystroke objects.

    Returns:
        str: The string representation of the keystrokes.
    """


def validate_keystrokes(keystrokes: List[Keystroke], input_string: str) -> bool:
    """
    Validate a list of Keystroke objects against the logs.

    Args:
        keystrokes (List[Keystroke]): A list of Keystroke objects.
        identifier (str, optional): The UUID or exact string to check for.

    Returns:
        bool: True if the keystrokes match the logs, False otherwise.
    """