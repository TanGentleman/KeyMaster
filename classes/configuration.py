from typing import List
from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeyGenerator
from scripts.simulate import DEFAULT_ALLOW_NEWLINES, DEFAULT_ALLOW_UNICODE, DEFAULT_DISABLE_SIMULATION, DEFAULT_LOGGING
from scripts.simulate import simulate_from_string, clipboard_main, listen_main
from utils.config import BANNED_KEYS, ROUND_DIGITS, SIM_MAX_DURATION

class Config:
    def __init__(self, disable: bool = DEFAULT_DISABLE_SIMULATION, logging: bool = DEFAULT_LOGGING,
                 allow_newlines: bool = DEFAULT_ALLOW_NEWLINES, allow_unicode: bool = DEFAULT_ALLOW_UNICODE,
                 logfile_name: str | None = None, banned_keys = BANNED_KEYS, round_digits = ROUND_DIGITS,
                 max_simulation_time = SIM_MAX_DURATION) -> None:
        """
        Initialize the Config class.
        """
        self.disable = disable
        self.logging = logging
        self.allow_newlines = allow_newlines
        self.allow_unicode = allow_unicode
        self.logfile_name = logfile_name # Files are .json and in the logs/ directory
        self.banned_keys = banned_keys #["√"]
        self.round_digits = round_digits

        self.max_simulation_time = max_simulation_time

    # Below scripts may be pulled from Script class in the future.
    def listen_script(self) -> None:
        listen_main(disable=self.disable, logging=self.logging, 
                        allow_newlines=self.allow_newlines, allow_unicode=self.allow_unicode)

    def clipboard_script(self) -> None:
        clipboard_main(disable=self.disable, logging=self.logging, 
                        allow_newlines=self.allow_newlines, allow_unicode=self.allow_unicode)
        
    def string_script(self, input_string: str) -> None:
        simulate_from_string(input_string=input_string, disable=self.disable, logging=self.logging, 
                             allow_newlines=self.allow_newlines, allow_unicode=self.allow_unicode)

    def set(self, disable: bool | None = None, logging: bool | None = None,
            allow_newlines: bool | None = None, allow_unicode: bool | None = None,
            log_filename: str | None = None, banned_keys: List[str] | None = None,
            round_digits: int | None = None) -> None:
        """
        Set any of the client-facing configuration attributes.
        """
        if disable != None:
            self.disable = disable
        if logging != None:    
            self.logging = logging
        if allow_newlines != None:
            self.allow_newlines = allow_newlines
        if allow_unicode != None:
            self.allow_unicode = allow_unicode
        if log_filename != None:
            self.log_filename = log_filename
        if banned_keys != None:
            self.banned_keys = banned_keys
        if round_digits != None:
            self.round_digits = round_digits

    def ban_key(self, key: str) -> None:
        if len(key) != 1:
            raise ValueError("ban_key: Error. Char length must be 1.")
        self.banned_keys.append(key)

    def KeyLogger(self) -> KeyLogger:
        if self.logging == False:
            filename = None
        else:
            filename = self.log_filename
        return KeyLogger(filename = filename, only_typeable = not(self.allow_unicode), round_digits = self.round_digits)

    def KeyParser(self) -> KeyParser:
        if self.logging == False:
            filename = None
        else:
            filename = self.log_filename
        return KeyParser(filename = filename)

    def KeyGenerator(self) -> KeyGenerator:
        return KeyGenerator(disable=self.disable, max_duration = self.max_simulation_time,
                            allow_newlines=self.allow_newlines, allow_unicode=self.allow_unicode, 
                            round_digits=self.round_digits, 
                            banned_keys=self.banned_keys)
        
    def __repr__(self) -> str:
        pretty_string = f"Configuration:\ndisable={self.disable}, \nlogging={self.logging}, \nallow_newlines={self.allow_newlines}, 
                            \nallow_unicode={self.allow_unicode}, \nlog_filename={self.log_filename}, \nbanned_keys={self.banned_keys}, 
                            \nround_digits={self.round_digits}"
        return pretty_string

    def __str__(self) -> str:
        return self.__repr__()
