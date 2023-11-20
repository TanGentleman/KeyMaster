# This file currently simulates keystrokes from a string set in the input_string variable.
# Handy for copy/pasting the terminal output from print(keystrokes) on a list of keystrokes.
import re
from validation import Keystroke

# Input strings for "This" and "Hey there my name tanuj*"
str1 = "[Keystroke(key=Key.shift, time=None), Keystroke(key='T', time=0.5551), Keystroke(key='h', time=0.2339), Keystroke(key='i', time=0.0361), Keystroke(key='s', time=0.0513)]"
str2 = "[Keystroke(key=Key.shift, time=None), Keystroke(key='H', time=0.1647), Keystroke(key='e', time=0.1345), Keystroke(key='y', time=0.0274), Keystroke(key=Key.space, time=0.1636), Keystroke(key='t', time=0.0261), Keystroke(key='h', time=0.0927), Keystroke(key='e', time=0.1143), Keystroke(key='r', time=0.1485), Keystroke(key='e', time=0.1076), Keystroke(key=Key.space, time=0.105), Keystroke(key='m', time=0.1918), Keystroke(key='y', time=0.075), Keystroke(key=Key.space, time=0.0673), Keystroke(key='n', time=0.1648), Keystroke(key='a', time=0.0829), Keystroke(key='m', time=0.0799), Keystroke(key='e', time=0.0871), Keystroke(key=Key.space, time=0.1047), Keystroke(key='t', time=0.1156), Keystroke(key='a', time=0.1734), Keystroke(key='n', time=0.0862), Keystroke(key='u', time=0.1327), Keystroke(key='j', time=0.1233), Keystroke(key=Key.shift, time=0.1244), Keystroke(key='*', time=0.1825)]"

new_format_str = "[Keystroke(key='c', time=None), Keystroke(key='a', time=0.0391), Keystroke(key='n', time=0.1114), Keystroke(key=Key.space, time=0.1378), Keystroke(key='w', time=0.1026), Keystroke(key='e', time=0.0972), Keystroke(key=Key.space, time=0.1041), Keystroke(key='d', time=0.1385), Keystroke(key='o', time=0.0572), Keystroke(key=Key.space, time=0.1288), Keystroke(key='t', time=0.1304), Keystroke(key='h', time=0.0853), Keystroke(key='i', time=0.0552), Keystroke(key='s', time=0.0818), Keystroke(key=Key.shift, time=0.2091), Keystroke(key='?', time=0.2594), Keystroke(key=Key.enter, time=1.8442), Keystroke(key='y', time=1.9875), Keystroke(key='a', time=0.0786), Keystroke(key='y', time=0.0744), Keystroke(key=Key.shift, time=0.1622), Keystroke(key='!', time=0.2619), Keystroke(key=Key.space, time=1.1956), Keystroke(key='∫', time=2.8853), Keystroke(key=Key.shift, time=3.004), Keystroke(key=':', time=0.6483), Keystroke(key='D', time=0.2159), Keystroke(key=Key.shift, time=2.1989), Keystroke(key='*', time=0.5374)]"

SIMULATE = True

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

def main(input_string = "Test print statement!"):
    keystroke_objects = string_to_keystroke_list(input_string)
    # Print the resulting list of Keystroke objects
    for obj in keystroke_objects:
        print(obj)
    if SIMULATE:
        print('now simulating')
        from keySimulator import KeySimulator
        simulator = KeySimulator()
        simulator.simulate_keystrokes(keystroke_objects)

if __name__ == "__main__":
    from sys import argv as args
    from validation import clean_string
    length = len(args)
    if length > 1:
        if length > 2:
            assert False, "Too many CLI arguments"
        arg_string = args[1]
        new_string = clean_string(arg_string)
        main(new_string)
    else:
        main(new_format_str)
