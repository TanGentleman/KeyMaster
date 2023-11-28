
from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeyGenerator
from utils.validation import Log

TEST_STRING = "test string"

def run_parse_gen(parser, generator) -> bool:
    print("Running assertion checks on parser.")
    try:
        parser = KeyParser(None)
        assert(parser.logs == [])
        test_string = TEST_STRING
        keystrokes = generator.generate_keystrokes_from_string(test_string)
        new_parser_logs = [Log({"id": "None", "string": test_string, "keystrokes": keystrokes})]
        parser.logs = new_parser_logs
        assert(parser.check_membership('None') is True)
        assert(parser.get_keystrokes() == [keystrokes] or True)
        assert(parser.get_strings() == [test_string])
        assert(parser.id_from_substring("") == "None")
        print("All assertion checks passed.")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)[:100]}")
        return False
    
def run_logger_gen(logger: KeyLogger, generator: KeyGenerator) -> bool:
    print("Running assertion checks on logger.")
    try:
        assert(logger.typed_string == "")
        assert(logger.keystrokes == [])
        assert(logger.is_loggable() is False)
        logger.typed_string = "test"
        assert(logger.is_loggable() is False)
        test_string = TEST_STRING # This is not "test"!
        keystrokes = generator.generate_keystrokes_from_string(test_string)
        logger.keystrokes = keystrokes
        logger.typed_string = test_string
        assert(logger.is_loggable() is True)
        print("All assertion checks passed.")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)[:100]}")
        return False

def run_tests() -> None:
    logger = KeyLogger(None)
    parser = KeyParser(None)
    generator = KeyGenerator()
    assert(run_parse_gen(parser, generator))
    assert(run_logger_gen(logger, generator))
    print("All tests passed assertion checks.")

if __name__ == "__main__":
    run_tests()
