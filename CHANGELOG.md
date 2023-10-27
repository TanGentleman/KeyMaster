# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Bugs
- Certain unicode characters may present a discrepancy between input string and generated keystrokes

## [Unreleased]
- Make a proper feature list and update the README file
- Convert print statements to proper logging
- Implement functions to double check the consistency between Keystrokes and input strings (robust to backspace, caps lock, other tricky input keys.)
- Repeated keypresses handled, possibly heavily reducing the time between repeated keys
- Utilize public datasets to make custom algorithm choices for generating keystroke delays

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

- Compatibility of keystrokes from different sources (str, Key, Keycode) to and from logfile
- Teeny typo in keyParser.py 
- Running KeyLogger.start_listener in jupyter notebook lacks perms and stalls, need separate thread to halt in x seconds
- Running simulator.main on a string with apostrophes is now failing.
- Simulation disabling works consistently
- Move KeyLogger.simulate to KeySimulator

### Changed

- Things I've changed...

### Removed

- Things I've removed...
