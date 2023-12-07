from init import *
# This import is equivalent to the following:

# from client.configurate import Config
# from client.collect import Collect
# from client.analyze import Analyze
# from client.generate import Generate


def run_tests_with_config():
    config = Config(disable_simulation=True)
    disabled_gen = Generate(config)
    keystrokes = disabled_gen.simulate_string("hello world")
    return keystrokes


def run_default_tests():
    gen = Generate()
    gen.disable()
    keystrokes = gen.simulate_string("hello world")
    return keystrokes


def run_tests():
    keystrokes_1 = run_tests_with_config()
    keystrokes_2 = run_default_tests()
    assert keystrokes_1 == keystrokes_2
    print("Tests passed.")


if __name__ == "__main__":
    run_tests()
