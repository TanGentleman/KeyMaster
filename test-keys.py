from pynput.keyboard import Key, Listener, KeyCode



BANNED_KEYS = ["'√'"]
DELIMITER_KEY = "*" # This key is used to stop the listener when pressed
SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    # 'Key.tab': Key.tab,
    # 'Key.enter': Key.enter,
    # 'Key.esc': Key.esc,
}
WEIRD_KEYS = ["'\\\\'", '"\'"']

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

def on_press(key):
    print('{0} pressed: {1}'.format(key, str(key)))
    key_as_string = str(key)
    if isinstance(key, KeyCode):
        # is_char = key.char is not None
        # print(f"Keycode: {key.char} | {key.vk} | {is_char}")
        print(f"KeyCode! {is_key_valid(key_as_string)}")
    elif isinstance(key, Key):
        print(f"Key! {is_key_valid(key_as_string)}")

def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
