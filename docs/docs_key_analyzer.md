# Function Documentation

This file contains documentation for all functions in the project.

## Function: `is_id_in_log`
Check if a log with the identifier exists in the loaded logs.
### Parameters:
- `identifier` (`str`): The UUID or exact string formatted as STOP_KEY + string
- `log` (`Log`): The log to check.
### Returns
`bool`: True if a log with the given UUID or exact string exists, False otherwise.
## Function: `init`
Initialize the KeyParser and load logs. None value for filename will initialize an empty KeyParser.
## Function: `load_logs`
Load logs from the file.
## Function: `extract_logs`
Reads logfile and extracts logs.
### Returns
`list`: A list of logs loaded from the file. If an error occurs, an empty list is returned.
## Function: `check_membership`
Check if a log with the identifier exists in the loaded logs.
### Parameters:
- `identifier` (`str`): The UUID or exact string to check for.
### Returns
`bool`: True if a log with the given UUID or exact string exists, False otherwise.
## Function: `id_by_index`
Get the ID of the log at a given index. 
Index begins at 1, as labeled in method `print_strings`.
### Parameters:
- `index` (`int`): The index of the log to get the ID of.
### Returns
`str` or `None`: The ID of the log at the given index. If no such log is found, `None` is returned.
## Function: `id_from_substring`
Get the ID of the first log that contains a given substring.
### Parameters:
- `keyword` (`str`): The substring to search for.
### Returns
`str` or `None`: The ID of the first log that contains the substring. If no such log is found, `None` is returned.
## Function: `get_strings`
Get a list of all strings in the logs. If an identifier is provided, 
only the associated string is included.
### Parameters:
- `identifier` (`str`, optional): The UUID or exact string to check for.
### Returns
`list`: A list of all strings in the logs. If an identifier is provided,
the list contains the string associated with that identifier.
If the identifier is not found, an empty list is returned.
## Function: `print_strings`
Prints strings from logs. If `identifier` is provided, prints associated string.
Strings longer than `truncate` value are appended with "...[truncated]".
### Parameters:
- `max` (int): Maximum number of strings to print. Defaults to 5.
- `truncate` (int): Maximum number of characters to print. Defaults to 25.
- `identifier` (str, optional): The UUID or exact string to check for.
## Function: `get_only_times`
Get a list of all keystroke delay times.
### Parameters:
- `identifier` (str, optional): The UUID or exact string to check for.
### Returns
`List[float]`: A list of float values.
## Function: `wpm`
Calculate the average words per minute.
Formula is CPM/5, where CPM is characters per minute.
### Parameters:
- `identifier` (str, optional): The UUID or exact string to check for.
### Returns
`float` or `None`: If no characters are found, None is returned.
## Function: `get_highest_keystroke_times`
Get the highest keystroke time for each log.
### Parameters:
- `identifier` (str, optional): The UUID or exact string to check for.
### Returns
`list`: A list of float values.
## Function: `get_average_delay`
Get the average time between keystrokes.
### Parameters:
- `identifier` (str, optional): The UUID or exact string to check for.
### Returns
`float` or `None`: Return average delay in seconds. If no keystroke times are found, None is returned.
## Function: `get_std_deviation`
Get the standard deviation of the time between keystrokes.
### Returns
`float` or `None`: If insufficient keystrokes are found, None is returned.
## Function: `visualize_keystroke_times`
Plots the average keystroke time for each character.
### Parameters:
- `identifier` (`str`, optional): The UUID or exact string to check for.
- `keystrokes`: (`KeystrokeList`, optional): A list of Keystroke items.
- `exclude_outliers` (bool, optional): A flag indicating whether to exclude outliers.
## Function: `get_keystrokes`
Get a list of all keystrokes in the logs.
### Parameters:
- identifier (str, optional): The UUID or exact string to check for.
### Returns
list: A list of Keystroke items.

## Function: `map_chars_to_times`
Calculates the average keystroke time for each character based on the provided keystrokes.
### Parameters:
- `keystrokes` (list, optional): A list of Keystroke items.
### Returns
`dict`: A dictionary mapping each character to its average keystroke time.
## Function: `visualize_keystroke_differences`
## Function: `nuke_duplicates`
Remove duplicate logs from the logs list.
## Function: `confirm_nuke`
This is a fun alias for dump_modified_logs.
## Function: `dump_modified_logs`
Save the changes to the logfile (likely made by nuke_duplicates).
