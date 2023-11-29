# Function Documentation

## Function: `is_id_in_log`
Client facing.
Check if a log with the identifier exists in the loaded logs.
### Parameters:
- `identifier` (`str`): The UUID or exact string formatted as STOP_KEY + string
- `log` (`Log`): The log to check.
### Returns
`bool`: True if a log with the given UUID or exact string exists, False otherwise.
## Function: `init`
## Function: `__repr__`
## Function: `__eq__`
## Function: `init`
>>> Keystroke("'a'", None)
Keystroke(key='a', time=None)
>>> Keystroke('Key.shift', 0.2222)
Keystroke(key=Key.shift, time=0.222)
## Function: `__iter__`
## Function: `__repr__`
## Function: `__eq__`
## Function: `legalize`
Returns a LegalKey object or None if the key is not valid.
## Function: `init`
## Function: `append`
## Function: `__iter__`
## Function: `__getitem__`
## Function: `__len__`
## Function: `__repr__`
## Function: `__eq__`
## Function: `extend`
## Function: `to_string`
Returns the string representation of the keystrokes.
## Function: `validate`
Validate a list of Keystroke objects against a string.
### Parameters:
- keystrokes (KeystrokeList): A list of Keystroke objects.
- input_string (str): The string to validate against.
### Returns
bool: True if the decomposed keystrokes match the input string.
## Function: `object_hook`
## Function: `default`
