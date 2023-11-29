import unittest
from utils.validation import KeystrokeEncoder, KeystrokeList, Keystroke


class TestKeystrokeEncoder(unittest.TestCase):
    def setUp(self):
        self.keystroke = Keystroke('a', 0.0)
        self.keystroke2 = Keystroke('b', 0.0)
        self.keystrokes = KeystrokeList([self.keystroke, self.keystroke2])
        self.log_dict = {
            'id': 1,
            'string': 'test string',
            'keystrokes': [self.keystroke, self.keystroke2]
        }

    def test_encode(self):
        encoder = KeystrokeEncoder()
        encoded_keystroke = encoder.default(self.keystroke)
        encoded_keystrokes = encoder.default(self.keystrokes)
        encoded_log = encoder.default(self.log_dict)

        self.assertEqual(encoded_keystroke, ['a', 0.0])
        self.assertEqual(encoded_keystrokes, [['a', 0.0], ['b', 0.0]])
        self.assertEqual(encoded_log, {
            'id': 1,
            'string': 'test string',
            'keystrokes': [['a', 0.0], ['b', 0.0]]
        })


def run_encoder_test():
    unittest.main()


if __name__ == '__main__':
    run_encoder_test()
