# This file is for validating keys across various types.

# Standard library imports
from json import JSONDecoder, JSONEncoder
import json
from typing import Iterator, TypedDict, Any

# Third party imports
from pynput.keyboard import Key

# KeyMaster imports
from utils.config import APOSTROPHE, MAX_KEY_LENGTH, SPECIAL_KEYS, BANNED_KEYS, STOP_KEY, STOP_CODE, EMPTY_WRAPPED_CHAR, KEYBOARD_CHARS
from utils.helpers import is_valid_wrapped_char, is_valid_wrapped_special_key, unwrap_key, is_key_valid


class UnicodeKey:
    """
    A class used to represent a unicode key. Chars have no quote wrapping.
    >>> UnicodeKey('a', False)
    key=a
    >>> UnicodeKey("'√'", 0.2222)
    """
    pass


class SpecialKey:
    pass


class LegalKey:
    """
    A class used to represent a legal key. Chars have no quote wrapping.
    STOP_CODE
    >>> LegalKey('a', False)
    key=a
    >>> LegalKey('Key.shift', True)
    key=Key.shift
    """

    def __init__(self, key: str, is_special: bool):
        if not isinstance(key, str) or not isinstance(is_special, bool):
            raise TypeError(
                'key must be a string and is_special must be a bool')
        if is_special:
            if not is_valid_wrapped_special_key(key):
                raise ValueError(
                    'key must be a special key. These are defined in utils/config.py')
        else:
            if len(key) != 1 or key not in KEYBOARD_CHARS:
                raise ValueError('key must be typeable character')
        self.key = key
        self.is_special = is_special

    def __repr__(self) -> str:
        return f"key={self.key}"

    def __eq__(self, other) -> bool:
        if isinstance(other, LegalKey):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return False


class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    Convention is to wrap the key in single quotes if it is a character.
    """

    def __init__(self, key: str, time: float | None):
        """
        >>> Keystroke("'a'", None)
        Keystroke(key='a', time=None)
        >>> Keystroke('Key.shift', 0.2222)
        Keystroke(key=Key.shift, time=0.222)
        """
        if not isinstance(key, str):
            raise TypeError('encoded key must be a string')
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        if len(key) == 0 or key == EMPTY_WRAPPED_CHAR:
            raise ValueError('encoded key must not be empty')
        if len(key) > MAX_KEY_LENGTH:
            raise ValueError(
                f'encoded key must be less than {MAX_KEY_LENGTH} characters')
        self.key = key
        self.time = time
        self.valid = is_key_valid(key)

        self.unicode_char = None
        if is_valid_wrapped_char(self.key):
            self.unicode_char = unwrap_key(self.key)
        self.is_unwrapped = len(self.key) == 1
        if self.is_unwrapped and self.valid:
            self.unicode_char = self.key

        self.unicode_only = False
        if self.unicode_char is not None:
            if self.unicode_char not in KEYBOARD_CHARS:
                self.unicode_only = True

        self.legal_key: LegalKey | None = None
        if self.valid and not self.unicode_only:
            self.legal_key = self.legalize()

    def __iter__(self) -> Iterator[tuple[str, float | None]]:
        yield self.key, self.time

    def __repr__(self) -> str:
        return f"Keystroke(key={self.key}, time={self.time})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Keystroke):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return False

    def legalize(self) -> LegalKey:
        """
        Returns a LegalKey object or None if the key is not valid.
        """
        if not self.valid:
            raise ValueError('Invalid char not legalized')

        if self.unicode_only:
            raise ValueError('Unicode char not legalized')

        is_special = False
        legal_key = ''
        if self.key == STOP_CODE or self.key in SPECIAL_KEYS:
            is_special = True
            legal_key = APOSTROPHE + self.key + APOSTROPHE
        else:
            key = unwrap_key(self.key)
            if len(key) != 1 or key not in KEYBOARD_CHARS:
                print(f"Invalid key!->{self.key}")
                raise ValueError(
                    'Legal keys are 1 character and must be typeable')
            legal_key = key
        return LegalKey(legal_key, is_special)


class KeystrokeList:
    def __init__(self, keystrokes: list[Keystroke] | None = None):
        if keystrokes is None:
            keystrokes = []
        if not isinstance(keystrokes, list):
            raise TypeError('keystrokes must be a list')
        if not all(isinstance(keystroke, Keystroke)
                   for keystroke in keystrokes):
            raise TypeError('keystrokes must be a list of Keystroke objects')

        self.length = len(keystrokes)
        self.keystrokes = keystrokes

    def append(self, keystroke: Keystroke) -> None:
        if not isinstance(keystroke, Keystroke):
            raise TypeError('keystroke must be a Keystroke object')
        self.keystrokes.append(keystroke)
        self.length += 1

    def extend(self, keystrokes) -> None:
        if not isinstance(keystrokes, KeystrokeList):
            raise TypeError('Must use KeystrokeList.extend with a KeystrokeList')
        self.keystrokes.extend(keystrokes.keystrokes)
        self.length = len(self.keystrokes)

    def is_empty(self) -> bool:
        return self.length == 0

    def __iter__(self) -> Iterator[Keystroke]:
        return iter(self.keystrokes)

    def __getitem__(self, index: int) -> Keystroke:
        return self.keystrokes[index]

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return "As string: " + self.to_string()

    def __eq__(self, other) -> bool:
        if isinstance(other, KeystrokeList):
            return self.keystrokes == other.keystrokes
        return False

    def to_string(self) -> str:
        """
        Returns the string representation of the keystrokes.
        """
        if self.is_empty():
            return ""
        output_string = ""
        word_count = 0
        keystrokes = self.keystrokes
        for keystroke in keystrokes:
            if not keystroke.valid:
                print(f"Invalid keystroke: {keystroke.key}")
                continue
            # This means keystroke.valid is true, so it is a valid keypress
            key = keystroke.key
            # Handle special keys
            if key == STOP_CODE:
                key = STOP_KEY
                output_string += key
            elif key in SPECIAL_KEYS:
                special_key = SPECIAL_KEYS[key]
                if special_key == Key.backspace:
                    if output_string != '':
                        # Remove the last character
                        output_string = output_string[:-1]
                elif special_key == Key.space:
                    output_string += ' '
                    word_count += 1
                elif special_key == Key.enter:
                    output_string += '\n'
                elif special_key == Key.tab:
                    output_string += '\t'
                else:
                    continue  # Ignore keys like CapsLock and Shift
            else:
                key = unwrap_key(key)
                if key in BANNED_KEYS:
                    continue
                # Append the character to the output string
                # It is 1 character because it passed is_key_valid() and is not
                # in SPECIAL_KEYS
                output_string += key
        return output_string

    def validate(self, input_string: str) -> bool:
        """
        Validate a list of Keystroke objects against a string.

        Args:
            keystrokes (KeystrokeList): A list of Keystroke objects.
            input_string (str): The string to validate against.

        Returns:
            bool: True if the decomposed keystrokes match the input string.
        """
        # Validate the keystrokes with the parser
        validation_string = self.to_string()
        if input_string == validation_string:
            return True
        if len(input_string) != len(validation_string):
            print(f"Warning: validate_keystrokes: Lengths not equal.")
        # Find the first character that differs
        max_length = max(len(input_string), len(validation_string))
        for i in range(max_length):
            # safety check
            if i >= len(input_string):
                print(
                    f"Validation string found extra char at index {i}:{(validation_string[i])}<-")
                break

            elif i >= len(validation_string):
                print(
                    f"Input string found extra char at index {i}: {(input_string[i])} <-")
                break
            typed_char = input_string[i]
            validation_char = validation_string[i]
            if typed_char != validation_char:
                print(f"String does not align with keystroke list!")
                print(f"Input:{typed_char}<-")
                print(f"Validation string:{validation_char}<-")
                break
        return False


class KeystrokeDecoder(JSONDecoder):
    """
    A JSONDecoder that decodes a list of dictionaries and replaces the "keystrokes" field
    with KeystrokeList objects.
    """

    def object_hook(self, dct: dict) -> dict:
        """
        Convert each keystroke into a Keystroke object and instantiate a KeystrokeList.
        """
        if 'keystrokes' in dct:
            keystrokes = dct['keystrokes']
            dct['keystrokes'] = KeystrokeList([Keystroke(*k) for k in keystrokes])
        return dct


class KeystrokeEncoder(JSONEncoder):
    """
    A JSONEncoder that encodes Keystrokes [Keystrokes->(key, time) and Log->Logfile)]
    """

    def default(self, obj):
        if isinstance(obj, Keystroke):
            return [obj.key, obj.time]
        elif isinstance(obj, KeystrokeList):
            return [[keystroke.key, keystroke.time] for keystroke in obj]
        elif isinstance(obj, dict) and 'id' in obj and 'string' in obj and 'keystrokes' in obj:
            # Directly encode the KeystrokeList within the dictionary
            return {'id': obj['id'], 'string': obj['string'], 'keystrokes': [
                [keystroke.key, keystroke.time] for keystroke in obj['keystrokes']]}
        return super().default(obj)


class Log(TypedDict):
    """
    A class used to represent a log. The logfile is a list of logs.
    """
    id: str
    string: str
    keystrokes: KeystrokeList
    # These look like [ {
    # "id": "6c03f172-abe8-4087-af47-bc84498b0f48",
    # "string": "*",
    # "keystrokes": [["Key.shift", null], ["'*'", 0.167]]
    # } ]


def is_id_in_log(identifier: str, log: Log) -> bool:
    """Client facing.
    Check if a log with the identifier exists in the loaded logs.

    Args:
        `identifier` (`str`): The UUID or exact string formatted as STOP_KEY + string
        `log` (`Log`): The log to check.

    Returns:
        `bool`: True if a log with the given UUID or exact string exists, False otherwise.
    """
    if not identifier:
        print("No identifier provided.")
        return False
    if not log:
        print("No log provided.")
        return False
    if log['id'] == identifier:
        return True
    if identifier[-1] == STOP_KEY:
        if log['string'] == identifier[1:]:
            return True
        else:
            print('Exact string not found.')
    return False
