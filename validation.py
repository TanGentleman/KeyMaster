# This file is for the key validation function and clearly typeset classes.
from typing import List, Union, Optional, Iterator, Tuple, TypedDict
from pynput.keyboard import Key, KeyCode
from config import SPECIAL_KEYS, BANNED_KEYS, WEIRD_KEYS
import json
# *** KEY VALIDATION ***
def is_key_valid(key) -> bool:
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

class LegalKey:
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

def validate_key(key: Union[Key, KeyCode, str]) -> Optional[LegalKey]:
    if is_key_valid(key):
        return LegalKey(str(key))
    else:
        return None

class Keystroke:
    def __init__(self, key: str, time: Optional[float]):
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        self.key = key
        self.time = time
        # Assuming is_key_valid is a function that checks the validity of the key
        self.valid = is_key_valid(key)
        if not self.valid:
            print(f"Keystroke class found Invalid key: {key}")

    def __iter__(self) -> Iterator[Tuple[str, Optional[float]]]:
        yield self.key, self.time

    def __repr__(self):
        return f"Keystroke(key={self.key}, time={self.time})"
    def to_json(self):
        return json.dumps([self.key, self.time])
    
class KeystrokeDecoder(json.JSONDecoder):
    def object_hook(self, dct):
        if 'keystrokes' in dct:
            dct['keystrokes'] = [Keystroke(*k) for k in dct['keystrokes']]
        return dct
class KeystrokeEncoder(json.JSONEncoder):
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
    
class Log(TypedDict):
    id: str
    string: str
    keystrokes: List[Keystroke]

class Keypress: Union[Key, KeyCode]