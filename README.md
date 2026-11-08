# KeyMaster

Record your own typing, measure it (WPM, per-key delays, plots), and replay text as realistic keystrokes.
A small Python toolkit built on [pynput](https://pynput.readthedocs.io/).

## Install

```bash
git clone https://github.com/TanGentleman/KeyMaster && cd KeyMaster
uv sync --all-extras   # Python 3.10+, installs pynput, matplotlib and pyperclip
```

Without uv: `pip install pynput matplotlib pyperclip`.

## Use

```bash
uv run python -m scripts.cli -d -n -s "hello world"   # dry run: no typing, no log
uv run python -m scripts.cli -s "hello world"         # types it into the focused window after 3 s
uv run python -m scripts.cli -c                       # types your clipboard
uv run python -m scripts.cli -l -d                    # records your typing (stop with Esc or *)
```

Recorded and simulated runs are appended to `logs/keystrokes.json` and `logs/simulated-keystrokes.json`.
Pass `-n` to skip logging. Without `-d`, `-l` replays what you typed when you stop.

From Python:

```python
from client.analyze import Analyze
from client.generate import Generate
from client.configurate import Config

ks = Generate(Config(disable=True)).simulate_string("The quick brown fox")
print(Analyze(Config(logging=False)).get_stats(ks))
# {'keystroke_count': 19, 'average_delay': 0.04, 'std_deviation': 0.01, 'highest_keystroke_time': 0.08, 'wpm': 283.1}

Analyze().visualize()  # bar chart of your average delay per key, from logs/keystrokes.json
```

Recording and typing need OS permission: on macOS, allow your terminal under
Privacy & Security > Accessibility (and Input Monitoring for `-l`). On Linux, pynput needs an X server,
and its `evdev` dependency builds from source, so a system Python needs its headers (`python3-dev`).

## Test

```bash
uv run pytest            # Linux without a display: xvfb-run -a uv run pytest
```

The tests fake the keyboard and never type or listen.

## License

MIT
