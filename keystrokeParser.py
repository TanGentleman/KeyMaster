import json
import statistics
import matplotlib.pyplot as plt
OUTLIER_CUTOFF = 0.8
from config import ABSOLUTE_FILENAME
# LOG_FILENAME = 'test.json'
class KeystrokeParser:
    """
    A class used to parse keystroke logs.
    """
    def __init__(self, filename=ABSOLUTE_FILENAME, exclude_outliers=True):
        """
        Initialize the KeystrokeParser with a filename and load logs.
        Outliers are excluded by default.
        """
        self.filename = filename
        self.logs = self.load_logs()
        self.exclude_outliers = exclude_outliers

    def load_logs(self) -> list:
        """
        Function to load logs from the file.
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

    def check_membership(self, identifier) -> bool:
        """
        Function to check if a log with the given UUID or exact string exists.
        """
        for log in self.logs:
            if log['id'] == identifier or log['string'] == identifier:
                return True
        return False

    def id_from_substring(self, keyword) -> str or None:
        """
        Function to return the ID of the first string that contains a given substring.
        """
        for log in self.logs:
            if keyword == log['string'] or keyword in log['string']:
                return log['id']
        return None

    def get_all_strings(self, identifier=None) -> list:
        """
        Function to return a list of all strings in the logs.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return []
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    return [log['string']]
        return [log['string'] for log in self.logs]
    
    def print_all_strings(self, identifier=None, truncate=25) -> None:
        """
        Function to print all strings in the logs.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if not isPresent:
                print("ID invalid, no strings found.")
                return
        string_list = self.get_all_strings(identifier)
        print(f"Number of strings: {len(string_list)}")
        for curr_string in string_list:
            if truncate > 0 and len(curr_string) > truncate:
                curr_string = curr_string[:truncate] + "...[truncated]"
            curr_string = curr_string.replace("\n", "\\n")
            print(curr_string)


    def get_only_times(self, identifier=None) -> list:
        """
        Function to return a list of all times in the logs.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return []
            keystrokes = self.get_all_keystrokes(identifier)
        else:
            keystrokes = self.get_all_keystrokes()
        outlier_count = 0
        times = []
        for (_, time) in keystrokes:
            if time == None:
                none_count += 1
                if none_count > 1:
                    print('Critical Error. Keystrokes invalid. Too many nuns!')
                continue
            elif (self.exclude_outliers == False) or (time < OUTLIER_CUTOFF):
                times.append(time)
            else:
                # This means time < OUTLIER_CUTOFF right?
                outlier_count += 1
        if outlier_count > 0:
            print(f"Removed {outlier_count} outliers.")
        return times
    
    def wpm(self, identifier=None) -> float or None:
        """
        Function to return the average words per minute.
        WPM is CPM/5, where CPM is characters per minute.
        """
        num_chars = 0
        avg_delay = 0
        total_seconds = 0
        total_seconds_extra = 0

        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return None
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    # Get the number of characters in the string
                    string = log['string']
                    num_chars = len(string)
                    # Get the average time between keystrokes
                    avg_delay = self.get_average_delay(identifier)
                    total_seconds_extra = sum(self.get_only_times(identifier))
                    break
        else:
            num_chars = 0
            for log in self.logs:
                num_chars += len(log['string'])
            # Get the average time between keystrokes
            avg_delay = self.get_average_delay()
            total_seconds_extra = sum(self.get_only_times()) #ONLY FOR no-ide
        # This one calculates the total seconds by multiplying the number of characters by the average delay
        if num_chars == 0:
            print("No characters found.")
            return 0
        total_seconds = num_chars * avg_delay
        if total_seconds == 0:
            print("No time found!!!")
            return 0
        # This one calculates the total seconds by summing the times between keystrokes, so it includes non-chars
        ## THESE ARE DIFFERENT BECAUSE THE TOTAL TIME IS CALCULATED DIFFERENTLY
        # Total seconds: 70.8942, Total seconds (extra): 76.78259
        # The extra time is due to the delays between keystrokes that are not characters in the final string
        # print(f"Total seconds: {total_seconds}")
        # print(f"Total seconds (extra): {total_seconds_extra}")
        # Calculate the CPM
        cpm = (num_chars / total_seconds) * 60
        return round(cpm / 5, 1)
    
    def get_highest_keystroke_times(self, identifier=None) -> list:
        """
        Function to return the highest times it took for keystrokes.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return []
            for log in self.logs:
                if log['id'] == identifier or log['string'] == identifier:
                    # times = [keystroke[1] for keystroke in log['keystrokes']]
                    times = self.get_only_times(identifier)
                    return [max(times) if times else 0]
            print("I should never get here, right?")
            return []
        highest_times = []
        for log in self.logs:
            times = [keystroke[1] for keystroke in log['keystrokes']]
            highest_times.append(max(times) if times else 0)
        return highest_times
    
    def get_average_delay(self, identifier=None) -> float or None:
        """
        Function to return the average time between keystrokes for a given log.
        """
        times = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return None
            times = self.get_only_times(identifier)
        else:
            times = self.get_only_times()
        if len(times) == 0:
            print ("No keystrokes found.")
            return 0
        return round(sum(times) / len(times), 4)

    def get_std_deviation(self, identifier=None) -> float or None:
        """
        Function to return the standard deviation of the time between keystrokes for a given log.
        """
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return None
            times = self.get_only_times(identifier)
        else:
            times = self.get_only_times()
        if len(times) < 2:
            print ("Not enough keystrokes to calculate standard deviation.")
            return 0
        return round(statistics.stdev(times), 4)
    
    def visualize_keystroke_times(self, keystrokes=None) -> None:
        """
        Plots the average keystroke time for each character based on the keystrokes in the logs.
        """
        if keystrokes is None:
            keystrokes = self.get_all_keystrokes()
        if not keystrokes:
            print("No keystrokes found.")
            return
        character_times = self.calculate_average_keystroke_times(keystrokes)

        characters = list(character_times.keys())
        times = list(character_times.values())

        plt.bar(characters, times)
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time')
        line_2 = "\nExcluding Outliers" if self.exclude_outliers else ""
        plt.title('Average Keystroke Time for Each Character' + line_2)
        plt.show()

    def get_all_keystrokes(self, identifier=None) -> list:
        """
        Returns a list of all keystrokes in the logs.

        Returns:
            list: A list of keystrokes, where each keystroke is represented by a list containing a character and a time.
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

    def calculate_average_keystroke_times(self, keystrokes=None) -> dict:
        """
        Calculates the average keystroke time for each character based on the provided keystrokes.

        Args:
            keystrokes (list): A list of keystrokes, where each keystroke is represented by a list containing a character and a time.

        Returns:
            dict: A dictionary mapping each character to its average keystroke time.
        """
        character_times = {}
        character_counts = {}
        if keystrokes is None:
            keystrokes = self.get_all_keystrokes()

        none_count = 0
        for key, time in keystrokes:
            if time == None:
                none_count += 1
                if none_count > 1:
                    print('Critical Error. Keystrokes invalid. Too many nuns!')
                continue
            if self.exclude_outliers and time > OUTLIER_CUTOFF:
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
    print(parser.check_membership("1 2 3 4 5"))
