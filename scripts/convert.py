from os.path import join as join_path

from classes.converter import convert
from client.analyze import Analyze
from client.configurate import Config
from utils.validation import Log
from utils.config import LOG_DIR
from utils.helpers import get_filepath

ENCODED_FILEPATH = join_path(LOG_DIR, "example.log")
CONVERTED_LOGFILE = "converted-keystrokes-example"
# Read logfile


def read_logfile(filename: str) -> str:
    """
    Read a logfile.

    Parameters
    ----------
    - filename (`str`): The name of the logfile.

    Returns
    -------
    - `str`: The logfile as a string.
    """
    filepath = get_filepath(filename)
    if not filepath:
        print("No logfile found.")
        return ""
    try:
        with open(filename, "r") as f:
            logfile_as_string = f.read()
    except FileNotFoundError:
        print("No logfile found.")
        return ""
    return logfile_as_string


def nuke_converted_logs(logs: list[Log], logfile=CONVERTED_LOGFILE) -> None:
    """
    Dump the converted logs into the configuration filepath.

    Parameters
    ----------
    - logs (`list[Log]`): The list of logs to dump.
    """
    # Analyze logfile using backend KeyParser class for heightened log
    # permissions
    config = Config(logfile=logfile)
    parser = config.config.KeyParser()
    # parser = Analyze(config).parser
    parser.logs = logs
    parser.confirm_nuke()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        default=ENCODED_FILEPATH,
        help="The logfile to analyze.")

    args = parser.parse_args()
    if args.file:
        logfile_as_string = read_logfile(args.file)
        if not logfile_as_string:
            print("Logfile is empty.")
            exit(1)
        logs = convert(logfile_as_string)
        nuke_converted_logs(logs)
    else:
        print("No logfile provided.")
        exit(1)
