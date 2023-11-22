# KeyMaster imports
from utils.validation import clean_string

# Test using a keyboard shortcut to run a shell script `python -m tests.test "$(pbpaste)"`
# This will run the test with the contents of the clipboard.
def main(input_string = "Test print statement!"):
    print(input_string)

if __name__ == "__main__":
    from sys import argv as args
    length = len(args)
    if length > 1:
        if length > 2:
            assert False, "Too many CLI arguments"
        arg_string = args[1]
        new_string = clean_string(arg_string)
        print("old string:", arg_string)
        print("new string:", new_string)
    else:
        main("test.")

