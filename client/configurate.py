from classes.configurator import Configurator


class Config:
    """
    The Config class is a wrapper for all the configuration options.
    """

    def __init__(
            self,
            config: Configurator | None = None,
            disable: bool | None = None,
            logging: bool | None = None,
            allow_newlines: bool | None = None,
            allow_unicode: bool | None = None,
            logfile: str | None = None,
            banned_keys: list[str] | None = None,
            round_digits: int | None = None,
            max_simulation_time: int | float | None = None,
            simulation_speed_multiple: int | float | None = None,
            exclude_outliers_in_analysis: bool | None = None,
            preload_analysis: bool | None = None
    ) -> None:
        """
        Initialize the Config class. All arguments are optional and have defaults in config.py
        """
        config = config if config is not None else Configurator()
        if not isinstance(config, Configurator):
            raise TypeError("config must be a Configurator.")

        self._config = config
        # BIG ERROR: ARGS FROM THIS WRAPPER CLASS ARE NOT BEING PASSED TO
        # CONFIGURATOR OBJECT

        self._disable = disable if disable is not None else config.disable
        self._logging = logging if logging is not None else config.logging
        self._allow_newlines = allow_newlines if allow_newlines is not None else config.allow_newlines
        self._allow_unicode = allow_unicode if allow_unicode is not None else config.allow_unicode
        self._logfile = logfile if logfile is not None else config.logfile
        self._banned_keys = banned_keys if banned_keys is not None else config.banned_keys
        self._round_digits = round_digits if round_digits is not None else config.round_digits
        self._max_simulation_time = max_simulation_time if max_simulation_time is not None else config.max_simulation_time
        self._simulation_speed_multiple = simulation_speed_multiple if simulation_speed_multiple is not None else config.simulation_speed_multiple
        self._exclude_outliers = exclude_outliers_in_analysis if exclude_outliers_in_analysis is not None else config.exclude_outliers
        self._preload = preload_analysis if preload_analysis is not None else config.preload
        self.validate_config()
        # print(self)

    def validate_config(self):
        if not isinstance(self.config, Configurator):
            raise TypeError("config must be a Configurator.")
        if not isinstance(self.disable, bool):
            raise TypeError("disable must be a bool.")
        if not isinstance(self.logging, bool):
            raise TypeError("logging must be a bool.")
        if not isinstance(self.allow_newlines, bool):
            raise TypeError("allow_newlines must be a bool.")
        if not isinstance(self.allow_unicode, bool):
            raise TypeError("allow_unicode must be a bool.")
        if not isinstance(self.logfile, str):
            raise TypeError("logfile must be a str.")
        if not isinstance(self.banned_keys, list):
            raise TypeError("banned_keys must be a list.")
        if not isinstance(self.round_digits, int):
            raise TypeError("round_digits must be an int.")
        if not isinstance(self.max_simulation_time, (int, float)):
            raise TypeError("max_simulation_time must be a number.")
        if not isinstance(self.simulation_speed_multiple, (int, float)):
            raise TypeError("simulation_speed_multiple must be a number.")
        if not isinstance(self.exclude_outliers, bool):
            raise TypeError("exclude_outliers must be a bool.")
        if not isinstance(self.preload, bool):
            raise TypeError("preload must be a bool.")
        self.config.disable = self.disable
        self.config.logging = self.logging
        self.config.allow_newlines = self.allow_newlines
        self.config.allow_unicode = self.allow_unicode
        self.config.logfile = self.logfile
        self.config.banned_keys = self.banned_keys
        self.config.round_digits = self.round_digits
        self.config.max_simulation_time = self.max_simulation_time
        self.config.simulation_speed_multiple = self.simulation_speed_multiple
        self.config.exclude_outliers = self.exclude_outliers
        self.config.preload = self.preload

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if not isinstance(value, Configurator):
            raise TypeError("config must be a Configurator.")
        self._config = value

    @property
    def disable(self):
        return self._disable

    @disable.setter
    def disable(self, value):
        if not isinstance(value, bool):
            raise TypeError("disable must be a bool.")
        self._disable = value
        self.config.disable = value

    @property
    def logging(self):
        return self._logging

    @logging.setter
    def logging(self, value):
        if not isinstance(value, bool):
            raise TypeError("logging must be a bool.")
        self._logging = value
        self.config.logging = value

    @property
    def allow_newlines(self):
        return self._allow_newlines

    @allow_newlines.setter
    def allow_newlines(self, value):
        if not isinstance(value, bool):
            raise TypeError("allow_newlines must be a bool.")
        self._allow_newlines = value
        self.config.allow_newlines = value

    @property
    def allow_unicode(self):
        return self._allow_unicode

    @allow_unicode.setter
    def allow_unicode(self, value):
        if not isinstance(value, bool):
            raise TypeError("allow_unicode must be a bool.")
        self._allow_unicode = value
        self.config.allow_unicode = value

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, value):
        if not isinstance(value, str):
            raise TypeError("logfile must be a str.")
        # TODO: Check if file exists
        # other checks?
        self._logfile = value
        self.config.logfile = value

    @property
    def banned_keys(self):
        return self._banned_keys

    @banned_keys.setter
    def banned_keys(self, value):
        if not isinstance(value, list):
            raise TypeError("banned_keys must be a list.")
        # TODO: Check if all elements are strings?
        self._banned_keys = value
        self.config.banned_keys = value

    @property
    def round_digits(self):
        return self._round_digits

    @round_digits.setter
    def round_digits(self, value):
        # TODO: Check if value is reasonable? Something like 1-5
        if not isinstance(value, int):
            raise TypeError("round_digits must be an int.")
        self._round_digits = value
        self.config.round_digits = value

    @property
    def max_simulation_time(self):
        return self._max_simulation_time

    @max_simulation_time.setter
    def max_simulation_time(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("max_simulation_time must be a number.")
        self._max_simulation_time = value
        self.config.max_simulation_time = value

    @property
    def simulation_speed_multiple(self):
        return self._simulation_speed_multiple

    @simulation_speed_multiple.setter
    def simulation_speed_multiple(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("simulation_speed_multiple must be a number.")
        self._simulation_speed_multiple = value
        self.config.simulation_speed_multiple = value

    @property
    def exclude_outliers(self):
        return self._exclude_outliers

    @exclude_outliers.setter
    def exclude_outliers(self, value):
        if not isinstance(value, bool):
            raise TypeError("exclude_outliers must be a bool.")
        self._exclude_outliers = value
        self.config.exclude_outliers = value

    @property
    def preload(self):
        return self._preload

    @preload.setter
    def preload(self, value):
        if not isinstance(value, bool):
            raise TypeError("preload must be a bool.")
        self._preload = value
        self.config.preload = value

    def __repr__(self) -> str:
        return self.config.__repr__()
