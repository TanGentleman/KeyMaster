import re
from uuid import uuid4
from client.generate import Generate
from utils.settings import ROUND_DIGITS
from utils.validation import Keystroke, KeystrokeList, Log
from utils.constants import LEFT_SHIFT, RIGHT_SHIFT, SHIFT_CODES, CODES, BEGIN_SPECIAL_KEY, BANNED_CODES, SHIFT_MAP
generator = Generate()
generator.disable()

KEYSTROKES_INTRO = "Keystrokes "
# TODO: Add the timestamps from prune_logfile to the logs rather than generating new ones

def get_keystroke(char: str) -> Keystroke:
    return generator.generate_keystroke(char)


def shift_char(char: str) -> str:
    assert len(char) == 1
    """
    Apply a shift to a character.
    """
    new_char = SHIFT_MAP.get(char, char)
    assert len(new_char) == 1
    return new_char


def handle_shift_sequence(snippet: str) -> tuple[KeystrokeList, int]:
    assert snippet.startswith(LEFT_SHIFT) or snippet.startswith(RIGHT_SHIFT)
    """
    Handle a shift sequence in a snippet of a logfile.
    """
    if snippet.startswith(LEFT_SHIFT):
        shift = LEFT_SHIFT
    elif snippet.startswith(RIGHT_SHIFT):
        shift = RIGHT_SHIFT
    else:
        raise ValueError("Invalid shift sequence")
    # Get the index of the next shift key
    # Modify all characters before the next shift key
    keystrokes = KeystrokeList()
    # Add the first shift key
    shift_length = len(shift)
    total_skipped_chars = shift_length
    skip_chars = 0
    skip = False
    # Iterate through each character in the snippet until the next '['
    snippet = snippet[shift_length:]
    for index in range(len(snippet)):
        # If the character is a '['
        if skip and index < skip_chars:
            continue
        skip = False
        char = snippet[index]
        if char == BEGIN_SPECIAL_KEY:
            next_key = get_next_special(snippet[index:])
            if next_key is None:
                char = shift_char(char)
                key = get_keystroke(char)
                keystrokes.append(key)
                total_skipped_chars += 1
                continue
            elif next_key == shift:
                total_skipped_chars += len(shift)
                break
            keystroke_list, skip_chars = handle_special(snippet[index:])
            keystrokes.extend(keystroke_list)
            total_skipped_chars += skip_chars
            skip_chars += index  # Since we are now skipping, we need to add the current index
            skip = True
            continue
        char = shift_char(char)
        keystroke = get_keystroke(char)
        keystrokes.append(keystroke)
        total_skipped_chars += 1
    return keystrokes, total_skipped_chars


def special_to_keystroke(special_key: str) -> Keystroke:
    """
    Convert a special key to a keystroke.

    Parameters
    ----------
    - special_key (`str`): The special key.

    Returns
    -------
    - `Keystroke`: The keystroke.
    """
    if special_key in CODES:
        return Keystroke(CODES[special_key], 3.333)
    else:
        raise ValueError("Invalid special key")


def get_next_special(snippet: str) -> str | None:
    """
    Get the next special key in a snippet of a logfile.

    Parameters
    ----------
    - snippet (`str`): The snippet of the logfile.

    Returns
    -------
    - `str | None`: The next special key.
    """
    assert snippet[0] == BEGIN_SPECIAL_KEY
    valid_specials = list(SHIFT_CODES.keys()) + list(CODES.keys())
    for code in valid_specials:
        if snippet.startswith(code):
            return code
    return None


def handle_special(snippet: str) -> tuple[KeystrokeList, int]:
    """
    Handle a special sequence in a snippet of a logfile.

    Parameters
    ----------
    - snippet (`str`): The snippet of the logfile.

    Returns
    -------
    - `tuple[KeystrokeList, int]`: The keystrokes and the number of characters to skip.
    """
    # Iterate through each character in the snippet
    assert snippet[0] == BEGIN_SPECIAL_KEY

    next_key = get_next_special(snippet)
    keystrokes = KeystrokeList()
    if next_key is None:
        skip_chars = 1
        keystrokes.append(get_keystroke(BEGIN_SPECIAL_KEY))
        return keystrokes, skip_chars
    if next_key in SHIFT_CODES:
        return handle_shift_sequence(snippet)
    elif next_key in CODES:
        keystroke = special_to_keystroke(next_key)
        skip_chars = len(next_key)
        return KeystrokeList([keystroke]), skip_chars
    else:
        print('ignoring special key:', next_key)
        skip_chars = len(next_key)
        return KeystrokeList(), skip_chars


def seek_log_start(snippet: str) -> int:
    """
    Given a snippet, returns the number of characters to skip.
    """
    assert snippet[0] == 'K'
    # get the index of the next '\n\n'

    index = snippet.find('\n\n')
    if index == -1:
        raise ValueError("Invalid log message")
    return index + 2

### LEGACY FUNCTION
# def prune_logfile(logfile_as_string: str) -> str:
#     # Remove all sequences of the strings in BANNED_CODES
#     pattern = '|'.join(re.escape(code) for code in BANNED_CODES)
#     logfile_as_string = re.sub(pattern, '', logfile_as_string)
#     return logfile_as_string.strip()

def prune_logfile(logfile_as_string: str) -> tuple[str, list[list[tuple[str, float]]]]:
    pruned_logfile = ''
    original_keystrokes: list[list[tuple[str, float]]] = []
    chunks = logfile_as_string.strip().split('\n\n\n')
    # print(len(chunks), "chunks found")
    for chunk in chunks:
        if not chunk.startswith(KEYSTROKES_INTRO):
            raise ValueError("Invalid intro to chunk")
        # TODO: I should extract date at this step')
        header, chunk = chunk.split('\n\n', 1)
        assert header, "No introduction found"
        assert chunk, "No keystrokes found"
        # This splits the header from the keystrokes
        keystrokes: list[tuple[str, float]] = []
        pruned_lines = []
        lines = chunk.split('\n')
        delay = None
        for line in lines:
            # These are either a timestamp or a key (char or special key)
            if re.match(r'^\d+\.\d+$', line):
                # This regex matches a timestamp line
                delay = float(line)
            elif line in BANNED_CODES:
                delay = None
                continue
            else:
                pruned_lines.append(line)
                if delay is None:
                    print("No timestamp found for key:", line)
                    raise ValueError("Can't set null")
                    # keystrokes.append((line, None))
                # Set the delay for each key
                else:
                    if delay < 0:
                        raise ValueError("Negative delay")
                    keystrokes.append((line, delay))
        pruned_segment = header + '\n\n' + ''.join(pruned_lines) + '\n\n'
        pruned_logfile += pruned_segment
        original_keystrokes.append(keystrokes)
    print(len(original_keystrokes), "chunks found")
    # print(keystrokes[:3], '...', keystrokes[-2:])
    # print(pruned_logfile)
    return pruned_logfile, original_keystrokes


def convert_chunk(snippet: str) -> Log | None:
    """
    Convert a snippet of a logfile into a Log dictionary.
    """
    length = len(snippet)
    if length == 0:
        return None

    keystrokes = KeystrokeList()
    skip = False
    skip_chars = 0
    skip_until_index = -1  # The index of the character to skip until
    # Iterate through the each character in the logfile
    for i in range(length):
        # If the character is a '['
        if skip and i < skip_until_index:
            continue
        skip = False
        char = snippet[i]
        if char == BEGIN_SPECIAL_KEY:
            next_key = get_next_special(snippet[i:])
            if next_key is None:
                key = get_keystroke(BEGIN_SPECIAL_KEY)
                keystrokes.append(key)
                continue
            keystroke_list, skip_chars = handle_special(snippet[i:])
            keystrokes.extend(keystroke_list)
            skip = True
            skip_until_index = i + skip_chars
            continue
        else:
            key = get_keystroke(char)
            keystrokes.append(key)
            continue
    if keystrokes.is_empty():
        return None
    return {
        "id": str(uuid4()),
        "string": keystrokes.to_string(),
        "keystrokes": keystrokes,
    }


def convert(logfile_as_string: str) -> list[Log]:
    """
    Convert a logfile into a list of dictionaries.

    Parameters
    ----------
    - logfile_as_string (`str`): The logfile.

    Returns
    -------
    - `list[dict[str, Any]]`: The list of log entries as dictionaries.
    """
    # Initialize the list of dictionaries
    logs: list[Log] = []

    # Iterate through the each character in the logfile
    text, original_keystrokes = prune_logfile(logfile_as_string)
    ignore_next_shift = False
    all_clean_keystrokes = []
    shift_count = 0
    exclude_shift = True
    for keystrokes in original_keystrokes:
        clean_keystrokes = []
        for key, delay in keystrokes:
            # remove every other shift
            if key in [LEFT_SHIFT, RIGHT_SHIFT]:
                if exclude_shift:
                    continue
                if ignore_next_shift:
                    ignore_next_shift = False
                    continue
                shift_count += 1
                clean_keystrokes.append((key, delay))
                ignore_next_shift = True
                continue
            clean_keystrokes.append((key, delay))
        all_clean_keystrokes.append(clean_keystrokes)

    chunks = text.split('\n\n')
    for chunk in chunks:
        if chunk.startswith(KEYSTROKES_INTRO):
            continue
        log = convert_chunk(chunk)
        if log is not None:
            logs.append(log)
    # Validation
    if len(logs) != len(all_clean_keystrokes):
        raise ValueError("Invalid log count")
    # Replace the delay for each keystroke
    for i in range(len(logs)):
        log = logs[i]
        clean_keystrokes = all_clean_keystrokes[i]
        if len(clean_keystrokes) != len(log['keystrokes']):
            raise ValueError("Invalid keystroke count")
        for keystroke, (key, delay) in zip(log['keystrokes'], clean_keystrokes):
            if delay is not None:
                keystroke.time = round(delay, ROUND_DIGITS)
        print('recorded keys:', len(clean_keystrokes), 'logged keys:', len(log['keystrokes']))
        # print(list(log['keystrokes']))

    # Return the list of dictionaries
    return logs
