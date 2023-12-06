from client.configurate import Config
from utils.validation import KeystrokeList


class Analyze:
    """
    The Analyze class is a wrapper for all the analysis options.
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the Analyze class.
        """
        if config is None:
            config = Config()
        self.parser = config.KeyParser()

    def load_logfile(self, logfile: str) -> None:
        """
        Change logfile and update the logs.
        """
        self.parser.filename = logfile
        self.parser.load_logs()

    def check_membership(self, identifier: str) -> bool:
        """
        Check if the string is in the logs.
        """
        return self.parser.check_membership(identifier)

    def id_by_index(self, index: int) -> str:
        """
        Get the identifier by index.
        """
        id = self.parser.id_by_index(index)
        if id is None:
            raise ValueError("Identifier not present.")
        return id

    def id_from_substring(self, substring: str) -> str:
        """
        Get the identifier from a substring.
        """
        id = self.parser.id_from_substring(substring)
        if id is None:
            raise ValueError("Substring not present in logs.")
        return id

    def get_strings(self, identifier: str | None = None) -> list[str]:
        """
        Get the strings from the logs.
        """
        return self.parser.get_strings(identifier)

    def print_strings(self, max: int = 5, truncate: int = 25,
                      identifier: str | None = None) -> None:
        """
        Print the strings from the logs.
        """
        self.parser.print_strings(max, truncate, identifier)

    def wpm(self, identifier: str | None = None) -> float:
        """
        Get the words per minute from the logs.
        """

        wpm = self.parser.wpm(identifier)
        if wpm is None:
            raise ValueError("WPM not present.")
        return wpm

    def get_highest_keystroke_times(
            self, identifier: str | None = None) -> list[float]:
        """
        Get the highest keystroke times from the logs.
        """
        return self.parser.get_highest_keystroke_times(identifier)

    def get_average_delay(self, identifier: str | None = None) -> float:
        """
        Get the average delay from the logs.
        """
        avg_delay = self.parser.get_average_delay(identifier)
        if avg_delay is None:
            raise ValueError("Average delay not present.")
        return avg_delay

    def get_std_deviation(self, identifier: str | None = None) -> float:
        """
        Get the standard deviation from the logs.
        """
        std_dev = self.parser.get_std_deviation(identifier)
        if std_dev is None:
            raise ValueError("Standard deviation not present.")
        return std_dev

    def visualize_keystroke_times(
            self,
            identifier: str | None = None,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None) -> None:
        """
        Plot the keystroke times from the logs.
        """
        self.parser.visualize_keystroke_times(
            identifier, keystrokes, exclude_outliers)

    def get_keystrokes(self, identifier: str | None = None) -> KeystrokeList:
        """
        Get the keystrokes from the logs.
        """
        return self.parser.get_keystrokes(identifier)

    def nuke_duplicates(self) -> None:
        """
        Remove duplicate strings from the logs.
        """
        self.parser.nuke_duplicates()

    def confirm_nuke(self) -> None:
        """
        Confirm the nuke.
        """
        self.parser.confirm_nuke()

    def dump_modified_logs(self) -> None:
        """
        Dump the modified logs.
        """
        self.parser.dump_modified_logs()
