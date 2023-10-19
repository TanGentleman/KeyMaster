# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Bugs
- Update this changelog! (I'm very behind)
## [Unreleased]
- Implement LegalKey validation and equality
- Implement proper logging instead of print statements
- Implement functions to double check the equality of all Keystrokes in the KeyLogger and KeySimulator
- Add complex logic in Keystroke to ensure non-ascii chars aren't typed ungodly fast
  - Some unicode testing needed, look into pynput docs too
- Build analysis functions in KeyParser that can compare lists of keystrokes

- Repeated keys can be handled, like heavily reducing the time between repeated keys
## [1.1.1] - 2023-10-13

### Added
- Add a stop_condition function to KeyLogger to allow STOP keys or word count/other checks
- Move KeyLogger.simulate to KeySimulator
- Simulation disabling works consistently
- include a separate thread for monitoring the elapsed time in the Listener
- Allow KeySimulator to run simulation while self.off == True where keystroke type events will not be executed

### Fixed

- Compatibility of keystrokes from different sources (str, Key, Keycode) to and from logfile
- Teeny typo in keyParser.py 
- Running KeyLogger.start_listener in jupyter notebook lacks perms and stalls, need separate thread to halt in x seconds
- Running simulator.main on a string with apostrophes is now failing.

- Handle modifier key logic more elegantly when simulating presses (Like shift key being held down when typing "##")
### Changed

- Things I've changed...

### Removed

- Things I've removed...

## [1.1.0] - 2019-02-15

### Added

- What I added...

### Fixed

- What I fixed...

## [1.0.0] - 2017-06-20
