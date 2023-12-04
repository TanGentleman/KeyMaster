from client.configurate import Config
from utils.validation import Keystroke, KeystrokeList


class Generate:
    """
    The Generate class is a wrapper for all the generation options.
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the Generate class.
        """
        if config is None:
            config = Config()
        self.generator = config.KeyGenerator()

    def set_speed(self, speed: int | float) -> None:
        """
        Set the speed of the generator.
        """
        self.generator.set_speed(speed)

    def disable(self) -> None:
        """
        Disable the generator.
        """
        self.generator.disable = True

    def enable(self) -> None:
        """
        Enable the generator.
        """
        self.generator.disable = False

    def generate_keystrokes_from_string(self, string: str) -> KeystrokeList:
        """
        Generate keystrokes from a string.
        """
        return self.generator.generate_keystrokes_from_string(string)

    def generate_keystroke(self, char: str) -> Keystroke:
        """
        Generate keystrokes from a character.
        """
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Character must be a single character string.")
        keystroke = self.generator.generate_keystroke(char)
        if keystroke is None:
            raise ValueError("Character could not be generated.")
        return keystroke

    def simulate_keystrokes(self, keystrokes: KeystrokeList) -> None:
        """
        Simulate the keystroke list
        """
        self.generator.simulate_keystrokes(keystrokes)

    def simulate_string(self, string: str) -> KeystrokeList:
        """
        Simulate a string and return the KeystrokeList.
        """
        keystrokes = self.generate_keystrokes_from_string(string)
        if not keystrokes.is_empty():
            self.simulate_keystrokes(keystrokes)
        return keystrokes
