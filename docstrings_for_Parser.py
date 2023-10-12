class KeystrokeParser:
    """
    A class used to parse keystroke logs.
    """
def __init__(self, filename=ABSOLUTE_FILENAME, exclude_outliers=True):
        """
        Initialize the KeystrokeParser with a filename and load logs.
        Outliers are excluded by default.
        """
def load_logs(self) -> list:
        """
        Function to load logs from the file.
        """
def check_membership(self, identifier) -> bool:
        """
        Function to check if a log with the given UUID or exact string exists.
        """
def id_from_substring(self, keyword) -> str or None:
        """
        Function to return the ID of the first string that contains a given substring.
        """
def get_all_strings(self, identifier=None) -> list:
        """
        Function to return a list of all strings in the logs.
        """
def print_all_strings(self, identifier=None, truncate=25) -> None:
        """
        Function to print all strings in the logs.
        """
def get_only_times(self, identifier=None) -> list:
        """
        Function to return a list of all times in the logs.
        """
def wpm(self, identifier=None) -> float or None:
        """
        Function to return the average words per minute.
        WPM is CPM/5, where CPM is characters per minute.
        """
def get_highest_keystroke_times(self, identifier=None) -> list:
        """
        Function to return the highest times it took for keystrokes.
        """
def get_average_delay(self, identifier=None) -> float or None:
        """
        Function to return the average time between keystrokes for a given log.
        """
def get_std_deviation(self, identifier=None) -> float or None:
        """
        Function to return the standard deviation of the time between keystrokes for a given log.
        """
def visualize_keystroke_times(self, keystrokes=None) -> None:
        """
        Plots the average keystroke time for each character based on the keystrokes in the logs.
        """
def get_all_keystrokes(self, identifier=None) -> list:
        """
        Returns a list of all keystrokes in the logs.

        Returns:
            list: A list of keystrokes, where each keystroke is represented by a list containing a character and a time.
        """
def calculate_average_keystroke_times(self, keystrokes=None) -> dict:
        """
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            keystrokes (list): A list of keystrokes, where each keystroke is represented by a list containing a character and a time.

        Returns:
            dict: A dictionary mapping each character to its average keystroke time.
        """