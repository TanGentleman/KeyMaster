from classes.configuration import Config
print("The logger, parser, and generator classes aliased kl, kp, and kg.")


def KeyLogger():
    return Config().KeyLogger()


def KeyParser():
    return Config().KeyParser()


def KeyGenerator():
    return Config().KeyGenerator()


kl = KeyLogger
kp = KeyParser
kg = KeyGenerator

print("Example: `parser = KeyParser()` or `gen = kg()`")
