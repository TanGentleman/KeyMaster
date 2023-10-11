import json
import statistics
import matplotlib.pyplot as plt
OUTLIER_CUTOFF = 0.6
class KeystrokeParser:
    def __init__(self, filename='keystrokes.json'):
        self.filename = filename
        self.logs = self.load_logs()

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
            if keyword in log['string']:
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

    def get_highest_keystroke_times(self) -> list:
        """
        Function to return the highest times it took for keystrokes.
        """
        highest_times = []
        for log in self.logs:
            times = [keystroke[1] for keystroke in log['keystrokes']]
            highest_times.append(max(times) if times else 0)
        return highest_times
    
    def get_average_time(self, identifier=None) -> float or None:
        """
        Function to return the average time between keystrokes for a given log.
        """
        times = []
        keystrokes = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return None
            keystrokes = self.get_all_keystrokes(identifier)
            times = [keystroke[1] for keystroke in keystrokes if keystroke[1] < OUTLIER_CUTOFF]
        else:
            keystrokes = self.get_all_keystrokes()
            times = [keystroke[1] for keystroke in keystrokes if keystroke[1] < OUTLIER_CUTOFF]
        if len(times) == 0:
            print ("No keystrokes found.")
            return 0
        return round(sum(times) / len(times), 4)

    def get_std_deviation(self, identifier=None) -> float or None:
        """
        Function to return the standard deviation of the time between keystrokes for a given log.
        """
        times = []
        if identifier is not None:
            isPresent = self.check_membership(identifier)
            if isPresent == False:
                return None
            keystrokes = self.get_all_keystrokes(identifier)
            times = [keystroke[1] for keystroke in keystrokes if keystroke[1] < OUTLIER_CUTOFF]
        else:
            keystrokes = self.get_all_keystrokes()
            times = [keystroke[1] for keystroke in keystrokes if keystroke[1] < OUTLIER_CUTOFF]
        if len(times) < 2:
            print ("Not enough keystrokes to calculate standard deviation.")
            return 0
        return round(statistics.stdev(times), 4)
    
    def visualize_keystroke_times(self, keystrokes=None, excludeOutliers=True) -> None:
        """
        Plots the average keystroke time for each character based on the keystrokes in the logs.
        """
        if keystrokes is None:
            keystrokes = self.get_all_keystrokes()
        if not keystrokes:
            print("No keystrokes found.")
            return

        character_times = self.calculate_average_keystroke_times(keystrokes, excludeOutliers)

        characters = list(character_times.keys())
        times = list(character_times.values())

        plt.bar(characters, times)
        plt.xlabel('Characters')
        plt.ylabel('Average Keystroke Time')
        plt.title('Average Keystroke Time for Each Character')
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

    def calculate_average_keystroke_times(self, keystrokes=None, excludeOutliers=True) -> dict:
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
        for key, time in keystrokes:
            if excludeOutliers and time > OUTLIER_CUTOFF:
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
