# Standard library imports
from os import path
import string

# Third party imports
from pynput.keyboard import Key

# Set absolute paths for the logs and the docs directory
ROOT = path.dirname(path.dirname(path.abspath(__file__)))

LOG_DIR = path.join(ROOT, "logs")  # Define the path for the logfiles directory
DOCS_DIR = path.join(ROOT, "docs")  # Define the path for the docs directory
ABSOLUTE_REG_FILEPATH = path.join(LOG_DIR, "keystrokes.json")
ABSOLUTE_SIM_FILEPATH = path.join(LOG_DIR, "simulated-keystrokes.json")

### CONFIGURATION.PY CONFIG ###
DEFAULT_EXCLUDE_OUTLIERS = True
DEFAULT_DISABLE_SIMULATION = False
DEFAULT_LOGGING = True
DEFAULT_ALLOW_NEWLINES = True
DEFAULT_ALLOW_UNICODE = True
DEFAULT_STRING = "hey look ma, it's a simulation!"
BANNED_KEYS = ['√']
ROUND_DIGITS = 4  # Precision for the time value in the log files
SIM_MAX_DURATION = 30
SIM_SPEED_MULTIPLE = 10

### KeyGenerator.py CONSTANTS ###
SHOW_SHIFT_INSERTIONS = True
SIM_DELAY_MEAN = 0.06
SIM_DELAY_STD_DEV = 0.015
SIM_MAX_WORDS = 300
MIN_DELAY = 0.03
SIM_MAX_SPEED = 10  # This is the maximum speed multiple for the simulation

### KeyLogger CONSTANTS ###
DEFAULT_LISTENER_DURATION = 30
MAX_LOGGABLE_DELAY = 3
LISTENER_WORD_LIMIT = 50
COLLECT_ONLY_TYPEABLE = False

# Misc
STOP_KEY = "*"  # This key is used to stop the listener when pressed
STOP_CODE = 'STOP'
SHIFT_SPEED = 0.2222  # keystroke.time value of formulaically generated shift keystrokes
# max length of Keystroke.key (to prevent invalid overflow)
MAX_KEY_LENGTH = 20

# DO NOT CHANGE
EMPTY_WRAPPED_CHAR = "''"
APOSTROPHE = "'"
SHIFTED_CHARS = r'~!@#$%^&*()_+{}|:"<>?'
KEYBOARD_CHARS = string.ascii_letters + \
    string.digits + string.punctuation + ' \n\t'

SPECIAL_KEYS = {
    'Key.space': Key.space,
    'Key.backspace': Key.backspace,
    'Key.shift': Key.shift,
    'Key.caps_lock': Key.caps_lock,
    'Key.tab': Key.tab,
    'Key.enter': Key.enter,
}
