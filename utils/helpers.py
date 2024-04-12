from os import path

from pynput.keyboard import Key, KeyCode

from utils.settings import (
    LOG_DIR,
    ABSOLUTE_REG_FILEPATH,
    ABSOLUTE_SIM_FILEPATH,
    STOP_CODE,
    SPECIAL_KEYS,
    BANNED_KEYS)
from utils.constants import DEFAULT_LOG_ID, APOSTROPHE, KEYBOARD_CHARS

REPLACE_WONKY_UNICODE = False
REPLACEMENTS = {
    '\u2028': '\n',  # replace line separator with newline
    '\u2029': '\n',  # replace paragraph separator with newline
    # add more replacements here if needed
}
# *** KEY VALIDATION ***


def is_key_valid(key: Key | KeyCode | str,
                 only_typeable: bool = False) -> bool:
    """
    Function to check if the key is valid.
    """
    if isinstance(key, Key):
        return key in SPECIAL_KEYS.values()
    elif isinstance(key, KeyCode):
        if key.char is None or len(key.char) != 1:
            return False
        char = key.char
        if char in BANNED_KEYS:
            return False
        return True
    key_string = key
    if key_string == STOP_CODE:
        return True
    if key_string in SPECIAL_KEYS:
        return True
    # Decode the character
    char = ''
    if len(key_string) != 1:
        if (key_string[0] != APOSTROPHE) or (key_string[-1] != APOSTROPHE):
            print(f"Error - is_key_valid: Invalid key length: {key_string}<-")
            return False
        char = key_string[1]
    else:
        char = key_string
    if char in BANNED_KEYS:
        return False
    # We know char is a single character
    if only_typeable:
        return key in KEYBOARD_CHARS
    return key.isprintable()


def is_valid_wrapped_char(key: str) -> bool:
    """
    Check if a character is wrapped in single quotes.
    Characters that fail is_key_valid() return False.
    """
    return (len(key) == 3
            and key[0] == APOSTROPHE
            and is_key_valid(key[1])
            and key[2] == APOSTROPHE)


def is_valid_wrapped_special_key(key: str) -> bool:
    """
    Check if a special key is wrapped in single quotes.
    """
    if len(key) > 3 and key[0] == APOSTROPHE and key[-1] == APOSTROPHE:
        key = key[1:-1]
        return key == STOP_CODE or "Key." + key in SPECIAL_KEYS
    return False


def unwrap_char(key_string: str) -> str:
    """
    Decode wrapped chars into a single character.

    Raise ValueError if a character cannot be returned.
    """
    if len(key_string) == 1:
        return key_string
    if len(
            key_string) == 3 and key_string[0] == APOSTROPHE and key_string[-1] == APOSTROPHE:
        char = key_string[1]
        return char
    else:
        raise ValueError("unwrap_char: Could not return a character.")


def replace_unicode_chars(input_string: str) -> str:
    """
    Replace weird keys with their string representations.
    I have found some present occasionally when copying text in the Notes app on macOS.
    Potentially things like different unicode representations for quotes could go here too.
    """
    for old, new in REPLACEMENTS.items():
        input_string = input_string.replace(old, new)
    return input_string


def filter_non_typeable_chars(input_string: str) -> str:
    """
    Filter out non-typeable characters from a string.
    Returns a string with only typeable characters.
    """
    return ''.join(c for c in input_string if c in KEYBOARD_CHARS)


def print_non_keyboard_chars(input_string: str) -> None:
    """
    Print non-typeable characters from a string.
    """
    print(
        f"Non-keyboard character: {c} -> {ord(c)}" for c in input_string if c not in KEYBOARD_CHARS)


def clean_string(input_string: str) -> str:
    """
    Returns a string with only typeable characters.
    """
    for c in input_string:
        if c not in KEYBOARD_CHARS:
            print(f"Invalid character: {c} -> {ord(c)}")
    return filter_non_typeable_chars((input_string))


def clean_filename(filename: str) -> str:
    """
    Format the filename for a .json log file.
    """

    # Us os module to get the extension
    if filename[-5:] != '.json' and filename[-4:] != '.log':
        filename = filename + '.json'
    # maximum length
    return filename[:255]


def get_filepath(filename: str | None) -> str | None:
    """
    Return the absolute filepath for a filename. 'REG' and 'SIM' return default logfiles.
    The file will always be a .json file in the LOG_DIR directory.
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

    if not path.exists(filepath):
        print(
            f"Warning: File {clean_filename(filename)} does not exist. (Yet?)")
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
        print("File does not exist.")
        return False
    return True


def resolve_filename(filename: str | None) -> str | None:
    """
    Resolve the filename to a valid filepath.
    """
    if not filename:
        print("No filename provided.")
        return None

    filepath = get_filepath(filename)
    if not filepath:
        return None
    # Return the last part of the filepath
    return path.basename(filepath)


def get_log_id() -> str:
    """
    Get the current log id.
    """
    filepath = path.join(LOG_DIR, "LOG_ID.txt")
    log_id = DEFAULT_LOG_ID
    try:
        with open(filepath, "r") as f:
            log_id = f.read()
            # Should I add assertions to make sure the log id is valid?
            if len(log_id) != 4:
                raise ValueError("Invalid log id. Needs to be 4 digit")
            return log_id
    except FileNotFoundError:
        return log_id
    except AssertionError:
        return log_id


def update_log_id(log_id: str) -> None:
    # Increment the number (Current is A001, update to A002)
    # Write the new number to {LOG_DIR}/LOG_ID.txt
    def next_id(id) -> str:
        """
        Get the next log id.
        """
        if len(id) != 4:
            raise ValueError("Invalid log id. Needs to be 4 digit")
        letter = id[0]
        number = int(id[1:])
        if not (ord('A') <= ord(letter) < ord('Z')):
            raise ValueError("Invalid log id. Series must be A-Z.")
        if number == 999:
            letter = chr(ord(letter) + 1)
            number = 0
        else:
            number += 1
        return letter + str(number).zfill(3)
    new_id = DEFAULT_LOG_ID
    try:
        new_id = next_id(log_id)
    except ValueError:
        print("Invalid log id. Using default.")
        pass
    filepath = path.join(LOG_DIR, "LOG_ID.txt")
    with open(filepath, "w") as f:
        f.write(new_id)
    return
