# This file is for validating keys across various types.

# Standard library imports
from json import JSONDecoder, JSONEncoder
from typing import List, Iterator, Tuple, TypedDict, Any

# Third party imports
from pynput.keyboard import Key

# KeyMaster imports
from utils.config import APOSTROPHE, SPECIAL_KEYS, BANNED_KEYS, STOP_KEY, STOP_CODE, EMPTY_WRAPPED_CHAR, KEYBOARD_CHARS
from utils.helpers import unwrap_key, is_key_valid

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
            raise TypeError('key must be a string and is_special must be a bool')
        if is_special:
            if key != STOP_CODE and key not in SPECIAL_KEYS:
                raise ValueError('key must be a special key. These are defined in utils/config.py')
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
        self.key = key
        self.time = time
        self.valid = is_key_valid(key)
        self.unicode_char = None
        if self.valid:
            self.unicode_char = unwrap_key(self.key)
        self.unicode_only = self.unicode_char and unwrap_key(self.key) not in KEYBOARD_CHARS

        self.legal_key: LegalKey | None = None
        if self.valid and not self.unicode_only:
           self.legal_key = self.legalize()

    def __iter__(self) -> Iterator[Tuple[str, float | None]]:
        yield self.key, self.time
    def __repr__(self) -> str:
        return f"Keystroke(key={self.key}, time={self.time})"
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Keystroke):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return False
    
    def legalize(self) -> LegalKey | None:
        """
        Returns a LegalKey object or None if the key is not valid.
        """
        if not self.valid:
            print(f"Invalid char not legalized:{self.key}<-")
            return None
        
        if self.unicode_only:
            print(f"Unicode char {self.key} restricted and not legalized.")
            return None
        
        is_special = False
        legal_key = ''
        if self.key == STOP_CODE:
            is_special = True
            legal_key = STOP_KEY
        elif self.key in SPECIAL_KEYS:
            # What should a legal key look like for a special key?
            print("Special key!")
            is_special = True
            legal_key = APOSTROPHE + self.key + APOSTROPHE
        else:
            key = unwrap_key(self.key)
            if key in BANNED_KEYS:
                print(f"Banned key!->{self.key}")
                return None
            if len(key) != 1 or key not in KEYBOARD_CHARS:
                print(f"Invalid key!->{self.key}")
                return None
            legal_key = key
        return LegalKey(legal_key, is_special)
        
class Log(TypedDict):
    """
    A class used to represent a log. The logfile is a list of logs.
    """
    id: str
    string: str
    keystrokes: List[Keystroke]
    # These look like [ {
    # "id": "6c03f172-abe8-4087-af47-bc84498b0f48", 
    # "string": "*", 
    # "keystrokes": [["Key.shift", null], ["'*'", 0.167]]
    # } ]

class KeystrokeDecoder(JSONDecoder):
    """
    A JSONDecoder that decodes Keystrokes [Logfile->List of Keystrokes]
    """
    def object_hook(self, dct: dict[str, Any]) -> dict[str, Any]:
        if 'keystrokes' in dct:
            dct['keystrokes'] = [Keystroke(*k) for k in dct['keystrokes']]
        return dct

class KeystrokeEncoder(JSONEncoder):
    """
    A JSONEncoder that encodes Keystrokes [Keystrokes->(key, time) and Log->Logfile)]
    """
    def default(self, obj):
        if isinstance(obj, Keystroke):
            return [obj.key, obj.time]
        elif isinstance(obj, dict) and 'id' in obj and 'string' in obj and 'keystrokes' in obj:
            return {
                'id': obj['id'], 
                'string': obj['string'], 
                'keystrokes': [self.default(keystroke) for keystroke in obj['keystrokes']]
            }
        return super().default(obj)

class KeystrokeList:
    def __init__(self, keystrokes: List[Keystroke]):
        if not isinstance(keystrokes, list):
            raise TypeError('keystrokes must be a list')
        self.keystrokes = keystrokes
        self.length = len(keystrokes)
    def __getitem__(self, index: int) -> Keystroke:
        return self.keystrokes[index]
    def __len__(self) -> int:
        return self.length
    def __repr__(self) -> str:
        return "Keys:" + "".join('\n' + keystroke.key for keystroke in self.keystrokes)
    def __eq__(self, other) -> bool:
        if isinstance(other, KeystrokeList):
            return self.keystrokes == other.keystrokes
        return False

def keystrokes_to_string(keystrokes: List[Keystroke]) -> str:
    """
    Converts a list of Keystroke objects into a string, taking into account special keys.

    Args:
        keystrokes (List[Keystroke]): A list of Keystroke objects.

    Returns:
        str: The string representation of the keystrokes.
    """
    output_string = ""
    word_count = 0
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
                    output_string = output_string[:-1]  # Remove the last character
            elif special_key == Key.space:
                output_string += ' '
                word_count += 1
            elif special_key == Key.enter:
                output_string += '\n'
            elif special_key == Key.tab:
                output_string += '\t'
            else:
                continue # Ignore keys like CapsLock and Shift
        else:
            key = unwrap_key(key)
            if key in BANNED_KEYS:
                continue
            # Append the character to the output string
            # It is 1 character because it passed is_key_valid() and is not in SPECIAL_KEYS
            output_string += key
    return output_string

def validate_keystrokes(keystrokes: List[Keystroke], input_string: str) -> bool:
    """
    Validate a list of Keystroke objects against a string.

    Args:
        keystrokes (List[Keystroke]): A list of Keystroke objects.
        input_string (str): The string to validate against.

    Returns:
        bool: True if the decomposed keystrokes match the input string.
    """
    # Validate the keystrokes with the parser
    validation_string = keystrokes_to_string(keystrokes)
    if input_string == validation_string:
        return True
    if len(input_string) != len(validation_string):
        print(f"Warning: validate_keystrokes: Lengths not equal.")
    # Find the first character that differs
    max_length = max(len(input_string), len(validation_string))
    for i in range(max_length):
        # safety check
        if i >= len(input_string):
            print(f"Validation string found extra char at index {i}: {(validation_string[i])} <-")
            break

        elif i >= len(validation_string):
            print(f"Input string found extra char at index {i}: {(input_string[i])} <-")
            break
        typed_char = input_string[i]
        validation_char = validation_string[i]
        if typed_char != validation_char:
            print(f"String does not align with keystroke list!")
            print(f"Input string: {typed_char} <-")
            print(f"Validation string: {validation_char} <-")
            break
    return False
