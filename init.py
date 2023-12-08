# Client facing
from client.generate import Generate
from client.analyze import Analyze
from client.collect import Collect
from client.configurate import Config
ENABLE_BACKEND = False
ENABLE_VALIDATION = True
if __name__ == "__main__":
    print("You can import the following classes from this module:" +
          ("\nBackend: KeyLogger, KeyParser, KeyGenerator" if ENABLE_BACKEND else "") +
          "\nConfig, Collect, Analyze, Generate.")
    exit(0)

# Backend
if ENABLE_BACKEND:
    from classes.key_collector import KeyLogger
    from classes.key_analyzer import KeyParser
    from classes.key_generator import KeyGenerator
if ENABLE_VALIDATION:
    from client.validate import Key, Keys

