# Function Documentation

This file contains documentation for all functions in the project.

## Function: `main`
## Function: `init`
Initialize the KeySimulator with the given parameters.
## Function: `calculate_delay`
Get a normally distributed delay between keystrokes.
### Parameters:
-     speed_multiple: The speed multiplier.
### Returns
    float: The delay between keystrokes.
## Function: `generate_keystrokes_from_string`
Generate valid Keystrokes from a string. Output object can be simulated.
## Function: `generate_keystroke`
Generate a single keystroke from a character.
:param char: The character to generate a keystroke for.             
:return: A Keystroke object or  None if the character is invalid.
## Function: `stop_simulation`
Stop the simulation.
## Function: `simulate_keystrokes`
Function to simulate the given keystrokes.
### Parameters:
-     keystrokes (List[Keystroke], optional): The list of keystrokes to simulate. 
## Function: `simulate_string`
Simulate the given string.
### Parameters:
-     string (str): The string to simulate.
