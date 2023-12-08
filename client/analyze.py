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

        Parameters
        ----------
        logfile (`str`): The logfile to use for logging.
        """
        self.parser.filename = logfile
        self.parser.load_logs()

    def is_id_present(self, identifier: str) -> bool:
        """
        Check if the string is in the logs.

        Parameters
        ----------
        identifier (`str`): The identifier to check.
        """
        return self.parser.is_id_present(identifier)

    def id_by_index(self, index: int) -> str:
        """
        Get the identifier by index, starting from 1.

        Parameters
        ----------
        index (`int`): The index to check.
        """
        length = len(self.parser)
        if index > length:
            print("Warning! Index too high. Returning the last id.")
            return self.id_by_index(length)

        id = self.parser.id_by_index(index)
        if id is None:
            raise ValueError("Logs are empty.")
        return id

    def id_from_substring(self, substring: str) -> str:
        """
        Get the identifier from a substring.

        Parameters
        ----------
        substring (`str`): The substring to check.
        """
        id = self.parser.id_from_substring(substring)
        if id is None:
            raise ValueError("Substring not present in logs.")
        return id

    def get_strings(self, identifier: str | None = None) -> list[str]:
        """
        Get the strings from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        """
        return self.parser.get_strings(identifier)

    def print_strings(self, max: int = 5, truncate: int = 25,
                      identifier: str | None = None) -> None:
        """
        Print the strings from the logs.

        Parameters
        ----------
        max (`int`, optional): The maximum number of strings to print.
        truncate (`int`, optional): The maximum number of characters to print.
        identifier (`str`, optional): The identifier to check.
        """
        self.parser.print_strings(max, truncate, identifier)

    def wpm(self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            id: str | None = None,
            ) -> float:
        """
        Get the words per minute from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        wpm = self.parser.wpm(identifier, exclude_outliers)
        if wpm is None:
            raise ValueError("WPM not present.")
        return wpm

    def get_highest_keystroke_times(
            self,
            identifier: str | None = None,
            exclude_outliers: bool | None = None) -> list[float]:
        """
        Get the highest keystroke times from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        return self.parser.get_highest_keystroke_times(
            identifier, exclude_outliers)

    def get_average_delay(
            self,
            identifier: str | None = None,
            exclude_outliers: bool | None = None) -> float:
        """
        Get the average delay from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        avg_delay = self.parser.get_average_delay(
            keystrokes, exclude_outliers, id)
        if avg_delay is None:
            raise ValueError("Average delay not present.")
        return avg_delay

    def get_std_deviation(
            self,
            identifier: str | None = None,
            exclude_outliers: bool | None = None) -> float:
        """
        Get the standard deviation from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        std_dev = self.parser.get_std_deviation(
            keystrokes, exclude_outliers, id)
        if std_dev is None:
            raise ValueError("Standard deviation not present.")
        return std_dev

    def visualize(
            self,
            mode: str | None = None,
            save_file: bool | None = None,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None) -> None:
        """
        Plot the keystroke times from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
        keystrokes (`KeystrokeList`, optional): The keystrokes to plot.
        exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        self.parser.visualize(
            mode,
            save_file,
            keystrokes,
            exclude_outliers,
            id)

    def get_keystrokes(self, identifier: str | None = None) -> KeystrokeList:
        """
        Get the keystrokes from the logs.

        Parameters
        ----------
        identifier (`str`, optional): The identifier to check.
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

    def __repr__(self) -> str:
        """
        Get the string representation of the Analyze class.
        """
        return self.parser.__repr__()
