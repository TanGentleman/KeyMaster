# This file is for the key validation function to explicitly typecheck classes.
from typing import List, Union, Optional, Iterator, Tuple, TypedDict, Any
from pynput.keyboard import Key, KeyCode
from config import SPECIAL_KEYS, BANNED_KEYS, WEIRD_KEYS
from json import JSONDecoder, JSONEncoder
import string

VALID_KEYBOARD_CHARS = string.ascii_letters + string.digits + string.punctuation + ' \n\t'

def replace_weird_keys(input_string: str) -> str:
    """
    Replace weird keys with their string representations.
    I have found some present occasionally when copying text in the Notes app on macOS.
    Potentially quotes with different unicode representations could go here too.
    """
    replacements = {
        '\u2028': '\n',  # replace line separator with newline
        # '\u2029': '\n',  # replace paragraph separator with newline
        # add more replacements here if needed
    }
    for old, new in replacements.items():
        input_string = input_string.replace(old, new)
    return input_string

def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    Returns a string with only typable characters.
    """
    return ''.join(c for c in input_string if c in VALID_KEYBOARD_CHARS)

def clean_string(input_string: str) -> str:
    """
    Returns a string with only typable characters.
    """
    for c in input_string:
        if c not in VALID_KEYBOARD_CHARS:
            print(f"Invalid character: {c} -> {ord(c)}")
    return filter_non_typable_chars(replace_weird_keys(input_string))

# *** KEY VALIDATION ***
def is_key_valid(key: Union[Key, KeyCode, str], strict = False) -> bool:
    """
    Function to check if the key is valid.
    """
    if isinstance(key, Key):
        return key in SPECIAL_KEYS.values()
    elif isinstance(key, KeyCode):
        if key.char is None:
            return False
        key = str(key)
    # We know isinstance(key, str)
    key_as_string = key
    # A string like 'a' is valid, but 'Key.alt' is not
    if key_as_string in BANNED_KEYS:
        return False
    elif key_as_string in SPECIAL_KEYS:
        return True
    if key_as_string in WEIRD_KEYS:
        return True
    # Check the length of the key stripped of single quotes
    key_as_string = key_as_string.strip("'")
    # This means that both wrapped and unwrapped chars are valid
    if strict:
        return len(key_as_string) == 1 and key_as_string in VALID_KEYBOARD_CHARS
    return len(key_as_string) == 1

class LegalKey:
    """
    A class used to represent a legal key. Chars have no quote wrapping.
    >>> LegalKey('a', False)
    key=a
    >>> LegalKey('Key.shift', True)
    key=Key.shift
    """
    def __init__(self, key: str, is_special: bool):
        if not isinstance(key, str) or not isinstance(is_special, bool):
            raise TypeError('key must be a string and is_special must be a bool')
        assert(is_key_valid(key, strict=True))
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
    def __init__(self, key: str, time: Optional[float]):
        """
        >>> Keystroke("'a'", None)
        Keystroke(key='a', time=None)
        >>> Keystroke('Key.shift', 0.2222)
        Keystroke(key=Key.shift, time=0.222)
        """
        if not isinstance(key, str) or key == '':
            raise TypeError('key must be a nonempty string')
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        self.key = key
        self.time = time
        self.valid = is_key_valid(key)
        self.typeable = is_key_valid(key, strict=True)
    def __iter__(self) -> Iterator[Tuple[str, Optional[float]]]:
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
        if self.typeable:
            is_special = False
            # Assertions should always pass
            if self.key in SPECIAL_KEYS:
                # What should a legal key look like for a special key?
                print("Special key! Legal key status is None")
                is_special = True
                legal_key = self.key
            elif self.key in WEIRD_KEYS:
                legal_key = WEIRD_KEYS[self.key]
            else:
                legal_key = self.key.strip("'")
                assert(len(legal_key) == 1 and legal_key in VALID_KEYBOARD_CHARS)
            return LegalKey(legal_key, is_special)
        else:
            print(f"Could not be legalized:{self.key}<-")
            if self.valid:
                print("This is likely a unicode character that is not typable.")
            return None

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