from os import path
# Get the absolute path of the current script
ROOT = path.dirname(path.abspath(__file__))

# Define the paths for the files
ABSOLUTE_FILENAME = path.join(ROOT, "keystrokes.json")
ABSOLUTE_SIM_FILENAME = path.join(ROOT, "simulated-keystrokes.json")
