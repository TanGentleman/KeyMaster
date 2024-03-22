from os.path import join as join_path

from classes.converter import convert
from client.configurate import Config
from utils.validation import Log
from utils.settings import LOG_DIR
from utils.helpers import get_filepath

ENCODED_FILEPATH = join_path(LOG_DIR, "keystrokes.log")
CONVERTED_LOGFILE = "converted-keystrokes"


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
    # Analyze using backend KeyParser for direct log access
    parser = Config(logfile=logfile).config.KeyParser()
    parser.logs = logs
    parser.confirm_nuke()


def main(file=ENCODED_FILEPATH):
    logfile_as_string = read_logfile(file)
    if not logfile_as_string:
        print("Logfile is empty.")
        return
    logs = convert(logfile_as_string)
    nuke_converted_logs(logs)


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
        main(args.file)
    else:
        print("No logfile provided.")
        exit(1)
