from client.configurate import Config
from utils.validation import KeystrokeList


class Collect:
    """
    The Collect class is a wrapper for all the collection options.
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the Collect class.
        """
        if config is None:
            config = Config()
        self.collector = config.KeyLogger()

    def reset(self) -> None:
        """
        Clear the current state of the collector.
        """
        self.collector.reset()

    def set_filename(self, filename: str) -> None:
        """
        Set the filename of the collector.

        Parameters
        ----------
        - filename (`str`): The filename to use for logging.
        """
        self.collector.set_filename(filename)

    def start_listener(self) -> None:
        """
        Start the listener.
        """
        self.collector.start_listener()

    def set_internal_log(self, keystrokes: KeystrokeList,
                         string: str) -> None:
        """
        Replace the internal log with the provided keystrokes and input string.

        Parameters
        ----------
        - keystrokes (`KeystrokeList`): The keystrokes to use.
        - string (`str`): The string to use.
        """
        self.collector.set_internal_log(keystrokes, string)

    def get_string(self) -> str:
        """
        Get the string from the collector.
        """
        return self.collector.typed_string

    def get_keystrokes(self) -> KeystrokeList:
        """
        Get the keystrokes from the collector.
        """
        return self.collector.keystrokes

    def save_log(self) -> None:
        """
        Save the log to the log file.
        """
        self.collector.save_log()

    def __repr__(self) -> str:
        return self.collector.__repr__()
