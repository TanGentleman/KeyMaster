import copy
import unittest
from utils.validation import KeystrokeEncoder, KeystrokeDecoder, KeystrokeList, Keystroke
from json import loads as json_loads
from json import dumps as json_dumps


class TestKeystrokeEncoder(unittest.TestCase):
    def setUp(self):
        self.keystroke = Keystroke('a', None)
        self.keystroke2 = Keystroke('b', 0.1)
        self.keystrokes = KeystrokeList([self.keystroke, self.keystroke2])
        self.log_dict = {
            'id': '1',
            'string': 'ab',
            'keystrokes': self.keystrokes
        }
        self.log_dict2 = copy.deepcopy(self.log_dict)
        self.log_dict2['id'] = '2'
        self.list_of_logs = [self.log_dict, self.log_dict2]

    def test_encode(self):
        encoder = KeystrokeEncoder()
        encoded_keystroke = encoder.default(self.keystroke)
        encoded_keystrokes = encoder.default(self.keystrokes)
        encoded_log = encoder.default(self.log_dict)
        encoded_log_list = encoder.default(self.list_of_logs)

        self.assertEqual(encoded_keystroke, ['a', None])
        self.assertEqual(encoded_keystrokes, [['a', None], ['b', 0.1]])
        self.assertEqual(encoded_log, {
            'id': '1',
            'string': 'ab',
            'keystrokes': [['a', None], ['b', 0.1]]
        })
        self.assertEqual(encoded_log_list, [
            {
                'id': '1',
                'string': 'ab',
                'keystrokes': [['a', None], ['b', 0.1]]
            },
            {
                'id': '2',
                'string': 'ab',
                'keystrokes': [['a', None], ['b', 0.1]]
            }
        ])


class TestKeystrokeDecoder(unittest.TestCase):
    def setUp(self):
        self.keystroke = Keystroke('a', None)
        self.keystroke2 = Keystroke('b', 0.1)
        self.keystroke_list = KeystrokeList([self.keystroke, self.keystroke2])
        self.log_dict = {
            'id': '1',
            'string': 'ab',
            'keystrokes': self.keystroke_list
        }
        self.log_dict2 = copy.deepcopy(self.log_dict)
        self.log_dict2['id'] = '2'
        self.list_of_logs = [self.log_dict, self.log_dict2]

    def test_decode(self):
        # Test decoding a string like stored in a log file
        json_data = '[{"id": "29cdad60-162f-4f68-adb9-08bfc674e5b2", "string": "*", "keystrokes": [["Key.shift", null], ["STOP", 0.5334]]}]'
        decoded_data = json_loads(json_data, cls=KeystrokeDecoder)
        assert isinstance(decoded_data[0]['keystrokes'], KeystrokeList)

        # Test decoding a Log object
        encoder = KeystrokeEncoder()
        encoded_log = encoder.default(self.log_dict)
        encoded_log_list = encoder.default(self.list_of_logs)

        json_encoded_log = json_dumps(encoded_log)
        json_encoded_log_list = json_dumps(encoded_log_list)

        decoder = KeystrokeDecoder()
        decoded_log = decoder.decode(json_encoded_log)
        decoded_log_list = decoder.decode(json_encoded_log_list)

        self.assertEqual(decoded_log, self.log_dict)
        self.assertEqual(decoded_log_list, self.list_of_logs)

        print(decoded_data)
        print(json_encoded_log)
        print(json_encoded_log_list)


def run_encoder_test():
    unittest.main()


if __name__ == '__main__':
    run_encoder_test()
