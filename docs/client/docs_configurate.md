# Class Documentation

## Class: `Config`
The Config class is a wrapper for configuration settings.

Use this object to pass configuration options to the other classes.

Attributes
----------
- disable (`bool`): Whether to disable the simulation.
- logging (`bool`): Whether to enable logging.
- allow_newlines (`bool`): Whether to allow newlines in the simulation.
- allow_unicode (`bool`): Whether to allow unicode in the simulation.
- logfile (`bool`): The logfile to use for logging.
- banned_keys (`str`): The list of banned keys.
- round_digits (`int`): The number of digits to round to.
- max_simulation_time (`int | float`): The maximum time to simulate.
- simulation_speed_multiple (`int`): The speed multiple to simulate at.
- exclude_outliers_in_analysis (`bool`): Whether to exclude outliers in analysis.

# Function Documentation

## Method: `set`
Set any of the client-facing configuration attributes.

## Method: `ban_key`
Ban a key (tied to BANNED_KEYS used for validation)

## Method: `unban_key`
Unban a key

## Method: `KeyLogger`
Return a KeyLogger object with the current configuration.

## Method: `KeyParser`
Return a KeyParser object with the current configuration.

## Method: `KeyGenerator`
Return a KeyGenerator object with the current configuration.

