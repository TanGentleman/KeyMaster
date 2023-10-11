from pynput.keyboard import Key, Listener, Controller
import time
import json
import uuid

MAX_WORDS = 158
speedHack = True
speedMultiplier = 4

special_keys = {
    'Key.space': Key.space,
    'Key.enter': Key.enter,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    'Key.tab': Key.tab,
    # 'Key.esc': Key.esc,
    # Add other keys as needed
}

### JSON FORMAT FROM keystrokes.json
# [
#   {
#     "id": "string",
#     "string": "string",
#     "keystrokes": [
#       ["string", number]
#     ]
#   }
# ]



class KeystrokeLogger:
    def __init__(self):
        self.keystrokes = []
        self.typed_string = ""
        self.prev_time = time.time()
        self.word_count = 0

    def on_press(self, keypress):
        """
        Function to handle key press events.
        """
        current_time = time.time()
        time_diff = current_time - self.prev_time
        time_diff = round(time_diff, 4)  # Round to 4 decimal places
        key_str = str(keypress)

        # Handle apostrophe key
        if key_str == "\"'\"":
            key_str = "'\''"
        if (key_str in special_keys) or (hasattr(keypress, 'char')):
            self.keystrokes.append((key_str, time_diff))
            self.prev_time = current_time

            # Append typed character to the string
            if hasattr(keypress, 'char'):
                self.typed_string += keypress.char
                if (keypress.char.isprintable() == False):
                    print('Found a non-printable character that counts as a char!')
            elif keypress == Key.space:
                self.typed_string += ' '
                self.word_count += 1
            elif keypress == Key.enter:
                self.typed_string += '\n'
            # logic for backspaces, including if going back on a space
            elif keypress == Key.backspace:
                self.typed_string = self.typed_string[:-1]
                if self.typed_string[-1] == ' ':
                    self.word_count -= 1

            # Stop listener when max words have been typed
            if self.word_count == MAX_WORDS:
                return False

    def on_release(self, key):
        """
        Function to handle key release events.
        """
        if key == Key.esc:
            return False

    def start_listener(self):
        """
        Function to start the key listener.
        """
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                print(f"Listener started. Type your text. The listener will stop after {MAX_WORDS} words have been typed or when you press ESC.")
                listener.join()
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_log(self):
        """
        Function to save the log to a file.
        """
        if self.typed_string == "":
            print("No keystrokes to save.")
            return
        # Create a unique ID
        unique_id = str(uuid.uuid4())

        # Create the log object
        log = {
            'id': unique_id,
            'string': self.typed_string,
            'keystrokes': self.keystrokes
        }

        # Append the log object to the file
        try:
            with open('keystrokes.json', 'r+') as f:
                logs = json.load(f)
                logs.append(log)
                f.seek(0)
                json.dump(logs, f)
                print("Logfile updated.")
        except FileNotFoundError:
            with open('keystrokes.json', 'w') as f:
                json.dump([log], f)

    def simulate_keystrokes(self, keystrokes=None):
        """
        Function to simulate the keystrokes with the same timing.
        """
        if keystrokes is None:
            keystrokes = self.keystrokes

        keyboard = Controller()

        for key, time_diff in keystrokes:
            # If time difference is greater than 3 seconds, set diff to 3.x seconds with decimal coming from time_diff
            if speedHack:
                time_diff = time_diff / speedMultiplier
            if time_diff > 3:
                time_diff = 3 + (time_diff / 1000)
            try:
                time.sleep(time_diff)  # Wait for the time difference between keystrokes
                if key in special_keys:
                    keyboard.press(special_keys[key])
                    keyboard.release(special_keys[key])
                elif key == "'\''":
                    keyboard.type("'")  # Type the apostrophe
                else:
                    keyboard.type(key.strip('\''))  # Type the character
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def simulate_from_log(self, identifier):
        """
        Function to load a log given a UUID or a string.
        """
        try:
            with open('keystrokes.json', 'r') as f:
                logs = json.load(f)
                for log in logs:
                    if log['id'] == identifier or log['string'] == identifier:
                        self.simulate_keystrokes(log['keystrokes'])
                        return
                print(f"No log found with the identifier: {identifier}")
        except FileNotFoundError:
            print("No log file found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    logger = KeystrokeLogger()
    logger.start_listener()
    logger.save_log()
    # print("\nLog saved. Now simulating keystrokes...\n")
    # logger.simulate_keystrokes()
