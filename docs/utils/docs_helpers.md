# Function Documentation

## Function: `is_key_valid`
Function to check if the key is valid.
## Function: `is_valid_wrapped_char`
Check if a character is wrapped in single quotes.
Characters that fail is_key_valid() return False.
## Function: `is_valid_wrapped_special_key`
Check if a special key is wrapped in single quotes.
## Function: `unwrap_key`
Decode a key string into a single character.
Invalid keys are not unwrapped.
>>> unwrap_key("'a'")
'a'
>>> unwrap_key("'ß'")
'ß'
>>> unwrap_key("'√'") [This is the banned key]
"'√'"
## Function: `replace_unicode_chars`
Replace weird keys with their string representations.
I have found some present occasionally when copying text in the Notes app on macOS.
Potentially things like different unicode representations for quotes could go here too.
## Function: `filter_non_typable_chars`
Filter out non-typable characters from a string.
Returns a string with only typable characters.
## Function: `print_non_keyboard_chars`
Print non-typable characters from a string.
## Function: `clean_string`
Returns a string with only typable characters.
## Function: `clean_filename`
Format the filename for a .json log file.
## Function: `get_filepath`
Return the absolute filepath for a filename. 'REG' and 'SIM' return default logfiles.
## Function: `is_filepath_valid`
Check if the filename leads to an existing file using get_filepath.
