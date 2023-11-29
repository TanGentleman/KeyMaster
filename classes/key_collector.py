# Standard library imports
from json import dump as json_dump
from json import load as json_load
from time import time, perf_counter
from uuid import uuid4
from typing import List
from threading import Timer

# Third party imports
from pynput.keyboard import Key, KeyCode, Listener
# KeyMaster imports
from utils.config import APOSTROPHE, SPECIAL_KEYS, STOP_KEY, STOP_CODE, ROUND_DIGITS
from utils.config import MAX_WORDS, DEFAULT_LISTENER_DURATION, MAX_LOGGABLE_DELAY
from utils.config import COLLECT_ONLY_TYPEABLE
from utils.helpers import get_filepath, is_key_valid
from utils.validation import Keystroke, KeystrokeList, Log, KeystrokeDecoder, KeystrokeEncoder


class KeyLogger:
    """
    A class used to log keystrokes and calculate delays between each keypress.
    This class is responsible for capturing and storing keystrokes values and timings.
    It also keeps track of the total number of words typed and the entire string of characters typed.
    """

    def __init__(
            self,
            filename: str | None = "REG",
            only_typeable: bool = COLLECT_ONLY_TYPEABLE,
            round_digits: int = ROUND_DIGITS,
            listen_duration: int | float = DEFAULT_LISTENER_DURATION) -> None:
        """
        Initialize the KeyLogger. If filename is None, the logger will not save to a file.
        Defaults to keystrokes.json in the logs directory.

        Args:
                `filename` (`str` or `None`): The filename to save the log to. Use 'REG' or 'SIM' for main logfiles.
        """
        self.filename = filename
        self.keystrokes = KeystrokeList([])
        self.word_count = 0
        self.typed_string = ""
        self.prev_time = time()
        self.timer: Timer | None = None

        self.only_typeable = only_typeable
        self.round_digits = round_digits
        self.duration = listen_duration

    def reset(self) -> None:
        """Client facing.
        Clear the current state of the logger.
        """
        self.keystrokes = KeystrokeList([])
        self.word_count = 0
        self.typed_string = ""
        self.prev_time = time()

    def set_filename(self, filename: str) -> None:
        """Client facing.
        Set the filename to save logs to.

        Args:
                `filename` (`str`): The filename to save the log to.
        """
        self.filename = filename

    def encode_keycode_char(self, key: str) -> str:
        """Not client facing.
        Encodes a character by wrapping it in single quotes.
        The STOP_KEY is encoded as STOP_CODE. For example, '*' may now be 'STOP'.
        """
        if len(key) != 1:
            raise ValueError("encode_keycode_char: Key length != 1")

        # Mark stop key or wrap the key in single quotes
        if key == STOP_KEY:
            encoded_key = STOP_CODE
        else:
            encoded_key = APOSTROPHE + key + APOSTROPHE
        return encoded_key

    def encode_special_char(self, key: Key) -> str:
        """Not client facing.
        Encodes a special key as a string.
        """
        encoded_key = None
        for key_string, value in SPECIAL_KEYS.items():
            if value == key:
                encoded_key = key_string

        if encoded_key is None:
            raise ValueError(
                "encode_special_char: Key not found in SPECIAL_KEYS")
        return encoded_key

    def log_valid_keypress(self, keypress: Key | KeyCode) -> None:
        """Not client facing.
        Logs a valid keypress to the internal keystrokes list.
        Valid keypresses are alphanumeric characters, space, tab, enter, and backspace.

        Args:
                `keypress` (`Key` or `KeyCode`): The key press event to log.
        """
        if not is_key_valid(keypress):
            print('CRITICAL: Only keys that pass is_key_valid .')
            raise ValueError(
                "log_valid_keypress: Invalid keypress. This should not happen.")

        encoded_key = ""
        # Calculate delay between keystrokes
        current_time = perf_counter()
        delay = current_time - self.prev_time
        self.prev_time = current_time
        if delay > MAX_LOGGABLE_DELAY:
            delay = MAX_LOGGABLE_DELAY + (delay / 1000)
        delay = round(delay, self.round_digits)

        if isinstance(keypress, KeyCode):
            # This is a non-special character
            if keypress.char is None:
                return
            key = keypress.char
            if self.only_typeable and not key.isprintable():
                return
            self.typed_string += key
            encoded_key = self.encode_keycode_char(key)
        else:
            # This is a KeyCode object
            if keypress in SPECIAL_KEYS.values():
                encoded_key = self.encode_special_char(keypress)
                if keypress == Key.space:
                    self.typed_string += ' '
                    self.word_count += 1
                elif keypress == Key.enter:
                    self.typed_string += '\n'
                elif keypress == Key.tab:
                    self.typed_string += '\t'
                # logic for backspaces, including if going back on a space
                elif keypress == Key.backspace and len(self.typed_string) > 0:
                    if self.typed_string[-1] == ' ':
                        self.word_count -= 1
                    self.typed_string = self.typed_string[:-1]
            else:
                return
        if not encoded_key:
            raise ValueError(
                "log_valid_keypress: Unable to encode keypress. This should not happen.")
        # Create a Keystroke object and append it to the list
        # If the list is empty, the first keystroke will have delay = None
        if len(self.keystrokes) == 0:
            keystroke = Keystroke(encoded_key, None)
        else:
            keystroke = Keystroke(encoded_key, delay)
        self.keystrokes.append(keystroke)
        return

    # on_press still needs to be tidied up a bit
    def on_press(self, keypress: Key | KeyCode | None) -> None:
        """Not client facing.
        Handles the event when a key is pressed.
        """
        if keypress is None:
            return None
        # Validate keypress
        if not is_key_valid(keypress):
            return None
        # do a cool function
        self.log_valid_keypress(keypress)
        return

    def stop_listener_condition(self, keypress: Key | KeyCode) -> bool:
        """Not client facing.
        Checks if the keypress triggers a stop condition.
        """
        if keypress == Key.esc:
            return True
        if self.word_count >= MAX_WORDS:
            return True
        if isinstance(keypress, KeyCode) and keypress.char is not None:
            return keypress.char == STOP_KEY
        return False

    def on_release(self, keypress: Key | KeyCode | None) -> None:
        """Not client facing.
        Handles key release events. Stop the listener when stop condition is met.
        """
        if keypress is None:
            return None
        if self.stop_listener_condition(keypress):
            print('')
            if self.timer is None:
                raise ValueError(
                    "Timer is None. Start it before listener.join")
            self.timer.cancel()
            raise KeyboardInterrupt
        return

    def start_listener(self, duration: int | float | None = None) -> None:
        """Client facing.
        Function to start the key listener.
        The listener will only stop when stop_listener_condition returns True.
        """
        if duration is None:
            duration = self.duration
        listener = None
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                print(
                    f"Listening for {duration} seconds. The listener will stop on ESC, STOP_KEY, or after {MAX_WORDS} words.")
                # Start a timer of 10 seconds
                self.timer = Timer(duration, listener.stop)
                self.timer.start()
                listener.join()
        except KeyboardInterrupt:
            print("Listener stopped.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the listener is stopped
            if listener is not None:
                listener.stop()
                print("Listener stopped!")
            # Ensure the timer is stopped
            if self.timer is not None:
                self.timer.cancel()
        return

    def is_loggable(
            self,
            keystrokes: KeystrokeList | None = None,
            input_string: str | None = None) -> bool:
        """Not client facing (This function might need revisiting)
        Checks the validity of a list of keystrokes and a string. If valid, it can be logged in a Log object.
        By default, this function checks the internal keystrokes and input_string attributes.

        Args:
                `keystrokes` (`KeystrokeList`): The list of keystrokes to validate.
                `input_string` (`str`): The input string to validate.

        Returns:
                `bool`: True if the decomposed keystrokes match the input string. False otherwise.
        """
        if keystrokes is None:
            keystrokes = self.keystrokes
        if input_string is None:
            input_string = self.typed_string

        if not input_string:
            print("No input string found. Log not legit")
            return False
        if not keystrokes:
            print("No keystrokes found. Log not legit")
            return False
        none_count = 0
        for keystroke in keystrokes:
            delay = keystroke.time
            if delay is None:
                none_count += 1
                if none_count > 1:
                    print('None value marks first character ONLY! Log not legit.')
                    return False
        success = keystrokes.validate(input_string)
        print(f"{len(keystrokes)} Keystrokes validated: {success}")
        # I want to solve banned key problem (spam prints), but for now, just return success
        # Eventually, one should be able to store banned keys in simulated string,
        # so string should be adjusted before using as an argument here
        return success

    def set_internal_log(
            self,
            keystrokes: KeystrokeList,
            input_string: str) -> bool:
        """Client facing.
        Replace the internal log with the provided keystrokes and input string.

        Args:
                `keystrokes` (`KeystrokeList`): The list of keystrokes to replace self.keystrokes with.
                `input_string` (`str`): The input string to replace self.typed_string with.

        Returns:
                bool: True if state successfully replaced. False if arguments invalid.
        """
        if not self.is_loggable(keystrokes, input_string):
            print("Invalid log. Internal log not set")
            return False
        self.keystrokes = keystrokes
        self.typed_string = input_string
        self.word_count = input_string.count(' ')
        return True

    def save_log(self, reset: bool = False) -> bool:
        """Client facing.
        Function to save the log to a file.

        Args:
                `reset` (`bool`): Whether to reset the logger after saving the log. Defaults to False.

        Returns:
                `bool`: True if the log was saved successfully, False otherwise.
        """
        filepath = get_filepath(self.filename)
        if filepath is None:
            print("Filename null. Log not saved.")
            return False
        if not self.typed_string:
            print("No keystrokes to save.")
            if reset:
                self.reset()
            return False
        # ensure log is legit
        legit = self.is_loggable()
        if not legit:
            print("Log is not legit. Did not update file.")
            return False

        # Create a unique ID
        unique_id = str(uuid4())

        # Create the log object of class Log
        log: Log = {
            'id': unique_id,
            'string': self.typed_string,
            'keystrokes': self.keystrokes
        }
        # Create var logs to store the logs
        # Replace keystrokes in json using KeystrokeEncoder
        # Append the log object to the file
        logs: List[Log] = []
        try:
            with open(filepath, 'r+') as f:
                logs = json_load(f, cls=KeystrokeDecoder)
                logs.append(log)
                f.seek(0)
                json_dump(logs, f, cls=KeystrokeEncoder)
                print("Logfile updated.")
        except FileNotFoundError:
            with open(filepath, 'w') as f:
                json_dump([log], f, cls=KeystrokeEncoder)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        if reset:
            self.reset()
        return True


if __name__ == "__main__":
    logger = KeyLogger()
    logger.start_listener()
    logger.save_log()
