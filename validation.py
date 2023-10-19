# This file is for the key validation function to explicitly typecheck classes.
from typing import List, Union, Optional, Iterator, Tuple, TypedDict
from pynput.keyboard import Key, KeyCode
from config import SPECIAL_KEYS, BANNED_KEYS, WEIRD_KEYS
from json import JSONDecoder, JSONEncoder
import string

def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    """
    replacements = {
        '\u2028': '\n',  # replace line separator with newline
        # '\u2029': '\n',  # replace paragraph separator with newline
        # add more replacements here if needed
    }
    typable_chars = string.ascii_letters + string.digits + string.punctuation + ' \n\t'
    for c in input_string:
        if c not in typable_chars:
            print(f"Non-typable character:{c}->{ord(c)}")
    for old, new in replacements.items():
        input_string = input_string.replace(old, new)
    filtered_string = ''.join(c for c in input_string if c in typable_chars)
    return filtered_string


# *** KEY VALIDATION ***
def is_key_valid(key: Union[Key, KeyCode, str]) -> bool:
    """
    Function to check if the key is valid.
    """
    if isinstance(key, KeyCode):
        return key.char is not None
    elif isinstance(key, Key):
        key_as_string = str(key)
        return key_as_string in SPECIAL_KEYS
    
    elif isinstance(key, str):
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
    if not key_as_string.isprintable():
        print(f"Weird unprintable key: {key_as_string}")
        return False
    return len(key_as_string) == 1

class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    """
    def __init__(self, key: str, time: Optional[float]):
        # Implement LegalKey here? Or can Keystrokes have illegal keys?
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        self.key = key
        self.time = time
        self.valid = is_key_valid(key)
    def __iter__(self) -> Iterator[Tuple[str, Optional[float]]]:
        yield self.key, self.time
    def __repr__(self):
        return f"Keystroke(key={self.key}, time={self.time})"
    def __eq__(self, other):
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

class KeystrokeDecoder(JSONDecoder):
    """
    A JSONDecoder that decodes Keystrokes [Logfile->List of Keystrokes]
    """
    def object_hook(self, dct):
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
    def __repr__(self):
        return f"key={self.key}"
    def __str__(self):
        return self.key
    def __eq__(self, other):
        if isinstance(other, LegalKey):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return False
