from pynput.keyboard import Key, Listener, Controller
import time
import json
import uuid

keystrokes = []
typed_string = ""
prev_time = time.time()
word_count = 0

def on_press(key):
    global prev_time, word_count, typed_string
    current_time = time.time()
    time_diff = current_time - prev_time
    keystrokes.append((str(key), time_diff))
    prev_time = current_time

    # Append typed character to the string
    if hasattr(key, 'char'):
        typed_string += key.char
    elif key == Key.space:
        typed_string += ' '
        word_count += 1
    elif key == Key.enter:
        typed_string += '\n'

    # Stop listener when 10 words have been typed
    if word_count == 5:
        return False

def on_release(key):
    if key == Key.esc:
        return False

# Use try-except block to handle potential issues
try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        print("Listener started. Type your text. The listener will stop after 10 words have been typed or when you press ESC.")
        listener.join()
except Exception as e:
    print(f"An error occurred: {e}")

# Create a unique ID
unique_id = str(uuid.uuid4())

# Create the log object
log = {
    'id': unique_id,
    'string': typed_string,
    'keystrokes': keystrokes
}

# Write the log object to a file
with open('keystrokes.json', 'w') as f:
    json.dump(log, f)

# Now simulate the keystrokes with the same timing
print('Dumped into json, now simulating back the keystrokes...')
keyboard = Controller()

for key, time_diff in keystrokes:
    try:
        time.sleep(time_diff)  # Wait for the time difference between keystrokes
        if 'Key' in key:
            key = eval(key)
            keyboard.press(key)
            keyboard.release(key)
        else:
            keyboard.type(key.strip('\''))  # Type the character
    except Exception as e:
        print(f"An error occurred: {e}")
        break
