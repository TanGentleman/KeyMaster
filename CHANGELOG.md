# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

See GitHub [Issues](https://github.com/tangentleman/KeyMaster/issues) for up-to date planned features and bugs

## [In Progress Goals]
- Simple, intuitively pythonic handling from an unwrapped key, to Keystroke, KeystrokeList, Log, and the classes themselves
- Jupyter notebook examples for all classes and their methods
- Formalize client facing interface functions and documentation
- Fully migrate from print statements to the logging module
- Utilize public datasets to make custom algorithm choices for generating keystroke delays

## [1.1.3] - 2023-November-2

### Added
- Patched a bunch of annoyances and creatively tackled many problems, check out the issues page!
- Added user friendly cli.py to run the program from the command line with various flags
    - These run various simple scripts defined in simulate.py
- Nailed handling obscure unicode and edge cases across various stages and functions
- Released initial test cases for cross-compatibility
- Create (getting there) consistent documentation format
    - Function info is now auto-generated for the classes using scripts/update_docs.py
- Strengthen validation of keystrokes and add `KeystrokeList` that will eventually replace `list[Keystroke]`

## [1.1.2] - 2023-November

### Added
- Add validation function in `KeyParser` class to compare keystroke lists to a string
- Implement LegalKey object for consistency of valid keystroke objects, robust to backspace, caps lock, unicode symbols, etc.
- Nuanced "Shift" keypress handling and appropriately generating in sample data
- Keystroke attributes `valid` and `typeable` allow unicode characters to be tightly controlled
- Strict validation of keystrokes with new `legalize` method that converts to object LegalKey
- Use files test.py and note built-in logging for edge cases
    - Troubleshoot unicode characters like `Invalid character: ˜ -> 732`
    - Customize list of banned characters in config.py

## [1.1.1] - 2023-October

### Added
- Add a stop_condition function to KeyLogger to allow STOP keys or word count/other checks
- include a separate thread for monitoring the elapsed time in the Listener
- Allow KeyGenerator to run simulation while self.off == True where keystroke type events will not be executed
- Implement keystroke validation and equality
- Add complex logic in Keystroke to ensure non-ascii chars aren't typed ungodly fast
- Build analysis functions in KeyParser that can compare lists of keystrokes
- Handle modifier key logic more elegantly when simulating presses (Like shift key being held down when typing "##")

### Fixed
- Constants for listening/simulating duration and max words in config.py work consistently 
- Certain unicode characters may present a discrepancy between input string and generated keystrokes
- Compatibility of keystrokes from different sources (str, Key, Keycode) to and from logfile
- Running KeyLogger.start_listener in jupyter notebook lacks perms and stalls, need separate thread to halt in x seconds
- Running simulator.main on a string with apostrophes is now failing.
- Simulation disabling works consistently
- Move KeyLogger.simulate to KeyGenerator

### Changed

- Things I've changed...

### Removed

- Things I've removed...
