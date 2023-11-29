# Function Documentation

## Function: `init`
Initialize the KeyLogger. If filename is None, the logger will not save to a file.
Defaults to keystrokes.json in the logs directory.
### Parameters:
- `filename` (`str` or `None`): The filename to save the log to. Use 'REG' or 'SIM' for main logfiles.
## Function: `reset`
Client facing.
Clear the current state of the logger.
## Function: `set_filename`
Client facing.
Set the filename to save logs to.
### Parameters:
- `filename` (`str`): The filename to save the log to.
## Function: `encode_keycode_char`
Not client facing.
Encodes a character by wrapping it in single quotes.
The STOP_KEY is encoded as STOP_CODE. For example, '*' may now be 'STOP'.
## Function: `encode_special_char`
Not client facing.
Encodes a special key as a string.
## Function: `log_valid_keypress`
Not client facing.
Logs a valid keypress to the internal keystrokes list.
Valid keypresses are alphanumeric characters, space, tab, enter, and backspace.
### Parameters:
- `keypress` (`Key` or `KeyCode`): The key press event to log.
## Function: `on_press`
Not client facing.
Handles the event when a key is pressed.
## Function: `stop_listener_condition`
Not client facing.
Checks if the keypress triggers a stop condition.
## Function: `on_release`
Not client facing.
Handles key release events. Stop the listener when stop condition is met.
## Function: `start_listener`
Client facing.
Function to start the key listener.
The listener will only stop when stop_listener_condition returns True.
## Function: `is_loggable`
Not client facing (This function might need revisiting)
Checks the validity of a list of keystrokes and a string. If valid, it can be logged in a Log object.
By default, this function checks the internal keystrokes and input_string attributes.
### Parameters:
- `keystrokes` (`KeystrokeList`): The list of keystrokes to validate.
- `input_string` (`str`): The input string to validate.
### Returns
`bool`: True if the decomposed keystrokes match the input string. False otherwise.
## Function: `set_internal_log`
Client facing.
Replace the internal log with the provided keystrokes and input string.
### Parameters:
- `keystrokes` (`KeystrokeList`): The list of keystrokes to replace self.keystrokes with.
- `input_string` (`str`): The input string to replace self.typed_string with.
### Returns
bool: True if state successfully replaced. False if arguments invalid.
## Function: `save_log`
Client facing.
Function to save the log to a file.
### Parameters:
- `reset` (`bool`): Whether to reset the logger after saving the log. Defaults to False.
### Returns
`bool`: True if the log was saved successfully, False otherwise.
