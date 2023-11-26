# Standard library imports
from json import load as json_load
from json import dump as json_dump
import statistics
import matplotlib.pyplot as plt
from typing import List, Dict

# KeyMaster imports
from utils.config import STOP_KEY
from utils.validation import Keystroke, Log, KeystrokeEncoder
from utils.helpers import get_filepath

NUKABLE = True
OUTLIER_CUTOFF = 0.8

# Function to see if an identifier is present in a log
def is_id_in_log(identifier: str, log: Log) -> bool:
    """
    Check if a log with the identifier exists in the loaded logs.

    Args:
        identifier (str): The UUID or exact string formatted as "*string". (* is the STOP_KEY)
        log (Log): The log to check.

    Returns:
        bool: True if a log with the given UUID or exact string exists, False otherwise.
    """
    if not identifier:
        print("No identifier provided.")
        return False
    if not log:
        print("No log provided.")
        return False
    if log['id'] == identifier:
        return True
    if identifier[-1] == STOP_KEY and log['string'] == identifier[1:]:
        return True
    return False

class KeyParser:
    """
    A class used to parse and analyze keystroke logs.

    Attributes:
        filename (str): The name of the file to load logs from.
        logs (list): The list of logs loaded from the file.
        exclude_outliers (bool): A flag indicating whether to exclude outliers.
    """
    def __init__(self, filename: str | None = 'REG', exclude_outliers: bool = True) -> None:
        """
        Initialize the KeyParser and load logs.

        Args:
            filename (str, optional): The name of the file to load logs from. Defaults to ABSOLUTE_REG_FILEPATH.
            exclude_outliers (bool, optional): A flag indicating whether to exclude outliers. Defaults to True.
        """
        self.filename = filename
        self.exclude_outliers = exclude_outliers
        self.logs: List[Log] = self.extract_logs()

    def load_logs(self) -> None:
        """
        Load logs from the file.
        """
        self.logs = self.extract_logs()
        
    def extract_logs(self) -> List[Log]:
        """
        Reads logfile and extracts logs.

        Returns:
            list: A list of logs loaded from the file. If an error occurs, an empty list is returned.
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
            logs:List[Log] = []
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
        """
        Check if a log with the identifier exists in the loaded logs.

        Args:
            identifier (str): The UUID or exact string to check for.

        Returns:
            bool: True if a log with the given UUID or exact string exists, False otherwise.
        """
        if not identifier:
            print("No identifier provided.")
            return False
        for log in self.logs:
            if is_id_in_log(identifier, log):
                return True
        return False
    
    def id_by_index(self, index: int) -> str | None:
        """
        Get the ID of the log at a given index. 
        Index begins at 1, as labeled in method print_strings.

        Args:
            index (int): The index of the log to get the ID of.

        Returns:
            str or None: The ID of the log at the given index. If no such log is found, None is returned.
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
        return self.logs[index-1]['id']

    def id_from_substring(self, keyword: str) -> str | None:
        """
        Get the ID of the first log that contains a given substring.

        Args:
            keyword (str): The substring to search for.

        Returns:
            str or None: The ID of the first log that contains the substring. If no such log is found, None is returned.
        """
        for log in self.logs:
            if keyword == log['string'] or keyword in log['string']:
                return log['id']
        return None

    def get_strings(self, identifier: str | None = None) -> List[str]:
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
    
    def print_strings(self, max: int = 5, truncate: int = 25, identifier: str | None = None) -> None:
        """
        Prints strings from logs. If 'identifier' is provided, prints associated string.
        Strings longer than 'truncate' value are appended with "...[truncated]".

        Args:
            max (int): Maximum number of strings to print. Defaults to 5.
            truncate (int): Maximum number of characters to print. Defaults to 25.
            identifier (str, optional): The UUID or exact string to check for.
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

    def get_only_times(self, identifier: str | None = None, exclude_outliers: bool | None = None) -> List[float]:
        """
        Get a list of all keystroke delay times.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            List[float]: A list of float values.
        """
        keystrokes = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return []
            keystrokes = self.get_keystrokes(identifier)
        else:
            keystrokes = self.get_keystrokes()

        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        outlier_count = 0
        times:List[float] = []
        if not keystrokes:
            print("No keystrokes found.")
            return []
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
            print(f"Removed {outlier_count} outliers.")
        return times
    
    def wpm(self, identifier: str | None = None) -> float | None:
        """
        Calculate the average words per minute.
        Formula is CPM/5, where CPM is characters per minute.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If no characters are found, None is returned.
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
                    num_chars = len(log['string'])
                    total_seconds = sum(self.get_only_times(identifier)) # type: ignore
                    break
        # If identifier is not provided, calculate WPM for all logs
        else:
            num_chars = sum(len(log['string']) for log in self.logs)
            total_seconds = sum(self.get_only_times()) # type: ignore

        # If no characters found
        if num_chars == 0:
            print("No characters found.")
            return None
        # If no time found
        if total_seconds == 0:
            print("No keystroke delay times found.")
            return None

        # Calculate the CPM
        cpm = (num_chars / total_seconds) * 60
        return round(cpm / 5, 1)
    
    def get_highest_keystroke_times(self, identifier: str | None = None) -> List[float]:
        """
        Get the highest keystroke time for each log.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of float values.
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
        """
        Get the average time between keystrokes.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If no keystroke times are found, None is returned.
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
            print ("No keystrokes found.")
            return 0
        return round(sum(times) / len(times), 4)

    def get_std_deviation(self, identifier: str | None = None) -> float | None:
        """
        Get the standard deviation of the time between keystrokes.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If insufficient keystrokes are found, None is returned.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return None
            times = self.get_only_times(identifier)
        else:
            times = self.get_only_times()
        if len(times) < 2:
            print ("Not enough keystrokes to calculate standard deviation.")
            return 0
        return round(statistics.stdev(times), 4)
    
    def visualize_keystroke_times(self, identifier: str | None = None, keystrokes: List[Keystroke] | None = None, 
                                  exclude_outliers: bool | None = None) -> None:
        """
        Plots the average keystroke time for each character.

        Args:
            identifier (str, optional): The UUID or exact string to check for.
            keystrokes (list, optional): A list of Keystroke items.
            exclude_outliers (bool, optional): A flag indicating whether to exclude outliers.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                print("ID invalid, no strings found.")
                return
            keystrokes = self.get_keystrokes(identifier)
        elif keystrokes is None:
            keystrokes = self.get_keystrokes()
        
        if keystrokes == []:
            print("No keystrokes found.")
            return
        
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        character_times = self.map_chars_to_times(keystrokes, exclude_outliers)
        if not character_times: # If no characters found
            print("No characters to visualize.")
            return
        characters = list(character_times.keys())
        times = list(character_times.values())

        plt.bar(characters, times)
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time')
        line_2 = "\nExcluding Outliers" if self.exclude_outliers else ""
        plt.title('Average Keystroke Time for Each Character' + line_2)
        plt.show()

    def get_keystrokes(self, identifier: str | None = None) -> List[Keystroke]:
        """
       Get a list of all keystrokes in the logs.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of Keystroke items.
        """
        keystrokes: List[Keystroke] = []
        for log in self.logs:
            if identifier is not None:
                if log['id'] == identifier or log['string'] == identifier:
                    keystrokes.extend(log['keystrokes'])
                    return keystrokes
            else:
                keystrokes.extend(log['keystrokes'])
            
        return keystrokes

    def map_chars_to_times(self, keystrokes: List[Keystroke] | None = None, exclude_outliers: bool | None = None) -> Dict[str, float]:
        """
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            keystrokes (list, optional): A list of Keystroke items.

        Returns:
            dict: A dictionary mapping each character to its average keystroke time.
        """
        character_times: Dict[str, float] = {}
        character_counts: Dict[str, int] = {}
        if keystrokes is None:
            keystrokes = self.get_keystrokes()
        elif not keystrokes:
            print("No keystrokes to map.")
            return {}
        # Else ensure keystrokes are valid
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers

        for keystroke in keystrokes:
            key = keystroke.key
            time = keystroke.time
            if time is None:
                continue
            if time > OUTLIER_CUTOFF and exclude_outliers:
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
        return character_times

    def visualize_keystroke_differences(self, keystrokes1: List[Keystroke], keystrokes2: List[Keystroke]) -> None:
        # Extract the keys and times from the keystrokes
        # assert all keys are valid
        assert(keystroke.valid for keystroke in keystrokes1)
        assert(keystroke.valid for keystroke in keystrokes2)
        # Get the intersection of the two lists
        assert(key1 == key2 for key1, key2 in zip(keystrokes1, keystrokes2))
        # This optional statement asserts that the keystrokes are the same length
        # assert (len(keystrokes1) == len(keystrokes2))
        keys1 = [keystroke.key for keystroke in keystrokes1]
        times1 = [keystroke.time if keystroke.time else 0.0 for keystroke in keystrokes1]
        length1 = len(keys1)

        keys2 = [keystroke.key for keystroke in keystrokes2]
        times2 = [keystroke.time if keystroke.time else 0.0 for keystroke in keystrokes2]
        length2 = len(keys2)

        # Create a bar chart for each key
        # Iterate through a list of all the unique keystroke.key values
        length = len(keys1)
        for i in range(length):
            # Get the times for each person
            # Plot the bar chart
            plt.figure()
            plt.bar(['Person 1', 'Person 2'], [times1[i], times2[i]])
            plt.title(f'Keystroke: {keys1[i]}')
            plt.xlabel('Person')
            plt.ylabel('Count')
            plt.show()

    def nuke_duplicates(self) -> None:
        """
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
        """
        This is a fun alias for dump_modified_logs.
        """
        self.dump_modified_logs()

    def dump_modified_logs(self) -> None:
        """
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

if __name__ == "__main__":
    parser = KeyParser()
    id = parser.id_from_substring("")
    print('Parser working!' if id else 'Get some keystrokes logged!')