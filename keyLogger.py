from pynput.keyboard import Key, KeyCode, Listener
from time import time
import json
import uuid
from os import path
from config import ROOT, ABSOLUTE_REG_FILEPATH, MAX_WORDS, STOP_KEY
from validation import Keystroke, Log, KeystrokeDecoder, KeystrokeEncoder, is_key_valid
from typing import List, Optional, Union
import threading
TIMEOUT_DURATION = 20
class KeyLogger:
    """
    A class used to log keystrokes and calculate delays between each keypress.
    This class is responsible for capturing and storing keystrokes values and timings.
    It also keeps track of the total number of words typed and the entire string of characters typed.
    """
    def __init__(self, filename: Optional[str] = "") -> None:
        self.keystrokes: List[Keystroke] = []
        self.word_count: int = 0
        self.typed_string: str = ""
        self.prev_time: float = time()
        if filename is None:
            # This will be treated as a null value
            pass
        elif filename == "":
            # This is the default keystrokes.json file (in ROOT folder for now)
            filename = ABSOLUTE_REG_FILEPATH
        else:
            # Make absolute path if not already
            if not path.isabs(filename):
                filename = path.join(ROOT, filename)
        self.filename = filename

        self.timer:Optional[threading.Timer] = None
        self.duration = float(TIMEOUT_DURATION)

    def reset(self) -> None:
        """
        Clear the current state of the logger.
        Keystrokes, the typed string, and the word count will be set to default values.
        """
        self.keystrokes = []
        self.word_count = 0
        self.input_string = ""
        self.start_time = None
        self.prev_time = time()

    # on_press still needs to be tidied up a bit
    def on_press(self, keypress: Union[Key, KeyCode, None]) -> None:
        """
        Handles key press events and logs valid Keystroke events.

        This function is called whenever a key is pressed. 
        It validates the keypress and appends the data
        KeyLogger attributes modified: keystrokes, typed_string, word_count, prev_time

        Args:
            keypress (Keypress): The key press event to handle.
        """
        if keypress is None:
            return None
        current_time = time()
        delay = current_time - self.prev_time
        if delay > 3:
            delay = 3 + (delay / 1000)

        # Alternatively, I could do Keystroke(str(keypress), delay) and then check if keypress is valid in Keystroke class
        # Right now, all Keystroke objects from this function have the property valid
        # I prefer using a Key or KeyCode object as the input key
        if is_key_valid(keypress):
            key_as_string = str(keypress)
            # Mark first character delay as None
            if not self.keystrokes:
                keystroke = Keystroke(key_as_string, None)
                self.keystrokes.append(keystroke)
            else:
                delay = round(delay, 4)  # Round to 4 decimal places
                keystroke = Keystroke(key_as_string, delay)
                self.keystrokes.append(keystroke)
            
            assert(keystroke.valid is True)
            self.prev_time = current_time # <----- Make sure this statement comes at an appropriate time.

            # Append typed character to the string
            if isinstance(keypress, KeyCode) and keypress.char is not None:
                self.typed_string += keypress.char
            elif keypress == Key.space:
                self.typed_string += ' '
                self.word_count += 1
            # logic for backspaces, including if going back on a space
            elif keypress == Key.backspace:
                self.typed_string = self.typed_string[:-1]
                if len(self.typed_string) > 0 and self.typed_string[-1]  == ' ':
                    self.word_count -= 1
            ## Enter/Tab not valid special keys, this may technically affect correctness of word count
            # elif keypress == Key.enter:
            #     # My logic is that spamming newlines should increase word count, but maybe just space is best
            #     self.typed_string += '\n'
            #     self.word_count += 1
            # elif keypress == Key.tab:
            #     self.typed_string += '\t'
            #     self.word_count += 1
        return None

    def stop_listener_condition(self, keypress: Union[Key, KeyCode]) -> bool:
        """
        Function to determine whether to stop the listener.

        Args:
            keypress (Keypress): The key press event to handle.

        Returns:
            bool: True if the listener should stop, False otherwise.
        """
        if keypress == Key.esc:
            return True
        elif self.word_count >= MAX_WORDS:
            return False
        elif isinstance(keypress, KeyCode) and keypress.char is not None:
            return keypress.char == STOP_KEY
        return False
    
    def on_release(self, keypress: Union[Key, KeyCode, None]) -> None:
        """
        Handles key release events. Stop the listener when stop condition is met.

        Args:
            keypress (Keypress): The key press event to handle.

        Returns:
            False or None: False if the maximum word count is reached. This stops the listener.
        """
        if keypress is None:
            return None
        if self.stop_listener_condition(keypress):
            print('')
            if self.timer is None:
                raise ValueError("Timer is None. Start it before listener.join")
            self.timer.cancel()
            raise KeyboardInterrupt
        return None

    def start_listener(self) -> None:
        """
        Function to start the key listener.
        The listener will only stop when stop_listener_condition returns True.
        """
        duration = self.duration
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                print(f"Listening for {duration} seconds. The listener will stop on ESC, STOP_KEY, or after {MAX_WORDS} words.")
                # Start a timer of 10 seconds
                self.timer = threading.Timer(duration, listener.stop)
                self.timer.start()
                listener.join()
        except KeyboardInterrupt:
            print("Listener stopped.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the timer is stopped
            if self.timer is not None:
                self.timer.cancel()
            # Ensure the listener is stopped
            if listener is not None:
                listener.stop()
                print("i had to do it manually!")
        

    def is_log_legit(self, keystrokes: List[Keystroke], input_string: str) -> bool:
        """
        Validates the input string and keystrokes to ensure well formatted Log.

        This function ensures keystrokes are correctly formatted and input string is nonempty.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to validate.
            input_string (str): The input string to validate.

        Returns:
            bool: True if the input is valid Log material, False otherwise.
        """
        if not input_string:
            print("No keystrokes found. Log not legit")
            return False
        none_count = 0
        for keystroke in keystrokes:
            key = keystroke.key
            delay = keystroke.time
            if delay is None:
                none_count += 1
                if none_count > 1:
                    print('None value marks first character. Only use once.')
                    return False
            elif type(key) != str or type(delay) != float:
                print('Invalid keystrokes. Format is (key:str, time:float)')
                return False
        return True

    def set_internal_log(self, keystrokes: List[Keystroke], input_string: str) -> bool:
        """
        Replace the internal log with the provided keystrokes and input string.

        Args:
            keystrokes (List[Keystroke]): The list of keystrokes to replace self.keystrokes with.
            input_string (str): The input string to replace self.typed_string with.

        Returns:
            bool: True if state successfully replaced. False if arguments invalid.
        """
        if not self.is_log_legit(keystrokes, input_string):
            print("Invalid log. Internal log not set")
            return False
        self.keystrokes = keystrokes
        self.typed_string = input_string
        self.word_count = input_string.count(' ')
        return True

    def save_log(self, reset: bool = False) -> bool:
        """
        Function to save the log to a file.

        Args:
            reset (bool, optional): Whether to reset the logger after saving the log. Defaults to False.

        Returns:
            bool: True if the log was saved successfully, False otherwise.
        """
        if not self.typed_string:
            print("No keystrokes to save.")
            if reset:
                self.reset()
            return False
        # ensure log is legit
        legit = self.is_log_legit(self.keystrokes, self.typed_string)
        if not legit:
            print("Log is not legit. Did not update file.")
            return False
        
        # Create a unique ID
        unique_id = str(uuid.uuid4())

        # Create the log object of class Log
        log: Log = {
            'id': unique_id,
            'string': self.typed_string,
            'keystrokes': self.keystrokes
        }
        # Create var logs to store the logs
        # Replace keystrokes in json using KeystrokeEncoder
        # Append the log object to the file
        logs: List[Log] = []
        if self.filename is None:
            print("Filename null. Log not saved.")
            return False
        try:
            with open(self.filename, 'r+') as f:
                logs = json.load(f, cls=KeystrokeDecoder)
                logs.append(log)
                f.seek(0)
                json.dump(logs, f, cls=KeystrokeEncoder)
                print("Logfile updated.")
        except FileNotFoundError:
            with open(self.filename, 'w') as f:
                json.dump([log], f, cls=KeystrokeEncoder)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        if reset:
            self.reset()
        return True

def main():
    logger = KeyLogger()
    logger.start_listener()
    success = logger.save_log()
    if not success:
        print("Log not saved.")
        return
    else:
        print("success!")
        from keyParser import KeyParser
        print("Running assertion checks")
        parser = KeyParser(None)
        print('parser created')
        assert(parser.logs == [])
        new_parser_logs = [{"id": "None", "string": logger.typed_string, "keystrokes": logger.keystrokes}]
        parser.logs = new_parser_logs
        assert(parser.check_membership('None') is True)
        assert(parser.get_keystrokes() == logger.keystrokes)
        assert(parser.get_strings() == [logger.typed_string])
        assert(parser.id_from_substring("") == "None")


if __name__ == "__main__":
    main()