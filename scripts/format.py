# This script is for auto formatting parameters and attributes with a
# bulletpoint
from os import path
from utils.settings import ROOT
CLIENT_DIR = path.join(ROOT, "client")
FILES = [
    'collect.py',
    'analyze.py',
    'generate.py',
    'configurate.py',
    'validate.py'
]

# Assuming 'lines' is a list of lines in your file
separator_found = False
lines = []
# open each file in classes


def get_lines(filepath):
    lines = []
    with open(filepath, 'r') as f:
        lines += f.readlines()
    return lines


for filename in FILES:
    filepath = path.join(CLIENT_DIR, filename)
    lines = get_lines(filepath)
    new_file = []
    # Modify to rewrite the file
    for line in lines:
        if '----------' in line:
            separator_found = True
        elif separator_found:
            if line.lstrip()[:3] == ('"""') or line == '\n':
                separator_found = False
            # Make sure it doesn't already have a bulletpoint
            elif not line.lstrip().startswith('-'):
                # Insert a '-' after the whitespace
                # get everything to the left of the first non-whitespace
                # character
                whitespace_len = len(line) - len(line.lstrip())
                line = line[:whitespace_len] + \
                    '- ' + line[whitespace_len:]
        new_file.append(line)
    with open(filepath, 'w') as f:
        f.write(''.join(new_file))
