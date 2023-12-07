from utils.validation import Keystroke, KeystrokeList


class Key:
    """
    The Key class is a wrapper for a Keystroke.

    Attributes
    ----------
    key (`str`): The key.
    time (`float` | `None`): The time of the keystroke.
    keystroke (`Keystroke`): The Keystroke object.
    """

    def __init__(self, key: str, time: float | None):
        self.keystroke = Keystroke(key, time)
        self.key = self.keystroke.key
        self.time = self.keystroke.time


class Keys:
    """
    The Keys class is a wrapper for a list of keystrokes.

    Attributes
    ----------
    keys (`KeystrokeList`): The KeystrokeList object.

    Methods
    -------
    is_empty(): Returns whether the list of keystrokes is empty.
    to_string(): Returns the string representation of the list of keystrokes.
    """

    def __init__(self, keys: list[Key]):
        self.keys = KeystrokeList([key.keystroke for key in keys])

    def is_empty(self) -> bool:
        return self.keys.is_empty()

    def to_string(self) -> str:
        return self.keys.to_string()
