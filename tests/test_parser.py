
from classes.keyLogger import KeyLogger
from classes.keyParser import KeyParser
from utils.validation import Log
def run_parser_tests(logger: KeyLogger) -> None:
	print("Running assertion checks on parser.")
	parser = KeyParser(None)
	assert(parser.logs == [])
	new_parser_logs = [Log({"id": "None", "string": logger.typed_string, "keystrokes": logger.keystrokes})]
	parser.logs = new_parser_logs
	assert(parser.check_membership('None') is True)
	assert(parser.get_keystrokes() == logger.keystrokes)
	assert(parser.get_strings() == [logger.typed_string])
	assert(parser.id_from_substring("") == "None")
	print("All assertion checks passed.")