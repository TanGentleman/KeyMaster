# Function Documentation

This file contains documentation for all functions in the project.

## Function: `main`
## Function: `init`
Initialize the KeyLogger.
### Parameters:
-         filename (str or None): The filename to save the log to.
-         Defaults to ABSOLUTE_REG_FILEPATH.
-         None value treated as null path.
## Function: `reset`
Clear the current state of the logger.
Keystrokes, the typed string, and the word count will be set to default values.
## Function: `on_press`
Handles key press events and logs valid Keystroke events.
ERROR: FIX DOCSTRING. Args should be chunk 2, not 3
## Function: `stop_listener_condition`
Function to determine whether to stop the listener.
### Parameters:
-         keypress (Keypress): The key press event to handle.
### Returns
        bool: True if the listener should stop, False otherwise.
## Function: `on_release`
Handles key release events. Stop the listener when stop condition is met.
### Parameters:
-         keypress (Keypress): The key press event to handle.
### Returns
        False or None: False if the maximum word count is reached. This stops the listener.
## Function: `start_listener`
Function to start the key listener.
The listener will only stop when stop_listener_condition returns True.
## Function: `is_loggable`
Checks the validity of a list of keystrokes and a string. If valid, it can be logged in a Log object.
By default, this function checks the internal keystrokes and input_string attributes.
### Parameters:
-         keystrokes (List[Keystroke]): The list of keystrokes to validate.
-         input_string (str): The input string to validate.
### Returns
        bool: True if the decomposed keystrokes match the input string. False otherwise.
## Function: `set_internal_log`
Replace the internal log with the provided keystrokes and input string.
### Parameters:
-         keystrokes (List[Keystroke]): The list of keystrokes to replace self.keystrokes with.
-         input_string (str): The input string to replace self.typed_string with.
### Returns
        bool: True if state successfully replaced. False if arguments invalid.
## Function: `save_log`
Function to save the log to a file.
### Parameters:
-         reset (bool): Whether to reset the logger after saving the log. Defaults to False.
### Returns
        bool: True if the log was saved successfully, False otherwise.
