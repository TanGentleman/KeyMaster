# KeyMaster imports
from utils.helpers import get_filepath, resolve_filename
from utils.validation import KeystrokeDecoder, KeystrokeList, Log, KeystrokeEncoder
from utils.config import STOP_KEY

# Standard library imports
from json import load as json_load
from json import dump as json_dump
import statistics
import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

# Third party imports
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # type: ignore


OUTLIER_CUTOFF = 3.0  # seconds


class KeyParser:
    """
    A class used to parse and analyze keystroke logs.

    Attributes:
    ----------
    - filename (`str`): The filename of the log file.
    - exclude_outliers (`bool`): A flag indicating whether to exclude outliers.
    - logs (`list`): A list of Log objects.
    """

    def __init__(self, filename: str | None = 'REG',
                 exclude_outliers: bool = True,
                 preload: bool = True) -> None:
        """
        Initialize the KeyParser and load logs. None value for filename will initialize an empty KeyParser.
        """
        self.filename = filename  # Client facing.
        self.exclude_outliers = exclude_outliers  # Client facing.
        # Not client facing.
        self.logs: list[Log] = []
        if preload:
            self.logs = self.extract_logs()
            logging.info(f"Loaded {len(self.logs)} logs.")

    def load_logs(self) -> None:
        """Client facing.
        Load logs from the file.
        """
        self.logs = self.extract_logs()

    def extract_logs(self) -> list[Log]:
        """Not client facing.
        Reads logfile and extracts logs.

        Returns:
            `list`: A list of logs loaded from the file. If an error occurs, an empty list is returned.
        """
        if self.filename is None:
            logging.warning("No filename assigned.")
            return []
        filepath = get_filepath(self.filename)
        if not filepath:
            logging.warning("No filepath found.")
            return []
        try:
            with open(filepath, 'r') as f:
                logs: list[Log] = json_load(f, cls=KeystrokeDecoder)
            return logs
        except FileNotFoundError:
            logging.warning("No log file found.")
            return []
        except Exception as e:
            logging.error(f"An error occurred! {e}")
            return []

    def is_id_present(self, km_id: str, log: Log | None = None) -> bool:
        """Client facing.
        Check if a log with the id exists in the loaded logs.

        Args:
            `km_id` (`str`): The UUID or exact string formatted as STOP_KEY + string
            `log` (`Log`): The log to check.

        Returns:
            `bool`: True if a log with the given UUID or exact string exists, False otherwise.
        """
        if not km_id:
            logging.error("No id provided.")
            return False
        if log is not None:
            if log['id'] == km_id:
                return True
            if km_id[0] == STOP_KEY:
                if log['string'] == km_id[1:]:
                    return True
                else:
                    logging.info('Exact string not found.')
            return False
        else:
            for unchecked_log in self.logs:
                if self.is_id_present(km_id, unchecked_log):
                    return True
            return False

    def id_by_index(self, index: int) -> str | None:
        """Client facing.
        Get the ID of the log at a given index.
        Index begins at 1, as labeled in method `print_strings`.

        Args:
            `index` (`int`): The index of the log to get the ID of.

        Returns:
            `str` or `None`: The ID of the log at the given index. If no such log is found, `None` is returned.
        """
        if not self.logs:
            logging.warning("No logs found.")
            return None
        if index < 1:
            if index == 0:
                logging.warning(
                    "Index begins at 1. Returning first log anyways.")
                index = 1
            else:
                raise ValueError("Index must be greater than 0.")
        if index > len(self.logs):
            raise ValueError("Index too high.")
        return self.logs[index - 1]['id']

    def id_from_substring(self, keyword: str) -> str | None:
        """Client facing.
        Get the ID of the first log that contains a given substring.

        Args:
            `keyword` (`str`): The substring to search for.

        Returns:
            `str` or `None`: The ID of the first log that contains the substring. If no such log is found, `None` is returned.
        """
        for log in self.logs:
            if keyword == log['string'] or keyword in log['string']:
                return log['id']
        return None

    def get_strings(self, km_id: str | None = None) -> list[str]:
        """Client facing.
        Get a list of all strings in the logs. If an id is provided,
        only the associated string is included.

        Args:
            `km_id` (`str`, optional): The UUID or exact string to check for.

        Returns:
            `list`: A list of all strings in the logs. If an id is provided,
            the list contains the string associated with that id.
            If the id is not found, an empty list is returned.
        """
        if not self.logs:
            return []
        if km_id is not None:
            isPresent = self.is_id_present(km_id)
            if isPresent is False:
                logging.error("ID invalid.")
                return []
            for log in self.logs:
                if self.is_id_present(km_id, log):
                    return [log['string']]
        return [log['string'] for log in self.logs]

    def print_strings(self,
                      max: int = 5,
                      truncate: int = 25,
                      km_id: str | None = None) -> None:
        """Client facing.
        Prints strings from logs. If `id` is provided, prints associated string.
        Strings longer than `truncate` value are appended with "...[truncated]".

        Args:
            `max` (int): Maximum number of strings to print. Defaults to 5.
            `truncate` (int): Maximum number of characters to print. Defaults to 25.
            `km_id` (str, optional): The UUID or exact string to check for.
        """
        if km_id is not None:
            isPresent = self.is_id_present(km_id)
            if not isPresent:
                logging.error("ID invalid.")
                return
            string_list = self.get_strings(km_id)
        else:
            string_list = self.get_strings()
        logging.info(f"Total strings: {len(string_list)}")
        count = 0
        for curr_string in string_list:
            count += 1
            if count > max:
                logging.info(f"First {max} strings printed.")
                break
            if truncate > 0 and len(curr_string) > truncate:
                curr_string = curr_string[:truncate] + "[...]"
            logging.info(f'{count}|{curr_string}')

    def get_only_times(self,
                       keystrokes: KeystrokeList | None = None,
                       exclude_outliers: bool | None = None,
                       km_id: str | None = None,
                       ) -> list[float]:
        """Not client facing.
        Get a list of all keystroke delay times.

        Args:
            `km_id` (str, optional): The UUID or exact string to check for.

        Returns:
            `list[float]`: A list of float values.
        """
        if keystrokes is None:
            if km_id is not None:
                isPresent = self.is_id_present(km_id)
                if isPresent is False:
                    logging.error("ID invalid.")
                    return []
                keystrokes = self.get_keystrokes(km_id)
            else:
                keystrokes = self.get_keystrokes()
        if keystrokes.is_empty():
            logging.warning("No keystrokes found.")
            return []
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        outlier_count = 0
        outliers = []
        times: list[float] = []
        for keystroke in keystrokes:
            time = keystroke.time
            if time is None:
                continue
            elif time > OUTLIER_CUTOFF and exclude_outliers:
                outliers.append((keystroke.key, time))
                outlier_count += 1
                continue
            else:
                times.append(time)
        if outlier_count > 0:
            logging.info(f"{outlier_count} Outlier times removed:\n{outliers}")
        return times

    def wpm(self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> float | None:
        """Client facing.
        Calculate the average words per minute.
        Formula is CPM/5, where CPM is characters per minute.

        Args:
            `km_id` (str, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: If no characters are found, None is returned.
        """

        num_chars = 0
        total_seconds = 0
        # If id is provided, calculate WPM for specific log
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        if keystrokes is None:
            if not self.logs:
                logging.warning("No logs found.")
                return None
            if km_id is not None:
                if not self.is_id_present(km_id):
                    return None
                times = self.get_only_times(
                    exclude_outliers=exclude_outliers, km_id=km_id)
                num_chars = len(times)
                total_seconds = sum(times)  # type: ignore
            # If id is not provided, calculate WPM for all logs
            else:
                times = self.get_only_times(exclude_outliers=exclude_outliers)
                num_chars = len(times)
                total_seconds = sum(times)  # type: ignore
        else:
            times = self.get_only_times(
                keystrokes, exclude_outliers=exclude_outliers,)
            num_chars = len(times)
            total_seconds = sum(times)  # type: ignore
        if num_chars == 0 or total_seconds == 0:
            logging.warning(
                "Num_chars or total_seconds is 0. Unable to get WPM.")
            return None

        # Calculate the CPM
        cpm = (num_chars / total_seconds) * 60
        return round(cpm / 5, 1)

    def get_highest_keystroke_times(
            self,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> list[float]:
        """Client facing.
        Get the highest keystroke time for each log.

        Args:
            `km_id` (str, optional): The UUID or exact string to check for.

        Returns:
            `list`: A list of float values.
        """
        if not self.logs:
            logging.warning("No logs found.")
            return []
        if km_id is not None:
            isPresent = self.is_id_present(km_id)
            if isPresent is False:
                logging.error("ID invalid.")
                return []
            times = self.get_only_times(
                exclude_outliers=exclude_outliers, km_id=km_id)
            if len(times) == 0:
                logging.warning("No keystroke times found.")
                return []
            return [max(times)]
        highest_times: list[float] = []
        # iterate through logs
        for log in self.logs:
            keystrokes = log['keystrokes']
            times = self.get_only_times(
                keystrokes, exclude_outliers=exclude_outliers)
            if times:
                highest_times.append(max(times))
        return highest_times

    def get_average_delay(
            self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> float | None:
        """Client facing.
        Get the average time between keystrokes.

        Args:
            `km_id` (str, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: Return average delay in seconds. If no keystroke times are found, None is returned.
        """
        times = []
        if keystrokes is None:
            if km_id is not None:
                isPresent = self.is_id_present(km_id)
                if isPresent is False:
                    logging.error("ID invalid.")
                    return None
                times = self.get_only_times(
                    exclude_outliers=exclude_outliers, km_id=km_id)
            else:
                times = self.get_only_times(exclude_outliers=exclude_outliers)
        else:
            times = self.get_only_times(
                keystrokes, exclude_outliers)
        if len(times) == 0:
            logging.warning("No keystrokes found.")
            return None
        return round(sum(times) / len(times), 4)

    def get_std_deviation(
            self,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> float | None:
        """Client facing.
        Get the standard deviation of the time between keystrokes.

        `Args`:
            `km_id (`str`, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: If insufficient keystrokes are found, None is returned.
        """
        times = []
        if keystrokes is None:
            if km_id is not None:
                isPresent = self.is_id_present(km_id)
                if isPresent is False:
                    logging.error("ID invalid.")
                    return None
                times = self.get_only_times(
                    exclude_outliers=exclude_outliers, km_id=km_id)
            else:
                times = self.get_only_times(exclude_outliers=exclude_outliers)
        else:
            times = self.get_only_times(
                keystrokes, exclude_outliers)
        if len(times) < 2:
            logging.warning(
                "Not enough keystrokes to calculate standard deviation.")
            return None
        return round(statistics.stdev(times), 4)

    def plot_boxplot(
            self,
            keystrokes: KeystrokeList,
            exclude_outliers: bool | None = None) -> None:
        """Not client facing.
        Plots a boxplot of the keystroke times.

        Args:
            `keystrokes` (`KeystrokeList`): A list of Keystroke items.
            `exclude_outliers` (bool, optional): A flag indicating whether to exclude outliers.
        """
        if plt is None:
            logging.warning("Matplotlib not installed. Cannot visualize.")
            return
        if keystrokes.is_empty():
            logging.warning("No keystrokes found.")
            return
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        times = self.get_only_times(keystrokes, exclude_outliers)
        if len(times) == 0:
            logging.warning("No keystroke times found.")
            return
        plt.figure(figsize=(15, 10))
        plt.boxplot(times, vert=False)
        plt.xlabel('Keystroke Time (s)')
        plt.title('Keystroke Times')
        plt.tight_layout()
        plt.show()

    def plot_bar(self,
                 character_times: dict[str, float],
                 save_file=False,
                 display=True) -> None:
        """Not client facing.
        Plots a bar chart of the average keystroke times for each character.

        :param character_times: A dictionary mapping each character to its average keystroke time.
        :type character_times: dict[str, float]
        """
        if plt is None:
            logging.warning("Matplotlib not installed. Cannot visualize.")
            return
        # Prepare data for plotting
        characters = list(character_times.keys())
        times = list(character_times.values())

        plt.figure(figsize=(15, 10))
        # plt.scatter(characters, times, color='skyblue') # Scatter plot!
        plt.bar(characters, times, color='skyblue')  # type: ignore
        # plt.barh(characters, times, color='skyblue')
        # Add labels and title
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time (s)')
        plt.title('Average Keystroke Times by Character')

        # Rotate x-axis labels for long strings
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        if save_file:
            plt.savefig('keystroke_times.png', dpi=200)
        plt.show(block=display)
        return

    def visualize(
            self,
            mode: str | None = None,
            save_file: bool | None = None,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None,
            km_id: str | None = None) -> None:
        """Client facing.
        Plots the average keystroke time for each character.

        Args:
            `km_id` (`str`, optional): The UUID or exact string to check for.
            `keystrokes`: (`KeystrokeList`, optional): A list of Keystroke items.
            `exclude_outliers` (bool, optional): A flag indicating whether to exclude outliers.
        """
        if keystrokes is not None:
            if km_id is not None:
                isPresent = self.is_id_present(km_id)
                if isPresent is False:
                    logging.error("ID invalid.")
                    return
                keystrokes = self.get_keystrokes(km_id)
        else:
            keystrokes = self.get_keystrokes()

        if keystrokes.is_empty():
            logging.warning("No keystrokes found.")
            return
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        if save_file is None:
            save_file = False
        if mode is None:
            mode = 'bar'
        if mode == 'bar':
            character_times = self.map_chars_to_times(
                keystrokes, exclude_outliers)
            if not character_times:  # If no characters found
                logging.warning("No characters to visualize.")
                return
            self.plot_bar(character_times, save_file=save_file)
        elif mode == 'box':
            self.plot_boxplot(keystrokes, exclude_outliers)

    def get_keystrokes(self, km_id: str | None = None) -> KeystrokeList:
        """Client facing.
       Get a list of all keystrokes in the logs.

        Args:
            km_id (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of Keystroke items.
        """
        keystrokes = KeystrokeList()
        if km_id is not None:
            isPresent = self.is_id_present(km_id)
            if isPresent is False:
                logging.error("ID invalid.")
                return keystrokes
        for log in self.logs:
            if km_id is not None and self.is_id_present(km_id, log):
                keystrokes.extend(log['keystrokes'])
                return keystrokes
            else:
                keystrokes.extend(log['keystrokes'])

        return keystrokes

    def refactor_special_key(self, key: str) -> str:
        """Not client facing.
        Replace special key names with more readable versions for display.
        These may be changed in the future.
        """
        display_names = {
            "'STOP'": "Stop",
            "'Key.space'": "Space",
            "'Key.enter'": "Enter",
            "'Key.backspace'": "Backspace",
            "'Key.tab'": "Tab",
            "'Key.caps_lock'": "Caps Lock",
            "'Key.shift'": "Shift",
        }
        return display_names.get(key, key)

    def map_chars_to_times(self,
                           keystrokes: KeystrokeList | None = None,
                           exclude_outliers: bool | None = None) -> dict[str,
                                                                         float]:
        """Not client facing.
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            `keystrokes` (list, optional): A list of Keystroke items.

        Returns:
            `dict`: A dictionary mapping each character to its average keystroke time.
        """
        character_times: dict[str, float] = {}
        character_counts: dict[str, int] = {}
        if keystrokes is None:
            keystrokes = self.get_keystrokes()
        if keystrokes.is_empty():
            logging.warning("No keystrokes to map.")
            return {}
        # Else ensure keystrokes are valid
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers

        outlier_count = 0
        outliers = []
        for keystroke in keystrokes:

            legal_key = keystroke.legal_key
            if legal_key is None:
                continue
            if legal_key.is_special:
                key = self.refactor_special_key(legal_key.key)
            else:
                key = legal_key.key
            time = keystroke.time
            if time is None:
                continue
            if time > OUTLIER_CUTOFF and exclude_outliers:
                outlier_count += 1
                outliers.append((key, time))
                continue
            if key in character_times:
                character_times[key] += time
                character_counts[key] += 1
            else:
                character_times[key] = time
                character_counts[key] = 1

        for key in character_times:
            character_times[key] /= character_counts[key]
        if not character_times:
            logging.warning("No character times to map.")
            return {}
        if outlier_count > 0:
            logging.info(f"{outlier_count} Outliers removed:\n{outliers}")
        return character_times

    def compare_keystroke_lists(
            self, list_of_keystroke_lists: list[KeystrokeList]) -> None:
        """Not client facing.
        Compare the keystroke times of multiple lists of keystrokes.
        """
        # TODO: Utilize map_chars_to_times
        return None

    def nuke_duplicates(self) -> None:
        """Client facing.
        Remove duplicate logs from the logs list.
        """
        if not self.logs:
            logging.warning("No logs found.")
            return
        unique_strings = set()
        unique_logs = []
        for log in self.logs:
            string = log['string']
            if string not in unique_strings:
                unique_strings.add(string)
                unique_logs.append(log)

        if len(unique_logs) == len(self.logs):
            logging.info("No duplicates found.")
            return
        logging.info(f"Removed {len(self.logs) - len(unique_logs)} duplicates.")
        logging.info(f"KeyParser allows confirm_nuke() to finalize changes.")
        self.logs = unique_logs

    def confirm_nuke(self) -> None:
        """Client facing.
        This is a fun alias for dump_modified_logs.
        """
        self.dump_modified_logs()

    def dump_modified_logs(self) -> None:
        """Client facing.
        Save the changes to the logfile (likely made by nuke_duplicates).
        """
        if not self.logs:
            logging.warning("No logs loaded.")
            return
        if self.logs == self.extract_logs():
            logging.warning("No changes made.")
            return
        if self.filename is None:
            logging.warning("No logfile set.")
            return

        filepath = get_filepath(self.filename)
        if filepath is None:
            logging.warning("No filepath found.")
            return
        try:
            with open(filepath, 'w') as f:
                json_dump(self.logs, f, cls=KeystrokeEncoder)
                logging.info("Logfile adjusted.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return

    def stats(self,
              keystrokes: KeystrokeList | None = None,
              exclude_outliers: bool | None = None,
              km_id: str | None = None,
              ) -> list[None | int | float] | None:
        """Client facing.
        Print statistics for the given log.
        PRECONDITION: km_id is valid if provided.
        """
        if keystrokes is None:
            if km_id is not None:
                # In the future, I can have this line instead be:
                # assert self.is_id_present(km_id), "ID invalid."
                isPresent = self.is_id_present(km_id)
                if isPresent is False:
                    logging.error("ID invalid.")
                    return None
                keystrokes = self.get_keystrokes(km_id)
            else:
                keystrokes = self.get_keystrokes(km_id)
        if keystrokes.is_empty():
            logging.warning("No keystrokes found.")
            return None
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        keystroke_count = len(keystrokes)
        average_delay = self.get_average_delay(keystrokes, exclude_outliers)
        std_deviation = self.get_std_deviation(keystrokes, exclude_outliers)
        highest_keystroke_time = max(
            self.get_only_times(
                keystrokes, exclude_outliers))
        wpm = self.wpm(keystrokes, exclude_outliers)
        # TODO: Handle Outliers
        logging.info(f"Total keystrokes: {keystroke_count}")
        logging.info(f"Average delay: {average_delay}")
        logging.info(f"Standard deviation: {std_deviation}")
        logging.info(f"Highest keystroke time: {highest_keystroke_time}")
        logging.info(f"Average WPM: {wpm}")
        return [
            keystroke_count,
            average_delay,
            std_deviation,
            highest_keystroke_time,
            wpm]

    def __repr__(self) -> str:
        pretty_string = (
            f"# Configuration:\nfile={resolve_filename(self.filename)},\nexclude_outliers={self.exclude_outliers},\n" +
            f"{len(self.logs)} logs loaded.")
        return pretty_string

    def __len__(self) -> int:
        return len(self.logs)
