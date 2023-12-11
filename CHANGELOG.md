# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

See GitHub [Issues](https://github.com/tangentleman/KeyMaster/issues) for features in the works, as well as potential bugs or questions.

## [1.1.3] - 2023-Early December
- 100 commits on the repository!
- KeyMaster 3.0 is live, with a new architecture and a focus on client facing code

### Added

- Custom JSON encoder and decoder (this was a frustrating puzzle piece)
- Robust test cases for reading/writing to logfiles
- Greatly improved validation and error handling for backend
- New testing framework for client facing code
- Add client classes `Config`, `Collect`, `Analyze`, and `Generate`
- Adjust `cli.py` to use client functions and run the program from the command line, still accepting various flags
- Handled edge cases, squashed numerous bugs, and closed many issues

### In Progress
- Fully migrate from print statements to the logging module
- Jupyter notebook walkthroughs and workflows for client facing classes
- Utilize public datasets to make custom algorithm choices for generating keystroke delays

## [1.1.3] - 2023-Late November

### Added
- Implement client-facing code with files found in the `client/` folder
- Add client files `configuration.py`, `collect.py`, `analyze.py`, and `generate.py` 
- Add `cli.py` to run scripts as defined in `simulate.py` from the command line
- Nailed handling obscure unicode and edge cases across various stages and functions
- Released initial test cases for cross-compatibility
- Auto-generate documentation for the classes using `update_docs.py`
- `KeystrokeList` replacement for `List[Keystroke]` with new methods for client facing interface

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

[Active Issues](https://github.com/tangentleman/KeyMaster/issues)