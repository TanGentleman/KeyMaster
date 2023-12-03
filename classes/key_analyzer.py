# Standard library imports
from json import load as json_load
from json import dump as json_dump
import statistics
from typing import List, Dict

# Third party imports
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None # type: ignore

# KeyMaster imports
from utils.validation import Keystroke, KeystrokeList, Log, KeystrokeEncoder, is_id_in_log
from utils.helpers import get_filepath, resolve_filename

NUKABLE = True
OUTLIER_CUTOFF = 0.8


class KeyParser:
    """
    A class used to parse and analyze keystroke logs.
    The logs can be loaded from a file or passed in as a list of Log objects.
    A None value for filename will initialize an empty KeyParser.
    """

    def __init__(self, filename: str | None = 'REG',
                 exclude_outliers: bool = True) -> None:
        """
        Initialize the KeyParser and load logs. None value for filename will initialize an empty KeyParser.
        """
        self.filename = filename  # Client facing.
        self.exclude_outliers = exclude_outliers  # Client facing.
        self.logs: List[Log] = self.extract_logs()  # Not client facing.

    def load_logs(self) -> None:
        """Client facing.
        Load logs from the file.
        """
        self.logs = self.extract_logs()

    def extract_logs(self) -> List[Log]:
        """Not client facing.
        Reads logfile and extracts logs.

        Returns:
            `list`: A list of logs loaded from the file. If an error occurs, an empty list is returned.
        """
        if self.filename is None:
            # print("No filename assigned.")
            return []
        filepath = get_filepath(self.filename)
        if not filepath:
            print("No filepath found.")
            return []
        try:
            with open(filepath, 'r') as f:
                log_contents = json_load(f)
            logs: List[Log] = []
            for log in log_contents:
                # Instantiate Keystrokes and replace them in each log
                keystrokes = [Keystroke(k[0], k[1]) for k in log['keystrokes']]
                log['keystrokes'] = keystrokes
                logs.append(log)
            return logs
        except FileNotFoundError:
            print("No log file found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def check_membership(self, identifier: str) -> bool:
        """Client facing.
        Check if a log with the identifier exists in the loaded logs.

        Args:
            `identifier` (`str`): The UUID or exact string to check for.

        Returns:
            `bool`: True if a log with the given UUID or exact string exists, False otherwise.
        """
        if not identifier:
            print("No identifier provided.")
            return False
        for log in self.logs:
            if is_id_in_log(identifier, log):
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
            print("No logs found. Returning None.")
            return None
        if index < 1:
            if index == 0:
                print("WARNING: Index begins at 1. Returning first log anyways.")
                index = 1
            else:
                raise ValueError("Index must be greater than 0.")
        if index > len(self.logs):
            print("Index too high. Returning the last id.")
            return self.logs[-1]['id']
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

    def get_strings(self, identifier: str | None = None) -> List[str]:
        """Client facing.
        Get a list of all strings in the logs. If an identifier is provided,
        only the associated string is included.

        Args:
            `identifier` (`str`, optional): The UUID or exact string to check for.

        Returns:
            `list`: A list of all strings in the logs. If an identifier is provided,
            the list contains the string associated with that identifier.
            If the identifier is not found, an empty list is returned.
        """
        if not self.logs:
            print("No logs found. Returning empty list.")
            return []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if not isPresent:
                return []
            for log in self.logs:
                if is_id_in_log(identifier, log):
                    return [log['string']]
        return [log['string'] for log in self.logs]

    def print_strings(self, max: int = 5, truncate: int = 25,
                      identifier: str | None = None) -> None:
        """Client facing.
        Prints strings from logs. If `identifier` is provided, prints associated string.
        Strings longer than `truncate` value are appended with "...[truncated]".

        Args:
            `max` (int): Maximum number of strings to print. Defaults to 5.
            `truncate` (int): Maximum number of characters to print. Defaults to 25.
            `identifier` (str, optional): The UUID or exact string to check for.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if not isPresent:
                print("ID invalid, no strings found.")
                return
            string_list = self.get_strings(identifier)
        else:
            string_list = self.get_strings()
        print(f"Total strings: {len(string_list)}")
        count = 0
        for curr_string in string_list:
            count += 1
            if count > max:
                print(f"First {max} strings printed.")
                break
            if truncate > 0 and len(curr_string) > truncate:
                curr_string = curr_string[:truncate] + "[...]"
            # Newlines get annoying, so replace them with "\n"
            # curr_string = curr_string.replace("\n", "\\n")
            print(f'{count}|{curr_string}')

    def get_only_times(self, identifier: str | None = None,
                       exclude_outliers: bool | None = None) -> List[float]:
        """Not client facing.
        Get a list of all keystroke delay times.

        Args:
            `identifier` (str, optional): The UUID or exact string to check for.

        Returns:
            `List[float]`: A list of float values.
        """
        keystrokes = KeystrokeList()
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return []
            keystrokes = self.get_keystrokes(identifier)
        else:
            keystrokes = self.get_keystrokes()
        if keystrokes.is_empty():
            print("No keystrokes found.")
            return []
        
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        outlier_count = 0
        times: List[float] = []
        
        for keystroke in keystrokes:
            time = keystroke.time
            if time is None:
                continue
            elif time > OUTLIER_CUTOFF and exclude_outliers:
                outlier_count += 1
                continue
            else:
                times.append(time)
        if outlier_count > 0:
            print(f"Removed {outlier_count} outliers in getting keystroke times.")
        return times

    def wpm(self, identifier: str | None = None) -> float | None:
        """Client facing.
        Calculate the average words per minute.
        Formula is CPM/5, where CPM is characters per minute.

        Args:
            `identifier` (str, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: If no characters are found, None is returned.
        """
        if not self.logs:
            print("No logs found.")
            return None
        num_chars = 0
        total_seconds = 0
        # If identifier is provided, calculate WPM for specific log
        if identifier is not None:
            if not self.check_membership(identifier):
                return None
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    times = self.get_only_times(identifier)
                    num_chars = len(times)
                    total_seconds = sum(times) # type: ignore
                    break
        # If identifier is not provided, calculate WPM for all logs
        else:
            times = self.get_only_times()
            num_chars = len(times)
            total_seconds = sum(times) # type: ignore

        if num_chars == 0 or total_seconds == 0:
            print("Num_chars or total_seconds is 0. Unable to get WPM.")
            return None

        # Calculate the CPM
        cpm = (num_chars / total_seconds) * 60
        return round(cpm / 5, 1)

    def get_highest_keystroke_times(
            self, identifier: str | None = None) -> List[float]:
        """Client facing.
        Get the highest keystroke time for each log.

        Args:
            `identifier` (str, optional): The UUID or exact string to check for.

        Returns:
            `list`: A list of float values.
        """
        if not self.logs:
            print("No logs found.")
            return []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return []
            times = self.get_only_times(identifier)
            if len(times) == 0:
                print("No keystroke times found.")
                return []
            return [max(times)]
        highest_times = []
        # iterate through logs
        for log in self.logs:
            id = log['id']
            times = self.get_only_times(id)
            if times:
                highest_times.append(max(times))
        return highest_times

    def get_average_delay(self, identifier: str | None = None) -> float | None:
        """Client facing.
        Get the average time between keystrokes.

        Args:
            `identifier` (str, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: Return average delay in seconds. If no keystroke times are found, None is returned.
        """
        times = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return None
            times = self.get_only_times(identifier)
        else:
            times = self.get_only_times()
        if len(times) == 0:
            print("No keystrokes found.")
            return 0
        return round(sum(times) / len(times), 4)

    def get_std_deviation(self, identifier: str | None = None) -> float | None:
        """Client facing.
        Get the standard deviation of the time between keystrokes.

        `Args`:
            `identifier (`str`, optional): The UUID or exact string to check for.

        Returns:
            `float` or `None`: If insufficient keystrokes are found, None is returned.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return None
            times = self.get_only_times(identifier)
        else:
            times = self.get_only_times()
        if len(times) < 2:
            print("Not enough keystrokes to calculate standard deviation.")
            return None
        return round(statistics.stdev(times), 4)

    def plot_keystroke_times(self, character_times: Dict[str, float]):
        """Not client facing.
        Plots a bar chart of the average keystroke times for each character.

        :param character_times: A dictionary mapping each character to its average keystroke time.
        :type character_times: Dict[str, float]
        """
        if plt is None:
            print("Matplotlib not installed. Cannot visualize.")
            return
        # Prepare data for plotting
        characters = list(character_times.keys())
        times = list(character_times.values())

        # Create the bar chart
        plt.figure(figsize=(15, 5))
        plt.bar(characters, times, color='skyblue')

        # Add labels and title
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time (s)')
        plt.title('Average Keystroke Times by Character')

        # Rotate x-axis labels for better readability if there are many
        # characters
        plt.xticks(rotation=45, ha='right')

        # Show the plot
        plt.tight_layout()
        plt.show()

    def visualize_keystroke_times(
            self,
            identifier: str | None = None,
            keystrokes: KeystrokeList | None = None,
            exclude_outliers: bool | None = None) -> None:
        """Client facing.
        Plots the average keystroke time for each character.

        Args:
            `identifier` (`str`, optional): The UUID or exact string to check for.
            `keystrokes`: (`KeystrokeList`, optional): A list of Keystroke items.
            `exclude_outliers` (bool, optional): A flag indicating whether to exclude outliers.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                print("ID invalid, no strings found.")
                return
            keystrokes = self.get_keystrokes(identifier)
        elif keystrokes is None:
            keystrokes = self.get_keystrokes()

        if keystrokes.is_empty():
            print("No keystrokes found.")
            return

        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        character_times = self.map_chars_to_times(keystrokes, exclude_outliers)
        if not character_times:  # If no characters found
            print("No characters to visualize.")
            return
        self.plot_keystroke_times(character_times)

    def get_keystrokes(self, identifier: str | None = None) -> KeystrokeList:
        """Client facing.
       Get a list of all keystrokes in the logs.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of Keystroke items.
        """
        keystrokes: List[Keystroke] = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return KeystrokeList()
        for log in self.logs:
            if identifier is not None and is_id_in_log(identifier, log):
                keystrokes.extend(log['keystrokes'])
                return KeystrokeList(keystrokes)
            else:
                keystrokes.extend(log['keystrokes'])

        return KeystrokeList(keystrokes)

    def refactor_special_key(self, key: str) -> str:
        """Not client facing.
        Replace special key names with more readable versions for display.
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
                           exclude_outliers: bool | None = None) -> Dict[str,
                                                                         float]:
        """Not client facing.
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            `keystrokes` (list, optional): A list of Keystroke items.

        Returns:
            `dict`: A dictionary mapping each character to its average keystroke time.
        """
        character_times: Dict[str, float] = {}
        character_counts: Dict[str, int] = {}
        if keystrokes is None:
            keystrokes = self.get_keystrokes()
        if keystrokes.is_empty():
            print("No keystrokes to map.")
            return {}
        # Else ensure keystrokes are valid
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers

        outlier_count = 0
        for keystroke in keystrokes:
            # I am removing the validity check because it is not necessary
            # if not keystroke.valid:
            #     continue
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
            print("No characters to map.")
            return {}
        if outlier_count > 0:
            print(f"Removed {outlier_count} outliers in mapping characters to average times.")
        return character_times

    def compare_keystroke_lists(
            self, list_of_keystroke_lists: List[KeystrokeList]) -> None:
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
            print("No logs found.")
            return
        unique_strings = []
        unique_logs = []
        for log in self.logs:
            string = log['string']
            if string not in unique_strings:
                unique_strings.append(string)
                unique_logs.append(log)

        if len(unique_logs) == len(self.logs):
            print("No duplicates found.")
            return
        print(f"Removed {len(self.logs) - len(unique_logs)} duplicates.")
        print(f"Use KeyParser.confirm_nuke() to save changes.")
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
            print("No logs loaded.")
            return
        if self.logs == self.extract_logs():
            print("No changes made.")
            return
        if self.filename is None:
            print("No logfile set.")
            return

        filepath = get_filepath(self.filename)
        if filepath is None:
            print("No filepath found.")
            return
        try:
            with open(filepath, 'w') as f:
                json_dump(self.logs, f, cls=KeystrokeEncoder)
                print("Logfile adjusted.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        
    def __repr__(self) -> str:
        pretty_string = (
            f"# Configuration:\nfile={resolve_filename(self.filename)},\nexclude_outliers={self.exclude_outliers},\n" +
            f"{len(self.logs)} logs loaded.")
        return pretty_string

    def __str__(self) -> str:
        return self.__repr__()
    
    def __len__(self) -> int:
        return len(self.logs)


if __name__ == "__main__":
    parser = KeyParser()
    id = parser.id_from_substring("")
    print('Parser active!' if id else 'Get some keystrokes logged!')
