# KeyMaster imports
from pynput.keyboard import Key, KeyCode, Listener
from utils.settings import (
    SPECIAL_KEYS,
    STOP_KEY,
    STOP_CODE,
    ROUND_DIGITS,
    LISTENER_WORD_LIMIT,
    DEFAULT_LISTENER_DURATION,
    MAX_LOGGABLE_DELAY,
    COLLECT_ONLY_TYPEABLE)
from utils.validation import Keystroke, KeystrokeList, Log, KeystrokeDecoder, KeystrokeEncoder
from utils.helpers import get_filepath, is_key_valid, resolve_filename, get_log_id, update_log_id
from utils.constants import APOSTROPHE, KEYBOARD_CHARS

# Standard library imports
from json import dump as json_dump
from json import load as json_load
from time import time, perf_counter
from uuid import uuid4
from threading import Timer
import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

# Third party imports
LOG_SHIFT_PRESSES = False


class KeyLogger:
    """
    A class used manage the listener and to accurately log keystroke data.

    Attributes:
    ----------
    - filename (`str`): The filename of the log file.
    - only_typeable (`bool`): Whether to only log typeable characters.
    - round_digits (`int`): The number of digits to round to.
    - duration (`int | float`): The duration to listen for.
    """

    def __init__(
            self,
            filename: str | None = "REG",
            only_typeable: bool = COLLECT_ONLY_TYPEABLE,
            round_digits: int = ROUND_DIGITS,
            duration: int | float = DEFAULT_LISTENER_DURATION,
            banned_keys: list[str] | None = None
    ) -> None:
        """
        Initialize the KeyLogger. If filename is None, the logger will not save to a file.
        Defaults to keystrokes.json in the logs directory.

        Args:
                `filename` (`str` or `None`): The filename to save the log to. Use 'REG' or 'SIM' for main logfiles.
        """
        self.filename = filename
        self.keystrokes = KeystrokeList()
        self.word_count = 0
        self.typed_string = ""
        self.prev_time = time()
        self.timer: Timer | None = None

        self.only_typeable = only_typeable
        self.round_digits = round_digits
        self.duration = duration

        self.banned_keys = banned_keys

        self.is_reset = True

    def reset(self) -> None:
        """Client facing.
        Clear the current state of the logger.
        """
        self.keystrokes = KeystrokeList()
        self.word_count = 0
        self.typed_string = ""
        self.prev_time = time()
        self.is_reset = True

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
            raise ValueError(f"encode_keycode_char: Key length != 1: {key}")

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
        assert is_key_valid(keypress), "log_valid_keypress: Invalid keypress"
        if LOG_SHIFT_PRESSES is False and keypress == Key.shift:
            return
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
            char = keypress.char
            if char is None or len(char) != 1:
                raise ValueError(
                    f"log_valid_keypress: Key length != 1: {char}")
            if self.only_typeable and char not in KEYBOARD_CHARS:
                return
            self.typed_string += char
            encoded_key = self.encode_keycode_char(char)
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
        # Create a Keystroke object and append it to the list
        # If the list is empty, the first keystroke will have delay = None
        if len(self.keystrokes) == 0:
            keystroke = Keystroke(encoded_key, None)
        else:
            keystroke = Keystroke(encoded_key, delay)
        self.keystrokes.append(keystroke)
        return

    # on_press still needs to be tidied up a bit
    def handle_keypress(self, keypress: Key | KeyCode) -> None:
        """Not client facing.
        Handles the event when a key is pressed.
        """
        # Exclude banned keys
        if isinstance(keypress, KeyCode):
            if keypress.char is None:
                return
            if self.banned_keys is not None and keypress.char in self.banned_keys:
                # logging.debug(f"Key {keypress.char} is banned. Ignoring.")
                return
        # Validate keypress
        if is_key_valid(keypress):
            self.log_valid_keypress(keypress)
        return

    def stop_listener_condition(self, keypress: Key | KeyCode) -> bool:
        """Not client facing.
        Checks if the keypress triggers a stop condition.
        """
        if keypress == Key.esc:
            return True
        if self.word_count >= LISTENER_WORD_LIMIT:
            return True
        if isinstance(keypress, KeyCode):
            return keypress.char == STOP_KEY
        return False

    def on_press(self, keypress: Key | KeyCode | None) -> None:
        """Not client facing.
        Handles key press events.
        """
        if keypress == Key.esc:
            raise KeyboardInterrupt
        return

    def on_release(self, keypress: Key | KeyCode | None) -> None:
        """Not client facing.
        Handles key release events. Stop the listener when stop condition is met.
        """
        if keypress is None:
            return None
        self.handle_keypress(keypress)
        if self.stop_listener_condition(keypress):
            print('')
            if self.timer:
                self.timer.cancel()
            raise KeyboardInterrupt
        return

    def start_listener(self, duration: int | float |
                       None = None) -> KeystrokeList:
        """Client facing.
        Function to start the key listener.
        Listener will stop on conditions in stop_listener_condition or when duration reached.
        """
        self.reset()  # reset the logger
        if duration is None:
            duration = self.duration
        listener = None
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                logging.info(
                    f"Listening for {duration} seconds. The listener will stop on ESC, STOP_KEY, or after {LISTENER_WORD_LIMIT} words.\n")
                # Start a timer of 10 seconds
                self.timer = Timer(duration, listener.stop)
                self.timer.start()
                listener.join()
        except KeyboardInterrupt:
            logging.info("Listener stopped.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            # Ensure the listener is stopped
            if listener is not None:
                listener.stop()
                logging.info("Listener stopped!")
            # Ensure the timer is stopped
            if self.timer is not None:
                self.timer.cancel()
        return self.keystrokes

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

        if keystrokes.is_empty():
            logging.error("No keystrokes found. Log not legit")
            return False
        none_count = 0
        for keystroke in keystrokes:
            delay = keystroke.time
            if delay is None:
                none_count += 1
                if none_count > 1:
                    logging.error(
                        'None value marks first character ONLY! Log not legit.')
                    return False
        success = keystrokes.validate(input_string)
        logging.info(f"{len(keystrokes)} Keystrokes validated: {success}")
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
        if self.is_loggable(keystrokes, input_string) is False:
            logging.error("Invalid log. Internal log not set")
            return False
        self.keystrokes = keystrokes
        self.typed_string = input_string
        self.word_count = input_string.count(' ')
        return True

    def create_log(self, log_id: str | None = None) -> Log | None:
        """Not client facing.
        Returns a Log object using the internal keystrokes and input string.
        """
        # ensure log is legit
        assert log_id is None or len(log_id) == 4
        legit = self.is_loggable()
        if legit is False:
            logging.error("Log not created.")
            return None

        # Create a unique ID
        unique_id = ''
        if log_id is None:
            unique_id = str(uuid4())
        else:
            unique_id = log_id

        # Create the log object of class Log
        log: Log = {
            'id': unique_id,
            'string': self.typed_string,
            'keystrokes': self.keystrokes
        }
        return log

    def save_log(self, reset: bool = False) -> bool:
        """Client facing.
        Function to save the log to a file.

        Args:
                `reset` (`bool`): Whether to reset the logger after saving the log. Defaults to False.

        Returns:
                `bool`: True if the log was saved successfully, False otherwise.
        """
        if self.is_reset is False:
            logging.error(
                "You have already saved a log. Please reset the logger before saving again.")
            return False
        filepath = get_filepath(self.filename)
        if filepath is None:
            logging.error("Filename null. Log not saved.")
            return False
        if self.keystrokes.is_empty():
            logging.error("No keystrokes to save.")
            if reset:
                self.reset()
            return False
        log_id = get_log_id()
        log = self.create_log(log_id)
        if not log:
            logging.error("Log had trouble saving!")
            return False
        # Create var logs to store the logs
        # Replace keystrokes in json using KeystrokeEncoder
        # Append the log object to the file
        try:
            with open(filepath, 'r+') as f:
                # I can use the KeystrokeDecoder here, but it seems unnecessary
                logs: list[Log] = json_load(f)
                logs.append(log)
                f.seek(0)
                json_dump(logs, f, cls=KeystrokeEncoder)
                logging.info("Logfile updated.")
        except FileNotFoundError:
            with open(filepath, 'w') as f:
                json_dump([log], f, cls=KeystrokeEncoder)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
        update_log_id(log_id)
        self.is_reset = False
        if reset:
            self.reset()
        return True

    def __repr__(self) -> str:
        pretty_string = (
            f"# Configuration:\nfile={resolve_filename(self.filename)}\nBanned Keys: {self.banned_keys}" +
            (f"\nTypeable-only mode enabled." if self.only_typeable else "")
        )
        return pretty_string


if __name__ == "__main__":
    logger = KeyLogger()
    logger.start_listener()
    logger.save_log()
