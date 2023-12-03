from client.configurate import Config
from utils.validation import KeystrokeList

class Collect:
    """
    The Collect class is a wrapper for all the collection options.
    """
    def __init__(self, config: Config) -> None:
        """
        Initialize the Collect class.
        """
        self.collector = config.KeyLogger()

    def reset(self) -> None:
        """
        Clear the current state of the collector.
        """
        self.collector.reset()
    
    def set_filename(self, filename: str) -> None:
        """
        Set the filename of the collector.
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
        """
        self.collector.set_internal_log(keystrokes, string)

    def save_log(self, reset: bool = False) -> None:
        """
        Save the log to the log file.
        """
        self.collector.save_log(reset)