# Standard library imports
from os import path
import string

# Third party imports
from pynput.keyboard import Key

# Set paths to json logs.
ROOT = path.dirname(path.dirname(path.abspath(__file__))) # abs path of the repo root directory

LOG_DIR = path.join(ROOT, "logs") # Define the path for the logfiles directory
DOCS_DIR = path.join(ROOT, "docs") # Define the path for the docs directory
ABSOLUTE_REG_FILEPATH = path.join(LOG_DIR, "keystrokes.json")
ABSOLUTE_SIM_FILEPATH = path.join(LOG_DIR, "simulated-keystrokes.json")

### SIMULATION.PY CONFIG ###
SIM_MAX_DURATION = 30
SIM_DISABLE = False
SHOW_SHIFT_INSERTIONS = True

SIM_DELAY_MEAN = 0.06
SIM_DELAY_STD_DEV = 0.015
SIM_MAX_WORDS = 300
MIN_DELAY = 0.03

ALLOW_SIMULATING_UNICODE = True
ALLOW_SIMULATING_NEWLINES = True

SIM_SPEED_MULTIPLE = 5

### KEYLOGGER.PY CONFIG ###
LISTEN_TIMEOUT_DURATION = 30
MAX_LOGGABLE_DELAY = 3
MAX_WORDS = 50
SPEEDHACK = True # Only applies for KeyLogger class, this will be changed

# Misc
STOP_KEY = "*" # This key is used to stop the listener when pressed
STOP_CODE = 'STOP'
BANNED_KEYS = ['√']
SHIFT_SPEED = 0.2222 # This is the speed of all logical insertions of Key.shift when generating keystrokes
ROUND_DIGITS = 4 # This is for logfile timestamps

# DO NOT CHANGE
EMPTY_WRAPPED_CHAR = "''"
APOSTROPHE = "'"
SHIFTED_CHARS = r'~!@#$%^&*()_+{}|:"<>?'
KEYBOARD_CHARS = string.ascii_letters + string.digits + string.punctuation + ' \n\t'

SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    'Key.tab': Key.tab,
    'Key.enter': Key.enter,
    }

if ALLOW_SIMULATING_NEWLINES:
    whitespace_dict = {
        ' ': str(Key.space),
        '\t': str(Key.tab),
        '\n': str(Key.enter),
    }
else:
    whitespace_dict = {
        ' ': str(Key.space),
        '\t': str(Key.tab),
    }
SIM_WHITESPACE_DICT = whitespace_dict
    
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