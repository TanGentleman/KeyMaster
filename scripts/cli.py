from client.configurate import Config
from scripts.simulate import simulate_from_string, listen_main, clipboard_main
from utils.config import DEFAULT_DISABLE_SIMULATION, DEFAULT_LOGGING, DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, DEFAULT_STRING
import argparse


class Script:
    """
    A class used to run the simulation scripts.

    Attributes
    ----------
    config (`Config`): The configuration object.
    disable (`bool`): Whether to disable the simulation.
    logging (`bool`): Whether to enable logging.
    allow_newlines (`bool`): Whether to allow newlines in the simulation.
    allow_unicode (`bool`): Whether to allow unicode in the simulation.
    input_string (`str`): The string to simulate.
    """

    def __init__(
            self,
            config: Config | None = None,
            disable: bool | None = None,
            logging: bool | None = None,
            allow_newlines: bool | None = None,
            allow_unicode: bool | None = None,
            input_string: str | None = None) -> None:
        """
        Initialize the Script class.
        """
        if config is None:
            config = Config()
        self.config = config
        if disable is not None:
            self.config.disable = disable
        if logging is not None:
            self.config.logging = logging
        if allow_newlines is not None:
            self.config.allow_newlines = allow_newlines
        if allow_unicode is not None:
            self.config.allow_unicode = allow_unicode
        self.input_string = input_string or DEFAULT_STRING

    def listen_script(self) -> None:
        listen_main(
            self.config.disable,
            self.config.logging,
            self.config.allow_newlines,
            self.config.allow_unicode)

    def string_script(self) -> None:
        simulate_from_string(
            self.input_string,
            self.config.disable,
            self.config.logging,
            self.config.allow_newlines,
            self.config.allow_unicode)

    def clipboard_script(self) -> None:
        clipboard_main(
            self.config.disable,
            self.config.logging,
            self.config.allow_newlines,
            self.config.allow_unicode)

# UI-less Shortcuts integration.
# Create a keyboard shortcut to run shell script `python -m
# scripts.simulate.py -c`


def main():
    parser = argparse.ArgumentParser()
    # Add flags
    parser.add_argument(
        "--disable",
        "-d",
        default=DEFAULT_DISABLE_SIMULATION,
        action='store_true',
        help="Disable simulation")
    parser.add_argument(
        "--no-log",
        "-n",
        default=not (DEFAULT_LOGGING),
        action='store_true',
        help="Disable logging")
    parser.add_argument(
        "--no-newlines",
        "-nn",
        default=not (DEFAULT_ALLOW_NEWLINES),
        action='store_true',
        help="Disable simulating newlines")
    parser.add_argument(
        "--no-unicode",
        "-nu",
        default=not (DEFAULT_ALLOW_UNICODE),
        action='store_true',
        help="Disable simulating unicode")

    # Choose script to run
    parser.add_argument(
        "--clipboard",
        "-c",
        action='store_true',
        help="Use clipboard as input")
    parser.add_argument(
        "--listen",
        "-l",
        action='store_true',
        help="Listen for input")
    parser.add_argument(
        "--string",
        "-s",
        default=DEFAULT_STRING,
        help="The string to simulate")

    args = parser.parse_args()

    disable = args.disable
    logging = not (args.no_log)
    allow_newlines = not (args.no_newlines)
    allow_unicode = not (args.no_unicode)
    input_string = args.string

    if disable:
        print("Simulation OFF.")
    if logging:
        print("Logging ON.")
    else:
        print("Logging OFF.")
    if allow_newlines:
        print("Simulating newlines ON.")
    if not allow_unicode:
        print("Simulating unicode OFF.")
    if input_string != DEFAULT_STRING:
        print(f"Input string: {input_string[:5]}" +
              ("[...]" if len(input_string) > 5 else ""))

    simulate = Script(
        None,
        disable,
        logging,
        allow_newlines,
        allow_unicode,
        input_string)

    if args.clipboard:
        simulate.clipboard_script()
    elif args.listen:
        simulate.listen_script()
    else:
        simulate.string_script()


if __name__ == "__main__":
    main()
