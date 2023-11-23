from scripts.simulate import simulate_from_string, listen_main, clipboard_main, DEFAULT_STRING, LOGGING_DEFAULT

class Script: 
    """
    A class used to run the simulation scripts.
    """
    def __init__(self, disable = False, logging = LOGGING_DEFAULT, input_string = DEFAULT_STRING) -> None:
        """
        Initialize the Script class.
        """
        self.disable = disable
        self.logging = logging
        self.input_string = input_string

    def listen_script(self) -> None:
        listen_main(self.disable, self.logging)

    def string_script(self) -> None:
        simulate_from_string(self.input_string, self.disable, self.logging)

    def clipboard_script(self) -> None:
        clipboard_main(self.disable, self.logging)

### UI-less Shortcuts integration.
# Create a keyboard shortcut to run shell script `python -m scripts.simulate.py -c`
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Add logging flag
    parser.add_argument("--no-log", "-n", default=False, action='store_true', help="Disable logging")
    parser.add_argument("--disable", "-d", default=False, action='store_true', help="Disable simulation")
    parser.add_argument("--clipboard", "-c", action='store_true', help="Use clipboard as input")
    parser.add_argument("--listen", "-l", action='store_true', help="Listen for input")
    parser.add_argument("--string", "-s", default=DEFAULT_STRING, help="The string to simulate")

    args = parser.parse_args()

    logging = not(args.no_log)
    disable = args.disable
    input_string = args.string
    if logging:
        print("Logging ON.")
    else:
        print("Logging OFF.")
    if disable:
        print("Simulation OFF.")

    simulate = Script(disable, logging, input_string)
    
    if args.clipboard:
        simulate.clipboard_script()
    elif args.listen:
        simulate.listen_script()
    else:
        simulate.string_script()
