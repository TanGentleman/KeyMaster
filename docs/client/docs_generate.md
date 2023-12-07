# Class Documentation

## Class: `Generate`
The Generate class is a wrapper for all the generation options.

# Function Documentation

## Method: `set_speed`
Set the speed of the generator.

Parameters
----------
- speed (`int` | `float`): The speed to set.

## Method: `disable`
Disable the generator.

## Method: `enable`
Enable the generator.

## Method: `generate_keystrokes_from_string`
Generate keystrokes from a string.

Parameters
----------
- string (`str`): The string to generate keystrokes from.

Returns
-------
`KeystrokeList`: The generated keystrokes.

## Method: `generate_keystroke`
Generate keystrokes from a character.

Parameters
----------
- char (`str`): The character to generate keystrokes from.

Returns
-------
`Keystroke`: The generated keystroke.

## Method: `simulate_keystrokes`
Simulate the given keystrokes.

Parameters
----------
- keystrokes (`KeystrokeList`): The keystrokes to simulate.

## Method: `simulate_string`
Simulate a string and return the KeystrokeList.

Parameters
----------
- string (`str`): The string to simulate.

