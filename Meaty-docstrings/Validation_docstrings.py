from pynput.keyboard import Key, KeyCode
from json import JSONEncoder, JSONDecoder
from typing import Union, Optional, TypedDict
from pynput.keyboard import Key, KeyCode

class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    """
def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    """
def is_key_valid(key: Union[Key, KeyCode, str]) -> bool:
    """
    Function to check if the key is valid.
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

class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    """
    
class Log(TypedDict):
    """
    A class used to represent a log. The logfile is a list of logs.
    """
class KeystrokeDecoder(JSONDecoder):
    """
    A JSONDecoder that decodes Keystrokes [Logfile->List of Keystrokes]
    """
class KeystrokeEncoder(JSONEncoder):
    """
    A JSONEncoder that encodes Keystrokes [Keystrokes->(key, time) and Log->Logfile)]
    """

class LegalKey:
    """
    A class used to represent a legal key. Not currently implemented
    """