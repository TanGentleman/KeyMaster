from pynput.keyboard import Key, KeyCode
from json import JSONEncoder, JSONDecoder
from typing import Union, TypedDict
from pynput.keyboard import Key, KeyCode


def replace_weird_keys(input_string: str) -> str:
    """
    Replace weird keys with their string representations.
    I have found some present occasionally when copying text in the Notes app on macOS.
    Potentially quotes with different unicode representations could go here too.
    """
def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    Returns a string with only typable characters.
    """
def clean_string(input_string: str) -> str:
    """
    Returns a string with only typable characters.
    """
def is_key_valid(key: Union[Key, KeyCode, str], strict = False) -> bool:
    """
    Function to check if the key is valid.
    """

class LegalKey:
    """
    A class used to represent a legal key. Chars have no quote wrapping.
    >>> LegalKey('a', False)
    key=a
    >>> LegalKey('Key.shift', True)
    key=Key.shift
    """

class Keystroke:
    """
    A class used to represent a keystroke. The validity is held in Keystroke.valid
    Convention is to wrap the key in single quotes if it is a character.
    >>> Keystroke("'a'", None)
    Keystroke(key='a', time=None)
    >>> Keystroke('Key.shift', 0.2222)
    Keystroke(key=Key.shift, time=0.222)
    """

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

class KeystrokeEncoder(JSONEncoder):
    """
    A JSONEncoder that encodes Keystrokes [Keystrokes->(key, time) and Log->Logfile)]
    """