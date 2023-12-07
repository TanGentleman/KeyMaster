from client.generate import Generate
from client.analyze import Analyze
from client.collect import Collect
from client.configurate import Config
ENABLE_BACKEND = False
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

# Client facing


# Example usage to instantiate a disabled generator and simulate 'hello world':
def method1():
    gen = Generate()
    gen.disable()
    keystrokes = gen.simulate_string("hello world")
    print(keystrokes)


def method2():
    config = Config(disable_simulation=True)
    disabled_gen = Generate(config)
    keystrokes = disabled_gen.simulate_string("hello world")
    print(keystrokes)
