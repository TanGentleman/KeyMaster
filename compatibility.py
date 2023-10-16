# This file currently simulates keystrokes from a string set in the input_string variable.

import re
from validation import Keystroke

# Input string
input_str = "[Keystroke(key=Key.shift, time=None), Keystroke(key='T', time=0.5551), Keystroke(key='h', time=0.2339), Keystroke(key='i', time=0.0361), Keystroke(key='s', time=0.0513)]"
input_str = "[Keystroke(key=Key.shift, time=None), Keystroke(key='H', time=0.1647), Keystroke(key='e', time=0.1345), Keystroke(key='y', time=0.0274), Keystroke(key=Key.space, time=0.1636), Keystroke(key='t', time=0.0261), Keystroke(key='h', time=0.0927), Keystroke(key='e', time=0.1143), Keystroke(key='r', time=0.1485), Keystroke(key='e', time=0.1076), Keystroke(key=Key.space, time=0.105), Keystroke(key='m', time=0.1918), Keystroke(key='y', time=0.075), Keystroke(key=Key.space, time=0.0673), Keystroke(key='n', time=0.1648), Keystroke(key='a', time=0.0829), Keystroke(key='m', time=0.0799), Keystroke(key='e', time=0.0871), Keystroke(key=Key.space, time=0.1047), Keystroke(key='t', time=0.1156), Keystroke(key='a', time=0.1734), Keystroke(key='n', time=0.0862), Keystroke(key='u', time=0.1327), Keystroke(key='j', time=0.1233), Keystroke(key=Key.shift, time=0.1244), Keystroke(key='*', time=0.1825)]"

def string_to_keystroke_list(input_str):
    # Regular expression pattern to match the key and time values
    pattern = r"Keystroke\(key=(.*?), time=(.*?)\)"

    # Find all matches in the input string
    matches = re.findall(pattern, input_str)

    # Create a list of Keystroke objects
    keystroke_objects = []
    for key, time in matches:
        # Remove quotes from the key value
        key = key.strip("'")
        # Convert the time value to float or None
        time = float(time) if time != 'None' else None
        keystroke_objects.append(Keystroke(key, time))
    return keystroke_objects

keystroke_objects = string_to_keystroke_list(input_str)
# # Print the resulting list of Keystroke objects
# for obj in keystroke_objects:
#     print(obj)

# print('now simulating')
# from keySimulator import KeySimulator
# simulator = KeySimulator()
# simulator.simulate_keystrokes(keystroke_objects)
