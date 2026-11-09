"""Pins down the behaviour that IMPLEMENTATION.md's "How it works" section describes."""
import random
import re
import statistics
from pathlib import Path

import pytest
from pynput.keyboard import Key, KeyCode

import classes.key_collector as key_collector
import classes.key_generator as key_generator
from classes.key_collector import KeyLogger
from classes.key_generator import KeyGenerator
from utils.validation import Keystroke, KeystrokeList

DOC = Path(__file__).resolve().parent.parent / "IMPLEMENTATION.md"


def keystrokes(*pairs):
    return KeystrokeList([Keystroke(key, time) for key, time in pairs])


# Timing model


@pytest.mark.parametrize("speed, mean, std", [(1, 0.12, 0.04), (3, 0.042, 0.012)])
def test_generated_delays_are_normal_over_speed(speed, mean, std):
    random.seed(0)
    gen = KeyGenerator(speed_multiplier=speed)
    delays = [gen.calculate_delay() for _ in range(20000)]
    assert statistics.mean(delays) == pytest.approx(mean, abs=0.002)
    assert statistics.stdev(delays) == pytest.approx(std, abs=0.002)


@pytest.mark.parametrize("drawn, delay", [(0.05, 0.05), (0.01, 0.031), (-0.02, 0.028)])
def test_delays_below_the_floor_are_lifted(monkeypatch, drawn, delay):
    monkeypatch.setattr(key_generator, "normalvariate", lambda mu, sigma: drawn)
    assert KeyGenerator().calculate_delay() == pytest.approx(delay)


def test_speed_is_capped_at_ten():
    gen = KeyGenerator()
    gen.set_speed(50)
    assert gen.speed_multiplier == 10
    with pytest.raises(ValueError):
        gen.set_speed(-1)


def test_typing_divides_generated_delays_by_speed_again(keyboard):
    gen = KeyGenerator(speed_multiplier=3)
    ks = gen.keystrokes_from_string("abcd")
    gen.simulate_keystrokes(ks)
    assert keyboard.sleeps == pytest.approx([k.time / 3 for k in ks[1:]])


def test_typing_caps_long_pauses(keyboard):
    KeyGenerator(speed_multiplier=1).simulate_keystrokes(keystrokes(("'a'", None), ("'b'", 6.0)))
    assert keyboard.sleeps == pytest.approx([3.006])


def test_typing_stops_when_max_duration_elapses(monkeypatch, keyboard):
    class ElapsedTimer:
        def __init__(self, seconds, callback):
            self.callback = callback

        def start(self):
            self.callback()

        def is_alive(self):
            return False

    monkeypatch.setattr(key_generator, "Timer", ElapsedTimer)
    KeyGenerator().simulate_keystrokes(KeyGenerator().keystrokes_from_string("hello"))
    assert keyboard.taps == []


# Shift insertion (off by default)


def test_shift_insertion_is_off_by_default():
    assert [k.key for k in KeyGenerator().keystrokes_from_string("Hi")] == ["'H'", "'i'"]


def test_one_shift_covers_a_run_of_shifted_chars(monkeypatch, keyboard):
    monkeypatch.setattr(key_generator, "GENERATE_SHIFTS", True)
    gen = KeyGenerator()
    ks = gen.keystrokes_from_string("Hi ##!")
    assert [k.key for k in ks] == [
        "Key.shift", "'H'", "'i'", "Key.space", "Key.shift", "'#'", "'#'", "'!'"]
    assert ks[0].time is None and ks[4].time == pytest.approx(2 / 9, abs=1e-4)
    assert ks.to_string() == "Hi ##!"
    gen.simulate_keystrokes(ks)
    # pynput's tap() shifts by itself, so the Shift keystrokes only add their delay.
    assert keyboard.taps == ["H", "i", Key.space, "#", "#", "!"]
    assert len(keyboard.sleeps) == len(ks) - 1


# Recording


def record(monkeypatch, logger, events):
    clock = [0.0]
    monkeypatch.setattr(key_collector, "perf_counter", lambda: clock[0])
    logger.reset()
    for key, delay in events:
        clock[0] += delay
        logger.on_press(key)
        logger.on_release(key)


def test_shift_is_not_logged_and_its_time_joins_the_next_key(monkeypatch):
    logger = KeyLogger(filename=None)
    record(monkeypatch, logger, [(KeyCode.from_char("a"), 0), (Key.shift, 0.1), (KeyCode.from_char("B"), 0.05)])
    assert [(k.key, k.time) for k in logger.keystrokes] == [("'a'", None), ("'B'", 0.15)]


def test_long_pauses_are_logged_as_three_seconds_plus_a_trace(monkeypatch):
    logger = KeyLogger(filename=None)
    record(monkeypatch, logger, [(KeyCode.from_char("a"), 0), (KeyCode.from_char("b"), 42.0)])
    assert logger.keystrokes[1].time == 3.042


def test_default_banned_key_is_dropped(monkeypatch):
    logger = KeyLogger(filename=None)
    record(monkeypatch, logger, [(KeyCode.from_char("a"), 0), (KeyCode.from_char("√"), 0.1),
                                 (KeyCode.from_char("b"), 0.1)])
    assert logger.typed_string == "ab"
    assert logger.keystrokes[1].time == pytest.approx(0.2)
    assert KeyGenerator().keystrokes_from_string("a√b").to_string() == "ab"


def test_unhandled_keys_are_ignored(monkeypatch):
    logger = KeyLogger(filename=None)
    record(monkeypatch, logger, [(KeyCode.from_char("a"), 0), (Key.left, 0.1), (Key.cmd, 0.1)])
    assert logger.typed_string == "a" and len(logger.keystrokes) == 1


def test_stop_key_is_logged_as_stop_code_and_ends_recording(monkeypatch):
    logger = KeyLogger(filename=None)
    with pytest.raises(KeyboardInterrupt):
        record(monkeypatch, logger, [(KeyCode.from_char("a"), 0), (KeyCode.from_char("*"), 0.1)])
    assert [k.key for k in logger.keystrokes] == ["'a'", "STOP"]


def test_recording_stops_at_the_word_limit(monkeypatch):
    logger = KeyLogger(filename=None)
    words = [(KeyCode.from_char("w"), 0.1), (Key.space, 0.1)] * key_collector.LISTENER_WORD_LIMIT
    with pytest.raises(KeyboardInterrupt):
        record(monkeypatch, logger, words)
    assert logger.word_count == 50 == len(logger.keystrokes) / 2


def test_a_log_is_saved_only_if_its_keystrokes_rebuild_the_text():
    logger = KeyLogger(filename=None)
    ks = keystrokes(("'a'", None), ("'x'", 0.1), ("Key.backspace", 0.1), ("'b'", 0.1))
    assert logger.set_internal_log(ks, "ab")
    assert not logger.set_internal_log(ks, "axb")


# The demo in IMPLEMENTATION.md


def test_readme_demo_output_matches(capsys):
    from scripts import demo

    demo.walkthrough()
    out = capsys.readouterr().out
    block = re.search(r"python -m scripts\.demo\n```\n\n```text\n(.*?)```", DOC.read_text(), re.S)
    assert block, "IMPLEMENTATION.md demo block not found"
    assert block.group(1) == out


def test_demo_chart(tmp_path):
    from scripts import demo

    demo.save_chart(str(tmp_path / "timing.png"), samples=200)
    assert (tmp_path / "timing.png").stat().st_size > 0
