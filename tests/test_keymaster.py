import json
import sys

import pytest
from pynput.keyboard import Key, KeyCode

import classes.key_collector as key_collector
from classes.key_analyzer import KeyParser
from classes.key_collector import KeyLogger
from classes.key_generator import KeyGenerator
from client.configurate import Config
from client.generate import Generate
import utils.helpers
from utils.validation import Keystroke, KeystrokeList


def keystrokes(*pairs):
    return KeystrokeList([Keystroke(key, time) for key, time in pairs])


# Generate


@pytest.mark.parametrize("text", ["Hello, world!", "tabs\tand\nnewlines", "it's 100% ok"])
def test_generated_keystrokes_round_trip(text):
    ks = KeyGenerator(disable=True).keystrokes_from_string(text)
    assert ks.to_string() == text
    assert ks.validate(text)
    assert ks[0].time is None
    assert all(k.time > 0 for k in ks[1:])


def test_generator_filters_unicode_and_newlines():
    assert KeyGenerator(allow_unicode=False).keystrokes_from_string("café").to_string() == "caf"
    assert KeyGenerator(allow_newlines=False).keystrokes_from_string("a\nb").to_string() == "ab"


def test_stop_key_ends_generation():
    ks = KeyGenerator().keystrokes_from_string("ab*cd")
    assert [k.key for k in ks] == ["'a'", "'b'", "STOP"]


def test_max_words():
    ks = KeyGenerator(max_words=2).keystrokes_from_string("one two three four")
    assert ks.to_string() == "one two "


# Simulate (fake keyboard)


def test_simulation_taps_each_key(keyboard):
    ks = KeyGenerator().keystrokes_from_string("Hi there\n")
    KeyGenerator().simulate_keystrokes(ks)
    assert keyboard.taps == ["H", "i", Key.space, "t", "h", "e", "r", "e", Key.enter]


def test_simulation_divides_delays_by_speed(keyboard):
    ks = keystrokes(("'a'", None), ("'b'", 0.3), ("'c'", 0.6))
    KeyGenerator(speed_multiplier=3).simulate_keystrokes(ks)
    assert keyboard.sleeps == pytest.approx([0.1, 0.2])


def test_simulation_skips_banned_keys_and_backspaces(keyboard):
    ks = keystrokes(("'a'", None), ("'x'", 0.1), ("Key.backspace", 0.1), ("'b'", 0.1))
    KeyGenerator(banned_keys=["x"]).simulate_keystrokes(ks)
    assert keyboard.taps == ["a", Key.backspace, "b"]


def test_disabled_simulation_types_nothing(keyboard):
    assert Generate(Config(disable=True)).simulate_string("hello").to_string() == "hello"
    gen = Generate()
    gen.disable()
    gen.simulate_string("hello")
    assert keyboard.taps == []


# Collect (recorded events, no listener)


def press(logger, *keys):
    for key in keys:
        logger.on_press(key)
        logger.on_release(key)


def test_collector_records_typed_text(monkeypatch):
    logger = KeyLogger(filename=None)
    clock = iter([0.5, 0.75, 1.0, 1.25, 1.5])
    monkeypatch.setattr(key_collector, "perf_counter", lambda: next(clock))
    press(logger, KeyCode.from_char("h"), KeyCode.from_char("x"), Key.backspace,
          KeyCode.from_char("i"), Key.space)
    assert logger.typed_string == "hi "
    assert logger.keystrokes.to_string() == "hi "
    assert [k.time for k in logger.keystrokes] == [None, 0.25, 0.25, 0.25, 0.25]


def test_collector_stops_on_stop_key_and_esc():
    logger = KeyLogger(filename=None)
    with pytest.raises(KeyboardInterrupt):
        logger.on_release(KeyCode.from_char("*"))
    with pytest.raises(KeyboardInterrupt):
        logger.on_press(Key.esc)


def test_collector_ignores_banned_keys():
    logger = KeyLogger(filename=None, banned_keys=["q"])
    press(logger, KeyCode.from_char("q"), KeyCode.from_char("a"))
    assert logger.typed_string == "a"


def test_save_and_reload_log(log_dir):
    path = str(log_dir / "mine.json")
    ks = KeyGenerator().keystrokes_from_string("hello world")
    for _ in range(2):
        logger = KeyLogger(filename=path)
        assert logger.set_internal_log(ks, "hello world")
        assert logger.save_log()
    saved = json.loads((log_dir / "mine.json").read_text())
    assert [log["id"] for log in saved] == ["A000", "A001"]
    parser = KeyParser(filename=path)
    assert parser.get_strings() == ["hello world", "hello world"]
    assert parser.get_keystrokes("A001").to_string() == "hello world"


def test_first_save_creates_the_log_dir(log_dir, monkeypatch):
    fresh = log_dir / "logs"
    monkeypatch.setattr(utils.helpers, "LOG_DIR", str(fresh))
    monkeypatch.setattr(utils.helpers, "ABSOLUTE_REG_FILEPATH", str(fresh / "keystrokes.json"))
    logger = KeyLogger(filename="REG")
    assert logger.set_internal_log(KeyGenerator().keystrokes_from_string("hi there"), "hi there")
    assert logger.save_log()
    assert json.loads((fresh / "keystrokes.json").read_text())[0]["string"] == "hi there"
    assert (fresh / "LOG_ID.txt").read_text() == "A001"


# Analyze


def parser_without_logs():
    return KeyParser(filename=None, preload=False)


def test_wpm_and_delay_stats():
    ks = keystrokes(("'a'", None), ("'b'", 0.2), ("'c'", 0.2), ("'d'", 0.2), ("'e'", 0.2))
    parser = parser_without_logs()
    # 4 timed keys in 0.8 s = 300 chars/min = 60 wpm
    assert parser.wpm(ks) == 60.0
    assert parser.get_average_delay(ks) == 0.2
    assert parser.get_std_deviation(ks) == 0.0


def test_outliers_are_excluded_by_default():
    ks = keystrokes(("'a'", None), ("'b'", 0.2), ("'c'", 5.0))
    parser = parser_without_logs()
    assert parser.get_only_times(ks) == [0.2]
    assert parser.get_only_times(ks, exclude_outliers=False) == [0.2, 5.0]


def test_stats_use_the_given_keystrokes_not_the_loaded_logs(log_dir):
    path = str(log_dir / "slow.json")
    logger = KeyLogger(filename=path)
    slow = keystrokes(("'a'", None), ("'b'", 1.0), ("'c'", 1.0))
    logger.set_internal_log(slow, "abc")
    logger.save_log()
    parser = KeyParser(filename=path)
    fast = keystrokes(("'x'", None), ("'y'", 0.1), ("'z'", 0.1))
    assert parser.get_stats(fast) == {
        "keystroke_count": 3,
        "average_delay": 0.1,
        "std_deviation": 0.0,
        "highest_keystroke_time": 0.1,
        "wpm": 120.0,
    }
    assert parser.wpm() == 12.0


def test_highest_keystroke_time_per_log():
    parser = parser_without_logs()
    parser.logs = [
        {"id": "A000", "string": "ab", "keystrokes": keystrokes(("'a'", None), ("'b'", 0.4))},
        {"id": "A001", "string": "cd", "keystrokes": keystrokes(("'c'", None), ("'d'", 0.9))},
    ]
    assert parser.get_highest_keystroke_times() == [("A000", 0.4), ("A001", 0.9)]


def test_char_times_map():
    ks = keystrokes(("'a'", None), ("'b'", 0.2), ("Key.space", 0.1), ("'b'", 0.4))
    assert parser_without_logs().map_chars_to_times(ks) == pytest.approx({"b": 0.3, "Space": 0.1})


def test_caps_lock_swaps_case():
    ks = keystrokes(("'a'", None), ("Key.caps_lock", 0.1), ("'b'", 0.1),
                    ("Key.caps_lock", 0.1), ("'c'", 0.1))
    ks.process_caps_lock()
    assert ks.to_string() == "aBc"


# CLI


def test_cli_dry_run(monkeypatch, capsys, keyboard):
    from scripts import cli

    monkeypatch.setattr(sys, "argv", ["cli", "--disable", "--no-log", "-s", "hello"])
    cli.main()
    assert "Simulation disabled." in capsys.readouterr().out
    assert keyboard.taps == []


def test_cli_stats(monkeypatch, capsys):
    from scripts import cli

    monkeypatch.setattr(sys, "argv", ["cli", "--stats"])
    cli.main()
    assert "No recorded keystrokes yet" in capsys.readouterr().out

    ks = keystrokes(("'h'", None), ("'i'", 0.2), (" ", 0.2), ("'y'", 0.2), ("'o'", 0.2))
    logger = KeyLogger(filename="REG")
    assert logger.set_internal_log(ks, "hi yo")
    assert logger.save_log()
    cli.main()
    out = capsys.readouterr().out
    assert "Logs: 1" in out
    assert "Keystrokes: 5" in out
    assert "WPM: 60.0" in out


# Plots


@pytest.fixture
def plots(monkeypatch, tmp_path):
    """Draw with Agg into tmp_path; plt.show records the figure instead of opening a window."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    shown = []
    monkeypatch.setattr(plt, "show", lambda *a, **k: shown.append(plt.gcf()))
    monkeypatch.chdir(tmp_path)
    yield shown
    plt.close("all")


@pytest.mark.filterwarnings("error::matplotlib.MatplotlibDeprecationWarning")
def test_bar_plot_saves_one_bar_per_key(plots, tmp_path):
    from client.analyze import Analyze

    ks = keystrokes(("'a'", None), ("'b'", 0.2), ("Key.space", 0.1), ("'b'", 0.4))
    Analyze(Config(logging=False)).visualize(save_file=True, keystrokes=ks)
    (fig,) = plots
    (ax,) = fig.axes
    assert [t.get_text() for t in ax.get_xticklabels()] == ["b", "Space"]
    assert [round(p.get_height(), 4) for p in ax.patches] == [0.3, 0.1]
    assert (tmp_path / "keystroke_times.png").stat().st_size > 0


@pytest.mark.filterwarnings("error::matplotlib.MatplotlibDeprecationWarning")
def test_box_plot_is_horizontal(plots):
    from client.analyze import Analyze

    ks = keystrokes(("'a'", None), ("'b'", 0.2), ("'c'", 0.4), ("'d'", 5.0))
    Analyze(Config(logging=False)).visualize(mode="box", keystrokes=ks)
    (fig,) = plots
    (ax,) = fig.axes
    # The 5.0 s outlier is excluded, so the box spans 0.2..0.4 along x.
    assert ax.get_xlabel() == "Keystroke Time (s)"
    assert ax.get_xlim()[1] < 1
