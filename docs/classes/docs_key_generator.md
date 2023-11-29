# Function Documentation

## Function: `init`
Initialize the KeyGenerator with the given parameters.
## Function: `calculate_delay`
Not client facing.
Get a normally distributed delay between keystrokes.
### Parameters:
- speed_multiple: The speed multiplier.
### Returns
float: The delay between keystrokes.
## Function: `generate_keystrokes_from_string`
Client facing.
Generate valid Keystrokes from a string. Output object can be simulated.
### Returns
KeystrokeList: A list of keystrokes.
## Function: `wrap_character`
Wrap a character in single quotes. Not client facing.
## Function: `generate_keystroke`
Generate a `Keystroke` from a character (`str`). Client facing.
## Function: `stop_simulation`
Not client facing.
Stop the simulation.
## Function: `simulate_keystrokes`
Client facing.
Function to simulate the given keystrokes.
### Parameters:
- keystrokes (KeystrokeList, optional): The list of keystrokes to simulate.
## Function: `simulate_string`
Client facing.
Simulate the given string.
### Parameters:
- string (str): The string to simulate.
## Function: `shift_eligible`
