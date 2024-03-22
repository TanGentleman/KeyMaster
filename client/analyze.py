from client.configurate import Config
from utils.validation import KeystrokeList


class Analyze:
    """
    The Analyze class is a wrapper for all the analysis options.
    """

    def __init__(self, config: Config | None = None,
                 preload: bool | None = None) -> None:
        """
        Initialize the Analyze class.
        """
        if config is None:
            config = Config()
        if preload is not None:
            config.preload = preload
        self.parser = config.config.KeyParser()

    def load_logfile(self, logfile: str | None = None) -> None:
        """
        Update logs from refreshed logfile.

        Parameters
        ----------
        - logfile (`str`, optional): The log filename.
        """
        if logfile is not None:
            self.parser.filename = logfile
        self.parser.load_logs()

    def is_id_present(self, km_id: str) -> bool:
        """
        Check if the string is in the logs.

        Parameters
        ----------
        - km_id (`str`): The id to check.
        """
        return self.parser.is_id_present(km_id)

    def id_by_index(self, index: int) -> str:
        """
        Get the id by index, starting from 1.

        Parameters
        ----------
        - index (`int`): The index to check.
        """
        length = len(self.parser)
        if index > length:
            print("Warning! Index too high. Returning the last id.")
            return self.id_by_index(length)

        km_id = self.parser.id_by_index(index)
        if km_id is None:
            raise ValueError("Logs are empty.")
        return km_id

    def id_from_substring(self, substring: str) -> str:
        """
        Get the id from a substring.

        Parameters
        ----------
        - substring (`str`): The substring to check.
        """
        km_id = self.parser.id_from_substring(substring)
        if km_id is None:
            raise ValueError("Substring not present in logs.")
        return km_id

    def get_strings(self, km_id: str | None = None) -> list[str]:
        """
        Get the strings from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        """
        return self.parser.get_strings(km_id)

    def print_strings(self, max: int = 5, truncate: int = 25,
                      km_id: str | None = None) -> None:
        """
        Print the strings from the logs.

        Parameters
        ----------
        - max (`int`, optional): The maximum number of strings to print.
        - truncate (`int`, optional): The maximum number of characters to print.
        - km_id (`str`, optional): The id to check.
        """
        self.parser.print_strings(max, truncate, km_id)

    def wpm(self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None,
            ) -> float:
        """
        Get the words per minute from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        wpm = self.parser.wpm(keystrokes, exclude_outliers, km_id)
        if wpm is None:
            raise ValueError("WPM not present.")
        return wpm

    def get_highest_keystroke_times(
            self,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> list[float]:
        """
        Get the highest keystroke times from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        return self.parser.get_highest_keystroke_times(exclude_outliers, km_id)

    def get_average_delay(
            self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> float:
        """
        Get the average delay from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        avg_delay = self.parser.get_average_delay(
            keystrokes, exclude_outliers, km_id)
        if avg_delay is None:
            raise ValueError("Average delay not present.")
        return avg_delay

    def get_std_deviation(
            self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> float:
        """
        Get the standard deviation from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        std_dev = self.parser.get_std_deviation(
            keystrokes, exclude_outliers, km_id)
        if std_dev is None:
            raise ValueError("Standard deviation not present.")
        return std_dev

    def get_stats(self,
              keystrokes: KeystrokeList | None = None,
              exclude_outliers: bool | None = None,
              km_id: str | None = None,
              ):
        """
        Get the stats of the logfile or provided keystrokes/km_id.

        Parameters
        ----------
        - keystrokes (`KeystrokeList`, optional): The keystrokes to check.
        - km_id (`str`, optional): The id to check.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        return self.parser.get_stats(keystrokes, exclude_outliers, km_id)

    def visualize(
            self,
            mode: str | None = None,
            save_file: bool | None = None,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> None:
        """
        Plot the keystroke times from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        - keystrokes (`KeystrokeList`, optional): The keystrokes to plot.
        - exclude_outliers (`bool`, optional): Whether to exclude outliers.
        """
        self.parser.visualize(
            mode,
            save_file,
            keystrokes,
            exclude_outliers,
            km_id)

    def get_keystrokes(self, km_id: str | None = None) -> KeystrokeList:
        """
        Get the keystrokes from the logs.

        Parameters
        ----------
        - km_id (`str`, optional): The id to check.
        """
        return self.parser.get_keystrokes(km_id)

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
