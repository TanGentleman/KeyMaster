# Standard library imports
from json import dump as json_dump
from json import load as json_load
from time import time, perf_counter
from uuid import uuid4
from typing import List
from threading import Timer

# Third party imports
from pynput.keyboard import Key, KeyCode, Listener
# KeyMaster imports
from utils.config import APOSTROPHE, MAX_WORDS, STOP_KEY, STOP_CODE, ROUND_DIGITS, LISTEN_TIMEOUT_DURATION, MAX_LOGGABLE_DELAY
from utils.helpers import get_filepath
from utils.validation import Keystroke, Log, KeystrokeDecoder, KeystrokeEncoder, is_key_valid, validate_keystrokes

VALIDATE_WITH_PARSER = True
if VALIDATE_WITH_PARSER:
	from classes.keyParser import KeyParser
class KeyLogger:
	"""
	A class used to log keystrokes and calculate delays between each keypress.
	This class is responsible for capturing and storing keystrokes values and timings.
	It also keeps track of the total number of words typed and the entire string of characters typed.
	"""
	def __init__(self, filename: str | None = "REG") -> None:
		"""
		Initialize the KeyLogger.

		Args:
			filename (str or None): The filename to save the log to.
			Defaults to ABSOLUTE_REG_FILEPATH.
			None value treated as null path.
		"""
		self.filename = filename
		self.keystrokes: List[Keystroke] = []
		self.word_count = 0
		self.typed_string = ""
		self.prev_time = time()
		self.timer: Timer | None = None
		self.duration = float(LISTEN_TIMEOUT_DURATION)

	def reset(self) -> None:
		"""
		Clear the current state of the logger.
		Keystrokes, the typed string, and the word count will be set to default values.
		"""
		self.keystrokes = []
		self.word_count = 0
		self.input_string = ""
		self.prev_time = time()

	# on_press still needs to be tidied up a bit
	def on_press(self, keypress: Key | KeyCode | None) -> None:
		"""
		Handles key press events and logs valid Keystroke events.

		This function is called whenever a key is pressed. 
		If key is valid, it is logged as a Keystroke object.
		KeyLogger attributes modified: keystrokes, typed_string, word_count, prev_time

		Args:
			keypress (Keypress): The key press event to handle.
		"""
		if keypress is None:
			return None
		
		# Validate keypress
		if not is_key_valid(keypress):
			return None
		
		# Calculate delay between keystrokes
		current_time = perf_counter()
		delay = current_time - self.prev_time
		self.prev_time = current_time
		if delay > MAX_LOGGABLE_DELAY:
			delay = MAX_LOGGABLE_DELAY + (delay / 1000)
		delay = round(delay, ROUND_DIGITS)

		if isinstance(keypress, KeyCode):
			# This is a non-special character
			if keypress.char is None:
				return
			key = keypress.char
			if len(key) != 1:
				print(f"CRITICAL: Keypress found with len!=1")
				return
			self.typed_string += key
			# Mark stop key or wrap the key in single quotes
			if key == STOP_KEY:
				key = STOP_CODE
			else:
				key = APOSTROPHE + key + APOSTROPHE
		else:
			if keypress == Key.space:
				self.typed_string += ' '
				self.word_count += 1
			elif keypress == Key.enter:
				self.typed_string += '\n'
			elif keypress == Key.tab:
				self.typed_string += '\t'
			# logic for backspaces, including if going back on a space
			elif keypress == Key.backspace and len(self.typed_string) > 0:
				if self.typed_string[-1] == ' ':
					self.word_count -= 1
				self.typed_string = self.typed_string[:-1]
			else:
				# Ignore special keys that are not space, enter, tab, or backspace
				return None
			key = str(keypress)

		# Create a Keystroke object and append it to the list
		# If the list is empty, the first keystroke will have delay = None
		if len(self.keystrokes) == 0:
			keystroke = Keystroke(key, None)
		else:
			keystroke = Keystroke(key, delay)
		self.keystrokes.append(keystroke)	
		return None
			
	def stop_listener_condition(self, keypress: Key | KeyCode) -> bool:
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
	
	def on_release(self, keypress: Key | KeyCode | None) -> None:
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
		listener = None
		try:
			with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
				print(f"Listening for {duration} seconds. The listener will stop on ESC, STOP_KEY, or after {MAX_WORDS} words.")
				# Start a timer of 10 seconds
				self.timer = Timer(duration, listener.stop)
				self.timer.start()
				listener.join()
		except KeyboardInterrupt:
			print("Listener stopped.")
		except Exception as e:
			print(f"An error occurred: {e}")
		finally:
			# Ensure the listener is stopped
			if listener is not None:
				listener.stop()
				print("Listener stopped!")
				
			# Ensure the timer is stopped
			if self.timer is not None:
				self.timer.cancel()
		
		return None
			

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
			print("No input string found. Log not legit")
			return False
		if not keystrokes:
			print("No keystrokes found. Log not legit")
			return False
		none_count = 0
		for keystroke in keystrokes:
			delay = keystroke.time
			if delay is None:
				none_count += 1
				if none_count > 1:
					print('None value marks first character. Only use once.')
					return False
		success = validate_keystrokes(keystrokes, input_string)
		print(f"{len(keystrokes)} Keystrokes validated: {success}")
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
			reset (bool): Whether to reset the logger after saving the log. Defaults to False.

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
		unique_id = str(uuid4())

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
		filepath = get_filepath(self.filename)
		if filepath is None:
			print("Filename null. Log not saved.")
			return False
		try:
			with open(filepath, 'r+') as f:
				logs = json_load(f, cls=KeystrokeDecoder)
				logs.append(log)
				f.seek(0)
				json_dump(logs, f, cls=KeystrokeEncoder)
				print("Logfile updated.")
		except FileNotFoundError:
			with open(filepath, 'w') as f:
				json_dump([log], f, cls=KeystrokeEncoder)
		except Exception as e:
			print(f"An error occurred: {e}")
			return False
		if reset:
			self.reset()
		return True

def run_parser_tests(logger: KeyLogger, parser) -> None:
	print("Running assertion checks on parser.")
	assert(parser.logs == [])
	new_parser_logs = [Log({"id": "None", "string": logger.typed_string, "keystrokes": logger.keystrokes})]
	parser.logs = new_parser_logs
	assert(parser.check_membership('None') is True)
	assert(parser.get_keystrokes() == logger.keystrokes)
	assert(parser.get_strings() == [logger.typed_string])
	assert(parser.id_from_substring("") == "None")
	
	print("All assertion checks passed.")


def main():
	logger = KeyLogger()
	logger.start_listener()
	success = logger.save_log()
	if not success:
		print("Log not saved.")
		return
	if VALIDATE_WITH_PARSER and KeyParser is not None:
		try:
			print("Now testing KeyParser.")
			parser = KeyParser(None)
			run_parser_tests(logger, parser)
		except:
			print(f"KeyParser error. Check the parser tests!")
			return

if __name__ == "__main__":
	main()
