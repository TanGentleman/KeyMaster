from utils.validation import Keystroke, KeystrokeList


class Key:
    """
    The Key class is a wrapper for a Keystroke.

    Attributes
    ----------
    - key (`str`): The key.
    - time (`float` | `None`): The time of the keystroke.
    - keystroke (`Keystroke`): The Keystroke object.
    """

    def __init__(self, key: str, time: float | None = None):
        try:
            self.keystroke = Keystroke(key, time)
        except Exception as e:
            print(e)
            raise ValueError("Invalid key or time.")
        self.key = self.keystroke.key
        self.time = self.keystroke.time
    
    def __repr__(self):
        return self.keystroke.props()


class Keys:
    """
    The Keys class is a wrapper for a list of keystrokes.

    Attributes
    ----------
    - keys (`KeystrokeList`): The KeystrokeList object.

    Methods
    -------
    - is_empty(): Returns whether the list of keystrokes is empty.
    - to_string(): Returns the string representation of the list of keystrokes.
    """

    def __init__(self, keys: list[Key] | KeystrokeList):
        if isinstance(keys, KeystrokeList):
            self.keys = keys
        elif isinstance(keys, list):
            try:
                self.keys = KeystrokeList([key.keystroke for key in keys])
            except:
                raise TypeError("Invalid KeystrokeList.")
        else:
            raise TypeError("Invalid type for Keys.")

    def is_empty(self) -> bool:
        return self.keys.is_empty()

    def to_string(self) -> str:
        return self.keys.to_string()
    
    def __repr__(self):
        return 'Keys=' + self.to_string()
