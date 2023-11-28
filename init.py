print("Use logger, parser, and generator classes as kl, kp, and kg.")
from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeyGenerator

kl = KeyLogger
kp = KeyParser
kg = KeyGenerator

print("Example: `gen = kg()`")
