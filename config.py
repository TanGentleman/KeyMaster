from os import path
# Get the absolute path of the current script
ROOT = path.dirname(path.abspath(__file__))

# Define the paths for the files
ABSOLUTE_REG_FILEPATH = path.join(ROOT, "keystrokes.json")
ABSOLUTE_SIM_FILEPATH = path.join(ROOT, "simulated-keystrokes.json")
from typing import List, Optional, Tuple, Iterator, TypedDict, Union
from pynput.keyboard import Key, KeyCode

### JSON FORMAT FROM keystrokes.json
# [
#   {
#     "id": "string",
#     "string": "string",
#     "keystrokes": [
#       ["string", number]
#     ]
#   }
# ]

class Keystroke:
    def __init__(self, key: str, time: Optional[float]):
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        if not isinstance(time, float) and time is not None:
            raise TypeError('time must be a float or None')
        self.key = key
        self.time = time

    def __iter__(self) -> Iterator[Tuple[str, Optional[float]]]:
        yield self.key, self.time

    def __repr__(self):
        return f"Keystroke(key={self.key}, time={self.time})"
class Log(TypedDict):
    id: str
    string: str
    keystrokes: List[Keystroke]

class Keypress: Union[Key, KeyCode]
