# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

### Bugs
- Squashed the unicode bugs! Compatibility strengthening each update!

## [Unreleased]
- Create test cases to ensure consistency across all 3 classes
- Formalize readable documentation and update the README file
- Move more constants to config.py
- Convert print statements to proper logging
- Repeated keypresses handled, possibly heavily reducing the time between repeated keys
- Utilize public datasets to make custom algorithm choices for generating keystroke delays
## [1.1.2] - 2023-November

### Added
- Add validation function in KeyParser class to compare keystroke lists to a string
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
- Allow KeySimulator to run simulation while self.off == True where keystroke type events will not be executed
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
- Move KeyLogger.simulate to KeySimulator

### Changed

- Things I've changed...

### Removed

- Things I've removed...
