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
SPEEDHACK = True
SPEEDMULTIPLIER = 2
STOP_KEY = "*" # This key is used to stop the listener when pressed

### SIMULATION.PY CONFIG ###
DEFAULT_DELAY_MEAN = 0.07
DEFAULT_DELAY_STANDARD_DEVIATION = 0.02
SIM_MAX_WORDS = 300
MIN_DELAY = 0.03

SIM_LOGGING_ON = True
SIM_ALLOW_ENTER_AND_TAB = True

if SIM_ALLOW_ENTER_AND_TAB:
    SIM_SPECIAL_KEYS = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
    }
else:
    SIM_SPECIAL_KEYS = {' ': Key.space}


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