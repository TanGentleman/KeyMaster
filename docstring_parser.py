import re
from config import ROOT
from os import path

DEFAULT_FILE = 'keySimulator.py'
FILE_TO_WRITE = 'docstrings.py'

def find_instances(string):
    classPattern = r'class .*?""".*?"""'
    functionPattern = r'def .*?""".*?"""'

    # pattern = r'c.*?(?=b).*b' # Regular expression pattern
    # Use first class match only
    class_matches = re.findall(classPattern, string, re.DOTALL)[:1]
    # add onto class_matches
    function_matches = re.findall(functionPattern, string, re.DOTALL)
    # return combined list of matches
    print(f'{len(class_matches)} classes found and {len(function_matches)} functions found')
    return class_matches + function_matches

def read_file(filename):
    absolute_filepath = path.join(ROOT, filename)
    try:
        with open(absolute_filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def write_file(filename, string):
    absolute_filepath = path.join(ROOT, filename)
    # if filename exists, find a new filename
    if path.exists(absolute_filepath):
        print(f"File {filename} already exists")

        # try to find a new filename
        base_filename, extension = path.splitext(filename)
        
        if len(base_filename) > 50: # truncate long filenames slightly
            base_filename = base_filename[:50]
        
        i = 1
        while path.exists(absolute_filepath):
            new_filename = f'{base_filename}_{i}{extension}'
            absolute_filepath = path.join(ROOT, new_filename)
            i += 1
        filename = new_filename
    try:
        with open(absolute_filepath, 'w') as f:
            f.write(string)
            print(f"Saved file to {filename}!")
    except Exception as e:
        print(f"An error occurred: {e}")
        return


def create_docstring_file_from_string(read_filename, write_filename):
    # Read file keyParser.py as string
    file_as_string = read_file(read_filename)
    # Find all instances of docstrings
    truncated_instances_list = find_instances(file_as_string)
    if truncated_instances_list is []:
        print('No docstrings found')
        return
    # Create a string with a newline between each instance
    docstrings_as_string = '\n'.join(truncated_instances_list)
    # Save instances to docstrings.py
    write_file(write_filename, docstrings_as_string)

# Example usage
# sample_string = r'junks zdef foo() """ This is a docstring """ junk here'
# print(find_instances(sample_string))

if __name__ == "__main__":
    from sys import argv as args
    length = len(args)
    if length > 1:
        file_as_string = args[1]
        if path.exists(file_as_string):
            FILE_TO_READ = file_as_string
            create_docstring_file_from_string(FILE_TO_READ, FILE_TO_WRITE)
        else:
            print(f"File {file_as_string} not found")
    else:
        FILE_TO_READ = DEFAULT_FILE
        print(f"Using default file {FILE_TO_READ}")
        create_docstring_file_from_string(FILE_TO_READ, FILE_TO_WRITE)