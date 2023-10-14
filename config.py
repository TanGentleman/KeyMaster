from os import path
from pynput.keyboard import Key
ROOT = path.dirname(path.abspath(__file__)) # Get the absolute path of the current script

# Define the paths for the logfiles
ABSOLUTE_REG_FILEPATH = path.join(ROOT, "keystrokes.json")
ABSOLUTE_SIM_FILEPATH = path.join(ROOT, "simulated-keystrokes.json")

# *** KEY VALIDATION ***
SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock
    # 'Key.tab': Key.tab,
    # 'Key.enter': Key.enter,
    # 'Key.esc': Key.esc,
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
SIM_DELAY_MEAN = 0.06
SIM_DELAY_STD_DEV = 0.015
SIM_MAX_WORDS = 300
MIN_DELAY = 0.025

SIM_LOGGING_ON = True
SIM_ALLOW_ENTER_AND_TAB = True
SIM_SPEED_MULTIPLE = 2

if SIM_ALLOW_ENTER_AND_TAB:
    SIM_WHITESPACE_DICT = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }
else:
    SIM_WHITESPACE_DICT = {' ': Key.space}


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