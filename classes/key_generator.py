# Standard library imports
from time import sleep
from threading import Timer
from random import normalvariate
import logging

from utils.constants import SHIFT_KEY
logging.basicConfig(encoding='utf-8', level=logging.INFO)
# Third party imports
from pynput.keyboard import Controller

# KeyMaster imports
from utils.config import (
    SIM_SPEED_MULTIPLE, DEFAULT_DISABLE_SIMULATION, DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, SIM_MAX_DURATION, SIM_MAX_WORDS, ROUND_DIGITS, BANNED_KEYS,
    SIM_MAX_SPEED, SIM_DELAY_MEAN, SIM_DELAY_STD_DEV, MIN_DELAY, GENERATE_SHIFTS, PRINT_SHIFT_INSERTIONS, SHIFT_SPEED,
    STOP_KEY, STOP_CODE, SPECIAL_KEYS)
from utils.constants import SHIFTED_CHARS, APOSTROPHE, KEYBOARD_CHARS
from utils.validation import Keystroke, Key, KeystrokeList

class KeyGenerator:
    """
    A class used to simulate keystrokes and log them.

    Attributes:
        speed_multiplier (float or int): The speed multiplier.
        delay_mean (float): The mean delay between keystrokes.
        delay_standard_deviation (float): The standard deviation of the delay between keystrokes.
        max_words (int): The maximum number of words to simulate.
        min_delay (float): The minimum delay between keystrokes.
        special_keys (dict): A dictionary of special keys and their corresponding keys.
        whitespace_dict (dict): A dictionary of encoded characters and their corresponding strings.
        disable (bool): Whether or not the simulation is disabled.
        max_duration (float): The maximum duration of the simulation.
    """

    def __init__(
            self,
            speed_multiplier: int | float = SIM_SPEED_MULTIPLE,
            disable: bool = DEFAULT_DISABLE_SIMULATION,
            allow_newlines: bool = DEFAULT_ALLOW_NEWLINES,
            allow_unicode: bool = DEFAULT_ALLOW_UNICODE,
            max_duration: int | float = SIM_MAX_DURATION,
            max_words: int = SIM_MAX_WORDS,
            round_digits: int = ROUND_DIGITS,
            banned_keys: list[str] = BANNED_KEYS) -> None:
        """
        Initialize the KeyGenerator with the given parameters.
        """
        self.speed_multiplier = float(speed_multiplier)
        self.disable = disable
        self.allow_newlines = allow_newlines
        self.allow_unicode = allow_unicode
        self.max_duration = float(max_duration)
        self.max_words = max_words
        self.round_digits = round_digits
        self.banned_keys = banned_keys
        self.whitespace_dict = {
            ' ': str(Key.space),
            '\t': str(Key.tab),
            '\n': str(Key.enter)
        }
        if self.allow_newlines is False:
            self.whitespace_dict.pop('\n')
        self.stop = False

    def set_speed(self, speed: int | float) -> None:
        """Client facing.
        Set the speed multiplier.

        Args:
            speed (float): The speed multiplier.
        """
        if speed < 0:
            raise ValueError("Speed multiplier must be greater than 0.")
        max_speed = SIM_MAX_SPEED
        if speed > max_speed:
            logging.error(
                f"Invalid speed multiplier: {speed}. Setting to {max_speed}")
            speed = max_speed
        self.speed_multiplier = float(speed)

    def calculate_delay(self, speed_multiple: int |
                        float | None = None) -> float:
        """Not client facing.
        Get a normally distributed delay between keystrokes.

        Args:
            speed_multiple: The speed multiplier.

        Returns:
            float: The delay between keystrokes.
        """
        # Ensure speed_by_multiple > 0
        if speed_multiple is None:
            speed_multiple = self.speed_multiplier

        if speed_multiple <= 0:
            # ERROR
            logging.error(
                f"Invalid speed multiplier: {speed_multiple}. Setting to 1")
            speed_multiple = 1
        delay = normalvariate(
            SIM_DELAY_MEAN / (speed_multiple),
            SIM_DELAY_STD_DEV / speed_multiple)
        if delay < MIN_DELAY:
            delay = MIN_DELAY + delay / 10
        return delay

    def keystrokes_from_string(
            self, input_string: str) -> KeystrokeList:
        """Client facing.
        Generate valid Keystrokes from a string. Output object can be simulated.

        Returns:
            KeystrokeList: A list of keystrokes.
        """
        # The rest of the code from the simulate_keystrokes function goes here.
        keystrokes = KeystrokeList()
        if not input_string:
            logging.error("No input string provided.")
            return keystrokes
        word_count = 0

        string_length = len(input_string)
        for i in range(string_length):
            if word_count == self.max_words:
                logging.info(f"Reached max words: {self.max_words}")
                break
            char = input_string[i]
            keystroke = self.generate_keystroke(char)
            if keystroke is None:
                continue
            
            if char == ' ':
                word_count += 1
            last_key = None
            if GENERATE_SHIFTS:
                if not keystrokes.is_empty():
                    last_key = keystrokes[-1].key
                if (last_key is None 
                    or last_key in self.whitespace_dict 
                    or (last_key not in SHIFTED_CHARS and not last_key.isupper())):
                    # Check if a shift key needs to be added
                    if char.isupper() or (char in SHIFTED_CHARS):
                        if PRINT_SHIFT_INSERTIONS:
                            logging.info(f"Inserting shift before key {i}: {char}")
                        # Add a shift keypress
                        if keystrokes.is_empty():
                            time = None
                        else:
                            time = SHIFT_SPEED
                        key = SHIFT_KEY
                        keystrokes.append(Keystroke(key, time))
            if keystrokes.is_empty():
                keystroke.time = None
            keystrokes.append(keystroke)
            # Should I stop generation at stop key too?
            if char == STOP_KEY:
                logging.warning(
                    'STOP key found. Halting keystroke generation.')
                break
        return keystrokes

    def wrap_character(self, char: str) -> str:
        """Not client facing.
        Wrap a character in single quotes.
        """
        return APOSTROPHE + char + APOSTROPHE

    def generate_keystroke(self, char: str) -> Keystroke | None:
        """Client facing.
        Generate a `Keystroke` from a character (`str`).
        """
        if len(char) != 1:
            logging.error(
                f"generate_keystroke: Character length is not 1: {char}")
            return None
        key_string = char
        if char in self.whitespace_dict:
            key_string = (self.whitespace_dict[char])
        elif char.isprintable():
            # Add '' around the character
            if char == STOP_KEY:
                key_string = STOP_CODE
            else:
                if self.allow_unicode is False and char not in KEYBOARD_CHARS:
                    return None
                key_string = APOSTROPHE + char + APOSTROPHE
        else:
            logging.error(
                f"generate_keystroke: Non-printable character: {char} -> {ord(char)}")
            return None

        delay = round(self.calculate_delay(), self.round_digits)
        return Keystroke(key_string, delay)

    def simulate_keystrokes(self, keystrokes: KeystrokeList) -> None:
        """Client facing.
        Function to simulate the given keystrokes.

        Args:
            keystrokes (KeystrokeList, optional): The list of keystrokes to simulate.
        """
        if self.disable:
            logging.error("Simulation disabled.")
            return
        if keystrokes.is_empty():
            logging.error("No keystrokes found.")
            return

        none_count = 0
        self.stop = False
        # Initialize the keyboard controller
        keyboard = Controller()
        def stop_simulation() -> None:
            self.stop = True
        simulation_timer = Timer(self.max_duration, stop_simulation)
        simulation_timer.start()
        try:
            for keystroke in keystrokes:
                if self.stop:
                    logging.info(
                        f'Duration {self.max_duration}s elapsed. Stopping simulation.')
                    break
                if keystroke.valid is False:
                    logging.error(
                        f"simulate_keystrokes: Invalid key: {keystroke.key}")
                    continue

                key = keystroke.key
                if key == STOP_CODE:
                    key = STOP_KEY
                time = keystroke.time
                if time is None:
                    none_count += 1
                    if none_count > 1:
                        logging.error(
                            'Critical error: None value marks first character. Only use once')
                        break
                    # What should this time diff be?
                    delay = 0.0
                else:
                    delay = time
                    # If time difference is greater than 3 seconds, set diff to 3.x
                    # seconds with decimal coming from delay
                    if self.speed_multiplier > 0:
                        delay = delay / self.speed_multiplier
                    if delay > 3:
                        delay = 3 + (delay / 1000)
                if delay > 0:
                    # Wait for the time difference between keystrokes
                    sleep(delay)
                if key in SPECIAL_KEYS:
                    # Ignore shift and caps lock
                    if key == SHIFT_KEY or key == 'Key.caps_lock':
                        continue
                    try:
                        keyboard.tap(SPECIAL_KEYS[key])
                    except Exception as e:    
                        logging.error(
                            f"ERROR! special key not pressed: {key}")
                        continue
                    
                else:
                    # Decode the character
                    char = keystroke.unicode_char
                    if char is None:
                        if key != STOP_KEY:
                            logging.error(f"Unicode value is None, key: {key}")
                            logging.info(f"Pre-emptively stopping simulation.")
                            break
                        char = STOP_KEY
                    # Don't simulate banned keys
                    if char in self.banned_keys:
                        continue
                    try:
                        keyboard.tap(char)
                    except Exception as e:
                        logging.error(
                            f"ERROR! Decoded key was not a character: {char}")
                        continue

                if key == STOP_KEY:
                    logging.warning('STOP key found. Stopping simulation.')
                    break
        except KeyboardInterrupt:
            logging.info("Simulation interrupted.")
        finally:
            if simulation_timer.is_alive():
                simulation_timer.cancel()

    def simulate_string(self, string: str) -> KeystrokeList | None:
        """Client facing.
        Simulate the given string.

        Args:
            string (str): The string to simulate.
        """
        keystrokes = self.keystrokes_from_string(string)
        if keystrokes.is_empty():
            logging.error("Given input was not simulated.")
            return None
        self.simulate_keystrokes(keystrokes)
        return keystrokes
