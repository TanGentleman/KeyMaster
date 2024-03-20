# This file is for validating keys across various types.

# Standard library imports
from json import JSONDecoder, JSONEncoder
from typing import Iterator, TypedDict, Any, Union

# Third party imports
from pynput.keyboard import Key

# KeyMaster imports
from utils.config import MAX_KEY_LENGTH, SPECIAL_KEYS, STOP_KEY, STOP_CODE, ROUND_DIGITS
from utils.constants import EMPTY_WRAPPED_CHAR, APOSTROPHE, KEYBOARD_CHARS
from utils.helpers import is_valid_wrapped_char, is_valid_wrapped_special_key, unwrap_char, is_key_valid


class LegalKey:
    """
    A class used to represent a legal key (a char or a special key on keyboard).
    Chars have no quote wrapping. Special keys are wrapped in single quotes.
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
        return f"|{self.key}|"

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
        self.unicode_char: str | None = None
        self.is_typeable_char = False
        self.legal_key: LegalKey | None = None

        if self.valid:
            is_unwrapped = len(self.key) == 1

            if is_valid_wrapped_char(self.key):
                self.unicode_char = unwrap_char(self.key)

            elif is_unwrapped and self.valid:
                self.unicode_char = self.key

            if self.unicode_char is not None and self.unicode_char in KEYBOARD_CHARS:
                self.is_typeable_char = True

            if self.is_typeable_char or self.key == STOP_CODE or self.key in SPECIAL_KEYS:
                self.legal_key = self.legalize()

    def props(self):
        """
        Returns the properties of the keystroke.
        """
        return (f"key: {self.key}"
              + f"\ntime: {self.time}"
              + f"\nvalid: {self.valid}"
              + f"\nunicode_char: {self.unicode_char}"
              + f"\nis_typeable_char: {self.is_typeable_char}"
              + f"\nlegal_key: {self.legal_key}"
              )

    def __iter__(self) -> Iterator[tuple[str, float | None]]:
        yield self.key, self.time

    def __repr__(self) -> str:
        return f"Keystroke(key={self.key}, time={self.time})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Keystroke):
            return self.key == other.key and self.time == other.time
        elif isinstance(other, str):
            return self.key == other
        return False

    def legalize(self) -> LegalKey:
        """
        Returns a LegalKey object or raises a ValueError.
        """
        if self.valid is False:
            raise ValueError('Invalid char not legalized')
        is_special = False
        legal_key = ''
        if self.unicode_char is None:
            if self.key in SPECIAL_KEYS:
                is_special = True
                legal_key = APOSTROPHE + self.key[4:] + APOSTROPHE
            elif self.key == STOP_CODE: 
                is_special = True
                legal_key = APOSTROPHE + self.key + APOSTROPHE
            else:
                raise ValueError('Non-char not legalized')
        else:
            if self.is_typeable_char is False:
                raise ValueError('Unicode char not legalized')
            else:
                char = self.unicode_char
                legal_key = char
        return LegalKey(legal_key, is_special)


class KeystrokeList:
    def __init__(self, keystrokes: list[Keystroke] | None = None):
        if keystrokes is None:
            keystrokes = []
        if not isinstance(keystrokes, list):
            raise TypeError('keystrokes must be a list')
        # if not all(isinstance(keystroke, Keystroke)
        #            for keystroke in keystrokes):
        #     raise TypeError('keystrokes must be a list of Keystroke objects')
        self.keystrokes = keystrokes
        self.length = len(keystrokes)
        self.set_null_time()

    def set_null_time(self) -> None:
        """
        Set the time of the first keystroke to None.
        """
        if self.is_empty():
            return
        self.keystrokes[0].time = None

    def append(self, keystroke: Keystroke) -> None:
        if not isinstance(keystroke, Keystroke):
            raise TypeError('keystroke must be a Keystroke object')
        if self.is_empty():
            keystroke.time = None
        self.keystrokes.append(keystroke)
        self.length += 1

    def extend(self, keystrokes, prune = False) -> None:
        """
        Extend the list of keystrokes with another list of keystrokes.

        Args:
            keystrokes (KeystrokeList): A list of Keystroke objects.
            prune (bool): If True, prune null times in the list. The default prune is non-destructive.
        """
        if not isinstance(keystrokes, KeystrokeList):
            raise TypeError(
                'Must use KeystrokeList.extend with a KeystrokeList')

        self.keystrokes.extend(keystrokes.keystrokes)
        self.length = len(self.keystrokes)
        # Ensure first Keystone.time set to None
        self.set_null_time()
        # prune other null values
        if prune:
            self.prune_bad_nuns()

    def is_empty(self) -> bool:
        return self.length == 0

    def __iter__(self) -> Iterator[Keystroke]:
        return iter(self.keystrokes)

    def __getitem__(self, index: int) -> Keystroke:
        return self.keystrokes[index]

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return f"(KeystrokeList={self.to_string()})"

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
            char = keystroke.unicode_char
            if char is not None:
                output_string += char
            else:
                # This means it is a special key
                key = keystroke.key
                # Handle special keys
                if key == STOP_CODE:
                    decoded_stop_key = STOP_KEY
                    output_string += decoded_stop_key
                elif key in SPECIAL_KEYS:
                    decoded_key = SPECIAL_KEYS[key]
                    if decoded_key == Key.backspace:
                        if output_string != '':
                            # Remove the last character
                            output_string = output_string[:-1]
                    elif decoded_key == Key.space:
                        output_string += ' '
                        word_count += 1
                    elif decoded_key == Key.enter:
                        output_string += '\n'
                    elif decoded_key == Key.tab:
                        output_string += '\t'
                    else:
                        continue  # Ignore keys like Shift
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

    def prune_bad_nuns(self, destructive = False) -> int:
        assert ROUND_DIGITS > 0
        """
        Remove all extraneous null (None) times from the list of keystrokes.
        
        Args:
            destructive (bool): If False, null times are replaced with 0.001 second delays.

        Returns:
            int: The number of null times removed.
        """
        pruned_keystrokes = []
        none_count = 0
        for keystroke in self.keystrokes:
            if keystroke.time is None:
                none_count += 1
                if none_count > 1:
                    if destructive:
                        print("Removing keystroke with None time")
                        continue
                    else:
                        print("Replacing keystroke with shortest delay")
                        shortest_delay = float(1 / (10 ** (ROUND_DIGITS-1)))
                        keystroke.time = shortest_delay
            pruned_keystrokes.append(keystroke)
        self.keystrokes = pruned_keystrokes
        return none_count

    def prune_shifts(self) -> None:
        """
        Remove all extraneous shift keys from the list of keystrokes.
        """
        pruned_keystrokes = []
        for keystroke in self.keystrokes:
            if keystroke.legal_key == "'shift'":
                continue
            pruned_keystrokes.append(keystroke)
        self.keystrokes = pruned_keystrokes

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


class KeystrokeDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: dict) -> Union[dict, Any]:
        # Check if the object is a log entry
        if 'id' in obj and 'string' in obj and 'keystrokes' in obj:
            # Validate the log entry
            if not isinstance(obj['id'], str):
                raise ValueError("Invalid ID type; expected a string.")
            if not isinstance(obj['keystrokes'], list):
                raise ValueError("Invalid keystrokes type; expected a list.")
            # Decode the keystrokes
            obj['keystrokes'] = KeystrokeList(
                [self.decode_keystroke(ks) for ks in obj['keystrokes']])
        return obj

    def decode_keystroke(self, obj: list) -> Keystroke:
        if isinstance(
            obj,
            list) and len(obj) == 2 and isinstance(
            obj[0],
            str) and (
            obj[1] is None or isinstance(
                obj[1],
                float)):
            return Keystroke(obj[0], obj[1])
        raise ValueError("Invalid Keystroke format.")


class KeystrokeEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Keystroke):
            return [obj.key, obj.time]
        elif isinstance(obj, KeystrokeList):
            return [[keystroke.key, keystroke.time]
                    for keystroke in obj.keystrokes]
        # Check for Log
        elif isinstance(obj, dict) and 'id' in obj and 'string' in obj and 'keystrokes' in obj:
            # Directly encode the KeystrokeList within the dictionary
            return {
                'id': obj['id'],
                'string': obj['string'],
                # Reuse the KeystrokeList encoding
                'keystrokes': self.default(obj['keystrokes'])
            }
        # Check for list[Log]
        elif isinstance(obj, list):
            return [self.default(log) for log in obj]
        raise TypeError(
            f"Object of type {type(obj)} is not JSON serializable.")
