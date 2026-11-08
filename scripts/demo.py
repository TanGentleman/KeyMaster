"""Run the record -> save -> analyze -> generate pipeline on synthetic keystrokes.

Nothing is typed, nothing is listened to and nothing is written under logs/.
The "typist" is a fixed script of key events with made-up delays.

    python -m scripts.demo                       # print the walkthrough
    python -m scripts.demo --chart docs/timing.png
"""
import argparse
import json
import logging
import random

from pynput.keyboard import Key, KeyCode

import classes.key_collector as key_collector
from classes.key_analyzer import KeyParser
from classes.key_collector import KeyLogger
from classes.key_generator import KeyGenerator
from utils.settings import MIN_DELAY, SIM_DELAY_MEAN, SIM_DELAY_STD_DEV
from utils.validation import KeystrokeEncoder

SEED = 7
TEXT = "The quick brown fox jumps over the lazy dog."

# (key, seconds since the previous event). Shift is pressed but not logged,
# "thr" gets a backspace, and a 5 s pause precedes the final "!".
SCRIPTED_TYPING = [
    (Key.shift, 0.0), (KeyCode.from_char("H"), 0.06), (KeyCode.from_char("i"), 0.14),
    (Key.space, 0.11), (KeyCode.from_char("t"), 0.19), (KeyCode.from_char("h"), 0.12),
    (KeyCode.from_char("r"), 0.09), (Key.backspace, 0.31), (KeyCode.from_char("e"), 0.16),
    (KeyCode.from_char("r"), 0.13), (KeyCode.from_char("e"), 0.1), (Key.shift, 5.0),
    (KeyCode.from_char("!"), 0.08),
]


def record_scripted_typing() -> KeyLogger:
    """Feed SCRIPTED_TYPING through the real collector with a fake clock."""
    clock = [0.0]
    real_clock = key_collector.perf_counter
    key_collector.perf_counter = lambda: clock[0]
    try:
        logger = KeyLogger(filename=None)
        for key, delay in SCRIPTED_TYPING:
            clock[0] += delay
            logger.on_press(key)
            logger.on_release(key)
    finally:
        key_collector.perf_counter = real_clock
    return logger


def stats_line(parser: KeyParser, keystrokes) -> str:
    s = parser.get_stats(keystrokes)
    return (f"{s['keystroke_count']} keystrokes, {s['wpm']} WPM, "
            f"mean {s['average_delay']} s, std {s['std_deviation']} s")


def walkthrough() -> None:
    parser = KeyParser(filename=None, preload=False)

    logger = record_scripted_typing()
    log = logger.create_log("A000")
    print("1. Recorded (scripted events through KeyLogger):")
    print(f"   typed {logger.typed_string!r}")
    print("   saved as " + json.dumps(log, cls=KeystrokeEncoder))
    pause = logger.keystrokes[-1].time
    print(f"   {stats_line(parser, logger.keystrokes)} (the {pause} s pause is left out)")

    random.seed(SEED)
    print("2. Generated from a string (nothing typed):")
    for speed in (1, 3):
        ks = KeyGenerator(speed_multiplier=speed, disable=True).keystrokes_from_string(TEXT)
        assert ks.validate(TEXT)
        print(f"   speed {speed}: {stats_line(parser, ks)}")


def save_chart(path: str, samples: int = 5000) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    random.seed(SEED)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for speed, color in ((1, "tab:blue"), (3, "tab:orange")):
        gen = KeyGenerator(speed_multiplier=speed, disable=True)
        delays = [gen.calculate_delay() * 1000 for _ in range(samples)]
        ax.hist(delays, bins=80, range=(0, 260), color=color, alpha=0.6,
                label=f"speed {speed}: normal({SIM_DELAY_MEAN * 1000 / speed:.0f} ms, "
                      f"{SIM_DELAY_STD_DEV * 1000 / speed:.0f} ms)")
    ax.axvline(MIN_DELAY * 1000, color="black", linestyle="--", linewidth=1)
    ax.annotate(f"{MIN_DELAY * 1000:.0f} ms floor", (MIN_DELAY * 1000, ax.get_ylim()[1] * 0.9),
                xytext=(-8, 0), textcoords="offset points", ha="right")
    ax.set_xlabel("Delay before each generated keystroke (ms)")
    ax.set_ylabel(f"Count of {samples}")
    ax.set_title("KeyGenerator timing model")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=100, metadata={"Software": None})
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--chart", metavar="PNG", help="also save the timing histogram here")
    args = parser.parse_args()
    logging.getLogger().setLevel(logging.WARNING)
    walkthrough()
    if args.chart:
        save_chart(args.chart)
        print(f"Saved {args.chart}")


if __name__ == "__main__":
    main()
