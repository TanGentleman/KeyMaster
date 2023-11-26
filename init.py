print("Use logger, parser, and simulator classes as kl, kp, and ks.")
from classes.key_collector import KeyLogger
from classes.key_analyzer import KeyParser
from classes.key_generator import KeySimulator

kl = KeyLogger
kp = KeyParser
ks = KeySimulator

print("Example: `sim = ks()`")
