# Class Documentation

## Class: `Collect`
The Collect class is a wrapper for all the collection options.

# Function Documentation

## Method: `reset`
Clear the current state of the collector.

## Method: `set_filename`
Set the filename of the collector.

Parameters
----------
- filename (`str`): The filename to use for logging.

## Method: `start_listener`
Start the listener.

## Method: `set_internal_log`
Replace the internal log with the provided keystrokes and input string.

Parameters
----------
- keystrokes (`KeystrokeList`): The keystrokes to use.
- string (`str`): The string to use.

## Method: `get_string`
Get the string from the collector.

## Method: `get_keystrokes`
Get the keystrokes from the collector.

## Method: `save_log`
Save the log to the log file.

