from os import path
from pynput.keyboard import Key
ROOT = path.dirname(path.abspath(__file__)) # Get the absolute path of the current script
LOG_DIR = path.join(ROOT, "Logfiles") # Define the path for the logfiles directory
# Define the paths for the logfiles
ABSOLUTE_REG_FILEPATH = path.join(LOG_DIR, "keystrokes.json")
ABSOLUTE_SIM_FILEPATH = path.join(LOG_DIR, "simulated-keystrokes.json")

# *** KEY VALIDATION ***
# The below constant is used by the functions: config.is_key_valid, KeySimulator.simulate_keystrokes, and KeyLogger.on_press
SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    'Key.tab': Key.tab,
    'Key.enter': Key.enter,
    }
BANNED_KEYS = ["'√'"]
WEIRD_KEYS = { # This maps str(Key.backslash) and str(Key.Apostrophe)
    "'\\\\'": '\\',
    '"\'"': "'"
}

MAX_WORDS = 50
SPEEDHACK = True # Only applies for KeyLogger class, this will be changed
STOP_KEY = "*" # This key is used to stop the listener when pressed

### SIMULATION.PY CONFIG ###
SIM_DISABLE = False

SIM_DELAY_MEAN = 0.06
SIM_DELAY_STD_DEV = 0.015
SIM_MAX_WORDS = 300
MIN_DELAY = 0.03

SIM_ALLOW_ENTER_AND_TAB = True
SIM_SPEED_MULTIPLE = 3

if SIM_ALLOW_ENTER_AND_TAB:
    SIM_WHITESPACE_DICT = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }
    SIM_MAP_CHARS = {
        ' ': str(Key.space),
        '\t': str(Key.tab),
        '\n': str(Key.enter),
        '\\': "'\\\\'",
        "'": '"\'"'
    }
else:
    SIM_WHITESPACE_DICT = {' ': Key.space}
    SIM_MAP_CHARS = {
        ' ': str(Key.space),
        '\\': "'\\\\'",
        "'": '"\'"'
    }
    
### JSON format for keystrokes.json
# [
#   {
#     "id": "string",
#     "string": "string",
#     "keystrokes": [
#       ["string", number]
#     ]
#   }
# ]