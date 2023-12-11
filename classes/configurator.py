from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeyGenerator
from utils.config import DEFAULT_DISABLE_SIMULATION, DEFAULT_LOGGING, DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, DEFAULT_EXCLUDE_OUTLIERS, SIM_SPEED_MULTIPLE
from utils.config import BANNED_KEYS, ROUND_DIGITS, SIM_MAX_DURATION
from utils.helpers import resolve_filename


class Configurator:
    """
    The Config class is a wrapper for configuration settings.

    Use this object to pass configuration options to the other classes.

    Attributes
    ----------
    - disable (`bool`): Whether to disable the simulation.
    - logging (`bool`): Whether to enable logging.
    - allow_newlines (`bool`): Whether to allow newlines in the simulation.
    - allow_unicode (`bool`): Whether to allow unicode in the simulation.
    - logfile (`bool`): The logfile to use for logging.
    - banned_keys (`str`): The list of banned keys.
    - round_digits (`int`): The number of digits to round to.
    - max_simulation_time (`int | float`): The maximum time to simulate.
    - simulation_speed_multiple (`int`): The speed multiple to simulate at.
    - exclude_outliers_in_analysis (`bool`): Whether to exclude outliers in analysis.
    - preload_analysis (`bool`): Whether to preload the analysis.
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
            exclude_outliers_in_analysis: bool = DEFAULT_EXCLUDE_OUTLIERS,
            preload_analysis: bool = True
    ) -> None:
        """
        Initialize the Config class. All arguments are optional and have defaults in config.py
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
        # print(self)
        self.preload = preload_analysis

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
        """
        Ban a key (tied to BANNED_KEYS used for validation)
        """
        if len(key) != 1:
            raise ValueError("ban_key: Error. Char length must be 1.")
        self.banned_keys.append(key)

    def unban_key(self, key: str) -> None:
        """
        Unban a key
        """
        if len(key) != 1:
            raise ValueError("unban_key: Error. Char length must be 1.")
        # remove key from banned_keys if it exists
        if key in self.banned_keys:
            self.banned_keys.remove(key)

    def KeyLogger(self) -> KeyLogger:
        """
        Return a KeyLogger object with the current configuration.
        """
        if self.logging is False:
            filename = None
        else:
            filename = self.logfile
        return KeyLogger(
            filename=filename,
            only_typeable=not (self.allow_unicode),
            round_digits=self.round_digits,
            banned_keys=list(self.banned_keys))

    def KeyParser(self) -> KeyParser:
        """
        Return a KeyParser object with the current configuration.
        """
        if self.logging is False:
            filename = None
        else:
            filename = self.logfile
        return KeyParser(
            filename=filename,
            exclude_outliers=self.exclude_outliers,
            preload=self.preload
        )

    def KeyGenerator(self) -> KeyGenerator:
        """
        Return a KeyGenerator object with the current configuration.
        """
        return KeyGenerator(
            disable=self.disable,
            max_duration=self.max_simulation_time,
            allow_newlines=self.allow_newlines,
            allow_unicode=self.allow_unicode,
            round_digits=self.round_digits,
            banned_keys=list(self.banned_keys))

    def __repr__(self) -> str:
        changed_values = []  # List to store the changed values

        # Compare each attribute with the default configuration and add the
        # changed values to the list
        if self.disable != DEFAULT_DISABLE_SIMULATION:
            changed_values.append(f"disable={self.disable}")
        if self.logging != DEFAULT_LOGGING:
            changed_values.append(f"logging={self.logging}")
        if self.allow_newlines != DEFAULT_ALLOW_NEWLINES:
            changed_values.append(f"allow_newlines={self.allow_newlines}")
        if self.allow_unicode != DEFAULT_ALLOW_UNICODE:
            changed_values.append(f"allow_unicode={self.allow_unicode}")
        if self.logfile != "REG":
            changed_values.append(f"logfile={resolve_filename(self.logfile)}")
        if self.banned_keys != BANNED_KEYS:
            changed_values.append(f"banned_keys={self.banned_keys}")
        if self.round_digits != ROUND_DIGITS:
            changed_values.append(f"round_digits={self.round_digits}")

        if not changed_values:
            return f"Configuration=default\nLogfile:{resolve_filename(self.logfile)}"
        # Create the pretty string representation with the changed values
        pretty_string = f"# Configuration:\n" + \
            '\n'.join(changed_values) + '\n#'
        return pretty_string
