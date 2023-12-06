from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeyGenerator
from utils.config import DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, DEFAULT_DISABLE_SIMULATION, DEFAULT_LOGGING, SIM_SPEED_MULTIPLE, DEFAULT_EXCLUDE_OUTLIERS
from utils.config import BANNED_KEYS, ROUND_DIGITS, SIM_MAX_DURATION
from scripts.simulate import simulate_from_string, clipboard_main, listen_main
from utils.helpers import resolve_filename


class Config:
    """
    The Config class is a wrapper for all the configuration options.
    It is used to pass the configuration options to the other classes.
    """

    def __init__(
            self,
            disable_simulation: bool = DEFAULT_DISABLE_SIMULATION,  # KeyGenerator and scripts
            logging: bool = DEFAULT_LOGGING,  # KeyLogger, KeyParser, and scripts
            allow_newlines: bool = DEFAULT_ALLOW_NEWLINES,  # KeyGenerator and scripts
            allow_unicode: bool = DEFAULT_ALLOW_UNICODE,  # KeyGenerator and scripts
            logfile: str | None = "REG",  # KeyLogger and KeyParser
            banned_keys: list[str] = BANNED_KEYS,
            # Warning: aliased to list referenced by is_key_valid.
            round_digits: int = ROUND_DIGITS,
            max_simulation_time: int | float = SIM_MAX_DURATION,
            simulation_speed_multiple: int | float = SIM_SPEED_MULTIPLE,
            exclude_outliers_in_analysis: bool = DEFAULT_EXCLUDE_OUTLIERS) -> None:
        """
        Initialize the Config class.
        """
        self.disable = disable_simulation
        self.logging = logging
        self.allow_newlines = allow_newlines
        self.allow_unicode = allow_unicode
        self.logfile = logfile  # Files are .json and in the logs/ directory
        # Create a copy of the banned_keys list to prevent aliasing?
        # self.banned_keys = list(banned_keys)
        self.banned_keys = banned_keys  # ["√"]
        self.round_digits = round_digits

        self.max_simulation_time = float(max_simulation_time)
        self.simulation_speed_multiple = float(simulation_speed_multiple)
        self.exclude_outliers = exclude_outliers_in_analysis
        print(self)

    # Below scripts may be pulled from Script class in the future.
    def listen_script(self) -> None:
        listen_main(
            disable=self.disable,
            logging=self.logging,
            allow_newlines=self.allow_newlines,
            allow_unicode=self.allow_unicode)

    def clipboard_script(self) -> None:
        clipboard_main(
            disable=self.disable,
            logging=self.logging,
            allow_newlines=self.allow_newlines,
            allow_unicode=self.allow_unicode)

    def string_script(self, input_string: str) -> None:
        simulate_from_string(
            input_string=input_string,
            disable=self.disable,
            logging=self.logging,
            allow_newlines=self.allow_newlines,
            allow_unicode=self.allow_unicode)

    def set(
            self,
            disable: bool | None = None,
            logging: bool | None = None,
            allow_newlines: bool | None = None,
            allow_unicode: bool | None = None,
            logfile: str | None = None,
            banned_keys: list[str] | None = None,
            round_digits: int | None = None,
            max_simulation_time: int | float | None = None,
            simulation_speed_multiple: int | float | None = None,
            exclude_outliers_in_analysis: bool | None = None) -> None:
        """
        Set any of the client-facing configuration attributes.
        """
        if disable is not None:
            self.disable = disable
        if logging is not None:
            self.logging = logging
        if allow_newlines is not None:
            self.allow_newlines = allow_newlines
        if allow_unicode is not None:
            self.allow_unicode = allow_unicode
        if logfile is not None:
            self.logfile = logfile
        if banned_keys is not None:
            self.banned_keys = banned_keys
        if round_digits is not None:
            self.round_digits = round_digits
        if max_simulation_time is not None:
            self.max_simulation_time = max_simulation_time
        if simulation_speed_multiple is not None:
            self.simulation_speed_multiple = simulation_speed_multiple
        if exclude_outliers_in_analysis is not None:
            self.exclude_outliers = exclude_outliers_in_analysis

    def ban_key(self, key: str) -> None:
        if len(key) != 1:
            raise ValueError("ban_key: Error. Char length must be 1.")
        self.banned_keys.append(key)

    def unban_key(self, key: str) -> None:
        if len(key) != 1:
            raise ValueError("unban_key: Error. Char length must be 1.")
        # remove key from banned_keys if it exists
        if key in self.banned_keys:
            self.banned_keys.remove(key)

    def KeyLogger(self) -> KeyLogger:
        if self.logging is False:
            filename = None
        else:
            filename = self.logfile
        return KeyLogger(
            filename=filename,
            only_typeable=not (self.allow_unicode),
            round_digits=self.round_digits)

    def KeyParser(self) -> KeyParser:
        if self.logging is False:
            filename = None
        else:
            filename = self.logfile
        return KeyParser(
            filename=filename,
            exclude_outliers=self.exclude_outliers)

    def KeyGenerator(self) -> KeyGenerator:
        return KeyGenerator(
            disable=self.disable,
            max_duration=self.max_simulation_time,
            allow_newlines=self.allow_newlines,
            allow_unicode=self.allow_unicode,
            round_digits=self.round_digits,
            banned_keys=list(self.banned_keys))

    def __repr__(self) -> str:
        pretty_string = (
            f"# Configuration:\ndisable={self.disable},\nlogging={self.logging},\nallow_newlines={self.allow_newlines},\n" +
            f"allow_unicode={self.allow_unicode},\nlogfile={resolve_filename(self.logfile)},\nbanned_keys={self.banned_keys},\n" +
            f"round_digits={self.round_digits}\n#")
        return pretty_string

    def __str__(self) -> str:
        return self.__repr__()
