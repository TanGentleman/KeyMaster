from pynput.keyboard import Controller, Key
import time
import numpy as np
# Sample keystrokes
# keystrokes = [
#     ('h', 0.1),
#     ('i', 0.1),
#     (Key.space, 0.2),
#     ('t', 0.1),
#     ('h', 0.1),
#     ('e', 0.1),
#     ('r', 0.1),
#     ('e', 0.1),
# ]
# simulate_keystrokes(keystrokes)
# sample_string = """causa provincia empiezo banana pero derecho en para
# polvo alguien los platos del para todos los alamos
# natural es casa juicio español de estadia estado imagen
# de los alas en unas derrota derecho manita orden
# olmos pepino ordenanza alzas algo estos estoy de las
# esa mis darle al los miembros más activos en las
# porque al no estar en pericia control de la lista de
# """
sample_string = """Today, there are some endangered animals on Earth. It means that we can find only a few of them around us. Some examples are whales, pandas, tigers and Asian elephants. Humans destroy the natural homes of the animals in the forests, lakes, and plains. When the number of people on Earth increases, they need more place for living. They cut down trees and destroy lakes. They make homes and roads instead. Then the animals won't have a place to live. They will die out. The Iranian cheetah is among these animals. This wild animal lives only in the plains of Iran. Now there are only a few Iranian cheetahs alive. If people take care of them, there is hope for this beautiful animal to live. Recently, families pay more attention to nature, students learn about saving wildlife, and some hunters don't go hunting anymore. In this way, the number of cheetahs is going to increase in the future."""
def words_from_string(string: str):
    return string.split()


def simulate_keystrokes(words, delay_mean, delay_standard_deviation):
    keyboard = Controller()
    special_keys = {
        '\n': Key.enter,
        '\t': Key.tab,
        ' ': Key.space,
        # Add more special keys here
    }

    for word in words:
        for char in word:
            delay = np.random.normal(delay_mean, delay_standard_deviation)
            try:
                time.sleep(delay)
                if char in special_keys:
                    keyboard.press(special_keys[char])
                    keyboard.release(special_keys[char])
                else:
                    keyboard.type(char)
            except Exception as e:
                print(f"An error occurred while typing the character: {e}")
                continue  # Continue with the next character

        # Add a random delay after each word
        delay = np.random.normal(delay_mean/1.5, delay_standard_deviation)
        try:
            time.sleep(delay)
            keyboard.type(' ')
        except Exception as e:
            print(f"An error occurred while typing the space: {e}")
            continue  # Continue with the next word

# words = ["Hello"]*8
words = words_from_string(sample_string)
simulate_keystrokes(words, delay_mean=0.09, delay_standard_deviation=0.02)
