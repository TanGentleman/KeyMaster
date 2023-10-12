from pynput.keyboard import Key, Listener, Controller
import time
import json
import uuid
from config import ABSOLUTE_FILENAME

MAX_WORDS = 50
SPEEDHACK = True
SPEEDMULTIPLIER = 2
BANNED_KEYS = ["'√'"]
SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    # 'Key.tab': Key.tab,
    # 'Key.enter': Key.enter,
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
    def __init__(self, filename=ABSOLUTE_FILENAME):
        self.filename = filename
        self.reset()

    def reset(self):
        self.keystrokes = []
        self.typed_string = ""
        self.prev_time = time.time()
        self.word_count = 0

    def on_press(self, keypress):
        """
        Function to handle key press events.
        """
        def is_key_valid(keypress):
            """
            Function to check if the key is valid.
            """
            key_as_string = str(keypress)
            if key_as_string in BANNED_KEYS:
                return False
            elif key_as_string in SPECIAL_KEYS:
                return True
            elif hasattr(keypress, 'char'):
                return True
            return False
        current_time = time.time()
        time_diff = current_time - self.prev_time
        if time_diff > 3:
            time_diff = 3 + (time_diff / 1000)
        time_diff = round(time_diff, 4)  # Round to 4 decimal places

        if is_key_valid(keypress):
            key_as_string = str(keypress)

            # Handle apostrophe key
            if key_as_string == "\"'\"":
                key_as_string = "'\''"
            self.keystrokes.append((key_as_string, time_diff))
            self.prev_time = current_time

            # Append typed character to the string
            if hasattr(keypress, 'char'):
                self.typed_string += keypress.char
            elif keypress == Key.space:
                self.typed_string += ' '
                self.word_count += 1
            # logic for backspaces, including if going back on a space
            elif keypress == Key.backspace:
                self.typed_string = self.typed_string[:-1]
                if len(self.typed_string) > 0 and self.typed_string[-1]  == ' ':
                    self.word_count -= 1
            ## Enter/Tab not valid logged keys, this may technically affect correctness of word count if used in lieu of space
            # elif keypress == Key.enter:
            #     self.typed_string += '\n'
            #     self.word_count += 1
            # elif keypress == Key.tab:
            #     self.typed_string += '\t'
            #     self.word_count += 1

            # Stop listener when max words have been typed
            if self.word_count == MAX_WORDS:
                return False

    def on_release(self, key):
        """
        Function to handle key release events.
        """
        if key == Key.esc:
            print('')
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

    def is_log_legit(self, keystrokes, input_string) -> bool:
        # Make sure keystrokes is validly typed
        # Make sure input_string is validly typed
        for key, time_diff in keystrokes:
            if type(key) != str or type(time_diff) != float:
                return False
        if type(input_string) != str:
            return False
        return True

    def set_internal_log(self, keystrokes, input_string):
        """
        Function to set the internal log.
        """
        ### MUST CHECK VALIDITY OF THESE!
        if self.is_log_legit(keystrokes, input_string) == False:
            print("Invalid log. Internal log not set")
            return False
        self.keystrokes = keystrokes
        self.typed_string = input_string
        self.word_count = input_string.count(' ')
        ## OR should it be self.word_count = input_string.count(' ')
        ## I can make a case 

    def save_log(self, reset=False) -> bool:
        """
        Function to save the log to a file.
        """
        if self.typed_string == "":
            print("No keystrokes to save.")
            if reset:
                self.reset()
            return False
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
            with open(self.filename, 'r+') as f:
                logs = json.load(f)
                logs.append(log)
                f.seek(0)
                json.dump(logs, f)
                print("Logfile updated.")
        except FileNotFoundError:
            with open(self.filename, 'w') as f:
                json.dump([log], f)
        if reset:
            self.reset()
        return True
    
    def simulate_keystrokes(self, keystrokes=None):
        """
        Function to simulate the keystrokes with the same timing.
        """
        if keystrokes is None:
            keystrokes = self.keystrokes

        keyboard = Controller()
        try:
            with Listener(on_release=self.on_release) as listener:
                print(f"Listener started. The simulation will start when you press ESC.")
                listener.join()
        except Exception as e:
            print(f"An error occurred: {e}")
        for key, time_diff in keystrokes:
            # If time difference is greater than 3 seconds, set diff to 3.x seconds with decimal coming from time_diff
            if SPEEDHACK:
                time_diff = time_diff / SPEEDMULTIPLIER
            if time_diff > 3:
                time_diff = 3 + (time_diff / 1000)
            try:
                time.sleep(time_diff)  # Wait for the time difference between keystrokes
                if key in SPECIAL_KEYS:
                    keyboard.press(SPECIAL_KEYS[key])
                    keyboard.release(SPECIAL_KEYS[key])
                elif key == "'\''":
                    keyboard.type("'")  # Type the apostrophe
                else:
                    keyboard.type(key.strip('\''))  # Type the character
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def simulate_from_id(self, identifier):
        """
        Function to load a log given a UUID or a string.
        """
        try:
            with open(self.filename, 'r') as f:
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
    success = logger.save_log()
    if success:
        print("\nLog saved. Now simulating keystrokes...\n")
        logger.simulate_keystrokes()
