from pynput.keyboard import Key, KeyCode, Listener, Controller
from time import time, sleep
import json
import uuid
from os import path
from config import ROOT, ABSOLUTE_REG_FILEPATH, Keystroke, Keypress, Log
from typing import List, Optional, Union


MAX_WORDS = 50
SPEEDHACK = True
SPEEDMULTIPLIER = 2
BANNED_KEYS = ["'√'"]
DELIMITER_KEY = "*" # This key is used to stop the listener when pressed
SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    # 'Key.tab': Key.tab,
    # 'Key.enter': Key.enter,
    # 'Key.esc': Key.esc,
}

class KeystrokeLogger:
    """
    A class used to log keystrokes and calculate delays between each keypress.
    """

    def __init__(self, filename: Optional[str] = None) -> None:
        """
        Initialize the KeystrokeLogger with a filename.
        Set attributes using the reset function.
        """
        if filename is None:
            filename = ABSOLUTE_REG_FILEPATH
        else:
            # Make absolute path if not already
            if not path.isabs(filename):
                filename = path.join(ROOT, filename)

        self.filename: str = filename
        self.reset()

    def reset(self) -> None:
        """
        Reset the keystrokes, typed string, previous time, word count, and first character typed flag.
        """
        # Keystroke related attributes
        self.keystrokes: List[Keystroke] = []
        self.typed_string: str = ""
        self.word_count: int = 0

        # Time related attribute
        self.prev_time: float = time() # The time at keypress is compared to this value.

    def is_key_valid(self, key: Union[str, Keypress]) -> bool:
        """
        Function to check if the key is valid.
        """
        if isinstance(key, KeyCode):
            return True
        elif isinstance(key, Key):
            key_as_string = str(key)
        elif isinstance(key, str):
            key_as_string = key
        else:
            # You can't get here! I think...
            assert(False)
        if key_as_string in BANNED_KEYS:
            return False
        elif key_as_string in SPECIAL_KEYS:
            return True
        
        # Im curious about the apostrophe and any other potential wacky characters
        is_legit = len(key_as_string) == 1 and key_as_string.isprintable()
        if not is_legit:
            print(f"Invalid key: {key_as_string}")
        return is_legit
    
    def on_press(self, keypress: Keypress) -> Optional[bool]:
        """
        Function to handle key press events.
        """
        current_time = time()
        time_diff = current_time - self.prev_time
        if time_diff > 3:
            time_diff = 3 + (time_diff / 1000)
        time_diff = round(time_diff, 4)  # Round to 4 decimal places
        key_as_string = str(keypress)
        if key_as_string == "\"'\"":
            print(f"found comma! It is {'valid' if self.is_key_valid(key_as_string) else 'invalid'} originally")
            key_as_string = "'\''"
            print(f"found comma! It is {'valid' if self.is_key_valid(key_as_string) else 'invalid'} after")
        if self.is_key_valid(keypress):
            # Handle apostrophe key
            # if key_as_string == "\"'\"":
            #     key_as_string = "'\''"

            # Mark first character's time_diff as None
            if self.keystrokes == []:
                self.keystrokes.append(Keystroke(key_as_string, None))
            else:
                self.keystrokes.append(Keystroke(key_as_string, time_diff))
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
        # Stop listener when DELIMITER_KEY typed
        if isinstance(keypress, KeyCode):
            if keypress.char == DELIMITER_KEY:
                return False
        return None

    def on_release(self, keypress: Keypress) -> Optional[bool]:
        """
        Function to handle key release events.
        """
        if keypress == Key.esc:
            print('')
            return False
        return None

    def start_listener(self) -> None:
        """
        Function to start the key listener.
        """
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener: # type: ignore
                print(f"Listener started. Type your text. The listener will stop after {MAX_WORDS} words have been typed or when you press ESC.")
                listener.join()
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_log_legit(self, keystrokes: List[Keystroke], input_string: str) -> bool:
        """
        Function to check if the log is valid.
        """
        # Make sure keystrokes is validly typed
        # Make sure input_string is validly typed

        if input_string == "":
            print("No keystrokes found. Log not legit")
            return False
        none_count = 0
        for keystroke in keystrokes:
            key = keystroke.key
            time_diff = keystroke.time
            if time_diff is None:
                none_count += 1
                if none_count > 1:
                    print('None value marks first character. Only use once.')
                    return False
            elif type(key) != str or type(time_diff) != float:
                print('Invalid keystrokes. Format is (key:str, time:float)')
                return False
        return True

    def set_internal_log(self, keystrokes: List[Keystroke], input_string: str) -> bool:
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
        return True
        ## OR should it be self.word_count = input_string.count(' ')
        ## I can make a case 

    def save_log(self, reset: bool = False) -> bool:
        """
        Function to save the log to a file.
        """
        if self.typed_string == "":
            print("No keystrokes to save.")
            if reset:
                self.reset()
            return False
        # ensure log is legit
        if self.is_log_legit(self.keystrokes, self.typed_string) == False:
            print("Log is not legit. Did not update file.")
            return False
        
        # Create a unique ID
        unique_id = str(uuid.uuid4())

        # Create the log object of class Log
        log: Log = {
            'id': unique_id,
            'string': self.typed_string,
            'keystrokes': self.keystrokes
        }
        # Append the log object to the file
        try:
            with open(self.filename, 'r+') as f:
                logs: List[Log] = json.load(f)
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
    
    def simulate_keystrokes(self, keystrokes: Optional[List[Keystroke]] = None) -> None:
        """
        Function to simulate the keystrokes with the same timing.
        """
        if keystrokes is None:
            keystrokes = self.keystrokes
        # Validate keystrokes
        # Maybe keystrokes have to be legit to even be passed here?
        if keystrokes == []:
            print("No keystrokes found.")
            return

        keyboard = Controller()
        try:
            with Listener(on_release=self.on_release) as listener: # type: ignore
                print(f"Listener started. The simulation will start when you press ESC.")
                listener.join()
        except Exception as e:
            print(f"An error occurred: {e}")
        none_count = 0
        for keystroke in keystrokes:
            key = keystroke.key
            time = keystroke.time

            if self.is_key_valid(key) == False:
                print(f"Invalid key: {key}")
                continue
            if time is None:
                none_count += 1
                if none_count > 1:
                    print('Critical error: None value marks first character. Only use once')
                    break
                # What should this time diff be?
                time_diff = 0.0
            else:
                time_diff = time
                # If time difference is greater than 3 seconds, set diff to 3.x seconds with decimal coming from time_diff
                if SPEEDHACK:
                    # Avoid any potential divide by 0 errors
                    if SPEEDMULTIPLIER == 0:
                        print("Speed multiplier cannot be 0. Setting to 1")
                        SPEEDMULTIPLIER = 1
                    time_diff = time_diff / SPEEDMULTIPLIER
                if time_diff > 3:
                    time_diff = 3 + (time_diff / 1000)
            try:
                if time_diff > 0:
                    sleep(time_diff)  # Wait for the time difference between keystrokes
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

    def simulate_from_id(self, identifier: str) -> None:
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
