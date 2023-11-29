from os import path

from pynput.keyboard import Key, KeyCode

from utils.config import LOG_DIR, ABSOLUTE_REG_FILEPATH, ABSOLUTE_SIM_FILEPATH, STOP_KEY
from utils.config import APOSTROPHE, STOP_CODE, SPECIAL_KEYS, BANNED_KEYS, KEYBOARD_CHARS
# *** KEY VALIDATION ***


def is_key_valid(key: Key | KeyCode | str, strict=False) -> bool:
    """
    Function to check if the key is valid.
    """
    if isinstance(key, Key):
        return key in SPECIAL_KEYS.values()
    elif isinstance(key, KeyCode):
        if key.char is None:
            return False
        key = key.char
        if key in BANNED_KEYS:
            return False
        return True
    # We know isinstance(key, str)
    # We are likely being handed an encoded string (e.g. "'a'" or 'STOP' or
    # 'Key.shift')
    key_string = key
    if key_string == STOP_CODE:
        return True
    if key_string in SPECIAL_KEYS:
        return True
    # Decode the character
    key_string = unwrap_key(key_string)

    # Check the length of the key ensure a single character
    if len(key_string) != 1:
        # Banned key enters this clause as well, still wrapped.
        # Technically this is unsafe for values of length 0, but that should
        # never happen.
        if key_string[1] in BANNED_KEYS:
            return False
        print(f"Error - is_key_valid: Invalid key length: {key_string}<-")
        # When this is inside a helper function, raise an exception instead
        # raise ValueError("is_key_valid: Error. Char length must be 1.")
        return False
    if key in BANNED_KEYS:
        return False
    # This means that both wrapped and unwrapped chars are valid
    if strict:
        return key in KEYBOARD_CHARS
    return key.isprintable()


def is_valid_wrapped_char(key: str) -> bool:
    """
    Check if a character is wrapped in single quotes.
    Characters that fail is_key_valid() return False.
    """
    return len(key) == 3 and key[0] == APOSTROPHE and is_key_valid(
        key[1]) and key[2] == APOSTROPHE


def is_valid_wrapped_special_key(key: str) -> bool:
    """
    Check if a special key is wrapped in single quotes.
    """
    if len(key) > 3 and key[0] == APOSTROPHE and key[-1] == APOSTROPHE:
        key = key[1:-1]
        return key == STOP_CODE or key in SPECIAL_KEYS
    return False


def unwrap_key(key_string: str) -> str:
    """
    Decode a key string into a single character.
    Invalid keys are not unwrapped.
    >>> unwrap_key("'a'")
    'a'
    >>> unwrap_key("'ß'")
    'ß'
    >>> unwrap_key("'√'") [This is the banned key]
    "'√'"
    """
    char = key_string
    if is_valid_wrapped_char(key_string):
        char = key_string[1]
    return char


REPLACE_WONKY_UNICODE = False
REPLACEMENTS = {
    '\u2028': '\n',  # replace line separator with newline
    '\u2029': '\n',  # replace paragraph separator with newline
    # add more replacements here if needed
}


def replace_unicode_chars(input_string: str) -> str:
    """
    Replace weird keys with their string representations.
    I have found some present occasionally when copying text in the Notes app on macOS.
    Potentially things like different unicode representations for quotes could go here too.
    """
    for old, new in REPLACEMENTS.items():
        input_string = input_string.replace(old, new)
    return input_string


def filter_non_typable_chars(input_string: str) -> str:
    """
    Filter out non-typable characters from a string.
    Returns a string with only typable characters.
    """
    return ''.join(c for c in input_string if c in KEYBOARD_CHARS)


def print_non_keyboard_chars(input_string: str) -> None:
    """
    Print non-typable characters from a string.
    """
    print(
        f"Non-keyboard character: {c} -> {ord(c)}" for c in input_string if c not in KEYBOARD_CHARS)


def clean_string(input_string: str) -> str:
    """
    Returns a string with only typable characters.
    """
    for c in input_string:
        if c not in KEYBOARD_CHARS:
            print(f"Invalid character: {c} -> {ord(c)}")
    return filter_non_typable_chars((input_string))


def clean_filename(filename: str) -> str:
    """
    Format the filename for a .json log file.
    """

    # Us os module to get the extension
    if len(filename) > 4:
        if filename[-5:] != '.json':
            filename = filename + '.json'
    # maximum length
    return filename[:255]


def get_filepath(filename: str | None) -> str | None:
    """
    Return the absolute filepath for a filename. 'REG' and 'SIM' return default logfiles.
    """
    if filename is None:
        return None

    if not filename:
        print("No filename provided.")
        return None

    if path.isabs(filename):
        filepath = filename
    elif filename.upper() == 'REG':
        filepath = ABSOLUTE_REG_FILEPATH
    elif filename.upper() == 'SIM':
        filepath = ABSOLUTE_SIM_FILEPATH
    else:
        filepath = path.join(LOG_DIR, clean_filename(filename))
    return filepath


def is_filepath_valid(filename: str | None) -> bool:
    """
    Check if the filename leads to an existing file using get_filepath.
    """
    if not filename:
        print("No filename provided.")
        return False

    filepath = get_filepath(filename)
    if not filepath:
        return False
    if not path.exists(filepath):
        print("File does not exist. (Yet?)")
        return False
    return True
