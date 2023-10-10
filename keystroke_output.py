from pynput.keyboard import Controller, Key
import time
import numpy as np
# def simulate_keystrokes(keystrokes):
#     keyboard = Controller()

#     for key, time_diff in keystrokes:
#         try:
#             time.sleep(time_diff)  # Wait for the time difference between keystrokes
#             if isinstance(key, Key):
#                 keyboard.press(key)
#                 keyboard.release(key)
#             else:
#                 keyboard.type(key)  # Type the character
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             break
# Key: 'c', Time difference: 0.6872968673706055
#     Key: 'a', Time difference: 0.14819002151489258
#     Key: 't', Time difference: 0.10239219665527344
#     Key: Key.space, Time difference: 0.27933382987976074
#     Key: 'd', Time difference: 0.5018448829650879
#     Key: 'o', Time difference: 0.15019631385803223
#     Key: 'g', Time difference: 0.2639338970184326
#     Key: Key.space, Time difference: 0.19953107833862305
#     Key: 'c', Time difference: 0.2928340435028076
#     Key: 'a', Time difference: 0.11474990844726562
#     Key: 't', Time difference: 0.10185384750366211
#     Key: Key.space, Time difference: 0.17363524436950684
# Sample keystrokes
keystrokes = [
    ('h', 0.1),
    ('i', 0.1),
    (Key.space, 0.2),
    ('t', 0.1),
    ('h', 0.1),
    ('e', 0.1),
    ('r', 0.1),
    ('e', 0.1),
]
# simulate_keystrokes(keystrokes)


def simulate_keystrokes(words, delay_mean, delay_standard_deviation):
    keyboard = Controller()
    for word in words:
        for char in word:
            # Generate a random time delay based on a normal distribution
            delay = np.random.normal(delay_mean, delay_standard_deviation)
            try:
                time.sleep(delay)
                keyboard.type(char) 
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        # Press Space after typing each word
        keyboard.type(' ')

words = ["Hello", "how", "are", "you"]
simulate_keystrokes(words, delay_mean=0.12, delay_standard_deviation=0.03)