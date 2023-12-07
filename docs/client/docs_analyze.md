# Class Documentation

## Class: `Analyze`
The Analyze class is a wrapper for all the analysis options.

# Function Documentation

## Method: `load_logfile`
Change logfile and update the logs.

Parameters
----------
- logfile (`str`): The logfile to use for logging.

## Method: `is_id_present`
Check if the string is in the logs.

Parameters
----------
- identifier (`str`): The identifier to check.

## Method: `id_by_index`
Get the identifier by index, starting from 1.

Parameters
----------
- index (`int`): The index to check.

## Method: `id_from_substring`
Get the identifier from a substring.

Parameters
----------
- substring (`str`): The substring to check.

## Method: `get_strings`
Get the strings from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.

## Method: `print_strings`
Print the strings from the logs.

Parameters
----------
- max (`int`, optional): The maximum number of strings to print.
- truncate (`int`, optional): The maximum number of characters to print.
- identifier (`str`, optional): The identifier to check.

## Method: `wpm`
Get the words per minute from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.
- exclude_outliers (`bool`, optional): Whether to exclude outliers.

## Method: `get_highest_keystroke_times`
Get the highest keystroke times from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.
- exclude_outliers (`bool`, optional): Whether to exclude outliers.

## Method: `get_average_delay`
Get the average delay from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.
- exclude_outliers (`bool`, optional): Whether to exclude outliers.

## Method: `get_std_deviation`
Get the standard deviation from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.
- exclude_outliers (`bool`, optional): Whether to exclude outliers.

## Method: `visualize_keystroke_times`
Plot the keystroke times from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.
- keystrokes (`KeystrokeList`, optional): The keystrokes to plot.
- exclude_outliers (`bool`, optional): Whether to exclude outliers.

## Method: `get_keystrokes`
Get the keystrokes from the logs.

Parameters
----------
- identifier (`str`, optional): The identifier to check.

## Method: `nuke_duplicates`
Remove duplicate strings from the logs.

## Method: `confirm_nuke`
Confirm the nuke.

## Method: `dump_modified_logs`
Dump the modified logs.

