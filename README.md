# KeyMaster

Command your keyboard! Even while afk :D 

Check out the Docs folder for documentation without the clutter of the function bodies.

## Features
Powerful classes to:
- Listen, filter, collect, and log keystrokes (key_collector.py)
- Load, parse, analyze, and visualize cross-compatible data (key_analyzer.py)
- Generate and simulate human-realistic keystrokes (key_generator.py)

KeyMaster excels at the backend validation, so configuration is easy and intuitive.
- Validate what it means to be an acceptable Keystroke or valid Log entry (validation.py)
- Configure filepaths and constants in config.py

## Running
- I've made some sample workflows for automation, you can run it using simulate.py alongside appropriate CLI arguments
- I typically use the MacOS shortcuts app to run the script with a hotkey
- Example use case: Paste using command-opt-v to simulates the typing of the clipboard contents (With custom speed or even personalized behavior)
- These will now be in the interface of scripts/cli.py
