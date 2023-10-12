import json
import statistics
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, TypedDict, Union
from os import path
OUTLIER_CUTOFF = 0.8
from config import ROOT, ABSOLUTE_FILENAME
# LOG_FILENAME = 'test.json'
# class Keystroke: Tuple[str, Optional[float]]
class Keystroke:
    def __init__(self, key: str, time: Optional[float]):
        self.key = key
        self.time = time
    def __iter__(self):
        yield self.key, self.time
    def __getitem__(self, index: int) -> Union[str, Optional[float]]:
        if index == 0:
            return self.key
        elif index == 1:
            return self.time
        else:
            raise IndexError("Index out of range.")
class Log(TypedDict):
    id: str
    string: str
    keystrokes: List[Keystroke]
class KeystrokeParser:
    """
    A class used to parse and analyze keystroke logs.

    Attributes:
        filename (str): The name of the file to load logs from.
        logs (list): The list of logs loaded from the file.
        exclude_outliers (bool): A flag indicating whether to exclude outliers.
    """
    def __init__(self, filename: Optional[str] = None, exclude_outliers: bool = True) -> None:
        """
        Initialize the KeystrokeParser and load logs.

        Args:
            filename (str, optional): The name of the file to load logs from. Defaults to ABSOLUTE_FILENAME.
            exclude_outliers (bool, optional): A flag indicating whether to exclude outliers. Defaults to True.
        """
        if filename is None:
            filename = ABSOLUTE_FILENAME
        else:
            filename = path.join(ROOT, filename)
        self.filename = filename
        self.logs = self.extract_logs()
        self.exclude_outliers = exclude_outliers

    def extract_logs(self) -> List[Log]:
        """
        Reads logfile and extracts logs.

        Returns:
            list: A list of logs loaded from the file. If an error occurs, an empty list is returned.
        """
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
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
        for log in self.logs:
            if log['id'] == identifier or log['string'] == identifier:
                return True
        return False

    def id_from_substring(self, keyword: str) -> Optional[str]:
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
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return []
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    return [log['string']]
        return [log['string'] for log in self.logs]
    
    def print_strings(self, identifier: Optional[str] = None, truncate: int = 25) -> None:
        """
        Prints strings from logs. If 'identifier' is provided, prints associated string.
        Strings longer than 'truncate' value are appended with "...[truncated]".

        Args:
            identifier (str, optional): The UUID or exact string to check for.
            truncate (int, optional): Maximum length for printed strings. Defaults to 25.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if not isPresent:
                print("ID invalid, no strings found.")
                return
        string_list = self.get_strings(identifier)
        print(f"Number of strings: {len(string_list)}")
        for curr_string in string_list:
            if truncate > 0 and len(curr_string) > truncate:
                curr_string = curr_string[:truncate] + "...[truncated]"
            # Newlines get annoying, so replace them with "\n"
            curr_string = curr_string.replace("\n", "\\n")
            print(curr_string)


    def get_only_times(self, identifier: Optional[str] = None, exclude_outliers: Optional[bool] = None) -> List[float]:
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
        none_count = 0
        outlier_count = 0
        times = []
        if keystrokes == []:
            print("No keystrokes found.")
            return []
        for (_, time) in keystrokes:
            if time is None:
                none_count += 1
                if none_count > 1:
                    print('Critical Error. Keystrokes invalid. Too many nuns!')
                continue
            elif (exclude_outliers is False) or (time < OUTLIER_CUTOFF):
                times.append(time)
            else:
                # This means time < OUTLIER_CUTOFF right?
                outlier_count += 1
        if outlier_count > 0:
            print(f"Removed {outlier_count} outliers.")
        return times
    
    def wpm(self, identifier: Optional[str] = None) -> Optional[float]:
        """
        Calculate the average words per minute.
        Formula is CPM/5, where CPM is characters per minute.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            float or None: If no characters are found, None is returned.
        """
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
    
    def get_highest_keystroke_times(self, identifier: Optional[str] = None) -> List[float]:
        """
        Get the highest keystroke time for each log.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of float values.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent is False:
                return []
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    # times = [keystroke[1] for keystroke in log['keystrokes']]
                    times = self.get_only_times(identifier)
                    return [max(times) if times else 0]
            print("I should never get here, right?")
            return []
        highest_times = []
        # iterate through logs
        for log in self.logs:
            id = log['id']
            times = self.get_only_times(id)
            highest_times.append(max(times) if times else 0)
        return highest_times
    
    def get_average_delay(self, identifier: Optional[str] = None) -> Optional[float]:
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

    def get_std_deviation(self, identifier: Optional[str] = None) -> Optional[float]:
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
    
    def visualize_keystroke_times(self, identifier: Optional[str] = None, keystrokes: Optional[List[Keystroke]] = None, 
                                  exclude_outliers: Optional[bool] = None) -> None:
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

        characters = list(character_times.keys())
        times = list(character_times.values())

        plt.bar(characters, times)
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time')
        line_2 = "\nExcluding Outliers" if self.exclude_outliers else ""
        plt.title('Average Keystroke Time for Each Character' + line_2)
        plt.show()

    def get_keystrokes(self, identifier: Optional[str] = None) -> List[Keystroke]:
        """
       Get a list of all keystrokes in the logs.

        Args:
            identifier (str, optional): The UUID or exact string to check for.

        Returns:
            list: A list of Keystroke items.
        """
        keystrokes = []
        for log in self.logs:
            if identifier is not None:
                if log['id'] == identifier or log['string'] == identifier:
                    keystrokes.extend(log['keystrokes'])
                    return keystrokes
            else:
                keystrokes.extend(log['keystrokes'])
            
        return keystrokes

    def map_chars_to_times(self, keystrokes: Optional[List[Keystroke]] = None, exclude_outliers: Optional[bool] = None) -> Dict[str, float]:
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
        if exclude_outliers is None:
            exclude_outliers = self.exclude_outliers
        none_count = 0
        for key, time in keystrokes:
            if time is None:
                none_count += 1
                if none_count > 1:
                    print('Critical Error. Keystrokes invalid. Too many nuns!')
                continue
            if exclude_outliers and time > OUTLIER_CUTOFF:
                continue
            if key in character_times:
                character_times[key] += time
                character_counts[key] += 1
            else:
                character_times[key] = time
                character_counts[key] = 1

        for key in character_times:
            character_times[key] /= character_counts[key]

        return character_times

if __name__ == "__main__":
    parser = KeystrokeParser()
    id = parser.id_from_substring("")
    print('Parser working!' if id else 'Get some keystrokes logged!')