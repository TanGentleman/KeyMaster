from convert import convert
from client.analyze import Analyze
from client.configurate import Config
# Read logfile
try:
    with open("keystrokes.log", "r") as f:
        logfile_as_string = f.read()
except FileNotFoundError:
    print("No logfile found.")
    exit(1)

# Convert logfile
logs = convert(logfile_as_string)
keystrokes = logs[0]["keystrokes"]

# Analyze logfile
config = Config(logfile='converted-keystrokes')
analyzer = Analyze(config)
analyzer.parser.logs = logs
analyzer.print_strings()
analyzer.confirm_nuke()