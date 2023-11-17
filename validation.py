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
def is_key_valid(key: Union[Key, KeyCode, str]) -> bool:
    """
    Function to check if the key is valid.
    """
    if isinstance(key, KeyCode):
        return key.char is not None
    elif isinstance(key, Key):
        return key in SPECIAL_KEYS.values()
    else:
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
    return len(key_as_string) == 1

class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    """
    def __init__(self, key: str, time: Optional[float]):
        # Implement LegalKey here? Or can Keystrokes have illegal keys?
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        if not isinstance(key, str) or key == '':
            raise TypeError('key must be a nonempty string')
        self.key = key
        self.time = time
        self.valid = is_key_valid(key)
        self.typeable = self.valid and all(c in VALID_KEYBOARD_CHARS for c in key)
    def __iter__(self) -> Iterator[Tuple[str, Optional[float]]]:
        yield self.key, self.time
    def __repr__(self):
        return f"Keystroke(key={self.key}, time={self.time})"
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Keystroke):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return False
    
def check_keystrokes_legit(keystrokes: List[Keystroke]) -> bool:
	"""
	Function to check if the keystrokes are valid.
	"""
	if keystrokes == []:
		return True
	for keystroke in keystrokes:
		if not keystroke.valid:
			print(f"Invalid keystroke: {keystroke.key}")
			return False
	return True
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

class LegalKey:
    """
    A class used to represent a legal key. Not currently implemented
    """
    def __init__(self, key: str):
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        if not is_key_valid(key):
            raise ValueError(f'Key {key} failed is_key_valid()')
        self.key = key
    def __repr__(self) -> str:
        return f"key={self.key}"
    def __str__(self):
        return self.key
    def __eq__(self, other):
        if isinstance(other, LegalKey):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
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
        if key in SPECIAL_KEYS:
            key = SPECIAL_KEYS[key]
            if key == Key.backspace and output_string != '':
                output_string = output_string[:-1]  # Remove the last character
            elif key == Key.space:
                output_string += ' '
                word_count += 1
            elif key == Key.enter:
                output_string += '\n'
            elif key == Key.tab:
                output_string += '\t'
            else:
                pass # Ignore CapsLock and Shift
        else:
            # Append the character to the output string
            # It is 1 character because it passed is_key_valid() and is not in SPECIAL_KEYS
            output_string += key.strip("'")
    return output_string